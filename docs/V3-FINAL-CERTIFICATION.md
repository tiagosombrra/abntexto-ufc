# V3 Final Certification — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — ENTRY SYNCHRONIZATION

## Purpose

Certify one final v3.0.0 candidate across the complete runtime, platform/font, PDF/A and distribution surfaces without reopening accepted Scientific Article or shared-foundation semantics.

Scientific Article closed on immutable candidate `923d11ef668b02ec4de3cad4906ad5ac1f527eaf`: Static `34154045481` SUCCESS; Linux `34154045509` SUCCESS with `SCOPE=complete PASS=36 FAIL=0 SKIP=0`; canonical article PDF visual review PASS 5/5.

## Entry boundary

The phase is active for transition/entry synchronization only while PR #286 remains open on `feat/v3-scientific-article`. No Final Certification runtime change should be made on that transition branch. After synchronized transition checks are green:

1. merge PR #286 into `main`;
2. read the resulting canonical `main` SHA;
3. create fresh branch `cert/v3-final-certification` from that exact main;
4. synchronize branch/main facts before technical certification work.

## Certification sequence

| Step | Work | State | Acceptance |
|---:|---|---|---|
| 1 | Entry synchronization and branch handoff | ACTIVE | article phase closed, PR #286 merged, fresh certification branch from updated main |
| 2 | Linux release baseline | QUEUED | permanent `Linux release check` / `make release-check` green on certification candidate |
| 3 | Profile and engine matrix | QUEUED | all supported document profiles and required pdfLaTeX/LuaLaTeX surfaces remain green |
| 4 | Literal fonts, Unicode and embedding | QUEUED | required Times New Roman/Arial identity evidence, Unicode extraction and embedding pass without proprietary-font redistribution |
| 5 | PDF/A certification | QUEUED | PDF/A-2b evidence passes on the final candidate using the established certification route |
| 6 | Distribution/public bundles | QUEUED | bundle/package integrity and distribution checks pass from the same candidate |
| 7 | Deterministic release reference PDF — issue #18 | QUEUED | pinned deterministic epoch, two clean builds and identical SHA-256 evidence while existing visual/text/font/PDF-A evidence remains intact |
| 8 | Final Certification phase-end regression | QUEUED | one immutable SHA passes Static, complete Linux, release/certification matrix and phase-specific evidence |

## Issue #18 boundary

Issue #18 is a P0 v3.0.0 release blocker. The solution must add reproducibility evidence, not alter article or shared normative semantics. Acceptance requires a deterministic release epoch (`SOURCE_DATE_EPOCH` or equivalently documented mechanism), stable PDF metadata/document ID, at least two controlled clean builds of the same reference PDF and identical SHA-256 digests.

## Non-negotiable boundaries

- Do not reopen accepted shared or Scientific Article runtime solely to satisfy packaging/reproducibility concerns.
- Preserve the 34-point librarian-review state: 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW.
- Item 33 remains fail-closed absent authoritative current NBR 6023:2025 evidence.
- Do not redistribute proprietary Microsoft fonts.
- Linux release evidence does not by itself substitute for literal-font/platform/PDF-A certification.
- CTAN/external publication remains blocked until Release.
- Tests and validators are not weakened to obtain green status.

## Phase exit

Final Certification closes only after its complete **phase-end regression** passes on one immutable candidate and all certification evidence is recorded. A **material advance** must update this plan, handoff, roadmap and machine state in the same work cycle.
