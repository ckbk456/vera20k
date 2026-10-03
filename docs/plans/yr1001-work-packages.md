# Vanilla 1.001 work packages

Draft decomposition for the [master plan](yr1001-masterplan.md). These are areas
and starting chains, not current defect claims or mandatory PR counts. All start
OPEN / NOT QUALIFIED. Discover the required variants and prerequisites before
opening a chain. Reuse qualified existing owners rather than reimplementing them.

Every instantiated chain covers trigger, initialization, admission, updates,
downstream consumers, interruption/replacement, cleanup and affected persistence.
The coordinator keeps current reservations/results in the
[checkpoint](yr1001-checkpoint.md) and evidence beside its code/tool owner; do not
create another competing historical status registry. Source observations and
reusable tools are in the [discovery report](yr1001-discovery.md).

## Foundation, world and ordinary match

| ID | Meaningful deliverable | Initial owner/route | Dependencies | Completion evidence |
| --- | --- | --- | --- | --- |
| B01 | Authenticated binary, patch/language and retail-input baseline | Existing native oracle/PE loader and retail-source resolver | Supplied installation/provenance | Immutable identities, accepted variant proof, unchanged original bytes; required unsupported variants explicit |
| B02 | Working checked native execution, inspection and full-game capture capability | Native oracle/inspect/Ghidra plus existing production observation | B01; host/media capability | Selected corpus reproduced, Python/native host receipt, initialized-game capture with observer limits; missing media stays blocked |
| B03 | Native capability census and owner/dependency map | Existing gameplay guide, native dispatchers and production retail readers | B01; B02 for execution claims | Every baseline area/retail type/mode/theater/mission plus authorable native path categorized with evidence, unknowns and actionable chain |
| F01 | One frame/clock/command/lifecycle authority | SimRuntime, master frame, frame pacer and command schedule | B01/B02 | Native speed/clock/command/Logic/delete histories; app/headless/replay use same frame contract; no assumed universal 15Hz |
| F02 | Reproducible first-divergence comparison | Existing parity digest, native harness and map observation owners | F01; B03 selects normalized fields | Independent initial inputs, semantic object correspondence, full relevant RNG/timer/event histories, first divergence reported with fixture seams |
| F03 | First joined production/native gameplay pilot | Existing AnyTown observation; start first frame/order before longer build route | B01/B02/F01/F02 | Actual native and app routes compared, not direct sim-only injection; grow to MCV→usable MTNK exit as dependencies qualify |
| W01 | Fixed-map startup through usable preplaced objects and first orders | Match bootstrap, rules/map loading, Simulation construction | F01/B03 | Native layer/default/house/start/seed/object-order histories; all affected production inputs, multiplayer/co-op setup variants inventoried |
| W02 | Ground vehicle route through arrival and next action | Existing Drive instance/path/Cell owners | W01/F02 | Real order→turn/traffic/ramp/bridge/crush→arrival/replacement/death; occupation and same-frame behavior, restore continuation |
| W03 | Infantry walking and subcell route | Walk, occupancy, mission and ground pose | W01/F02 | Bandbox/order through subcell conflicts/stances/bridge/arrival; native turns, timers, pose and cleanup |
| W04 | World terrain lifecycle | Bridge/overlay/resource/terrain owners | W01; movement/combat as each route needs | One collapse/repair, wall/gate or scenery route per chain, including objects on/below it, vision/path/placement/readers and persistence |
| W05 | Other locomotor families | Ship/Hover/Fly/Jumpjet/Chrono/rocket and installed/piggyback owner | Qualified shared W02/W03 prerequisites | One locomotor route at a time; native transitions, rate/rounding and blocked recovery, cancellation/load/death; no blanket fixed tolerance |
| E01 | War Miner resource→payment→next trip | Miner, radio, House wallet and resource grid | W01/W02 | Original resource/cargo/payment/RNG/timer histories, interruptions and concurrent spending, retail-reader and production map route |
| E02 | Chrono Miner alternate return loop | Existing shared miner/payment owner plus Chrono locomotion | E01's actual shared owners; W05 Chrono | Teleport/return/dock/release/retry and next trip, refinery loss and save/restore, preserving distinct native path |
| E03 | Slave/resource generation loops | Slave manager/miner, ore growth/tree and House owner | Relevant world/lifecycle owners | Workforce allocation→harvest→deposit→mobilize/death release; separate ore generation/growth chains with exact RNG/order/retail keys |
| P01 | MCV deployment through usable construction authority | Conversion/constructor/House/production owners | W01/W02 | Turn/admission/create/remove/select→usable yard→reverse conversion; rejection/blocked cases, startup/restore |
| P02 | Purchase through usable product and next queue item | Sidebar/AI→eligibility→factory→spawn or placement | W01/P01/wallet; selected mobility | Cost/time/charge/hold/cancel/blocked exits/provider loss; each product category/clone/upgrade native branch through production reader |
| P03 | Building service, sale, capture, power and radar | Existing building/House/power owners | P01/P02/C02 as required | One repair/sale/capture/provider-loss route per chain, downstream eligibility/visibility/credits, destruction and restore |
| C01 | Ordinary infantry engagement through death and retarget | Mission/targeting/fire/projectile/damage/lifecycle | W03/visibility/F02 | Native aim/ROF/RNG/launch/impact/death/experience/cleanup history; actual order and ordinary retail opponents |
| C02 | Ordinary tank engagement through building/unit aftermath | Existing shared combat owners, Drive and artillery projectile | W02/C01 shared dependencies | Cannon→flight/collision→Verses/armor/damage→death/debris/crew/score→next action; renderer/audio events and affected load state |
| C03 | Air and naval engagement/service variants | Shared combat plus sortie/spawn/naval/dock owners | W05/C02 and required factory/dock owners | One sortie, anti-air, ship or launched-rocket route at a time including ammo/reload/return/death/service and original ordering |

## Objects, abilities, authored content and continuity

| ID | Meaningful deliverable | Initial owner/route | Dependencies | Completion evidence |
| --- | --- | --- | --- | --- |
| U01 | Deployable infantry route | Existing GI/GGI deployment and fire owners | W03/C01 | Command/automatic deploy→stance/weapon/fire→undeploy/move/death; timer and target edge cases |
| U02 | Engineer and infiltration route | Mission/radio/capture/repair/infiltration | W02/W03/P03 | Approach/admission/entrance→effect/benefits→consumption or exit; spy/disguise variants as separate chains |
| U03 | Transport/garrison/bunker route | Cargo/radio/occupancy/shared attack owners | World/combat/lifecycle | Board/carry/passenger weapon or garrison fire→unload/release/destruction, capacity/blocked recovery/ownership/restore |
| U04 | Depot/airfield service and related special lifecycle | Service/dock/aircraft owners | Production and selected locomotor/combat | Admission→repair/reload→payment→departure; denial, provider loss, interrupted/load-restored links |
| X01 | Reversible control and attachment abilities | Capture manager/parasite/temporal/transport owners | Complete ordinary combat/lifecycle | Individual mind-control, parasite, temporal, Magnetron or similar chain through target/owner death, release, expiry and load |
| X02 | Special firing and cooperative weapon behavior | Shared weapon/warhead/effect owners | Ordinary fire/House/radio/selected movement | Individual Gattling/Prism/Tesla/laser/sonic/Boris/dog/Disc chain, all draws/ranges/timers and downstream deaths |
| X03 | Charges, radiation and status/effect lifecycles | Bomb/C4/radiation/particle/warhead owners | Combat/numeric/lifecycle | Individual Ivan/C4/suicide/Virus/Chaos/Desolator/Yuri pulse/crate route; spreading/cleanup and future-state effects, native numeric deviations resolved |
| X04 | Every vanilla strategic power | Existing superweapon plus House/power/effect owners | Native readers, affected world/combat/visibility | One power per chain: charge/suspend→target/launch→effect→expiry/recharge; force shield, nuclear, weather, chrono, dominator, mutator, spy/paradrop variants |
| A01 | Native House strategy and base recovery | Existing House AI/base plan/production/placement | E/P chains and B03 census | Native weights/RNG/cadence→purchase/site→usable object→provider loss/repair/recovery, country/difficulty/mode variants |
| A02 | Team creation/recruitment through script completion | Team/TaskForce/Script owner and actual units | B03, world/AI and required mission actions | Native selection/spawn/recruit/action/next-step/disband, all active and authorable native opcodes inventoried; no silent stalled unsupported step |
| A03 | Tactical AI cooperation and threat recovery | House/team/techno threat and mission owners | A01/A02/C chains | One defend/respond/attack/regroup/rebuild route; callback order and full required lifecycle, long-running native scenarios |
| T01 | Live Tag/trigger lifecycle foundation | Existing trigger runtime, map attachment and object lifecycle | W01/F01; B03 dispatcher census | Construct/attach→native event poll→ordered actions→repeat/disable/detach, local/global state and destruction/load behavior |
| T02 | Native scenario events/actions through outcome | Trigger/Team/reinforcement/House owners | T01 plus selected action prerequisites | One authored mission route at a time, linked trigger order, reinforcements/variables/timers/objectives/terminal event, all native opcodes categorized |
| T03 | Modes, cooperative scenarios and random-map startup | Mode layering, launch/session and map RMG owners | W01/T01 and required economy/combat | Mode-specific initialization/objectives/teams/House relationships; RMG seed/settings→usable world, native RNG and asset binding |
| K01 | First complete campaign mission | Campaign shell→scenario→briefing/objectives/score | T/A chains, gameplay, actual media | Native setup and difficulty branch correspondence; win/lose/retry/save/resume→next mission, human authored-content packet |
| K02 | Both shipped YR campaigns | Existing K01 owners | Each mission's discovered gameplay/trigger prerequisites | Every shipped mission and difficulty-dependent route mapped and tested; progression/finale/outcome/media closure, no representative-mission certification |
| Q01 | Rust continuity and diagnostic replay | Existing snapshot/restore/replay/runtime owner | F01/F02 and each affected state owner | Game save/reload→equivalence to corresponding native restored execution with matched fresh/in-process context and proven reset/retention policy for each RNG stream; diagnostic replay/checkpoint semantics distinguished |
| Q02 | Native save compatibility | Existing persistence owner extended after format discovery | Investigation at B03; qualified affected lifecycles | Native construction/serialization/reference-rebinding identified; import and export native-compatible saves, future behavior and original-load acceptance separately evidenced |
| Q03 | Complete save/replay transition matrix | Same owners; no duplicate world snapshot | Q01/Q02 and required game mechanisms | Save/load at movement/fire/transport/control/trigger/power/terminal boundaries, schema migration and future native-restored comparisons; native RNG reset/retention context preserved separately from diagnostic replay |
| N01 | Two Rust peers complete a LAN session | Existing command lockstep plus session/transport | F01/Q01 and gameplay/session initialization | Start/lobby/seed/rules agreement→ordered inputs/checksums→defeat/exit/dropout, delay/jitter/loss recovery, convergence and real latency |
| N02 | Native packet/session and LAN interoperability | Extend existing net/session owners; early protocol discovery | Investigation at B03; N01 for implementation | Packet/compression/scheduling/checksum contracts, observer capture and native-peer route; Rust convergence alone cannot close original-client interoperability |
| N03 | Multiplayer mode/session closure | Native session/House/outcome/transport owners | N01/N02/T03 and covered strategic gameplay | Mode/team/alliance/speed/pause/disconnect/result cases, transport-independent gameplay; legacy service dependencies explicitly inventoried |

## Presentation, optimization and final qualification

| ID | Meaningful deliverable | Initial owner/route | Dependencies | Completion evidence |
| --- | --- | --- | --- | --- |
| R01 | Runtime services independent of redraw and immutable handoff | App runtime/frame pacing, SimRuntime outputs and presentation state | F01/F02 | Migrate sim/render/UI/picking readers; committed views plus lossless events, clock generation/acks/backpressure, same traces under synthetic display schedules |
| R02 | Smooth ground-vehicle motion and interaction | Existing locomotor visual/instances/input owners | R01 and qualified W02 | Previous/current pose samples, one anchor for selections/effects, discontinuity reset; clicks revalidated in sim, unchanged gameplay and human HP1 |
| R03 | Legacy effect/service cadence at high refresh | Trail/effect/radar/audio/UI timing owners | R01/F01; relevant native effect evidence | Launch/attach/update/impact/detach/retire with native cadence; all required events delivered once, paused/stalled/uncapped routes |
| R04 | Independent simulation executor lifecycle | Existing runtime orchestration, window/GPU and transport | R01–R03 boundary proof | One gameplay writer on eligible worker; native command attribution, load/exit/abort/focus/loss shutdown; bounded memory and no orphan workers |
| V01 | Ordinary tactical composition | Existing wgpu sprite/terrain/voxel/depth/shroud | Qualified W/C routes; F02 | Native-coordinate reference mode; common vehicle/infantry/building→shadow/depth/selection/shroud/light, original blitter/capture and actual GPU readback |
| V02 | Special visual routes and mutable draw-cache closure | Same render/pose/cache owners | V01, ability/world chains | Air/naval/bridge/debris/cloak/warp/lighting/effect routes with cache invalidation and event lifetimes, no simulation feedback; source-driven palettes/order |
| V03 | Platform GPU and output qualification | Existing GPU/readback/capture diagnostics | V01/V02/R routes | Metal/DX12/Vulkan outputs on real devices, fullscreen/resize/resolution/UI scale/reference sampling; masks/differences/limits explicit |
| H01 | Complete shell and in-game player route | Existing UI/sidebar/input/frontend owners | W/P/C plus selected T/K/N | Shell→setup/load→select/order/build→pause/options/save/load→outcome/score→shell, hit/repeat/focus/hotkeys and actual command receipts |
| H02 | Audio/EVA/theme and positional sound lifecycle | Existing event dispatch and rodio audio service | R03; selected gameplay/terminal events | Ordered sound admission/channel/stop/release/theme/EVA/native cadence, camera/ownership changes and pause; hardware human listening |
| H03 | Briefing, movies and localization content | Existing CSF/Bink/media/shell owners | Genuine retail media, K/H routes | Native source selection/decode/layout/transitions/audio and complete mission media flow; empty placeholder archives cannot qualify |
| O01 | Measured ordinary production optimization | Existing sim-bench/app diagnostics/render/asset owners | Fidelity-qualified selected chains | Stage timings/tails/latency/queue pressure and real benefit; same semantic traces/events, explicitly scoped hardware/content |
| O02 | Deterministic parallel compute and asset/presentation workers | Existing authoritative mechanisms and deterministic joins | O01 and per-chain dependency proof | Worker-count/order perturbation versus qualified sequential path, platform/restore checks; RNG/same-frame effects preserved, no duplicate long-term implementation |
| Z01 | Vanilla release-candidate closure | Coordinator using existing evidence/CI/build owners | Every required baseline area and human packet | Whole-scope audit, no required unexplained gap, reproducible candidate/evidence bundle, native save/LAN results and human/platform limits honestly reported |

## Task brief template

Use a short outcome brief rather than copying the entire master plan into a worker.
Expand when required scope would otherwise be lost.

```text
Make <specific vanilla 1.001 player route> behave like the authenticated native
baseline, from <trigger> through <terminal result/cleanup>, including required
initialization, numeric/RNG/timer order, downstream consumers and persistence.
Resume from <checkpoint/owner evidence> at <revision>. Own <worktree and owners>;
<workers' independent read/write boundaries>. Reuse existing owners and tools.
<Explicit exclusions and current publication authority, if relevant>.
DONE WHEN the complete production route and required variants have bounded native
comparison evidence, actual regression/integration validation, one fresh critic
where required, and no unrecorded required gap. Recording work does not close it.
Prepare <human packet> if this changes the tested player outcome.
```

If evidence reveals a large prerequisite mechanism, add its dependency and perform
the coherent foundation first. Do not shrink the parent acceptance until it silently
passes. State which route remains open and resume it after the prerequisite.
