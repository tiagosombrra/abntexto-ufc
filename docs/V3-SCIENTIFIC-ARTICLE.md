# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 7 VISUAL PASS / CLEANUP CI PENDING

## Current state

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
| 6 | Evidence hardening | ACCEPTED | `e941a7f9...`; Static `34146793998`; Linux `34146794016`; exact 18-rule map; zero validation-mode promotions |
| 7 | Canonical article PDF | **VISUAL-PASS — CLEANUP CI PENDING** | artifact from `f62ac703...`; run `34153348385`; 5/5 visual PASS; executor removed in cleanup checkpoint |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 7 result

Canonical source: `template/scientific-article.tex`.

Artifact build:

- source SHA `f62ac703d8992af96b79cf83e125350ee561bd92`;
- temporary workflow run `34153348385` — SUCCESS;
- artifact ID `10030160290`;
- PDF SHA-256 `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db`;
- 129791 bytes;
- 5 A4 pages;
- PDF 1.7;
- all listed fonts embedded.

Complete 200-DPI inspection reviewed 5/5 pages. Article front block, optional foreign elements, body hierarchy, footnotes, citations and references are visually coherent. No clipping, overlap, broken glyph, unexplained blank page or academic-work-only front-matter leakage was observed.

The shared section mechanism starts primary sections on new pages and therefore creates visible whitespace on pages 2 and 4. `standards/coverage-rules-article.json` does not define a continuity/no-page-break requirement. This is recorded as **OBSERVATION — NON-BLOCKING UNDER CURRENT AUTHORITY** and is not converted into a new runtime predicate.

`docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md` is the complete Step 7 provenance/visual record.

The temporary workflow used only for artifact generation is removed by the synchronized cleanup checkpoint. Step 7 final acceptance waits for that cleanup checkpoint's Static contract and selected Linux scope.

## Step 8 phase-end regression

After Step 7 acceptance, Scientific Article closes only when one immutable candidate passes Static contract, Linux integration with **complete** scope, all article-specific executable gates and accepted canonical article PDF evidence. Scoped article checks are intermediate evidence only and never replace Step 8.

## Remaining V3 work

Final Certification must still cover the complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must establish deterministic release-reference-PDF reproducibility with pinned epoch/SOURCE_DATE_EPOCH and stable hash evidence. Release then finalizes bundles, checksums, tag/GitHub Release and external publication actions.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Documentation discipline

Every **material advance** updates the relevant execution documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
