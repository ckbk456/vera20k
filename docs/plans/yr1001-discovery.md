# Vanilla 1.001 discovery — 2026-10-03

Three independent read-only discovery agents inspected gameplay, presentation and
native evidence/data tooling. No project builds/tests/native execution ran. Initial
inspection used local main `9f631a2aff22410dc1c5304557c619a8f7208857`;
consequential findings were checked against fetched main
`7e932b968e9b901142d80944095af68fe178ebdc`, the plan branch base. Current code
observations are not a parity certification. Static file hashing and environment
inspection establish only the facts described below.

Use the [master plan](yr1001-masterplan.md) for direction and the
[work packages](yr1001-work-packages.md) for decomposition. Line anchors below are
for the inspected revision and must be rechecked on resumption.

## Current architecture and immediate gaps

| Observation | Source and inspected lines | Planning consequence |
| --- | --- | --- |
| SimRuntime binds one Simulation to immutable resources; SimView is a live borrow | [runtime.rs](../../src/sim/runtime.rs), 1–10, 60–99, 191 onward | Reuse authoritative owner; a borrow is not a concurrent snapshot boundary |
| Logic execution order is independent of BTreeMap storage order | [logic_vector.rs](../../src/sim/world/logic_vector.rs), 1–53; [entity_store.rs](../../src/sim/entity_store.rs), 1–60 | Sorting IDs or batching class updates can change native order |
| Live callbacks commit object effects before the next object; new objects may join the same walk | [world/mod.rs](../../src/sim/world/mod.rs), 4207, 6215–6257 | Trace causal same-frame dependencies before threading |
| Due commands run after live Logic; frame increment/removal are late | [world/mod.rs](../../src/sim/world/mod.rs), 5893–5919; [command_schedule.rs](../../src/sim/world/command_schedule.rs), 1–24 | Do not move commands earlier while extracting render scheduling; verify full order in F01 |
| Simulation advances inside render_frame on redraw | [frame.rs](../../src/app/frame.rs), 139–155; [handler.rs](../../src/app/handler.rs), 1067–1070 | Independent scheduling is a real implementation gap |
| Pacer allows at most one tick per redraw; speed zero admits each callback | [frame_pacer.rs](../../src/app/match_runtime/frame_pacer.rs), 142–159, 233–238 | Rendering throughput affects pace; native speed/stall behavior needs executable evidence |
| App supplies 22 ms, headless supplies 66 ms | [types.rs](../../src/app/types.rs), 25–28; [headless_scenario.rs](../../src/headless_scenario.rs), 90–94; [fixed_math.rs](../../src/util/fixed_math.rs), 61–66 | Existing tooling documents a 3× divergence; mechanics fraction is not universal wall-clock rate |
| Render builders read live sim state; interpolation helper only projects current pose | [build_instances.rs](../../src/app/presentation/render/build_instances.rs), 169–188; [helpers.rs](../../src/app/presentation/instances/helpers.rs), 348–352; [locomotor_visual.rs](../../src/render/locomotor_visual.rs), 98–104 | Implement explicit sample history, stable lifetimes and consumer migration |
| Input command paths mutate/read live simulation | [commands.rs](../../src/app/input/commands.rs), 17–27, 784–810, 900–911 | Command admission/interning/execution-frame ownership must migrate before a sim thread |
| Ordered sim outputs already cover useful event seams | [sim_tick.rs](../../src/app/match_runtime/sim_tick.rs), 881–961, 1006–1044 | Extend existing output owner; avoid deriving fire/death events from sampled views |
| Audio service is outside tick admission but inside render_frame | [frame.rs](../../src/app/frame.rs), 124–132; [sim_tick.rs](../../src/app/match_runtime/sim_tick.rs), 780–795 | Audio, shell and terminal waits need service scheduling separate from redraw |
| Trails fade once per tactical composite, even without a simulation frame | [line_trails.rs](../../src/app/presentation/line_trails.rs), 83–109 | High-rate redraw would alter effects without a separate native presentation cadence |
| Mutable presentation caches include waterline/pitch/lifetime state | [state.rs](../../src/app/presentation/state.rs), 31–57; [units.rs](../../src/app/presentation/instances/units.rs), 295–300 | Define source, invalidation, load/exit lifecycle and timeline generation |
| GPU uses FIFO; voxel atlas workers already join independent poses in key order | [gpu.rs](../../src/render/gpu.rs), 197–200; [unit_atlas.rs](../../src/render/unit_atlas.rs), 874–907 | Keep graphics backend initially; reuse bounded deterministic worker patterns |

## Gameplay and continuity

| Observation | Source and inspected lines | Coverage limit |
| --- | --- | --- |
| Three native-shaped RNG streams and independent continuation rules exist | [rng.rs](../../src/sim/rng.rs), 1–79; [world/mod.rs](../../src/sim/world/mod.rs), 966–980 | Full draw/state/load equivalence is per mechanism, not implied by one seed |
| Deterministic integer-backed finite 53-bit x87 subset and I16F16 helpers exist | [native_x87.rs](../../src/util/native_x87.rs), module header; [fixed_math.rs](../../src/util/fixed_math.rs), module header | Representation may be reusable; ambient state/unsupported operations still need checking |
| Fly code explicitly retains numeric differences | [fly_height.rs](../../src/sim/movement/fly_height.rs), 43–55; [air_movement.rs](../../src/sim/movement/air_movement.rs), 952 | Under this program they are unresolved fidelity leads, not accepted by small magnitude alone |
| Drive/Ship state now belongs to private installed/suspended locomotor payloads | [drive_locomotion.rs](../../src/sim/movement/drive_locomotion.rs), 1–51; [locomotor_owner.rs](../../src/sim/movement/locomotor_owner.rs), module header | Latest main removed entity mirrors; do not reintroduce them. Chronosphere replacement remains a named missing path |
| Standard War Miner chains have native corpora, retail-reader and loader evidence | [miner guide](../../src/sim/miner/README.md) | Useful complete-chain example; not all harvesters, full-clock/combat/render or whole-game parity |
| Production already consumes BuildSpeed in native-derived arithmetic | [factory.rs](../../src/sim/production/factory.rs), 313, 351, 457, 1355 | The old divergence ledger's missing-BuildSpeed claim is stale |
| Trigger runtime is deliberately narrow; live Tags/native polling remain absent | [trigger_runtime.rs](../../src/sim/trigger_runtime.rs), 1–17, 158–450 | Unsupported events/actions and lifetime semantics prevent authored-scenario closure |
| Team VM ports only actions 0,2,5,6,11,19,24,49,53,54,58 | [actions.rs](../../src/sim/team_script_vm/actions.rs), 18, 62–64 | Unsupported steps retain/stall teams; current retail census needs rerunning |
| Campaign selections cannot start scenarios | [shell_campaign.rs](../../src/app/shell_campaign.rs), 234–249 | Shell art is not campaign gameplay/progression |
| Save schema is VERA-specific, version 288 | [snapshot.rs](../../src/sim/snapshot.rs), 824–832 | Rust restore exists; native file import/export is unproven |
| Lockstep staging exists, but packet/session boundaries remain incomplete | [lockstep.rs](../../src/net/lockstep.rs), module header | No full LAN/native-client interoperability claim |
| Headless digest is not directly native-comparable | [parity_digest.rs](../../src/sim/parity_digest.rs), 6–31, 74–79 | Different entity initialization/hash, excluded height, partial RNG observation; extend the owner |
| net module says all math is fixed point, contradicted by sim/numeric owners | [net/mod.rs](../../src/net/mod.rs), 8–10; [sim/mod.rs](../../src/sim/mod.rs), 1–6 | Correct this lead when touching the networking chain; deterministic does not mean fixed-only |

Broad code exists for movement, economy, combat, powers, AI and persistence. Discovery
did not execute it or audit every branch. Public fields create a potential competing-
writer risk, not proof of an actual duplicate writer; trace current consumers when
the selected chain touches them. Historical plans and ledgers are hypotheses, not
a current completion database. The existing [gameplay guide](2026-09-11-gameplay-goal-catalog.md)
is useful for its 77 selections/83 coverage references, but not an exhaustive native
census or measured completion status.

## Native identity and local capability

The checked oracle currently accepts only
`1cdd1180e49024fbda8ad568caac2e86e856063ff67ab38f62b7d2c7bb84298c`,
PE32 x86 image base `0x00400000`:
[native_oracle.py](../../tools/native_oracle.py), 28–37, 100–149;
[native workflow](../../tools/native_oracle.md), executable identity section.

The main checkout's configured `.local/game/gamemd.exe` and preserved Downloads
original both hash to
`d4ad8c6f6642844cb40b2a45ceb71c6f7a0adff83da921162fdb7cfcf5628c0c`,
size 4,813,072 bytes, PE32 x86. Static version-resource strings say `1.11`; a
VS_FIXEDFILEINFO signature candidate contains words `0x10000,0x10001`. This does
not authenticate its YR patch identity and is not proof of a wrong version.
Do not relax the existing oracle hash. B01 must establish provenance, code/address
compatibility and behavior or obtain an authenticated supported native executable
from a legitimate existing installation. Variants need separate enrollment evidence.

Machine-local facts observed on 2026-10-03 (not portable requirements):

- Main `config.toml` selects `.local/game`; LOCAL.md records a preserved 500-file
  copy. Three supplied movie MIXes were empty; the runtime copy contains empty
  valid headers while originals survive. Movie source content remains absent.
- Current shell has no `VERA20K_GAMEMD_EXE` or `RA2_DIR`; Python 3.14 cannot import
  Unicorn/Capstone. Required versions are pinned in
  [requirements-test.txt](../../tools/requirements-test.txt): Python >=3.12,
  Unicorn 2.1.4, Capstone 5.0.7. Confirm interpreter-wheel support during bootstrap.
- No wine/wine64/ghidra-up on the inspected PATH, no observed Java/Ghidra/Wine
  process and no main `.mcp.json`. This does not prove no installation exists.
  Resolve discoverable installations and service capability before declaring a
  host unavailable. Full native game capture may need a genuine Windows host;
  emulation of selected x86 functions is not a Windows loader.
- Rust is available through the main checkout's `.local/env.sh`. The plan worktree
  has no copied local config/retail inputs/toolchain activation and has not been
  built. Future implementation preflight must resolve assets/config deliberately.

## Tools worth extending

| Existing owner | Capability | What it does not establish |
| --- | --- | --- |
| [native inspection](../../tools/native_inspect.md) | Identity-checked bytes/disassembly and indexed scanning | Reachability/absence from a linear sweep |
| [native oracle](../../tools/native_oracle.md) | Checked bounded x86 execution, provenance and goldens | Full initialized game/OS/device state; fixture substitutions and x87 limits remain explicit |
| [Ghidra workflow](../research/ghidra-workflow.md), [comparison guide](../../tools/ghidra_compare.md) | Native program/field/caller investigation | Names/signatures/layouts as unquestioned truth; remote service capability not yet proven here |
| [retail corpus](../../tools/retail_corpus.md) | Inventory/asset decoder checks | Actual mounted reachability or native decoder parity from Rust digests |
| [map observation](../../tools/map_observation.md) | Production loader, exact steps, clock/input contracts and GPU receipts; existing AnyTown build loop | Native whole-route parity; app/headless initialization still needs correspondence |
| [tactical certification](../../tools/tactical_certification/README.md) | Bounded production readiness/capture comparison | Universal object/scene/clock equivalence |
| [shell diff](../../tools/shell_capture_diff.py) | Native/Rust capture comparison in RGB565 units | A pass when no explicit limits are set; default exit 0 is not a parity gate |
| [frame readback](../../src/render/frame_readback.rs) | Actual composited GPU output | Native visual evidence without original comparison |
| [sim-bench](../../src/bin/sim-bench.rs), [dev overlay](../../src/app/diagnostics/dev_overlay.rs) | Headless benchmark and rolling frame intervals | App/native clock equivalence or full sim/extraction/GPU/present cost separation |
| [Rust CI](../../.github/workflows/rust.yml), [test CI](../../.github/workflows/test.yml) | Cross-platform clippy; manual library suites; data-free tool tests | Retail/native checks and cross-architecture simulation equivalence; skips can be green |

The current render owner supplies injectable radar presentation time through
GameRenderTimes ([render/mod.rs](../../src/app/presentation/render/mod.rs), 87–92;
[frame.rs](../../src/app/frame.rs), 442–443). Older depth reports describing that
clock as unsealed are partly superseded. Read current consumers before copying
historical limitations. Existing replay corpora often compare two Rust revisions;
their own receipts explicitly limit native claims.

## Pinned C++/extension references

The machine-local reference root is
`/Users/khangcao/Documents/Software/ra2-yr-references`. Bootstrap should accept a
configurable root; absolute local paths are not distributed dependencies. Existing
upstream histories and notices were preserved. Recorded revisions:

| Repository | Origin | Commit |
| --- | --- | --- |
| ReSource | https://github.com/Ritanlisa/RA2YR_ReSource | `b01d3cf93db69aca9b5cb5054ba04e4358963828` |
| Public Ares | https://github.com/Ares-Developers/Ares | `4f1d929920aca31924c6cd4d3dfa849daa65252a` |
| Phobos develop | https://github.com/Phobos-developers/Phobos | `9c859353b3e6407af6dad6df1e4d71415cbcaaac` |
| Antares | https://github.com/Phobos-developers/Antares | `1ff9aa00915a9b6c08b85f55a13f5ae722ad97bf` |
| Phobos YRpp | https://github.com/Phobos-developers/YRpp | `8468aab5eab6c2057532ed095e36f639a37564fc` |
| Antares YRpp | https://github.com/Phobos-developers/YRpp | `ef1c565ade4a9233177a7949034ed7bd245259f3` |

ReSource is useful reconstruction evidence, not original released YR source. Its
`src/misc/rules.cpp:25–41` InitRules still returns true with the full INI chain TODO.
Its README reports 12 Capture hooks, one SetPixel replacement and zero active Inject
hooks. The roughly 19K-function inventory is not verified behavior coverage or a
ready whole-game comparator. Its protected comparison files require attention to
that repository's own authorization rules before modification.

Public Ares targets 0.A. Antares reconstructs 3.0p1 with deliberate changes;
Phobos is a develop snapshot. Those are later version-specific targets, not vanilla
ground truth. YRpp declarations/layouts remain native-checkable leads.

Actual notices include ReSource GPLv3 with EA additional terms, Phobos GPLv3, and
Ares/Antares four-condition BSD-style terms including advertising acknowledgement.
This inventory makes no combined-distribution conclusion. Preserve file provenance
and notices; assess terms before translating copied code into distributed engine
code. Licensed native binaries/media stay outside the repository and public CI.
