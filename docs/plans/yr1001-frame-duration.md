# Admitted frames do not depend on diagnostic duration

Stage 2 / F01 prerequisite, based on `7743c549`, 2026-10-04.

An ordinary frame with diagnostic duration zero used to take the pending missile
impact queue, return early from combat, and discard those impacts. The same frame
still committed its gameplay counter. This made identical frame inputs produce
different damage, death and future state according to an unrelated host label.

The existing combat owner now performs its admitted work for every diagnostic
duration. The unused argument is removed from combat, its production caller and
the test adapters. The remaining runtime/world/replay argument is named
`diagnostic_frame_ms`; it only accumulates nominal elapsed time. Existing app
22 ms and headless 66 ms labels and the sealed capture policy remain intact.
Those values do not establish a universal native wall-clock frame rate.

## Native evidence and limits

Original Main `0x0055D360` calls Logic `0x0055AFB0` at `0x0055DC9E` without
an elapsed-time argument, then increments Frame at `0x0055DE81`. The already
merged [Steam Main corpus](../../tools/projectile_oracle/line_trail_steam_cadence.json)
and its [guarded provenance](../../tools/projectile_oracle/line_trail_steam_cadence.meta.json)
record `normal_pre_logic` and `uncapped_each_main` with all supplied frame and
millisecond clock words zero. Both still reach Logic, commands, frame increment,
throttle and pending drain in order. Whole-image identity is Steam SHA-256
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.

The new runtime test consumes those original execution results for frame admission
and commit. Logic is a declared ABI sink in this corpus: these controls do not
establish native unit AI, missile damage or whole-game equivalence. No oracle,
numeric implementation, native artifact or global image gate has changed.

## Production regression and validation

`sim::spawn_manager_tests::missile_impact_kills_through_the_shared_death_pipeline`
uses the real V3 child pool, payload producer and detonation queue, then runs the
bound `SimRuntime` ordinary transaction. A 200-damage impact against a 50-HP
target is checked for diagnostic labels `0`, `1`, `22`, `66`, `1000` and
`u32::MAX`. The test checks target death/removal, committed tick/frame, empty
impact queue, full frame output, all three complete RNG objects, real UnInit
removal trace and gameplay hash. Nominal elapsed accumulation is asserted
separately. It does not manually flush the frame's pending deletions.

The regression first failed on the old source at the zero-duration target-death
assertion. After correction, all 33 spawn-manager tests and the original-Main
golden consumer passed. Final retail-required library checks passed **9,589 / 0
/ 231 ignored**; Clippy exited zero with 729 existing tree warnings. The writable
simulation field ratchet remains **2,513**. Source and raw-log hashes, literal
command sessions and limits are in the
[validation receipt](evidence/yr1001-frame-duration.validation.json).

One fresh read-only critic found no actionable defects and independently checked
the changed-leaf, native-artifact and raw-validation hashes. No second review or
duplicate validation run was performed.

## Remaining compatibility work

Native Rocket impact applies damage inline; the current Rust producer queues it
for the combat tail. This ordering residual remains open and is not certified by
the label-independence test. Presentation sparkles still consume nominal elapsed
labels, so app/headless frames can differ visually despite matching gameplay.
Original full initialization, command histories, pause/network admission and
F01/F02 closure remain open, as do Stage 2 immutable handoff, vehicle interpolation
and worker lifecycle. Humans have not accepted this candidate through playtesting.
