"""Literal original Steam helpers reached by live Building and Terrain readers.

Declarative enrollment only. No execution, callbacks, fixtures or sinks.
See steam_live_reader_helpers_scope.md for the bounded Windows import contract.
"""

LIVE_READER_HELPER_REGIONS = (
    # Concrete Terrain image getter through original primary vtable+9C.
    (0x41CFA0, 0x41CFA7, "aabd205c59f5a2ae488fe7441a532856f43654015b0bf5af7c8432912465f8b7"),
    # Building MuzzleFlash / DamageFireOffset suffix conversion: original _itoa.
    (0x7D468C, 0x7D46B9, "0b10051bfe983a39084ed57ab72f0bd42db98bbb410280c695c0bf184fb02308"),
    (0x7D46B9, 0x7D4715, "54f936226be9f51f7f9ab44240f5dbece70134c0aa2cd2fcbf98441ee7e33527"),
    # Terrain frame-color wrapper; existing asset owner retains69E580/69E930.
    (0x69E860, 0x69E8CA, "ccdf076f3656eb13b68e73e8e00e6611b9512379f7b973e550ce357d1027e797"),
)

LIVE_READER_HELPER_READ_ONLY = (
    (0x7F54F4, 4),  # Original Terrain primary vtable+9C points to41CFA0.
    (0x7E36A8, 4),  # Original Anim primary vtable+A0 points to427B50.
    (0x81A634, 12),  # AddOccupy%d plus NUL.
    (0x81A624, 15),  # RemoveOccupy%d plus NUL.
    (0x7E14B0, 4),   # Original USER32.dll!wsprintfA import slot.
)

LIVE_READER_HELPER_DATA_SHA256 = {
    "0x007F54F4:4": "d83ed6eae01db6c93c6998f74a53b6dbdd5b3fa1105c73f78e1c7228c5dfbdb4",
    "0x007E36A8:4": "b606e4e9ca7004a4d89c4e0e8854932d37bc0b5c2a3b4f82bc6520659b8f0839",
    "0x0081A634:12": "36f59756e6cbaa25c18f7332b6a85bcda86a2f723d93f3ce3c750470d505feb8",
    "0x0081A624:15": "2fb9c1ac38073a478621c8324d4f3ae74edf76ddde74e6c44c0becd5ae195e77",
    "0x007E14B0:4": "b8d50566df5511b781d7e87b1d5737fd053ca08c33ed072d6027aa54f4f80ffb",
}

# Metadata for the separately owned bounded Windows import transport.
# Argument and destination offsets refer to ESP BEFORE the original CALL.
# The original caller performs ADD ESP,12 after the import returns (cdecl).
LIVE_READER_WS_PRINTF_CALLS = (
    {
        "site": 0x461442, "iat": 0x7E14B0,
        "instruction_bytes": "ff15b0147e00", "instruction_bytes_count": 6,
        "argument_bytes": 12, "cleanup_bytes": 0,
        "destination_argument_offset": 0, "format_argument_offset": 4,
        "integer_argument_offset": 8,
        "format_address": 0x81A634, "format_bytes": b"AddOccupy%d\0",
        "prefix_bytes": b"AddOccupy", "index_min": 1, "index_max": 8,
        "destination_sp_offset": 0x38, "stack_reads": ((0, 12),),
        "stack_writes": ((0x38, 11),), "result_characters": 10,
        "caller_cleanup_site": 0x46144D,
    },
    {
        "site": 0x461495, "iat": 0x7E14B0,
        "instruction_bytes": "ff15b0147e00", "instruction_bytes_count": 6,
        "argument_bytes": 12, "cleanup_bytes": 0,
        "destination_argument_offset": 0, "format_argument_offset": 4,
        "integer_argument_offset": 8,
        "format_address": 0x81A624, "format_bytes": b"RemoveOccupy%d\0",
        "prefix_bytes": b"RemoveOccupy", "index_min": 1, "index_max": 8,
        "destination_sp_offset": 0x38, "stack_reads": ((0, 12),),
        "stack_writes": ((0x38, 14),), "result_characters": 13,
        "caller_cleanup_site": 0x4614A0,
    },
)
