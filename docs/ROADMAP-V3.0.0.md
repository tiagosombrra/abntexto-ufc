# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Scientific Article is ACTIVE.**

The shared academic-work foundation has completed all pre-article phases:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, with provenance-bound canonical PDF and complete 55/55 visual PASS.

The librarian review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains a deliberate fail-closed authority gap pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.  
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.  
Active phase plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.  
Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, article proof/evidence state, acceptance state, current work, artifact provenance, temporary-executor lifecycle or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks, compile success and visual inspection do not replace that gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | `5f67560a...` passed Static/full Linux. |
| **Reference PDF Validation** | CLOSED | Validate the corrected canonical academic-work PDF page by page. | `b64074c...` passed Static/full Linux after provenance + 55/55 visual PASS. |
| **Scientific Article** | **ACTIVE** | Implement one canonical article profile on the corrected shared foundation using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Accepted Reference PDF evidence

| Evidence | State |
|---|---|
| Git-bound canonical build | PASS — `da02f17df4d2d0a1568edbbe8bfbbfffb7208966` |
| Build workflow | PASS — `33983729996` |
| Artifact | `9974546873` |
| PDF SHA-256 | `bb96593849f4c76d32f43248ab9d5e23afa303a168fd76b2b6166431353ec04c` |
| Preflight | PASS — 55 A4 pages, PDF 1.7, text based, unencrypted, fonts embedded |
| Complete 200 DPI page sequence | PASS — 55/55 |
| Global clipping/overlap/broken glyph review | PASS |
| Presentation-sensitive librarian reconfirmation | PASS |
| Phase-end Static | `33985595790` — SUCCESS |
| Phase-end Linux | `33985595798` — SUCCESS |
| Temporary executor | Removed |

The optional licensed-photo placeholders in the canonical reference PDF are intentional normal-build fallback behavior when `make reference-assets` has not been run.

## Scientific Article entry state

The source-backed article contract contains 18 rules. All remain source-reviewed and no article-specific proof is inferred from the shared foundation.

Current runtime inspection shows that `abntexto-ufc/core.def` does **not** yet expose the canonical `scientific-article` type. This is the first bounded runtime gap; it is not a regression of the accepted non-article profiles.

Implementation order:

| Step | Work | Acceptance |
|---:|---|---|
| 1 | Profile and metadata surface | Canonical `scientific-article` route compiles; no aliases; shared profiles unchanged |
| 2 | Required article front block | Primary title, authorship metadata, submission/approval dates and primary summary have article-specific evidence |
| 3 | Optional foreign elements | Foreign title/summary can be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | Introduction/development/final considerations/references and article body presentation are validated using shared infrastructure |
| 5 | Recommendations and conditional boundary | Recommended summary/authorship rules remain advisory; journal instructions remain conditional |
| 6 | Evidence hardening | Positive/negative article-specific evidence is fail-closed and contribution/proof state is truthful |
| 7 | Canonical article PDF | Real LaTeX artifact is provenance-bound and visually inspected |
| 8 | Phase-end regression | Static + full Linux + article-specific acceptance on one immutable SHA |

## Gate before Final Certification

Scientific Article must close with no article runtime FAIL, truthful article proof state, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable phase-end candidate green on the complete relevant regression.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. Historical labels are retained only when identifying old evidence. GitHub issue/PR numbers and immutable SHAs provide traceability.
