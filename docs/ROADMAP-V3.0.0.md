# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE.**

Accepted checkpoints:

- object/Core: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`, Static `33965794475`, Linux `33965794519`;
- canonical reference content: `c4c59f83b67cb152ed9a88345541457b8f18021c`, Static `33969505681`, Linux `33969505614`;
- engineering-language hardening: `edeb14b7a96d1cab3ad9551701087ddf4dff059a`, Static `33972111694`, Linux `33972111696`;
- bounded reference evidence: `bcd851b3176b516091a254bc57b5ae4e8add9358`, Static `33974062993`, Linux `33974063103`, `PASS=31 FAIL=0 SKIP=0`.

Current review state is **29 PASS / 4 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. The remaining PARTIAL items are 1, 2, 7 and 34.

Current closeout evidence began at implementation `33bdd0bd5f9360c645b4166071c32dbba6c647f0`. Synchronized checkpoint `48e7e6841b63ea62d6811e734dde09931b8f608c` failed Static `33980486317` because a newly added project-owned error diagnostic contained the prohibited Portuguese technical term `pre-textual`. Correction `dc381d4517341062d53ae5e93082c7856fc4af17` changes only that diagnostic wording to engineering English. Evidence predicates and runtime are unchanged.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current correction batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | 34-item contract plus green Static/full Linux phase-end regression. |
| **Core Corrections** | ACTIVE | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | No unresolved shared FAIL; blocking evidence complete; authority gaps explicit/fail-closed; phase-end regression green on one immutable SHA. |
| **Reference PDF Validation** | QUEUED | Inspect the corrected canonical V3 PDF page by page against accepted UFC requirements, recovered reviews and preservation baseline. | Visual checklist and reproducible presentation evidence pass; phase-end regression green. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Active phase — Core Corrections

### Validated work

- readable control plane and machine-protected 34-item review contract;
- documentation-on-material-advance and phase-end regression governance;
- front-matter advisor/co-advisor and committee foundations;
- citation/locator/body/list corrections and evidence;
- object typography authority/runtime/evidence;
- canonical source/PDF evidence for items 11, 16 and 28;
- engineering-language hardening accepted at `edeb14...`;
- bounded bibliography evidence for items 30-32 accepted at `bcd851b...`, leaving item 33 fail-closed.

### Current work — Front Matter and Annex Closeout

Evidence scope:

1. item 1 — academic cover blank department omitted / filled department rendered;
2. item 2 — canonical complete-author-name placeholder rendered in generated output;
3. item 7 — approval-page committee institution preserved in `Instituição (sigla)` form;
4. item 34 — canonical annex source attribution, heading presence and TOC entry, combined with independent bold-heading final-PDF evidence.

Current failure classification:

- Static `33980486317`: engineering-language guard failure only; new item-2 diagnostic used `pre-textual`;
- correction `dc381d4517341062d53ae5e93082c7856fc4af17`: diagnostic wording only, no predicate/runtime change;
- corrected synchronized Static/full Linux acceptance pending.

If corrected CI is green and all four items emit PASS, update to **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

### Core Corrections closeout after item acceptance

Do not close the phase immediately after targeted evidence passes. Create a separate immutable Core Corrections phase-end candidate with all documentation synchronized. Run Static contract, full Linux integration and all phase-specific acceptance checks on that same SHA. Only a green recorded result can close Core Corrections and activate Reference PDF Validation.

## Gate before Reference PDF Validation

No shared runtime FAIL; all blocking P0/P1 corrections have evidence; item 33 is explicit, non-contradictory and fail-closed; documentation/machine state match the candidate; one immutable candidate passes the complete Core Corrections phase-end regression.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation and its own phase-end regression.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
