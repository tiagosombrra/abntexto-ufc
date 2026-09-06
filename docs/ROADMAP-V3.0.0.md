# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 4 — textual structure and body typography.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 4** | Steps 1–3 accepted; Step 4 now owns required textual structure/body typography |
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

## Step 3 accepted evidence

Step 3 was accepted at synchronized checkpoint `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`. Static `34031144114` and Linux `34031144269` both completed successfully. This closes the earlier evidence-convergence, runner-import and unavailable-`before` scope-orchestration defects without changing article authority, modality or proof state.

The accepted workflow behavior is fail-closed: when incremental synchronize endpoints are unavailable, `auto` falls back to the authoritative full PR range rather than terminating. The article/profile acceptance also preserves exactly six non-article profiles as the compatibility matrix and keeps `scientific-article` separate.

## Step 4 scope

Step 4 owns these retained article rules:

| Rule | Requirement |
|---|---|
| `article.introduction.required` | introduction present |
| `article.development.required` | development present |
| `article.final-considerations.required` | final considerations present |
| `article.references.required` | references present |
| `article.body.typography` | 12 pt, justified, 2 cm first-line indent, single spacing |

Step 4 must reuse shared section/reference mechanisms where compatible, add article-specific executable evidence, include a controlled negative path where safely machine-detectable, and register its executable gate in the `article` Linux scope in the same material advance. Shared mechanisms alone do not prove article conformance.

## README ownership

The repository README is a user guide, not a roadmap transcript. It must prioritize stable-release selection, Overleaf/local installation, document configuration, compilation, content layout and common usage problems. Detailed SHAs, CI runs, issue history, regression failures and normative/control-plane state remain in this roadmap, handoff, phase documents and GitHub.

Until v3.0.0 is released, normal users are directed to stable v2.1.0; unreleased v3 capabilities are identified only as development state.

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

As Step 4 introduces a new executable article gate, that gate must be added to `article` in the same synchronized checkpoint. Multiple known domains run a deduplicated union. Unknown technical paths remain `complete`.

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
