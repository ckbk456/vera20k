"""Literal Steam missing-CSF-label wide formatter dependency declarations.

Original SHA256: 3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
Extends the existing 7D21BE..7D2233 formatter prefix. No execution, discovery,
fixture writes, fabricated output, broad data grants or private string corpus.
Only cold C-locale ASCII %hs and owned in-memory wide output are qualified by
the selected caller. Other switch cases still fail closed at unowned helpers.
"""
from tools.native_oracle import EdiImportTransport,ImportTransport

FORMATTER_REGIONS = (
    # Complete original eight-way formatter switch body, through original RET.
    (0x7D2233, 0x7D28EB, "24c4da678316c58ef64a2c13bd76e7fa187b216e06b1e1bb8d2602b84bf41a87"),
    # Original wide-character write/count, padding and wide-string output loops.
    (0x7D290B, 0x7D292B, "ccb0449d949f8112040485da9c00426aeb40772c8dd2ad07450c00477aacce03"),
    (0x7D292B, 0x7D295C, "a0b5fe923f6826dbeb2c80c220a63a1bd70445ab97459b7786a0a974ad8b118f"),
    (0x7D295C, 0x7D2995, "87fc0b6b6ab29f08917f6e85b523a5bc4148c64af66fd9ed7f591aca59730d14"),
    # Original DWORD vararg cursor, used for the narrow label pointer.
    (0x7D2995, 0x7D29A2, "639148f2f162bda27c1f66ab90d68794bac59a533c7cbf65580a2c6853ef771f"),
    # Original in-memory wide-character FILE output (flag0x40).
    (0x7D2FC8, 0x7D30C1, "9efb43019ef574599762960c16211d80319929b726c14f5fbd84d7a7be922502"),
    # Original locale-reader counter wrapper and native mbtowc body.
    (0x7D9D7F, 0x7D9DDC, "b850f01bfadd3fb3fc4e3877c573c90d90542dd0e7b9ed12fefd55c8dfe7b158"),
    (0x7D9DDC, 0x7D9EA5, "e54202f90d8a43713e3582c13ea48552517e342ddc87621a0eff85bd57e686ba"),
)

FORMATTER_SWITCH_TABLE = 0x7D28EB
FORMATTER_SWITCH_TARGETS = (
    0x7D2359, 0x7D2233, 0x7D224E, 0x7D2299,
    0x7D22D1, 0x7D22D9, 0x7D2312, 0x7D2375,
)

FORMATTER_READ_ONLY = (
    (FORMATTER_SWITCH_TABLE, 32),  # cmpEAX7 bounds eight original DWORDs.
    # Character classes for0x20..0x78 and overlapped state transitions. The
    # original classification low nibble never exceeds8; valid dispatch state
    # is bounded0..7. The selected original format visits states0,1,6,7.
    (0x7F97EC, 89),
    (0x845820, 28),  # Original missing-label wide format, including UTF16 NUL.
    (0x7E11C8, 4),  # Original InterlockedIncrement IAT DWORD.
    (0x7E11CC, 4),  # Original InterlockedDecrement IAT DWORD.
    (0xB78BA0, 4),  # Untouched loader-zero locale mutation flag.
    (0xB782A0, 4),  # Untouched loader-zero C-locale codepage.
)

# File-backed data identities only; BSS flags have no file-backed byte span.
FORMATTER_DATA_SHA256 = (
    (0x7D28EB, 32, "2f3af4d962946551e1d1b575e75e8dcefe955be2a9e8382aee66e39058f6df29"),
    (0x7F97EC, 89, "dc1a434091c9556591738b4d80d697c4e4d915c53fc9c26667938b7cb1f48f17"),
    (0x845820, 28, "afb2e7b4ba0adec74ff57aa8886b31a89e76afbe327a6412b84d88c843e4bdef"),
    (0x7E11C8, 4, "4516da656103affed3838a218839d6bad154c06737c657c6b8c7c86400f3eb7a"),
    (0x7E11CC, 4, "abd06c01798a6852ef01cb3d94caed607870e8a5ef383c3d19d47059585a7374"),
)

FORMATTER_NATIVE_DATA = (
    (0xB78BA4, 4),  # Native atomic locale-reader counter: increment then decrement.
)

# Call declarations for the existing transport owner to enroll, with exactly
# one guest DWORD argument. Register-call provenance requires EDI to equal the
# original unmodified 7E11CC IAT payload; no imported body is emulated here.
FORMATTER_INTERLOCKED_CALLS = (
    (0x7D9D8B, 0x7E11C8, 4, "memory", +1),
    (0x7D9DD2, 0x7E11CC, 4, "edi", -1),
)
FORMATTER_INTERLOCKED_ARGUMENT = 0xB78BA4
FORMATTER_TRANSPORTS = tuple((EdiImportTransport if register=='edi'else ImportTransport)(site,iat,size)
    for site,iat,size,register,delta in FORMATTER_INTERLOCKED_CALLS)

# Existing native owner entry734E60 uses fastcall ECX=label and EDX=optional
# extra-value output pointer. Caller410B52 passes EDX0 and two callee-cleaned
# stack arguments: source file pointer, then source line215.
MISSING_LOOKUP_ENTRY = 0x734E60
MISSING_LOOKUP_CALLER = 0x410B57
MISSING_LOOKUP_SOURCE_FILE = 0x817830
MISSING_LOOKUP_SOURCE_LINE = 0xD7
MISSING_LOOKUP_STACK_BYTES = 8
MISSING_LOOKUP_ALLOCATION_BYTES = 0x208

# Existing historical prereader scope owns the authentic one-byte logging RET
# at4068E0; no new sink, replacement logger or duplicate region is needed.
MISSING_LOOKUP_LOG_ENTRY = 0x4068E0
