# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 4 LITERAL-FONT / UNICODE / EMBEDDING

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | **ACTIVE** | fresh current-candidate Windows proof required |
| 5 | Scientific Article PDF/A-2b | **ACCEPTED** | bounded `34175388675` PASS; cleanup `7307164...`, Static `34208318971`, Linux `34208318754` PASS |
| 6 | Distribution/public bundle integrity | **ACCEPTED** | 4 bundles, checksums and archive integrity PASS; cleanup accepted |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

## Steps 5-6 lifecycle closure

The successful bounded checkpoint `13e491d18d46a86835b4ab1d7f331f6f09f38849` passed Static `34175388673`, Linux `34175388665` and bounded release `34175388675`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

Step 5 evidence:

`FINAL-CERTIFICATION-EVIDENCE surface=scientific-article-pdfa status=PASS profile=scientific-article engine=pdflatex pdfa=2b font_embedding=PASS`

Step 6 evidence:

`FINAL-CERTIFICATION-EVIDENCE surface=distribution-bundles status=PASS version=3.0.0 artifacts=4 checksums=PASS archive_integrity=PASS source_date_epoch=1788829436 proprietary_fonts_redistributed=false`

The proof-only `.github/workflows/final-cert-bounded-matrix.yml` was removed at `7307164ba4cf924beecb6678c7af5b79d551d513`. Cleanup Static `34208318971` and Linux `34208318754` both succeeded. Steps 5-6 are therefore ACCEPTED and no temporary executor remains active.

## Step 4 acceptance contract

Fresh current-candidate evidence must cover all four combinations:

| Family | Engine | Required proof |
|---|---|---|
| Times New Roman | pdfLaTeX | literal family identity, Unicode extraction, embedding |
| Arial | pdfLaTeX | literal family identity, Unicode extraction, embedding |
| Times New Roman | LuaLaTeX | literal family identity, Unicode extraction, embedding |
| Arial | LuaLaTeX | literal family identity, Unicode extraction, embedding |

Windows runner fonts may be used for proof, but proprietary font files must never be committed, uploaded as standalone artifacts or redistributed in bundles. PDF artifacts may be used only as bounded certification evidence. Reuse existing `tools/prepare-windows-fonts.ps1`, `tests/integration/font-poc.sh` and `tests/integration/windows-font-pdfa.sh` where they still represent the current product contract; historical V2 certification is precedent, not acceptance evidence for the current candidate.

If a temporary Step 4 workflow is required, its lifecycle is create -> execute -> validate -> remove -> cleanup Static/Linux. Step 4 becomes ACCEPTED only after both proof and cleanup are recorded.

## Step 7 boundary

Issue #18 remains a release-build reproducibility concern. The permanent gate must pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
