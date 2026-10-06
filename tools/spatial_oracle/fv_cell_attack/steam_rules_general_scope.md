# Retained native General scope

`steam_rules_general_scope.py` declares immutable original code and read extents
for the selected W02 retained VM. It contains literal tuples only. The existing
startup owner must compose these declarations into a new optional profile before
creating its VM; historical profiles and artifacts keep their existing scope.

The reviewed image is SHA-256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
The original continuation calls AI `672AE0`, Powerups `673E80`, Land `674000`,
IQ `674240`, then General `66D530` at `668EE8`. Its next boundary is `668EED`.
General's rooted original extent is `66D530..671E99`; its absence branch returns
AL=0 and its present-section branch returns AL=1. Declaration hashes identify
original file bytes, not execution or complete startup parity.

## Receiver review

Original Rules constructor `665650` establishes the vector receivers:

| Vector | Derived vtable | Original constructor writer | General temporary writer |
| --- | --- | --- | --- |
| Anim pointers | `7EB6D4` | `665A43` at Rules+2A0, also other fields | `66D59F`, also other lists |
| Int values | `7E4DD8` | `665B53`, also other fields | `47712A`, also other readers |
| VoxelAnim pointers | `7F0D3C` | `6656E4`, `665EB4` | `66D719` |
| Building pointers | `7ED90C` | `66621E`, also other fields | `67B5AC` |
| Unit pointers | `7EABE8` | `666535`, `666558`, `6667CD` | `67B77C` |
| Aircraft pointers | `7EABC8` | `66657B` | `67B94C` |
| Infantry pointers | `7EAC08` | `66666F`, also other fields | `67BB6C` |
| Terrain pointers | `7F0CFC` | `666BF9` | `67BE2C` |

General list readers overwrite the generic constructor vtable before invoking
virtual growth at +8. Their copy/assignment paths invoke either the derived
clear at +C or a fixed original generic clear slot. Only these dispatch words
are added as read extents; unused method slots are excluded. Generic resize
candidates `50E950`, `513050`, `513420`, `512C80`, `67B230`, `67AB30`, `525110`
and `477C70` have no established active receiver on this path and are excluded.

Rules also constructs five float vectors with vtable `7F0D1C`, at +7C4, +7E0,
+7FC, +818 and +834 (`666192..666202`). Neither full General nor AI uses these
receiver fields. Their `67B050` growth and `67A680` clear bodies and dispatch
words are excluded. The Generic/Derived distinction must remain intact;
template address similarity does not establish receiver identity.

The scope reuses already enrolled original scalar readers, type factories and
constructors, Int/Building/Anim/Voxel derived clear bodies, and the existing
boolean jump table. It adds General and 63 reviewed helper extents. It creates
no allocation, delete, clock, TLS or OS service boundary.

## Read extents

Every declared literal has its original push site next to its NUL-inclusive
extent. General key readers `526810`, `5276D0`, `5283D0`, `528A10`, `5295F0`
calculate lengths with byte `REPNE SCASB`; CRC `4A1DE0` consumes byte loads.
Prerequisite category comparisons use the retained C-locale byte path at
`7C8D40/7C8D43`. Therefore these keys/categories require their string bytes
and NUL, with zero trailing word overread.

The DWORD loads in native `strncpy` at `7C9266/7C926F` can read three bytes
beyond a source NUL. That source is the cached INI value or default string,
not the key literal. Existing INI cache and empty-string ownership supplies
those extents. The comma tokenizer likewise reads its delimiter by byte at
`7C9CE3`; its existing delimiter extent is reused. Values that resemble ASCII
inside a vtable are handled as dispatch words, never as string declarations.

Additional absolute constants are the original DropPodAngle double bounds
(`7ED8A0`, `7F0DC0`, eight bytes each) and TalkBubbleTime's reciprocal float
(`7F0DB8`, four bytes). General uses the original reader, clamp and x87/ftol
instructions; this scope supplies no calculated field result.

## Type creation and remaining qualification

The physical retail General has `LargeVisceroid=VISC_LRG`,
`SmallVisceroid=VISC_SML`, and `DropPodWeapon=Vulcan2`. The first two names are
absent from VehicleTypes; no WeaponTypes master list exists. Original factories
`7480D0` at `66E67F/66E6B8` and `772FA0` at `66ECB8` can create these types.
The retained execution must preserve their actual allocations, registry order
and Scenario IDs. An unchanged counter or registry count is not an admission
condition. This static review does not predict the resulting IDs.

The declarations assume the existing cold Rules/registry/INI owners, retained
C-locale service prior and established CRT/WinMain numeric state. They must not
be used to admit arbitrary injected vector receivers or donor state. Dynamic
dispatch must resolve to the reviewed vtables. The reviewed new helper dispatches and absolute constants have identified
original targets/extents. Existing admitted descendants are reused, not
exhaustively rediscovered here. Actual retained execution still has to establish
active branches, allocation bounds, numeric outcomes and completion at `668EED`.

Static working receipts are under
`.local/fv-movement-validation/rules-general-20261006/`:
`general-closure-candidate-manifest.json`, `general-recursive-static.json`,
`general-direct-callee-static.json`, and `general-key-read-extents-static.json`.
They retain rooted callers, original ranges/hashes and candidate limits. The
declaration module does not read or enroll these JSON files at runtime.
Further native continuation, validation and publication belong to the W02
owner. No emulation, test, build or commit was performed for this review.
