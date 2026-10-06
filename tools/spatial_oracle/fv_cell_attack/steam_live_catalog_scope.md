# Original live-reader EVA prerequisite

Authenticated Steam `gamemd.exe` SHA-256:
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
The literal declarations in `steam_live_catalog_scope.py` were derived from
identity-checked file-backed spans and Capstone instruction reading. This is
static evidence; declarations alone establish no successful native execution.

The live Building reader `45FE50` reads `CaptureEvaEvent` (`81AC90`) at
`460258`, passes the incoming rules section and current `+1554` default to
`474FA0` at `460260`, and stores its result at `460265`. A nonempty key value
reaches `474FD4 -> 753250`. The latter compares names case-insensitively against
the array at `B1D4A4`, using count `B1D4B0`, and returns the source-order index
or `-1`. `474FA0` is an EVA reader; its earlier Theme annotation is incorrect.
Retail building sections author `CaptureEvaEvent`, so an empty registry would
silently lose an active required input even if the lookup code were enrolled.

The original 3945-entry CRT table at `812000` selects EVA callback `752210`
at ordinal 3484, slot `815670`, after Sound ordinal 3470 (`750300`). The
ordered startup owner must select this callback on its new fresh live profile,
execute it in ascending table order before Scenario, and preserve its destructor
registration `752250`. It initializes the 24-byte vector at `B1D4A0` with
vtable `7F6904`, empty pointer/capacity/count, valid flag 1, ownership flag 0
and capacity increment 10. Supplying vector bytes or repairing it later is
outside this declaration.

Original Init_Game loads SOUNDMD first (`52C796 -> 7510D0`), then selects
`EVAMD.INI` (`825DF0`, filename call `52C7AF`), clears EVA at
`52C894 -> 7531A0` and reads it at `52C8A0 -> 753000`. The physical source
owner must supply the complete, independent EVAMD lexical cache. The loader
receives ECX=INI with no stack arguments; it walks every ordered `DialogList`
value, reuses existing case-insensitive names, allocates original `54`-byte
records, and calls `752DB0` with ECX=record and one stack INI argument (`RET 4`).
That original entry reader reads Volume, Type, Priority, Yuri, Russian and
Allied. No parsed entry fields or selected EVA indices are supplied. Validate
the entire resulting name order against the physical source, including native
duplicate-name handling, before continuing live types.

The selected clear call runs only on the original cold empty registry and
loader-zero `B1D4BC/B1D4C4/B1D4CC`. Nonzero playback/queue state is not supplied
or enrolled. The resize body and its empty-vector clear are enrolled explicitly;
allocator, ASCII, lexical INI and CRT exit leaves remain with existing owners.
Only the native registry has new write authority; there are no fixture grants.

Theme is excluded from this bounded prerequisite. Native startup separately
selects THEMEMD (`825D94`), clears `A83D10` through `720770` at `52C918`,
loads `720590` at `52C92A` and scans physical music through `7207F0` at
`52C934`. Its actual name resolver is `721210`, with array `g_Theme+18` and
count `+24`. No key-to-that-resolver path has been established in the selected
16 live type readers. Startup proximity or the incorrect `474FA0` annotation
does not justify adding Theme state, helpers or physical music inputs.
Vanilla Steam also contains no `EVA.UnitLost`, `EVA.Sold`, `EVA.Destroyed` or
`EVA.UnderAttack` key literals; those names do not establish dependencies here.

Limits: supplied physical lexical input and checked host I/O; no complete
Windows startup, audio playback, EVA queue lifecycle, scenario placement or
Move/Stop/resume parity claim. Any newly reached undeclared path must fail
closed and receive its own original-caller/data review.
