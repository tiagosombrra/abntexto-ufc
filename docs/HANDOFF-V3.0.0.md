# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Steps 1-7 | ACCEPTED |
| Step 7 cleanup | `34e6bf8299e582803d1726e8dd699271c356fda5`; Static `34232017286`; complete Linux `34232017359`, `PASS=36 FAIL=0 SKIP=0` |
| Issue #18 | CLOSED — completed |
| Current batch | **Step 8 — release-matrix PR transport preparation** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 8 preparation

The permanent `Linux release check` workflow is being given a narrowly scoped `pull_request` trigger only for `release/final-certification-candidate.json`. It still executes the existing permanent `make release-check` contract. This enables the final immutable PR candidate to receive the required release/certification matrix without merging first or creating another temporary executor.

This orchestration checkpoint must pass Static and complete Linux. Only then is the candidate marker added in the immutable Step 8 candidate commit.

## Immediate action

| Order | Action | Gate |
|---:|---|---|
| 1 | Validate Step 8 orchestration checkpoint | Static + complete Linux |
| 2 | Create immutable candidate with candidate marker | no amendment after CI begins |
| 3 | Run Static + complete Linux + Linux release check | same candidate |
| 4 | Record candidate evidence and close Final Certification | complete matrix green |
| 5 | Remove candidate marker and activate Release | phase-transition cycle |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
