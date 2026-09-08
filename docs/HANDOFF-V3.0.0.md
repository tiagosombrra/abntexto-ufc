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
| Rejected candidate | `fc907856ac4ba0febf4d44fb408407a0fc2e94d4`; Static `34239113996` SUCCESS; Linux `34239114066` workflow SUCCESS but heavy integration SKIPPED as documentation-only, so required complete-scope predicate failed |
| Current batch | **Step 8 — immutable candidate retry with complete-scope guard** |
| Candidate marker | `release/final-certification-candidate.json` present and changed in retry |
| Scope guard | candidate marker explicitly forces `complete` in `tests/integration_suites.py` and self-test |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-FINAL-CERTIFICATION-PHASE-END.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 8 preparation acceptance

The permanent `Linux release check` PR transport remains accepted. Preparation checkpoint `4d94e9c...` changed orchestration only and retained `make release-check`. Static `34235990523` and complete Linux `34235990383` are green.

## Rejected candidate classification

Candidate `fc907856...` did not satisfy the phase-end gate. Its Linux workflow concluded `success`, but `tests/integration_suites.py` saw only the incremental documentation-control commit and returned `none`; the workflow therefore skipped heavy integration. Final Certification requires complete Linux, so the candidate is rejected fail-closed. No runtime/normative predicate failed and no accepted test is weakened.

The correction is orchestration-only: make `release/final-certification-candidate.json` an explicit force-complete path with self-test coverage, and modify the marker in each retry candidate so the incremental scope window includes it.

## Immutable retry state

The retry candidate contains the updated marker, scope guard and synchronized retry-running control state. Its exact SHA is obtained after commit creation and recorded in PR/evidence metadata. The machine sentinel remains `phase_end_regression.candidate = one-immutable-sha`.

Required gates on that same retry candidate:

1. Static contract;
2. **complete** Linux integration (not a scoped skip);
3. permanent Linux release check executing `make release-check`;
4. accepted literal-font/Unicode/embedding/PDF-A/distribution and deterministic-reference-PDF predicates remain green;
5. no temporary certification executor;
6. item 33 remains explicit/fail-closed.

## Immediate action

| Order | Action | Gate |
|---:|---|---|
| 1 | Record retry candidate SHA and workflow IDs after commit creation | no branch amendment |
| 2 | Verify Linux actually reports `SCOPE=complete` and runs heavy integration | mandatory |
| 3 | Wait for Static + complete Linux + Linux release check | same SHA |
| 4 | Classify any failure before changing code/tests | failed candidate is rejected |
| 5 | If all pass, record evidence, close Final Certification, remove marker and activate Release | synchronized transition |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
