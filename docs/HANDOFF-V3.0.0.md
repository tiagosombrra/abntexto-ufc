# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main` at merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- PR #285 is **MERGED**; the accepted shared foundation and Scientific Article Step 1 are on `main`.
- Active task branch: `ci/scoped-linux-integration`, created from current `main` for bounded Linux orchestration only.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections: CLOSED — `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation: CLOSED — `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798`; canonical 55/55 visual PASS.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.
- Scientific Article source contract: 18 rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Scientific Article Step 1: ACCEPTED — implementation `b46ba2051f8c9c712a7b5d25748b81baa52b920a`; synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953`, `PASS=31 FAIL=0 SKIP=0`.
- Current material advance: **Scoped Linux integration orchestration**. Step 2 runtime is intentionally blocked on this infrastructure branch.
- Issue #18 remains an explicit v3.0.0 release blocker owned by Final Certification/Release.
- No temporary executor is active.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI orchestration stabilization | **DOCUMENTED / IMPLEMENTATION NEXT** | active branch `ci/scoped-linux-integration`; bounded suite contract in `docs/LINUX-INTEGRATION-SCOPES.md` |
| 2. Required article front block | NEXT AFTER ORCHESTRATION MERGE | start only on fresh `feat/v3-scientific-article` from updated `main` |
| 3. Optional foreign elements | QUEUED | foreign title/summary remain optional |
| 4. Textual structure/body typography | QUEUED | article-specific executable evidence required |
| 5. Recommendations/conditional boundary | QUEUED | recommendations advisory; journal instructions conditional |
| 6. Evidence hardening | QUEUED | rule-specific positive/negative proof only |
| 7. Canonical article PDF | QUEUED | provenance-bound real PDF + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + `complete` Linux + article acceptance |

## Linux integration scope model

| Scope class | Use | Transition authority |
|---|---|---|
| `auto` | infer narrowest safe suite from changed paths | No |
| bounded scopes | intermediate domain-specific validation | No |
| `complete` | shared/unknown technical work and phase-end regression | **Yes — required for phase closeout** |

Documentation-only changes skip heavy Linux. Unknown technical paths and shared/core/standards changes fail closed to `complete`. Manual `auto` also resolves to `complete`. The active `article` suite must include executable article evidence plus the source/validator contract.

## Repository and branch readiness

| Surface | State | Action |
|---|---|---|
| `main` | current through PR #285 | orchestration PR will target this branch |
| `ci/scoped-linux-integration` | active infrastructure branch | land only scoped Linux orchestration + synchronized docs |
| `plan/v3-regression-reset` | historical provenance | do not continue work there |
| `feat/v3-scientific-article` | next feature branch | create from updated `main` immediately after orchestration merges |

## Immediate action

1. open the scoped-orchestration PR from `ci/scoped-linux-integration` to `main` with documentation-only state first;
2. land the technical orchestration implementation on that PR;
3. require Static plus bounded Linux selection/evidence; classify any failure before changing tests;
4. record the accepted orchestration checkpoint and run IDs in all control documents;
5. merge the orchestration PR;
6. create `feat/v3-scientific-article` from updated `main`;
7. synchronize branch facts and begin **Required article front block**;
8. retain `complete` Linux for Scientific Article phase-end regression.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase, acceptance, article-rule evidence, integration-scope policy, proof state, branch/checkpoint facts, release blockers and temporary-executor lifecycle must remain synchronized with roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Scoped/targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Preserve the accepted non-article foundation and reference PDF presentation.
- Do not change the 18-rule article authority/modality contract without new current source evidence.
- Do not promote recommendations into required failures.
- Do not fork shared citation, reference, section, summary or object infrastructure.
- Do not weaken tests merely to recover green CI.
- Item 33 remains fail-closed.
- Resolve issue #18 before v3.0.0 publication.
- CTAN submission remains blocked until **Release**.
