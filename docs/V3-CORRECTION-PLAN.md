# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-08  
Status: SHARED CORRECTIONS AND SCIENTIFIC ARTICLE CLOSED — FINAL CERTIFICATION STEP 8 CANDIDATE ACTIVE

## Purpose

This document preserves the correction history produced by Regression Audit and the phase boundaries built on that corrected foundation. Active certification execution is defined in `docs/V3-FINAL-CERTIFICATION.md`.

## Execution discipline

Every **material advance** updates the relevant implementation/review/certification state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace that gate.

## Accepted shared foundation

Core Corrections closed on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Reference PDF Validation closed on `b64074c64941895f97fbe0f795ce826c798d17ce` with 55/55 page-level visual PASS.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Items 1–32 and 34 are PASS. Item 33 remains a fail-closed current-authority gap.

## Scientific Article closeout

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481`, complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`, and canonical article PDF 5/5 visual PASS. PR #286 merged into main as `22e3c19235fa5245505b92d919a09d31eb2bfecb`.

## Final Certification accepted work

| Step | State | Evidence |
|---:|---|---|
| 1-3 | ACCEPTED | entry, Linux release baseline and profile/engine matrix accepted |
| 4 | ACCEPTED | literal Times New Roman/Arial, Unicode, embedding and PDF/A proof `34219229025`; cleanup accepted |
| 5 | ACCEPTED | Scientific Article PDF/A-2b evidence accepted |
| 6 | ACCEPTED | distribution/public bundle integrity and deterministic transport accepted |
| 7 | ACCEPTED | deterministic reference PDF proof `34231038578`; two clean builds hash `1c92535f...`; cleanup `34e6bf8...`; issue #18 closed |
| 8 preparation | ACCEPTED | `4d94e9c...`; Static `34235990523`; complete Linux `34235990383`, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| 8 candidate | **RUNNING** | synchronized immutable candidate must pass Static + complete Linux + Linux release check |

Earlier Step 5/6 runner-transport failures are historical and resolved; they are not current correction work and do not reopen accepted runtime or normative predicates.

## Current batch — Final Certification Step 8 immutable candidate

The accepted permanent PR transport uses the one-shot `release/final-certification-candidate.json` marker to run the existing `make release-check` contract before merge. The synchronized candidate contains the marker and candidate-running control state and is not amended after CI begins.

Marker-only/intermediate commits that did not synchronize documentation are rejected as candidates. The exact synchronized candidate SHA is recorded after creation in PR/evidence metadata while the machine invariant remains `phase_end_regression.candidate = one-immutable-sha`.

Required acceptance:

1. Static contract success;
2. complete Linux integration success;
3. Linux release check success using permanent `make release-check`;
4. deterministic reference PDF, literal-font, Unicode, embedding, PDF/A and bundle predicates remain accepted;
5. no temporary executor;
6. item 33 remains fail-closed.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed edge cases.

## Phase transition gate

Final Certification -> Release requires the complete certification matrix and one immutable Final Certification candidate passing the phase-end regression. Only after that evidence is recorded may the marker be removed and Release become active in a synchronized phase-transition commit.
