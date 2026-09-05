# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Core Corrections**.
- Regression baseline: `c4bf51b574647226ee488440579ec2a204c16c79`; Static `33937439818` and Linux `33937439846` succeeded.
- Object/Core checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0`: Static `33965794475` and Linux `33965794519` succeeded, `PASS=31 FAIL=0 SKIP=0`.
- Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` and Linux `33969505614` succeeded, `PASS=31 FAIL=0 SKIP=0`; librarian items 11, 16 and 28 closed.
- Engineering-language hardening checkpoint `edeb14b7a96d1cab3ad9551701087ddf4dff059a`: Static `33972111694` and Linux `33972111696` succeeded; permanent detector reports zero project-owned Portuguese technical diagnostics.
- Reference evidence checkpoint `bcd851b3176b516091a254bc57b5ae4e8add9358`: Static `33974062993` and Linux `33974063103` succeeded, `PASS=31 FAIL=0 SKIP=0`; reviewer-specific items 30, 31 and 32 evidence passed and item 32 closed.
- Current 34-item state: `29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Current bounded batch: **Core Corrections — Front Matter and Annex Closeout**.
- Current implementation: `33bdd0bd5f9360c645b4166071c32dbba6c647f0`; evidence for items 1, 2, 7 and 34 is implemented but acceptance is pending synchronized Static/full Linux.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Current front-matter and annex implementation

Implementation `33bdd0bd...` is evidence-only unless CI exposes a real implementation defect:

1. item 1 — `frontmatter-cover-evidence.sh` now compiles a blank-department academic cover and a generated filled-department variant; blank must omit the marker and filled must render it;
2. item 2 — the canonical reference PDF must render `NOME COMPLETO DO AUTOR` in pre-textual output;
3. item 7 — the approval-page fixture uses `Instituição Externa de Teste (IET)` and the generated doctoral approval page must preserve the institution/acronym presentation;
4. item 34 — the canonical reference gate requires annex heading/source attribution in generated PDF and annex entry in generated TOC, while the existing independent appendix/annex final-PDF gate continues to prove bold/uppercase/12 pt/centered heading behavior.

## Immediate action

1. publish a synchronized documentation checkpoint on top of `33bdd0bd...`;
2. run Static contract and full Linux integration on that exact checkpoint;
3. require explicit `LIBRARIAN-REVIEW-EVIDENCE` PASS lines for items 1, 2, 7 and 34;
4. classify any failure before changing runtime; do not weaken the evidence;
5. if both gates pass, promote the 34-item matrix to `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` and synchronize all control documents;
6. prepare a **separate immutable Core Corrections phase-end regression candidate** and run the complete phase regression;
7. activate Reference PDF Validation only after that phase-end regression is green and recorded;
8. keep item 33 untouched/fail-closed.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state and branch/checkpoint facts must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks never authorize a phase transition by themselves.

## Hard boundaries

- Do not resume Scientific Article while Core Corrections or Reference PDF Validation are open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
