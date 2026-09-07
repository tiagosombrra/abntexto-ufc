# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 6 EVIDENCE HARDENING / CURRENT MAIN RECONCILED

## Entry state

Core Corrections and Reference PDF Validation are closed. The shared foundation was integrated at `e6833ed5cf07aaf1021c690260cecfacec1a119a`; canonical `main` has since advanced to `789c6f3f4669ae36c3d4fe831ae939a340592568` with accepted scoped Linux orchestration.

The active branch is `feat/v3-scientific-article`, PR #286. It was reconciled with current `main` through merge `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` before Step 6 evidence work continues.

The retained article authority product is `4d018a92697e8f39e3a53b034c451e55996c84fb`, represented by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`. There are exactly 18 article rules. Their source-backed requirement text, modality, locators and applicability are not rewritten merely because runtime evidence now exists.

## Progress

| Step | Work | State | Accepted evidence / next gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | ACCEPTED | `0947669c2c096dca93991e042d8ae245754688ba`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa63950bb2acd0576f8ea6ad27bef8f49ba`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd615042a12fb0393fddd4941b635f6ce3`; Static `34119007413`; Linux `34119007425`; body 12 pt, justified, 2 cm, single spacing; negative missing-development case rejected correctly |
| 5 | Recommendations and conditional applicability | ACCEPTED | `55fa1c8dc1b503c119d564950d04141cf45ad345`; Static `34132291198`; Linux `34132291304`; `SCOPE=article PASS=6 FAIL=0 SKIP=0` |
| 6 | Evidence hardening | **ACTIVE** | exact 18-rule article-specific evidence map + static checker + truthful validation/evidence ownership |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF and complete page-level visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Repository reconciliation before Step 6

`main` moved after Step 5 activation. PR #286 became dirty because the active branch and `main` independently contained scoped-Linux orchestration work. The branch version is a stricter superset of the merged `main` behavior: it keeps the accepted domain-selection model and additionally falls back to the full PR range when incremental synchronize endpoints are unavailable.

Merge `ae7e2cf...` records `789c6f3...` as current-main ancestry without discarding Steps 1–5 or weakening orchestration. This is control-plane reconciliation, not article proof-state promotion.

## Step 6 objective

Create a machine-readable article-specific evidence map covering **exactly all 18 retained article rule IDs**. Every entry must state what current executable article evidence actually proves and what remains manual, conditional, advisory or unproven.

Shared implementation reuse is never sufficient proof. A rule may move from source-review-only validation only when a direct article-specific executable observer or rejection predicate owns that claim.

## Step 6 implementation contract

1. add `standards/article-evidence-map.json` with exactly the 18 rule IDs from `standards/coverage-rules-article.json`;
2. classify each rule by normativity, current validation mode, article-specific owner/support gate, positive/negative/final-PDF evidence and proof disposition;
3. reject missing, duplicate or unknown article rule IDs;
4. reject executable/proof ownership when the only basis is a shared mechanism or a recommendation-following default;
5. keep `article.authorship.alignment.recommended`, `article.summary.word-count.recommended`, `article.summary.keywords.minimum.recommended` and `article.summary.single-paragraph.recommended` non-enforcing;
6. keep `article.journal-guidelines.precedence` as `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`;
7. preserve independent present/absent evidence for `article.title.foreign.optional` and `article.summary.foreign.optional`;
8. wire a dedicated Step 6 static checker into `tests/static.py`;
9. when a required rule is promoted to executable validation, its declared evidence must be an article-specific runner gate that emits rule-specific `rule=<id> status=PASS` evidence;
10. if validation/evidence metadata in `standards/coverage-rules-article.json` changes, update the evidence-contribution policy atomically; source requirement text, modality, locators and applicability remain unchanged without new authority;
11. synchronize this plan, handoff, roadmap, normative contract when evidence ownership changes, release-readiness inventory and `release/v3-roadmap.json` in the same material-advance cycle;
12. accept Step 6 only after Static and the Linux scope selected by changed-path policy are green.

## Truthful evidence disposition

The current executable surfaces support the following bounded design:

| Rule family | Direct current evidence | Step 6 boundary |
|---|---|---|
| primary title, authorship, primary summary, dates, title typography, author metadata footnote | `scientific-article-front-block` under pdfLaTeX + LuaLaTeX with final-PDF measurements | may own executable validation without claiming full `PROVEN` status |
| introduction, development, final considerations, references, body typography | `scientific-article-body` with two-engine physical evidence; controlled negative path exists for missing development | may own executable validation without claiming full `PROVEN` status |
| foreign title / foreign summary | `scientific-article-foreign-elements`, four present/absent combinations × two engines | preserve optionality; conditional evidence, not mandatory presence |
| recommended author alignment / summary recommendations | `scientific-article-recommendations` recommended + outside-recommendation scenarios | support/default evidence only; remain manual/advisory and non-enforcing |
| target-journal precedence | source/applicability boundary only | remains conditional-manual; generic runtime must not automate it |

`standards/proof-policy.json` remains conservative: executable validation is not equivalent to a normative rule becoming `PROVEN`. Step 6 hardens ownership and evidence truthfulness; it does not manufacture full proof.

## Step 7 gate

Step 7 starts only when Step 6 is accepted with:

- exact 18-rule map protected by Static;
- no unauthorized authority/modality/locator/applicability change;
- direct article-specific ownership for any executable promotion;
- optional rules still optional;
- recommendations still non-enforcing;
- journal precedence still conditional-manual;
- Step 6 Static/Linux acceptance recorded.

## Step 7 canonical article PDF

Produce a real article PDF from the accepted branch using the project build/runtime, bind it to Git provenance, and inspect every page. Synthetic PDFs do not satisfy this step. Visual review must explicitly cover article-specific presentation, required/optional blocks, typography, structure, citations/references and absence of academic-work front-matter leakage.

## Step 8 phase-end regression

Scientific Article closes only when one immutable candidate passes:

1. Static contract;
2. Linux integration with **`complete`** scope;
3. all article-specific executable gates;
4. accepted canonical article PDF provenance and complete visual inspection;
5. no unresolved article runtime/evidence failure.

Scoped `article` checks are valid intermediate evidence but never replace the complete phase-end regression.

## Cross-phase boundaries

- Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a Final Certification/Release blocker and does not justify changing article runtime.
- Final Certification begins only after Scientific Article closes.
- CTAN/publication actions remain blocked until Release.

## Documentation discipline

Every **material advance** updates the relevant execution documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Branch/base reconciliation is itself a material control-plane advance and must be recorded before further feature/evidence work.
