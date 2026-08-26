# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history. Detailed historical evidence remains authoritative in Git history, PR bodies/comments and exact GitHub Actions runs.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 direct-citation-source evidence merge: `3de83d0f216b62ba837fe5d594bc0379e38d63f8`
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
| Direct citation source | `#98` / `3de83d0f216b62ba837fe5d594bc0379e38d63f8` | exact final head `e961b0a05ae9e83d53dcfa75bdf3d30f42801307`; `PASS=1`; one marker-only instrumentation correction; no implementation change |

## Latest closed increment: direct citation source

Evidence PR `#98`, squash merge `3de83d0f216b62ba837fe5d594bc0379e38d63f8`.

Stable base: `5d3fa2929ad9509ba9ccbb37b09f8bddb38a615a`.

Final exact audited head: `e961b0a05ae9e83d53dcfa75bdf3d30f42801307`.

Ruleset and exact rule:

- `citations.direct-source`
- `citation.direct.source`
- stored predicates: `source_required = true`, `locator_when_available = true`

Locator state remains unchanged:

- ruleset status: `PARTIAL_WITH_REASON`
- UFC Guia de Citações 2025 `2.3.1, p. 6-7`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text: `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Supported rendering route used by the evidence:

- controlled direct quotation through `\enquote{...}`;
- source attribution through existing `\cite[103]{oliveira2011}` integration;
- bibliography source: `tests/fixtures/referencias-v2.bib` through `\ufcbibliografia`.

Final exact-head CI:

- Normative source contract run `32917579066`: SUCCESS; job `98024404595`
- LaTeX preflight run `32917579079`: SUCCESS
- objects/bibliography job `98024404205`: SUCCESS; `PASS=8 FAIL=0 SKIP=0`
- structural job `98024404412`: SUCCESS
- profile matrix job `98024404388`: SUCCESS including PDF/A-2b
- reference document job `98024404443`: SUCCESS
- post-textual job `98024404320`: SUCCESS
- aggregate `latex-preflight` job `98025491743`: SUCCESS
- `N6-EVIDENCE direct-citation-source-summary PASS=1 source_tokens=3/3 locator=103 locator_present=true`

Measured final-PDF result:

- source-identification tokens `Oliveira`, `Nunes` and `2011` were all present in the generated citation window;
- applicable locator token `103` survived rendering;
- source window contained 5 words and remained in the same controlled sentence as the quotation;
- punctuation, token order and parenthetical/textual form were explicitly observational only and were not promoted into new predicates.

Instrumentation history:

- initial head `088cede3ae1f70f6a92c9960e896f1e9b20663c9` failed before normative measurement because start marker `N6DSQ` was a prefix of end marker `N6DSQE`; substring lookup therefore found two matches;
- only scenario/fixture markers were changed to non-overlapping `N6DSOPN` and `N6DSCLS`;
- checker logic, normative rule, locator, tolerances and class/runtime implementation were unchanged.

No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed in this increment.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order:

1. remaining citation attribution/system dimensions;
2. object/table dimensions;
3. post-textual dimensions;
4. deposit/distribution-related evidence measurable from the relevant final artifact or institutional workflow.

Closed N6 scopes must not be reopened without evidence of regression or a changed normative source.

## Immediate next bounded increment

Next candidate: `citations.indirect-source`.

Rederived on stable main `3de83d0f216b62ba837fe5d594bc0379e38d63f8` from `normativa/locator-audit-citations.json` and `normativa/coverage-rules-citations.json`:

- exact rule: `citation.indirect.source`
- stored predicate: `source_required = true`
- current locator: `ABNT NBR 10520:2023; Guia UFC 2025, 2.3.2`
- locator status: `PARTIAL_WITH_REASON`
- UFC citation guide 2025 `2.3.2, p. 10`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text remains `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Supported citation routes already exercised by the bibliography fixture include `\cite{silva2020}` and `\textcite{silva2020}`.

Recommended evidence design:

1. rederive the exact rule payload and locator state from the then-current full contract before branch creation;
2. create a controlled paraphrase/indirect-citation fixture using an existing bibliography key and the supported citation route;
3. delimit the generated citation window in the final PDF and verify that an identifiable source survives rendering;
4. treat the fixture's paraphrase status as positive applicability evidence only — final-PDF extraction cannot prove semantic paraphrasing;
5. measure only `source_required=true`; do not add a locator requirement, punctuation rule, citation order or mandatory textual/parenthetical form;
6. keep `citation.system.ufc`, `citation.apud.presentation`, direct-quotation rules and reference-list formatting outside the increment;
7. integrate the gate in the existing `bibliography` validation domain;
8. preserve FAIL and isolate implementation corrections if the final-PDF evidence exposes a real defect.

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

From stable main `3de83d0f216b62ba837fe5d594bc0379e38d63f8`, rederive `citations.indirect-source` and `citation.indirect.source`. If unchanged, create an evidence-only N6 PR using a controlled indirect-citation fixture and the existing bibliography/citation route to prove source presence in the final PDF. Keep citation-system policy, `apud`, direct-quotation presentation, class/runtime changes, normative values, locators, N5 tolerances, compatibility mappings and proof-state outside that increment.
