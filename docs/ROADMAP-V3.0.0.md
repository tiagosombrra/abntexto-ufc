# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 4 — textual structure and body typography.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 4** | Steps 1–3 accepted; README user guide accepted; Step 4 owns required textual structure/body typography |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | **ACCEPTED** | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **ACTIVE** | required structure plus 12 pt/justified/2 cm/single-spaced article body evidence |
| 5 | Recommendations and conditional applicability | QUEUED | recommendations stay advisory; journal instructions stay conditional |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + **complete Linux scope** + article-specific evidence on one immutable SHA |

## README usability state

The root README is now intentionally user-facing. It prioritizes stable-release selection, Overleaf/local setup, document configuration, compilation, content organization and common problems. Detailed implementation history remains in engineering documents and GitHub.

| Checkpoint | Static | Linux | State |
|---|---|---|---|
| `3e3ece5...` first rewrite | `34053874788` FAIL — unclassified retired class identity | `34053874750` SUCCESS | rejected |
| `a99f1e19...` corrected README | `34054110778` SUCCESS | `34054110738` SUCCESS | **ACCEPTED** |

The canonical-identity checker was not weakened. Until v3.0.0 is released, the README directs normal users to stable v2.1.0 and does not present the article profile as released functionality.

## Step 4 scope

The shared academic-work layout uses 12 pt, 2 cm first-line indentation and 1.5 line spacing. The article contract instead requires single line spacing. Therefore Step 4 requires a profile-specific body activation rather than assuming the shared layout satisfies the article.

| Rule | Requirement |
|---|---|
| `article.introduction.required` | introduction present |
| `article.development.required` | development present |
| `article.final-considerations.required` | final considerations present |
| `article.references.required` | references present |
| `article.body.typography` | 12 pt, justified, 2 cm first-line indent, single spacing |

Step 4 must add article-specific physical PDF evidence and a bounded executable gate. Shared mechanisms alone do not prove article conformance. The new executable gate must be registered in the `article` Linux suite in the same material advance.

## Linux integration scopes

| Scope | Intended surface | Phase-transition authority |
|---|---|---|
| `auto` | infer safe bounded scope; missing incremental provenance falls back to full PR diff | No |
| `article` | current article executable gates | No |
| `profiles` | exactly six non-article profiles + compatibility | No |
| `reference-document`, `reference-pdf` | canonical document/PDF | No |
| `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter` | bounded shared domains | No |
| `research-project` | research-project-specific work | No |
| `smoke` | integration-orchestration-only changes | No |
| `complete` | shared/core/unknown changes and phase-end regression | **Required at phase end** |

Detailed contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

## Shared state

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Shared librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a Release blocker for deterministic reference-PDF reproduction.

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, Linux integration scope policy, current batch, README ownership policy or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json` when machine state is affected.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; the phase-end Linux scope is `complete`.

## Gate before Final Certification

Scientific Article must complete Steps 4–7 and then pass Step 8 on one immutable SHA. The article canonical PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass on the final candidate and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
