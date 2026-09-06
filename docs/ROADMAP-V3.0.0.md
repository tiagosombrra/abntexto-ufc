# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Scientific Article is ACTIVE — Step 1 implemented, acceptance pending.**

The shared academic-work foundation is closed and accepted:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, with complete 55/55 visual PASS.

The librarian-review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

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
| **Scientific Article** | **ACTIVE — STEP 1 CI PENDING** | Implement one canonical article profile using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Scientific Article execution state

| Step | Work | State | Acceptance gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | IMPLEMENTED — CI PENDING | `b46ba2051f8c9c712a7b5d25748b81baa52b920a` is included in a synchronized checkpoint that must pass Static + full Linux |
| 2 | Required article front block | QUEUED | Primary title, authorship metadata footnote, submission/approval dates and primary summary have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary can be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Introduction/development/final considerations/references and article body typography validated with shared infrastructure |
| 5 | Recommendations and conditional boundary | QUEUED | Recommendations remain advisory; journal instructions remain conditional |
| 6 | Evidence hardening | QUEUED | Positive/negative article evidence is rule-specific and proof state truthful |
| 7 | Canonical article PDF | QUEUED | Real Git-bound TeX Live 2026 artifact with complete visual review |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

### Step 1 technical scope

The bounded implementation adds exactly one canonical `type = scientific-article` route, reuses `author`, `title` and `approval-date`, and adds only `submission-date` plus `article-author-note`. A dedicated static contract rejects aliases, and a two-engine compile gate proves profile selection and metadata round-trip. The existing six non-article profile matrix remains intact and is still executed.

No `article.*` presentation/proof state is promoted merely from this registration step. Foreign-title semantics are deferred to Step 3 rather than inferred from the generic `title-variant` key.

## Gate before Final Certification

Scientific Article must close with no article runtime FAIL, truthful article proof state, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable phase-end candidate green on the complete relevant regression.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. Historical labels are retained only when identifying old evidence. GitHub issue/PR numbers and immutable SHAs provide traceability.
