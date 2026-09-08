# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 8 IMMUTABLE CANDIDATE RETRY

## Purpose

Final Certification proves the accepted V3 product without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | complete release matrix green |
| 3 | Profile/engine matrix | ACCEPTED | current matrix accepted |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACCEPTED | proof `34219229025`; cleanup green |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded + cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | bundle integrity accepted |
| 7 | Deterministic release reference PDF / issue #18 | ACCEPTED | `34231038578`; cleanup `34e6bf8...`; issue closed |
| 8 preparation | Release-matrix PR transport | ACCEPTED | `4d94e9c...`; Static `34235990523`; complete Linux `34235990383`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| 8 candidate `fc907856...` | Final Certification phase-end regression | **REJECTED** | Linux `34239114066` skipped heavy integration; complete-scope predicate not met |
| 8 retry | Final Certification phase-end regression | **RUNNING** | updated marker + complete-scope guard; await Static + complete Linux + Linux release check |

## Step 7 accepted evidence

Cleanup checkpoint `34e6bf8299e582803d1726e8dd699271c356fda5` passed Static `34232017286` and complete Linux `34232017359`, `PASS=36 FAIL=0 SKIP=0`, with the temporary executor absent and permanent `make release-reference-reproducibility` retained. Issue #18 is closed.

## Step 8 preparation accepted

Preparation checkpoint `4d94e9cd7a565eac2e226360bd2b4a92fee52586` added only the permanent PR transport. Static `34235990523` passed and complete Linux `34235990383` passed with `SCOPE=complete PASS=36 FAIL=0 SKIP=0`.

## Candidate `fc907856...` rejection

Static `34239113996` passed. Linux workflow `34239114066` also reported overall `success`, but its heavy integration step was skipped because automatic scope inference saw an incremental documentation-only window. Final Certification requires complete Linux; therefore the candidate is rejected despite the workflow conclusion.

This is an orchestration-scope failure, not a product/runtime/normative failure.

## Retry correction

The retry makes `release/final-certification-candidate.json` an explicit force-complete path in `tests/integration_suites.py`, adds self-tests for marker-only and marker+orchestration inference, and updates the marker in the same retry commit so the synchronize diff includes it.

The retry candidate is not amended after CI begins. Its exact SHA is recorded after creation in PR/evidence metadata while `phase_end_regression.candidate = one-immutable-sha` remains the machine invariant.

The exact retry must pass Static, **complete** Linux and the permanent Linux release check executing `make release-check`. Any failure is classified first; a correction creates a new candidate rather than amending this one.

## Phase-end rule

`docs/V3-FINAL-CERTIFICATION-PHASE-END.md` is authoritative for Step 8. Do not weaken tests, redistribute proprietary fonts, or convert librarian item 33 into speculative runtime behavior.
