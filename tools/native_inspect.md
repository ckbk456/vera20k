# Identify candidates and inspect the pinned native executable

Use `python -m tools.native_inspect` before writing a session-local disassembler,
VA mapper or whole-code scan. It shares executable selection, SHA checking and
PE parsing with `tools.native_oracle`; `native_oracle.file_span` is the single
owner of original file-backed VA reads. This tool performs no emulation, writes
no goldens and does not modify Ghidra.

Install the repository's pinned Python dependencies:

```sh
python -m pip install -r tools/requirements-test.txt
```

Select `VERA20K_GAMEMD_EXE` or `RA2_DIR` as described in
[native setup](native_oracle.md). Byte/instruction inspection still accepts only
the pinned original executable. The separate `identity` command identifies an
unqualified candidate without admitting it to those operations or execution.
Import and `--help` do not read it. Missing/wrong images and invalid requests fail
with nonzero status, diagnostics on stderr and no JSON evidence on stdout.

```sh
python -m tools.native_inspect sections
python -m tools.native_inspect read 0x8610B4 --bytes 16
python -m tools.native_inspect disasm 0x773070 --bytes 96
python -m tools.native_inspect calls 0x773070
python -m tools.native_inspect calls 0x773070 --include-jumps
python -m tools.native_inspect field 0x68A --width 1
python -m tools.native_inspect find-bytes "32 c0 c2 04 00"
```

## Candidate identification

```sh
python -m tools.native_inspect identity
python -m tools.native_inspect identity --reference ramp-height --reference foot-z
```

`identity` reads the configured executable once and uses the shared PE owner to
validate its PE32 x86 layout at `0x00400000`. It reports the actual whole-file
SHA-256, length and file-backed section hashes, including raw padding but never
synthesized BSS. It writes no executable bytes, private paths or goldens.
`native_execution_supported` means only that its whole-file hash equals the
existing pinned execution identity. It is independent of reference-region matches.
An unqualified candidate remains rejected by `image_bytes`, all native fixtures
and every other inspection command.

References reuse `REGIONS` from the existing ramp-height and Foot-Z fixture
owners and their stored `region_sha256` goldens. Each profile records its owner,
reference artifact hash, original image hash, addresses, sizes and individual
matching/nonmatching hashes. A changed/missing region, wrong reference image,
invalid hash or unbacked range cannot silently become a successful comparison.
No fixture is instantiated and no native code runs. Matching samples establish
those original file bytes only; callers, constants/globals, initialization,
runtime patches, other bodies and gameplay remain outside their coverage.

The [Steam build 15918130 identity receipt](native_inspect.steam-15918130.identity.json)
was generated on 2026-10-03 with `identity --reference ramp-height --reference foot-z`.
Its source was the user's verified English Steam app 2229850 installation:
436 files / 1,961,731,509 bytes matched the Windows source. The receipt records
candidate hash `3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`,
all 11 reference regions matching and `native_execution_supported=false`.
This is a bounded static comparison, not a YR patch-version or gameplay qualification.
The existing `sections` command still returned exit 2 and no JSON for this image.

Save stdout to a file when preserving a finding. Each deterministic JSON packet
records schema version, actual image SHA-256, Capstone version and the complete parsed
request. Addresses and file offsets are JSON integers; command arguments accept
decimal or `0x` notation. No timestamps or machine-specific paths affect comparison.

## Scope and coverage

- `sections` reports section index, VA, raw offset/length, virtual size and flags.
  A virtual tail is not original file content. Do not convert VA to file offset
  by subtracting the image base: the retail fourth section differs, and `.data`
  includes a large unbacked runtime region.
- `read` and `disasm` require a positive byte count wholly inside one file-backed
  section. Headers, gaps, BSS and cross-section ranges fail. Raw section padding
  is available exactly as the existing oracle loader maps it.
- `calls` and `field` scan executable sections by default. Supply both
  `--start <VA> --bytes <N>` to inspect one explicit file-backed range instead.
  An explicit range can include data; its start is caller-selected, not a proven
  function or instruction boundary.
- `calls` matches decoded near immediate call targets. `--include-jumps` adds
  immediate jump targets. Indirect/far transfers are counted as unresolved;
  matching constants in unrelated instructions are not callers.
- `field` returns literal displacement and overlapping access-width candidates,
  with operand index, base/index/segment registers and Capstone access flags.
  `--width` describes the queried field's byte extent. A numeric displacement
  does not identify the receiver class. `--nearby <N>` (default16) separately
  includes LEAs within that displacement distance; LEAs form addresses and are
  not reported as reads/writes. Pointer aliases and derived addresses remain
  outside this scan's proof.
  Displacements are compared literally as Capstone reports them: use signed
  decimal `field -4` for `[ecx - 4]`; `0xfffffffc` is a different unsigned value.
  Absolute memory addresses such as `[0xffffffff]` remain unsigned. The tool
  does not reinterpret these encodings as the same field.
- `find-bytes` scans all file-backed sections by default, including data, and
  includes overlapping hits. An optional explicit range uses the same paired
  flags. Matches crossing section boundaries, PE headers and unbacked bytes
  are excluded. A pattern match does not establish executable code.

Disassembly and instruction scans share one Capstone loop. Each range reports
its byte extent, decoded instruction/byte counts and every undecoded interval.
Skip-data resynchronization can find candidate instructions after invalid bytes;
it cannot prove they are true boundaries. Linear sweep can also decode embedded
data successfully. Neither an empty result nor a clean decode proves absence of
aliases, unreachable code, complete callers or active-YR reachability. Use original
callers, gates and checked execution for those claims; see the
[Ghidra workflow](../docs/research/ghidra-workflow.md).

## Reuse and validation

Python callers that need checked static bytes can use
`native_oracle.file_span(native_oracle.image_bytes(), va, size)`, which returns
`(raw_offset, bytes)`. The inspection module's `selected_ranges`, `decode_ranges`,
`calls`, `field` and `find_bytes` own the generic scan behavior. Mechanism-specific
interpretation and runtime-memory inspection remain with their current oracle;
these static scans must not replace observations of initialized or patched memory.

```sh
python -m unittest tools.tests.test_native_image tools.tests.test_native_inspect -v
python -m tools.run_tests
```

Portable tests use synthetic PE/x86 inputs: unequal VA/file offsets, BSS, malformed
headers, section boundaries, truncated instructions, near/indirect calls, immediate
data, read/write overlap, LEA semantics and overlapping byte matches. Live pinned
smoke reads are `0x4B6640` → `32c0c20400`, `0x773070` →
`8b81a000000083ec08`, and `0x8610B4` → `0000000058f4c73c`.
These establish byte mapping and decoder operation, not gameplay parity.
