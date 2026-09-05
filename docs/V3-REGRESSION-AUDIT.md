# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work.

Evidence at closeout:

- the two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`;
- `docs/V3-CORRECTION-PLAN.md` contains the executable correction queue;
- the active roadmap uses readable phase names;
- object typography and selected NBR 6023:2025 disputes had explicit unresolved authority status at audit closeout;
- Static contract `33937439818` passed;
- full Linux integration `33937439846` passed;
- scientific-article runtime had not started before the regression reset.

The project therefore advanced to **Core Corrections**. This closeout does not mean the 34 review items were already corrected.

## Findings transferred to Core Corrections

Unambiguous defects included title-page advisor/co-advisor punctuation, incomplete optional-department/full-name guidance, incomplete committee acronym examples, missing annex source demonstration, stale V2-era wording, retired public API vocabulary, and stale reference paths in the canonical V3 guide.

At audit closeout, object-title size was intentionally unresolved because existing tests certified reduced-size upper object titles while the recovered reviews requested body-size titles and the institutional guide distinguished upper identification/title from lower source/legend/note elements. The audit therefore correctly blocked runtime changes until authority was reconciled.

Selected DOI, online-availability, repeated-author, and corporate-author cases also remained under current-edition NBR 6023:2025 review rather than being copied mechanically from the older reviewed template.

Code/algorithm typography already had strong implementation evidence: the configured text family was shared across body, code and algorithms, and the typography fixture checked nominal 12 pt across supported family/engine combinations. The audit also found Portuguese project-owned diagnostics that the engineering-language gate did not detect; that coverage defect was transferred to Core Corrections.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit baseline counts and remain historical closeout facts.

## Post-audit disposition in Core Corrections

The object-title authority conflict is resolved and accepted. `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md` records the 12 pt upper identification/title and reduced 10 pt lower source/legend/note split where applicable.

The implementation exposed two independent residuals during regression: the `tabularray-abnt` adapter still forcing table captions to 10 pt, then a legacy IBGE observer still expecting that retired value. Both were corrected. Synchronized checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` subsequently passed Static `33965794475` and full Linux `33965794519` with `PASS=31 FAIL=0 SKIP=0`. Review item 21 is therefore closed as PASS.

The active post-audit batch now targets canonical reviewed reference content. Implementation checkpoint `c464a1bc2ca04a4ce398878f25e9521f5840d48e` adds source-level regressions for items 11, 16 and 28. These remain PARTIAL until synchronized branch acceptance and generated-PDF evidence are green.

Current review state in Core Corrections: **25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed.

Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
