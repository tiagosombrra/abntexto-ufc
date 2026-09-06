# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE — Step 1 ACCEPTED; Step 2 Required article front block is in EVIDENCE CORRECTION / CI PENDING.**

The validated shared foundation lives on canonical `main` through PR #285, squash merge `e6833ed5cf07aaf1021c690260cecfacec1a119a`. Remaining article work continues on `feat/v3-scientific-article` through PR #286.

Accepted foundation:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, complete 55/55 visual PASS;
- Scientific Article Step 1 — ACCEPTED on synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`, Static `34001350884`, Linux `34001350953`, `PASS=31 FAIL=0 SKIP=0`.

Current Step 2 state:

- runtime implementation checkpoint `90293af760c4063b02a16831196ec3d932f1471d`;
- normative-currency reconciliation `e29501bd8cae98d6442f08e17bc3a54892fc7e0d`;
- post-currency synchronized checkpoint `6587636f8550dcd68b3feec5bbd145551775eb4b`;
- Static `34003838489`: SUCCESS;
- Linux `34003838521`: FAILURE, `PASS=29 FAIL=1 SKIP=1`;
- isolated Linux failure: article front-block validator imposed a fixed physical-page bottom threshold on author-note placement although the runtime uses a genuine LaTeX `\footnote` route;
- validator-predicate correction checkpoint `bb52697a0e71b2d6a8bc135196f40dba9497b38f`;
- runtime `abntexto-ufc/articles.def` unchanged by this correction;
- corrected evidence requires semantic `\footnote` routing plus rendered post-front-block 10 pt footnote typography, without inventing a page-height percentage;
- optional foreign elements, body typography and recommendation enforcement remain deliberately deferred;
- article coverage proof state remains manual/conditional-manual pending later truthful promotion.

The librarian-review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.  
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.  
Active phase plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.  
Normative currency: `docs/NORMATIVE-CURRENCY.md`.  
Release readiness: `docs/V3-RELEASE-READINESS.md`.  
Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, article proof/evidence state, acceptance state, current work, artifact provenance, release blockers, temporary-executor lifecycle or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks, compile success and visual inspection do not replace that gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | `5f67560a...` passed Static/full Linux. |
| **Reference PDF Validation** | CLOSED | Validate the corrected canonical academic-work PDF page by page. | `b64074c...` passed Static/full Linux after provenance + 55/55 visual PASS. |
| **Scientific Article** | **ACTIVE — STEP 2 EVIDENCE CORRECTION / CI PENDING** | Complete the canonical article profile using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification and release-reference-PDF reproducibility proof. | Heavy certification matrix plus deterministic release-reference-PDF evidence green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Issue #18 resolved; release checklist complete; final regression recorded. |

## Scientific Article execution state

| Step | Work | State | Acceptance gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953`, 31/31 PASS |
| 2 | Required article front block | **EVIDENCE CORRECTION — CI PENDING** | runtime `90293af...`; currency fix `e29501b...`; Static `34003838489` PASS; Linux `34003838521` classified; validator fix `bb52697...`; synchronized Static/full Linux required |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary can be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Introduction/development/final considerations/references and article body typography validated with shared infrastructure |
| 5 | Recommendations and conditional boundary | QUEUED | Recommendations remain advisory; journal instructions remain conditional |
| 6 | Evidence hardening | QUEUED | Positive/negative article evidence is rule-specific and proof state truthful |
| 7 | Canonical article PDF | QUEUED | Real Git-bound TeX Live 2026 artifact with complete visual review |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Step 2 gate classification

| Gate | Result | Interpretation |
|---|---|---|
| Static `34003576066` on `768d355...` | FAIL | stale pre-activation normative-currency coupling; corrected at `e29501b...` |
| Static `34003838489` on `6587636...` | PASS | normative-currency transition accepted |
| Linux `34003838521` on `6587636...` | FAIL, 29/1/1 | only `Document profiles` failed; `ARTICLE-PROFILE-EVIDENCE` passed before front-block validator rejected unsupported page-bottom geometry |

The article source contract requires complementary author metadata in a footnote. It does **not** prescribe a physical-page percentage for footnote placement. The previous `note_y >= 65% page height` predicate therefore exceeded the authority contract. Correcting that predicate is not test weakening: the semantic LaTeX `\footnote` route remains source-enforced, and final-PDF evidence still requires the note after the front block using the shared 10 pt footnote typography.

No article runtime, source authority, rule ID, modality, locator or proof state changes in this correction.

## Step 2 acceptance boundary

The synchronized corrected checkpoint must prove:

- normative currency and technical precedence remain green;
- article profile route on pdfLaTeX and LuaLaTeX;
- primary title rendered at 12 pt, centered and bold, with single-spacing composition guarded in source;
- `article-author-note` routed through a genuine `\footnote` and rendered at shared 10 pt footnote typography after the front block;
- submission and approval dates rendered;
- primary summary rendered;
- no academic-work front-matter leakage;
- all six accepted non-article profiles remain green;
- no foreign-element, body-typography or recommendation modality is prematurely promoted;
- Static and full Linux are green.

## Repository integration and branch plan

| Surface | State | Policy |
|---|---|---|
| `main` | current at/after `e6833ed5...` | canonical integration base |
| `feat/v3-scientific-article` | ACTIVE | only branch for new Scientific Article implementation |
| PR #286 | OPEN | active integration/review surface for Scientific Article work |
| `plan/v3-regression-reset` | HISTORICAL | no new work; removal is repository hygiene only |
| historical `audit/`, `docs/`, `r3-*`, old `feat/`, `fix/`, `refactor/` branches | PROVENANCE ONLY | not active authority and never a base for new work |

## Known v3.0.0 blockers and tracked debt

| Item | State | Owner / treatment |
|---|---|---|
| Scientific Article phase / #280 | ACTIVE | finish Steps 2–8 and phase-end regression |
| Release reference PDF bit reproducibility / #18 | OPEN — **RELEASE BLOCKER** | Final Certification/Release must pin a release epoch/`SOURCE_DATE_EPOCH` and compare rebuilt hashes |
| Historical workflow issue #217 | CLOSED — SUPERSEDED | current permanent workflow/readable phase model is authoritative |
| Librarian-review item 33 | NORMATIVE-REVIEW | explicit authority gap; no speculative runtime change; not silently converted to PASS |
| Historical branch clutter | NON-BLOCKING HYGIENE | provenance only; active work follows `main` + one current task branch |

## Gate before Final Certification

Scientific Article must close with no article runtime FAIL, truthful article proof state, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable phase-end candidate green on the complete relevant regression.

## Gate before Release

Final Certification must prove the profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must also be resolved with deterministic release reference-PDF evidence. Release then owns final bundles, checksums, tag/release assets and publication verification.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. Historical labels are retained only when identifying old evidence. GitHub issue/PR numbers and immutable SHAs provide traceability.
