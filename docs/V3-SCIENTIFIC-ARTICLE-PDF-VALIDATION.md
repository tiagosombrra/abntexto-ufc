# V3 Scientific Article PDF Validation

Updated: 2026-09-07  
Status: VISUAL-PASS — CLEANUP CHECKPOINT CI PENDING

## Purpose

This record controls Scientific Article Step 7. Acceptance is based on the real rendered article, not merely on source/runtime tests.

Step 6 is accepted at `e941a7f9b4685a9bcf687135e8d5168af2d69ec7`, with Static `34146793998` and Linux `34146794016` successful.

## Accepted artifact candidate provenance

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
| File size | 129791 bytes |
| Pages | 5 |
| Geometry | A4, `595.276 x 841.89 pt` |
| PDF version | 1.7 |
| Encrypted | no |
| Openable | yes |
| Likely scanned | no |
| XFA | absent |
| Embedded fonts | PASS — TeXGyreTermesX Bold/Regular/Italic embedded |

The artifact is a real project-class build from a concrete Git SHA. It is neither synthetic nor a reused academic-work PDF.

## Canonical source coverage

`template/scientific-article.tex` exercises:

- `type = scientific-article`;
- primary title and complete author placeholder;
- submission and approval dates;
- author metadata note;
- primary summary and keywords;
- optional foreign title and foreign summary;
- Introduction, Development, subsections and Final Considerations;
- a controlled footnote;
- textual citations and a rendered reference list;
- absence of article-irrelevant academic-work front-matter commands.

Extracted output contains the expected article title/authorship, summary/keywords, foreign elements, required textual sections and references. Academic-work-only terms that occur in explanatory prose are not standalone leaked front-matter elements.

## Complete visual review

The PDF was rendered at 200 DPI and every page was inspected.

| Page | Main surface | Result | Notes |
|---:|---|---|---|
| 1 | Article title, author, dates, primary summary/keywords, foreign title/summary, author-note footnote | PASS | coherent ordering; no clipping, overlap or broken glyphs |
| 2 | `1 INTRODUÇÃO`, body paragraphs and controlled footnote | PASS | typography and footnote visually coherent |
| 3 | `2 DESENVOLVIMENTO`, subsections 2.1–2.3 and citations | PASS | hierarchy/citations clean; no overflow |
| 4 | `3 CONSIDERAÇÕES FINAIS` | PASS | clean rendering; no clipping or overlap |
| 5 | `REFERÊNCIAS` | PASS | three references readable; long URL wraps without page overflow |

Summary: **5/5 pages reviewed; unexplained visual FAIL = 0**.

## Visual checklist

| Review surface | State |
|---|---|
| Complete page sequence reviewed | PASS — 5/5 |
| Primary title and authorship | PASS |
| Submission/approval/author-note block | PASS |
| Primary summary and keywords | PASS |
| Optional foreign title and summary | PASS |
| Body section hierarchy and paragraph presentation | PASS |
| Footnote presentation | PASS |
| Citations and references | PASS |
| Academic-work front-matter leakage | PASS — none observed as rendered elements |
| Clipping / overlap / broken glyphs | PASS — none observed |
| Unexpected blank page | PASS — none |
| Global visual quality | PASS |

## Classified observation — primary-section page starts

Pages 2 and 4 contain substantial unused vertical space because the shared section mechanism starts each primary section on a new page. The retained 18-rule Scientific Article contract requires Introduction, Development, Final Considerations and body typography, but does **not** define a continuity/no-page-break predicate between primary sections.

Classification: **OBSERVATION — NON-BLOCKING UNDER CURRENT AUTHORITY**.

This observation is not converted into a runtime defect or a new normative rule. If future authoritative article guidance explicitly constrains primary-section page starts, it must return through authority review before implementation.

## Temporary executor lifecycle

The artifact was recovered successfully from temporary workflow run `34153348385`. The synchronized cleanup checkpoint removes `.github/workflows/tmp-scientific-article-pdf.yml` immediately after recovery, as required by project policy.

Step 7 is not marked finally ACCEPTED until the cleanup checkpoint itself passes the repository Static contract and its selected Linux scope without reintroducing a presentation/runtime defect.

## Acceptance gate

Current evidence already satisfies artifact provenance, preflight and complete visual review. Remaining Step 7 gate:

1. temporary executor absent from the cleanup checkpoint;
2. synchronized operational documentation and machine state;
3. cleanup checkpoint Static contract green;
4. selected Linux integration scope green or classified if GitHub supersedes it through the cleanup push.

After that, Step 7 becomes ACCEPTED and Step 8 becomes active.

## Next gate — Step 8

Step 8 creates one immutable Scientific Article phase-end candidate and requires Static contract, **complete** Linux integration and article-specific evidence on the same SHA before Scientific Article may close.

Every **material advance** in this loop updates the operational documentation in the same work cycle. The phase still requires its own **phase-end regression**.
