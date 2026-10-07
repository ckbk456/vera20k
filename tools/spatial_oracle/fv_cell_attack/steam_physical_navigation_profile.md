# Original Tiberium closure for the retained Rules.Process tail

The declaration owner remains `steam_physical_navigation_profile.py`.
`RULES_TIBERIUM_REGIONS`, `RULES_TIBERIUM_READ_ONLY`,
`RULES_TIBERIUM_NATIVE_DATA` and `RULES_TIBERIUM_ENTRIES` extend only the new
retained Rules tail profile. Existing physical profiles and control entry
points do not consume these additions. The source is original Steam
`gamemd.exe`, SHA256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
This is authenticated static closure; native execution evidence is separate.

The live parent already inherits the existing physical owner declarations:

| Existing authority | Extent | Original proof |
| --- | --- | --- |
| Cold registry initializer | `721640..72167D` | SHA256 `e6d0a3e4de5debb5c2afb6dc43ff857f9afdbc04d3c17a9aa152174e15ef02a0` |
| Named Tiberium constructor | `7216C0..72187E` | SHA256 `3c352c498af301fa2aca6fee238ad654f4a728c22f87a2686915dc0bbf5626ce` |
| Registry | `B0F4E8`, 24 bytes | Original initializer writes vtable `7F56BC`, empty count/capacity, owned-storage flags and growth 10 |
| Registry vtable | `7F56BC`, 28 bytes | SHA256 `7c7fdda06d6b0302d8b4ca388e6ebb5bf42844a251589a4a9212a6e041a6c440` |
| Image switch table | `721CF8`, 24 bytes | SHA256 `6c5dad683252e160e16a854cdfb3388b851446df9b139c01b406a238981b4ee7` |

The original CRT table index 3220, slot `815250`, contains `40 16 72 00`
(SHA256 `010ba0da7c63e75989e6763dd2b2a509834b02ab5e44f5e4b71dafb3cfb64d3c`).
The original cold callback must execute before Scenario construction. It also
registers exit `721680` through the existing `7C978A` boundary. Its code and
table slot are already granted by the parent; declaring the callback does not
establish execution or authorize late registry reset.

Full `721A50` ReadINI uses the supplied physical root INI as its stack argument
and the actual Tiberium receiver in ECX; its native returns pop four bytes.
The existing owner already declares `721AFA..721B12`, `721C3F..721C5C`,
`721C5C..721C7B` and `721C88..721CDC`. The additions fill only the remaining
original function bytes, excluding alignment padding and the following switch
table. Original `721D10` All receives the physical root INI in ECX with no
stack arguments, enumerates the original Tiberiums section, reads each name,
reuses an existing ordinal or allocates an original 0x128-byte object, and
invokes its primary virtual slot +0x64 at `721D9F`.

| Added code | Bytes | Original SHA256 |
| --- | ---: | --- |
| `721A50..721AFA` | 170 | `6d5183de7c54f6fa6e02fe89cf79ac94d71273293c2a4752a0fa55bbef1a3d89` |
| `721B12..721C3F` | 301 | `ef88c42a22de53b33367befac15aef8a5b75d4715578cb1d3b1ed73fd3cf14a4` |
| `721C7B..721C88` | 13 | `b5902c20b349b25dffece689edb470d48874cc646a13a51544b8e5189312120d` |
| `721CDC..721CF6` | 26 | `794eca6091bac2c13e01601d445e019bf1e65b9810ef4940e6753298c5d5997b` |
| `721D10..721DBA` | 170 | `89cd46d5fad87ef8006dea6e40fe7db90da2c52e63299b5eaa589843ff0e71ef` |

Only the exact four-byte slot `7F578C` is added for this virtual dispatch. Its
payload `50 1A 72 00` selects original `721A50`, SHA256
`ecc2fc7bb7d98b306ce83df89a96a7d5a84d1ad52776df1244f97707a5e00ee3`.
The missing NUL-terminated literals are Debris `8448E4/7`, GrowthPercentage
`8448F4/17`, Growth `844908/7`, SpreadPercentage `844910/17`, Spread
`844924/7` and Tiberiums `84492C/10`. Value, Power, Color, Image, empty-string
and comma literals remain with their existing owners. All direct helpers are
already admitted by the live parent: Abstract construction/ReadINI, scalar
and string INI readers, ColorScheme lookup, Anim lookup, native vector
construction/copy/growth/retirement, strtok/atoi and the allocator.

`physical_sections(..., names=None)` establishes source order Riparius,
Cruentus, Vinifera and Aboreus. Original Image values 1/2/3/4 select switch
indices 2/3/4/5 and Overlay registry ordinals 102/27/127/147, whose physical
source names are TIB01/GEM01/TIB2_01/TIB3_01. The reader obtains their actual
registered pointers from `A83D84`; these ordinals are observations, never
supplied pointers or image results. Riparius has no Debris key. The other
three rows select four CRYSTAL debris names already present in the physical
Animations list. The native reader and factory own their resolution and
vector contents; full retained Anim and Overlay masters must precede this
late reader.

`RULES_TIBERIUM_NATIVE_DATA` is empty because the parent already owns every
required mutable global and the native heap. No host registry header,
insertion, type index, scalar, palette, image or animation result is supplied.
Static declarations do not qualify arithmetic, list contents or execution of
the complete Rules tail. The qualification owner must record the retained
native Process return and actual objects/results; Session, House, placement,
rendering and gameplay acceptance remain outside this chain.
