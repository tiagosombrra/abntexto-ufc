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
| Step 8 transport preparation | `4d94e9cd7a565eac2e226360bd2b4a92fee52586`; Static `34235990523` SUCCESS; complete Linux `34235990383` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Current batch | **Step 8 — immutable Final Certification phase-end candidate** |
| Candidate marker | `release/final-certification-candidate.json` present |
| Issue #18 | CLOSED — completed |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 8 preparation acceptance

The permanent `Linux release check` PR transport is accepted. The preparation checkpoint changed only orchestration and retained the existing permanent `make release-check` contract. Static `34235990523` and complete Linux `34235990383` are green; Linux reported `SCOPE=complete PASS=36 FAIL=0 SKIP=0`.

## Immutable candidate state

The synchronized candidate contains the one-shot marker `release/final-certification-candidate.json` and this candidate-running control state. Intermediate marker-only/control-plane-incomplete commits are rejected as candidates and do not authorize closure.

The exact synchronized candidate SHA is obtained from Git after this immutable commit exists and is recorded in the PR/evidence after CI begins. The machine sentinel intentionally remains `phase_end_regression.candidate = one-immutable-sha`.

Required gates on that same candidate:

1. Static contract;
2. complete Linux integration;
3. permanent Linux release check executing `make release-check`;
4. accepted literal-font/Unicode/embedding/PDF-A/distribution and deterministic-reference-PDF predicates remain green;
5. no temporary certification executor;
6. item 33 remains explicit/fail-closed.

## Immediate action

| Order | Action | Gate |
|---:|---|---|
| 1 | Record the synchronized candidate SHA and workflow IDs in PR metadata after creation | no branch amendment |
| 2 | Wait for Static + complete Linux + Linux release check | all on same candidate |
| 3 | Classify any failure before changing code/tests | failed candidate is rejected |
| 4 | If all pass, record candidate evidence and close Final Certification | complete matrix green |
| 5 | Remove candidate marker and activate Release in a later phase-transition commit | synchronized documentation cycle |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
