# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Reference PDF Validation is ACTIVE.**

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, with Static `33982156041` and full Linux `33982156042` both successful. Linux summary: `PASS=31 FAIL=0 SKIP=0`.

The librarian review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 is an explicit authority gap and remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Core Corrections closure record: `docs/V3-CORE-CORRECTIONS-PHASE-END.md`.
Active presentation-validation contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current work, artifact provenance, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | Candidate `5f67560a...` passed Static `33982156041` and Linux `33982156042`. |
| **Reference PDF Validation** | ACTIVE | Inspect the corrected canonical V3 PDF page by page against accepted UFC requirements, recovered reviews and preservation baseline. | Provenance-bound canonical PDF, complete visual checklist, reproducible presentation evidence and green phase-end regression. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Core Corrections closure state

All resolvable review corrections are accepted. Items 1-32 and 34 are PASS; item 33 remains NORMATIVE-REVIEW and fail-closed. No PARTIAL or shared runtime FAIL remains.

The accepted phase-end candidate `5f67560a...` used the required machine sentinel `phase_end_regression.candidate = one-immutable-sha`. Static `33982156041` and full Linux `33982156042` passed on the same immutable SHA, satisfying the phase-transition contract.

## Active phase — Reference PDF Validation

The phase validates actual rendered presentation, not merely source semantics. The canonical PDF must be a real LaTeX build with recorded Git/environment provenance. Every page must be rendered and inspected.

Primary review groups:

- artifact provenance and preflight;
- cover, title and approval pages;
- remaining pre-textual pages and TOC/lists;
- main-text typography, headings, citations, quotations and lists;
- figures, tables, code, algorithms and equations;
- references;
- appendices, annexes and index;
- global visual quality, pagination and page-side behavior.

Presentation-sensitive librarian items 10, 15, 21 and 34 receive explicit visual reconfirmation. Canonical examples for 1, 2, 7, 11, 16 and 28 are also checked in the rendered artifact.

If a visual defect is discovered, classify it before changing runtime/reference content. Rebuild and re-render after every correction.

## Gate before Scientific Article

Scientific Article starts only after the corrected canonical V3 reference PDF has accepted provenance, the complete page-level visual checklist contains no unexplained FAIL, presentation evidence is reproducible, documentation is synchronized, and one immutable Reference PDF Validation candidate passes Static plus full Linux.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
