# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-04

## Current status

**Core Corrections is ACTIVE.**

Regression Audit closed after the machine-protected 34-item review contract, the additional regression findings, the readable control-plane migration, and the full regression CI baseline were established. Static contract run `33937439818` and Linux integration run `33937439846` both passed on checkpoint `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.

Machine authority: `release/v3-roadmap.json`.
Closed audit: `docs/V3-REGRESSION-AUDIT.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review contract: `docs/UFC-LIBRARIAN-REVIEW.md`.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Closed with a green static/full-integration baseline and explicit classification of all findings. |
| **Core Corrections** | ACTIVE | Correct shared runtime, template, normative mapping, documentation, and tests identified by the audit. | No unresolved shared `FAIL`; no `NORMATIVE-REVIEW` is silently encoded as runtime behavior; all shared P0/P1 corrections have evidence. |
| **Reference PDF Validation** | QUEUED | Compile the canonical V3 reference and inspect it page by page against accepted UFC requirements, recovered reviews, and the V2.1 preservation baseline where applicable. | Visual checklist passes and every presentation correction has reproducible evidence. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime, modality, positive/negative evidence, and canonical rendering pass. |
| **Final Certification** | QUEUED | Run the complete profile/engine/font/Unicode/embedding/PDF-A/distribution matrix on one immutable candidate. | Complete certification matrix is green on the same candidate SHA. |
| **Release** | QUEUED | Finalize user documentation, bundles, release assets, checksums, and publication steps. | Release checklist complete with no unresolved roadmap or normative item. |

## Active phase — Core Corrections

Work follows `docs/V3-CORRECTION-PLAN.md`. Corrections are grouped by behavior rather than historical opaque identifiers.

### Shared front matter and institutional metadata

- make optional department/unit guidance explicit without creating phantom lines;
- use a complete-author-name placeholder;
- preserve subtitle propagation and optional co-advisor behavior;
- correct title-page advisor/co-advisor final punctuation;
- preserve concentration-area behavior for master's/doctoral profiles;
- demonstrate `Instituição (sigla)` for committee members where applicable;
- retain variable committee size and CAPES guidance;
- re-measure summary/list/TOC placement in the corrected canonical PDF.

### Body structure, citations and reference-guide hygiene

- remove stale V2 wording and retired public API vocabulary from the V3 reference;
- demonstrate first use of Universidade Federal do Ceará (UFC) in body text;
- preserve current NBR 10520 capitalization;
- add direct-quotation locator and punctuation evidence without inventing locators for synthetic fixtures;
- preserve alínea/subalínea and paragraph-indentation behavior;
- correct sentence-case examples where the reviewed cases apply.

### Figures, tables and documentary objects

The current implementation and tests conflate the upper identification/title with lower source/legend/note typography. The recovered review requests 12 pt for the upper title, while the current machine contract certifies reduced size. This is a real authority conflict.

Do not change object-title size merely to make the review look satisfied. First split the semantic contract and reconcile current authority. Source, legend, note, object width, single spacing, and page-locator guidance must remain separately testable.

### References and NBR 6023:2025

Current-edition authority has precedence over older template-review examples. Expand fixtures for unambiguous cases, but keep DOI/availability/repeated-author/corporate-author disputes fail-closed until current NBR 6023:2025 evidence supports the decision.

### Appendices and annexes

- preserve direct `APÊNDICE A` / `ANEXO A` flow;
- preserve heading/TOC presentation;
- demonstrate an explicit `Fonte:` for external annex material.

## First correction batch

The initial Core Corrections batch is intentionally bounded to unambiguous behavior/reference defects:

- advisor/co-advisor final punctuation plus final-PDF assertion;
- optional department and complete-name canonical placeholders;
- institution/acronym examples for committee members;
- first-use UFC acronym introduction;
- replacement of retired V2/public-API wording;
- explicit source guidance for annexes;
- long-quotation locator guidance;
- source-level reference-guide hygiene that prevents those regressions from returning.

It does not modify disputed object-title typography or disputed NBR 6023:2025 runtime.

## Gate before Reference PDF Validation

Core Corrections closes only when:

1. all shared P0/P1 corrections have runtime/reference behavior and evidence;
2. affected normative mappings and tests have been updated atomically where authority changed;
3. no shared `FAIL` remains;
4. every remaining `NORMATIVE-REVIEW` is either resolved or explicitly non-blocking for the canonical shared output, with rationale;
5. Linux integration is green on the corrected shared foundation.

## Gate before Scientific Article

Scientific Article starts only after:

1. Core Corrections is closed;
2. the canonical V3 reference PDF passes page-level visual validation;
3. no unexplained visual regression remains against the accepted V2.1 preservation baseline;
4. the corrected foundation has a green integration checkpoint.

## Naming policy

Use descriptive names such as `Core Corrections — Front Matter`, `Core Corrections — Objects`, `Core Corrections — References`, and `Reference PDF Validation — Pre-textual Pages`. Do not create new nested letter/number work identifiers. Issue/PR numbers and immutable SHAs provide traceability.

## Retained checkpoints

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`;
- regression planning/full-integration checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`.

Detailed history remains in Git, pull requests, issues, workflow runs, tags, and releases rather than being duplicated in the active roadmap.
