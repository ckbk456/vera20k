# Stage 2 prerequisite: authenticated clock and throttle qualification

This chain qualifies bounded integer clock/offline timer/throttle behavior from the
owned Steam 15918130 `gamemd.exe`, then protects the existing production frame
pacer with those captured values. It does not close F01/F02 or Stage 2.

## Owners and bounded execution

The existing `tools/native_oracle.py` owns executable identity, PE mapping, original
spans, bounded execution, diagnostics and provenance. A trusted explicit scoped
profile binds an immutable image identity to its machine. The default image loader,
`call()` and unrelated native generators retain the historical whole-image pin;
this is not global enrollment of the Steam candidate. Instructions, data accesses,
fixture writes, nonexecuting endpoints and sink ABIs are constrained by the declared
profile. No original instructions are replaced.

The existing `tools/input_oracle/fast_scroll.py::native_throttle` remains the sole
throttle producer. Its `--steam-clock` selector runs only the qualified closure,
not the full right-drag/camera corpus. Original `timeGetTime` leaves execute;
the OS import returns supplied wrapping 32-bit uptime. Sleep, service, input,
command, tactical and render calls are recorded sinks, not emulated gameplay.

[Profile and reproduction](../../tools/input_oracle/README.md) and
[runner contract](../../tools/native_oracle.md) state the supported ranges:
clock `0x6C8C40..0x6C8C4A`, raw millisecond thunk `0x5D5890..0x5D5896`, offline
mode dispatch `0x55D440..0x55D456`, timer setup `0x55D767..0x55D7C2` and
throttle `0x55E160..0x55E33B` (all ranges end-exclusive). Whole image SHA-256:
`3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`.

## Result and production consumer

The original integer clock returns `timeGetTime() >> 4`. Timer setup captures
campaign/skirmish mode distinctions and the supplied campaign override flag;
campaign's force-2 branch is characterized separately. The production app currently
launches offline skirmish, so this chain does not implement campaign admission.

Native throttle prefix observations expose a real speed-0 discrepancy: after a
wrapping clock yields a negative signed elapsed bucket value, the native remaining
wait is positive even at duration zero. Rust formerly returned true before checking
that elapsed value. `LocalFramePacer::should_admit` now compares signed elapsed
against duration zero through the same owner as timed speeds. Speed 0 remains
uncapped in the same bucket and during forward progression. First admission,
pause, timed-speed clamp, explicit-step reanchoring, one-frame stall recovery and
output consumers retain their owners.

The named regression `frame_admission_matches_authenticated_native_timer_prefixes`
first fails on the old bypass, then reads captured native results to exercise the
production pacer. The contradictory speed-0 wake assertion is corrected while
keeping no-wrap uncapped coverage. Native results and metadata live in the separate
[Steam payload](../../tools/input_oracle/fast_scroll.steam-clock.json) and
[sidecar](../../tools/input_oracle/fast_scroll.steam-clock.meta.json); historical
`fast_scroll.json` and its metadata remain unchanged.

There are no RNG draws, simulation timer writes or object detach calls in the
production correction. The native fixture records frame timer writes and service
calls explicitly; it supplies OS clock inputs and initialized fixture globals.

## Coverage and remaining acceptance

The native corpus contains 37 historical throttle controls replayed with original
clock leaves, 112 offline setup controls and 171 arithmetic controls. All 168
physical histories execute native setup and throttle together; three stopped-timer
sentinel rows instead supply their stopped state explicitly. Positive waits around
rollover/sentinels stop before potentially unbounded waiting; they do not claim a
completed native wait. Real Windows scheduling, complete Main_Tick admission,
Logic/command order, pause/focus lifecycle, audio/render effects, gameplay RNG and
joined production/native game histories remain unqualified here.

The app's 22ms versus headless 66ms simulation inputs remain a separate F01 gap.
R01's owned committed handoff, R02's movement/picking evidence, R03's legacy
composite admission and R04's worker lifecycle remain open. Native normal rendering
precedes Logic; a later trail cadence change cannot simply gate today's post-step
sampling by committed frames. This finding is research ahead, not implemented
trail behavior.

Final local checks are saved in the [sanitized validation receipt](evidence/yr1001-clock-qualification.validation.json):
9,582 Rust tests pass (231 ignored), 16 focused pacer checks pass, 573 Python tests
run successfully (five optional skips), optimized guard checks and native reproduction pass,
and clippy passes. A final release exact capture is VALID and MATCHES the merged
runtime-seam capture. An initial full run lacked the math-table fixture
`RA2_DIR` prerequisite; the corrected environment passes without changing its code.
Single critic disposition and delivery state are recorded in the
[current checkpoint](yr1001-checkpoint.md). Human playtesting of focus,
pause, minimize/restore and feel remains pending; this bounded correction does not
require reproducing a 49-day uptime rollover by hand.
