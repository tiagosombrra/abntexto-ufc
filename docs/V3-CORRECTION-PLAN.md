# abntexto-ufc v3 — Correction Plan

Updated: 2026-09-07  
Status: SHARED CORRECTIONS AND SCIENTIFIC ARTICLE CLOSED — FINAL CERTIFICATION ACTIVE

## Purpose

This document preserves the correction history produced by Regression Audit and the phase boundaries built on that corrected foundation. Active certification execution is defined in `docs/V3-FINAL-CERTIFICATION.md`.

## Execution discipline

Every **material advance** updates the relevant implementation/review/certification state and canonical handoff in the same work cycle. Every phase has a mandatory **phase-end regression** on one immutable candidate SHA. Targeted green checks and visual review never replace that gate.

## Accepted shared foundation

Core Corrections closed on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Reference PDF Validation closed on `b64074c64941895f97fbe0f795ce826c798d17ce` with 55/55 page-level visual PASS.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Items 1–32 and 34 are PASS. Item 33 remains a fail-closed current-authority gap.

## Scientific Article closeout

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481`, complete Linux `34154045509`, `PASS=36 FAIL=0 SKIP=0`, and canonical article PDF 5/5 visual PASS. PR #286 is merged into main as `22e3c19235fa5245505b92d919a09d31eb2bfecb`.

## Active work — Final Certification

Entry synchronization, Linux release baseline and the profile/engine matrix are accepted. The first bounded Step 5/6 transport on `21455c3344bfe0413dbe44f29b9cfae5bee58521` produced Static `34172047639` PASS and Linux `34172047586` PASS. Release transport `34172047786` ran the existing permanent matrix to `SCOPE=complete PASS=38 FAIL=0 SKIP=0` and then passed the explicit Scientific Article PDF/A/embedding gate.

The run failed only when Step 6 attempted to derive the deterministic bundle epoch with Git inside the TeX Live Docker container. Git rejected the mounted checkout because of ownership mismatch (`dubious ownership`). The failure is therefore classified inside Step 6 runner integration; no accepted runtime, normative or evidence predicate is reopened.

Current correction:

1. keep the distribution bundle checks unchanged;
2. perform the provenance timestamp read with `git -c safe.directory="$PWD"`;
3. use full Git history in the temporary transport so the exact `SOURCE_COMMIT_SHA` can be resolved;
4. rerun the same permanent `make release-check` contract;
5. after PASS, remove the temporary workflow and require cleanup Static/Linux before Steps 5-6 acceptance.

Remaining sequence after that cleanup: current-candidate literal-font/Unicode/embedding Step 4; issue #18 deterministic reference PDF; Final Certification immutable phase-end regression; Release.

Certification and reproducibility work do not authorize speculative normative changes.

## Remaining authority boundary

Review item 33 remains fail-closed pending authoritative current NBR 6023:2025 text for disputed edge cases.

## Phase transition gate

Final Certification -> Release requires the complete certification matrix, issue #18 acceptance, synchronized documentation and one immutable Final Certification candidate passing Static, complete Linux, release/certification evidence and all applicable phase-specific checks.
