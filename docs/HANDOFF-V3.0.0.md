# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main` at merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- PR #285 is **MERGED**; the accepted shared foundation and Scientific Article Step 1 are on `main`.
- Active integration branch: `ci/scoped-linux-integration`; PR #287 is open against `main`.
- Existing Scientific Article branch/PR #286 is preserved but **paused for control-plane advancement** until PR #287 lands and the branch is reconciled with updated `main`.
- Active phase: **Scientific Article**.
- Regression Audit: CLOSED.
- Core Corrections: CLOSED — `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Reference PDF Validation: CLOSED — `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798`; canonical 55/55 visual PASS.
- Librarian review: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.
- Scientific Article source contract: 18 rules in `docs/ARTICLE-NORMATIVE-CONTRACT.md` / `standards/coverage-rules-article.json`.
- Scientific Article Step 1 on merged `main`: ACCEPTED — implementation `b46ba2051f8c9c712a7b5d25748b81baa52b920a`; synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953`, `PASS=31 FAIL=0 SKIP=0`.
- Current material advance: **Scoped Linux integration — runner file-spec import correction**.
- PR #287 technical checkpoint `d089215e540b1e63bc8921cd5b4ab69497e8bc42` correctly selected `smoke`, but Static `34137588226` and Linux `34137588237` both failed the same import-boundary defect: `tests/run.py` could not resolve sibling `integration_suites` when loaded through `importlib.util.spec_from_file_location` by normative traceability.
- The failure is classified as orchestration/import-boundary only. It did not change LaTeX runtime, article semantics, normative predicates, reference-PDF presentation, or the librarian-review state.
- The current correction makes `tests/run.py` location-independent for sibling import resolution and adds an isolated Static file-spec import regression probe.
- Issue #18 remains an explicit v3.0.0 release blocker owned by Final Certification/Release.
- No temporary executor is active.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-SCIENTIFIC-ARTICLE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/V3-RELEASE-READINESS.md`, `docs/ARTICLE-NORMATIVE-CONTRACT.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and `docs/ENGINEERING-LANGUAGE.md`.

## Scientific Article progress

| Step | State | Evidence / boundary |
|---:|---|---|
| 1. Profile and metadata surface | **ACCEPTED ON MAIN** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI orchestration stabilization | **IMPORT FIX PENDING CI** | PR #287; rejected technical checkpoint `d089215e...`; Static `34137588226` + Linux `34137588237` classified as one import-boundary defect |
| 2–4 on PR #286 | **PRESERVED / PAUSED FOR RECONCILIATION** | existing feature history is not discarded; no further control-plane promotion until PR #287 merges and branch is reconciled |
| 5. Recommendations/conditional boundary | BLOCKED | resume only after reconciled Step 4 executable acceptance |
| 6. Evidence hardening | QUEUED | rule-specific positive/negative proof only |
| 7. Canonical article PDF | QUEUED | provenance-bound real PDF + complete visual review |
| 8. Phase-end regression | QUEUED | one immutable SHA; Static + `complete` Linux + article acceptance |

## Linux integration failure classification

| Surface | Observation | Classification |
|---|---|---|
| Automatic scope | synchronize range selected `smoke` | PASS — orchestration path worked |
| Static `34137588226` | `validator_source.py` reached normative traceability and failed importing `integration_suites` through file-spec loaded `tests/run.py` | IMPORT-BOUNDARY DEFECT |
| Linux `34137588237` | `smoke` ran; repository/reference/PDF validator passed; validator-source failed the same import | IMPORT-BOUNDARY DEFECT |
| Normative/runtime state | no rule, locator, tolerance, article requirement or LaTeX implementation failure | UNCHANGED |

The correction is intentionally narrow: `tests/run.py` adds its own `tests/` directory to `sys.path` before importing the sibling suite module, and `tests/checks/linux_integration_suites.py` now proves file-spec importability from an isolated interpreter.

## Immediate action

1. publish the synchronized runner import fix on PR #287;
2. require Static plus bounded `smoke` Linux on that exact technical checkpoint;
3. classify any failure before changing tests or scope semantics;
4. if green, record accepted checkpoint/run IDs in all control documents and PR #287;
5. merge PR #287;
6. reconcile the existing `feat/v3-scientific-article` / PR #286 with updated `main` rather than recreating or discarding its work;
7. obtain executable `article`-scope evidence for the pending Step 4 structural checker state;
8. continue Scientific Article from the reconciled accepted step;
9. retain `complete` Linux for Scientific Article phase-end regression.

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
