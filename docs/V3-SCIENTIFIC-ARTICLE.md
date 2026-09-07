# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 7 PROVENANCE BUILD

## Entry and current state

Core Corrections and Reference PDF Validation are closed. Canonical `main` is `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`. Active article work remains PR #286 on `feat/v3-scientific-article`, reconciled with current main through `85cf22b6fe5d117bb2611a2865911e0d20a19363`.

The retained article authority product remains `4d018a92697e8f39e3a53b034c451e55996c84fb`, represented by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`. There are exactly 18 source-backed article rules.

## Progress

| Step | Work | State | Evidence / next gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | completed |
| 2 | Required article front block | ACCEPTED | completed |
| 3 | Optional foreign title and summary | ACCEPTED | completed |
| 4 | Textual structure and body typography | ACCEPTED | completed |
| 5 | Recommendations and conditional applicability | ACCEPTED | `55fa1c8...`; Static `34132291198`; Linux `34132291304` |
| 6 | Evidence hardening | **ACCEPTED** | `e941a7f9...`; Static `34146793998`; Linux `34146794016`; exact 18-rule map; zero validation-mode promotions |
| 7 | Canonical article PDF | **ACTIVE — PROVENANCE BUILD** | `template/scientific-article.tex` + temporary artifact workflow |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 6 acceptance

The accepted evidence map covers exactly all 18 retained IDs and records source-contract normativity, current validation mode, article-specific owner where present, evidence kind, conservative proof disposition and promotion state. It promotes zero validation modes. Optionality, recommendations and journal-precedence applicability remain unchanged.

## Step 7 canonical article PDF

Canonical source: `template/scientific-article.tex`.

Validation record: `docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md`.

Temporary executor: `.github/workflows/tmp-scientific-article-pdf.yml` — **ACTIVE only until artifact recovery**.

The canonical source exercises the accepted article front block, optional foreign title/summary, primary summary/keywords, author metadata, required textual structure, subsection hierarchy, a footnote, citations and references while excluding academic-work-only front matter.

The temporary workflow builds that source using TeX Live 2026/pdfLaTeX and uploads the PDF together with `pdfinfo`, `pdffonts`, extracted text, SHA-256, file size and Git/workflow provenance. It is not a permanent workflow and must be removed before Step 7 acceptance.

Required visual review scope remains: article front block, optional foreign elements, typography, body structure, citations/references, footnotes, leakage absence and global visual quality. Every page must be rendered at 200 DPI and inspected.

Synthetic or stale PDFs are inadmissible. Any defect must be classified before runtime/test changes and the artifact rebuilt/re-rendered after correction.

## Step 8 phase-end regression

Scientific Article closes only when one immutable candidate passes Static contract, Linux integration with **complete** scope, all article-specific executable gates and accepted canonical article PDF visual/provenance evidence. Scoped article checks are intermediate evidence only and never replace Step 8.

## What remains after Scientific Article

Final Certification must still cover the complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must establish deterministic release-reference-PDF reproducibility with pinned epoch/SOURCE_DATE_EPOCH and stable hash evidence. Release then finalizes bundles, checksums, tag/GitHub Release and external publication actions.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Documentation discipline

Every **material advance** updates the relevant execution documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
