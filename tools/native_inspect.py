"""Identify candidate images; read/scan the pinned retail executable.

See tools/native_inspect.md. Candidate identification never enables execution.

Static byte/instruction evidence only: linear sweep does not establish instruction
boundaries, active reachability, class ownership or exhaustive cross-references.
"""
from __future__ import annotations

import argparse
import hashlib
import importlib
import json
from pathlib import Path
import sys

import capstone
from capstone import CS_AC_READ, CS_AC_WRITE, CS_ARCH_X86, CS_GRP_CALL, CS_GRP_JUMP, CS_MODE_32, Cs
from capstone.x86_const import X86_INS_CALL, X86_INS_LEA, X86_OP_IMM, X86_OP_MEM

from tools import native_oracle as native

EXECUTABLE = 0x20000000
STATIC_LIMITS = [
    'Static file bytes only; runtime initialization, relocations and patches are not represented.',
    'Linear sweep and a requested start address do not establish valid instruction boundaries or active reachability.',
    'Undecodable bytes are reported; resynchronization after them can misidentify instructions.',
]
# Ranges remain with their existing fixture owners; goldens are read, never rewritten.
IDENTITY_REFERENCES = {
    'ramp-height': ('tools.ramp_height_oracle', 'ramp_height_vectors.json'),
    'foot-z': ('tools.render_depth_oracle', 'render_depth_vectors.json'),
}


def section_rows(data: bytes) -> list[dict]:
    return [dict(index=index, address=native.IMAGE_BASE + rva, file_offset=raw,
                 file_bytes=size, virtual_bytes=virtual, flags=flags)
            for index, (rva, raw, size, virtual, flags) in enumerate(native._sections(data))]


def fingerprint_rows(data: bytes, regions: dict, reference: dict) -> list[dict]:
    """Compare only the existing owner's file-backed regions, without emulation."""
    hashes = reference.get('region_sha256')
    if (reference.get('native_sha256') != native.NATIVE_SHA256
            or not isinstance(hashes, dict) or set(hashes) != set(regions)):
        raise ValueError('Reference must identify the pinned image and every owner region')
    rows = []
    for name, (start, end) in regions.items():
        expected = hashes[name]
        if (not isinstance(expected, str) or len(expected) != 64
                or any(c not in '0123456789abcdef' for c in expected)):
            raise ValueError('Reference region SHA-256 must be 64 lowercase hex digits')
        offset, payload = native.file_span(data, start, end - start)
        actual = hashlib.sha256(payload).hexdigest()
        rows.append(dict(name=name, address=start, bytes=len(payload), file_offset=offset,
                         sha256=actual, reference_sha256=expected, matches=actual == expected))
    return rows


def identity(data: bytes, references: list[str]) -> dict:
    """Describe the same immutable bytes hashed; matching samples cannot enroll them."""
    sections = section_rows(data)  # Shared PE validation, including every section.
    for section in sections:
        start = section['file_offset']
        section['sha256'] = hashlib.sha256(data[start:start + section['file_bytes']]).hexdigest()
    profiles = []
    for name in references:
        module_name, filename = IDENTITY_REFERENCES[name]
        owner = importlib.import_module(module_name)
        artifact = Path(__file__).with_name(filename).read_bytes()
        reference = json.loads(artifact)
        if not isinstance(reference, dict):
            raise ValueError('Reference artifact must be a JSON object')
        profiles.append(dict(name=name, owner=module_name, reference_file='tools/' + filename,
                             reference_file_sha256=hashlib.sha256(artifact).hexdigest(),
                             reference_native_sha256=reference.get('native_sha256'),
                             regions=fingerprint_rows(data, owner.REGIONS, reference)))
    digest = hashlib.sha256(data).hexdigest()
    return dict(sha256=digest, file_bytes=len(data), sections=sections,
                native_execution_supported=digest == native.NATIVE_SHA256,
                execution_sha256=native.NATIVE_SHA256, references=profiles,
                limits=['Identity/static region comparison only; no native code was executed.',
                        'Matching regions do not qualify other code, globals, callers, runtime initialization or gameplay.',
                        'Unsupported whole-image hashes remain rejected by all execution and byte/instruction inspection paths.'])


def selected_ranges(data: bytes, start: int | None, size: int | None, *, code_only: bool) -> list[dict]:
    if (start is None) != (size is None):
        raise ValueError('--start and --bytes must be supplied together')
    if start is not None:
        offset, payload = native.file_span(data, start, size)
        return [dict(address=start, file_offset=offset, bytes=payload)]
    return [dict(address=row['address'], file_offset=row['file_offset'],
                 bytes=data[row['file_offset']:row['file_offset'] + row['file_bytes']])
            for row in section_rows(data)
            if row['file_bytes'] and (not code_only or row['flags'] & EXECUTABLE)]


def instruction_row(ins) -> dict:
    return dict(address=ins.address, size=ins.size, bytes=bytes(ins.bytes).hex(),
                mnemonic=ins.mnemonic, operands=ins.op_str)


def decode_ranges(ranges: list[dict], select) -> dict:
    """One Capstone loop owns disassembly and scans; selectors own their meaning."""
    decoder = Cs(CS_ARCH_X86, CS_MODE_32)
    decoder.detail = True
    decoder.skipdata = True
    matches, coverage = [], []
    for span in ranges:
        start, payload = span['address'], span['bytes']
        skipped = []
        decoded_bytes = decoded_items = 0
        cursor = start

        def skip(address, size):
            if not size:
                return
            if skipped and skipped[-1]['address'] + skipped[-1]['bytes'] == address:
                skipped[-1]['bytes'] += size
            else:
                skipped.append(dict(address=address, bytes=size))

        for ins in decoder.disasm(payload, start):
            if ins.address < cursor or ins.address + ins.size > start + len(payload):
                raise native.OracleError('Disassembler returned an overlapping or out-of-range instruction')
            skip(cursor, ins.address - cursor)
            if ins.id == 0:  # Capstone skip-data pseudo-item has no operand detail.
                skip(ins.address, ins.size)
            else:
                decoded_bytes += ins.size
                decoded_items += 1
                matches.extend(select(ins))
            cursor = ins.address + ins.size
        skip(cursor, start + len(payload) - cursor)
        coverage.append(dict(address=start, file_offset=span['file_offset'], bytes=len(payload),
                             decoded_items=decoded_items, decoded_bytes=decoded_bytes,
                             undecoded_bytes=sum(row['bytes'] for row in skipped), undecoded_ranges=skipped))
    return dict(coverage=coverage, matches=matches)


def calls(ranges: list[dict], target: int, include_jumps: bool = False) -> dict:
    if not 0 <= target <= 0xFFFFFFFF:
        raise ValueError('Control-transfer target must be a 32-bit virtual address')
    counts = dict(direct_control_transfers=0, indirect_or_unresolved_control_transfers=0)

    def select(ins):
        call = ins.group(CS_GRP_CALL)
        jump = include_jumps and ins.group(CS_GRP_JUMP)
        if not (call or jump):
            return []
        # Far calls have selector+offset operands: do not treat a selector as a VA.
        if len(ins.operands) != 1 or ins.operands[0].type != X86_OP_IMM or (call and ins.id != X86_INS_CALL):
            counts['indirect_or_unresolved_control_transfers'] += 1
            return []
        counts['direct_control_transfers'] += 1
        destination = ins.operands[0].imm & 0xFFFFFFFF
        return [dict(**instruction_row(ins), transfer='call' if call else 'jump', target=destination)] if destination == target else []

    report = decode_ranges(ranges, select)
    report.update(counts)
    report['limits'] = STATIC_LIMITS + ['Only decoded immediate control transfers are matched; indirect calls and dataflow aliases are outside coverage.']
    return report


def field(ranges: list[dict], offset: int, width: int = 1, nearby: int = 16) -> dict:
    if not -(1 << 31) <= offset <= 0xFFFFFFFF or not 0 < width <= 0x100000000 or nearby < 0:
        raise ValueError('Use a 32-bit displacement, positive field width and nonnegative LEA distance')

    def select(ins):
        rows = []
        for index, operand in enumerate(ins.operands):
            if operand.type != X86_OP_MEM:
                continue
            displacement = operand.mem.disp
            formation = ins.id == X86_INS_LEA
            exact = displacement == offset
            overlaps = displacement < offset + width and offset < displacement + operand.size
            if not (abs(displacement - offset) <= nearby if formation else exact or overlaps):
                continue
            rows.append(dict(**instruction_row(ins), operand_index=index,
                             displacement=displacement, access_bytes=0 if formation else operand.size,
                             exact_displacement=exact, overlaps_field=False if formation else overlaps,
                             address_formation=formation,
                             read=False if formation else bool(operand.access & CS_AC_READ),
                             write=False if formation else bool(operand.access & CS_AC_WRITE),
                             access_metadata=operand.access,
                             base=ins.reg_name(operand.mem.base) or None,
                             index=ins.reg_name(operand.mem.index) or None,
                             scale=operand.mem.scale, segment=ins.reg_name(operand.mem.segment) or None))
        return rows

    report = decode_ranges(ranges, select)
    report['limits'] = STATIC_LIMITS + [
        'Literal memory displacements and overlapping access widths are candidates, not object/class identities or an alias proof.',
        'LEAs form addresses, not memory accesses; nearby LEAs are reported separately. Access flags are Capstone metadata.',
    ]
    return report


def find_bytes(ranges: list[dict], pattern: bytes) -> dict:
    if not pattern:
        raise ValueError('Byte pattern must not be empty')
    matches = []
    for span in ranges:
        start = 0
        while (at := span['bytes'].find(pattern, start)) >= 0:
            matches.append(dict(address=span['address'] + at, file_offset=span['file_offset'] + at))
            start = at + 1  # Include overlapping matches.
    return dict(matches=matches, coverage=[dict(address=s['address'], file_offset=s['file_offset'],
                                                bytes=len(s['bytes'])) for s in ranges],
                limits=['Exact bytes within each selected file-backed span; PE headers, gaps, BSS and cross-section patterns are excluded.',
                        'Byte matches do not establish code, function boundaries or reachability.'])


def integer(value: str) -> int:
    try:
        return int(value, 0)
    except ValueError as error:
        raise argparse.ArgumentTypeError('Expected a decimal or 0x-prefixed integer') from error


def parser() -> argparse.ArgumentParser:
    cli = argparse.ArgumentParser(description=__doc__)
    commands = cli.add_subparsers(dest='command', required=True)
    command = commands.add_parser('identity', help='Identify a candidate PE without enrolling or executing it')
    command.add_argument('--reference', choices=IDENTITY_REFERENCES, action='append', default=[],
                         help='Compare an existing fixture owner’s stored region hashes; repeat for multiple owners')
    commands.add_parser('sections', help='Describe checked PE sections and file backing')
    for name in ('read', 'disasm'):
        command = commands.add_parser(name, help='Read bytes' if name == 'read' else 'Disassemble a file-backed range')
        command.add_argument('address', type=integer)
        command.add_argument('--bytes', type=integer, required=True)
    command = commands.add_parser('calls', help='Find decoded direct callers of a VA')
    command.add_argument('target', type=integer)
    command.add_argument('--include-jumps', action='store_true', help='Also match immediate jump targets')
    command = commands.add_parser('field', help='Find literal displacement and overlapping access candidates')
    command.add_argument('offset', type=integer)
    command.add_argument('--width', type=integer, default=1)
    command.add_argument('--nearby', type=integer, default=16, help='LEA displacement distance (default16)')
    command = commands.add_parser('find-bytes', help='Find an exact hexadecimal byte pattern, including overlapping hits')
    command.add_argument('pattern', help='Quoted hex bytes, for example "32 c0 c2 04 00"')
    for name in ('calls', 'field', 'find-bytes'):
        command = commands.choices[name]
        command.add_argument('--start', type=integer, help='Optional explicit range start VA')
        command.add_argument('--bytes', type=integer, help='Explicit range length; requires --start')
    return cli


def inspect(data: bytes, options: argparse.Namespace) -> dict:
    if options.command == 'identity':
        return identity(data, options.reference)
    if options.command == 'sections':
        return dict(sections=section_rows(data), limits=['Section virtual tails can be BSS, not bytes from the executable.'])
    if options.command == 'read':
        offset, payload = native.file_span(data, options.address, options.bytes)
        return dict(address=options.address, file_offset=offset, bytes=payload.hex(),
                    limits=['Original file bytes only; no emulation or runtime initialization.'])
    if options.command == 'disasm':
        ranges = selected_ranges(data, options.address, options.bytes, code_only=False)
        return dict(**decode_ranges(ranges, lambda ins: [instruction_row(ins)]), limits=STATIC_LIMITS)
    ranges = selected_ranges(data, options.start, options.bytes, code_only=options.command != 'find-bytes')
    if options.command == 'calls':
        return calls(ranges, options.target, options.include_jumps)
    if options.command == 'field':
        return field(ranges, options.offset, options.width, options.nearby)
    return find_bytes(ranges, bytes.fromhex(options.pattern))


def main(argv: list[str] | None = None) -> int:
    options = parser().parse_args(argv)  # Import/help never opens the executable.
    try:
        data = (native.configured_gamemd().read_bytes() if options.command == 'identity'
                else native.image_bytes())
        result = inspect(data, options)
        packet = dict(schema=1, native_sha256=hashlib.sha256(data).hexdigest(), image_base=native.IMAGE_BASE,
                      capstone_version=capstone.__version__, request=vars(options), result=result)
        print(json.dumps(packet, indent=2))
        return 0
    except (native.OracleError, OSError, ValueError, capstone.CsError) as error:
        print(f'native_inspect: {error}', file=sys.stderr)
        return 2


if __name__ == '__main__':
    raise SystemExit(main())
