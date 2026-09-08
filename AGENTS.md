# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation for v3 development.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, or release metadata:

1. identify actual Git branch and HEAD;
2. read `release/v3-roadmap.json`;
3. read `docs/HANDOFF-V3.0.0.md` and `docs/ROADMAP-V3.0.0.md`;
4. during **Final Certification**, also read `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, and `docs/UFC-LIBRARIAN-REVIEW.md`;
5. reconcile Git facts, machine state, handoff, roadmap, release blockers and candidate-marker lifecycle before work.

Memory, prior chats and historical branches never override current repository state.

## Current state

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Final Certification** |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Steps 1-7 | ACCEPTED |
| Step 8 preparation | `4d94e9cd7a565eac2e226360bd2b4a92fee52586`; Static `34235990523` SUCCESS; complete Linux `34235990383` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Rejected candidate | `fc907856ac4ba0febf4d44fb408407a0fc2e94d4`: Static `34239113996` SUCCESS, but Linux `34239114066` performed only documentation-only scoped skip; therefore phase-end complete-Linux predicate FAILED |
| Current batch | **Step 8 — immutable Final Certification candidate retry** |
| Candidate marker | `release/final-certification-candidate.json` present and changed in the retry commit |
| Scope guard | candidate marker is explicitly `complete` in `tests/integration_suites.py` |
| Candidate gate | Static + complete Linux + permanent Linux release check on one immutable candidate |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

## Readable phase model

1. Regression Audit — closed
2. Core Corrections — closed
3. Reference PDF Validation — closed
4. Scientific Article — closed
5. Final Certification — active, immutable candidate retry gate
6. Release — queued

## Closure-scope freeze

Remaining scope is fixed to Final Certification Step 8 **phase-end regression**, then Release. Do not create a new roadmap workstream merely because a validator exposes a defect; classify it inside the existing acceptance predicate.

## Step 8 candidate rule

The permanent `.github/workflows/linux-release-check.yml` PR route runs only when the one-shot `release/final-certification-candidate.json` marker is present and executes the same repository-owned `make release-check` contract used by release validation.

The first synchronized candidate `fc907856...` is rejected even though the Linux workflow conclusion was `success`: the heavy integration step was skipped as `documentation-only`, while Final Certification explicitly requires `complete` Linux. Workflow success is not equivalent to predicate success.

The retry fixes the orchestration scope classifier, not product runtime: the marker is now an explicit complete-scope path and has self-test coverage. The retry candidate changes the marker in the same commit, guaranteeing the incremental-scope window sees the certification trigger.

A candidate is not amended after CI begins. A failed candidate is rejected; corrections produce a new candidate commit rather than rewriting history.

## Engineering rules

- Project-owned technical surfaces are English. Portuguese is allowed only in academic/rendered content, bibliography data, official wording, literal output under test, or explicit upstream/current-runtime boundaries.
- Preserve accepted v3 public API and shared/article semantics unless a concrete regression or current authority requires change.
- Do not silently change normative IDs, values, tolerances, locators, applicability, source precedence, modality or proof state.
- A green workflow conclusion proves only that workflow's own execution contract; phase predicates such as `complete` scope must also be verified.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary Microsoft fonts.
- Item 33 remains fail-closed and is not a hidden implementation task.
- Do not perform CTAN/external publication before **Release**.

## Progress documentation discipline

A **material advance** changes runtime, evidence, certification result/scope, phase/acceptance state, artifact provenance, reproducibility state or release readiness. Update relevant execution documents and handoff in the same work cycle; synchronize roadmap/machine state whenever those facts change.

## Mandatory phase-end regression

No phase closes until one immutable candidate SHA passes the complete **phase-end regression** and the result is recorded. Final Certification requires Static, complete Linux and the full applicable release/certification matrix on the same accepted candidate. The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`; the real SHA is recorded only after the immutable commit exists.

## Fail-closed rule

If a required fact cannot be established from current Git state, canonical state files, current evidence or reviewed source material, record ambiguity and stop advancement.
