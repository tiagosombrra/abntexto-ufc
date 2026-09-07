# V3 Final Certification — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — RELEASE BASELINE EXECUTOR

## Entry facts

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481` SUCCESS; Linux `34154045509` SUCCESS with `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; canonical article PDF visual review PASS 5/5.

PR #286 was squash-merged into canonical `main` as `22e3c19235fa5245505b92d919a09d31eb2bfecb`. Active branch `cert/v3-final-certification` / PR #289 was created from exactly that SHA.

Entry synchronization checkpoint `aa6cc4a1754bae4ee1b9b89b58441e6cf44d7951` passed Static `34161228915`; Linux `34161228823` succeeded with documentation-only heavy skip. Step 1 is accepted.

## Certification sequence

| Step | Work | State | Acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and branch handoff | **ACCEPTED** | `aa6cc4a...`; Static `34161228915`; Linux `34161228823` SUCCESS, docs-only heavy skip |
| 2 | Linux release baseline | **ACTIVE — TEMPORARY EXECUTOR** | exact permanent `make release-check` green; validation evidence recorded; executor removed before acceptance |
| 3 | Profile and engine matrix | QUEUED | all supported document profiles and required pdfLaTeX/LuaLaTeX surfaces remain green |
| 4 | Literal fonts, Unicode and embedding | QUEUED | required Times New Roman/Arial identity evidence, Unicode extraction and embedding pass without proprietary-font redistribution |
| 5 | PDF/A certification | QUEUED | PDF/A-2b evidence passes on final candidate using established certification route |
| 6 | Distribution/public bundles | QUEUED | bundle/package integrity and distribution checks pass from same candidate |
| 7 | Deterministic release reference PDF — issue #18 | QUEUED | pinned deterministic epoch, two clean builds and identical SHA-256 while existing visual/text/font/PDF-A evidence stays intact |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux, release/certification matrix and phase-specific evidence |

## Linux release baseline executor

Direct `workflow_dispatch` is not available through the active automation interface, so `.github/workflows/final-cert-release-baseline.yml` is temporarily present on PR #289. It invokes the same TeX Live 2026 environment, dependencies and `make release-check` command as the permanent `.github/workflows/linux-release-check.yml`.

This executor is transport only:

- it introduces no new certification predicate;
- failures are classified before any code/test change;
- generated validation evidence is uploaded when available;
- it must be removed before Step 2 is accepted;
- later literal-font/platform/PDF-A and phase-end evidence remain mandatory.

## Baseline-first rule

Do not modify release/certification machinery until this baseline is classified. Reuse prior proof only where provenance/applicability remains valid; rerun when final-candidate identity is required by the phase exit.

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
