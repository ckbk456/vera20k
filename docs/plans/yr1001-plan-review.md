# Independent plan review — 2026-10-03

One fresh read-only subagent reviewed the five initial plan documents, both shared
contract diffs and relevant source/evidence. It did not implement the draft, edit
files, run project code/tests/builds or execute native code. The review covers plan
consistency and selected source claims, not whole-engine parity or behavior.

## Findings and owner disposition

| Finding | Impact | Owner response |
| --- | --- | --- |
| P2: local integration flow conflicted with fetched-origin/main feature-base rule | Local-only dependent chains could lose previous work or improvise unsafe main integration | Added one explicit owned feature integration branch and narrow chain-base exception to both contracts and master plan; integrated-candidate validation and no-main/no-unmerged-stack rules stated |
| P2: Q01 future-trace save criterion did not name the reference continuation | Agents might change native load RNG behavior to force equality with uninterrupted execution | Q01/Q03 and master plan now compare corresponding native restored execution with matched process context; distinguish Scenario/Main/MapGen reset/retention from diagnostic replay |

The critic found no other blocking architecture/area-coverage issue. It specifically
checked the native/regression/human evidence distinction, native ordering under
threading, speed-policy assumptions and publication boundaries. The owner also made
the single live census location/state ownership explicit for future sessions.

The owner checked the RNG finding against current
[Simulation source](../../src/sim/world/mod.rs), restore/seed policies around lines
917–987, and preserved its native-load distinctions. Both confirmed findings were
fixed in the draft; no second critic pass was requested. Final document links,
package references, shared-contract consistency and whitespace were rechecked after
the edits. No gameplay source changed and no machine/native parity claim is implied.
