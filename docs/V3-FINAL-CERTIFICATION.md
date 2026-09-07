# V3 Final Certification — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — RELEASE BASELINE CLEANUP CANDIDATE

## Entry facts

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481` SUCCESS; Linux `34154045509` SUCCESS with `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; canonical article PDF visual review PASS 5/5.

PR #286 was squash-merged into canonical `main` as `22e3c19235fa5245505b92d919a09d31eb2bfecb`. Active branch `cert/v3-final-certification` / PR #289 was created from exactly that SHA.

Entry synchronization checkpoint `aa6cc4a1754bae4ee1b9b89b58441e6cf44d7951` passed Static `34161228915`; Linux `34161228823` succeeded with documentation-only heavy skip. Step 1 is accepted.

## Certification sequence

| Step | Work | State | Acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and branch handoff | **ACCEPTED** | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS |
| 2 | Linux release baseline | **PASS EXECUTION — CLEANUP CI PENDING** | transport `f8be323...`; Static `34168471299`; Linux `34168471312`; release run `34168471371`; `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; artifact `10035242168`; executor removed in cleanup candidate |
| 3 | Profile and engine matrix | QUEUED | all supported document profiles and required pdfLaTeX/LuaLaTeX surfaces remain green |
| 4 | Literal fonts, Unicode and embedding | QUEUED | required Times New Roman/Arial identity evidence, Unicode extraction and embedding pass without proprietary-font redistribution |
| 5 | PDF/A certification | QUEUED | PDF/A-2b evidence passes on final candidate using established certification route |
| 6 | Distribution/public bundles | QUEUED | bundle/package integrity and distribution checks pass from same candidate |
| 7 | Deterministic release reference PDF — issue #18 | QUEUED | pinned deterministic epoch, two clean builds and identical SHA-256 while existing visual/text/font/PDF-A evidence stays intact |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux, release/certification matrix and phase-specific evidence |

## Linux release baseline result

The temporary PR executor ran the exact permanent repository command `make release-check` in TeX Live 2026. Run `34168471371` completed successfully with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

The transport SHA `f8be323027b42eefcdbe3d13b2f269abdd6ec17f` also passed Static `34168471299` and normal Linux integration `34168471312`. The release-baseline validation artifact is `10035242168`, digest `sha256:d5f3f75c29e294728dbc59fe569b2aba8cfc7f7ba23d05eb80bc7abfdf302604`.

The temporary executor has now been removed in the current cleanup candidate. This material advance is not yet Step 2 acceptance: the cleanup candidate must itself pass Static and Linux first. If either fails, classify the failure before any code/test change.

## Baseline-first rule

Do not modify release/certification machinery until the cleanup candidate is classified. After Step 2 acceptance, proceed to the profile/engine evidence inventory. Reuse prior proof only where provenance/applicability remains valid; rerun when final-candidate identity is required by the phase exit.

## Issue #18 boundary

Issue #18 is a P0 v3.0.0 release blocker. Acceptance requires one deterministic release epoch (`SOURCE_DATE_EPOCH` or equivalent documented mechanism), stable PDF metadata/document ID, at least two controlled clean builds of the same reference PDF and identical SHA-256 digests. Reproducibility is additional evidence and must not replace existing visual/text/font/PDF-A validation.

## Non-negotiable boundaries

- Do not reopen accepted shared or Scientific Article runtime solely for packaging/reproducibility concerns.
- Preserve librarian review state 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW.
- Item 33 remains fail-closed absent authoritative current NBR 6023:2025 evidence.
- Do not redistribute proprietary Microsoft fonts.
- Linux release evidence does not by itself substitute for literal-font/platform/PDF-A certification.
- CTAN/external publication remains blocked until Release.
- Tests and validators are not weakened to obtain green status.

## Phase exit

Final Certification closes only after its complete **phase-end regression** passes on one immutable candidate and all certification evidence is recorded. A **material advance** must update this plan, handoff, roadmap and machine state in the same work cycle.
