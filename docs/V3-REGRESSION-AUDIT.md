# abntexto-ufc v3 — Regression Audit

Updated: 2026-09-05
Status: CLOSED
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`
Closeout checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`

## Closeout

Regression Audit closed after the shared V3 foundation was rechecked before scientific-article runtime work.

Evidence at closeout: the two reviewed PDFs are represented by exactly 34 tracked requirements in `docs/UFC-LIBRARIAN-REVIEW.md`; `docs/V3-CORRECTION-PLAN.md` contains the executable correction queue; the active roadmap uses readable phase names; object typography and selected NBR 6023:2025 disputes had explicit unresolved authority status at audit closeout; Static `33937439818` passed; full Linux `33937439846` passed; scientific-article runtime had not started before the regression reset.

The project therefore advanced to **Core Corrections**. This closeout does not mean the 34 review items were already corrected.

## Findings transferred to Core Corrections

Unambiguous defects included title-page advisor/co-advisor punctuation, incomplete optional-department/full-name guidance, incomplete committee acronym examples, missing annex source demonstration, stale V2-era wording, retired public API vocabulary, and stale reference paths in the canonical V3 guide.

At audit closeout, object-title size was intentionally unresolved because existing tests certified reduced-size upper object titles while the recovered reviews requested body-size titles and the institutional guide distinguished upper identification/title from lower source/legend/note elements. Selected DOI, online-availability, repeated-author, and corporate-author cases also remained under current-edition NBR 6023:2025 review rather than being copied mechanically from the older reviewed template.

Code/algorithm typography already had strong implementation evidence. The audit also found project-owned Portuguese diagnostics that the language gate did not detect; this class of false negative remains relevant to Core Corrections evidence hardening.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit baseline counts and remain historical closeout facts.

## Post-audit disposition in Core Corrections

The object-title authority conflict is resolved and accepted. Checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and full Linux `33965794519`; review item 21 is PASS.

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, closing review items 11, 16 and 28. Current librarian-review state is therefore **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

The engineering-language false-negative finding is now being exercised fail-closed. Static `33970711005` exposed `algorithm-numbering.sh`; Static `33970988780` separately exposed temporary documentation-governance drift; after governance restoration, Static `33971156481` exposed four additional old project-owned Portuguese diagnostic surfaces. Current implementation `1129935fe5e4f97d6fe3798fd5e4777760f0d61b` translates those surfaces and expands detector self-tests to 18 cases. This hardening is not accepted until a synchronized Static/full Linux checkpoint is green.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence. Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
