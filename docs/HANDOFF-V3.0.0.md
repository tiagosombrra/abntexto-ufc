# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Reference PDF Validation**.
- Core Corrections immutable phase-end candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da` passed Static `33982156041` and full Linux `33982156042`; Linux summary `PASS=31 FAIL=0 SKIP=0`.
- Core Corrections is CLOSED.
- Current 34-item state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Phase-transition checkpoint: `a6bd8a7385162ca8a83c0d938ebec7a95538f88e`; Static `33983464772` passed; its full Linux run may be superseded by the dedicated artifact-build commit and is not the Core Corrections closure gate.
- Pre-existing 2026-09-04 canonical-looking PDF is rejected as current acceptance evidence because its rendered content predates accepted corrections.
- Current batch: **Reference PDF Validation — fresh provenance-bound canonical build**.
- Temporary executor: `.github/workflows/tmp-reference-pdf.yml`; lifecycle state `ACTIVE`, must be removed after artifact recovery/validation.
- Active phase contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap, active phase document and this handoff must describe the same active phase and acceptance state. Disagreement fails closed.

## Core Corrections closure

The corrected immutable candidate `5f67560a...` preserved `phase_end_regression.candidate = one-immutable-sha`, passed Static `33982156041`, and passed full Linux `33982156042`. The Linux run executed all 31 PR checks and ended with `PASS=31 FAIL=0 SKIP=0`.

The same run retained explicit evidence for the resolved librarian-review surfaces. No shared runtime FAIL remained. Item 33 stayed explicit and fail-closed.

## Reference PDF provenance finding

The local `abntexto-ufc-v3-template-example.pdf` generated on 2026-09-04 is real LaTeX output but is stale relative to the accepted shared foundation. Its extracted pages still show the old complete-author placeholder and title-page advisor presentation. It is therefore comparison-only.

A dedicated temporary GitHub Actions executor now rebuilds `template/main.tex` from the current branch with TeX Live 2026/pdfLaTeX and uploads the PDF together with Git SHA, workflow run, `pdfinfo` and SHA-256 provenance. The executor is temporary by policy and must be removed once the artifact is recovered.

## Immediate action

1. publish and execute the temporary canonical build;
2. recover the uploaded artifact and verify provenance;
3. remove the temporary workflow in the next synchronized repository checkpoint;
4. preflight and render every page at 200 DPI;
5. inspect the complete page sequence and record page-level results;
6. classify any defect before changing runtime/reference content;
7. rebuild/re-render after any correction;
8. prepare one immutable Reference PDF Validation phase-end candidate only after the visual checklist is clean;
9. do not start Scientific Article until that candidate passes Static/full Linux.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state, branch/checkpoint facts, artifact provenance and temporary-executor lifecycle must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks and visual spot checks never authorize a phase transition by themselves.

## Hard boundaries

- Do not start Scientific Article while Reference PDF Validation is open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not use stale or synthetic PDFs as canonical acceptance evidence.
- Do not leave the temporary PDF-build workflow in the repository after artifact recovery.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
