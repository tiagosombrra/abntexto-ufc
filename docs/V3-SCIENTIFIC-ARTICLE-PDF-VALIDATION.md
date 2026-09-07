# V3 Scientific Article PDF Validation

Updated: 2026-09-07  
Status: ACCEPTED

## Artifact provenance

| Field | Observation |
|---|---|
| Source/build SHA | `f62ac703d8992af96b79cf83e125350ee561bd92` |
| Workflow run | `34153348385` — SUCCESS |
| Artifact ID | `10030160290` |
| Artifact name | `v3-scientific-article-pdf-f62ac703d8992af96b79cf83e125350ee561bd92` |
| Artifact ZIP digest | `sha256:8b9823271995b2a760f671bcdc636381e8134419382c9d898642310eaeb60052` |
| TeX Live | 2026 |
| Engine | pdfLaTeX / pdfTeX `1.40.29` |
| Source path | `template/scientific-article.tex` |
| PDF SHA-256 | `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db` |
| Size | 129791 bytes |
| Pages | 5 |
| Geometry | A4, `595.276 x 841.89 pt` |
| PDF version | 1.7 |
| Embedded fonts | PASS |

The artifact is a real project-class build from a concrete Git SHA; it is not synthetic and is not reused from the academic-work reference PDF.

## Complete visual review

The PDF was rendered at 200 DPI and every page was inspected.

| Page | Main surface | Result |
|---:|---|---|
| 1 | title, authorship, dates, primary/foreign summaries, keywords, author note | PASS |
| 2 | Introduction and footnote | PASS |
| 3 | Development, subsections and citations | PASS |
| 4 | Final Considerations | PASS |
| 5 | References | PASS |

Summary: **5/5 pages PASS; unexplained visual FAIL = 0**. No clipping, overlap, broken glyph, unexplained blank page or academic-work-only front-matter leakage was observed.

## Classified observation

Primary sections begin on new pages, creating visible whitespace on pages 2 and 4. The retained 18-rule Scientific Article contract does not define a continuity/no-page-break predicate. Classification remains **OBSERVATION — NON-BLOCKING UNDER CURRENT AUTHORITY**.

## Cleanup and final acceptance

The temporary artifact-build workflow was removed before checkpoint acceptance. Cleanup checkpoint `923d11ef668b02ec4de3cad4906ad5ac1f527eaf` then passed:

| Gate | Result |
|---|---|
| Static contract | `34154045481` — SUCCESS |
| Linux integration | `34154045509` — SUCCESS |
| Linux scope | `complete` |
| Summary | `PASS=36 FAIL=0 SKIP=0` |
| Temporary executor | absent |

Therefore Step 7 is **ACCEPTED**. Because this same immutable checkpoint also ran complete Linux with all article-specific gates, it is the accepted Step 8 phase-end candidate as recorded in `docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md`.

## Documentation discipline

This acceptance is a **material advance** and is synchronized with handoff, roadmap and machine state. Every later phase retains its own mandatory **phase-end regression**.
