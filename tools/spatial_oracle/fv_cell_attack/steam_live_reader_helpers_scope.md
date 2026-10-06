# Original live reader helpers

The declarations identify only original Steam image bytes with SHA256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
They contain no discovery, emulation, fixture patches, callbacks or sinks.
Static inspection does not establish retail execution or W02 parity.

Anim primary reader `427D00` dispatches its image accessor at `427DDD` through
vtable slot+A0. Original word `7E36A8` is `427B50`; the four-byte grant retains
its literal digest. The accessor's original body remains with the existing type
scope. This slot was reached by the fresh joined run and independently by the
TWLT100 primary-body control; no accessor result or virtual pointer is supplied.

Building reader `45FE50` calls original `_itoa` at `4602DF` and `4603D4`
to form indexed `MuzzleFlash` (`81AC74`) and `DamageFireOffset` (`81AC60`)
keys. The caller supplies radix10 and stack destination. Original wrapper
`7D468C..7D46B9` calls leaf `7D46B9` at `7D46AC`; the wrapper returns the
destination pointer and leaves caller argument cleanup to native code. The
leaf divides the supplied integer by its radix, writes digits, terminates and
reverses them in native code. Neither root has further helper or fixed-table
dependencies. Their literal regions include every rooted direct branch and RET.

Terrain always dispatches its image getter at `71DFCA` through primary
vtable+9C, after Object reading succeeds. Original slot `7F54F4` contains
`41CFA0`; that seven-byte leaf returns the retained object pointer at+A4.
The null check follows the dispatch at `71DFD0`, so even a genuinely missing
SHP does not bypass the slot or leaf. Only this word and literal leaf are added.

Terrain reader `71DEA0` calls `69E860` at `71DFDD` after its original SHP
accessor returns a nonnull object. The wrapper calls existing asset-owned
`69E580` at `69E861`, reads signed16 frame count at data+6, compares frame
index using unsigned `JAE`, and forms a frame-header address with stride24
from data+8. It copies bytes+12/+13/+14 to the three-byte caller destination,
or writes native zero bytes for a null data pointer or failed frame bound.
Its RET8 preserves the original ABI. `69E580` and its `69E930` dependency
remain declared by `steam_live_asset_scope.py`; this module does not duplicate
them. Physical SHP bytes and native heap objects remain the data authority.

Building's original occupancy loop requires `USER32.dll!wsprintfA` at import
slot `7E14B0`. The two original six-byte CALL instructions are
`FF 15 B0 14 7E 00` at `461442` and `461495`. The original format pointers
are `81A634` (`AddOccupy%d`,12 bytes including NUL) and `81A624`
(`RemoveOccupy%d`,15 bytes including NUL). Exact file-backed hashes enroll
these two literals and the four-byte import slot.

The original loop stores initial index1 at `461425`. The tail increments the
index at `4614DF`, stores it at `4614E0`, then decrements the comparison
register at `4614E4`, compares it with8 at `4614E5` and branches back to
`461433` while less. Thus the import receives exactly indices1 through8.
It formats identity keys consumed by original `529880` at `461476` and
`4614C9`, using ART receiver `887180` and the original incoming image name.

At `461437` and `46148A`, native LEA forms the destination as ESP+`2C`
before three DWORD pushes. At the original CALL boundary this is
**PRE-CALL ESP+`38`**. Arguments are destination at ESP+0, format pointer at
ESP+4 and integer at ESP+8. The bounded transport must check these pointers,
literal format bytes, original call instruction/import identity and index
domain. Exact stack writes including NUL are `(0x38,11)` for `AddOccupy`
and `(0x38,14)` for `RemoveOccupy`; result character counts are10 and13.
The transport cleans **zero** argument bytes. Native caller ADD ESP,12 at
`46144D` or `4614A0` must execute after return.

The Windows import body is a separately supplied OS boundary, like the existing
Windows character-conversion imports. Supplying these two fixed ASCII key
patterns for indices1..8 does not execute or measure the Windows implementation,
qualify generic formatting, or establish numeric/gameplay parity. Every other
format, index, destination, import or callsite must fail closed. This scope
provides metadata for the runtime owner; it installs no transport itself.
