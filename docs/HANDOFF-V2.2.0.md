# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 section-hierarchy evidence merge: `2a4b38a57bf1fafa3f4dbb9a7992340f3f03e2a8`
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
- implementation corrections discovered by evidence must be isolated in separate fix PRs;
- measured fixture observations must not silently strengthen the stored normative predicate;
- evidence PRs merge only on the exact audited head, up to date with `main`.

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

Historical baseline; do not recompute or rewrite it without an explicit proof-state phase/change.

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

## N6 completed increments

### Dedication and epigraph

PRs `#59`, `#60`, `#61`.

The first measured fixture exposed three real implementation divergences instead of masking them:

- `dedication.indent.left`: unintended +20 mm paragraph indent;
- `epigraph.short.quotation-marks`: required quotation marks missing;
- `epigraph.long.indent.left`: unintended +20 mm paragraph indent.

PR #60 corrected implementation only. PR #61 added naturally wrapped text so justification could be measured rather than inferred from explicit line breaks. Final bounded evidence passes all dedication/short-epigraph/long-epigraph dimensions, including wrapped-text alignment.

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

Exact audited head: `d3fb8957f50868c3334ee29c134db9b6b8a42e10`.

- Normative source contract `32802206747`: SUCCESS
- LaTeX preflight `32802206746`: SUCCESS
- structural job `97665147264`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE title-page-summary PASS=7`

Scoped rules:

- `title-page.element.required`
- `title-page.fields.order`
- `volume.number.cover-title-page`
- `nature.line-spacing`
- `nature.block.alignment`
- `project.title-page.required`
- `project.anonymization.policy`

### Approval page

PR `#67`, squash-merged as `673d25252b3b526b5503309535cb423184456e35`.

Exact audited head: `effeab0cbc9a6b82d2d81cf038e2656e42c603f5`.

- Normative source contract `32830408562`: SUCCESS
- LaTeX preflight `32830408536`: SUCCESS
- structural job `97747584964`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE approval-summary PASS=2 academic_profiles=4 supplemental_profiles=2`

Scoped rules:

- `approval.element.required`
- `approval.fields.order`

The first evidence run used a nature marker that appeared twice in graduation/specialization output. This was an instrumentation ambiguity, not a class defect; the marker was moved to a single-occurrence metadata position without altering implementation, expectation, locator, tolerance or proof-state.

### Errata

PR `#69`, squash-merged as `5b6050b89e701e9463242de9d9948af9bb6a2687`.

Exact audited head: `c1351a194e47afc5f8996d7f64fd2d31ad9d0762`.

- Normative source contract `32833494577`: SUCCESS
- LaTeX preflight `32833494574`: SUCCESS
- structural job `97757168011`: SUCCESS
- aggregate job `97758970932`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE errata-summary PASS=3 present_pages=3 absent_pages=2`

Scoped rules:

- `errata.element.optional`
- `errata.position`
- `errata.contents`

The first oracle incorrectly strengthened `after=title-page` into immediate adjacency. The final predicate is only `errata_page > title_page`; `page_delta` is observational.

### Optional pre-textual lists

PR `#71`, squash-merged as `961cfb41de76c192b7a703956e861c7aba88c251`.

Exact audited head: `33c41dc741dfce7c110a657acdd5cf091b6f2024`.

- Normative source contract `32841169790`: SUCCESS
- LaTeX preflight `32841169894`: SUCCESS
- structural job `97780773494`: SUCCESS
- aggregate job `97782325510`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE optional-lists-summary PASS=4 present_fixtures=4 absent_pages=1`

Scoped rules:

- `list.illustrations.optional`
- `list.tables.optional`
- `list.abbreviations.optional`
- `list.symbols.optional`

Normative PASS is restricted to `required=false`. List-entry content, object generation, ordering, layout and typography are not inferred as additional requirements.

### Table of contents

PR `#73`, squash-merged as `1f1feed15e2c69a067022042f26aa663447cdd9d`.

Exact audited head: `f042ff99910a7e9e0fb0d3ca40cc292f047f9980`.

- Normative source contract `32845862671`: SUCCESS
- LaTeX preflight `32845862682`: SUCCESS
- structural job `97795253961`: SUCCESS
- aggregate job `97797391157`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE toc-summary PASS=5 toc_pages=5 hierarchy_levels=5 non_normative=1`

Scoped normative rules:

- `toc.pretextual-exclusion`
- `toc.heading.alignment`
- `toc.heading.case`
- `toc.page-number.position`
- `toc.section-hierarchy.mirror`

The first scope filter incorrectly included non-normative `toc.leaders.dotted.project`. Final scope derives only `authority=normative` and separately accounts for the project-policy member.

### Pre-textual pagination and start-side transition

PR `#75`, squash-merged as `d1c0fd5580d172fd41863f0b67f63d6c724eb8c5`.

Exact audited head: `b5a9f1188b8d981dbd519561cdd7e4ba446782e1`.

- Normative source contract `32849497792`: SUCCESS
- LaTeX preflight `32849497722`: SUCCESS
- structural job `97806826028`: SUCCESS
- aggregate job `97809054286`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE pretextual-pagination-summary PASS=4 duplex_pages=27 catalog_pages=3 recto_markers=13`

Scoped rules:

- `pagination.pretextual.counted-not-numbered`
- `pagination.catalog-data.not-counted`
- `pagination.textual.display-start`
- `pretextual.start.recto`

Measured highlights include 26 unnumbered physical pre-textual pages, textual display starting on physical/logical page 27, a catalog-card fixture where physical page 3 displays logical page 2, all controlled pre-textual starts on recto, and the catalog card as the immediate title-page verso exception.

The first exact-head structural run used an author marker that legitimately appeared again on the approval page. Only the controlled marker was moved to the title-page-only location string `N6 Pagination Title City`; no normative or class semantics changed.

### Textual section hierarchy

PR `#77`, squash-merged as `2a4b38a57bf1fafa3f4dbb9a7992340f3f03e2a8`.

Exact audited head: `5c5db3a2e9a78bc97d252a8da9fb3bdad74577b5`.

Required evidence:

- Normative source contract `32854036704`: SUCCESS
- LaTeX preflight `32854036715`: SUCCESS
- structural job `97821531899`: SUCCESS
- aggregate `latex-preflight` job `97823695121`: SUCCESS
- structural result: `PASS=14 FAIL=0 SKIP=0`
- `N6-EVIDENCE section-hierarchy-summary PASS=3 levels=5 first_primary_page=1 second_primary_page=2`

Three scoped rules passed final-PDF measurement:

- `section.numbering.progressive`
- `section.levels.max`
- `section.primary.new-page`

Measured highlights:

- the final PDF exposes the exact controlled progressive sequence `1`, `1.1`, `1.1.1`, `1.1.1.1`, `1.1.1.1.1`, followed by primary section `2`;
- the deepest controlled/observed hierarchy depth is five; this is recorded as positive evidence only and does not claim the class prevents an unsupported sixth level;
- the complete first controlled hierarchy and its body marker remain on physical page 1 while the second primary section starts on page 2;
- `page_delta=1` is observational only; the normative predicate is only that the next primary section starts on a later page.

Instrumentation/auditability history:

- the first run stopped before normative measurement because the body control marker was emitted as `N6Omega.` while the extractor required exact `N6Omega`; only fixture punctuation changed;
- the next green run exposed a harness auditability gap: successful `N6-EVIDENCE` was surfaced only for the `pretextual` check;
- the final head changes the harness generically so every passing check that actually contains `N6-EVIDENCE` surfaces those lines in the Actions log;
- no oracle predicate, class/runtime implementation, normative value, locator, tolerance, compatibility scope or proof-state changed.

The final authoritative certification comment is recorded on PR #77.

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order from this checkpoint:

1. remaining textual section layout/typography dimensions;
2. quotation and paragraph dimensions;
3. citation/object dimensions;
4. post-textual dimensions;
5. deposit/distribution-related normative evidence that is actually measurable from the relevant final artifact or institutional workflow.

Current section-related rulesets from `normativa/locator-audit-sections-footnotes-nature.json` that remain outside the completed `sections.hierarchy` scope are:

- `sections.indicator`: `section.indicator.alignment`, `section.indicator.separator`
- `sections.primary-recto-duplex`: `section.primary.recto-duplex`
- `sections.primary-after-spacing`: `section.primary.after-spacing`
- `sections.subsection-spacing`: `section.subsection.before-after-spacing`
- `sections.multiline-hanging`: `section.multiline.hanging`
- `sections.unnumbered-centered`: `heading.unnumbered.centered`

Do not infer any of those dimensions from the green hierarchy evidence.

The immediate next bounded candidate is `sections.indicator`, with exactly two rule IDs:

- `section.indicator.alignment`
- `section.indicator.separator`

At PR creation, rederive that exact scope and the expected values from the current full contract and compatibility/source mappings. Do not hard-code expected values from this handoff. Use controlled final-PDF section headings and `pdftotext -bbox-layout` geometry/token extraction to distinguish indicator alignment from title text and to verify the stored separator predicate. Keep spacing, duplex recto behavior, multiline hanging and typography outside this increment.

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

## M1 state

Implementation is complete through PR #19:

- Node 24 migration;
- `configure-pages` v6;
- `upload-pages-artifact` v5;
- `deploy-pages` v5;
- repository `has_pages=true`.

M1 is not formally `DONE` until explicit Pages/runtime/deployment evidence is reviewed and recorded. Do not conflate implementation completion with closure evidence.

## Open release-adjacent items

- PR #36 remains D5 distribution rehearsal only; do not merge/publish it as final v2.2.0 release certification.
- Issue #18 remains open for bit-reproducible PDF differences (`CreationDate`, `ModDate`, PDF `/ID`) even though pages/text/fonts/images were identical; reassess release-blocking status under the final public bundle policy later.
- D5 final remains blocked by N15.
- D6 CTAN resubmission remains blocked by final D5.

## How to resume in a new ChatGPT conversation

Read, in this order:

1. `docs/HANDOFF-V2.2.0.md`;
2. current `main` SHA and open PRs;
3. the latest bounded audit PR body/comments and its exact-head workflow runs;
4. `normativa/atomic-rules.json`, relevant `coverage-rules-*.json`, locator/proof policy and oracle policy only as needed for the next scope.

Do not reconstruct status primarily from old chat messages. Git history, this handoff and exact CI evidence are authoritative.

## Next action

From stable main `2a4b38a57bf1fafa3f4dbb9a7992340f3f03e2a8`, rederive `sections.indicator` from the current full contract and locator mappings. If it remains exactly `section.indicator.alignment` plus `section.indicator.separator`, create an evidence-only N6 PR with controlled final-PDF section headings. Measure only the stored alignment and separator predicates. Do not absorb spacing, duplex recto behavior, multiline hanging, unnumbered-heading centering, class/runtime changes, normative values, locators, tolerances or proof-state into that evidence increment.
