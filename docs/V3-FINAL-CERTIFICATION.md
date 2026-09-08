# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 8 RELEASE-MATRIX TRANSPORT PREPARATION

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
| 8 | Final Certification phase-end regression | **PREPARATION** | validate PR transport, then create immutable candidate |

## Step 7 accepted evidence

Cleanup checkpoint `34e6bf8299e582803d1726e8dd699271c356fda5` passed Static `34232017286` and complete Linux `34232017359`, `PASS=36 FAIL=0 SKIP=0`, with the temporary executor absent and permanent `make release-reference-reproducibility` retained. Issue #18 is closed.

## Step 8 orchestration

The permanent `linux-release-check.yml` is being extended with a narrowly scoped PR trigger on `release/final-certification-candidate.json`. This does not introduce a new validator: it transports the existing permanent `make release-check` contract onto the immutable PR candidate. Normal `main` push and manual-dispatch behavior remain intact.

The orchestration preparation checkpoint must pass Static and complete Linux before candidate creation. The candidate marker is then added in one immutable candidate commit, causing Static, complete Linux and Linux release check to execute against that candidate. After acceptance, the marker is removed during phase transition.

## Phase-end rule

`docs/V3-FINAL-CERTIFICATION-PHASE-END.md` is authoritative for Step 8. Do not amend the immutable candidate after CI begins, weaken tests, redistribute proprietary fonts, or convert librarian item 33 into speculative runtime behavior.
