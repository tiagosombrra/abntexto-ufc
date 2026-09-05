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
- Static contract run `33937439818` passed;
- full Linux integration run `33937439846` passed;
- scientific-article runtime had not started before the regression reset.

The project therefore advanced to **Core Corrections**. This closeout does not mean the 34 review items were already corrected.

## Findings transferred to Core Corrections

Unambiguous defects included title-page advisor/co-advisor punctuation, incomplete optional-department/full-name guidance, incomplete committee acronym examples, missing annex source demonstration, stale V2-era wording, retired public API vocabulary, and stale reference paths in the canonical V3 guide.

At audit closeout, object-title size was intentionally unresolved because existing tests certified reduced-size upper object titles while the recovered reviews requested body-size titles and the institutional guide distinguished upper identification/title from lower source/legend/note elements. The audit therefore correctly blocked runtime changes until authority was reconciled.

Selected DOI, online-availability, repeated-author, and corporate-author cases also remained under current-edition NBR 6023:2025 review rather than being copied mechanically from the older reviewed template.

Code/algorithm typography already had strong implementation evidence: the configured text family was shared across body, code and algorithms, and the existing typography fixture checked nominal 12 pt across supported family/engine combinations. The remaining task was evidence classification and engineering-language cleanup.

The audit also found Portuguese project-owned diagnostics in `tests/integration/code-typography.sh` that the engineering-language gate did not detect. This coverage defect was transferred to Core Corrections.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit baseline counts and are retained as historical closeout facts rather than rewritten to match later Core Corrections progress.

## Post-audit disposition in Core Corrections

The object-title authority conflict has since been resolved and implemented. `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md` records the accepted split: 12 pt upper identification/title and reduced 10 pt lower source/legend/note where applicable.

The first branch regression exposed a second independent `tabularray-abnt` adapter that still forced table captions to 10 pt; that runtime residual was corrected at `7ec385ebecf21ba17e59db1e7ec16d3336f4bf4c`. A subsequent full Linux run `33964421597` then showed the corrected final-PDF measurements all green — illustration title 12 pt, illustration source 10 pt, table title 12 pt, table source 10 pt — while one legacy IBGE integration assertion still expected the historical 10 pt table caption. Commit `a3ce2d82899162d12b06c7335b149dc2b44ecfa3` aligns that stale observer with the accepted contract without weakening the final-PDF evidence.

Review item 21 remains open until a normal branch checkpoint containing that correction passes Static contract and full Linux integration. This post-audit note does not alter the closed audit baseline or its counts.

Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
