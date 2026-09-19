# V3 release-state history

This directory preserves closed machine-readable v3 release/development state and migration/evidence contracts that remain useful for auditability or current fail-closed checks.

Current release/development authority is:

- `release/v3-release-candidate.json`;
- `docs/RELEASE-STATE.md`;
- current Git/GitHub facts.

Files here are historical evidence only.

## Retention policy

Keep a historical machine-state file when it:

- is consumed by a current repository/test/governance check;
- records a frozen/published candidate or immutable release receipt;
- preserves a machine-readable API/normative/evidence contract still used for negative/residual validation;
- contains source-SHA or release-control facts not represented by a smaller retained receipt.

Do not promote a historical JSON back into active authority merely because a current check reads it. A current check may use historical state as a negative baseline or audit reference.

Removal requires an explicit consumer audit and must not weaken current fail-closed behavior.

The root `release/v3-release-candidate.json` intentionally stays at a stable path while the active development line evolves.
