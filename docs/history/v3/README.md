# V3 Historical Engineering Evidence

This directory is the controlled home for historical v3/v3.0.1 engineering evidence. Files here are **not current control-plane authority**.

Current development authority:

- `AGENTS.md`;
- `docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md`;
- `docs/V3.0.2-BRANCH-HYGIENE-MANIFEST.md` for branch-cleanup evidence;
- issue #313 for live operational receipts.

## Structure

- `control/` — historical handoffs, roadmaps, correction plans and lifecycle snapshots;
- `certification/` — historical final-certification records;
- `release/` — historical release/recovery/readiness and v3.0.1 R5/R6 evidence;
- `evidence/` — phase, normative, reference-PDF, article and v3.0.1 R1-R4 evidence;
- `audits/` — branch-only audits preserved before pruning;
- `plans/` — branch-only historical plans preserved before pruning.

## Contract

Every retained historical Markdown snapshot outside this README must begin with the repository's explicit `Historical snapshot` banner. The permanent repository contract rejects any documentation-history root other than `docs/history/v3/`.

Historical content may intentionally preserve obsolete branch names, paths and phase-time statements. Those statements document what was true at that time; they do not override current Git facts or v3.0.2 authority.
