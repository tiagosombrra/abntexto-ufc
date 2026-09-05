# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-04

## Current checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical branch: `main`; task branches are short-lived.
- Active phase: **Regression Audit**.
- Pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.
- Certified non-article foundation retained for comparison: `c79f3c73f1d51a30175e8259269504d029442a1c`.
- Scientific-article authority reconstruction is retained, but article runtime implementation is deferred and had not started when this regression reset began.
- Active regression plan: `docs/V3-REGRESSION-AUDIT.md`.
- Consolidated review input: `docs/UFC-LIBRARIAN-REVIEW.md` with exactly 34 tracked requirements.
- Initial review state: 19 `PASS`, 11 `PARTIAL`, 1 `FAIL`, 3 `NORMATIVE-REVIEW`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must describe the same active phase. Disagreement fails closed.

## Immediate action

Continue **Regression Audit** before making broad runtime corrections:

1. run the full current integration contract on the regression branch;
2. treat any failure as a finding until proven otherwise;
3. finish authority reconciliation for shared normative disputes;
4. close the audit matrix with owning files/tests for every item;
5. advance to **Core Corrections** only after the audit gate is satisfied.

The first high-priority authority review is object typography. The recovered librarian comments mark object titles as body-size text, while current V3 applies the reduced size to the complete object title box. The current UFC guide distinguishes the upper identification/title from legend/source text, so title and auxiliary object text must be audited separately.

## Known correction groups

- front-matter/reference placeholders and advisor punctuation;
- object title/source/legend/note typography and page-locator guidance;
- sentence-case examples and first-use acronym presentation;
- long-quotation locator/punctuation fixtures;
- selected NBR 6023:2025 edge cases;
- annex source example;
- stale V2 wording and retired V2-era profile vocabulary in the V3 reference document;
- final canonical-PDF visual parity/acceptance.

## Hard boundaries

- Do not resume Scientific Article runtime while shared regression/correction gates are open.
- Preserve the closed V3 public API unless current evidence authorizes a change.
- Do not convert reviewer comments directly into normative runtime behavior when current authority is unresolved.
- Do not weaken tests merely to recover a green build; correct the rule, generator, observer, or fixture according to the classified finding.
- Do not redistribute proprietary fonts.
- CTAN submission remains a future action owned by the explicit **Release** phase.
