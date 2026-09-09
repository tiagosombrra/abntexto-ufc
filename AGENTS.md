# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata, or publication state:

1. identify the actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/V3-CONTINUATION.md`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `docs/V3-RELEASE-READINESS.md`;
4. during **Release**, also read `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers, retained-artifact provenance, and publication state before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Release** |
| Canonical branch | `main` |
| Last merged publication-closeout synchronization checkpoint | `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Active Release work branch | `release/v3-release`, synchronized to that canonical `main` checkpoint |
| Release PR #293 | **MERGED** by squash as `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout PR #294 | **MERGED** as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Superseded PR #292 | **CLOSED**; historical evidence only |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **PHASE-END REGRESSION ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS, complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Retained distribution artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Post-merge control sync on canonical `main` | Static `34333350711` — SUCCESS |
| Current batch | **Release publication — tag/GitHub Release and post-publication verification pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Always start a new local/session continuation from the latest `origin/main`. `docs/V3-CONTINUATION.md` is the concise operational handoff.

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — closed
6. Release — active

## Engineering and Release rules

- Release is the final roadmap phase; do not invent a new phase for publication closeout.
- Project-owned technical surfaces are English; preserve the accepted v3 public API and normative/proof semantics.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed and is not a hidden Release implementation task.
- External publication is an explicit Release action and is never inferred from a build or candidate validation.
- Accepted publication ZIPs must come from the retained candidate artifact; do not rebuild them after candidate acceptance.
- Superseded PR #292 and old task branches are historical evidence only; do not resume them as active work.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification/release result, phase/acceptance state, artifact provenance, reproducibility state, tag/release state, candidate transport, or publication readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

Release phase-end regression is accepted on immutable candidate `75ead435eabe5157ed17c295ac26fce76438b0ca`. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`; the actual Git candidate SHA is recorded in evidence rather than self-recorded inside the candidate.

Accepted gates on the same candidate:

- Static contract `34303586782` — SUCCESS;
- Linux integration `34303586778` — SUCCESS with required complete scope;
- Linux release check `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- deterministic reference-PDF reproducibility — PASS, SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`, 450652 bytes;
- candidate-retained distribution bytes — independently downloaded and verified without rebuilding.

Release remains ACTIVE until publication and post-publication verification are recorded.

## Immediate Release discipline

1. fetch the latest `main` and create a new short-lived branch for any new publication work;
2. create `v3.0.0` tag and GitHub Release from canonical `main` while uploading the exact retained candidate-produced bytes;
3. verify published asset hashes against the accepted checksums;
4. run current CTAN `pkgcheck`; perform actual CTAN upload only as an explicit action with receipt/evidence;
5. update documentation after every **material advance** and perform final Release verification before marking Release CLOSED.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record the ambiguity and stop advancement.
