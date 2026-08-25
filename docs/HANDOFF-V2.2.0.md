# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 pre-textual pagination/start-side evidence merge: `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5`
- Latest published release: `v2.1.0`
- Future release under audit: `v2.2.0`
- Canonical class/package identity: `abntexto-ufc`
- The legacy class entry point remains only as a deprecated compatibility shim.
- UFC institutional mark is excluded from public/CTAN bundles; users may supply an official local asset through the supported class option.

## Governing method

The v2.2.0 audit must not equate green CI with normative proof. Each normative rule must be tracked through source provenance, locator quality, atomicity, positive/negative evidence and, when applicable, final-PDF measurement.

Conservative proof policy remains in force:

- no rule is promoted to `PROVEN` merely because a parent/aggregate check passes;
- source text unavailable at authoritative/licensed clause level remains `UNAVAILABLE_WITH_REASON` or `PARTIAL_WITH_REASON` as appropriate;
- measured N6 conformance does not itself change proof-state;
- normative values, locators and oracle tolerances must not be changed inside evidence-only PRs;
- implementation corrections discovered by evidence must be isolated in separate fix PRs.

## Phase status

| Phase | Status | Canonical result |
| --- | --- | --- |
| N0 | DONE | normative baseline established |
| N1 | DONE | 170/170 normative locators classified; `UNASSESSED=0`; mode `complete` |
| N2 | DONE | UFC/ABNT reconciliation complete; `unknown-review=0` |
| N3 | DONE | 46/46 atomicity gaps resolved |
| N4 | DONE | false-coverage policy active; `unsafe-proven=0` |
| N5 | DONE | final-PDF oracle calibrated and integrated |
| N6 | IN PROGRESS | positive final-PDF evidence by bounded component |
| N7-N15 | PENDING | continue only after N6 closure |
| M1 | IMPLEMENTED | Node 24 / Pages migration merged; formal runtime/deployment closure still requires explicit evidence review |
| D0-D4 | DONE | CTAN identity, asset and distribution remediation completed |
| D5 rehearsal | VALIDATED | rehearsal only; not a release decision |
| D5 final | BLOCKED | repeat only on N15-approved final source tree |
| D6 | BLOCKED | CTAN resubmission follows final D5 certification |

## Normative baseline after N5

- full atomic rules: 181
- normative rules: 170
- N1 locator coverage: 170/170
- N2 unknown review relationships: 0
- N3 gaps resolved: 46/46
- N4 unsafe `PROVEN`: 0
- proof-state baseline before later promotions:
  - `PARTIAL=114`
  - `NOT_PROVEN=51`
  - `CONDITIONAL=10`
  - `MANUAL=5`
  - `NOT_APPLICABLE=1`
  - `PROVEN=0`

Do not recompute or alter these historical baseline numbers without an explicit proof-state phase/change.

## N6 completed increments

### Dedication and epigraph

PRs `#59`, `#60`, `#61`.

The first measured fixture exposed real divergences instead of masking them:

- `dedication.indent.left` inherited an unintended +20 mm paragraph indent;
- `epigraph.short.quotation-marks` was missing required quotation marks;
- `epigraph.long.indent.left` inherited the same unintended +20 mm paragraph indent.

PR #60 corrected implementation only. PR #61 added naturally wrapped text so justification could be measured rather than inferred from explicit line breaks.

Final bounded evidence: all dedication/short-epigraph/long-epigraph dimensions pass, including wrapped-text alignment.

### Acknowledgements

PR `#62`.

Final evidence: `PASS=8` for own-page transition, heading case/weight/alignment/font size and body font size/1.5 spacing/justification.

### Summary / abstract / keywords

PR `#63`.

Final evidence: `PASS=14`, including required vernacular/foreign summaries, one-paragraph structure, 150-500 word range, keyword presence/position/separator/punctuation/case, 12 pt, 1.5 spacing, zero first-line indent and justified alignment.

### Cover

PR `#64`.

Final evidence: `PASS=4` for required academic cover, field order, volume on cover/title-page and optional project cover suppression.

### Title page

PR `#65`, squash-merged as `c4b7865e5857ab3195a2b4e32f7da94673a29569`.

Exact audited head before merge: `d3fb8957f50868c3334ee29c134db9b6b8a42e10`.

Required evidence:

- `Normative source contract` run `32802206747`: SUCCESS;
- `LaTeX preflight` run `32802206746`: SUCCESS;
- structural job `97665147264`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE title-page-summary PASS=7`.

Seven scoped rules passed final-PDF measurement:

- `title-page.element.required`;
- `title-page.fields.order`;
- `volume.number.cover-title-page`;
- `nature.line-spacing`;
- `nature.block.alignment`;
- `project.title-page.required`;
- `project.anonymization.policy`.

Measured highlights:

- academic title-page field order verified from final-PDF vertical geometry;
- multivolume marker independently verified on cover and title page;
- nature spacing matches same-document `singlesp` calibration;
- nature block matches the expected midpoint-to-right-margin extent within oracle tolerance;
- project and anonymized-project profiles contain required title pages;
- anonymized project suppresses secret author/advisor markers while retaining the public identifier.

A final evidence review comment is recorded directly on PR #65.

### Approval page

PR `#67`, squash-merged as `673d25252b3b526b5503309535cb423184456e35`.

Exact audited head before merge: `effeab0cbc9a6b82d2d81cf038e2656e42c603f5`.

Required evidence:

- `Normative source contract` run `32830408562`: SUCCESS;
- `LaTeX preflight` run `32830408536`: SUCCESS;
- structural job `97747584964`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE approval-summary PASS=2 academic_profiles=4 supplemental_profiles=2`.

Two scoped rules passed final-PDF measurement:

- `approval.element.required`;
- `approval.fields.order`.

Measured highlights:

- approval-page presence verified in all four applicable academic profiles: `tccgraduacao`, `tccespecializacao`, `dissertacao`, and `tese`;
- author, title/subtitle, nature, approval date and committee ordering verified from final-PDF geometry in all four profiles;
- project and anonymized-project suppression was recorded only as supplemental non-applicability/regression observation and did not determine normative PASS.

The first evidence run reported an order FAIL only for graduation/specialization because the fixture used a nature marker that occurred twice inside those generated nature strings. This was an instrumentation ambiguity, not a class defect. The marker was moved to a single-occurrence metadata position; the class implementation, normative expectation, locator, tolerance and proof-state remained unchanged.

A final unchanged-head evidence review comment is recorded directly on PR #67.

### Errata

PR `#69`, squash-merged as `5b6050b89e701e9463242de9d9948af9bb6a2687`.

Exact audited head before merge: `c1351a194e47afc5f8996d7f64fd2d31ad9d0762`.

Required evidence:

- `Normative source contract` run `32833494577`: SUCCESS;
- `LaTeX preflight` run `32833494574`: SUCCESS;
- structural job `97757168011`: SUCCESS;
- required aggregate job `97758970932`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE errata-summary PASS=3 present_pages=3 absent_pages=2`.

Three scoped rules passed final-PDF measurement:

- `errata.element.optional`;
- `errata.position`;
- `errata.contents`.

Measured highlights:

- a controlled absent fixture verified that errata is optional rather than mandatory;
- a controlled present fixture placed the errata after the title page and before a sentinel page;
- work-reference and correction markers were independently observed on the errata page;
- `page_delta=1` is retained only as a measured fixture observation; the normative position check is strictly `after=title-page` and does not strengthen the contract to require adjacency.

Before final certification, the oracle was corrected because an earlier implementation incorrectly required immediate adjacency to the title page. The correction changed only the measurement predicate; no class implementation, normative expectation, locator, tolerance or proof-state was changed.

The branch was synchronized with the then-current `main` before final certification so the required merge gate was evaluated on an up-to-date head. A final unchanged-head evidence review comment is recorded directly on PR #69.

### Optional pre-textual lists

PR `#71`, squash-merged as `961cfb41de76c192b7a703956e861c7aba88c251`.

Exact audited head before merge: `33c41dc741dfce7c110a657acdd5cf091b6f2024`.

Required evidence:

- `Normative source contract` run `32841169790`: SUCCESS;
- `LaTeX preflight` run `32841169894`: SUCCESS;
- structural job `97780773494`: SUCCESS;
- required aggregate job `97782325510`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE optional-lists-summary PASS=4 present_fixtures=4 absent_pages=1`.

Four scoped rules passed final-PDF measurement:

- `list.illustrations.optional`;
- `list.tables.optional`;
- `list.abbreviations.optional`;
- `list.symbols.optional`.

Measured highlights:

- four isolated present fixtures exercise exactly one documented public list command each;
- every present fixture exposes its corresponding heading on exactly one PDF page;
- the common absent fixture exposes none of the four headings;
- normative PASS is restricted to `required=false`; list-entry content, object generation, ordering, layout and typography are not inferred as additional requirements.

The instrumentation required two corrections before final certification. First, an illustration fixture used the standard LaTeX `figure`/`caption` path and produced an overflow; repository documentation and the canonical object regression suite show that the documented V2 object API is `\legend{...}` plus `ufcobjeto`, and object generation is outside this bounded optionality contract, so that unrelated route was removed instead of changing the class or weakening warning checks. Second, each textual control sentence repeated its list heading phrase, causing the substring-based final-PDF extractor to report a second heading page. The control text was neutralized while preserving the strict exact-one-present/zero-absent criterion.

No class/runtime implementation, normative value, locator, oracle tolerance or proof-state changed. A final unchanged-head evidence comment is recorded directly on PR #71.

### Table of contents

PR `#73`, squash-merged as `1f1feed15e2c69a067022042f26aa663447cdd9d`.

Exact audited head before merge: `f042ff99910a7e9e0fb0d3ca40cc292f047f9980`.

Required evidence:

- `Normative source contract` run `32845862671`: SUCCESS;
- `LaTeX preflight` run `32845862682`: SUCCESS;
- structural job `97795253961`: SUCCESS;
- required aggregate job `97797391157`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE toc-summary PASS=5 toc_pages=5 hierarchy_levels=5 non_normative=1`.

Five scoped normative rules passed final-PDF measurement:

- `toc.pretextual-exclusion`;
- `toc.heading.alignment`;
- `toc.heading.case`;
- `toc.page-number.position`;
- `toc.section-hierarchy.mirror`.

Measured highlights:

- controlled pre-textual markers do not appear inside the identified TOC page range;
- the `SUMÁRIO` heading is uppercase and centered with measured center delta `0.0002 pt`;
- all five controlled hierarchy page numbers terminate within `0.0041 pt` of the contract-derived right text margin;
- section through subparagraph TOC entries reproduce the corresponding body-heading font identity/family and size, with `0.0 pt` font-size delta for all five levels.

The first run stopped before PDF measurement because the initial scope filter treated every `toc.*` rule as normative and therefore included `toc.leaders.dotted.project`. Inspection confirmed that this sixth namespace member is explicitly `authority=project-policy` with `normative_claim=false`. The oracle was corrected to derive the five N6 rules from `authority=normative` while separately accounting for the one non-normative TOC policy rule. No class implementation, normative value, locator, oracle tolerance or proof-state changed.

A final exact-head certification comment is recorded directly on PR #73.

### Pre-textual pagination and start-side transition

PR `#75`, squash-merged as `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5`.

Exact audited head before merge: `b5a9f1188b8d981dbd519561cdd7e4ba446782e1`.

Required evidence:

- `Normative source contract` run `32849497792`: SUCCESS;
- `LaTeX preflight` run `32849497722`: SUCCESS;
- structural job `97806826028`: SUCCESS;
- required aggregate job `97809054286`: SUCCESS;
- structural result: `PASS=14 FAIL=0 SKIP=0`;
- `N6-EVIDENCE pretextual-pagination-summary PASS=4 duplex_pages=27 catalog_pages=3 recto_markers=13`.

Four scoped normative rules passed final-PDF measurement:

- `pagination.pretextual.counted-not-numbered`;
- `pagination.catalog-data.not-counted`;
- `pagination.textual.display-start`;
- `pretextual.start.recto`.

Measured highlights:

- all 26 physical pre-textual pages in the controlled duplex fixture expose no visible Arabic or Roman header page-number token;
- the first textual page is physical page 27 and displays Arabic page number `27`, directly matching physical/logical progression when no uncounted page is present;
- in the catalog-card fixture, the title page is physical page 1, the catalog card is physical page 2 and the first textual page is physical page 3 displaying logical page number `2`, providing final-PDF evidence that the catalog card is not counted;
- the title page and catalog card expose no visible page-number tokens;
- all 13 controlled pre-textual starts occur on odd physical pages;
- the catalog card is the immediate physical verso of the title page, satisfying the stored exception to recto starts.

The first exact-head structural run aborted before measuring any scoped rule because the original title-page marker used the author string, which legitimately appears again on the approval page. Only the controlled fixture marker was moved to the title-page-only location string `N6 Pagination Title City`. The class implementation, normative expectation, scope, locator, tolerance and proof-state remained unchanged. The final oracle also retains hardened detection for both Arabic and Roman visible header numbering.

A final exact-head certification comment is recorded directly on PR #75.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order from this checkpoint:

1. textual section hierarchy and typography dimensions;
2. quotation and paragraph dimensions;
3. citation/object dimensions;
4. post-textual dimensions;
5. deposit/distribution-related normative evidence that is actually measurable from the relevant final artifact or institutional workflow.

The immediate next bounded candidate is the existing `sections.hierarchy` ruleset identified by `normativa/locator-audit-sections-footnotes-nature.json`. Its exact three-rule scope is:

- `section.numbering.progressive`;
- `section.levels.max`;
- `section.primary.new-page`.

Before creating the evidence PR, derive and assert this scope again from the current full contract rather than relying only on the handoff. Use controlled final-PDF section markers to measure progressive numbering, the five-level ceiling and primary-section page transitions. Keep adjacent section rules separate unless their own authority/applicability and fixture design justify a later bounded component, including:

- `section.indicator.alignment`;
- `section.indicator.separator`;
- `section.primary.recto-duplex`;
- `section.primary.after-spacing`;
- `section.subsection.before-after-spacing`;
- `section.multiline.hanging`;
- `heading.unnumbered.centered`.

Do not infer those adjacent dimensions from a green `sections.hierarchy` increment.

## Required PR discipline from this checkpoint forward

Every bounded audit PR should contain, in its body or final comment:

1. stable base SHA;
2. exact head SHA used for evidence;
3. complete rule scope;
4. fixtures and measurement strategy;
5. required workflow run IDs and relevant job ID;
6. structured `N6-EVIDENCE` summary;
7. explicit statement that normative values/locators/tolerances/proof-state were not changed, unless the PR is explicitly a policy/source/proof-state PR;
8. merge only on unchanged audited head;
9. after merge, update this handoff file with the merge SHA and the next action.

If measurement exposes a class defect, do not hide it by changing the oracle. Record the `FAIL`, open an isolated implementation-fix PR, preserve the normative expectation, rerun the evidence, and only then close the bounded component.

## CTAN / release state

The original CTAN blockers have been technically remediated for v2.2.0:

- canonical package/class renamed to `abntexto-ufc`;
- the legacy package identity is retained only through the compatibility surface outside the CTAN canonical package;
- UFC coat of arms externalized from public/CTAN archives;
- CTAN archive reduced to the canonical runtime, essential documentation and portable example;
- archive/asset identity guards and allowlists are present;
- D5 distribution certification has been rehearsed on PR #36.

Do not tag or publish v2.2.0 from the rehearsal. Final D5 must be repeated on the source tree approved at N15, and D6 CTAN resubmission follows that final certification.

## How to resume in a new ChatGPT conversation

Read, in this order:

1. `docs/HANDOFF-V2.2.0.md`;
2. current `main` SHA and open PRs;
3. the latest bounded audit PR body/comments and its exact-head workflow runs;
4. `normativa/atomic-rules.json`, relevant `coverage-rules-*.json`, locator/proof policy and oracle policy only as needed for the next scope.

Do not reconstruct status primarily from old chat messages. Git history, this handoff and exact CI evidence are authoritative.

## Next action

From stable main `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5`, derive the exact `sections.hierarchy` N6 scope from the current full contract and existing bounded evidence. If it remains the three-rule set documented above, create an evidence-only PR with controlled final-PDF fixtures for progressive numbering, the five-level section ceiling and primary-section new-page behavior. Do not alter class/runtime, normative values, locators, tolerances or proof-state unless measurement independently exposes a defect requiring a separate implementation-fix PR.
