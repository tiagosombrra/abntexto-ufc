# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main` at merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- PR #285 is MERGED; shared foundation and Scientific Article Step 1 are on `main`.
- Active integration branch: `ci/scoped-linux-integration`; PR #287 is **accepted and ready to merge**.
- Accepted PR #287 technical checkpoint: `47ac2e27c5c2f6797269ccc4e1c07caafea1c643`; Static `34139608322` SUCCESS; Linux `34139608364` SUCCESS, `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`.
- The preceding checkpoint `d089215e...` is rejected/classified: Static `34137588226` and Linux `34137588237` failed the same runner file-spec import-boundary defect. The correction is now protected by Static `runner_file_spec_import=true`.
- Existing Scientific Article branch/PR #286 is preserved but paused for control-plane advancement until PR #287 merges and the branch is reconciled with updated `main`.
- Active phase: **Scientific Article**.
- Core Corrections: CLOSED — `5f67560a...`; Static `33982156041`; Linux `33982156042`.
- Reference PDF Validation: CLOSED — `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.
- Scientific Article Step 1 on merged foundation: ACCEPTED — `08b878a...`; Static `34001350884`; Linux `34001350953`.
- Issue #18 remains an explicit v3.0.0 release blocker.
- No temporary executor is active.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scoped Linux orchestration acceptance

| Requirement | Evidence | State |
|---|---|---|
| Incremental synchronize path | `d089...` and `47ac...` both selected `smoke` | PASS |
| Runner file-spec import | Static `34139608322` emitted `runner_file_spec_import=true` | PASS |
| Repository contract | Linux `34139608364` | PASS |
| Validator/source contract | Linux `34139608364` | PASS |
| Canonical reference build | Linux `34139608364` | PASS |
| PDF validator | Linux `34139608364` | PASS |
| Smoke summary | `SCOPE=smoke PASS=4 FAIL=0 SKIP=0` | PASS |
| Phase transition authority | scoped run is intermediate only; `complete` remains mandatory | PRESERVED |

No suite membership, normative predicate, article rule, authority source, LaTeX runtime or reference-PDF presentation was weakened.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | **ACCEPTED ON MAIN** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI orchestration stabilization | **ACCEPTED — MERGE NEXT** | `47ac2e27...`; Static `34139608322`; Linux `34139608364` |
| 2–4 on PR #286 | **PRESERVED / PAUSED FOR RECONCILIATION** | branch history retained; reconcile after #287 merge |
| 5. Recommendations/conditional boundary | BLOCKED | resume after reconciled Step 4 executable acceptance |
| 6. Evidence hardening | QUEUED | rule-specific proof only |
| 7. Canonical article PDF | QUEUED | provenance-bound real PDF + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + `complete` Linux + article acceptance |

## Immediate action

1. merge PR #287 after this documentation synchronization remains Static-clean;
2. reconcile existing PR #286 / `feat/v3-scientific-article` with updated `main`;
3. obtain executable `article`-scope evidence for the pending Step 4 structural-checker state;
4. synchronize accepted article step/proof state;
5. continue Scientific Article from the reconciled accepted state;
6. retain `complete` Linux for phase-end regression.

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
- CTAN submission remains blocked until Release.
