# V3 historical engineering evidence

This directory is the controlled archive for completed v3 engineering evidence. Its contents are retained for auditability, not as current user or maintainer instructions.

Current authority is outside this directory:

- current Git/GitHub facts;
- `release/v3-release-candidate.json`;
- `docs/RELEASE-STATE.md`;
- current technical documentation indexed by `docs/README.md`.

## Retention policy

Historical material is retained when it preserves at least one of the following:

- release/certification receipts, source SHAs or workflow-run evidence;
- normative decisions or evidence still referenced by current checks;
- visual/PDF validation receipts that cannot be reconstructed from a short current document;
- lifecycle/audit evidence needed to explain a published release or a fail-closed control decision;
- compact repository-hygiene receipts that document why an active path disappeared.

Operational documents such as old handoffs, roadmaps and plans may remain when they contain unique SHAs/runs or materially useful audit context. Their presence does not make them current authority.

Historical material should be removed only when all of the following are true:

1. it has no active machine/test consumer;
2. it contains no unique release, certification, normative or visual-review evidence;
3. its substantive information is already preserved by Git/PR/Issue/release history or a smaller retained receipt;
4. removing it does not create broken historical references.

Repository size alone is not a reason to delete this archive.

## Structure

- `audits/` — completed repository/document/tool/regression audits and compact hygiene receipts;
- `certification/` — completed certification records;
- `control/` — historical handoffs, roadmaps and lifecycle/control snapshots;
- `evidence/` — normative, profile, visual and reference-PDF evidence;
- `plans/` — closed plans retained for traceability;
- `release/` — release/recovery/readiness and publication evidence.

## Permanent boundary

Every historical Markdown file outside this README must retain an explicit historical/superseded banner.

Historical files may mention obsolete paths, issues, branches, APIs or phase-time states. Those statements describe the historical moment only. They must never be linked from current user documentation as instructions for using the project.
