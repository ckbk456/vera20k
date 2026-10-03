# Stage 2: ordinary runtime services outside redraw

This first R01 chain separates the existing app runtime opportunities from surface
sampling. It does not close S2, R01's owned immutable worker handoff, R02–R04 or
native compatibility qualification. The user authorized implementation, scoped PRs
and merges on 2026-10-03.

## State and ordering owners

`handler::about_to_wait` calls `App::pump_runtime_services` for ordinary execution.
The existing `LocalFramePacer`, `RuntimePassDecision`, `SimRuntime::advance_frame`
and its ordered `SimFrameOutput` remain authoritative. Ordinary `render_frame`
never admits gameplay or services audio/terminal exits. No second simulation,
mutable shared lock or drop-prone event queue was introduced. `SimView` remains an
immutable borrow of committed state on this single event-loop thread; it is not
an owned snapshot that can cross threads.

The pump retains abort consumption → outcome voice wait → scenario teardown →
graceful quit → audio service → admitted simulation → terminal edge consumption.
Output channels retain their existing native order and consumers; every admitted
frame drains them before the next opportunity. Camera input follows the existing
admission decision. Shell first-paint, tooltip/message sampling, loading after
present, power-bar/gadget updates, radar drawing and LineTrail composite history
retain their display owner. Exact tactical capture owns its one gameplay step;
its explicit render prelude only services audio/exits. Shell capture retains its
previous ordinary prelude and presentation update.

The app wakes within 16ms for service opportunities even with hidden/poisoned
surfaces, paused or inactive windows. This latency bound is an app scheduling
choice, not a claim about native presentation cadence or a universal simulation
rate. The unchanged pacer decides eligibility in native-width 16ms buckets;
uncapped eligible gameplay polls, first admission is immediate, a stall admits
one frame rather than a catch-up burst, and signed uptime rollover still rejects
admission. Focus loss freezes simulation, not audio/exit servicing. Hidden but
focused gameplay can progress without drawing.

## Evidence and validation limits

Native branch/body leads retained without changing their algorithms:

- `Main_Tick` 0x55D360, `ThrottleFrame` 0x55E160 and offline input admission:
  [37 throttle executions and coverage limits](../../tools/input_oracle/README.md).
- `AudioSystem::Pump` 0x406F70 through `Network_ServiceLoop` 0x48D080, pause and
  Theme/EVA owners: nearby provenance in `sim_tick::pump_audio_service`.
- [LineTrail original composite/ring/retirement evidence](../../tools/projectile_oracle/line_trail.md)
  expressly does not support replacing composites with a fixed simulation-Hz clock.
- `sidebar::PowerBarAnimState` retains unqualified callback-count approximations;
  this change does not accelerate them with service timer wakes.

The authenticated Steam candidate remains outside the default native execution
gate. Historical executed goldens and matching slices are bounded evidence, not
a new Steam execution result. No new native arithmetic/RNG port is added here.

Rust tests cover wake deadlines, blocked surfaces, uncapped polling, native pacer
admission/rollover, existing focus/modal/exact-step decisions and a structural
ordinary-redraw guard. A joined Rust-only fixture constructs an authored scenario
through the production runtime owner, consumes an attributed command and one-shot
trigger output, and compares every committed frame hash, complete logical RNG
state, command and trigger history with display periods 1/7/16/33/192ms and no
display samples. It is a regression comparison of Rust executions; no native
whole-frame parity or real OS/VSync timing independence is claimed.

One fresh critic found an exact-step sidebar/EVA ordering regression. The owner
first observed `exact_capture_sidebar_reconciliation_precedes_sound_drain` fail,
then restored sidebar producers before the sound drain and camera/zoom after it.
All app checks pass after that correction. No second critic was requested.

RNG draws remain inside the existing frame and sound owners; waking or borrowing
views introduces no simulation draws. The pacer records only committed admitted
frames and retains exact-step reanchoring. Existing physical-destruction outputs
still detach trails in their emitted order; load still clears their history.
Unqualified native service/cleanup branches remain in the packages above.

Full lib, post-correction app/clippy and production capture results are saved in
the [sanitized validation receipt](evidence/yr1001-runtime-seam.validation.json)
and [current checkpoint](yr1001-checkpoint.md). The reviewed 30-step release capture
matches pre-correction state and rendered bytes; this does not observe EVA audio. Automated checks do not replace human
playtesting.

## Remaining Stage 2 acceptance

F01/F02 remain required: app frame duration is 22ms while the headless owner uses
66ms, and no joined native production frame/command/RNG history is qualified.
This chain preserves those existing values rather than choosing a guessed clock.

R02 requires a qualified ground-vehicle route, previous/current samples and one
anchor across body/shadow/brackets/effects/picking, with lifecycle/discontinuity
resets. R03 requires executed legacy composite admission, including pause/stall
routes; LineTrail's native draw callback cannot be silently converted to sim ticks.
R04 requires an owned immutable view, command attribution and acknowledgement
transport before moving the sole simulation writer to a worker. Synchronous
surface acquisition/present still blocks this event-loop thread. Timing checks
above do not certify worker stall independence, cross-platform equality, rendered
native pixel parity or legacy feel.

Human packet for this seam: start an ordinary retail skirmish, issue orders, open
and close the options modal, Alt+Tab and return, minimize/restore, save/load,
abort to shell and quit. Check pause/focus freezes, correct sound return, no extra
frame on a redraw, and no orphan process. Run on Windows/Linux/macOS after
candidate preparation. Record OS/GPU/display refresh/map/seed and observations;
this packet is pending, and smooth-motion HP1 is not ready yet.
