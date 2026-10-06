# Steam missing-CSF-label formatter dependency

`steam_live_formatter_scope.py` declares bounded original bytes from Steam
build15918130, whole-file SHA256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
This is static dependency enrollment. Its declarations do not establish a
successful type-reader run or W02 gameplay parity.

The original `AbstractType` UIName reader calls `734E60` at `410B52`, returning
to `410B57`. It passes ECX=the nonempty narrow label, EDX=0, and two stack
arguments, source file pointer `817830` and line `D7`; the original lookup uses
`RET8`. A physically missing label follows the original allocation of `208`
bytes, an intrusive list header at allocation+0, and wide output at allocation+4.
It then calls native wide sprintf `7CA564` with the original UTF16 format at
`845820` and the narrow label as its first vararg. The additional file/line
arguments are passed by the lookup, but this format does not consume them.

The preexisting scope stopped at formatter prefix `7D21BE..7D2233`. The actual
`JMP[EAX*4+7D28EB]` follows `CMP EAX,7` and `JA` to the loop tail. The eight
original DWORD targets are declared explicitly. The extension includes the
entire remaining switch body through its original `RET` at `7D28EA`; it never
executes the table bytes as code. The classifier reads characters20..78 from
`7F97CC+character`; its89-byte physical range is `7F97EC..7F9845`. The same
range contains the overlapped transition table. Original classifier values have
maximum class8; valid dispatch states are0..7, requiring at most72 bytes for
transition reads. The selected original format visits states0,1,6,7. Invalid
transition values take the original out-of-range dispatch branch and are not
qualified for arbitrary formats. This is an exact bounded table extent, not a guessed
string grant.

The selected original `%hs` branch takes a narrow ASCII label. It reads the
vararg using `7D2995`, measures its original C-locale narrow length, and converts
each byte using `7D9D7F -> 7D9DDC`. Untouched loader-zero `B782A0` selects the
native one-byte conversion, producing one UTF16 unit per byte. No locale or
formatted result is injected. The formatter's actual wide-write/count helpers
are `7D290B`, `7D292B`, and `7D295C`, which reach original `7D2FC8`; the owned
stack FILE created by `7CA564` has flag42 and a positive in-memory byte count,
so the wide-output branch uses its original buffer and never enters file IO.
The caller's31-byte maximum UIName fits the lookup's516-byte output payload.

`7D9D7F` increments the original locale-reader DWORD `B78BA4`, calls the native
conversion body, and decrements that same word before returning. The literal
IAT imports are **InterlockedIncrement** at `7E11C8` and
**InterlockedDecrement** at `7E11CC`, identified from the pinned PE import-name
records. They are not critical-section calls. The exact selected call sites
are `7D9D8B` (`FF15`, four argument bytes) and `7D9DD2` (`FFD7`, four argument
bytes, EDI loaded from the unchanged decrement IAT DWORD). Their transport owner
must enforce that exact argument pointer and native LONG update/return
semantics. No fixture write is declared for the counter. The unchanged
loader-zero mutation flag `B78BA0` bypasses the other lock13 routes.

The missing-label lookup calls original logging entry `4068E0`. That pinned
build's body is literally one `RET`, already owned by the prereader profile;
the extension introduces no logging sink or replacement. The native lookup
then links the actual allocation through existing writable head `B1CF88` and
returns its wide-output pointer. An isolated regression can use the existing
physical CSF preparation owner, invoke actual `734E60`, and compare returned
UTF16 output, original linked-list head, exact allocation extent, stack cleanup,
and unchanged final reader counter. Missing output must come from native
execution, never a fake lookup or formatter callback.

The declarations include complete switch bytes but do not qualify arbitrary
format strings. Floating-point conversion, numeric helper closure, non-ASCII
locale imports, nonzero locale-mutation lock13 routes, FILE exhaustion, and
external FILE IO remain outside this selected mechanism and fail closed at
their undeclared helper/import/data dependencies. Source strings, full CSF
values, retail files and host identities are excluded from this artifact.
