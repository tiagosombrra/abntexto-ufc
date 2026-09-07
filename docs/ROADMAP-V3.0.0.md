# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 4 — body-spacing correction implemented, acceptance rerun pending.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 4 CORRECTION CI PENDING** | Steps 1–3 accepted; rejected Step 4 checkpoint `8b52ee4...` exposed real body-spacing runtime defect; corrected synchronized checkpoint now awaits CI |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | **ACCEPTED** | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **CORRECTION IMPLEMENTED — CI PENDING** | `8b52ee4...`: Static `34058435312` PASS, Linux `34058435311` FAIL; body gap `20.700 pt` vs `13.800 pt` calibration; current checkpoint moves article override to `begindocument/end` |
| 5 | Recommendations and conditional applicability | BLOCKED | starts only after Step 4 acceptance is recorded |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + **complete Linux scope** + article-specific evidence on one immutable SHA |

## Step 4 failure and correction

The bounded Linux run `34058435311` passed four of five article checks and failed only `scientific-article-body`. The measured body spacing remained at the shared academic-work 1.5-spacing gap (`20.700 pt`) rather than the same-document single-spacing calibration (`13.800 pt`). This classifies the defect as runtime initialization order.

The correction keeps the existing article-only predicate and applies the body typography override at `begindocument/end`, after shared begin-document layout initialization. The checker and its expected single-spacing calibration are unchanged.

| Rule / property | Required | Current correction evidence target |
|---|---|---|
| `article.introduction.required` | introduction present | existing positive fixture |
| `article.development.required` | development present | positive fixture + missing-development negative fixture |
| `article.final-considerations.required` | final considerations present | existing structure checker |
| `article.references.required` | references present | shared bibliography route from article fixture |
| `article.body.typography` | 12 pt, justified, 2 cm indent, single spacing | physical final-PDF measurement under pdfLaTeX and LuaLaTeX; spacing must match `13.800 pt` calibration, not `20.700 pt` |

## Linux integration scopes

| Scope | Intended surface | Current main checks | Phase-transition authority |
|---|---|---|---|
| `article` | Scientific Article executable gates | validator-source + profile + front block + foreign elements + body | No |
| `profiles` | exactly six non-article profiles + compatibility | profile matrix/build path/multivolume/catalog card | No |
| bounded shared scopes | reference/frontmatter/layout/objects/bibliography/backmatter/research-project/smoke | domain-specific gates | No |
| `complete` | shared/core/unknown changes and phase-end regression | all PR gates + normative contribution | **Required at phase end** |

## Current acceptance gate

| Gate | Required before Step 5 |
|---|---|
| Static contract | corrected synchronized Step 4 checkpoint PASS |
| Bounded Linux | `article` scope PASS=5 FAIL=0 |
| Body typography | 12 pt / justified / 2 cm / single physically measured under both engines |
| Required structure | positive structure present and missing-development negative rejected |
| Shared boundary | correction remains scoped to `scientific-article` |
| Proof-state boundary | no retained article rule promoted merely because shared mechanisms are reused |

## Shared state

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Step 4 implementation commit: `e5291137d4753b7d776916ca0f08c67929dbb76b`.
- Rejected synchronized checkpoint: `8b52ee4b36b23868fecce9bbe9b843f689ccc01e`; Static `34058435312` success; Linux `34058435311` failure.
- Shared librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a Release blocker for deterministic reference-PDF reproduction.

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** updates the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase, acceptance, evidence, Linux-scope policy, current batch or branch/checkpoint facts update this roadmap and `release/v3-roadmap.json` when machine state is affected.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; Scientific Article Step 8 requires `complete` Linux.

## Gate before Final Certification

Scientific Article must complete Steps 4–7 and then pass Step 8 on one immutable SHA. The article canonical PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass on the final candidate and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.
