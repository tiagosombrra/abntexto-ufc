# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Reference PDF Validation is ACTIVE — visual review PASS, phase-end regression candidate gate.**

Core Corrections closed on immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, with Static `33982156041` and full Linux `33982156042` successful; Linux summary `PASS=31 FAIL=0 SKIP=0`.

The librarian review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains an explicit fail-closed authority gap.

Canonical PDF provenance is accepted from build SHA `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`, workflow run `33983729996`, artifact `9974546873`, SHA-256 `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c`.

The complete 55-page, 200 DPI visual review is **PASS** with zero unexplained visual failures. Detailed evidence is in `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.

Machine authority: `release/v3-roadmap.json`.  
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.  
Active phase contract: `docs/V3-REFERENCE-PDF-VALIDATION.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current work, artifact provenance, visual-review status or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks and visual inspection do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | Candidate `5f67560a...` passed Static `33982156041` and Linux `33982156042`. |
| **Reference PDF Validation** | ACTIVE — PHASE-END CANDIDATE | Validate the corrected canonical V3 PDF page by page. | Provenance PASS + 55/55 visual PASS + immutable candidate passes Static/full Linux. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Reference PDF Validation evidence

| Evidence | State |
|---|---|
| Git-bound canonical build | PASS — `da02f17d...` |
| Build workflow | PASS — `33983729996` |
| Artifact digest / local digest | PASS — exact SHA-256 match |
| Preflight | PASS — 55 A4 pages, PDF 1.7, text based, unencrypted, no XFA, fonts embedded |
| Complete 200 DPI page sequence | PASS — 55/55 |
| Global clipping/overlap/broken glyph review | PASS |
| Presentation-sensitive librarian reconfirmation | PASS |
| Stale-PDF comparison | Preservation-only; 28 unchanged / 27 changed pages, no page-count drift |
| Item 33 | NORMATIVE-REVIEW — authority deferred |
| Temporary executor | Removed |

The optional licensed-photo placeholders on page 36 are intentional normal-build fallback behavior and are documented by the reference source itself.

## Current gate

The repository state containing the complete visual-review record is the next immutable Reference PDF Validation phase-end candidate. It must pass Static contract and full Linux integration on the same SHA. Only a later result-recording commit may close this phase.

## Gate before Scientific Article

Scientific Article starts only after the accepted canonical V3 reference PDF has provenance PASS, complete visual PASS, synchronized documentation, and one immutable Reference PDF Validation candidate with Static and full Linux both green.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
