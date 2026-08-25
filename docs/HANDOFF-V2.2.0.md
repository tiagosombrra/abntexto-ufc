# abntexto-ufc v2.2.0 — Canonical Handoff

Updated: 2026-08-25

This file is the canonical continuation point for the v2.2.0 audit/release plan. Future work should read this file before relying on chat history.

## Current stable checkpoint

- Repository: `tiagosombrra/modelo-latex-ufc`
- Default branch: `main`
- Stable main after N6 approval-page merge: `673d25252b3b526b5503309535cb423184456e35`
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

## N6 remaining work

Continue with bounded, independently measurable components. Preferred order:

1. errata;
2. optional pre-textual lists;
3. table of contents;
4. remaining pre-textual/structural atomic dimensions not yet covered by N6 final-PDF evidence;
5. then move to textual, citation/object, post-textual and deposit-related evidence according to the canonical N6 scope before declaring N6 complete.

The immediate next increment is errata. Its current active contract is compact and conditional:

- `errata.element.optional`;
- `errata.position`;
- `errata.contents`.

The evidence should distinguish optional absence from valid presence. When present, it must measure placement after the title page and verify both required content parts without inventing additional normative layout dimensions.

The scenario must derive its expected rule set from the full contract and fail on scope drift, following the title-page/cover/approval pattern.

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

Create the N6 errata evidence increment from stable main `673d25252b3b526b5503309535cb423184456e35`, preserving the same evidence-only semantics used by prior bounded N6 PRs.
