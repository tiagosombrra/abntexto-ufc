# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 4 CLEANUP VALIDATION

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | **PROOF PASS — CLEANUP VALIDATION PENDING** | bounded run `34219229025`; temporary executor removed; cleanup Static/Linux required |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded `34175388675` PASS; cleanup `7307164...`, Static `34208318971`, Linux `34208318754` PASS |
| 6 | Distribution/public bundle integrity | ACCEPTED | 4 bundles, checksums and archive integrity PASS; cleanup accepted |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

Steps 5-6 acceptance was synchronized at `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750` and Linux `34218086734` passed.

## Step 4 proof result

Bounded run `34219229025` executed on source checkpoint `fae338e16304ad45c353067a0b7982f73a8363c5` and completed successfully.

| Family | Engine | Literal build | Unicode | Embedding | PDF/A-2b |
|---|---|---|---|---|---|
| Times New Roman | pdfLaTeX | PASS | PASS | PASS | PASS |
| Arial | pdfLaTeX | PASS | PASS | PASS | PASS |
| Times New Roman | LuaLaTeX | PASS | PASS | PASS | PASS |
| Arial | LuaLaTeX | PASS | PASS | PASS | PASS |

The Windows job generated four strict PDFs from fonts already installed on the hosted Windows runner. Artifact `10053151610` contained only those four generated PDFs, with one-day retention; artifact ZIP digest was `sha256:6b0cd0a6ac2543017a8496a1af7feeca70640f2b73862311a4325a981dc5fb60`. No raw proprietary font files were uploaded or committed.

The Linux certification job emitted:

`FINAL-CERTIFICATION-EVIDENCE surface=literal-font-unicode-embedding status=PASS families=Times-New-Roman,Arial engines=pdflatex,lualatex unicode=PASS embedding=PASS pdfa=PASS`

The temporary executor `.github/workflows/final-cert-literal-fonts.yml` has now been removed. Per the acceptance contract, Step 4 remains open until this cleanup checkpoint passes Static contract and Linux integration.

## Step 7 boundary

Issue #18 remains a release-build reproducibility concern. The permanent gate must pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
