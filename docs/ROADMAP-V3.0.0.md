# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 4 — implementation complete, acceptance pending.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 4 CI PENDING** | Steps 1–3 accepted; Step 4 implementation `e5291137...` now owns article structure/body evidence |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | **ACCEPTED** | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **IMPLEMENTED — CI PENDING** | `e5291137...`; synchronized checkpoint must pass Static + bounded article Linux |
| 5 | Recommendations and conditional applicability | QUEUED | recommendations stay advisory; journal instructions stay conditional |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + **complete Linux scope** + article-specific evidence on one immutable SHA |

## Step 4 implemented scope

| Rule | Requirement | Step 4 evidence |
|---|---|---|
| `article.introduction.required` | introduction present | article-specific positive fixture and structure checker |
| `article.development.required` | development present | positive fixture plus missing-development negative fixture |
| `article.final-considerations.required` | final considerations present | article-specific structure checker |
| `article.references.required` | references present | shared bibliography route exercised from article fixture |
| `article.body.typography` | 12 pt, justified, 2 cm first-line indent, single spacing | article-specific physical final-PDF measurements under both engines |

The runtime change is intentionally narrow: shared academic-work layout still uses its accepted body behavior, while `scientific-article` applies a profile-scoped begin-document body contract. No new article alias or parallel bibliography/section implementation was created.

The previous Step 2/3 tests no longer prohibit all article `\AtBeginDocument` use. They now require the accepted Step 4 body activation to exist and remain explicitly scoped to `scientific-article`, preserving the original isolation intent without freezing a pre-Step4 implementation boundary.

## Linux integration scopes

| Scope | Intended surface | Current main checks | Phase-transition authority |
|---|---|---|---|
| `auto` | infer safe bounded scope; missing incremental provenance falls back to full PR diff | inferred union | No |
| `article` | Scientific Article executable gates | validator-source + profile + front block + foreign elements + **body** | No |
| `profiles` | exactly six non-article profiles + compatibility | profile matrix/build path/multivolume/catalog card | No |
| `reference-document`, `reference-pdf` | canonical document/PDF | bounded reference gates | No |
| `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter` | bounded shared domains | domain-specific gates | No |
| `research-project` | research-project-specific work | research-project gate | No |
| `smoke` | integration-orchestration-only changes | repository/source/reference/PDF-validator smoke | No |
| `complete` | shared/core/unknown changes and phase-end regression | all PR gates + normative contribution | **Required at phase end** |

`scientific-article-body` was added to the `article` suite in the same implementation advance that created it. `tests/checks/linux_integration_suites.py` now fails if the Scientific Article phase loses that executable gate.

Detailed contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

## Current acceptance gate

| Gate | Required before Step 5 |
|---|---|
| Static contract | synchronized Step 4 checkpoint PASS |
| Bounded Linux | `article` scope PASS |
| Body typography | 12 pt / justified / 2 cm / single physically measured on article PDF under pdfLaTeX + LuaLaTeX |
| Required structure | positive structure present and missing-development negative rejected |
| Shared boundary | six non-article profiles remain isolated; no shared-foundation behavior intentionally changed |
| Proof-state boundary | no retained article rule promoted simply because Step 4 reused shared mechanisms |

Step 5 cannot start until these results are recorded in the next documentation cycle.

## Shared state

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Step 4 implementation commit: `e5291137d4753b7d776916ca0f08c67929dbb76b`.
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

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
