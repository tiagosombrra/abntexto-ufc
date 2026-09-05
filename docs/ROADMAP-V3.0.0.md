# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Regression Audit is closed. The latest fully validated Core Corrections/control checkpoint is `f6ca012164273e67480dca127fe17b392e8a8a21`, with Static contract run `33939512055` and full Linux integration run `33939512019` both successful. The Linux run completed the full repository integration contract with `PASS=31 FAIL=0 SKIP=0`.

The 34-point librarian contract now stands at **24 PASS, 8 PARTIAL, 1 FAIL, 1 NORMATIVE-REVIEW**. Items 19, 20 and 23 are closed by reviewer-specific evidence in full integration. Item 17 is closed by code-typography evidence. Item 4 is closed after the advisor/co-advisor punctuation correction. Item 21 is now a classified runtime/contract FAIL rather than an unresolved authority question.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.
Object typography decision: `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`.

## Operating discipline

Every material advance must update the relevant execution documentation and the canonical handoff in the same work cycle. Phase/machine-state changes must also update this roadmap and `release/v3-roadmap.json`. Documentation reconciliation is part of the advance, not deferred cleanup.

Every phase ends with a mandatory phase-end regression on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate. At minimum, phase closeout requires Static contract, full relevant Linux integration, phase-specific acceptance evidence and recorded SHA/run results. Presentation phases additionally require canonical-PDF inspection. Final Certification additionally requires the heavy literal-font/Windows/PDF-A/distribution matrix.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Closed with 34-item contract, classified findings and green static/full-integration phase-end regression. |
| **Core Corrections** | ACTIVE | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | No unresolved shared FAIL; all blocking P0/P1 corrections have evidence; remaining normative reviews are explicit/fail-closed; phase-end regression green on one immutable SHA. |
| **Reference PDF Validation** | QUEUED | Compile the corrected canonical V3 reference and inspect it page by page against accepted UFC requirements, recovered reviews and the V2.1 preservation baseline where applicable. | Page-level visual checklist and reproducible presentation evidence pass, then phase-end regression is green. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation using the retained article authority contract. | Article runtime, modality, positive/negative evidence, canonical rendering and phase-end regression pass on the same candidate. |
| **Final Certification** | QUEUED | Run complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Complete heavy certification matrix and phase-end regression green on one immutable candidate. |
| **Release** | QUEUED | Finalize user documentation, bundles, release assets, checksums and publication actions. | No unresolved roadmap/normative item; release checklist and final release regression/verification recorded. |

## Active phase — Core Corrections

### Completed/validated work

- readable phase/control-plane migration;
- machine-protected 34-item librarian contract;
- mandatory documentation-on-material-advance governance;
- mandatory phase-end regression governance;
- advisor/co-advisor final punctuation correction;
- optional department and complete-author-name guidance improvements;
- committee institution/acronym examples;
- first textual `Universidade Federal do Ceará (UFC)` reference update;
- stale V2/current-reference vocabulary protection begun;
- explicit annex-source example added;
- long-direct-quotation locator evidence (`p. 42`);
- long-direct-quotation punctuation evidence rejecting an extraneous full stop before the parenthetical citation;
- external-illustration source locator evidence (`p. 42`);
- mixed-language engineering diagnostics cleaned in touched gates;
- full Core Corrections/control integration checkpoint green at `f6ca012...`.

### Current work — Objects

Review item 21 is the active P1 correction.

Current runtime and final-PDF tests still certify the upper illustration/table identification/title at 10 pt. Authority reconciliation is now recorded in `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`:

- upper identification/title: **12 pt**, single spacing;
- lower source/legend/note: **10 pt**, single spacing where applicable;
- all object text remains bound to object width;
- historical rule IDs must not be silently repurposed to mean the opposite value.

The implementation batch must update runtime, normative contract, locator audits and final-PDF evidence atomically. Item 21 remains FAIL until the corrected final-PDF measurements pass.

### Remaining Core Corrections after Objects

- finish canonical/visual confirmation for partial front-matter items 1, 2 and 7;
- finish sentence-case/reference examples for item 11 and item 28;
- confirm first-use UFC acronym presentation in the corrected canonical PDF (item 16);
- expand safe/current NBR 6023:2025 regression cases for items 30-32;
- keep item 33 as NORMATIVE-REVIEW until authoritative current-edition text supports the disputed edge cases;
- confirm annex external-source presentation and heading/TOC styling in the corrected canonical PDF (item 34);
- run the complete Core Corrections phase-end regression on one immutable SHA.

## Gate before Reference PDF Validation

Core Corrections closes only when:

1. all shared blocking P0/P1 corrections have implementation/reference behavior and evidence;
2. affected normative mappings and tests are updated atomically where authority changed;
3. no shared runtime FAIL remains;
4. remaining NORMATIVE-REVIEW items are explicitly fail-closed and proven non-blocking for the shared canonical output, or resolved;
5. documentation/review matrices match the candidate SHA;
6. Static contract and full Linux integration pass on the same immutable phase-end candidate;
7. required phase-specific/manual results are recorded before Reference PDF Validation becomes active.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation, including its own phase-end regression.

## Naming policy

Use descriptive work names such as `Core Corrections — Objects`, `Core Corrections — References`, `Reference PDF Validation — Pre-textual Pages`. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Retained checkpoints

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`;
- regression planning/full-integration checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`;
- reviewer evidence implementation checkpoint: `1eab2539e418224e2a6ce85ef09065941b719ef7`;
- latest fully validated Core Corrections/control checkpoint: `f6ca012164273e67480dca127fe17b392e8a8a21`.

Detailed implementation history remains in Git, pull requests, issues, workflow runs, tags and releases rather than being duplicated in active control files.
