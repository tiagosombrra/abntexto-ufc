# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 6 ACCEPTED / STEP 7 CANONICAL PDF ACTIVE

## Entry and current state

Core Corrections and Reference PDF Validation are closed. Canonical `main` is `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`. Active article work remains PR #286 on `feat/v3-scientific-article`, reconciled with current main through `85cf22b6fe5d117bb2611a2865911e0d20a19363`.

The retained article authority product remains `4d018a92697e8f39e3a53b034c451e55996c84fb`, represented by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`. There are exactly 18 source-backed article rules.

## Progress

| Step | Work | State | Evidence / next gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425` |
| 5 | Recommendations and conditional applicability | ACCEPTED | `55fa1c8...`; Static `34132291198`; Linux `34132291304`; article scope `PASS=6 FAIL=0 SKIP=0` |
| 6 | Evidence hardening | **ACCEPTED** | `e941a7f9...`; Static `34146793998`; Linux `34146794016`; exact 18-rule map; zero validation-mode promotions |
| 7 | Canonical article PDF | **ACTIVE** | real TeX Live 2026 PDF + provenance + complete page-level visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 6 acceptance

Step 6 added `standards/article-evidence-map.json` and `tests/checks/scientific_article_evidence_map.py`, wired into `tests/static.py`. The synchronized technical checkpoint `e941a7f9b4685a9bcf687135e8d5168af2d69ec7` passed Static `34146793998` and Linux `34146794016`.

The accepted map covers exactly all 18 retained IDs and records source-contract normativity, current validation mode, article-specific owner where present, evidence kind, conservative proof disposition and promotion state. It promotes zero validation modes. Optionality, recommendations and journal-precedence applicability remain unchanged.

## Step 7 canonical article PDF

Step 7 now becomes the active work. Produce a real article PDF from the accepted branch using the project runtime and TeX Live 2026. Bind the artifact to Git provenance and inspect every page.

Required review scope:

| Review surface | Required observation |
|---|---|
| Primary title and authorship | correct article front block, no academic-work cover/title-page semantics |
| Optional foreign title/summary | rendered only when configured; no forced optional content |
| Primary summary / keywords | correct ordering and legible presentation |
| Dates and author metadata footnote | present where configured and visually coherent |
| Body structure | introduction, development, final considerations and references |
| Body typography | no unexpected family/size/spacing drift |
| Citations/references | readable and consistent with shared accepted bibliography runtime |
| Footnotes | no overlap, clipping or typography anomaly |
| Leakage | no cover, approval page, catalog card, dedication, academic abstract/list/TOC leakage unless article contract explicitly requires it |
| Global visual quality | no clipping, overlap, broken glyph, unexplained blank page or page-boundary anomaly |

Step 7 acceptance requires a provenance record containing source SHA, workflow run, TeX Live 2026, engine, source path, PDF SHA-256, size, page count, geometry/PDF version and font-embedding preflight where measurable. Synthetic or stale PDFs are inadmissible.

Any temporary artifact-build workflow is permitted only as an executor for this bounded step and must be removed before Step 7 acceptance.

## Step 8 phase-end regression

Scientific Article closes only when one immutable candidate passes Static contract, Linux integration with **complete** scope, all article-specific executable gates and accepted canonical article PDF visual/provenance evidence.

Scoped article checks are intermediate evidence only and never replace Step 8.

## What remains after Scientific Article

Final Certification must still cover the complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must establish deterministic release-reference-PDF reproducibility with pinned epoch/SOURCE_DATE_EPOCH and stable hash evidence. Release then finalizes bundles, checksums, tag/GitHub Release and external publication actions.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Documentation discipline

Every **material advance** updates the relevant execution documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
