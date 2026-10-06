"""Shared, bounded execution and reference-file workflow for retail YR oracles.

This is a CPU fixture runner, not a Windows loader or a game environment.
See tools/native_oracle.md for supported workflows and evidence limits.
Unicorn 2.1.4 API: https://github.com/unicorn-engine/unicorn/blob/2.1.4/include/unicorn/unicorn.h
"""

from __future__ import annotations

import argparse
from bisect import bisect_right
from collections import deque
import copy
from dataclasses import dataclass, field
from functools import lru_cache, cached_property
import hashlib
import json
import os
from pathlib import Path
import struct
import uuid

import unicorn
from unicorn import Uc, UcError, UC_ARCH_X86, UC_MODE_32, UC_HOOK_CODE, UC_HOOK_MEM_READ, UC_HOOK_MEM_WRITE, UC_QUERY_TIMEOUT
from unicorn.x86_const import (
    UC_X86_REG_EAX, UC_X86_REG_EBX, UC_X86_REG_ECX, UC_X86_REG_EDX,
    UC_X86_REG_ESI, UC_X86_REG_EDI, UC_X86_REG_ESP, UC_X86_REG_EBP,
    UC_X86_REG_EIP, UC_X86_REG_EFLAGS, UC_X86_REG_FPCW,
)

NATIVE_SHA256 = "1cdd1180e49024fbda8ad568caac2e86e856063ff67ab38f62b7d2c7bb84298c"
IMAGE_BASE = 0x00400000
# Preserve the original fixture mapping, including runtime globals in BSS.
IMAGE_SIZE = 0x00A00000
STACK_BASE, STACK_SIZE = 0x10000000, 0x00100000
SCRATCH, SCRATCH_SIZE = 0x20000000, 0x00010000
RET_MAGIC = 0x30000000
# Legacy RMG fixture contract: 53-bit precision, truncate. A caller must establish
# the appropriate ambient state for its own native entry; this is not universal.
NATIVE_FPCW = 0x0E7F


class OracleError(RuntimeError):
    """No trustworthy result was obtained; do not publish reference outputs."""


class NativeExecutionError(OracleError):
    """An unsuccessful run with captured evidence, never a native result."""

    def __init__(self, message: str, diagnostics: dict):
        self.diagnostics = diagnostics
        self.report_path = None
        directory = os.environ.get("VERA20K_NATIVE_FAILURE_DIR")
        if directory:
            try:
                parent = Path(directory).expanduser().resolve()
                parent.mkdir(parents=True, exist_ok=True)
                path = parent / f"native-failure-{uuid.uuid4().hex}.json"
                # Never replace a golden or an earlier failure, including when
                # several processes use the same diagnostic directory.
                with path.open("x", encoding="utf-8") as output:
                    output.write(json.dumps(diagnostics, indent=2, allow_nan=False) + "\n")
                self.report_path = path
                message += f"; failure report: {path}"
            except (OSError, ValueError) as error:
                message += f"; Could not save failure report: {error}"
        super().__init__(message)


def compare_cpu_context(uc: Uc, saved_context) -> dict:
    """Compare every context byte without changing the saved restore snapshot.

    The caller supplies a stopped VM's own CPU-only snapshot, using Unicorn's
    default context mode. Memory snapshots are outside this helper's contract.
    No guest memory is restored, and the caller's saved context remains usable.

    Unicorn 2.1.4 allocates an opaque context with g_malloc, leaving the
    CPU-only ramblock_freed/last_block metadata unset. Independent allocations
    therefore need not have equal bytes even with identical CPU state:
    https://github.com/unicorn-engine/unicorn/blob/2.1.4/uc.c#L2234-L2314
    https://github.com/unicorn-engine/unicorn/blob/2.1.4/include/uc_priv.h#L438-L447
    Serialize-copy the saved context, then update that inspection allocation
    through the public Python context_update API. Compare ALL bytes, including
    the complete native CPU payload (x87/vector state); never mask offsets or
    replace this guard with a selected register list.
    https://github.com/unicorn-engine/unicorn/blob/2.1.4/bindings/python/unicorn/unicorn_py3/unicorn.py
    """
    if (saved_context.arch, saved_context.mode) != (uc.ctl_get_arch(), uc.ctl_get_mode()):
        raise OracleError("CPU observation requires the saved VM architecture and mode")
    expected = bytes(saved_context)
    inspection = copy.copy(saved_context)
    uc.context_update(inspection)
    actual = bytes(inspection)
    if bytes(saved_context) != expected:
        raise OracleError("CPU observation changed the saved restore snapshot")
    if len(actual) != len(expected):
        raise OracleError("CPU observation changed the complete context size")
    return {
        "matches": actual == expected,
        "architecture": saved_context.arch,
        "mode": saved_context.mode,
        "context_bytes": len(expected),
        "expected_context_hex": expected.hex(),
        "observed_context_hex": actual.hex(),
        "different_offsets": [index for index, (before, after) in enumerate(zip(expected, actual))
                              if before != after],
        "method": "full-byte comparison after context_update into a serialized inspection clone",
        "saved_restore_snapshot_unchanged": True,
    }


def _machine_state(uc: Uc) -> dict:
    """Read a bounded diagnostic snapshot without mapping or changing memory."""
    registers = {}
    unavailable = {}
    for name, register in (
        ("eax", UC_X86_REG_EAX), ("ebx", UC_X86_REG_EBX),
        ("ecx", UC_X86_REG_ECX), ("edx", UC_X86_REG_EDX),
        ("esi", UC_X86_REG_ESI), ("edi", UC_X86_REG_EDI),
        ("esp", UC_X86_REG_ESP), ("ebp", UC_X86_REG_EBP),
        ("eip", UC_X86_REG_EIP), ("eflags", UC_X86_REG_EFLAGS),
        ("fpcw", UC_X86_REG_FPCW),
    ):
        try:
            registers[name] = uc.reg_read(register)
        except UcError as error:
            unavailable[name] = str(error)
    stack = {"address": registers.get("esp"), "words": [], "requested_words": 16}
    if stack["address"] is not None:
        for index in range(stack["requested_words"]):
            address = stack["address"] + 4 * index
            if address + 4 > 0x100000000:
                stack["unavailable"] = "Stack sample reached the end of the x86 address space"
                break
            try:
                stack["words"].append(struct.unpack("<I", uc.mem_read(address, 4))[0])
            except UcError as error:
                stack["unavailable"] = str(error)
                break
    else:
        stack["unavailable"] = "ESP unavailable"
    return {"registers": registers, "unavailable_registers": unavailable, "stack": stack}


def configured_gamemd() -> Path:
    explicit = os.environ.get("VERA20K_GAMEMD_EXE")
    retail_dir = os.environ.get("RA2_DIR")
    if not explicit and not retail_dir:
        raise OracleError("Set VERA20K_GAMEMD_EXE or RA2_DIR to the original retail gamemd.exe")
    path = Path(explicit) if explicit else Path(retail_dir) / "gamemd.exe"
    path = path.expanduser().resolve()
    if not path.is_file():
        raise OracleError(f"Missing original executable: {path}")
    return path


@lru_cache(maxsize=2)
def _verified_image(path: Path) -> bytes:
    # Hash the same immutable bytes subsequently mapped, not a separate read.
    data = path.read_bytes()
    digest = hashlib.sha256(data).hexdigest()
    if digest != NATIVE_SHA256:
        raise OracleError(f"Unsupported gamemd.exe SHA-256 {digest}; expected {NATIVE_SHA256}")
    return data


def image_bytes() -> bytes:
    return _verified_image(configured_gamemd())


def _sections(data: bytes):
    if len(data) < 0x40:
        raise OracleError("Truncated PE DOS header")
    pe = struct.unpack_from("<I", data, 0x3C)[0]
    if pe < 0x40 or pe + 24 > len(data):
        raise OracleError("PE header offset is outside the file")
    machine, count = struct.unpack_from("<HH", data, pe + 4)
    optional_size = struct.unpack_from("<H", data, pe + 20)[0]
    optional = pe + 24
    if optional_size < 32 or optional + optional_size > len(data):
        raise OracleError("Truncated PE32 optional header")
    if optional + optional_size + count * 40 > len(data):
        raise OracleError("Truncated PE section table")
    if (data[:2] != b"MZ" or data[pe:pe + 4] != b"PE\0\0" or machine != 0x14C
            or struct.unpack_from("<H", data, optional)[0] != 0x10B
            or struct.unpack_from("<I", data, optional + 28)[0] != IMAGE_BASE):
        raise OracleError("Expected the pinned PE32 x86 image at 0x00400000")
    for index in range(count):
        offset = optional + optional_size + index * 40
        virtual_size, rva, raw_size, raw_ptr = struct.unpack_from("<IIII", data, offset + 8)
        flags = struct.unpack_from("<I", data, offset + 36)[0]
        if rva + max(virtual_size, raw_size) > IMAGE_SIZE or raw_ptr + raw_size > len(data):
            raise OracleError("PE section exceeds the verified fixture mapping")
        yield rva, raw_ptr, raw_size, virtual_size, flags


def file_span(data: bytes, va: int, size: int) -> tuple[int, bytes]:
    """Resolve one original file-backed section span, never synthesized memory.

    The input bytes must be identity-checked by the caller for native claims.
    Unlike load_image's zero-filled mapping, headers, gaps, BSS and requests
    crossing a section boundary have no supported file span. Section raw padding
    remains readable exactly as load_image maps it, even beyond VirtualSize.
    """
    if size <= 0:
        raise OracleError("PE file span size must be positive")
    start = va - IMAGE_BASE
    end = start + size
    if start < 0 or end > IMAGE_SIZE:
        raise OracleError("PE file span is outside the fixture image")
    # Validate every section before returning data, including malformed sections
    # after the requested one. _sections remains the single PE parsing owner.
    sections = list(_sections(data))
    intersecting = [section for section in sections
                    if start < section[0] + max(section[2], section[3])
                    and end > section[0]]
    if len(intersecting) == 1:
        rva, raw_ptr, raw_size, _, _ = intersecting[0]
        if rva <= start and end <= rva + raw_size:
            offset = raw_ptr + start - rva
            return offset, bytes(data[offset:offset + size])
    raise OracleError(
        f"PE file span 0x{va:08X}+{size} must lie within one file-backed section "
        "(not headers, gaps, BSS or a section crossing)")


@dataclass(frozen=True)
class ImportTransport:
    """One audited original FF15 import site; no imported instruction executes.

    Stack ranges are offsets/bytes relative to ESP before CALL pushes a return.
    forward_entry is limited to the original CoCreateInstance five-word to
    native four-argument factory adaptation, not a generic call-forward API.
    """
    site: int
    iat: int
    argument_bytes: int
    stack_reads: tuple[tuple[int, int], ...] = ()
    stack_writes: tuple[tuple[int, int], ...] = ()
    forward_entry: int | None = None


@dataclass(frozen=True)
class EbpImportTransport(ImportTransport):
    """One original CALL EBP site with EBP equal to its immutable IAT payload.

    RawFileClass::Seek65CF00 uses this form at65CF8B/65CFD4/65D030 after
    loading SetFilePointer from7E11C0. This declaration permits no other
    register/opcode or target and cannot forward a COM factory call.
    """


@dataclass(frozen=True)
class EdiImportTransport(ImportTransport):
    """Original CALL EDI site, bound to an unchanged declared IAT payload."""


def _register_import(spec):
    if isinstance(spec,EbpImportTransport):return 'EBP',b'\xff\xd5'
    if isinstance(spec,EdiImportTransport):return 'EDI',b'\xff\xd7'
    return None


def _transport_instruction_bytes(spec):
    return 2 if _register_import(spec) else 6


@dataclass(frozen=True)
class ExecutionProfile:
    """Trusted mechanism declaration, never a CLI-configurable hash bypass.

    Regions are (start, end-exclusive, sha256). Data ranges are (start, bytes).
    Sink declarations are (address, argument_bytes); callbacks must return through
    the original stack address, and no instruction at a sink may execute.
    """
    name: str
    native_sha256: str
    regions: tuple[tuple[int, int, str], ...]
    entries: tuple[tuple[int, tuple[int, ...]], ...]
    reads: tuple[tuple[int, int], ...]
    writes: tuple[tuple[int, int], ...]
    fixture_writes: tuple[tuple[int, int], ...]
    sinks: tuple[tuple[int, int], ...] = ()
    transports: tuple[ImportTransport, ...] = ()


def _within(address: int, size: int, ranges) -> bool:
    return size > 0 and any(start <= address and address + size <= start + length
                           for start, length in ranges)


@dataclass(frozen=True)
class _RangeIndex:
    """Exact single-grant containment; adjacent ranges are never merged.

    At an address, the greatest end among starts at or before it belongs to
    one original grant. Containment under that end therefore has exactly the
    same meaning as the original linear predicate, even with nested grants.
    """
    starts: tuple[int, ...]
    greatest_ends: tuple[int, ...]

    @classmethod
    def build(cls,ranges):
        starts=[];ends=[];greatest=None
        for start,length in sorted(ranges):
            end=start+length
            greatest=end if greatest is None else max(greatest,end)
            starts.append(start);ends.append(greatest)
        return cls(tuple(starts),tuple(ends))

    def within(self,address,size):
        if size<=0:return False
        index=bisect_right(self.starts,address)-1
        return index>=0 and address+size<=self.greatest_ends[index]


@dataclass(frozen=True)
class ScopedImage:
    """Immutable image identity bound to one machine and one explicit profile."""
    machine: Uc = field(repr=False, compare=False)
    data: bytes = field(repr=False)
    profile: ExecutionProfile

    @cached_property
    def _instruction_index(self):
        return _RangeIndex.build((start,end-start)for start,end,_ in self.profile.regions)

    @cached_property
    def _read_index(self):return _RangeIndex.build(self.profile.reads)

    @cached_property
    def _write_index(self):return _RangeIndex.build(self.profile.writes)

    @cached_property
    def _original_byte_cache(self):
        # Derived only from this immutable file identity, never mapped guest
        # bytes. Authorization and current mapped bytes remain checked on every
        # instruction, including cache hits. Each image owns its own cache.
        return {}

    def _original_bytes(self, address: int, size: int) -> bytes:
        key = (address, size)
        if key not in self._original_byte_cache:
            self._original_byte_cache[key] = file_span(self.data, address, size)[1]
        return self._original_byte_cache[key]

    def write(self, address: int, blob: bytes) -> None:
        self._check_code_write(address, len(blob))
        if not _within(address, len(blob), self.profile.fixture_writes):
            raise OracleError(f"Profile {self.profile.name}: undeclared fixture write {address:#x}+{len(blob)}")
        self.machine.mem_write(address, blob)

    def _check_code_write(self, address: int, size: int) -> None:
        # The loader maps executable sections only within this image. Keep
        # the original overlap check for image accesses; ordinary heap/stack
        # writes cannot touch code and need no repeated PE header decoding.
        if address>=IMAGE_BASE+IMAGE_SIZE or address+size<=IMAGE_BASE:return
        if any(flags & 0x20000000 and address < IMAGE_BASE + rva + max(raw, virtual)
               and address + size > IMAGE_BASE + rva
               for rva, _, raw, virtual, flags in _sections(self.data)):
            raise OracleError("Scoped fixture writes cannot replace native executable instructions")

    def verify_code(self) -> None:
        for start, end, digest in self.profile.regions:
            if hashlib.sha256(bytes(self.machine.mem_read(start, end - start))).hexdigest() != digest:
                raise OracleError(f"Profile {self.profile.name}: mapped original code changed at {start:#x}")

    def identity(self) -> dict:
        return {"name": self.profile.name, "native_sha256": self.profile.native_sha256,
                "regions": [{"start": start, "end": end, "sha256": digest}
                            for start, end, digest in self.profile.regions],
                "entries": [{"start": start, "ends": list(ends)} for start, ends in self.profile.entries],
                "reads": [list(item) for item in self.profile.reads],
                "writes": [list(item) for item in self.profile.writes],
                "fixture_writes": [list(item) for item in self.profile.fixture_writes],
                "sinks": [list(item) for item in self.profile.sinks],
                "transports": [vars(item) for item in self.profile.transports]}


class TransportCall:
    """Checked data/stack access for a declared OS boundary; redirects owned here."""
    def __init__(self,image,spec,sp):
        self._image=image;self._machine=image.machine;self.spec=spec;self.sp=sp
        # A no-argument API does not read the caller's stack. Keep zero-byte
        # accesses invalid everywhere else rather than widening data guards.
        self.arguments=(struct.unpack('<'+'I'*(spec.argument_bytes//4),self.read(sp,spec.argument_bytes))
                        if spec.argument_bytes else ())

    def _check(self,address,size,write):
        ranges=self._image.profile.writes if write else self._image.profile.reads
        if not _within(address,size,ranges):
            raise OracleError('Import transport data access outside declared profile')
        if address<STACK_BASE+STACK_SIZE and address+size>STACK_BASE:
            allowed=self.spec.stack_writes if write else ((0,self.spec.argument_bytes),)+self.spec.stack_reads
            if not _within(address,size,tuple((self.sp+a,n)for a,n in allowed)):
                raise OracleError('Import transport stack access outside declared site ranges')
        if write:self._image._check_code_write(address,size)

    def read(self,address,size):
        self._check(address,size,False)
        return bytes(self._machine.mem_read(address,size))

    def write(self,address,blob):
        self._check(address,len(blob),True)
        self._machine.mem_write(address,blob)

    def return_to_native(self,eax):
        if self.spec.forward_entry is not None:
            raise OracleError('Factory transport must forward to its original body')
        self._machine.reg_write(UC_X86_REG_EAX,eax)
        self._machine.reg_write(UC_X86_REG_ESP,self.sp+self.spec.argument_bytes)
        self._machine.reg_write(UC_X86_REG_EIP,self.spec.site+_transport_instruction_bytes(self.spec))

    def forward_to_factory(self):
        if self.spec.forward_entry is None or len(self.arguments)!=5:
            raise OracleError('Only the declared five-word COM factory adaptation is supported')
        _,outer,_,iid,ppv=self.arguments
        self.write(self.sp,struct.pack('<5I',self.spec.site+6,0,outer,iid,ppv))
        self._machine.reg_write(UC_X86_REG_EIP,self.spec.forward_entry)


def _validate_transports(data,profile):
    sites=set()
    for spec in profile.transports:
        if (not isinstance(spec,ImportTransport) or spec.site in sites
                or spec.argument_bytes<0 or spec.argument_bytes%4
                or spec.site in dict(profile.sinks)):
            raise OracleError('Invalid or duplicate scoped import transport declaration')
        sites.add(spec.site)
        instruction_bytes=_transport_instruction_bytes(spec)
        if not any(a<=spec.site and spec.site+instruction_bytes<=b for a,b,_ in profile.regions):
            raise OracleError('Import transport straddles or lies outside qualified original code')
        if register_import:=_register_import(spec):
            register,opcode=register_import
            if file_span(data,spec.site,2)[1]!=opcode:
                raise OracleError('Register import transport must identify original CALL '+register+' bytes')
            if spec.forward_entry is not None:
                raise OracleError('Register import transport cannot forward a COM factory')
        elif file_span(data,spec.site,6)[1]!=b'\xff\x15'+struct.pack('<I',spec.iat):
            raise OracleError('Import transport must identify original FF15/IAT bytes')
        if not _within(spec.iat,4,profile.reads):
            raise OracleError('Import transport IAT must have declared read authorization')
        for offset,size in spec.stack_reads+spec.stack_writes:
            if offset<0 or size<=0:raise OracleError('Import transport stack ranges must be positive')
        if spec.forward_entry is not None:
            if (spec.argument_bytes!=20 or not _within(0,20,spec.stack_writes)
                    or not any(a<=spec.forward_entry<b for a,b,_ in profile.regions)):
                raise OracleError('Import transport factory adaptation requires five words and enrolled destination')


def load_image(uc: Uc, *, profile: ExecutionProfile | None = None) -> ScopedImage | None:
    """Map verified original PE sections, zero-fill gaps/BSS; no OS initialization.

    The mapping retains legacy RWX permissions for existing fixture hooks. That
    does not authorize treating patched code or supplied call results as native.
    """
    if profile is None:
        data = image_bytes()
    else:
        data = configured_gamemd().read_bytes()
        if hashlib.sha256(data).hexdigest() != profile.native_sha256:
            raise OracleError(f"Profile {profile.name}: unsupported executable identity")
        for start, end, digest in profile.regions:
            if hashlib.sha256(file_span(data, start, end - start)[1]).hexdigest() != digest:
                raise OracleError(f"Profile {profile.name}: original region mismatch at {start:#x}")
    if profile is not None:_validate_transports(data,profile)
    sections = list(_sections(data))
    uc.mem_map(IMAGE_BASE, IMAGE_SIZE)
    uc.mem_write(IMAGE_BASE, data[:0x1000])
    for rva, raw_ptr, raw_size, _, _ in sections:
        if raw_size:
            uc.mem_write(IMAGE_BASE + rva, data[raw_ptr:raw_ptr + raw_size])
    if profile is None:
        return None
    image = ScopedImage(uc, data, profile)
    uc._vera20k_scoped_image = image
    uc._vera20k_scoped_run_active = False

    def require_guarded_run(machine, _address, _size, _data):
        if not machine._vera20k_scoped_run_active:
            machine.emu_stop()
            raise OracleError("Scoped images require their guarded run_checked handle")
        machine._vera20k_scope_instruction=(_address,machine.reg_read(UC_X86_REG_ESP))

    # The loader-owned lifetime hook also blocks accidental raw emu_start calls.
    uc.hook_add(UC_HOOK_CODE, require_guarded_run)
    return image


def run_checked(uc: Uc, begin: int, end: int | tuple[int, ...], *,
                count: int = 5_000_000, timeout_us: int = 10_000_000,
                required_addresses=(), context: dict | None = None,
                image: ScopedImage | None = None, sinks: dict | None = None,
                transports: dict | None = None) -> int:
    """Execute to a declared return/region boundary or fail with a short trace.

    Boundaries are reached BEFORE executing their instruction. Existing hooks may
    remain, but stopping anywhere else fails. No faults are swallowed. Unicorn's
    count/time limits stop emulation normally, so absence of UcError is not proof
    of completion (uc.c:987, unicorn.h uc_emu_start). This function owns exits for
    this run; custom ctl_set_exits are disabled in favor of these explicit ends.

    Failures carry JSON-compatible diagnostics; set VERA20K_NATIVE_FAILURE_DIR
    to also save them. context may identify the case and supplied fixture inputs.
    A reached instruction budget is an observation, not proof that an external
    hook did not stop at that same instruction.
    """
    bound_image = getattr(uc, "_vera20k_scoped_image", None)
    if bound_image is not None and image is not bound_image:
        raise OracleError("Scoped machine requires its matching image handle")
    if bound_image is not None and uc._vera20k_scoped_run_active:
        raise OracleError("Scoped native execution is not reentrant")
    ends = (end,) if isinstance(end, int) else tuple(end)
    if not ends or begin in ends or count <= 0 or timeout_us <= 0:
        raise ValueError("Use distinct entry/endpoints and positive instruction/time limits")
    required = set(required_addresses)
    if required.intersection(ends):
        raise ValueError("Required instruction addresses must precede the stop boundary")
    if context is not None and not isinstance(context, dict):
        raise TypeError("Native diagnostic context must be a JSON object")
    # Freeze caller inputs before hooks execute, and fail invalid context before
    # running anything. This does not change the successful result schema.
    diagnostic_context = json.loads(_canonical(context or {}))
    initial = _machine_state(uc)
    violation = None
    allowed_sinks = {}
    allowed_transports = {}
    transport_events=[]
    if image is not None:
        if image.machine is not uc:
            raise OracleError("Scoped image belongs to a different machine")
        if not any(begin == entry and set(ends) <= set(boundaries)
                   for entry, boundaries in image.profile.entries):
            raise OracleError("Profile does not authorize this entry/endpoint pair")
        image.verify_code()
        allowed_sinks = dict(image.profile.sinks)
        allowed_transports = {item.site:item for item in image.profile.transports}
        if set(transports or {})-set(allowed_transports):
            raise OracleError("Profile does not authorize supplied import transports")
        if set(sinks or {}) - set(allowed_sinks):
            raise OracleError("Profile does not authorize supplied sink callbacks")
        if required.intersection(set(allowed_sinks)|set(allowed_transports)):
            raise OracleError("A substituted sink is not original instruction coverage")
    elif sinks or transports:
        raise OracleError("Runner-owned sinks require an explicit scoped image")
    visited = set()
    trail = deque(maxlen=16)
    observed = 0

    def reject(address, size, kind, detail):
        nonlocal violation
        if violation is None:
            violation = {"address": address, "bytes": size, "kind": kind, "detail": detail}
        uc.emu_stop()

    def memory_guard(_uc, access, address, size, _value, _data):
        from unicorn import UC_MEM_WRITE
        if access == UC_MEM_WRITE:
            try:
                image._check_code_write(address, size)
            except OracleError as error:
                reject(address, size, "native_code_write", str(error))
                return
            index = image._write_index
            kind = "undeclared_write"
        else:
            index = image._read_index
            kind = "undeclared_read"
        if not index.within(address, size):
            reject(address, size, kind, "Guest data access outside declared ranges")

    def observe(_uc, address, size, _data):
        nonlocal observed
        trail.append(address)
        if image is not None and (
                uc.reg_read(UC_X86_REG_EIP)!=address
                or getattr(uc,"_vera20k_scope_instruction",None)!=(address,uc.reg_read(UC_X86_REG_ESP))):
            reject(address,size,"prehook_control_mutation","A prior hook changed native PC/ESP before the runner guard");return
        # Stop boundaries never authorize executing their original instruction.
        if address in ends:
            _uc.emu_stop()
            return
        if image is not None:
            if address in allowed_sinks:
                callback = (sinks or {}).get(address)
                if callback is None:
                    reject(address, size, "missing_sink", "Declared sink has no callback")
                    return
                sp = uc.reg_read(UC_X86_REG_ESP)
                if not _within(sp, 4 + allowed_sinks[address], image.profile.reads):
                    reject(sp, 4, "sink_stack", "Sink return/arguments outside declared data")
                    return
                destination = struct.unpack("<I", uc.mem_read(sp, 4))[0]
                try:
                    callback(uc)
                except Exception as error:
                    reject(address, size, "sink_failure", f"{type(error).__name__}: {error}")
                    return
                if (uc.reg_read(UC_X86_REG_EIP) != destination
                        or uc.reg_read(UC_X86_REG_ESP) != sp + 4 + allowed_sinks[address]):
                    reject(address, size, "sink_abi", "Sink did not redirect through declared return/stack cleanup")
                    return
            elif not image._instruction_index.within(address,size):
                reject(address, size, "undeclared_instruction", "Instruction outside qualified closure or straddles its boundary")
                return
            elif bytes(uc.mem_read(address, size)) != image._original_bytes(address, size):
                reject(address, size, "native_code_changed", "Mapped instruction differs from immutable original bytes")
                return
        if address in allowed_transports:
            spec=allowed_transports[address]
            callback=(transports or {}).get(address)
            if callback is None:
                reject(address,size,'missing_transport','Declared import transport has no callback');return
            if bytes(uc.mem_read(spec.iat,4))!=image._original_bytes(spec.iat,4):
                reject(spec.iat,4,'transport_iat_changed','Original IAT slot changed');return
            if register_import:=_register_import(spec):
                from unicorn.x86_const import UC_X86_REG_EBP,UC_X86_REG_EDI
                register,_=register_import
                target=struct.unpack('<I',image._original_bytes(spec.iat,4))[0]
                if uc.reg_read(UC_X86_REG_EBP if register=='EBP'else UC_X86_REG_EDI)!=target:
                    reject(address,size,'transport_register_target','CALL '+register+' target differs from original declared IAT payload');return
            sp=uc.reg_read(UC_X86_REG_ESP)
            try:
                call=TransportCall(image,spec,sp)
                callback(call)
            except Exception as error:
                reject(address,size,'transport_failure',f'{type(error).__name__}: {error}');return
            expected_pc=spec.site+_transport_instruction_bytes(spec) if spec.forward_entry is None else spec.forward_entry
            expected_sp=sp+spec.argument_bytes if spec.forward_entry is None else sp
            if uc.reg_read(UC_X86_REG_EIP)!=expected_pc or uc.reg_read(UC_X86_REG_ESP)!=expected_sp:
                reject(address,size,'transport_abi','Import transport redirect/stack cleanup differs from declaration');return
            if spec.forward_entry is not None:
                _,outer,_,iid,ppv=call.arguments
                if bytes(uc.mem_read(sp,20))!=struct.pack('<5I',spec.site+6,0,outer,iid,ppv):
                    reject(sp,20,'transport_abi','Original five-word COM factory adaptation differs');return
            transport_events.append(dict(site=address,iat=spec.iat,arguments=list(call.arguments),
                                         original_instruction_executed=False,redirect=expected_pc,stack_after=expected_sp))
            return
        if address in required:
            visited.add(address)
        observed += 1

    uc.ctl_exits_enabled(False)
    hook = uc.hook_add(UC_HOOK_CODE, observe)
    memory_hook = (uc.hook_add(UC_HOOK_MEM_READ | UC_HOOK_MEM_WRITE, memory_guard)
                   if image is not None else None)
    try:
        fault = None
        try:
            if image is not None:
                uc._vera20k_scoped_run_active = True
            uc.emu_start(begin, ends[0], timeout=timeout_us, count=count)
        except UcError as error:
            fault = error
        # Query before another emulation or diagnostic callback can replace it.
        timed_out = bool(uc.query(UC_QUERY_TIMEOUT))
        pc = uc.reg_read(UC_X86_REG_EIP)
        missing = required - visited
        if violation or fault or timed_out or pc not in ends or missing:
            if violation:
                reason = "profile_violation"
                message = f"Profile {image.profile.name}: {violation['kind']} at {violation['address']:#x}"
            elif fault:
                reason = "fault"
                message = f"Native execution 0x{begin:08X} faulted: {fault}"
            elif timed_out or pc not in ends:
                reason = ("timeout" if timed_out else
                          "instruction_limit_reached" if observed >= count else "early_stop")
                message = (f"Incomplete execution from 0x{begin:08X}: stopped at 0x{pc:08X}; "
                           f"expected {', '.join(f'0x{x:08X}' for x in ends)}")
            else:
                reason = "required_addresses_missing"
                message = f"Required native instruction addresses not reached: {sorted(hex(x) for x in missing)}"
            trace = ", ".join(f"0x{x:08X}" for x in trail)
            diagnostics = {
                "schema": "vera20k.native-execution-failure.v1", "reason": reason,
                "entry": begin, "expected_endpoints": list(ends), "timed_out": timed_out,
                "instruction_limit": count, "timeout_us": timeout_us,
                "observed_instructions": observed,
                "required_addresses": sorted(required), "missing_required_addresses": sorted(missing),
                "trace": list(trail), "initial": initial, "final": _machine_state(uc),
                "context": diagnostic_context,
                "fault": {"errno": fault.errno, "message": str(fault)} if fault else None,
                "unicorn_binding": unicorn.__version__, "unicorn_core": list(unicorn.uc_version()),
                # run_checked also accepts synthetic machines and cannot attest
                # their image identity just because this runner knows the pin.
                "expected_native_sha256": (image.profile.native_sha256 if image is not None else NATIVE_SHA256),
            }
            if image is not None:
                diagnostics.update(profile=image.identity(), profile_violation=violation, import_transports=transport_events)
            raise NativeExecutionError(
                f"{message}; reason={reason}, timeout={timed_out}, "
                f"observed={observed}/{count}; trace: {trace}", diagnostics) from fault
        if image is not None:
            image.verify_code()
        return pc
    finally:
        if image is not None:
            uc._vera20k_last_import_transports=transport_events
            uc._vera20k_scoped_run_active = False
        uc.hook_del(hook)
        if memory_hook is not None:
            uc.hook_del(memory_hook)


def call(func: int, *, ecx=None, edx=None, stack_args=None, writes=None,
         dumps=None, capture_st0=False, fpcw=NATIVE_FPCW,
         timeout_instr=5_000_000, timeout_us=10_000_000, required_addresses=(),
         context: dict | None = None, profile: ExecutionProfile | None = None) -> dict:
    """Run one function in fresh state. Results preserve the legacy harness schema.

    ECX/EDX and stack arguments are explicit calling-convention inputs. Writes
    supply fixture data; executable-section writes are rejected. ST0 capture
    stores binary64 through a six-byte FSTP return stub outside native memory;
    it is a declared observation conversion, not full x87 80-bit capture.
    """
    if profile is not None and capture_st0:
        raise OracleError('Scoped call() cannot execute the external ST0 observation stub')
    uc = Uc(UC_ARCH_X86, UC_MODE_32)
    image = load_image(uc) if profile is None else load_image(uc, profile=profile)
    sections = list(_sections(image.data if image is not None else image_bytes()))
    if not any(flags & 0x20000000 and IMAGE_BASE + rva <= func < IMAGE_BASE + rva + raw
               for rva, _, raw, _, flags in sections):
        raise OracleError("call() entry must be an original native executable-section address")
    uc.mem_map(STACK_BASE, STACK_SIZE)
    uc.mem_map(SCRATCH, SCRATCH_SIZE)
    uc.mem_map(RET_MAGIC, 0x1000)
    executable = [(IMAGE_BASE + rva, IMAGE_BASE + rva + max(raw, size))
                  for rva, _, raw, size, flags in sections if flags & 0x20000000]
    for address, blob in (writes or {}).items():
        if any(address < high and address + len(blob) > low for low, high in executable):
            raise OracleError("call() fixture writes cannot replace native executable instructions")
        if image is None:
            uc.mem_write(address, blob)
        else:
            image.write(address, blob)
    stop_at = RET_MAGIC
    st0_slot = RET_MAGIC + 0x100
    if capture_st0:
        uc.mem_write(RET_MAGIC, b"\xdd\x1d" + struct.pack("<I", st0_slot))
        stop_at += 6
    sp = STACK_BASE + STACK_SIZE - 0x1000
    for value in reversed(stack_args or []):
        sp -= 4
        if image is None:
            uc.mem_write(sp, struct.pack("<I", value))
        else:
            image.write(sp, struct.pack("<I", value))
    sp -= 4
    if image is None:
        uc.mem_write(sp, struct.pack("<I", RET_MAGIC))
    else:
        image.write(sp, struct.pack("<I", RET_MAGIC))
    uc.reg_write(UC_X86_REG_ESP, sp)
    for register, value in [(UC_X86_REG_FPCW, fpcw), (UC_X86_REG_ECX, ecx), (UC_X86_REG_EDX, edx)]:
        if value is not None:
            uc.reg_write(register, value)
    required = set(required_addresses)
    if capture_st0:
        required.add(RET_MAGIC)
    detail = dict(context or {})
    if "call" in detail:
        raise ValueError("The diagnostic context key 'call' is reserved for calling-convention inputs")
    detail["call"] = {
        "function": func, "ecx": ecx, "edx": edx, "stack_args": list(stack_args or []),
        "fpcw": fpcw, "capture_st0": capture_st0,
        "writes": [{"address": address, "bytes": len(blob)} for address, blob in (writes or {}).items()],
    }
    run_checked(uc, func, stop_at, count=timeout_instr, timeout_us=timeout_us,
                required_addresses=required, context=detail, image=image)
    result = {"eax": uc.reg_read(UC_X86_REG_EAX) & 0xFFFFFFFF, "dumps": {}}
    for name, (address, length) in (dumps or {}).items():
        if image is not None and not _within(address, length, image.profile.reads):
            raise OracleError('Scoped call() dump must lie within declared data reads')
        result["dumps"][name] = bytes(uc.mem_read(address, length)).hex()
    if capture_st0:
        raw = bytes(uc.mem_read(st0_slot, 8))
        result.update(st0_bits=struct.unpack("<Q", raw)[0], st0=struct.unpack("<d", raw)[0])
    return result


def provenance(*, scope: str, assumptions: list[str], substitutions: list[str],
               entry_points: dict[str, int], image: ScopedImage | None = None) -> dict:
    """Record identity and claims separately from legacy vector payloads."""
    if not scope.strip() or not assumptions or not entry_points:
        raise ValueError("Declare scope, runtime assumptions, and native entry points")
    result = {
        "schema_version": 1, "native_sha256": hashlib.sha256(image.data if image is not None else image_bytes()).hexdigest(),
        "unicorn_binding": unicorn.__version__, "unicorn_core": list(unicorn.uc_version()),
        "scope": scope, "assumptions": assumptions, "substitutions": substitutions,
        "entry_points": {name: f"0x{value:08X}" for name, value in entry_points.items()},
    }
    if image is not None:
        result["execution_profile"] = image.identity()
    return result


def _canonical(data) -> bytes:
    return json.dumps(data, sort_keys=True, separators=(",", ":"), allow_nan=False).encode("utf-8")


def first_difference(expected, actual, path="$", limit=180) -> str | None:
    """Locate the first mismatch without dumping whole model states."""
    if type(expected) is not type(actual):
        return f"{path}: expected {type(expected).__name__}, got {type(actual).__name__}"
    if isinstance(expected, dict):
        if expected.keys() != actual.keys():
            return f"{path}: missing keys {sorted(expected.keys() - actual.keys())}, extra keys {sorted(actual.keys() - expected.keys())}"
        for key in expected:
            if difference := first_difference(expected[key], actual[key], f"{path}.{key}"):
                return difference
    elif isinstance(expected, list):
        if len(expected) != len(actual):
            return f"{path}: expected {len(expected)} entries, got {len(actual)}"
        for index, (left, right) in enumerate(zip(expected, actual)):
            if difference := first_difference(left, right, f"{path}[{index}]"):
                return difference
    elif isinstance(expected, float) and struct.pack("<d", expected) != struct.pack("<d", actual):
        return f"{path}: expected {expected!r}, got {actual!r} (binary64 differs)"
    elif isinstance(expected, str) and expected != actual and max(len(expected), len(actual)) > limit:
        offset = next((i for i, (left, right) in enumerate(zip(expected, actual)) if left != right),
                      min(len(expected), len(actual)))
        start = max(0, offset - 24)
        return (f"{path}: first differing character {offset}; "
                f"expected {expected[start:offset + 40]!r}, got {actual[start:offset + 40]!r}")
    elif expected != actual:
        return f"{path}: expected {repr(expected)[:limit]}, got {repr(actual)[:limit]}"
    return None


def source_identity(source_paths: dict[str, Path] | None = None) -> dict:
    """One UTF-8/LF identity owner for native reference producers."""
    return {name: hashlib.sha256(path.read_text(encoding="utf-8").encode("utf-8")).hexdigest()
            for name, path in (source_paths or {}).items()}


def finish_vectors(data, default_path: Path, *, provenance: dict, argv=None,
                   source_paths: dict[str, Path] | None = None,
                   description: str | None = None) -> None:
    """Default: check without writing. --write deliberately replaces the reference.

    Existing payloads retain their Rust-facing schema. A .meta.json sidecar records
    provenance and the canonical payload hash. Old files without metadata can be
    compared, but their historical provenance is explicitly unknown. Optional
    source_paths captures UTF-8/LF source identity before invoking the lazy
    generator and rejects drift immediately before comparison or publication.
    """
    parser = argparse.ArgumentParser(description=description or "Compare native outputs with recorded reference data")
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--check", action="store_true", help="compare only (default)")
    mode.add_argument("--write", action="store_true", help="explicitly write outputs and provenance")
    parser.add_argument("--output", type=Path, default=default_path)
    args = parser.parse_args(argv)
    sources = source_identity(source_paths)
    data = data() if callable(data) else data
    provenance = provenance() if callable(provenance) else provenance
    if source_paths is not None:
        if "source_normalized_lf_sha256" in provenance:
            raise OracleError("Source provenance must be supplied through source_paths")
        provenance = dict(provenance, source_normalized_lf_sha256=sources)
    # Compare payload and provenance in their persisted JSON representation:
    # tuples (including nested transport ranges) become arrays in sidecars.
    # Canonical serialization rejects NaN/Infinity in either workflow.
    normalized = json.loads(_canonical(data))
    metadata = json.loads(_canonical(dict(
        provenance, payload_sha256=hashlib.sha256(_canonical(normalized)).hexdigest())))
    payload_text = json.dumps(normalized, indent=2, allow_nan=False) + "\n"
    metadata_text = json.dumps(metadata, indent=2, allow_nan=False) + "\n"
    target = args.output
    sidecar = target.with_suffix(".meta.json")
    if difference := first_difference(sources, source_identity(source_paths)):
        raise OracleError(f"Source changed during native generation: {difference}")
    if args.write:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(payload_text, encoding="utf-8")
        sidecar.write_text(metadata_text, encoding="utf-8")
        print(f"WROTE {target} and {sidecar}; review before accepting changed native references")
        return
    if not target.is_file():
        raise OracleError(f"Reference missing: {target}; use --write to deliberately create it")
    expected = json.loads(target.read_text(encoding="utf-8"))
    if difference := first_difference(expected, normalized):
        raise OracleError(f"Reference mismatch in {target}: {difference}")
    if sidecar.is_file():
        expected_metadata = json.loads(sidecar.read_text(encoding="utf-8"))
        if difference := first_difference(expected_metadata, metadata):
            raise OracleError(f"Provenance mismatch in {sidecar}: {difference}")
    else:
        print("NOTE: legacy reference has no provenance sidecar; historical environment is unknown")
    print(f"PASS {target}: native outputs match; no files written")
