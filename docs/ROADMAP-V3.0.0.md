# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 3 — optional foreign elements; missing-before fail-closed scope fallback and synchronized acceptance are the current batch.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 3 ACCEPTANCE PENDING** | Steps 1–2 accepted; Step 3 executable evidence is green, but synchronized scoped acceptance remains open after orchestration robustness fixes |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | **IMPLEMENTED — SCOPE FALLBACK FIX / CI PENDING** | runtime `81e0832...`; migration `336bc982...`; runner fix `4068414...`; scope fallback `0a48d72...` |
| 4 | Textual structure and body typography | QUEUED | required article structure plus 12 pt/justified/2 cm/single-spaced body evidence |
| 5 | Recommendations and conditional applicability | QUEUED | recommendations stay advisory; journal instructions stay conditional |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + **complete Linux scope** + article-specific evidence on one immutable SHA |

## Step 3 evidence history

| Checkpoint / run | Result | Classification |
|---|---|---|
| `567a5b2...` / Linux `34028373060` | foreign-elements gate failed on first-pass rerun warnings | evidence convergence defect; runtime unaffected |
| `336bc982...` / Static `34030098936` | `validator-source` failed loading `tests/run.py` | runner sibling-import defect |
| `336bc982...` / Linux `34030098924` | scope `profiles,article`, PASS=7 FAIL=1; all article/profile checks green except `validator-source` | same runner sibling-import defect |
| `4f1c9a1...` / Static `34030827665` | **SUCCESS** | runner import fix confirmed |
| `4f1c9a1...` / Linux `34030827664` | failed in scope determination before integration: unavailable event `before` commit | scope-orchestration robustness defect |

Technical checkpoint `0a48d72c83b601c3ca8e0942f4c9b735ac5f0eb9` adds a fail-closed fallback: use incremental `before -> after` only when both commits exist locally; otherwise retain the full PR `base -> head` range. The static suite contract now protects this behavior. The same checkpoint strengthens profile-count/article-exclusion evidence and foreign-element final-pass warning evidence without changing runtime or normative rules.

## Linux integration scopes

| Scope | Intended surface | Phase-transition authority |
|---|---|---|
| `auto` | infer safe bounded scope; missing incremental provenance falls back to full PR diff | No |
| `article` | article source/profile/front-block/foreign-elements | No |
| `profiles` | exactly six non-article profiles + compatibility | No |
| `reference-document`, `reference-pdf` | canonical document/PDF | No |
| `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter` | bounded shared domains | No |
| `research-project` | research-project-specific work | No |
| `smoke` | integration-orchestration-only changes | No |
| `complete` | shared/core/unknown changes and phase-end regression | **Required at phase end** |

For a normal PR `synchronize`, `auto` uses the reachable incremental pushed range. If either endpoint is unavailable, it falls back to the full PR range rather than terminating. Multiple known domains run a deduplicated union. Unknown technical paths remain `complete`.

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

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, Linux integration scope policy, current batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; the phase-end Linux scope is `complete`.

## Gate before Final Certification

Scientific Article must complete Steps 3–7 and then pass Step 8 on one immutable SHA. The article canonical PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass on the final candidate and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
