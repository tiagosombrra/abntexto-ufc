# V3 Final Certification

Updated: 2026-09-08
Status: ACTIVE — STEP 4 BOUNDED LITERAL-FONT PROOF

## Purpose

Final Certification proves the accepted V3 product across the remaining bounded release surfaces without reopening closed shared or Scientific Article semantics. Every **material advance** is synchronized with roadmap, handoff, readiness and machine state. Final Certification closes only after one immutable **phase-end regression** candidate passes the complete applicable matrix.

## Step status

| Step | Certification surface | State | Current evidence / next gate |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | branch/PR and control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | release `34168471371`, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; cleanup Static/Linux green |
| 3 | Profile/engine matrix | ACCEPTED | current complete release evidence |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | **ACTIVE — BOUNDED PROOF** | temporary Windows/Linux executor active |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded `34175388675` PASS; cleanup `7307164...`, Static `34208318971`, Linux `34208318754` PASS |
| 6 | Distribution/public bundle integrity | ACCEPTED | 4 bundles, checksums and archive integrity PASS; cleanup accepted |
| 7 | Deterministic release reference PDF / issue #18 | QUEUED | two clean builds, identical SHA-256, preserved validation |
| 8 | Final Certification phase-end regression | QUEUED | one immutable candidate with complete matrix |

Steps 5-6 acceptance was synchronized at `237cb53b65c91052a469ab67991ea78e71ade283`; Static `34218086750` and Linux `34218086734` passed.

## Step 4 acceptance contract

Temporary executor: `.github/workflows/final-cert-literal-fonts.yml`.

Fresh current-candidate evidence must cover all four combinations:

| Family | Engine | Required proof |
|---|---|---|
| Times New Roman | pdfLaTeX | literal family identity, Unicode extraction, embedding, PDF/A-2b |
| Arial | pdfLaTeX | literal family identity, Unicode extraction, embedding, PDF/A-2b |
| Times New Roman | LuaLaTeX | literal family identity, Unicode extraction, embedding, PDF/A-2b |
| Arial | LuaLaTeX | literal family identity, Unicode extraction, embedding, PDF/A-2b |

The Windows job prepares local TeX support from fonts already installed on the Windows runner and compiles four strict PDFs. The artifact contains only those bounded generated PDFs with one-day retention. Raw proprietary font files are not uploaded, committed or included in public/distribution bundles. A Linux job runs the current `tests/integration/windows-font-pdfa.sh` contract.

The existing `font-poc.sh` diagnostics are normalized to project-owned English in the same advance; test literals in Portuguese remain unchanged because they are intentional Unicode extraction content.

Step 4 does not become ACCEPTED from a successful bounded run alone. The workflow must then be removed and the cleanup checkpoint must pass Static and Linux.

## Step 7 boundary

Issue #18 remains a release-build reproducibility concern. The permanent gate must pin deterministic provenance time, perform at least two clean reference-PDF rebuilds, compare SHA-256 exactly and preserve existing PDF validation/font/PDF-A checks.

## Phase-end rule

Final Certification closes only when Steps 4-7 are accepted, temporary executors are absent, documentation is synchronized and one immutable candidate passes Static, complete Linux and the full applicable release/certification matrix. `phase_end_regression.candidate = one-immutable-sha` remains the machine sentinel until that candidate is created.
