# V3 Historical Engineering Evidence

This directory is the controlled home for closed v3 engineering evidence. Files here are **not current control-plane authority**.

Current development and release authority:

- `AGENTS.md`;
- `release/v3-release-candidate.json`;
- `docs/V3.0.3-DISTRIBUTION-CORRECTION.md`;
- issue #328.

Issue #313 is retained only for the external v3.0.2 CTAN publication receipt while that submission remains open. It does not control v3.0.3 development.

## Structure

- `control/` — historical handoffs, roadmaps, correction plans and lifecycle snapshots;
- `certification/` — historical final-certification records;
- `release/` — historical release/recovery/readiness evidence;
- `evidence/` — phase, normative, reference-PDF and article evidence;
- `audits/` — historical repository/branch audits and compact closeout receipts;
- `plans/` — historical plans preserved for traceability.

The compact v3.0.2 repository-hygiene closeout is retained as:

`audits/V3.0.2-REPOSITORY-HYGIENE-RECEIPT.md`

The former active-root files `docs/V3.0.2-BRANCH-HYGIENE-MANIFEST.md` and `docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md` were removed from the current tree during final v3.0.3 cleanup. Their exact historical blobs are identified in that receipt and remain recoverable through Git history.

## Contract

Every retained historical Markdown snapshot outside this README must begin with the repository's explicit `Historical snapshot` banner. The permanent repository contract rejects documentation-history roots other than `docs/history/v3/`.

Historical content may intentionally preserve obsolete branch names, paths and phase-time statements. Those statements document what was true at that time; they do not override current Git facts, the active v3.0.3 marker, or issue #328.
