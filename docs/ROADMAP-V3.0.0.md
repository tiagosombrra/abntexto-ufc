# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE at its phase-end regression candidate gate.**

Accepted closeout state:

- Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`: Static `33980847191`, Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`;
- acceptance-state synchronization checkpoint `c066697691df748a3b24a716ba69d5e4cb168f5d`;
- librarian review matrix: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Phase-end candidate contract: `docs/V3-CORE-CORRECTIONS-PHASE-END.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current correction batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | ACTIVE — PHASE-END CANDIDATE | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | Immutable candidate passes Static/full Linux with phase-specific evidence green. |
| **Reference PDF Validation** | QUEUED | Inspect the corrected canonical V3 PDF page by page against accepted UFC requirements, recovered reviews and preservation baseline. | Visual checklist and reproducible presentation evidence pass; phase-end regression green. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Core Corrections closeout state

All resolvable review corrections are accepted. Items 1-32 and 34 are PASS; item 33 remains NORMATIVE-REVIEW and fail-closed. There is no shared runtime FAIL and no PARTIAL item.

The commit that first introduces `docs/V3-CORE-CORRECTIONS-PHASE-END.md` is the immutable phase-end candidate. It must pass Static contract and full Linux integration on the same SHA. Only then may Core Corrections close.

## Gate before Reference PDF Validation

No shared runtime FAIL; all blocking correction evidence accepted; item 33 explicit/fail-closed; documentation/machine state synchronized; immutable phase-end candidate green on Static and full Linux.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation and its own phase-end regression.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
