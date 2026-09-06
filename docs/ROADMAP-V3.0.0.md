# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE at Step 3 — optional foreign elements; evidence correction and scoped Linux integration are the current acceptance batch.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 3 ACCEPTANCE PENDING** | Steps 1–2 accepted; Step 3 runtime implemented; bounded evidence correction + scoped Linux migration under validation |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | **IMPLEMENTED — EVIDENCE FIX / CI PENDING** | `81e0832...`; synchronized run `34028373060` classified as one-pass evidence-orchestration failure |
| 4 | Textual structure and body typography | QUEUED | required article structure plus 12 pt/justified/2 cm/single-spaced body evidence |
| 5 | Recommendations and conditional applicability | QUEUED | recommendations stay advisory; journal instructions stay conditional |
| 6 | Evidence hardening | QUEUED | article-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + **complete Linux scope** + article-specific evidence on one immutable SHA |

## Step 3 failure classification

Linux `34028373060` on synchronized head `567a5b2d21a16b653d7704639bdd5012d7c2f99b` ran the former complete integration path. All preceding shared checks passed; the six accepted non-article profiles also completed under both engines. The failure appeared only when the profile matrix recursively entered the article gate and the first foreign-elements scenario inspected expected first-pass Biber/cross-reference rerun warnings after one LaTeX pass.

The correction is limited to test/orchestration behavior: use two LaTeX passes before warning inspection, expose article gates directly in the coordinated runner, and separate article validation from the non-article profile matrix. No article runtime or normative rule changes.

## Linux integration scopes

| Scope | Intended surface | Phase-transition authority |
|---|---|---|
| `auto` | infer safe bounded scope from changed paths | No |
| `article` | article source/profile/front-block/foreign-elements | No |
| `profiles` | six non-article profiles + profile compatibility | No |
| `reference-document`, `reference-pdf` | canonical document/PDF | No |
| `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter` | bounded shared domains | No |
| `research-project` | research-project-specific work | No |
| `smoke` | integration-orchestration-only changes | No |
| `complete` | shared/core/unknown changes and phase-end regression | **Required at phase end** |

For PR `synchronize`, `auto` uses the incremental push diff (`before` → `after`) rather than the entire accumulated PR diff. Opened/reopened/ready events use the full PR diff. Documentation-only changes skip heavy Linux. Unknown technical paths and shared/core/standards/integration infrastructure fail closed to `complete`.

Multiple known domains run a deduplicated union. The current migration modifies both non-article profile orchestration and article evidence, so the expected first bounded run is `profiles,article`.

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
