# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 3 — Optional foreign elements.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0` |
| Reference PDF Validation | CLOSED | `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798`; canonical academic-work PDF 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 3** | Steps 1–2 accepted; Steps 3–8 remain; phase closes only after canonical article PDF and one-SHA phase-end regression |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0`; profile/front-block evidence PASS on both engines |
| 3 | Optional foreign title and summary | **ACTIVE** | independent present/absent behavior under pdfLaTeX and LuaLaTeX; no modality drift; no `title-variant` repurposing |
| 4 | Textual structure and body typography | QUEUED | required structure plus 12 pt/justified/2 cm/single-spaced body evidence |
| 5 | Recommendations and conditional applicability | QUEUED | recommendations remain advisory; journal instructions remain conditional |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific evidence on one immutable SHA |

Step 2 acceptance does **not** alter the 18-rule proof state: the article rule contract remains manual/conditional-manual until Step 6 explicitly promotes evidence.

## Step 3 acceptance boundary

The Step 3 implementation must keep `article.title.foreign.optional` and `article.summary.foreign.optional` independently optional. Both may be absent, either may appear alone, or both may appear. Absence is never a failure. The article surface must be explicit and must not infer foreign-title semantics from shared `title-variant` metadata. Presentation defaults used for rendering must not be misrepresented as new normative typography requirements.

## Shared state

- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Shared librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a Release blocker for deterministic reference-PDF reproduction.

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted Step checks accumulated during a phase do not replace this gate.

## Gate before Final Certification

Scientific Article must complete Steps 3–7 and then pass Step 8 on one immutable SHA. The article canonical PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass on the final candidate and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
