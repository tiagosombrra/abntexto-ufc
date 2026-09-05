# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Reference PDF Validation**.
- Core Corrections immutable phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da` passed Static `33982156041` and full Linux `33982156042`; Linux summary `PASS=31 FAIL=0 SKIP=0`.
- Core Corrections is therefore CLOSED.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Current batch: **Reference PDF Validation — canonical artifact provenance and page-level review**.
- Active phase contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap, active phase document and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Core Corrections closure

The corrected immutable candidate `5f67560a...` preserved `phase_end_regression.candidate = one-immutable-sha`, passed Static `33982156041`, and passed full Linux `33982156042`. The Linux run executed all 31 PR checks and ended with `PASS=31 FAIL=0 SKIP=0`.

The same run retained explicit evidence for librarian-review items 1, 2, 7, 11, 16, 19, 20, 23, 28, 30, 31, 32 and 34, plus the accepted object, front-matter, back-matter, typography and reference contracts. No shared runtime FAIL remained. Item 33 stayed explicit and fail-closed.

Rejected candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2` and Static `33981960024` remain historical evidence of the governance sentinel check; they do not affect the accepted closure.

## Reference PDF Validation entry

The next obligation is presentation acceptance of the corrected canonical V3 reference PDF. The phase must use a real LaTeX build tied to a concrete Git SHA; older or synthetic PDFs are comparison-only unless provenance proves they still represent the accepted candidate.

Required work:

1. establish the canonical artifact provenance;
2. preflight the PDF;
3. render every page at 200 DPI;
4. inspect the complete page sequence for visual defects and presentation-sensitive requirements;
5. record page-level PASS/FAIL evidence in `docs/V3-REFERENCE-PDF-VALIDATION.md`;
6. rebuild/re-render after any correction;
7. prepare one immutable Reference PDF Validation phase-end candidate;
8. activate Scientific Article only after that candidate passes Static/full Linux and the visual checklist is accepted.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state, branch/checkpoint facts and artifact provenance must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks and visual spot checks never authorize a phase transition by themselves.

## Hard boundaries

- Do not start Scientific Article while Reference PDF Validation is open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not use stale or synthetic PDFs as canonical acceptance evidence.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
