# Vanilla 1.001 — current agentic checkpoint

Updated 2026-10-03. Replace this current state on continuation; do not append a diary.

## Scope and authority

- Faithful vanilla Yuri's Revenge **1.001** first; independent smooth rendering and
  behavior-preserving optimization. Ares/Phobos and expanded limits are later baselines.
- Agents automate engineering/checks/native comparisons; humans playtest/assess feel.
- Implementation, scoped PRs, merges and fast-forward primary main are authorized.
  Update [masterplan progress](yr1001-masterplan.md#implementation-progress) per task.
- Delivery: `ckbk456/vera20k` main through `delivery`; `origin` preserves upstream
  `YuriPlanet/vera20k` as source only. No upstream publication or deployment.

## Git and current ownership

- [PR #1](https://github.com/ckbk456/vera20k/pull/1) merged as
  `0b0993991ac5e34fa0fa313b4b764e94d49998c2`; primary main fast-forwarded there.
  Its exact-head Python and Clippy workflows passed on Windows/Linux/macOS, and
  the field ratchet passed. Workflows were manually dispatched after fork bootstrap.
- Current owner/worktree: coordinator, `feature/yr1001-native-identity`,
  `/Users/khangcao/Documents/Software/ra2-yr-rust-worktrees/yr1001-native-identity`.
  Base is fetched delivery main `0b099399`; resolve candidate HEAD/status with Git.
- Chain: configured candidate image → immutable identity/section hashes → existing
  region/golden comparison → reproducible saved receipt. No executable enrollment,
  native execution, asset resolver/INI changes, gameplay or rendering changes.
- Original assets/config and extracted INIs remain intact. No local Cargo command,
  game, persistent server or capture process was started for this chain.

## Inputs and actual validation

- Official source: English Steam app 2229850, build 15918130, acquired from
  MAICHI_DESKTOP. All 436 files / 1,961,731,509 bytes matched Windows-source SHA-256.
  Main ignored `.local/steam-baseline-2026-10-03/` retains files and full receipts.
  Three genuine movie archives total 1,055,768,688 bytes; playback remains untested.
- Candidate gamemd SHA `3e81a61775d2745d1dabe397325ef663cd994ffc194da4e998e3bf5d2d308600`
  remains unsupported by the execution gate `1cdd1180...84298c`. The previous runtime
  copy is separately preserved and also unsupported; no piracy conclusion established.
- Isolated interpreter: main `.local/native-tools-venv/bin/python` (Python 3.14),
  pinned Unicorn 2.1.4/Capstone 5.0.7 installed from requirements-test.txt.
- Focused identity/PE checks: `python -m unittest tools.tests.test_native_inspect
  tools.tests.test_native_image -v` — **22 passed**. The new identity regression
  was first observed failing before implementation (missing command).
- `python -m tools.run_tests` — **555 tests, one failure, five optional skips**.
  The untouched macOS sleep-copy fixture exits SIGKILL (-9) before lsof observes it;
  isolated diagnostics reproduced this. Follow-up [issue #2](https://github.com/ckbk456/vera20k/issues/2)
  records the local validation limitation. Do not claim this run passed or alter
  retirement logic merely to satisfy a dead-child fixture.
- Live `native_inspect identity --reference ramp-height --reference foot-z` —
  **11/11 region hashes match** the existing pinned-image reference artifacts.
  [Saved report](../../tools/native_inspect.steam-15918130.identity.json) contains
  actual candidate/reference/section hashes and bounds. This is static byte evidence,
  never native execution or gameplay parity. All other inspection/execution paths
  still reject this candidate; live `sections` returned exit 2 with empty stdout.
- One fresh read-only identity critic found no actionable defects and independently
  checked the saved whole-file/section/reference/region hashes against source bytes.
  Review supports this bounded tooling scope only. Final PR/CI/merge evidence must
  be reported against the published head; no claim the candidate is merged yet.

## Ready queue and outstanding acceptance

1. Publish the reviewed identity-tool PR, wait for exact-head CI, merge and
   fast-forward primary main. No repeat critic is required.
2. B01 remains open: qualify actual Steam function/caller/global/address/behavior
   compatibility and production-selected retail input/layer identities. Matching
   11 code regions cannot admit every fixture or establish patch/gameplay identity.
3. B02: select a bounded execution profile (RNG seed/draw is a discovery lead), prove
   its reachable bodies/constants/calling convention before any execution enrollment.
   Windows SSH inventory/transfer works; interactive game/capture remains unqualified.
4. Resolve the local macOS process-fixture issue as a separate tooling chain, retaining
   the running-file safety check and proving child startup/cleanup.
5. B03 native capability census can proceed independently; then F01–F03 joined frame
   authority/comparison before R01 smooth-render handoff or gameplay porting.

Human packets HP0–HP6: none ready or accepted. Whole B01/B02 and all later gameplay,
network/native-save/campaign/platform/media acceptance remain open.
