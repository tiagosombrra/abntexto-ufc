# V3.0.0 Release Readiness

Updated: 2026-09-06
Status: ACTIVE — SCIENTIFIC ARTICLE STEP 3 CI PENDING

## Purpose

Keep repository structure, active plans, issues, branches and release blockers explicit while V3 advances. This document is operational inventory; normative authority remains in the dedicated standards/contracts.

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | green phase-end regression; 34-point librarian contract established |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE** | Steps 1–2 accepted; Step 3 implementation `81e0832...` awaiting synchronized Static/full Linux; Steps 4–8 remain |
| Final Certification | QUEUED | literal-font/Unicode/embedding/PDF-A/distribution matrix plus release-PDF reproducibility proof |
| Release | QUEUED | release assets, checksums, tag/release publication and final verification |

## Scientific Article current checkpoint

| Surface | State |
|---|---|
| Step 1 | ACCEPTED — `08b878a...`; Static `34001350884`; Linux `34001350953` |
| Step 2 | ACCEPTED — `0947669...`; Static `34026680871`; Linux `34026680882`, `PASS=31 FAIL=0 SKIP=0` |
| Step 3 technical implementation | `81e08321222efb03626ac421fc645bd66edd5ae8` |
| Step 3 behavior | explicit article-only foreign-elements route; title/summary independently optional |
| Step 3 evidence | four scenarios × pdfLaTeX/LuaLaTeX through `scientific-article-foreign-elements.sh` |
| Step 3 acceptance | **PENDING synchronized Static + full Linux** |
| Article proof state | unchanged; manual/conditional-manual until dedicated evidence hardening |

## Integration state

PR #285 is merged into canonical `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`. The active branch is `feat/v3-scientific-article`, tracked by PR #286.

## Open issue inventory

| Issue | Classification | Release impact | Treatment |
|---|---|---|---|
| #280 Scientific Article | active implementation | BLOCKS Final Certification | keep open until article phase-end regression closes |
| #18 deterministic release reference PDF | release-quality defect | **BLOCKS v3.0.0 Release** | implement pinned release epoch/`SOURCE_DATE_EPOCH`; rebuild in controlled contexts; compare PDF hashes and retain evidence |
| #217 historical Linux orchestration | superseded | none | closed/not planned; current workflows supersede it |

## Active branch model

| Branch class | State | Rule |
|---|---|---|
| `main` | canonical | accepted shared foundation |
| `feat/v3-scientific-article` | **ACTIVE** | only current Scientific Article work branch |
| `plan/v3-regression-reset` | historical | no new work |
| other historical branches | provenance only | not active authority |

## Current release blockers

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article incomplete | P0 feature completeness | Steps 3–8 complete; canonical article PDF visually accepted; phase-end regression green |
| Issue #18 reference-PDF reproducibility | P0 release reproducibility | deterministic build policy and stable digest evidence |
| Final Certification not run on final candidate | P0 | heavy platform/font/PDF-A/distribution matrix green on one immutable SHA |
| Release phase not executed | P0 | bundles/checksums/assets/tag/release verification complete |
| Librarian item 33 authority gap | explicit NORMATIVE-REVIEW | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

## Step 3 release-safety boundary

Step 3 must remain bounded to optional article foreign elements. It may not create mandatory foreign fields, repurpose ambiguous shared metadata, activate body typography, promote recommendation semantics, or alter article proof state. The accepted non-article profile matrix must remain green.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active implementation plan |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | article source/authority/modality contract |
| `standards/coverage-rules-article.json` | machine article rule contract |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point shared review contract |
| accepted Reference PDF documents | academic-work presentation evidence |
| this file | release-readiness inventory |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Final Certification and Release additionally must account for issue #18 so the published V3 reference artifact is reproducible, not merely visually/normatively correct.
