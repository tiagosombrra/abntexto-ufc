# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Regression Audit is closed. Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and Linux `33965794519`, closing review item 21.

Canonical-reference source checkpoint `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f` passed Static `33968579418` and Linux `33968579449`. Generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` then passed Static `33969505681` and full Linux `33969505614`, with `PASS=31 FAIL=0 SKIP=0`, closing review items 11, 16 and 28.

Current 34-point state is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Current implementation checkpoint `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` starts **Core Corrections — Engineering Language Evidence Hardening**. It strengthens mixed-language diagnostic detection and translates known project-owned mixed diagnostics. Synchronized Static/full Linux acceptance is pending.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.
Engineering language policy: `docs/ENGINEERING-LANGUAGE.md`.
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
- object typography authority/runtime/test migration accepted by Static `33965794475` + Linux `33965794519`;
- source-level reviewed reference-content evidence for items 11, 16 and 28 accepted at `3ae9dd...`;
- generated-PDF reviewed reference-content evidence for items 11, 16 and 28 accepted at `c4c59...` with Static `33969505681` + Linux `33969505614`.

### Current work — Engineering Language Evidence Hardening

The permanent engineering-language gate had a false-negative class: mixed Portuguese/English project-owned diagnostics could remain while the static audit reported zero violations.

Implementation `5d74c0c...`:

- adds high-confidence mixed-language phrase detection to `tests/checks/engineering_language.py`;
- extends the self-test to 11 cases, including known former false negatives;
- translates mixed project-owned diagnostics in `tests/integration/multivolume.sh`;
- translates mixed project-owned diagnostics in `tests/integration/references-6023.sh`;
- keeps academic/rendered Portuguese, bibliography data and official wording protected.

Acceptance gate:

1. publish a synchronized branch checkpoint containing `5d74c0c...` and current control docs;
2. run normal Static and full Linux integration;
3. if the stronger detector finds additional project-owned mixed diagnostics, correct them rather than weakening the detector;
4. close the finding only when Static/full Linux are green and the permanent audit truthfully reports zero violations.

### Remaining Core Corrections

- canonical confirmation for partial front-matter items 1, 2 and 7;
- safe/current NBR 6023:2025 regression expansion for items 30-32;
- keep item 33 as NORMATIVE-REVIEW until authoritative current-edition evidence exists;
- canonical annex external-source/heading/TOC confirmation for item 34;
- complete Core Corrections phase-end regression on one immutable SHA.

## Gate before Reference PDF Validation

Core Corrections closes only when all shared blocking P0/P1 corrections have implementation/reference behavior and evidence, affected normative mappings/tests are updated atomically where authority changed, no shared runtime FAIL remains, remaining NORMATIVE-REVIEW items are explicitly fail-closed/non-contradictory or resolved, documentation/review matrices match the candidate SHA, and Static plus full Linux pass on the same immutable phase-end candidate.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation, including its own phase-end regression.

## Naming policy

Use descriptive work names such as `Core Corrections — Engineering Language Evidence Hardening`, `Core Corrections — References`, `Reference PDF Validation — Pre-textual Pages`. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Retained checkpoints

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression `main` baseline: `c4bf51b574647226ee488440579ec2a204c16c79`;
- regression planning/full-integration checkpoint: `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2`;
- accepted object/Core Corrections checkpoint: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`;
- accepted canonical-reference source checkpoint: `3ae9dd698e021a117ba2b64ebf970dc8c507fa8f`;
- accepted canonical-reference PDF checkpoint: `c4c59f83b67cb152ed9a88345541457b8f18021c`;
- engineering-language hardening implementation: `5d74c0c5b85ec501b04c5050af81180ad7e3f2ee` (branch acceptance pending).

Detailed history remains in Git, pull requests, issues, workflow runs, tags and releases rather than being duplicated in active control files.
