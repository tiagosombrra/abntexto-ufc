# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-05

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`.
- Active task branch: `plan/v3-regression-reset`.
- Active phase: **Reference PDF Validation**.
- Core Corrections candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`: Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`.
- Librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Canonical PDF build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, run `33983729996`, artifact `9974546873`.
- PDF SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`; 55 pages; A4; PDF 1.7; TeX Live 2026/pdfLaTeX; unencrypted; fonts embedded.
- Artifact provenance/preflight: **PASS**.
- Complete 200 DPI page review: **PASS — 55/55 pages, 0 unexplained visual FAIL**.
- Visual review record: `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.
- Page 36 licensed-photo fallback boxes are intentional normal-build behavior when optional reference assets are absent.
- Stale 2026-09-04 PDF remains comparison-only.
- Temporary PDF-build workflow is absent.
- Current batch: **Reference PDF Validation — immutable phase-end regression candidate**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Scientific Article runtime remains deferred.

Canonical control documents: `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-REFERENCE-PDF-VALIDATION.md`, `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`, `docs/V3-CORRECTION-PLAN.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, `docs/V3-CORE-CORRECTIONS-PHASE-END.md`, `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`, `docs/V3-REGRESSION-AUDIT.md`, and `docs/ENGINEERING-LANGUAGE.md`.

Git facts, machine state, roadmap, active phase documents and this handoff must describe the same phase and acceptance state. Disagreement fails closed.

## Visual review result

All 55 pages were rendered at 200 DPI and inspected in order through grouped contact sheets, with targeted full-page inspection of front matter, TOC, dense main-text pages, figures/tables/code/algorithms/equations, references and appendices/annexes/index.

No clipping, overlap, replacement glyph, unexpected blank page, object overflow, unexplained heading drift or pagination anomaly was found. Presentation-sensitive review items 1, 2, 7, 10, 11, 15, 16, 21, 28 and 34 were visually reconfirmed without changing their normative classifications.

A comparison against the stale 2026-09-04 PDF is preservation evidence only: both PDFs have 55 pages; 28 pages were pixel-identical at 120 DPI and 27 changed in accepted correction/reference-content areas.

## Immediate action

1. freeze this synchronized visual-review-complete state as the Reference PDF Validation phase-end candidate;
2. wait for Static contract and full Linux integration on that exact immutable SHA;
3. classify any failure before changing implementation/tests;
4. if both pass, record the candidate SHA/run IDs and mark Reference PDF Validation `CLOSED`;
5. activate **Scientific Article** only in the subsequent synchronized phase-transition commit.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Phase/acceptance/evidence state, branch/checkpoint facts and artifact provenance must remain synchronized with the roadmap and machine state.

Every phase requires a **phase-end regression** on one immutable candidate before closure. Targeted checks and visual review never authorize a phase transition by themselves.

## Hard boundaries

- Do not start Scientific Article while Reference PDF Validation is open.
- Preserve the closed V3 public API unless current evidence explicitly authorizes a change.
- Do not translate reviewer comments directly into normative runtime behavior when current authority remains unresolved.
- Do not use stale or synthetic PDFs as canonical acceptance evidence.
- Do not weaken tests merely to recover green CI.
- Do not redistribute proprietary fonts.
- CTAN submission remains blocked until **Release**.
