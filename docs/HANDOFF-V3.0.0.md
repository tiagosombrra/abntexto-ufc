# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation merge | `85cf22b6fe5d117bb2611a2865911e0d20a19363` |
| Active phase | **Scientific Article** |
| Steps 1–6 | **ACCEPTED** |
| Step 6 acceptance | `e941a7f9b4685a9bcf687135e8d5168af2d69ec7`; Static `34146793998`; Linux `34146794016` |
| Step 7 | **ACTIVE — CANONICAL ARTICLE PDF** |
| Step 8 | QUEUED — immutable complete phase-end regression |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Final Certification | QUEUED |
| Release | QUEUED |

Step 6 is accepted. Its exact 18-rule evidence map remained conservative, promoted zero validation modes, preserved recommendation rules as manual/non-enforcing, and preserved journal precedence as conditional-manual. No source-contract, locator, applicability or modality change was authorized by Step 6.

## Active work — Step 7

Step 7 must produce and accept a real canonical Scientific Article PDF from the current accepted branch state using TeX Live 2026. The artifact must be bound to Git provenance and inspected page by page.

Required Step 7 evidence:

1. dedicated canonical article source using the public V3 Scientific Article runtime;
2. real LaTeX build with recorded source SHA, workflow run, TeX Live version, engine, PDF metadata and SHA-256;
3. complete page-level visual review covering article front block, optional foreign elements, typography, textual structure, citations/references, footnotes and absence of academic-work front-matter leakage;
4. classification of any defect before runtime/test changes;
5. temporary build executor removed before acceptance;
6. synchronized documentation after artifact/visual acceptance.

Synthetic or stale PDFs do not satisfy Step 7.

## Immediate action

1. establish the Step 7 canonical article source and provenance-build path;
2. generate the real TeX Live 2026 artifact and recover it;
3. remove any temporary executor immediately after artifact recovery;
4. preflight, render and inspect every page;
5. record the visual/provenance result and accept Step 7 only if clean;
6. create one immutable Step 8 candidate for Static + **complete** Linux plus article-specific gates;
7. close Scientific Article and activate Final Certification only after Step 8 succeeds.

## What still blocks V3 completion

| Blocker | State |
|---|---|
| Scientific Article Step 7 canonical PDF | ACTIVE |
| Scientific Article Step 8 phase-end regression | QUEUED |
| PR #286 / issue #280 | remain open until Scientific Article acceptance |
| Final Certification | not executed on final candidate |
| Issue #18 deterministic release-reference-PDF reproducibility | open release blocker |
| Release packaging/tag/assets/publication | not executed |
| Librarian item 33 | explicit `NORMATIVE-REVIEW`, fail-closed |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete phase-end regression on one immutable SHA. Scoped intermediate checks never authorize a phase transition.
