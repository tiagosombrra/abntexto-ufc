# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history. Detailed historical evidence remains authoritative in Git history, PR bodies/comments and exact GitHub Actions runs.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 `apud` evidence merge: `84e57059795da7927466d6834e733b1d61800631`
- Latest published release: `v2.1.0`
- Future release under audit: `v2.2.0`
- Canonical class/package identity: `abntexto-ufc`
- Legacy class entry point: deprecated compatibility shim only; outside the canonical CTAN package.
- UFC institutional mark: externalized from public/CTAN bundles; users may supply an official local asset through the supported class option.

## Governing method

The audit must not equate green CI with normative proof. Conservative policy remains in force:

- no rule is promoted to `PROVEN` merely because an aggregate check passes;
- unavailable authoritative/licensed clause text remains unavailable or partial;
- measured N6 conformance does not change proof-state;
- evidence-only PRs do not change normative values, locators, N5 tolerances or compatibility mappings;
- implementation defects exposed by evidence are corrected separately while the evidence predicate remains unchanged;
- fixture observations must not strengthen stored predicates;
- merge evidence only on the exact audited head with `behind_by=0`;
- after each bounded evidence merge, update this handoff before creating the next evidence branch.

## Phase status

| Phase | Status | Canonical result |
| --- | --- | --- |
| N0 | DONE | normative baseline established |
| N1 | DONE | 170/170 normative locators classified; `UNASSESSED=0` |
| N2 | DONE | UFC/ABNT reconciliation complete; `unknown-review=0` |
| N3 | DONE | 46/46 atomicity gaps resolved |
| N4 | DONE | false-coverage policy active; `unsafe-proven=0` |
| N5 | DONE | final-PDF oracle calibrated and integrated |
| N6 | IN PROGRESS | bounded positive final-PDF evidence; citation family dedicated scopes closed |
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
| Title page | `#65` | `PASS=7` |
| Approval | `#67` | `PASS=2` |
| Errata | `#69` | `PASS=3` |
| Optional lists | `#71` | `PASS=4` |
| TOC | `#73` | `PASS=5` |
| Pre-textual pagination/start-side | `#75` | `PASS=4` |
| Section hierarchy | `#77` | `PASS=3` |
| Section indicators | `#79/#80` | real separator defect fixed separately; final 3.0 pt gap matched calibration |
| Primary section recto duplex | `#82` | primary pages 1,3,5 |
| Primary after-spacing | `#84` | 41.55 pt vs 41.40 pt calibration; initial false FAIL was instrumentation |
| Subsection spacing | `#86` | `PASS=1` |
| Multiline hanging | `#88` | five levels, 10 continuation lines, max delta 0.9 pt |
| Unnumbered heading centering | `#90` | max delta 0.2162 pt |
| Body paragraph | `#92` | 20 mm measured 56.6930 pt; extra spacing 0.0 pt |
| Long direct quotation | `#94` / `e98c807cfb56dcac7bb15857efb2390dea38e887` | exact head `0c9d1f32609a61826d8c836412e75f9a0514aa48`; `PASS=5`; no implementation change |
| Short direct citation | `#96` / `df60a280dc952a5d8dc17480a07ea61479a01acd` | exact final head `6fbf6bd6260a904a7fe630968c2c5867be4eeea4`; `PASS=3`; two fixture-only instrumentation corrections |
| Direct citation source | `#98` / `3de83d0f216b62ba837fe5d594bc0379e38d63f8` | exact final head `e961b0a05ae9e83d53dcfa75bdf3d30f42801307`; `PASS=1`; one marker-only instrumentation correction |
| Indirect citation source | `#100` / `c0ff40d8841ca3ff689681b4f2beae2c14d5f866` | exact head `c58f0d0e1f70c81a37556472577f3a0ecf915f28`; `PASS=1`; no instrumentation incident |
| UFC author-date citation system | `#102` / `1b1a675e041ed40abad901c98b95a9c38854a4e0` | exact head `48e77a37295ca7e6d0f82c3b9a639e25d66739cc`; `PASS=1`; 2/2 author-date surfaces |
| Citation of citation (`apud`) | `#104` / `84e57059795da7927466d6834e733b1d61800631` | exact head `c20f1079640fd57329d07e0b9e7b05cb7ff95407`; `PASS=1`; 2/2 supported surfaces; no instrumentation incident |

## Citation-family N6 status

The dedicated citation rulesets currently present in `normativa/locator-audit-citations.json` are now covered by bounded N6 final-PDF evidence:

- `citations.direct-short` → #96
- `citations.direct-source` → #98
- `citations.indirect-source` → #100
- `citations.ufc-system` → #102
- `citations.apud` → #104
- `citations.direct-long` → #94

This statement is about dedicated measured N6 evidence only; it does not promote proof-state and must be rederived if the citation contract changes.

## Latest closed increment: citation of citation (`apud`)

Evidence PR `#104`, squash merge `84e57059795da7927466d6834e733b1d61800631`.

Stable base: `a4938f306a9b72899c05f4671a919a1fd2f42b00`.

Final exact audited head: `c20f1079640fd57329d07e0b9e7b05cb7ff95407`.

Ruleset and exact rule:

- `citations.apud`
- `citation.apud.presentation`
- stored predicate: `apud_supported = true`
- normativity: `required-when-applicable`
- locator status: `PARTIAL_WITH_REASON`
- UFC Guia de Citações 2025 `2.3.3, p. 11`: `VERIFIED`
- exact authoritative ABNT NBR 10520:2023 clause text remains `UNAVAILABLE_WITH_REASON` in the repository/public evidence corpus.

Supported rendering routes used by the evidence:

- parenthetical: `\apud[121]{eco1983}[147]{koche2009}`
- textual: `\textapud{eco1983}{koche2009}`
- bibliography fixture: `tests/fixtures/referencias-v2.bib` via `\ufcbibliografia`

Final exact-head CI:

- Normative source contract run `32921837629`: SUCCESS; job `98036787034`
- LaTeX preflight run `32921837576`: SUCCESS
- objects/bibliography job `98036786993`: SUCCESS; `PASS=8 FAIL=0 SKIP=0`
- post-textual job `98036786812`: SUCCESS
- reference document job `98036787035`: SUCCESS
- profile matrix job `98036787400`: SUCCESS including PDF/A-2b
- structural job `98036786955`: SUCCESS
- aggregate `latex-preflight` job `98038148107`: SUCCESS
- `N6-EVIDENCE apud-presentation-summary PASS=1 surfaces=2 supported_surfaces=2/2`

Measured final-PDF result:

- parenthetical surface preserved original source `Eco/1983`, `apud`, and consulted source `Koche/2009`; bounded window contained 9 words;
- textual surface preserved the same required identification; bounded window contained 5 words;
- both surfaces reported `apud_supported=true`;
- locator survival (`121`, `147`), punctuation, token order, typography/italics and exact parenthetical/textual form remained observational only;
- `exact_apud_format_not_strengthened=true` and `positive_fixture_evidence_only=true`.

Instrumentation / implementation history:

- the exact initial head passed the bounded oracle without fixture/instrumentation correction;
- no class/runtime implementation correction was required.

No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed in this increment.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order after citation-family closure:

1. object/table dimensions;
2. post-textual dimensions not already covered by bounded evidence;
3. deposit/distribution-related evidence measurable from the relevant final artifact or institutional workflow.

Closed N6 scopes must not be reopened without evidence of regression or a changed normative source.

## Immediate next bounded increment

No object/table ruleset is preselected in this documentation checkpoint.

After this handoff update is merged, rederive remaining N6 object/table candidates from the then-current `main`, full normative contract and relevant locator-audit files. Select the next bounded scope only from that rederived state; do not assume a candidate from chat history.

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

Merge this documentation checkpoint. Then, from the resulting stable `main`, rederive remaining N6 object/table rulesets and select the next bounded evidence scope from current contract/locator state. Do not create the next evidence branch before that rederivation.
