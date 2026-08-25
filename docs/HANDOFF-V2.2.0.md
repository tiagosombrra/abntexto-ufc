# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history. Detailed historical evidence remains authoritative in Git history, PR bodies/comments and exact GitHub Actions runs; this handoff keeps the current state, critical audit history and the next bounded action compact enough to resume efficiently.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 long-direct-quotation evidence merge: `e98c807cfb56dcac7bb15857efb2390dea38e887`
- Latest published release: `v2.1.0`
- Future release under audit: `v2.2.0`
- Canonical class/package identity: `abntexto-ufc`
- Legacy class entry point: deprecated compatibility shim only; outside the canonical CTAN package.
- UFC institutional mark: externalized from public/CTAN bundles; users may supply an official local asset through the supported class option.

## Governing method

The audit must not equate green CI with normative proof. Each rule is tracked through provenance, locator quality, atomicity and, when applicable, direct final-PDF measurement.

Conservative proof policy remains in force:

- no rule is promoted to `PROVEN` merely because a parent or aggregate check passes;
- unavailable authoritative/licensed clause text remains explicitly unavailable or partial;
- measured N6 conformance does not itself change proof-state;
- evidence-only PRs do not change normative values, locators, N5 tolerances or compatibility mappings;
- implementation defects exposed by evidence are corrected in isolated implementation PRs;
- fixture observations must not strengthen the stored normative predicate;
- evidence PRs merge only on the exact audited head and while `behind_by=0`;
- after every bounded merge, update this handoff before starting the next evidence head.

## Phase status

| Phase | Status | Canonical result |
| --- | --- | --- |
| N0 | DONE | normative baseline established |
| N1 | DONE | 170/170 normative locators classified; `UNASSESSED=0` |
| N2 | DONE | UFC/ABNT reconciliation complete; `unknown-review=0` |
| N3 | DONE | 46/46 atomicity gaps resolved |
| N4 | DONE | false-coverage policy active; `unsafe-proven=0` |
| N5 | DONE | final-PDF oracle calibrated and integrated |
| N6 | IN PROGRESS | bounded positive final-PDF evidence |
| N7-N15 | PENDING | continue only after N6 closure |
| M1 | IMPLEMENTED | Node 24 / Pages migration merged; formal runtime/deployment evidence pending |
| D0-D4 | DONE | CTAN identity, asset and distribution remediation completed |
| D5 rehearsal | VALIDATED | rehearsal only; not a release decision |
| D5 final | BLOCKED | repeat only on N15-approved final source tree |
| D6 | BLOCKED | CTAN resubmission follows final D5 certification |

## Normative baseline after N5

Historical baseline; do not recompute or rewrite without an explicit proof-state phase/change.

- full atomic rules: 181
- normative rules: 170
- N1 locator coverage: 170/170
- N2 unknown review relationships: 0
- N3 gaps resolved: 46/46
- N4 unsafe `PROVEN`: 0
- historical proof-state baseline:
  - `PARTIAL=114`
  - `NOT_PROVEN=51`
  - `CONDITIONAL=10`
  - `MANUAL=5`
  - `NOT_APPLICABLE=1`
  - `PROVEN=0`

## N5 final-PDF oracle policy

Tools:

- `pdftotext -bbox-layout`
- `pdftohtml -xml -zoom 1.0`
- `pdfinfo`
- `pdffonts`

Tolerances remain unchanged:

- page size: `1 pt`
- horizontal position: `5 pt`
- vertical position: `5 pt`
- font size: `1 pt`

## Major normative-audit milestones

- N1: PR `#55` — 170/170 locator coverage.
- N2: PR `#56` — reconciliation complete.
- N4: PR `#57` — parent/local promotion policy and `unsafe-proven=0`.
- N5: PR `#58` — final-PDF oracle calibrated and integrated.

## N6 completed increments

The detailed fixtures, exact rule payloads and measurements remain in each PR. The ledger below is the canonical resume index.

| Scope | PR / merge | Result / critical note |
| --- | --- | --- |
| Dedication + epigraph | `#59/#60/#61` | Evidence exposed three real class divergences; #60 fixed dedication +20 mm indent, short-epigraph quotation marks and long-epigraph +20 mm indent; final bounded evidence passed. |
| Acknowledgements | `#62` | `PASS=8` |
| Summary / abstract / keywords | `#63` | `PASS=14` |
| Cover | `#64` | `PASS=4` |
| Title page | `#65` / `c4b7865e5857ab3195a2b4e32f7da94673a29569` | exact head `d3fb8957f50868c3334ee29c134db9b6b8a42e10`; `PASS=7` |
| Approval | `#67` / `673d25252b3b526b5503309535cb423184456e35` | exact head `effeab0cbc9a6b82d2d81cf038e2656e42c603f5`; `PASS=2` |
| Errata | `#69` / `5b6050b89e701e9463242de9d9948af9bb6a2687` | exact head `c1351a194e47afc5f8996d7f64fd2d31ad9d0762`; `PASS=3` |
| Optional lists | `#71` / `961cfb41de76c192b7a703956e861c7aba88c251` | exact head `33c41dc741dfce7c110a657acdd5cf091b6f2024`; `PASS=4` |
| TOC | `#73` / `1f1feed15e2c69a067022042f26aa663447cdd9d` | exact head `f042ff99910a7e9e0fb0d3ca40cc292f047f9980`; `PASS=5` |
| Pre-textual pagination/start-side | `#75` / `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5` | exact head `b5a9f1188b8d981dbd519561cdd7e4ba446782e1`; `PASS=4` |
| Section hierarchy | `#77` / `2a4b38a57bf1fafa3f4dbb9a7992340f3f03e2a8` | exact head `5c5db3a2e9a78bc97d252a8da9fb3bdad74577b5`; `PASS=3` |
| Section indicators | `#79` / `96ee28fd04d17514fa21a5925c2305571c43220a` | evidence found real separator defect; implementation fix `#80` / `9dd63e4cd54e47d1d5a2226160437283014b6e89`; final 3.0 pt gap == 3.0 pt calibration |
| Primary section recto duplex | `#82` / `838e83d19a133d19e7f9aae9d3d675f274da2ed3` | exact head `8f5926f43230131fafc5410e3a955ffc3af06f22`; primary pages 1,3,5 |
| Primary after-spacing | `#84` / `9a9b9bf8fda4807b83526c4843562229308e1378` | exact head `d36ad9c12327da4bb3d6ac5ef0003e5661a9a3d2`; final gap 41.55 pt vs 41.40 pt calibration; initial false FAIL was instrumentation |
| Subsection spacing | `#86` / `19e1fa90a87b35fd5a9f987328bdcfd609809bd9` | exact head `c959db09f1622f96db6050c5a244fe43c4884f57`; `PASS=1` |
| Multiline hanging | `#88` / `decea2b1c7adc3093764ec22922d73fc87cfb22d` | exact head `e083cae66ac2bc05716009867b736d43e0745f28`; five levels, 10 continuation lines, max delta 0.9 pt |
| Unnumbered heading centering | `#90` / `0bf1a098688bdd1c6ceba077434bab53f448ffb8` | exact head `d4888fb6a6641c2e028d8046c0c6c364e033b6be`; three implementation routes; max delta 0.2162 pt |
| Body paragraph | `#92` / `7e509a68f5dd3adc4aead749404425885cbe8745` | exact head `6080d321d7b5b37b1bb5d2821b8cf8fa072ac601`; 20 mm = 56.6929 pt, measured 56.6930 pt; extra spacing 0.0 pt |
| Long direct quotation | `#94` / `e98c807cfb56dcac7bb15857efb2390dea38e887` | exact head `0c9d1f32609a61826d8c836412e75f9a0514aa48`; `PASS=5`, no implementation change |

## Latest closed increment: long direct quotation

Evidence PR `#94`, squash merge `e98c807cfb56dcac7bb15857efb2390dea38e887`.

Stable base: `56684fb3bafaaf34e756761f69212511e159e568`.

Exact audited head: `0c9d1f32609a61826d8c836412e75f9a0514aa48`.

Ruleset and rules:

- `citations.direct-long`
- `quotation.long.block`
- `quotation.long.indent.left`
- `quotation.long.font.size`
- `quotation.long.line-spacing`
- `quotation.long.quotation-marks`

Stored predicates/applicability:

- `block = true`
- `min_lines = 4`
- `left_indent_mm = 40`
- `font_pt = 10`
- `line_spacing = 1.0`
- `quotation_marks = false`

Locator state remains unchanged:

- ruleset status: `PARTIAL_WITH_REASON`
- UFC Guia de Citações 2025 `2.3.1.2, p. 9`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text: `UNAVAILABLE_WITH_REASON` in repository/public evidence corpus.

Real rendering route: supported upstream public `\Enquote{...}` from required `abntexto >= 1.1`.

Exact-head CI:

- Normative source contract run `32911638143`: SUCCESS
- LaTeX preflight run `32911638181`: SUCCESS
- structural job `98006834382`: SUCCESS
- aggregate `latex-preflight` job `98008115532`: SUCCESS
- structural `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE long-quotation-summary PASS=5 lines=10 max_indent_delta_pt=0.0002 average_gap_pt=11.5000 calibration_gap_pt=11.5000 max_spacing_delta_pt=0.0000 max_font_delta_pt=0.0000 quote_marks=0`

Measured final-PDF results:

- distinct block: 10 naturally wrapped lines; applicability requires at least 4;
- left indent: all ten lines at `113.386 pt` from the text-left control; 40 mm expected = `113.3858 pt`; max delta `0.0002 pt`;
- font: start/middle/end samples all `10.0 pt`;
- line spacing: all nine internal gaps `11.5 pt`; same-document `abntsmall` + `singlesp` calibration `11.5 pt`;
- quotation marks: zero visible quotation-mark characters in the measured quote range.

No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed in this increment.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order after the closed body-paragraph and long-quotation blocks:

1. remaining citation presentation and attribution dimensions;
2. object/table dimensions;
3. post-textual dimensions;
4. deposit/distribution-related evidence measurable from the relevant final artifact or institutional workflow.

Closed N6 scopes must not be reopened without evidence of regression or a changed normative source.

## Immediate next bounded increment

Next: `citations.direct-short`.

Current rederived scope from `normativa/locator-audit-citations.json` and `normativa/coverage-rules-citations.json` on stable main `e98c807cfb56dcac7bb15857efb2390dea38e887`:

- exact rules:
  - `citation.direct-short.max-lines`
  - `citation.direct-short.quotation-marks`
  - `citation.direct-short.emphasis`
- stored predicates:
  - `values.max_lines = 3`
  - `values.style = "double"`
  - `values.citation_emphasis = false`
- current locator: `ABNT NBR 10520:2023; Guia UFC 2025, 2.3.1.1`
- locator status: `PARTIAL_WITH_REASON`
- UFC citation guide 2025 `2.3.1.1, p. 8`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text remains `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Rendering-path observation to re-confirm at evidence-branch creation time:

- `abntexto` loads `csquotes` and documents public `\enquote{...}` for ordinary quotation marks;
- `abntexto-ufc` requires `abntexto >= 1.1`;
- source-attribution rule `citation.direct.source` is a separate ruleset and must not be absorbed into this presentation-only increment.

Recommended final-PDF evidence design:

1. rederive all three exact rule payloads and locator state from the then-current full contract before creating the evidence branch;
2. exercise the supported `\enquote{...}` route inside ordinary body text with a controlled short quotation that wraps naturally but remains within three lines;
3. verify applicability with measured line count only; do not convert the threshold into an exact required line count;
4. verify the rendered opening and closing marks are the expected double-quotation style using PDF text extraction, with source fixture wording chosen to avoid unrelated quote characters;
5. compare typography inside the short quotation against adjacent ordinary body text of the same paragraph to prove that citation status alone adds no bold/italic/small-cap emphasis;
6. keep source attribution, citation locator formatting, long quotation rules and body typography rules outside this increment;
7. if evidence exposes a real implementation defect, preserve the FAIL, isolate the implementation correction, then rerun the unchanged evidence.

## Required PR discipline

Every bounded audit PR must record:

1. stable base SHA;
2. exact audited head SHA;
3. complete rule scope;
4. fixtures and measurement strategy;
5. required workflow run IDs and relevant job ID;
6. structured `N6-EVIDENCE` summary;
7. explicit statement about normative values, locators, tolerances and proof-state;
8. merge only on the unchanged audited head and while `behind_by=0`;
9. after merge, update this handoff with the merge SHA and next action.

## CTAN / release state

Technical blockers already remediated for v2.2.0:

- canonical package/class identity is `abntexto-ufc`;
- legacy identity remains only through compatibility surface outside the canonical CTAN package;
- UFC coat of arms is externalized from public/CTAN archives;
- CTAN archive is limited to canonical runtime, essential documentation and portable example;
- archive/asset identity guards and allowlists are present;
- D5 distribution rehearsal exists in PR #36.

Do not tag or publish v2.2.0 from the rehearsal. Final D5 must run on the N15-approved final source tree; D6 CTAN resubmission follows that certification.

## M1 state

Implementation is complete through PR #19:

- Node 24 migration;
- `configure-pages` v6;
- `upload-pages-artifact` v5;
- `deploy-pages` v5;
- repository `has_pages=true`.

M1 remains `IMPLEMENTED`, not formally `DONE`, until explicit Pages/runtime/deployment evidence is reviewed and recorded.

## Open release-adjacent items

- PR #36 remains D5 distribution rehearsal only.
- Issue #18 remains open for bit-reproducible PDF differences (`CreationDate`, `ModDate`, PDF `/ID`) although pages/text/fonts/images were identical; reassess release-blocking status later under the final public bundle policy.
- D5 final remains blocked by N15.
- D6 CTAN resubmission remains blocked by final D5.

## How to resume

Read, in order:

1. this file;
2. current `main` SHA and open PRs;
3. latest bounded audit PR body/comments and exact-head workflow runs;
4. current full contract, relevant locator ruleset and N5 oracle policy for the next scope.

Do not reconstruct state primarily from old chats. Git history, this handoff and exact CI evidence are authoritative.

## Next action

From stable main `e98c807cfb56dcac7bb15857efb2390dea38e887`, rederive `citations.direct-short` and its three presentation rules. If unchanged, create an evidence-only N6 PR using the supported `\enquote{...}` route to measure the short-quotation line threshold, double quotation marks and absence of citation-only typographic emphasis. Keep `citation.direct.source`, long-quotation rules, class/runtime changes, normative values, locators, N5 tolerances, compatibility mappings and proof-state outside that increment.
