# Bounded 32-bit Windows OleRun OS-boundary measurement; no game process is launched.
# Source API contracts:
# https://learn.microsoft.com/en-us/windows/win32/api/ole2/nf-ole2-olerun
# https://learn.microsoft.com/en-us/windows/win32/api/unknwn/nf-unknwn-iunknown-queryinterface(refiid_void)
# https://learn.microsoft.com/en-us/windows/win32/api/combaseapi/nf-combaseapi-coinitializeex
param([string]$OutputPath = '')
$ErrorActionPreference = 'Stop'
if ([IntPtr]::Size -ne 4) {
    throw 'Run this probe using the 32-bit SysWOW64 Windows PowerShell executable.'
}
$source = @'
using System;
using System.Collections.Generic;
using System.Diagnostics;
using System.IO;
using System.Runtime.InteropServices;
using System.Security.Cryptography;
using System.Threading;

public static class YrOleRunProbe {
    [UnmanagedFunctionPointer(CallingConvention.Winapi)]
    private delegate int QueryInterface(IntPtr self, IntPtr iid, IntPtr output);
    [UnmanagedFunctionPointer(CallingConvention.Winapi)]
    private delegate uint RefCount(IntPtr self);
    [DllImport("ole32.dll", ExactSpelling = true, PreserveSig = true)]
    private static extern int OleRun(IntPtr unknown);
    [DllImport("ole32.dll", ExactSpelling = true, PreserveSig = true)]
    private static extern int CoInitializeEx(IntPtr reserved, uint flags);
    [DllImport("ole32.dll", ExactSpelling = true, PreserveSig = true)]
    private static extern int OleInitialize(IntPtr reserved);
    [DllImport("ole32.dll", ExactSpelling = true)]
    private static extern void OleUninitialize();
    [DllImport("ole32.dll", ExactSpelling = true)]
    private static extern void CoUninitialize();
    private static readonly Guid Unknown = new Guid("00000000-0000-0000-C000-000000000046");
    private static readonly Guid Runnable = new Guid("00000126-0000-0000-C000-000000000046");
    private static string Hr(int value) { return "0x" + unchecked((uint)value).ToString("x8"); }
    private static string Pointer(IntPtr value) { return "0x" + value.ToInt64().ToString("x"); }
    public sealed class Call {
        public int Sequence;
        public string Method;
        public string Iid;
        public string Result;
        public uint Before;
        public uint After;
        public bool OutputNull;
    }
    public sealed class Measurement {
        public string Control;
        public string Apartment;
        public string InitializeHresult;
        public uint InitializeFlags;
        public string OleRunHresult;
        public List<string> OleInitializeHresults = new List<string>();
        public uint ReferencesBefore;
        public uint ReferencesAfter;
        public string UnknownQueryHresult;
        public string RunnableQueryHresult;
        public bool UnknownIdentityMatches;
        public bool RunnableOutputNull;
        public string ObjectPointer;
        public string VtablePointer;
        public string Error;
        public List<string> CallbackErrors = new List<string>();
        public List<Call> PreflightCalls = new List<Call>();
        public List<Call> OleRunCalls = new List<Call>();
    }
    public sealed class Module {
        public string Name;
        public string Path;
        public string ResolvedFilePath;
        public string LoadedPeMachine;
        public string FilePeMachine;
        public string Version;
        public string Sha256;
    }
    public sealed class Result {
        public int SchemaVersion = 1;
        public string TimestampUtc;
        public int PointerBytes;
        public string OsVersion;
        public string ClrVersion;
        public string ProcessPath;
        public List<Measurement> Measurements = new List<Measurement>();
        public List<Module> Modules = new List<Module>();
    }
    private static Measurement Measure(ApartmentState apartment, uint flags, int oleCalls) {
        Measurement result = new Measurement();
        result.Control = apartment.ToString() + (oleCalls == 0 ? "-CoInitializeEx" : "-OleInitialize-twice");
        result.Apartment = apartment.ToString();
        result.InitializeFlags = flags;
        Thread thread = new Thread(delegate() {
            IntPtr table = IntPtr.Zero, obj = IntPtr.Zero;
            QueryInterface query = null;
            RefCount add = null, release = null;
            bool initialized = false;
            int initializedOle = 0;
            uint refs = 1;
            List<Call> calls = result.PreflightCalls;
            try {
                int init = CoInitializeEx(IntPtr.Zero, flags);
                result.InitializeHresult = Hr(init);
                if (init < 0) throw new InvalidOperationException("CoInitializeEx failed: " + Hr(init));
                initialized = true;
                // Original CRT77B8A0 and WinMain6BC33C each pass NULL to
                // OleInitialize before factory registration; both ignore HR.
                for (int call = 0; call < oleCalls; call++) {
                    int ole = OleInitialize(IntPtr.Zero);
                    result.OleInitializeHresults.Add(Hr(ole));
                    if (ole < 0) throw new InvalidOperationException("OleInitialize failed: " + Hr(ole));
                    initializedOle++;
                }
                table = Marshal.AllocHGlobal(3 * IntPtr.Size);
                obj = Marshal.AllocHGlobal(IntPtr.Size);
                query = delegate(IntPtr self, IntPtr iid, IntPtr output) {
                    uint before = refs;
                    Guid value = Guid.Empty;
                    int hr;
                    try {
                        if (output == IntPtr.Zero) hr = unchecked((int)0x80004003);
                        else {
                            Marshal.WriteIntPtr(output, IntPtr.Zero);
                            value = (Guid)Marshal.PtrToStructure(iid, typeof(Guid));
                            if (self != obj) throw new InvalidOperationException("Unexpected this pointer");
                            if (value == Unknown) { refs++; Marshal.WriteIntPtr(output, obj); hr = 0; }
                            else hr = unchecked((int)0x80004002);
                        }
                    } catch (Exception ex) {
                        result.CallbackErrors.Add(ex.ToString());
                        hr = unchecked((int)0x80004005);
                    }
                    calls.Add(new Call { Sequence = calls.Count, Method = "QueryInterface", Iid = value.ToString("D"), Result = Hr(hr), Before = before, After = refs, OutputNull = output == IntPtr.Zero || Marshal.ReadIntPtr(output) == IntPtr.Zero });
                    return hr;
                };
                add = delegate(IntPtr self) {
                    uint before = refs;
                    if (self != obj) result.CallbackErrors.Add("AddRef this mismatch");
                    refs++;
                    calls.Add(new Call { Sequence = calls.Count, Method = "AddRef", Before = before, After = refs });
                    return refs;
                };
                release = delegate(IntPtr self) {
                    uint before = refs;
                    if (self != obj || refs == 0) result.CallbackErrors.Add("Release invalid this/refcount");
                    else refs--;
                    calls.Add(new Call { Sequence = calls.Count, Method = "Release", Before = before, After = refs });
                    return refs;
                };
                Marshal.WriteIntPtr(table, 0, Marshal.GetFunctionPointerForDelegate(query));
                Marshal.WriteIntPtr(table, IntPtr.Size, Marshal.GetFunctionPointerForDelegate(add));
                Marshal.WriteIntPtr(table, 2 * IntPtr.Size, Marshal.GetFunctionPointerForDelegate(release));
                Marshal.WriteIntPtr(obj, table);
                result.ObjectPointer = Pointer(obj);
                result.VtablePointer = Pointer(table);
                IntPtr iidBuffer = Marshal.AllocHGlobal(16), outputBuffer = Marshal.AllocHGlobal(IntPtr.Size);
                try {
                    Marshal.StructureToPtr(Unknown, iidBuffer, false);
                    result.UnknownQueryHresult = Hr(query(obj, iidBuffer, outputBuffer));
                    result.UnknownIdentityMatches = Marshal.ReadIntPtr(outputBuffer) == obj;
                    release(obj);
                    Marshal.StructureToPtr(Runnable, iidBuffer, false);
                    result.RunnableQueryHresult = Hr(query(obj, iidBuffer, outputBuffer));
                    result.RunnableOutputNull = Marshal.ReadIntPtr(outputBuffer) == IntPtr.Zero;
                } finally {
                    Marshal.FreeHGlobal(outputBuffer);
                    Marshal.FreeHGlobal(iidBuffer);
                }
                if (refs != 1 || !result.UnknownIdentityMatches || !result.RunnableOutputNull)
                    throw new InvalidOperationException("IUnknown preflight failed");
                calls = result.OleRunCalls;
                result.ReferencesBefore = refs;
                result.OleRunHresult = Hr(OleRun(obj));
                result.ReferencesAfter = refs;
                GC.KeepAlive(query); GC.KeepAlive(add); GC.KeepAlive(release);
            } catch (Exception ex) { result.Error = ex.ToString(); }
            finally {
                GC.KeepAlive(query); GC.KeepAlive(add); GC.KeepAlive(release);
                if (obj != IntPtr.Zero) Marshal.FreeHGlobal(obj);
                if (table != IntPtr.Zero) Marshal.FreeHGlobal(table);
                while (initializedOle-- > 0) OleUninitialize();
                if (initialized) CoUninitialize();
            }
        });
        thread.SetApartmentState(apartment);
        thread.Start();
        thread.Join();
        return result;
    }
    public static Result Run() {
        if (IntPtr.Size != 4) throw new InvalidOperationException("Expected x86 process");
        Result result = new Result();
        result.TimestampUtc = DateTime.UtcNow.ToString("o");
        result.PointerBytes = IntPtr.Size;
        result.OsVersion = Environment.OSVersion.VersionString;
        result.ClrVersion = Environment.Version.ToString();
        result.ProcessPath = Process.GetCurrentProcess().MainModule.FileName;
        result.Measurements.Add(Measure(ApartmentState.STA, 2, 0));
        result.Measurements.Add(Measure(ApartmentState.MTA, 0, 0));
        result.Measurements.Add(Measure(ApartmentState.STA, 2, 2));
        foreach (ProcessModule module in Process.GetCurrentProcess().Modules) {
            string name = module.ModuleName.ToLowerInvariant();
            if (name != "ole32.dll" && name != "combase.dll") continue;
            int peOffset = Marshal.ReadInt32(module.BaseAddress, 0x3c);
            if (Marshal.ReadInt32(module.BaseAddress, peOffset) != 0x00004550)
                throw new InvalidOperationException("Loaded module PE signature mismatch");
            ushort loadedMachine = unchecked((ushort)Marshal.ReadInt16(module.BaseAddress, peOffset + 4));
            // WOW64 module names may spell System32. Hash the explicit x86 file,
            // and compare its machine with the actual loaded module header.
            string resolved = module.FileName;
            string windows = Environment.GetFolderPath(Environment.SpecialFolder.Windows);
            string system32 = Path.Combine(windows, "System32") + Path.DirectorySeparatorChar;
            if (Environment.Is64BitOperatingSystem && resolved.StartsWith(system32, StringComparison.OrdinalIgnoreCase))
                resolved = Path.Combine(Path.Combine(windows, "SysWOW64"), Path.GetFileName(resolved));
            ushort fileMachine;
            using (FileStream stream = File.OpenRead(resolved)) using (BinaryReader reader = new BinaryReader(stream)) {
                stream.Position = 0x3c;
                int filePeOffset = reader.ReadInt32();
                stream.Position = filePeOffset;
                if (reader.ReadUInt32() != 0x00004550)
                    throw new InvalidOperationException("Module file PE signature mismatch");
                fileMachine = reader.ReadUInt16();
            }
            if (loadedMachine != 0x014c || fileMachine != loadedMachine)
                throw new InvalidOperationException("Loaded/file module is not matching x86");
            string hash;
            using (SHA256 sha = SHA256.Create()) using (FileStream stream = File.OpenRead(resolved))
                hash = BitConverter.ToString(sha.ComputeHash(stream)).Replace("-", "").ToLowerInvariant();
            result.Modules.Add(new Module { Name = name, Path = module.FileName, ResolvedFilePath = resolved,
                LoadedPeMachine = "0x" + loadedMachine.ToString("x4"), FilePeMachine = "0x" + fileMachine.ToString("x4"),
                Version = module.FileVersionInfo.FileVersion, Sha256 = hash });
        }
        return result;
    }
}
'@
Add-Type -TypeDefinition $source -Language CSharp
$result = [YrOleRunProbe]::Run()
$osRegistry = Get-ItemProperty -LiteralPath 'HKLM:\SOFTWARE\Microsoft\Windows NT\CurrentVersion'
$packet = [ordered]@{
    probe = 'windows-olerun-rejecting-irunnableobject'
    script_sha256 = (Get-FileHash -LiteralPath $PSCommandPath -Algorithm SHA256).Hash.ToLowerInvariant()
    csharp_source_sha256 = [BitConverter]::ToString([Security.Cryptography.SHA256]::Create().ComputeHash([Text.Encoding]::UTF8.GetBytes($source))).Replace('-', '').ToLowerInvariant()
    powershell_version = $PSVersionTable.PSVersion.ToString()
    os_64bit = [Environment]::Is64BitOperatingSystem
    process_64bit = [Environment]::Is64BitProcess
    computer_name = $env:COMPUTERNAME
    process_id = $PID
    os_registry = [ordered]@{ product_name = $osRegistry.ProductName; current_build = $osRegistry.CurrentBuild; ubr = $osRegistry.UBR; display_version = $osRegistry.DisplayVersion }
    measurement = $result
    coverage = 'Actual x86 Windows OleRun on manual valid IUnknown rejecting IRunnableObject. CoInitializeEx STA/MTA controls and STA with two literal OleInitialize(NULL) calls. No gamemd instructions or full startup execute here; CRT and WinMain call order/arguments have separate static native evidence.'
}
$json = $packet | ConvertTo-Json -Depth 12
if ($OutputPath) {
    [IO.File]::WriteAllText([IO.Path]::GetFullPath($OutputPath), $json + [Environment]::NewLine, (New-Object Text.UTF8Encoding $false))
}
[Console]::Out.WriteLine($json)
if (($result.Measurements | Where-Object { $_.Error -or $_.CallbackErrors.Count -gt 0 }).Count -gt 0) { exit 1 }
