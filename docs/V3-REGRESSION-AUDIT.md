# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-04
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work.

Evidence at closeout:

- the two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`;
- `docs/V3-CORRECTION-PLAN.md` contains the executable correction queue;
- the active roadmap uses readable phase names;
- object typography and selected NBR 6023:2025 disputes have explicit unresolved authority status;
- Static contract run `33937439818` passed;
- full Linux integration run `33937439846` passed;
- scientific-article runtime had not started before the regression reset.

The project therefore advances to **Core Corrections**. This closeout does not mean the 34 review items are already corrected.

## Findings transferred to Core Corrections

Unambiguous defects include title-page advisor/co-advisor punctuation, incomplete optional-department/full-name guidance, incomplete committee acronym examples, missing annex source demonstration, stale V2-era wording, retired public API vocabulary, and stale reference paths in the canonical V3 guide.

The object-title size conflict remains a normative review item. Existing tests certify reduced-size upper object titles, while the recovered review requests body-size titles and the institutional guide distinguishes upper identification/title from lower source/legend/note elements. Runtime must not change until that authority conflict is reconciled.

Selected DOI, online-availability, repeated-author, and corporate-author cases also remain under current-edition NBR 6023:2025 review rather than being copied mechanically from the older reviewed template.

Code/algorithm typography already has strong implementation evidence: the configured text family is shared across body, code and algorithms, and the existing typography fixture checks nominal 12 pt across supported family/engine combinations. The remaining task is evidence classification and engineering-language cleanup.

The audit also found Portuguese project-owned diagnostics in `tests/integration/code-typography.sh` that the engineering-language gate did not detect. This is a coverage defect transferred to Core Corrections.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit baseline counts. Update them only after the corresponding correction evidence passes.

Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
