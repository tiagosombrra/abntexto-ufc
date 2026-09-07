# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify the actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Final Certification**, also read `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and the permanent release/certification workflow definitions;
5. reconcile Git facts, machine state, handoff, roadmap, accepted article evidence, release blockers and temporary-executor lifecycle before certification work.

Memory, prior chats, historical branches and old workflow names never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Final Certification** |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Entry synchronization | **ACCEPTED** — `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| Scientific Article phase-end | **CLOSED** — `923d11ef...`; Static `34154045481`; complete Linux `34154045509`; PDF 5/5 visual PASS |
| Linux release baseline execution | **PASS** at `f8be323027b42eefcdbe3d13b2f269abdd6ec17f`: Static `34168471299`, Linux `34168471312`, release baseline `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release-baseline artifact | `10035242168`; digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604` |
| Current batch | **Final Certification — Release Baseline Cleanup Candidate** |
| Temporary executor | removed in the cleanup candidate; Step 2 acceptance waits for cleanup-candidate Static/Linux |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active
6. Release — queued

## Final Certification rules

- `cert/v3-final-certification` is the only active certification task branch and starts from canonical main `22e3c192...`.
- The permanent `make release-check` contract passed through the temporary executor at `f8be323...`; the executor is now removed in the cleanup candidate.
- Do not mark the release baseline ACCEPTED until the cleanup candidate itself passes Static and Linux, proving repository hygiene after executor removal.
- Preserve accepted shared and Scientific Article semantics; certification is proof/packaging work unless a genuine regression is found.
- Literal Times New Roman/Arial evidence must not redistribute proprietary fonts.
- Issue #18 reproducibility work adds deterministic build evidence and must not modify normative article/shared behavior merely to stabilize bytes.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Engineering rules

- Project-owned technical surfaces are English.
- Preserve the accepted v3 public API unless current authority explicitly authorizes a change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green test proves only the encoded contract.
- Reviewer comments are evidence, not automatic normative authority.
- Do not weaken tests merely to recover green CI.
- Negative evidence must fail for the intended predicate.
- Permanent workflows remain `Static contract`, `Linux integration`, and `Linux release check`.
- Temporary workflow/executor lifecycle must be atomic: create -> execute -> validate -> remove before bounded checkpoint acceptance.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission before **Release**.

## Progress documentation discipline

A **material advance** is any change that alters runtime behavior, normative classification, test/evidence coverage, certification scope/result, canonical content, phase status, acceptance status, branch/base facts, artifact provenance, reproducibility state or release readiness. Update the relevant execution documents and handoff in the same work cycle; synchronize roadmap and machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. The machine invariant remains `phase_end_regression.candidate = one-immutable-sha`. Final Certification requires complete Linux plus the full applicable certification/release evidence matrix.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current normative evidence, or reviewed source material, record the ambiguity and stop advancement.
