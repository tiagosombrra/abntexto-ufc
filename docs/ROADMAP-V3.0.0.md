# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Regression Audit is closed. Core Corrections validated checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and full Linux `33965794519` with `PASS=31 FAIL=0 SKIP=0`.

That regression closes the object-typography correction. Review item 21 is now PASS: illustration/table/object upper identification/title is 12 pt, lower source/legend/note remains 10 pt where applicable, and the final-PDF plus IBGE table evidence is green.

Current implementation checkpoint `c464a1bc2ca04a4ce398878f25e9521f5840d48e` adds explicit canonical-reference source regressions for librarian items 11, 16 and 28. The next synchronized branch checkpoint must pass Static/full Linux before this batch advances to generated-PDF text evidence.

Current 34-point state: **25 PASS / 8 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.
Object typography decision: `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`.

## Operating discipline

Every material advance must update the relevant execution documentation and canonical handoff in the same work cycle. Phase/machine-state changes also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory phase-end regression on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Closed with 34-item contract, classified findings and green Static/full Linux phase-end regression. |
| **Core Corrections** | ACTIVE | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | No unresolved shared FAIL; blocking P0/P1 evidence complete; authority gaps explicit/fail-closed; phase-end regression green on one immutable SHA. |
| **Reference PDF Validation** | QUEUED | Compile the corrected canonical V3 reference and inspect it page by page against accepted UFC requirements, recovered reviews and V2.1 preservation baseline where applicable. | Page-level visual checklist and reproducible presentation evidence pass, then phase-end regression green. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation using the retained article authority contract. | Article runtime, modality, positive/negative evidence, canonical rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Run complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Complete heavy certification matrix and phase-end regression green on one immutable candidate. |
| **Release** | QUEUED | Finalize user documentation, bundles, release assets, checksums and publication actions. | No unresolved roadmap/normative item; release checklist and final regression/verification recorded. |

## Active phase — Core Corrections

### Completed/validated work

- readable phase/control-plane migration;
- machine-protected 34-item librarian contract;
- mandatory documentation-on-material-advance and phase-end regression governance;
- advisor/co-advisor final punctuation;
- optional department/full-name guidance improvements;
- committee institution/acronym examples;
- first textual UFC full-name reference update;
- stale V2/current-reference vocabulary protection;
- annex-source example;
- reviewer-specific long-direct-quotation locator/punctuation evidence;
- external-illustration source locator evidence;
- code/body typography consistency evidence;
- object typography authority/runtime/test migration accepted by Static `33965794475` + Linux `33965794519`.

### Current work — Canonical Reference Content

Implementation checkpoint `c464a1b...` protects source-level reviewed content for:

- item 11 — object-title sentence case;
- item 16 — first body-text `Universidade Federal do Ceará (UFC)`;
- item 28 — heading sentence case and `etc.` punctuation.

Current gate:

1. publish synchronized documentation/control state on top of `c464a1b...`;
2. run normal Static and full Linux integration;
3. if green, add PDF-text assertions in `tests/integration/reference-corpus.sh` for the same reviewed requirements;
4. reclassify only when generated-PDF evidence supports closure.

### Remaining Core Corrections

- canonical confirmation for partial front-matter items 1, 2 and 7;
- safe/current NBR 6023:2025 regression expansion for items 30-32;
- keep item 33 as NORMATIVE-REVIEW until authoritative current-edition evidence exists;
- canonical annex external-source/heading/TOC confirmation for item 34;
- complete Core Corrections phase-end regression on one immutable SHA.

## Gate before Reference PDF Validation

Core Corrections closes only when:

1. all shared blocking P0/P1 corrections have implementation/reference behavior and evidence;
2. affected normative mappings/tests are updated atomically where authority changed;
3. no shared runtime FAIL remains;
4. remaining NORMATIVE-REVIEW items are explicitly fail-closed and non-contradictory to the canonical shared output, or resolved;
5. documentation/review matrices match the candidate SHA;
6. Static contract and full Linux integration pass on the same immutable phase-end candidate;
7. required phase-specific/manual results are recorded before Reference PDF Validation becomes active.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation, including its own phase-end regression.

## Naming policy

Use descriptive work names such as `Core Corrections — Canonical Reference Content`, `Core Corrections — References`, `Reference PDF Validation — Pre-textual Pages`. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Retained checkpoints

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`;
- regression planning/full-integration checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`;
- reviewer evidence implementation checkpoint: `1eab2539e418224e2a6ce85ef09065941b719ef7`;
- validated object/Core Corrections checkpoint: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`;
- canonical-reference source evidence implementation: `c464a1bc2ca04a4ce398878f25e9521f5840d48e` (synchronized branch acceptance pending).

Detailed history remains in Git, pull requests, issues, workflow runs, tags and releases rather than being duplicated in active control files.
