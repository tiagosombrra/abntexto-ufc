# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Regression Audit is closed. Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and Linux `33965794519`, closing review item 21.

Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, with `PASS=31 FAIL=0 SKIP=0`, closing review items 11, 16 and 28.

Current 34-point state is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Engineering-language hardening remains active. Static `33970711005` exposed a previously missed diagnostic in `algorithm-numbering.sh`. Static `33970988780` exposed documentation-governance drift caused by a shortened roadmap; the required governance wording was restored. Static `33971156481` then passed phase governance and exposed four further project-owned Portuguese diagnostics in `catalog-card.sh`, `duplex-backmatter.sh`, `table-ibge-vector-evidence.sh`, and `vector-rule-validation.sh`.

Current implementation checkpoint `1129935fe5e4f97d6fe3798fd5e4777760f0d61b` translates those newly exposed engineering diagnostics and expands the permanent language self-test to 18 cases. It awaits a synchronized Static/full Linux acceptance checkpoint.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.
Engineering language policy: `docs/ENGINEERING-LANGUAGE.md`.
Object typography decision: `docs/V3-OBJECT-TYPOGRAPHY-DECISION.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current correction batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

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
- source and generated-PDF reviewed reference-content evidence for items 11, 16 and 28 accepted through `c4c59...`.

### Current work — Engineering Language Evidence Hardening

The detector is intentionally being strengthened fail-closed. Each newly exposed diagnostic is treated as evidence debt, not as a reason to weaken the language policy.

Current progression:

1. `fd3727...` / Static `33970711005` exposed `algorithm-numbering.sh`;
2. `6c23a49...` / Static `33970988780` exposed temporary documentation-governance drift, which was corrected;
3. `da7fbf7...` / Static `33971156481` confirmed governance recovery and exposed four additional old diagnostic surfaces;
4. implementation `1129935...` translates those surfaces and expands the self-test to 18 cases.

Acceptance gate:

1. publish a synchronized documentation checkpoint on top of `1129935...`;
2. run normal Static and full Linux integration on the same checkpoint;
3. require zero project-owned Portuguese technical diagnostics and a green detector self-test;
4. if stronger detection exposes more violations, clean the complete related engineering surface;
5. close the finding only when Static/full Linux are green and control documents record the accepted SHA/runs.

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
- accepted object/Core Corrections checkpoint: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`;
- accepted canonical-reference PDF checkpoint: `c4c59f83b67cb152ed9a88345541457b8f18021c`;
- language-hardening discovery checkpoint: `fd3727d89848eb52a9c79021cd9765ad9e1806db`;
- governance-recovery checkpoint with additional language discovery: `da7fbf7614ed8e50ee600bf010db7ecd3694f310`;
- current language-hardening implementation: `1129935fe5e4f97d6fe3798fd5e4777760f0d61b` (acceptance pending).
