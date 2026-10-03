# Vanilla 1.001 — current agentic checkpoint

Updated 2026-10-03. Replace this current state on continuation; reconcile actual
Git/PR/process state before acting.

## Scope and delivery

Faithful vanilla YR1.001 first, smooth independent rendering and deterministic
optimization. User explicitly authorized Stage2 implementation, scoped PRs, merge
and fast-forward primary main. Agents own automated checks/native comparisons;
humans playtest/assess feel. Preserve original assets/config and upstream `origin`.
Delivery target is `ckbk456/vera20k` through `delivery`, no upstream publication.

PRs #1/#3/#4 merged; primary input main `726f330b60cf06bba82b3fb7e146f1d0b0a46988`.
Issue #2 is closed. Current owned branch `feature/yr1001-presentation-runtime` at
`ra2-yr-rust-worktrees/yr1001-presentation-runtime`; inspect actual HEAD/status.
Current code is the first bounded R01 event-loop seam. **S2 and whole R01 remain
open**; interpolation, legacy composite qualification and worker handoff are not
implemented or certified. [Mechanism and human packet](yr1001-stage2-runtime.md).

## Completed implementation and checks

- Ordinary redraws no longer advance gameplay or service audio/exit. The existing
  pacer/admission/runtime/output consumers operate from `about_to_wait`.
- Hidden/poisoned windows retain service wakes; focus/pause/startup/terminal gates,
  no catch-up and native-width pacer rollover remain. The 16ms service latency bound
  is app scheduling, not native legacy composite or gameplay cadence.
- Exact capture has its explicit one-step owner; power bar, gadget idle, radar and
  trail composites retain existing display ownership. Borrowed SimView is immutable
  committed state; no owned worker snapshot or shared mutable simulation is added.
- Steam source remains primary ignored `.local/steam-baseline-2026-10-03/game/`:
  app2229850/build15918130/English, acquired436files/1,961,731,509bytes. Candidate
  gamemd SHA3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600
  is still rejected by the default native execution gate1cdd1180...84298c.
- Existing `asset extract` recovered all27previously present INIs into the owned
  worktree `.local/official-extract/extract`. All YR(*md) files match prior extraction;
  only RA2 `rules.ini`/`sound.ini` differ. Original files preserved. Owned `ini/` symlink
  selects fresh Steam extractions; config selects official assets. Receipts ignored.
- Required full `python3 -m tools.cargo_run -- test -p vera20k --lib` with
  `VERA20K_REQUIRE_RETAIL_INI=1` and official `RA2_DIR`: **9579passed,0failed,231ignored**.
  Initial full run also passed; repeat was justified by switching to fresh official
  INIs. Full lib coverage does not mean all ignored native/GPU/retail routes ran.
- Required clippy lib passes (730reported existing warnings), including the official
  input selection. Field ratchet:2513fields, unchanged against delivery main.
- First runtime-focused checks:6passed. One fresh read-only critic found1P2:
  exact-step sidebar reconciliation could enqueue EVA after the sound drain.
  New source-order regression first failed; producer-before-drain restored while
  camera/zoom stays after drain. Post-fix app check: **984passed,0failed,31ignored**.
  This covers all changed modules. Final-source clippy also passes after the fix.
- Initial release label `yr1001-runtime-seam` built app+asset. 30-step Fight.MAP
  explicit Battle production capture:VALID, hidden/unfocused,800x600,Metal AppleM5Pro,
  child exit0, no input/focus violations. It exercises diagnostic exact stepping,
  loading and GPU readback; no native pixel/parity, ordinary OS timing or feel claim.
  Post-critic release label `yr1001-runtime-seam-reviewed` passes; its new sealed
  capture is VALID and matches all compared state/render fields from the prior run.
  [Sanitized receipt](evidence/yr1001-runtime-seam.validation.json) records source,
  binary, retail input and frame hashes, review disposition and coverage limits.
- Ordinary quickplay runtime attempts were noncertifying and unfocused, with no
  committed trace. Raw app UI identity was unavailable; owned bundle CUA controls
  timed out twice. Exact owned app PIDs were terminated and their sessions completed.
  No successful ordinary OS focus/modal/minimize/restore/exit acceptance is claimed.

## Next safe actions and unresolved scope

Publish and link one R01 scoped PR, enable authorized auto-merge, confirm seven exact-head
checks and merge, fast-forward clean primary main, then dry-run owned label retirement.
Do not report Stage2 complete when this seam merges.

Continue the prerequisite native profile/frame/command/comparison chain before
R02/R03. F01 still has app22ms vs headless66ms inputs; F02/F03 joined native production
histories are open. R02's selected W02 numeric/future-state domain is unqualified;
R03's trail callback is composite-owned, with no universal fixed-Hz proof. R04 needs
actual owned immutable reader/command/ack transport; synchronous GPU stalls still
block this event-loop thread.

Research lead (static only, not enrollment): candidate entire .text401000..7E1000
SHA4cd5557a7490debc493ff965afc4483d8d2f1065f434f6b665cbb8fc4835b0cc matches
historical cmin_dock guards.11line-trail and4drive-fresh-turn ranges plus selected
vtable guards match. A bounded profile in existing native_oracle can join offline
Main_Tick timer setup55D440..55D7C2, clock6C8C40/timeGetTime and throttle55E160,
with controlled OS/gameplay sinks; default unknown-candidate execution stays closed.
FV paid-movement corpus is the strongest existing W02 lead, but native f64→SimFixed
and Stop precision residuals require resolution. These are engineering prerequisites,
not a demonstrated need for a different download or new human permission.

Human seam packet is drafted; all hands-on/platform/feel acceptance remains pending.
HP1 smooth-motion packet is not ready. Resolve current command/PR state on resumption.
