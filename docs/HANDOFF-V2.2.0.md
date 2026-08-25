# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 subsection-spacing evidence merge: `19e1fa90a87b35fd5a9f987328bdcfd609809bd9`
- Latest published release: `v2.1.0`
- Future release under audit: `v2.2.0`
- Canonical class/package identity: `abntexto-ufc`
- The legacy class entry point remains only as a deprecated compatibility shim and is outside the canonical CTAN package.
- UFC institutional mark is externalized from public/CTAN bundles; users may supply an official local asset through the supported class option.

## Governing method

The v2.2.0 audit must not equate green CI with normative proof. Each normative rule is tracked through source provenance, locator quality, atomicity and, when applicable, direct final-PDF measurement.

Conservative proof policy remains in force:

- no rule is promoted to `PROVEN` merely because a parent or aggregate check passes;
- unavailable authoritative/licensed clause text remains explicitly unavailable or partial as appropriate;
- measured N6 conformance does not itself change proof-state;
- normative values, locators and N5 oracle tolerances are not changed inside evidence-only PRs;
- implementation defects exposed by evidence are corrected in isolated implementation PRs;
- fixture observations must not silently strengthen the stored normative predicate;
- evidence PRs merge only on the exact audited head and while up to date with `main`.

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
| M1 | IMPLEMENTED | Node 24 / Pages migration merged; formal runtime/deployment evidence still pending |
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

## Major normative-audit milestones

- N1: PR `#55` — 170/170 locator coverage.
- N2: PR `#56` — reconciliation complete.
- N4: PR `#57` — parent/local promotion policy and `unsafe-proven=0`.
- N5: PR `#58` — PDF oracle based on `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo` and `pdffonts`.
- N5 tolerances remain: page size 1 pt, horizontal position 5 pt, vertical position 5 pt, font size 1 pt.

## N6 completed increments

### Dedication and epigraph

PRs `#59`, `#60`, `#61`.

Initial measurement exposed three real class divergences: dedication +20 mm left indent, missing short-epigraph quotation marks, and long-epigraph +20 mm left indent. PR #60 corrected implementation only; PR #61 added wrapped-text evidence. Final bounded evidence passes all scoped dimensions.

### Acknowledgements

PR `#62`: final `PASS=8`.

### Summary / abstract / keywords

PR `#63`: final `PASS=14`.

### Cover

PR `#64`: final `PASS=4`.

### Title page

PR `#65`, squash merge `c4b7865e5857ab3195a2b4e32f7da94673a29569`.

Exact audited head `d3fb8957f50868c3334ee29c134db9b6b8a42e10`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE title-page-summary PASS=7`.

### Approval page

PR `#67`, squash merge `673d25252b3b526b5503309535cb423184456e35`.

Exact audited head `effeab0cbc9a6b82d2d81cf038e2656e42c603f5`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE approval-summary PASS=2 academic_profiles=4 supplemental_profiles=2`.

The first fixture had a duplicated marker in graduation/specialization output; only fixture instrumentation was corrected.

### Errata

PR `#69`, squash merge `5b6050b89e701e9463242de9d9948af9bb6a2687`.

Exact audited head `c1351a194e47afc5f8996d7f64fd2d31ad9d0762`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE errata-summary PASS=3 present_pages=3 absent_pages=2`.

The initial oracle incorrectly strengthened `after=title-page` into immediate adjacency. Final predicate is only `errata_page > title_page`; `page_delta` is observational.

### Optional pre-textual lists

PR `#71`, squash merge `961cfb41de76c192b7a703956e861c7aba88c251`.

Exact audited head `33c41dc741dfce7c110a657acdd5cf091b6f2024`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE optional-lists-summary PASS=4 present_fixtures=4 absent_pages=1`.

### Table of contents

PR `#73`, squash merge `1f1feed15e2c69a067022042f26aa663447cdd9d`.

Exact audited head `f042ff99910a7e9e0fb0d3ca40cc292f047f9980`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE toc-summary PASS=5 toc_pages=5 hierarchy_levels=5 non_normative=1`.

### Pre-textual pagination and start-side transition

PR `#75`, squash merge `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5`.

Exact audited head `b5a9f1188b8d981dbd519561cdd7e4ba446782e1`; structural `PASS=14 FAIL=0 SKIP=0`; `N6-EVIDENCE pretextual-pagination-summary PASS=4 duplex_pages=27 catalog_pages=3 recto_markers=13`.

Scoped rules:

- `pagination.pretextual.counted-not-numbered`
- `pagination.catalog-data.not-counted`
- `pagination.textual.display-start`
- `pretextual.start.recto`

### Textual section hierarchy

PR `#77`, squash merge `2a4b38a57bf1fafa3f4dbb9a7992340f3f03e2a8`.

Exact audited head `5c5db3a2e9a78bc97d252a8da9fb3bdad74577b5`.

- Normative source contract `32854036704`: SUCCESS
- LaTeX preflight `32854036715`: SUCCESS
- structural job `97821531899`: SUCCESS
- aggregate `latex-preflight` `97823695121`: SUCCESS
- structural `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE section-hierarchy-summary PASS=3 levels=5 first_primary_page=1 second_primary_page=2`

Scoped rules:

- `section.numbering.progressive`
- `section.levels.max`
- `section.primary.new-page`

### Textual section indicators

Evidence PR `#79`, squash merge `96ee28fd04d17514fa21a5925c2305571c43220a`.

Final exact audited head `23ce3c5de0d580aab0caaea59349732e8f7e1535`.

Scoped rules:

- `section.indicator.alignment`
- `section.indicator.separator`

Initial evidence correctly exposed a real implementation defect: the inherited wide separator exceeded the single-character-space calibration. PR `#80`, exact head `0fc77f034ce63ac9bc4804fe0071435342404144`, squash merge `9dd63e4cd54e47d1d5a2226160437283014b6e89`, corrected only the five numbered textual-section printers.

Final evidence:

- Normative source contract `32872834514`: SUCCESS
- LaTeX preflight `32872834517`: SUCCESS
- structural job `97883700774`: SUCCESS
- aggregate `latex-preflight` `97886512955`: SUCCESS
- structural `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE section-indicator-summary PASS=2 levels=5`
- measured heading gap = 3.0 pt; same-font literal-space calibration = 3.0 pt; delta = 0.0 pt at all five levels.

### Primary section recto in duplex documents

Evidence PR `#82`, squash merge `838e83d19a133d19e7f9aae9d3d675f274da2ed3`.

Exact audited head `8f5926f43230131fafc5410e3a955ffc3af06f22`.

- Normative source contract `32876510274`: SUCCESS
- LaTeX preflight `32876510233`: SUCCESS
- structural job `97895584067`: SUCCESS
- aggregate `latex-preflight` `97898148526`: SUCCESS
- structural `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE section-primary-recto-duplex-summary PASS=1 primaries=3 pages=1,3,5`

Rule `section.primary.recto-duplex` passed on physical pages 1, 3 and 5. Blank transition pages are observational only.

### Primary section after-spacing

Evidence PR `#84`, squash merge `9a9b9bf8fda4807b83526c4843562229308e1378`.

Stable base: `8fcdfb72f91860c32ff952b46f4992e0a680bf60`.

Final exact audited head: `d36ad9c12327da4bb3d6ac5ef0003e5661a9a3d2`.

Scoped rule:

- `section.primary.after-spacing`

Stored predicate:

- `values.after_factor = 1.5`

Final evidence:

- Normative source contract `32884056552`: SUCCESS
- LaTeX preflight `32884056758`: SUCCESS
- structural job `97920193298`: SUCCESS
- aggregate `latex-preflight` `97922278296`: SUCCESS
- structural `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE section-primary-after-spacing-summary PASS=1 gap_pt=41.5500 calibration_pt=41.4000`
- measured delta = `0.15 pt`, within the N5 vertical tolerance of `5 pt`.

Instrumentation history is part of the audit record. Initial head `07b11dc7965b9e514062c14bb6a1576e5cf9b669` compared the heading/body center-to-center interval (`41.55 pt`) against directly adjacent 1.5-spaced calibration lines (`20.70 pt`) and therefore reported a false FAIL. Inspection of the pinned upstream section implementation showed that the primary heading applies one baseline vertical skip after the heading. Existing N6 keyword-position evidence independently uses the same geometry: one blank 1.5-spaced interval is approximately two center-to-center baseline intervals. The final fixture therefore uses a like-for-like same-document calibration with one explicit 1.5-spaced vertical interval, yielding `41.40 pt`.

This was an instrumentation correction, not a class defect. No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed.

### Subsection before/after spacing

Evidence PR `#86`, squash merge `19e1fa90a87b35fd5a9f987328bdcfd609809bd9`.

Stable base: `060a4e7e0f96b92a9b40518daee87be66f520061`.

Final exact audited head: `c959db09f1622f96db6050c5a244fe43c4884f57`.

Scoped rule:

- `section.subsection.before-after-spacing`

Stored predicates:

- `values.before_factor = 1.5`
- `values.after_factor = 1.5`

Final exact-head CI evidence:

- Normative source contract `32886010258`: SUCCESS
- LaTeX preflight `32886010255`: SUCCESS
- structural job `97926524853`: SUCCESS
- aggregate `latex-preflight` `97929084769`: SUCCESS
- `N6-EVIDENCE subsection-spacing-summary PASS=1`

The final-PDF oracle measures the before and after intervals independently with `pdftotext -bbox-layout` word-center geometry and compares both against a same-document `onehalfsp` calibration containing one explicit `\baselineskip` interval. The N5 vertical tolerance remains `5 pt`; the gate hard-fails unless both predicates are within tolerance.

No class/runtime implementation, normative value, locator, N5 tolerance, compatibility mapping or proof-state changed in this increment.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order:

1. remaining textual section layout/typography dimensions;
2. quotation and paragraph dimensions;
3. citation/object dimensions;
4. post-textual dimensions;
5. deposit/distribution-related evidence measurable from the relevant final artifact or institutional workflow.

Current section-related rulesets still outside the completed section scopes:

- `sections.multiline-hanging`: `section.multiline.hanging`
- `sections.unnumbered-centered`: `heading.unnumbered.centered`

Do not infer either dimension from prior green section evidence.

## Immediate next bounded increment

Next: `sections.multiline-hanging`.

Current rederived scope from `normativa/locator-audit-sections-footnotes-nature.json` and the full contract:

- ruleset: `sections.multiline-hanging`
- exact rule: `section.multiline.hanging`
- stored predicate: `values.enabled = true`
- institutional locator: UFC `4.5.1(d), p. 77`

Before creating the evidence PR:

1. rederive the exact ruleset mapping and current full-contract value from the source tree again at branch creation time;
2. construct controlled final-PDF fixtures that force numbered section titles to wrap naturally to multiple lines;
3. measure the continuation-line horizontal alignment relative to the first title-text character, not relative to the numeric indicator;
4. exercise enough section levels to avoid proving only one printer implementation while keeping the single stored predicate unchanged;
5. use only the N5 horizontal-position tolerance and treat line-break positions/wording as fixture integrity or observational evidence, not new normative predicates;
6. keep unnumbered-heading centering, section spacing, typography and unrelated dimensions outside this increment;
7. if evidence exposes a real class defect, preserve the FAIL, use an isolated implementation-fix PR, rerun unchanged evidence, then close the component.

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

From stable main `19e1fa90a87b35fd5a9f987328bdcfd609809bd9`, rederive `sections.multiline-hanging` and `section.multiline.hanging` (`values.enabled=true`). If the scope remains exactly one rule, create an evidence-only N6 PR with controlled final-PDF measurement of multiline continuation alignment. Do not absorb unnumbered-heading centering, runtime/class changes, normative values, locators, tolerances, compatibility mappings or proof-state into that increment.
