# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-06

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset` until PR #285 merges the accepted foundation, Scientific Article Step 1 and the scoped Linux orchestration update.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation candidate `b64074c64941895f97fbe0f795ce826c798d17ce`: Static `33985595790`, Linux `33985595798`, both SUCCESS.
- Canonical reference PDF: build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, artifact `9974546873`, SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`, 55/55 visual PASS.
- Librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article source contract: 18 rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Step 1 synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`: Static `34001350884` SUCCESS; Linux `34001350953` SUCCESS; `PASS=31 FAIL=0 SKIP=0`.
- Step 1 state: **ACCEPTED**.
- Current infrastructure batch: **Scoped Linux integration orchestration**, documented in `docs/LINUX-INTEGRATION-SCOPES.md`.
- Issue #18 remains an explicit v3 release blocker owned by Final Certification/Release.
- No temporary executor is active.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI orchestration optimization | **IMPLEMENTING** | named Linux scopes; Static + scoped Linux acceptance pending |
| 2. Required article front block | NEXT | start on fresh article branch after PR #285 lands |
| 3. Optional foreign elements | QUEUED | foreign title/summary optionality must remain non-mandatory |
| 4. Textual structure/body typography | QUEUED | reuse shared citation/reference/section/object machinery |
| 5. Recommendations/conditional boundary | QUEUED | recommendations advisory; journal instructions conditional |
| 6. Evidence hardening | QUEUED | rule-specific positive/negative proof only |
| 7. Canonical article PDF | QUEUED | real Git-bound TeX Live 2026 artifact + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + `complete` Linux + article acceptance |

## Linux integration scope model

| Scope class | Use | Authority |
|---|---|---|
| `auto` | PR changed-path inference; synchronize events use only the incremental push window | intermediate |
| bounded scopes | `article`, `reference-document`, `reference-pdf`, `frontmatter`, `layout`, `objects`, `bibliography`, `backmatter`, `research-project`, `profiles`, `smoke` | intermediate only |
| `complete` | shared/unknown technical changes and explicit full regression | **required for phase-end regression** |

Unknown technical paths and shared/core/standards changes fail closed to `complete`. Documentation-only changes skip heavy Linux. Manual workflow dispatch exposes the named scopes; manual `auto` resolves to `complete`.

The active `article` suite must contain `scientific-article-profile` plus `validator-source`. As new article executable gates are added, the suite must be expanded in the same material-advance cycle.

## Repository and branch readiness

| Surface | State | Action |
|---|---|---|
| PR #285 | integration boundary extended by scoped Linux orchestration | validate Static + bounded Linux; then merge if still green/mergeable |
| `main` | stale until PR #285 lands | do not start Step 2 from current `main` |
| current branch | transition branch | finish orchestration acceptance only; no Step 2 feature runtime |
| post-merge branch | planned `feat/v3-scientific-article` | create from updated `main` and continue Step 2 |
| historical branches | provenance only | not active authority |

## Immediate action

1. validate the scoped Linux orchestration contract with Static;
2. require the PR synchronize run to choose the bounded `smoke` scope for the orchestration-only push rather than the full historic PR diff;
3. if green, record the orchestration checkpoint and run IDs in the documentation/machine state;
4. merge PR #285 once the synchronized boundary remains green and mergeable;
5. create `feat/v3-scientific-article` from updated `main`;
6. begin **Required article front block** using `article` scoped Linux during intermediate work;
7. retain `complete` Linux for the Scientific Article phase-end regression.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, article-rule evidence, integration-scope policy, proof state, branch/checkpoint facts, release blockers and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Scoped/targeted checks never authorize a phase transition by themselves; the phase-end Linux scope is `complete`.

## Hard boundaries

- Preserve the accepted non-article foundation and reference PDF presentation.
- Do not change the 18-rule article authority/modality contract without new current source evidence.
- Do not promote recommendations into required failures.
- Do not fork shared citation, reference, section, summary or object infrastructure.
- Do not weaken tests merely to recover green CI.
- Item 33 remains fail-closed.
- Resolve issue #18 before v3.0.0 publication.
- CTAN submission remains blocked until **Release**.
