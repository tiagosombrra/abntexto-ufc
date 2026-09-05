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

Code/algorithm typography already had strong implementation evidence. The audit also found project-owned Portuguese diagnostics that the language gate did not detect; this false-negative class was transferred to Core Corrections evidence hardening.

## Initial 34-item baseline

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit baseline counts and remain historical closeout facts.

## Post-audit disposition in Core Corrections

The object-title authority conflict is resolved and accepted. `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md` records the 12 pt upper identification/title and reduced 10 pt lower source/legend/note split where applicable. Synchronized checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and full Linux `33965794519` with `PASS=31 FAIL=0 SKIP=0`; review item 21 is PASS.

The canonical-reference source batch closed at `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f`: Static `33968579418` and full Linux `33968579449` succeeded and emitted source-level librarian evidence for items 11, 16 and 28.

The generated-PDF acceptance batch then closed at `c4c59f83b67cb152ed9a88345541457b8f18021c`: Static `33969505681` and full Linux `33969505614` succeeded, Linux reported `PASS=31 FAIL=0 SKIP=0`, and the canonical `Reference document` gate emitted explicit PDF-level PASS evidence for items 11, 16 and 28. Those three review items are now PASS.

Current review state in Core Corrections is therefore **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

The remaining evidence-quality finding is the permanent engineering-language detector false-negative class. Implementation `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` strengthens high-confidence mixed-language detection, expands its self-test, and translates known project-owned mixed Portuguese/English diagnostics in `multivolume.sh` and `references-6023.sh`. This correction is not accepted until a synchronized branch checkpoint passes Static and full Linux; any additional mixed diagnostics exposed by the stronger detector must be corrected rather than hidden by weakening the gate.

Item 33 remains fail-closed because current authoritative NBR 6023:2025 text for the disputed edge cases is not available in the evidence corpus.

Scientific Article remains deferred until Core Corrections and Reference PDF Validation close.
