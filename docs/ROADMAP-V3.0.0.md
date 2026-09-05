# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-04

## Current status

**Regression Audit is ACTIVE.**

The previously planned scientific-article runtime implementation is intentionally deferred. At the regression entry checkpoint it had not started, so there is no partial runtime work to preserve. The shared V3 foundation is being revalidated first against current implementation, current normative authority, the canonical rendered PDF, and the recovered librarian review evidence.

Machine authority: `release/v3-roadmap.json`.
Detailed audit: `docs/V3-REGRESSION-AUDIT.md`.
Librarian review contract: `docs/UFC-LIBRARIAN-REVIEW.md`.

## Why the roadmap was reset

The repository has strong engineering and certification infrastructure, but the regression found that internal consistency and green tests were not sufficient to guarantee that every encoded presentation rule matched the recovered institutional review. It also found stale V2-era wording and retired profile vocabulary inside the current V3 reference document.

The reset therefore places foundation verification and correction ahead of new feature work.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | ACTIVE | Revalidate the shared V3 foundation and classify every recovered review requirement and newly discovered defect. | Every finding has an authority classification, owning surface, correction decision, and acceptance evidence plan. |
| **Core Corrections** | QUEUED | Correct shared runtime, template, normative mapping, documentation, and tests identified by the audit. | No unresolved shared `FAIL`; no `NORMATIVE-REVIEW` is silently encoded as runtime behavior. |
| **Reference PDF Validation** | QUEUED | Compile the canonical V3 reference and inspect it page by page against the accepted UFC requirements, the recovered reviews, and the V2.1 visual baseline where behavior should have been preserved. | Visual checklist passes; every presentation correction has reproducible evidence. |
| **Scientific Article** | QUEUED | Implement the article profile using the already reconstructed article authority contract after the shared foundation is stable. | Article runtime, modality, positive/negative evidence, and canonical article rendering pass. |
| **Final Certification** | QUEUED | Re-run the full profile/engine/font/Unicode/embedding/PDF-A/distribution matrix on one immutable corrected candidate. | Complete certification matrix is green on the same candidate SHA. |
| **Release** | QUEUED | Finalize user documentation, bundles, release assets, checksums, and publication steps. | Release checklist is complete and no roadmap/normative item remains unresolved. |

## Active phase — Regression Audit

### Control plane

- confirm branch/HEAD and canonical state agreement;
- replace history-heavy active-state prose with the readable phase model;
- keep only immutable checkpoints that are still required to validate the current product;
- preserve old implementation history in Git, PRs, issues, releases, and tags instead of the active roadmap.

### Normative authority

- reconfirm current UFC institutional sources and applicable ABNT editions;
- map all 34 librarian-review items through the project precedence policy;
- distinguish title, legend, source, and note typography instead of treating every object text element as one undifferentiated caption rule;
- reconcile disputed NBR 6023:2025 reference cases before changing bibliography runtime.

### Front matter

- optional department/unit presentation;
- complete-author-name guidance;
- subtitle propagation;
- advisor/co-advisor punctuation;
- concentration-area behavior;
- committee size and institution/acronym presentation;
- summary, lists, and table-of-contents positioning.

### Text and structure

- body spacing and first-line indentation;
- heading capitalization;
- first-use acronym presentation;
- alíneas and subalíneas;
- long quotations and citation punctuation;
- appendices and annexes.

### Objects

- title versus legend/source/note typography;
- single spacing;
- real object-width binding;
- source/page-locator guidance;
- figures, charts, tables, code, and algorithms.

### References

- current NBR 6023:2025 compatibility layer;
- thesis/dissertation cases;
- unknown place/publisher data for online resources;
- standards and multivolume works;
- DOI/URL/availability cases;
- repeated-author and institutional-author cases.

### Tests and rendered evidence

- retain current source/repository/test-surface contracts;
- protect all 34 librarian-review items from disappearing from the plan;
- add rule-specific positive and negative fixtures as corrections are made;
- use the canonical V3 PDF as the visual acceptance artifact for presentation rules.

## Initial review matrix

The first machine-protected pass over the 34 recovered review requirements reports:

- `PASS`: 19
- `PARTIAL`: 11
- `FAIL`: 1
- `NORMATIVE-REVIEW`: 3

These are audit states, not completion statistics. A `PASS` remains subject to final rendered verification when the requirement is visual.

The direct implementation defect already identified is the title-page advisor punctuation. Partial items include reference/template communication gaps such as the optional department, complete-name placeholder, committee institution acronym, source-page guidance, selected heading examples, bibliography edge-case fixtures, and annex-source guidance.

The audit also found defects outside the 34 review items, including stale V2 wording in the current V3 reference guide and a retired Portuguese profile value (`tccgraduacao`) still described in the V3 introduction.

## Current normative clarification: object text

The current UFC normalisation page states that its guides remain the institutional requirements and track applicable ABNT standards. The current academic-work guide distinguishes the upper identification/title of an illustration from its source, legend, and notes. It requires the identification/title to use single spacing and requires page location in the source when the illustration is not author-produced. Its general typography rule reserves the smaller uniform size recommendation for long quotations, footnotes, pagination, catalog-card data, legends, and illustration/table sources.

The current V3 implementation instead applies `\abntsmall` to the entire object title box, and the machine catalog currently maps `illustration-caption` and `table-caption` into the 10 pt reduced-size policy. Combined with the recovered librarian markings on object titles, this mapping must be re-audited in **Core Corrections** rather than accepted merely because current tests are green.

## Required gates before Core Corrections

Regression Audit closes only when:

1. the 34-point review contract is complete and machine-protected;
2. all additional regression findings are listed;
3. current authority is identified for every normative dispute that affects shared runtime;
4. the current full integration suite is green or every failure is classified as a regression finding;
5. the control plane consistently reports this readable phase model.

## Required gates before Scientific Article

Scientific Article starts only after:

1. shared Core Corrections are complete;
2. the 34-point contract has no unexplained shared `FAIL` or `NORMATIVE-REVIEW` state;
3. stale V2/reference-vocabulary defects are removed;
4. the canonical V3 reference PDF passes page-level visual validation;
5. the corrected foundation has a green integration baseline.

## Naming policy

New work packages use descriptive names such as:

- `Regression Audit — Front Matter`
- `Regression Audit — Objects`
- `Core Corrections — References`
- `Reference PDF Validation — Pre-textual Pages`
- `Scientific Article — Runtime Profile`

Do not create new opaque nested identifiers. Issue/PR numbers and immutable SHAs provide traceability without making the roadmap unreadable.

## Retained certified checkpoints

Only checkpoints that still matter to the current plan remain in the active roadmap:

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article source-contract closeout / pre-runtime predecessor: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`.

Detailed historical milestones remain available from Git history, pull requests, issues, workflow runs, tags, and releases. They are intentionally not duplicated in this active roadmap.
