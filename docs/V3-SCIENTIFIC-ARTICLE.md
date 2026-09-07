# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 6 EVIDENCE HARDENING

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. The phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.  
Linux orchestration contract: `docs/LINUX-INTEGRATION-SCOPES.md`.

## Step status

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign elements | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425` |
| 5 | Recommendations and conditional applicability | **ACCEPTED** | `55fa1c8dc1b503c119d564950d04141cf45ad345`; Static `34132291198`; Linux `34132291304`; bounded `article` scope; all six first-class checks PASS |
| 6 | Evidence hardening | **ACTIVE** | map all 18 rules to direct article-specific evidence or retain honest manual/conditional state |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

## Step 5 acceptance record

The short-sentinel correction is accepted at `55fa1c8dc1b503c119d564950d04141cf45ad345`.

| Gate | Result |
|---|---|
| Static `34132291198` | **PASS** |
| Automatic Linux inference | **`article`** |
| Linux `34132291304` | **PASS**, all six first-class article checks green |
| Recommended scenario | pdfLaTeX + LuaLaTeX compiled; summary marker and `ARTKEYONE`, `ARTKEYTWO`, `ARTKEYTHREE` rendered |
| Outside-recommendation scenario | both engines compiled; two summary paragraphs and `ARTOUTKEY` rendered |
| Recommendation semantics | non-enforcing; recommendation hard failures `0` |
| Journal precedence | `required-when-applicable`, `conditional-manual`, target-journal-bound |
| Steps 1–4 | remained green |
| Proof state | `proof_state_promoted=0` |

The correction changed only controlled evidence sentinels. It did not change article runtime, rule IDs, locators, normativity, applicability or proof state.

## Step 6 objective — article-specific evidence hardening

Step 6 makes proof-state semantics explicit. The retained 18-rule source contract must be paired with a machine-readable article-specific evidence map. Every rule is classified by what the current executable article suite actually proves.

Shared implementation reuse does not count as article proof. A rule can be promoted from manual only when an article-specific observer/rejection predicate directly measures the rule. Optional and recommended rules must retain their modality even when positive scenarios exist.

### Expected evidence classes

| Rule family | Evidence expectation |
|---|---|
| Required primary title, authorship, primary summary, submission/approval dates | direct article front-block evidence; negative required-field paths where supported |
| Required introduction, development, final considerations, references | direct article structure evidence; negative missing-section paths where supported |
| Primary title typography and author-note metadata | article front-block physical/semantic evidence |
| Body typography | direct physical article-body evidence in both engines |
| Optional foreign title and summary | article-specific present/absent combinations; optionality must not be strengthened |
| Recommended alignment/word-count/keyword-minimum/single-paragraph | retain non-enforcing status; recommendation scenario evidence is advisory/default evidence only |
| Journal precedence | retain `conditional-manual`; no generic runtime predicate may claim target-journal compliance |

## Step 6 implementation contract

1. Create a machine-readable map covering exactly the 18 article rule IDs.
2. Each entry identifies article-specific evidence surfaces and the truthful proof-state disposition.
3. Reject missing/duplicate/unknown rule IDs.
4. Reject automatic/proof promotion when only a shared mechanism or recommendation default exists.
5. Require recommended rules to remain non-enforcing.
6. Require `article.journal-guidelines.precedence` to remain `conditional-manual` and context-bound.
7. Protect the mapping with a static checker wired into the repository contract.
8. If `standards/coverage-rules-article.json` proof-state metadata is changed, update it atomically with the evidence map and checker; do not change source-backed requirement text, modality, locators or applicability without authority.
9. Synchronize handoff, roadmap, machine state and this plan in the same material-advance cycle.
10. Accept Step 6 only after the required Static/Linux gates pass.

## Step 6 acceptance gate

| Gate | Required result |
|---|---|
| 18-rule evidence map | exactly one entry per retained article rule |
| Article-specific provenance | every promoted rule points to direct article-specific executable evidence |
| Required-rule evidence | truthful bounded-positive/automatic state only where the executable predicate exists |
| Optional rules | optionality preserved; present/absent article scenarios mapped |
| Recommended rules | remain advisory and non-enforcing |
| Journal precedence | remains conditional-manual and target-journal-bound |
| Shared mechanisms | never counted as proof by themselves |
| Static contract | PASS |
| Linux | required scope selected by changed-path policy and PASS |
| Steps 1–5 | remain accepted |

Step 7 is not activated until Step 6 is accepted and recorded.

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no aliases.
- Preserve all accepted non-article profiles and shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain conditional.
- Shared implementation is not article proof.
- Do not weaken Step 4 physical PDF evidence or Step 5 non-enforcement evidence.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker.
- Every **material advance** updates handoff, roadmap, machine state and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

| Fact | Value |
|---|---|
| Canonical base | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch | `feat/v3-scientific-article` |
| Active PR | #286 |
| Step 5 accepted checkpoint | `55fa1c8dc1b503c119d564950d04141cf45ad345` |
| Step 5 Static | `34132291198` PASS |
| Step 5 Linux | `34132291304` PASS, scope=`article` |

Next: inventory the 18 rules against Steps 1–5 evidence, implement the protected evidence map/checker, synchronize documentation, and validate Step 6 without over-promoting proof state.
