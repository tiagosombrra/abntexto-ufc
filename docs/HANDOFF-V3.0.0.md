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
| Step 7 | **ACTIVE — PROVENANCE BUILD** |
| Canonical article source | `template/scientific-article.tex` |
| Temporary executor | `.github/workflows/tmp-scientific-article-pdf.yml` — ACTIVE |
| Step 7 record | `docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md` |
| Step 8 | QUEUED — immutable complete phase-end regression |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Final Certification | QUEUED |
| Release | QUEUED |

Step 6 is accepted. Its exact 18-rule evidence map remained conservative, promoted zero validation modes, preserved recommendation rules as manual/non-enforcing, and preserved journal precedence as conditional-manual.

## Active work — Step 7 provenance build

A dedicated canonical article source and temporary GitHub Actions executor are active solely to produce the provenance-bound PDF. The executor must be removed immediately after the artifact is recovered.

Required Step 7 sequence:

1. publish the synchronized canonical source + temporary executor;
2. recover the real TeX Live 2026 artifact and record source SHA/run/artifact metadata;
3. remove the temporary executor in the next synchronized checkpoint;
4. preflight the PDF, render every page at 200 DPI and inspect the complete page sequence;
5. classify any defect before code/test changes;
6. update `docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md` and all control documents with the result;
7. accept Step 7 only when the visual checklist is clean and the temporary executor is absent;
8. create one immutable Step 8 candidate for Static + **complete** Linux plus article gates.

Synthetic or stale PDFs do not satisfy Step 7.

## What still blocks V3 completion

| Blocker | State |
|---|---|
| Scientific Article Step 7 canonical PDF | ACTIVE |
| Temporary Step 7 executor | ACTIVE — must be removed after artifact recovery |
| Scientific Article Step 8 phase-end regression | QUEUED |
| PR #286 / issue #280 | remain open until Scientific Article acceptance |
| Final Certification | not executed on final candidate |
| Issue #18 deterministic release-reference-PDF reproducibility | open release blocker |
| Release packaging/tag/assets/publication | not executed |
| Librarian item 33 | explicit `NORMATIVE-REVIEW`, fail-closed |

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete phase-end regression on one immutable SHA. Scoped intermediate checks never authorize a phase transition.
