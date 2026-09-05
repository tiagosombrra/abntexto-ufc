# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Regression Audit is closed. Object/Core Corrections checkpoint `3f47081cbbd00a44b9ee86a6b406580e79b593c0` passed Static `33965794475` and Linux `33965794519`, closing review item 21. Canonical-reference generated-PDF checkpoint `c4c59f83b67cb152ed9a88345541457b8f18021c` passed Static `33969505681` and full Linux `33969505614`, with `PASS=31 FAIL=0 SKIP=0`, closing review items 11, 16 and 28.

Current 34-point state is **28 PASS / 5 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Engineering-language hardening remains active. Static `33971849196` on synchronized checkpoint `0818bc2c5f50f6f1c60d4cef98d1c85031cb2fcd` passed repository and phase-governance checks, then exposed five remaining project-owned Portuguese diagnostics in `tests/integration/backmatter.sh`. Current implementation `a1c139a6efa8bacefcd3294f01b1f7ed3447a8dd` translates that complete diagnostic surface and normalizes its technical job identifier while retaining Portuguese academic literals under test. Acceptance requires a synchronized Static/full Linux checkpoint.

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
- advisor/co-advisor punctuation, optional-department/full-name guidance, committee acronym examples and UFC first-use correction;
- long-quotation and external-source locator/punctuation evidence;
- code/body typography consistency evidence;
- object typography authority/runtime/test migration accepted through `3f47081...`;
- source and generated-PDF reference-content evidence for items 11, 16 and 28 accepted through `c4c59...`.

### Current work — Engineering Language Evidence Hardening

The detector is intentionally fail-closed and is being used to discover old evidence debt. Successive Static runs exposed `algorithm-numbering.sh`, then documentation-governance drift, then catalog-card/duplex/vector diagnostics, and most recently the back-matter diagnostic surface. The rule is to translate the complete related engineering surface rather than suppress the first reported token.

Current implementation `a1c139...` corrects the back-matter surface. Acceptance gate:

1. publish a synchronized documentation checkpoint on top of `a1c139...`;
2. run Static and full Linux integration on that exact checkpoint;
3. require zero project-owned Portuguese technical diagnostics;
4. if more violations appear, clean the complete related engineering surface and update the control plane again;
5. close the language finding only when Static/full Linux are green and accepted evidence is recorded.

### Remaining Core Corrections

- canonical confirmation for partial front-matter items 1, 2 and 7;
- safe/current NBR 6023:2025 regression expansion for items 30-32;
- keep item 33 as NORMATIVE-REVIEW until authoritative current-edition evidence exists;
- canonical annex external-source/heading/TOC confirmation for item 34;
- complete Core Corrections phase-end regression on one immutable SHA.

## Gate before Reference PDF Validation

Core Corrections closes only when all shared blocking P0/P1 corrections have implementation/reference behavior and evidence, affected normative mappings/tests are updated atomically where authority changed, no shared runtime FAIL remains, remaining NORMATIVE-REVIEW items are explicit/fail-closed or resolved, documentation/review matrices match the candidate SHA, and Static plus full Linux pass on the same immutable phase-end candidate.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation, including its own phase-end regression.

## Naming policy

Use descriptive work names such as `Core Corrections — Engineering Language Evidence Hardening`, `Core Corrections — References`, and `Reference PDF Validation — Pre-textual Pages`. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.

## Retained checkpoints

- certified non-article foundation: `c79f3c73f1d51a30175e8259269504d029442a1c`;
- article source-contract implementation: `4d018a92697e8f39e3a53b034c451e55996c84fb`;
- article pre-runtime checkpoint: `7a7562d23e8bf6c92abb635718639d617a2ed6ff`;
- pre-regression main baseline: `c4bf51b574647226ee488440579ec2a204c16c79`;
- accepted object/Core checkpoint: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`;
- accepted canonical-reference PDF checkpoint: `c4c59f83b67cb152ed9a88345541457b8f18021c`;
- latest synchronized language discovery checkpoint: `0818bc2c5f50f6f1c60d4cef98d1c85031cb2fcd`;
- current language-hardening implementation: `a1c139a6efa8bacefcd3294f01b1f7ed3447a8dd` (acceptance pending).
