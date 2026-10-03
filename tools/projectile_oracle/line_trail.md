# DRAGON LineTrail input, lifecycle and pixels

`line_trail.py` executes the pinned active-retail executable. The physical input
set is the same selected Hills scenario as the IFV chain: RULESMD, absent
LANGRULE, MPBattleMD, Hills and fixed ARTMD. Its `source_files` records the exact
extracted-byte hashes. Archive traversal is supplied by the production asset
extraction boundary; this harness does not execute the native MIX filesystem.

Run from the repository using the native-oracle Python environment:

```sh
VERA20K_GAMEMD_EXE=/path/to/gamemd.exe \
VERA20K_PROJECTILE_RENDER_ASSETS=/path/to/extracted-inputs \
PYTHONPATH=. python tools/projectile_oracle/line_trail.py --check
```

The extraction directory needs ARTMD.INI, RULESMD.INI, MPBattleMD.ini, Hills.map
and dragon.shp. The local research set is `/tmp/bridge-ifv-assets-1dDM9D/extract`;
its frozen input manifest is
`/tmp/bridge-ifv-assets-1dDM9D/manifest-native-inputs.json`. The DRAGON SHA256 is
`f361b34efa27811f8f8cc5d12aed2e2b62b82e185bb1424f597a54d0682c09c2`.

## Original instructions and boundaries

The full original BulletType reader46BEE0 calls ObjectType5F9574..5F95E2 for
`UseLineTrail`, `LineTrailColor`, `LineTrailColorDecrement` in the retained ART
Image section. Native constructor defaults are false, RGB128/128/128,16.
Selected DRAGON reads true,216/216/255,16. Rules constructor66784C..66785E and
AudioVisual66B77D..66B7A7 independently establish override RGB0/0/0. Options
constructor5FA350 and reader5FA776..5FA7B4 establish DetailLevel default2 and
clamp0..2. Only detail0 doubles the copied decrement (556B50).

ObjectUnlimbo5F514B..5F5210 executes with prior world admission supplied. It
uses the actual Bullet vtable and selected type, allocates210 bytes, calls
original556A20, appends the plain registry, copies the selected RGB/decrement,
and writes both Object+A8 and trail+4. No Abstract identity or RNG is consumed.
Allocator and atexit services are supplied; no game-world admission is claimed.

Original556D40 visits the registry backwards. Each visit samples a changed
owner coordinate into a32-slot ring and starts strength255, then subtracts
the copied decrement from every slot in the SAME visit. There is no simulation
frame guard. Detach556B30 clears both owner links but retains history until a
later visit sees the unattached newest strength reach0. ZeroXYZ terminates the
draw walk. Existing rings do not reread Options/type/Rules configuration.

The segmented cadence witness executes original RenderFrame4F4480 and the
Tactical suffix6D4582..6D4678. With its original53BAE0 gate open, RenderFrame
calls passes0,1,2; only pass2 reaches LineTrail. A separately supplied pass3
also reaches it. Peripheral display virtuals, time service, and unrelated
scene families are substituted. MainThrottle55E160 and pause683EB0 callers
were inspected rather than executed in that historical segmented corpus. The
bounded Steam caller extension below executes their selected caller closure;
neither corpus establishes a fixed-Hz trail clock.

Original556C00 projects both endpoints through6D2140, supplies
`-2-AdjustForZ(Z)` and newer-sample strength to4BEAC0. The full original line
body clips XY via7BC2B0 and adjusts clipped endpoint Z using4C1B50
(Sqrt_Approx4CAC40 then ftol). Its dominant axis may be depth: the steep control
makes53 stores at49 pixels. Pixel order and repeated blending are observable.
It narrows candidate Z to u16 before strict comparison with stored Z, reads
u16 ABuffer, blends packed RGB565, and never writes depth. The42 individual pixel controls
cover geometry, clipping/origins, backgrounds, depth, A values and fade visits.
The RGB565 surface, scene Z/A contents and camera are supplied boundaries;
no full-scene lighting/visibility production or GPU parity is claimed here.

The2 persistence controls execute original AbstractSave410320, ClearAll556DF0
(single trail) and full BulletLoad46AE70 including ObjectLoad5F5E80. The356-byte
stream contains the old pointer token, but ObjectLoad5F5EED clears+A8 and never
queues that field for swizzle. No ring is restored by this object path. The
IStream transport is supplied; the whole game loader and post-load scene are
not executed. The separate joined impact witness
[`ifv_trail_impact`](ifv_trail_impact.md) reaches556B30 only from
physical Bullet destruction at ObjectDtor5F3D56; UnInit/conceal keeps it attached.

## Authenticated Steam caller admission extension

`line_trail.py --steam-cadence --check` reproduces
`line_trail_steam_cadence.json` and its provenance sidecar against Steam15918130
SHA256 `3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
Use `--write` only to deliberately regenerate this explicit profile. The global
historical binary gate and the original reader/pixel corpus remain unchanged.

The profile executes full Main55D360, original RenderFrame4F4480 and gate53BAE0,
full Tactical6D3D10, the actual registry556D40, ring556B70, native vector resize
and Find557140, detach556B30, full offline Throttle55E160 through its return,
the modal display suffix683F66 and offline modal pump623120. It guards original
code bytes and declares data/fixture/sink boundaries through `native_oracle`.
Each case saves actual instruction visits separately from supplied boundaries.

Eight controls cover pre-Logic sampling over repeated normal calls, repeated
Scenario-depth pause, render suppression and recovery, offline modal entry plus
three pumps, one serviced positive wait, a5000ms stall, repeated uncapped calls,
and detach through native registry removal/deletion. Normal Main reaches one
pass2 ring callback before the supplied Logic boundary; the first callback sees
the old coordinate, and the next sees the Logic sink's previous output. A
Scenario-depth pause samples without Logic or frame increment. Gate1 skips
Tactical/ring but proceeds through Logic. Modal entry's SetRedraw2 forced branch
samples once; its offline pump reaches no Main/Render. The positive offline wait
services once without another composite; stall still admits one frame/sample.
The stall also executes Main's signed wall-delta cap1000, independently of the
ring's single decrement. Commands, frame increment and pending-drain ordering
are saved; commands/Logic/pending bodies are declared external boundaries.

Both clocks share the existing `fast_scroll.ThrottleServices` input owner. The
full Throttle FPS epilogue55E33B..55E404 is enrolled here, with actual counter
storage and its additional clock reads. `clock_reads.reader` identifies the
shifted-clock or raw-millisecond input stream; direct Main timeGetTime visits
use the raw stream too. `time_get_time_return_addresses` distinguishes their
actual caller return addresses. FPCW0E7F is explicit, inherited from the original
LineTrail fixture; the enrolled cadence/ring arithmetic is integer. No new
numeric port or clock implementation is introduced.

The shared service refactor rebinds only the prior Steam clock producer hash.
Its executable rerun preserved `fast_scroll.steam-clock.json` byte for byte:
file SHA256 `a2afe453663c3684de7573e5fad4fbd0f07e6f4e2cee61ef3afa2e79c5eed7cc`.
The old producer hash was `2f79be45310677771479ae054376b2e37e733f52548651605dc2b6d68e29b96a`.

The extension supplies an already-admitted owner/style (XYZ256/256/0,
RGB216/216/255, decrement16, detail2), zeroed scene registries, disabled scenario
message timer, mode5 and explicit uptime inputs. Those style values are the
historical reader corpus's DRAGON controls, not a newly qualified Steam reader
or launch. Allocator, window/input outputs, scene-family drawing and LineTrail
draw556C00 remain explicit ABI sinks. Rectangle intersection421B60 executes
unchanged on the forced modal path; no fitted drawing behavior substitutes it.
This proves bounded caller admission into the existing ring mechanism, not
Windows initialization, full scene pixels or real wall cadence.

Production now publishes immutable Bullet draw records and world-space trail
segments together at the normal admitted pre-Logic seam. The existing presentation
owner retains one immutable `Arc<NativeDisplayOrder>` for every parent family;
Bullet records and unit/animation/terrain consumers use that same membership/rank
generation even when Logic removes a peer. Records retain type/frame,
bridge-ground geometry and lifetime; they never clone Simulation. Modern displays
only resolve the atlas and reproject current
camera/shroud. Launch, movement and physical detach after this composite affect
the next admitted composite; an existing trail can fade after body removal.
Offline modal entry also publishes once; repeated modal displays/pumps do not
age it. One joint clear transaction drops order, Bullet bodies and trail history
on load/new timeline/menu exit, including natural victory/defeat score-screen exit.
Map/restore seed publishes body/order inputs without aging or restoring trail
history, so zero-step and paused-load displays retain their admitted objects.
Existing projection, frame, geometry and draw lowering ports remain shared by
production and native tests.

Whole R03 stays open. Scenario+62C producers (for example nuke/movie gameplay)
are absent from the selected runtime, so supplied pause controls cannot become
a fabricated app pause predicate. When those producers run, native Main can
continue trail fading without Logic; missing wiring would freeze the effect and
retain history longer. Timed resume, focus/minimize, native A9FAB0 producer
branches, network paths and full-scene committed views are also unqualified.
Other object families still read current simulation geometry, despite sharing
retained parent ranks, so this selected Bullet body/trail view does not establish
a complete scene or worker boundary. Native
ring/caller CPU goldens alone do not establish rendered DRAGON/GPU parity.

## Coverage and implementation boundaries

The corpus contains6 producer/ring/retirement sequences,14 reader controls,
8 Options controls,42 complete pixel controls,2 save/load controls,4 RenderFrame
and4 Tactical pass controls, a reverse-registry case and retained-config/zeroXYZ
case. Five additional complete native registry draws place1/8/128/512 trails
on the same30pixels, with alternating copied colors; one uses A64. These
exercise ordered destination blending across trails, not only within one line.
Malformed RGB controls additionally poison original sscanf locals:
incomplete nonempty scans expose caller stack residue, not a zero default.
VERA deliberately retains current RGB on malformed/incomplete scans. Complete
triplets use the shared native decimal scanner and byte narrowing. This matches
the selected retail triplets; malformed stack residue is not a parity claim.

The first retained candidate passes the ring/save-load and42-case CPU raster
comparisons. Root also ran `production_line_trail_matches_original_full_line_pixels`
against all42 original cases in both BGRA and RGBA formats, with exact color
and unchanged depth. The retained executable is
`/tmp/bridge-ifv-trail-gpu-libtests`, SHA256
`4c6831230234fa9583f78ba837e19b09f4edcfc48dfcd3566192e412bdaafdd4`.
The later retained selector candidate
`/tmp/bridge-ifv-selector-libtests`, SHA256
`25d0126000e51a881508e816d6c1533c4491ea27b8238b66747b2040e4276e77`,
passes all5 native overlap cases in both formats. Its8-trail/A127 control also
passes with forced3-operation chunks, crossing a bounded submission boundary
(80 chunks,160 passes). Color remains exact and depth unchanged. The reverse
registry-order CPU comparison passes. Receipts are
`/tmp/bridge-ifv-trail-overlap.log` and `/tmp/bridge-ifv-trail-order.log`.
The earlier integrated CPU group passes6 reader/ring/load/projection/raster
checks (`/tmp/bridge-ifv-integrated-trail.log`). Native comparisons remain
bounded to the listed inputs. Failed/repeated Bullet Unlimbo, all multi-trail
world-clear behavior, non-selected callers, and whole-scene compositing remain
outside this witness.

## Current production integration

The app owns a presentation-only ring keyed by a stable runtime handle. Ordered
launch and physical-destruction outputs attach/detach it; loading clears it.
One actual tactical composite ages it once, regardless of simulation tick count.
The render owner groups the original ordered pixel operations by destination
and resolves each group against the existing TerrainDrawRenderer color/Z
snapshot. Different pixels may execute independently; operations at one pixel
keep their original order. Bounded chunks retain that order across snapshots.

The current app uses a late global shroud multiply, unlike native per-family
ABuffer blits. The trail runs after that multiply and before UI so its exact
ABuffer operation is not followed by another blanket multiplication. The shared
background producer still uses an approximate sRGB curve at fog edges: A<127
can therefore alter the already-composed background and its mix with a trail.
This is a frequent fog-edge rendering limitation with no gameplay/RNG effect.
Native later RadBeam/other effect overlap ordering is not established by the
selected ordinary IFV scene. Zoom1 is the original pixel domain; other zooms
scale logical pixels. These limits preclude a whole-scene parity claim.

## Bounded rendering cost

The same selector executable passes the quiet Apple M4/Metal timing fixture
in both formats (`/tmp/bridge-ifv-trail-timing.log`). Each row uses a64x96 target,
one30-pixel segment per trail,2 warmups and20 measured samples. Total time
includes CPU preparation, encoder finish, queue submission, GPU execution and
completion wait; readback is outside the measured region. These debug-fixture
medians are neither GPU-only timings nor game FPS, and do not measure full rings
or a20,000-unit scene.

| Trails at A127 | Preparation median, ms | Completed submission median, ms |
| --- | ---: | ---: |
| 1 | 0.020–0.045 | 1.563–1.620 |
| 8 | 0.069–0.101 | 1.608–1.674 |
| 128 | 0.875–1.176 | 2.421–2.736 |
| 512 | 3.515–3.556 | 5.096–5.121 |

The8-trail/A64 control completes in1.613–1.617ms with0.072–0.073ms
preparation. Native overlapping pixels, chunk correctness and production timing
have separate receipts; the timing values are not native performance comparisons.
Final full-library, release and visible-runtime validation for the whole IFV
chain remains with its owner.
