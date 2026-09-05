# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Reference PDF Validation is ACTIVE — fresh canonical artifact build in progress.**

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, with Static `33982156041` and full Linux `33982156042` successful; Linux summary `PASS=31 FAIL=0 SKIP=0`.

The librarian review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 is an explicit authority gap and remains fail-closed pending authoritative current NBR 6023:2025 evidence.

The pre-existing 2026-09-04 PDF is not admissible as the current canonical artifact because rendered content predates accepted Core Corrections. A temporary TeX Live 2026 build workflow is active to produce a provenance-bound replacement.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Active presentation-validation contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current work, artifact provenance, temporary-executor lifecycle, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | Candidate `5f67560a...` passed Static `33982156041` and Linux `33982156042`. |
| **Reference PDF Validation** | ACTIVE — CANONICAL REBUILD | Inspect the corrected canonical V3 PDF page by page against accepted UFC requirements, recovered reviews and preservation baseline. | Provenance-bound canonical PDF, complete visual checklist, reproducible presentation evidence, temporary executor removed and green phase-end regression. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Active phase — Reference PDF Validation

Current artifact work:

- reject the 2026-09-04 PDF as stale acceptance evidence;
- build `template/main.tex` from the current remote branch with TeX Live 2026/pdfLaTeX;
- record Git SHA, workflow run, SHA-256 and `pdfinfo`;
- download the artifact;
- remove `.github/workflows/tmp-reference-pdf.yml` immediately after artifact recovery;
- preflight/render every page at 200 DPI and perform the complete visual checklist.

Presentation-sensitive librarian items 10, 15, 21 and 34 receive explicit visual reconfirmation. Canonical examples for 1, 2, 7, 11, 16 and 28 are also checked in the rendered artifact.

If a visual defect is discovered, classify it before changing runtime/reference content. Rebuild and re-render after every correction.

## Gate before Scientific Article

Scientific Article starts only after the corrected canonical V3 reference PDF has accepted provenance, the complete page-level visual checklist contains no unexplained FAIL, presentation evidence is reproducible, the temporary executor is removed, documentation is synchronized, and one immutable Reference PDF Validation candidate passes Static plus full Linux.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
