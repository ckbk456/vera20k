# Ordered Bullet startup and retained live readers

This is a bounded native-tooling prerequisite for W02. It changes no Rust game
code. The delivery branch starts at `b43304db864b49979e2246317ebfd16a496ade49`
and excludes the held movement implementation and its unqualified corpora.

The authenticated Steam gamemd.exe is SHA-256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
Original bodies, exact immutable data and explicit host boundaries remain guarded
by the existing native oracle. Static declarations alone establish no parity.

## Initialization and ownership

The existing ordered CRT owner executes Bullet `4E75E0`, original table index
1184/slot `813280`, before Scenario construction. The actual callback writes the
24-byte `A83C80` registry and registers `4E7620`; no late initialization, donor
state or fixture header repair is allowed. Historical profiles stay unchanged.
Sound `750300` and EVA `752210` likewise execute in original selected CRT order
before Scenario. The live profile is selected at fresh VM creation.

The retained caller uses the existing native Rules/ART lexical cache, heap,
factories, constructors, palettes and prereader owners. The new live owner
continues `668EED -> 679A10 -> 668EF5` on the same actual Rules/INI/stack frame.
Its observer checks primary callsites, current registry membership, constructor
IDs/allocations, postpasses and all 32 MissionControls. RNG stores and observed
draws are retained as evidence, without claiming unchanged RNG by assumption.
See [literal type scope](../../tools/spatial_oracle/fv_cell_attack/steam_live_types_scope.md).

The existing physical-buffer reader owns guest asset pointers. The physical
supplier shares the stock MIX hash/index/decryption implementation and freezes
named archive order and member extents. Native File/RawFile, shape, voxel and HVA
bodies receive genuine bytes; real missing files take native failure branches.
Read-only Win32 transports check exact callsites and argument ABIs, including
three original `CALL EBP` seek sites. No write/device/unknown imports are granted.
See [asset boundaries](../../tools/spatial_oracle/fv_cell_attack/steam_live_assets.md)
and [EVA caller proof](../../tools/spatial_oracle/fv_cell_attack/steam_live_catalog_scope.md).

The original CSF comparator `7C8D20` folds ASCII letters to lowercase. Its
punctuation ordering differs from uppercase byte order. Supplied records now
sort by the native fold while retaining physical value ordinals and extra
payloads. Native `734E60` checks passed for all 5,211 physical labels and 14
actually absent retail UIName labels. Original missing-label `%hs` formatting
executes through its eight-way switch and native ASCII conversion, with two
checked single-thread Interlocked calls updating the original reader counter.
No missing string or formatter result is supplied. See the
[formatter scope](../../tools/spatial_oracle/fv_cell_attack/steam_live_formatter_scope.md).

Building's two occupancy-key `wsprintfA` sites remain explicitly supplied
Windows boundaries: only original patterns, indices 1–8, exact stack destinations
and caller-owned cleanup are admitted. The contract follows Microsoft's
[wsprintfA documentation](https://learn.microsoft.com/en-us/windows/win32/api/winuser/nf-winuser-wsprintfa).
Original `_itoa` and Terrain frame-color bodies execute; the Windows formatter
implementation is not executed or measured. See
[reader helper scope](../../tools/spatial_oracle/fv_cell_attack/steam_live_reader_helpers_scope.md).

Original `Full_Init` binds the incoming map's `[Map]/Theater` at
`687631..68764F`, before `6686C0` enters the root Rules.Process prefix.
The live owner reuses that native reader on a separate 58-byte Map-only cache,
then retains its original Scenario store. The physical map is source-bound;
ART and root Rules cache identities, ID counter and RNG remain intact.
The existing physical asset owner supplies the authenticated theater archive
registration order, then executes original palette-manager activation `6267A0`
on the retained cold manager. Its original store replaces index `-1` with the
same native theater selection before Process. Existing named-color vectors,
31 empty hash buckets and allocations remain unchanged. With a null manager,
the same original function constructs the manager, two vectors, hash table and
31 empty buckets through exactly five native allocations. Both branches retain
the ID counter and all three RNG stores; warm-entry reload is rejected. No host
index write or palette result substitution is allowed.
The native null/retained-manager controls both request genuine `LIBTEM.PAL`
bytes (768 bytes, SHA-256
`79e668c9bd08bc5eed811df19de2af418cf8b434b97abf1fe2d65809321507e0`)
and return a nonnull palette pointer in the owned native heap. Supplied RGB565
Surface properties remain an input boundary; render parity remains open.
Original later map Rules processing is outside this early binding. The supplied
boundary does not claim that the complete `Init_Theater` or `Full_Init` executed.

The stock GAAIRC/AMRADR `NumberOfDocks=4` path executes native vector resize
`465E70` and its complete clear branch `465F50`, through the original virtual
slots. Both complete primary-body controls grew the constructor's capacity1
to4 with native allocation. Armor's actual eleven-row pointer table is retained
in full. Native DWORD string copying admits only the precisely observed aligned
`None`/`yellow`/`DontCare` default extents. Helper declarations and enum labels follow
original constructor/caller/loop evidence; these controls certify closure under
stated cold priors, with joined qualification reported separately.

Native Sound and EVA loaders read complete physical definition lists before the
retained Process pass. Original disabled-output Sound factory establishes its
null-index state. The full decoded physical CSF cache is supplied through the
existing CSF parser; original native string lookup executes. Windows device
startup, archive traversal and original CSF parsing remain supplied boundaries.

The guard owner now indexes exact read/write/code ranges without coalescing
adjacent grants. It caches expected instruction/IAT bytes only within each
immutable file image, using the existing file-span parser on misses. Every
instruction still checks current mapped bytes and exact authorization; cache-hit
tamper and image/VM isolation controls retain those boundaries. Repeated lexical CRC results are cached only within the same
immutable image and machine, after an actual native call. Synthetic rejection
controls cover incorrect IAT/registers, ABI/stack misuse, straddling grants and
image changes; they are guard tests, not game parity.
The live dispatch has a finite 500-million-instruction/3,600-second bound,
selected after preserving a 1,200-second timeout at 166.7 million instructions
and Building entry 297. An observer reports every 50 actual primary entries
with their family and native name; it does not alter VM state or loop control.

The measured rejecting-IRO OleRun boundary is shared through the existing
Mission owner. Its public projection retains actual x86 callbacks, result,
reference counts and measured DLL identities, with a pinned projection digest
and original packet digest. Host/session metadata stays private. A matching
private original packet can still be used, and any wrong digest fails closed.

## Validation and reproducibility

Required commands run after sourcing the workspace `environment.sh`, with an
operator-owned authenticated installation and original physical Rules/ART and
palette inputs. No game files or extracted INIs/art are delivered in this PR.

```sh
python -m tools.spatial_oracle.fv_cell_attack.steam_bullet_startup_scope --check
python -m tools.spatial_oracle.fv_cell_attack.retained_startup_run \
  --scope live-types --run-name ordered-live-types-unique-name --execute
env -u VERA20K_GAMEMD_EXE python -m tools.run_tests
python tools/skill_sync.py --check
python tools/sim_field_ratchet.py --base delivery/main
VERA20K_REQUIRE_RETAIL_INI=1 VERA20K_REQUIRE_RETAIL_ASSETS=1 \
  python -m tools.cargo_run -- test -p vera20k --lib
VERA20K_REQUIRE_RETAIL_INI=1 VERA20K_REQUIRE_RETAIL_ASSETS=1 \
  python -m tools.cargo_run -- clippy -p vera20k --lib
VERA20K_REQUIRE_RETAIL_INI=1 VERA20K_REQUIRE_RETAIL_ASSETS=1 \
  python -m tools.cargo_run -- test --release -p vera20k --lib \
  headless_scenario::retail_construction_tests::retail_headless_funnel_construction_is_deterministic_and_populated \
  -- --ignored --exact
```

Set `VERA20K_FV_COLOR_PALETTES` to authenticated extracted palette inputs in a
fresh checkout. The retained runner refuses reused outputs or an equivalent
active process, freezes source owners and physical inputs, records diagnostics
at 900 seconds, and waits for the original child. A slow quadratic native
catalog loop is not bypassed. Failures and partial observations stay local and
cannot produce a successful live corpus. Full lexical/type/asset outputs stay
ignored because they contain retail material; publish only sanitized facts and
artifact/source hashes.

The standalone native controls establish complete SoundList loading (819 source
entries, 818 unique native records), all 470 EVA records and lookups, and actual
FV VXL/HVA parsing with genuine missing-barrel handling. These controls do not
certify the joined live type pass. Final joined qualification and command
results are recorded in the validation receipt before publication.

Local retail Rust validation passed 9,589 tests, with 231 explicitly ignored.
Clippy completed with the existing 729 warnings. The named release test loaded
retail assets and passed deterministic populated scenario construction. It is
headless map-loading evidence; no GUI, rendering or gameplay acceptance follows.

## Remaining W02 gates

Full Process after `668EF5`, accepted Session settings, House/map placement,
native paid Move/Stop/resume and hands-on gameplay acceptance stay open. This
PR does not deliver the held movement changes or claim numeric/rendering parity
for declaring native type bodies. Windows capture access remains separate.
