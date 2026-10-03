# Vanilla 1.001 — current agentic checkpoint

Updated 2026-10-03. Replace current state on continuation; reconcile Git, PRs and
owned processes before acting.

## Authority and delivery

Faithful vanilla YR1.001 first. User authorized Stage 2 implementation, scoped PRs,
merge into `ckbk456/vera20k` through `delivery`, and fast-forward primary main.
Agents automate/native-compare; humans playtest and assess feel. Preserve original
assets/config, upstream `origin`, unrelated worktrees and processes.

PRs #1/#3/#4/#5 merged. Clean primary main is
`627f982be03c401aa83836b130bcbbb0764116d5`; PR #5's seven required checks passed
at `0cdcd590466780874fdb5a2b9782ebef739dd98e`. Its bounded event-loop R01 seam is
delivered. [Mechanism, receipt and human packet](yr1001-stage2-runtime.md).
**Whole Stage 2 and R01–R04 remain open.**

## Current owned chain

Worktree `ra2-yr-rust-worktrees/yr1001-clock-qualification`, branch
`feature/yr1001-clock-qualification`, base `627f982b`. Complete bounded native
clock/offline timer/throttle qualifier plus production pacer correction is validated
at implementation commit `509d7accc4d3904696615285541c36d8aa07ad10`.
[PR #6](https://github.com/ckbk456/vera20k/pull/6) is open, ready and linked; all
seven exact-head CI checks/merge are pending. Root owns docs/publication. No active owned build/test
or app process; one independent critic completed with no confirmed defects.

[Clock chain](yr1001-clock-qualification.md) and
[sanitized validation receipt](evidence/yr1001-clock-qualification.validation.json)
record source hashes, executable bounds, native payloads and literal checks:

- 168 histories execute original timer setup and throttle together; 112 setup,
  37 historical throttle and three explicitly supplied stopped-timer controls.
- Native signed elapsed comparison rejects speed-0 admission at clock rollover.
  Focused regression failed before correction, then all 16 pacer tests passed.
- Required final retail lib suite: **9582 passed, 0 failed, 231 ignored**. Initial
  full run:9581 passed/1 failed because the existing math-table fixture lacked
  `RA2_DIR`; explicit official input corrected it without code changes.
- Clippy passes (730 existing warnings); Python suite:573 tests/five optional skips;
  optimized scope/lifecycle checks:20 passed. Native reproduction passes.
- Field ratchet:2513 unchanged. Release label `yr1001-clock-qualified` builds;
  sealed 30-step Fight.MAP exact capture VALID and MATCHES PR #5's reviewed capture.
  This is Rust regression, not native pixels or ordinary rollover execution.
- Default historical executable gate remains fail-closed. Steam qualification is
  explicit and scoped; unrelated generators and historical payloads are unchanged.
- One fresh read-only critic independently checked image/regions/source provenance,
  native arithmetic and guards. No confirmed defects; no second critic is needed.

## Local assets and retained candidates

Official source: primary ignored `.local/steam-baseline-2026-10-03/game/`, Steam
app2229850/build15918130/English,436 files/1,961,731,509 bytes source-SHA matched.
Owned `ini/` selects all27 fresh official extractions; YR files match prior values.
Primary original INIs/config and old assets remain untouched.

PR #5 reviewed capture and clock-qualified label are retained for comparison/human
acceptance. Earlier retirement dry-run of only `yr1001-runtime-seam` was blocked by
PID732 (`tccd`, unrelated system service); no files deleted or processes killed.
Ordinary app focus/modal/minimize acceptance is pending; prior unfocused UI attempts
were noncertifying and their exact owned app processes ended.

## Next safe actions and residuals

Enable exact-head auto-merge for PR #6 after this progress commit, wait for all seven
required checks, confirm merge, then fast-forward clean primary main. Update task
progress at delivery.
No routine human permission is missing.

Continue prerequisites before R02–R04: F01 app22ms vs headless66ms, native frame and
command order, F02/F03 joined initial state/gameplay histories. W02's vehicle numeric
future-state domain is not qualified. R01 still needs owned immutable readers and
lossless output transport; the borrowed SimView and synchronous GPU can block.
R04 requires native command attribution, timeline-aware acks and actual worker
load/exit/focus lifecycle, not a shared mutable simulation shortcut.

R03 research (static only): normal Main_Tick renders before Logic; Scenario pause
can render without a commit; offline modal entry renders once and modal pumping
uses a distinct route. Existing LineTrail callbacks mutate on actual composites.
Do not gate today's post-step trail sample by committed frames or assume fixed15Hz.
Research the joined caller/callback controls in existing native owners, then implement
one DRAGON attach/composite/impact/deferred detach/retire chain with executed proof.
All human HP0/HP1/platform/feel acceptance remains pending.
