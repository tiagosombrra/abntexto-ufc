# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 6 — evidence hardening. Steps 1–5 are accepted, and PR #286 is reconciled with current `main`.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 6** | Steps 1–5 accepted; current-main reconciliation recorded; Step 6 must map all 18 retained rules to truthful article-specific evidence before canonical article PDF work |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425` |
| 5 | Recommendations and conditional applicability | ACCEPTED | `55fa1c8...`; Static `34132291198`; Linux `34132291304`; bounded `article` scope; six first-class checks PASS |
| 6 | Evidence hardening | **ACTIVE** | exact 18-rule machine map; article-specific ownership; truthful validation/evidence promotion only where directly supported |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Current-main reconciliation

Canonical `main` advanced to `789c6f3f4669ae36c3d4fe831ae939a340592568` with accepted scoped Linux orchestration. PR #286 had been based on `e6833ed...` and became dirty. Merge `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` reconciles the article branch with current `main` while preserving the branch's newer fail-closed synchronize fallback.

This reconciliation does not change article authority, runtime predicates, 18-rule modality, or proof state. It restores current-main ancestry before Step 6 evidence work continues.

## Step 6 evidence-hardening objective

Step 6 must distinguish executable article-specific proof ownership from shared implementation reuse. The retained 18-rule source contract is not rewritten merely because an implementation or generic shared test exists.

| Rule group | Required Step 6 treatment |
|---|---|
| Required front block, textual structure and body typography | map each rule to direct article-specific executable evidence before executable proof ownership is declared |
| Optional foreign title/summary | preserve optionality while recording both present and absent article scenarios |
| Recommended author alignment, summary word count, keyword minimum and single paragraph | keep advisory/non-enforcing semantics; positive scenarios do not become rejection predicates |
| Journal-guideline precedence | keep `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission` |

The implementation is a machine-readable article evidence map plus a static contract checker that rejects missing, duplicated, stale, over-promoted, shared-only, or modality-breaking claims.

## Shared state

| Fact | State |
|---|---|
| Canonical `main` | `789c6f3f4669ae36c3d4fe831ae939a340592568` |
| Shared-foundation integration checkpoint | `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Reconciliation merge | `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Item 33 | fail-closed pending authoritative current NBR 6023:2025 evidence |
| Release blocker | issue #18 |

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** updates the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase, acceptance, evidence, Linux-scope policy, current batch, branch/base reconciliation or checkpoint facts update this roadmap and machine state.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; Scientific Article Step 8 requires `complete` Linux.

## Gate before Step 7

Step 6 must have a machine-protected 18-rule evidence classification, no unauthorized authority/modality change, recommendations still non-enforcing, journal precedence still conditional-manual, and its required Static/Linux acceptance gates green.

## Gate before Final Certification

Scientific Article must complete Steps 6–7 and pass Step 8 on one immutable SHA. The canonical article PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.
