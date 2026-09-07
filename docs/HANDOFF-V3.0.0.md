# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation merge | `85cf22b6fe5d117bb2611a2865911e0d20a19363` |
| Active phase | **Scientific Article** |
| Steps 1–6 | **ACCEPTED** |
| Step 6 acceptance | `e941a7f9b4685a9bcf687135e8d5168af2d69ec7`; Static `34146793998`; Linux `34146794016` |
| Step 7 artifact source | `f62ac703d8992af96b79cf83e125350ee561bd92` |
| Step 7 artifact run | `34153348385` — SUCCESS; artifact `10030160290` |
| Step 7 visual review | **PASS — 5/5 pages, unexplained visual FAIL 0** |
| Step 7 state | **VISUAL-PASS — CLEANUP CHECKPOINT CI PENDING** |
| Temporary executor | removed in current synchronized cleanup checkpoint |
| Step 8 | QUEUED — immutable complete phase-end regression |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Final Certification | QUEUED |
| Release | QUEUED |

## Step 7 artifact result

The canonical Scientific Article PDF is a real TeX Live 2026/pdfLaTeX build of `template/scientific-article.tex` from SHA `f62ac703...`.

| Artifact fact | Value |
|---|---|
| PDF SHA-256 | `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db` |
| Size | 129791 bytes |
| Pages | 5 |
| Geometry | A4 (`595.276 x 841.89 pt`) |
| PDF version | 1.7 |
| Embedded fonts | PASS |
| Complete visual review | PASS — 5/5 |

No clipping, overlap, broken glyph or unexplained blank page was observed. Article front block, optional foreign elements, body hierarchy, footnotes, citations and references rendered coherently. No academic-work-only front-matter element leaked into the article output.

Primary sections start on new pages, leaving substantial whitespace on pages 2 and 4. The retained 18-rule contract does not define continuity/no-page-break behavior for primary article sections, so this is classified **OBSERVATION — NON-BLOCKING UNDER CURRENT AUTHORITY** rather than silently promoted to a new requirement.

## Immediate action

1. let the synchronized cleanup checkpoint run Static contract and its selected Linux scope;
2. classify any failure before changing predicates/runtime;
3. if green, mark Step 7 ACCEPTED and activate Step 8;
4. create one immutable Step 8 candidate for Static + **complete** Linux plus article-specific gates;
5. close Scientific Article and activate Final Certification only after Step 8 succeeds.

## What still blocks V3 completion

| Blocker | State |
|---|---|
| Scientific Article Step 7 cleanup acceptance | CI PENDING |
| Scientific Article Step 8 phase-end regression | QUEUED |
| PR #286 / issue #280 | remain open until Scientific Article acceptance |
| Final Certification | not executed on final candidate |
| Issue #18 deterministic release-reference-PDF reproducibility | open release blocker |
| Release packaging/tag/assets/publication | not executed |
| Librarian item 33 | explicit `NORMATIVE-REVIEW`, fail-closed |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA. Scoped intermediate checks never authorize a phase transition.
