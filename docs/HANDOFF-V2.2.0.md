# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history. Detailed historical evidence remains authoritative in Git history, PR bodies/comments and exact GitHub Actions runs.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 short-direct-citation evidence merge: `df60a280dc952a5d8dc17480a07ea61479a01acd`
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
- historical proof-state baseline: `PARTIAL=114`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=5`, `NOT_APPLICABLE=1`, `PROVEN=0`

## N5 final-PDF oracle policy

Tools: `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo`, `pdffonts`.

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

Detailed fixtures and measurements remain in each PR. This ledger is the canonical resume index.

| Scope | PR / merge | Result / critical note |
| --- | --- | --- |
| Dedication + epigraph | `#59/#60/#61` | Evidence exposed three real class divergences; #60 fixed dedication +20 mm indent, short-epigraph quotation marks and long-epigraph +20 mm indent; final evidence passed. |
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
| Section indicators | `#79` / `96ee28fd04d17514fa21a5925c2305571c43220a` | evidence found a real separator defect; implementation fix `#80` / `9dd63e4cd54e47d1d5a2226160437283014b6e89`; final 3.0 pt gap == 3.0 pt calibration |
| Primary section recto duplex | `#82` / `838e83d19a133d19e7f9aae9d3d675f274da2ed3` | exact head `8f5926f43230131fafc5410e3a955ffc3af06f22`; primary pages 1,3,5 |
| Primary after-spacing | `#84` / `9a9b9bf8fda4807b83526c4843562229308e1378` | exact head `d36ad9c12327da4bb3d6ac5ef0003e5661a9a3d2`; 41.55 pt vs 41.40 pt calibration; initial false FAIL was instrumentation |
| Subsection spacing | `#86` / `19e1fa90a87b35fd5a9f987328bdcfd609809bd9` | exact head `c959db09f1622f96db6050c5a244fe43c4884f57`; `PASS=1` |
| Multiline hanging | `#88` / `decea2b1c7adc3093764ec22922d73fc87cfb22d` | exact head `e083cae66ac2bc05716009867b736d43e0745f28`; five levels, 10 continuation lines, max delta 0.9 pt |
| Unnumbered heading centering | `#90` / `0bf1a098688bdd1c6ceba077434bab53f448ffb8` | exact head `d4888fb6a6641c2e028d8046c0c6c364e033b6be`; max delta 0.2162 pt |
| Body paragraph | `#92` / `7e509a68f5dd3adc4aead749404425885cbe8745` | exact head `6080d321d7b5b37b1bb5d2821b8cf8fa072ac601`; 20 mm measured 56.6930 pt; extra spacing 0.0 pt |
| Long direct quotation | `#94` / `e98c807cfb56dcac7bb15857efb2390dea38e887` | exact head `0c9d1f32609a61826d8c836412e75f9a0514aa48`; `PASS=5`; no implementation change |
| Short direct citation | `#96` / `df60a280dc952a5d8dc17480a07ea61479a01acd` | exact final head `6fbf6bd6260a904a7fe630968c2c5867be4eeea4`; `PASS=3`; two fixture-only instrumentation corrections; no implementation change |

## Latest closed increment: short direct citation

Evidence PR `#96`, squash merge `df60a280dc952a5d8dc17480a07ea61479a01acd`.

Stable base: `5af7ef2e8be47e02c0ac9073613430cfbda1da49`.

Final exact audited head: `6fbf6bd6260a904a7fe630968c2c5867be4eeea4`.

Ruleset and exact rules:

- `citations.direct-short`
- `citation.direct-short.max-lines` → `max_lines = 3`
- `citation.direct-short.quotation-marks` → `style = "double"`
- `citation.direct-short.emphasis` → `citation_emphasis = false`

Locator state remains unchanged:

- ruleset status: `PARTIAL_WITH_REASON`
- UFC Guia de Citações 2025 `2.3.1.1, p. 8`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text: `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Supported rendering route: `\enquote{...}` through `csquotes`, already loaded by required `abntexto >= 1.1`.

Final exact-head CI:

- Normative source contract run `32915246185`: SUCCESS; job `98017494931`
- LaTeX preflight run `32915246180`: SUCCESS
- objects/bibliography job `98017494963`: SUCCESS; `PASS=8 FAIL=0 SKIP=0`
- structural job `98017494780`: SUCCESS
- profile matrix job `98017494974`: SUCCESS including PDF/A-2b certification
- aggregate `latex-preflight` job `98018574930`: SUCCESS
- `N6-EVIDENCE short-direct-citation-summary PASS=3 lines=3 opening_marks=["“"] closing_marks=["”"] font_control_id=1`

Measured final-PDF results:

- short-citation threshold: controlled quotation occupies exactly 3 lines; this is positive applicability evidence only, not a claim that the class automatically truncates or converts longer quotations;
- quotation marks: visible opening/closing marks are typographic double quotes `“` and `”`;
- citation-only emphasis: start/middle/end quote samples use the same `12.0 pt` font id and black color as the same-document body control; font-size delta is `0.0 pt` for every sample.

Instrumentation history:

1. Initial fixture used long unbreakable sentinels and produced an artificial `Overfull \\hbox (3.0972pt)`. Only marker strings were shortened; warning policy was not relaxed.
2. The next fixture payload itself occupied 5 lines, contradicting the positive short-citation applicability scenario. Only the controlled quotation text was shortened; checker and stored predicate remained unchanged.

Neither incident was a class/runtime defect. No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order:

1. remaining citation attribution/system dimensions;
2. object/table dimensions;
3. post-textual dimensions;
4. deposit/distribution-related evidence measurable from the relevant final artifact or institutional workflow.

Closed N6 scopes must not be reopened without evidence of regression or a changed normative source.

## Immediate next bounded increment

Next candidate: `citations.direct-source`.

Rederived on stable main `df60a280dc952a5d8dc17480a07ea61479a01acd` from `normativa/locator-audit-citations.json` and `normativa/coverage-rules-citations.json`:

- exact rule: `citation.direct.source`
- stored predicates:
  - `source_required = true`
  - `locator_when_available = true`
- current locator: `ABNT NBR 10520:2023; Guia UFC 2025, 2.3.1`
- locator status: `PARTIAL_WITH_REASON`
- UFC citation guide 2025 `2.3.1, p. 6-7`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text remains `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Supported citation route already exercised by the repository's bibliography fixture:

- `\cite[103]{oliveira2011}` renders a parenthetical author-date citation with locator;
- `\textcite[103]{oliveira2011}` renders a textual author-date citation with locator;
- both use the existing `\ufcbibliografia{tests/fixtures/referencias-v2.bib}` integration.

Recommended next evidence design:

1. rederive the exact rule payload and locator state from the then-current full contract before branch creation;
2. create a controlled direct-quotation fixture using an actual quotation plus the supported citation command and an available page locator;
3. verify from the final PDF that the direct quotation is accompanied by an identifiable source and that the supplied locator survives rendering;
4. measure only the stored predicates; do not strengthen them into one mandatory punctuation order, one exact citation command, or one exact textual/parenthetical form;
5. keep indirect citations, author-date system policy, `apud`, short/long quotation typography and reference-list formatting outside this increment;
6. integrate the gate into the existing `bibliography` validation domain;
7. if final-PDF evidence exposes a real implementation defect, preserve the FAIL and isolate the implementation fix before rerunning unchanged evidence.

## Required PR discipline

Every bounded audit PR must record stable base SHA, exact audited head SHA, complete rule scope, fixture/measurement strategy, workflow/job IDs, structured `N6-EVIDENCE`, and an explicit statement about normative values/locators/tolerances/proof-state. Merge only on the unchanged audited head with `behind_by=0`; then update this handoff before the next evidence branch.

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

Implementation is complete through PR #19: Node 24 migration, `configure-pages` v6, `upload-pages-artifact` v5, `deploy-pages` v5, and repository `has_pages=true`.

M1 remains `IMPLEMENTED`, not formally `DONE`, until explicit Pages/runtime/deployment evidence is reviewed and recorded.

## Open release-adjacent items

- PR #36 remains D5 distribution rehearsal only.
- Issue #18 remains open for bit-reproducible PDF differences (`CreationDate`, `ModDate`, PDF `/ID`) although pages/text/fonts/images were identical; reassess release-blocking status under the final public bundle policy.
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

From stable main `df60a280dc952a5d8dc17480a07ea61479a01acd`, rederive `citations.direct-source` and `citation.direct.source`. If unchanged, create an evidence-only N6 PR using the existing bibliography/citation route to prove source presence and preservation of an available locator in the final PDF. Keep indirect citations, system-policy rules, `apud`, quotation typography, class/runtime changes, normative values, locators, N5 tolerances, compatibility mappings and proof-state outside that increment.
