"""Literal Steam EVA prerequisites of the original Building type reader.

Native SHA256: 3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600.
Declaration only; no discovery, execution, fixture writes or catalog injection.
The ordered startup owner executes the original CRT callback before Scenario;
the asset owner supplies full physical EVAMD lexical input to original readers.
Theme is excluded: 474FA0 resolves EVA, and no live Theme dependency is proven.
"""
from tools.native_oracle import RET_MAGIC


EVA_COLD_ENTRY = 0x752210
EVA_COLD_TABLE_INDEX = 3484
EVA_COLD_TABLE_SLOT = 0x815670
EVA_REGISTRY = 0xB1D4A0
EVA_REGISTRY_BYTES = 24
EVA_REGISTRY_VTABLE = 0x7F6904
EVA_EXIT_CALLBACK = 0x752250
EVA_CLEAR_ENTRY = 0x7531A0
EVA_LOAD_ENTRY = 0x753000
EVA_LOOKUP_ENTRY = 0x753250
EVA_ENTRY_BYTES = 0x54

CATALOG_REGIONS = (
    # Original empty registry initialization and CRT exit registration.
    (0x752210, 0x75224D, "1fde5d7044138c9e01d56fef7ceb536f91d31dd8521686d7f9eb1fe469e62e99"),
    # Original full source-order DialogList allocation/deduplication/read loop.
    (0x753000, 0x7531A0, "2519f3b587f34db0d657b0047d1901dc87a139ac872f50773814b117d5684fe2"),
    # Original Volume/Type/Priority/Yuri/Russian/Allied entry reader.
    (0x752DB0, 0x752FF8, "3ab0366ca31d0ff8796e018569b1403453c0338adcfafb3b314b398337c7fbd2"),
    # CaptureEvaEvent's original case-insensitive source-order lookup.
    (0x753250, 0x753293, "9a785b8a3856bbc7487faf9f04b877d5d56b0f448af70806d81ba94eabb2effa"),
    # Registry virtual +8 resize and its virtual +C empty-vector clear.
    (0x753830, 0x7538E0, "8a5925ac132a1f23273332dad015f89af6933ea1beaf6c249ca733d6723e567c"),
    (0x753650, 0x75367A, "8a887055d76c4c02b0ced2295c8a76011fe581cea85a6ceb56e90e7931cadfba"),
    # Init_Game's original clear call, admitted only on cold empty state.
    (0x7531A0, 0x753242, "69ca85d1a8f9a84be70b946c421a193246031024e935e52c7ce1bcdc041c9c96"),
    (0x752370, 0x75245D, "573c7d79ab9912e16b26291f9fc7d5c0d7f4715364d5049c4eb5103710ef881c"),
)

CATALOG_READ_ONLY = (
    (0x7F6904, 16),  # Original registry virtual +8/+C targets.
    # Literal extents include terminal DWORD reads by original ASCII helpers.
    (0x8467D4, 12),  # DialogList
    (0x846568, 8),   # Volume
    (0x824314, 8),   # Type
    (0x8467CC, 8),   # QUEUE
    (0x8467C0, 12),  # STANDARD
    (0x816120, 12),  # INTERRUPT
    (0x8467AC, 20),  # QUEUED_INTERRUPT
    (0x84301C, 12),  # Priority
    (0x8161DC, 4),   # LOW
    (0x8161D4, 8),   # NORMAL
    (0x8467A0, 12),  # IMPORTANT
    (0x8161C0, 12),  # CRITICAL
    (0x846798, 8),   # Yuri
    (0x846790, 8),   # Russian
    (0x846788, 8),   # Allied
    # Cold clear reads these untouched loader-zero globals and skips playback.
    (0xB1D4BC, 4),
    (0xB1D4C4, 4),
    (0xB1D4CC, 4),
)

CATALOG_NATIVE_DATA = ((EVA_REGISTRY, EVA_REGISTRY_BYTES),)
CATALOG_ENTRIES = tuple((entry, (RET_MAGIC,)) for entry in (
    EVA_COLD_ENTRY, EVA_CLEAR_ENTRY, EVA_LOAD_ENTRY, EVA_LOOKUP_ENTRY,
))
