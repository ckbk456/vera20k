# Stage 2: retained DRAGON body and trail composites

This bounded R03 prerequisite publishes Bullet drawing inputs and LineTrail
history together before Logic. Modern redraws reproject those retained values
without sampling newer Bullet state, fading the ring or retiring a trail. The
existing projectile geometry/frame/lowering, Display order and physical-destruction
owners remain shared; no Simulation clone, new numeric port or simulation RNG
draw was introduced. A private `LegacyComposite` owns body/trail retention and one
immutable Display ordering shared by every parent family. Initial map/restore
seeds drawing inputs without aging trail history; joint cleanup includes score exit.

## Native identity and admitted route

The explicit Steam15918130 profile uses authenticated gamemd SHA256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.
[Harness, native goldens and boundaries](../../tools/projectile_oracle/line_trail.md#authenticated-steam-caller-admission-extension)
execute Main55D360 → RenderFrame4F4480 → gate53BAE0 → Tactical6D3D10 →
registry556D40 → sample556B70. Normal sampling precedes Logic55DC9E and frame
increment. Modal suffix683F66 admits one forced composite; offline modal
pump623120 admits none. Eight controls include Scenario-depth pause, suppression,
wait, stall, repeated uncapped calls and detach556B30 through native retirement.
Prepared owner/style, scene-family draws, Logic and Windows services have explicit
boundaries. This is not full Steam initialization, launch or world execution.

Production advances the existing presentation owners on a normal admitted runtime
visit before Logic, including a visit that does not commit a frame. Offline modal
entry advances once; nested transitions and later pumps do not. Bullet records
retain type/frame, bridge-ground geometry and native Display membership/rank so
post-Logic launch, movement and physical removal cannot mix body/trail phases.
Camera, clipping, atlas lookup and shroud remain display inputs. Attached trails
still detach only through the existing physical lifecycle output; detached rings
fade on admitted composites until retirement. The native decrement and sample
order remain in their single existing owner, not a fixed-Hz timer.

## Checks and release evidence

[Validation receipt](evidence/yr1001-legacy-composite.validation.json) records actual
commands/results, leaf and native artifact hashes, retained release identity and
capture comparisons. Final retail Rust lib:9588 passed/0 failed/231 ignored;
clippy passes; Python tools:573 tests/five optional skips. The field ratchet stays
2513. Native cadence reproduction and the prior Steam clock reproduction pass;
the shared clock-service refactor leaves its golden payload byte-exact.
Initial pre-review Cargo results were observed without raw transcripts. Final
post-review Cargo, release and Python-tool logs are retained locally.

One fresh critic found two P2 defects: mixing old Bullet/new peer ranks could
reverse overlapping ReadOnly draws after removal, and score exit missed cleanup.
Both focused regressions failed before correction. All parent builders now consume
the same retained Arc; one clear/seed/advance transaction owns retention. Functional
planner/owner checks pass, as does the structural score-caller guard (constructing
AppState requires a GPU/window). Full lib/clippy and release captures were repeated
after the fixes. No second critic was run; live score/modal acceptance stays pending.

The release production loader/capture uses retail rules and assets on Apple M5 Pro
Metal,800×600, authored flat-ground map, FV actor13 and seed305419896. Force fire
cell(50,46) at step10; capture flight at25 and impact at45. A separate route issues
Stop at30 and captures draining at80. Before/after inputs are byte-identical.
Every compared initial/final gameplay fingerprint, command/actor/terrain transcript
and atlas statistic matches. Pixel comparisons report MISMATCH at25/45 only:
89 pixels within[258,213,302,231] and131 within[293,238,368,305], respectively.
Readback inspection locates these in the Bullet/trail region. At80 the complete
frame matches. A zero-step initial-load capture also matches, protecting map seeding.
No pixel tolerance or ignored field was used.

These are exact-step Rust production comparisons, with one legacy composite per
step; they do not certify ordinary OS timing, native scene pixels, Windows/Linux
output or worker stall independence. Original ring/caller CPU comparisons have
their own bounded coverage. Human playtesting remains pending.

## Reproduce the authored capture inputs

Use the existing fixture and capture owners. This generates only authored map and
profile data, with no unit/rules overrides. Choose an absolute owned output folder.

```python
import hashlib, json, re
from pathlib import Path
from tools.render_depth_fixture import build_fixture

folder = Path("/absolute/owned/dragon-fixture")
folder.mkdir(parents=True, exist_ok=True)
text = re.sub(r"(?m)^Name=.*$", "Name=DRAGON Legacy Composite",
              build_fixture(walls_only=True), count=1)
for section, body in [("Structures", ""), ("Units",
        "0=VERA-OBSERVER,FV,256,46,46,64,Guard,None,0,-1,0,-1,1,1"),
        ("Infantry", "")]:
    text = re.sub(r"(?ms)^\[" + section + r"\]\n.*?(?=^\[)",
                  f"[{section}]\n{body}\n\n", text, count=1)
assert hashlib.sha256(text.encode()).hexdigest() == (
    "1c52b7c47c7417cca8c88e217dc8e2a91e74a423185db418876d687828edb00a")
map_path = folder / "dragon-cadence.map"
map_path.write_text(text)
profile = json.loads(Path("tools/map_observation.ifv-turret.example.json").read_text())
profile.update(ticks=25, camera_cell=[48, 46], observe_types=["FV"])
profile["launch"]["selected_map_file"] = str(map_path)
profile["commands"] = [{"issue_after_step": 10, "owner": "VERA-OBSERVER",
    "payload": {"ForceAttackCell": {"attacker_id": 13,
                                  "target_rx": 50, "target_ry": 46}}}]
(folder / "flight25.profile.json").write_text(json.dumps(profile, indent=2) + "\n")
```

For impact set ticks45. For draining set ticks80 and append
`{"issue_after_step":30,"owner":"VERA-OBSERVER","payload":{"Stop":{"entity_id":13}}}`.
Run `python -m tools.map_observation --build-label yr1001-legacy-composite-reviewed`
with absolute `--profile`, `--contract src/app/diagnostics/tactical_capture/contract.v2.json`,
`--cwd` and new `--output` paths (the contract path must also be absolute).
Use the existing [saved observation comparison](../../tools/map_observation.md#validate-and-compare-saved-observations)
owner. Preserve before/after bundles, labels and inputs; do not add preview images
inside sealed capture directories.

## Residuals and human packet

Whole R03 and Stage 2 stay open. Scenario+62C producers such as nuke/movie gameplay
are a separate absent mechanism: native Main can sample trails while Logic is
paused; missing production admission would freeze fade and extend retained history
when that mechanism is implemented. The supplied native control is not an app
pause predicate. Native render-gate producers, timed resume, focus/minimize and
network routes remain unqualified. Other scene families still read current
simulation, so this Bullet view is not a complete immutable scene or worker boundary.

Humans: in an ordinary retail-rule skirmish, watch an IFV missile launch, flight,
impact and fading trail; open options mid-flight, change display refresh/VSync,
pan/zoom, then save/load and exit/re-enter. Record platform/GPU/refresh/map/seed,
body/trail alignment, pause/resume behavior, input feel and residual ghost trails.
Native versus Rust side-by-side feel and platform/device acceptance remain pending;
agents continue independent prerequisite work while this packet waits.
