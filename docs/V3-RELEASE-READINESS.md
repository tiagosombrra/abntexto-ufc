# V3.0.0 Release Readiness

Updated: 2026-09-07
Status: ACTIVE — SCIENTIFIC ARTICLE STEP 6 IMPLEMENTED / CI PENDING

## Phase readiness

| Phase | State | Accepted evidence / pending work |
|---|---|---|
| Regression Audit | CLOSED | phase-end regression accepted |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE** | Steps 1–5 accepted; Step 6 implemented/CI pending; Steps 7–8 remain |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility matrix |
| Release | QUEUED | bundles, checksums, tag/GitHub Release and publication verification |

## Current Scientific Article checkpoint

| Surface | State |
|---|---|
| Steps 1–5 | ACCEPTED |
| Step 6 evidence map | IMPLEMENTED — exactly 18 rule IDs |
| Step 6 Static checker | IMPLEMENTED — `scientific_article_evidence_map.py` |
| Step 6 proof promotions | **0** |
| Optional foreign elements | remain optional |
| Recommendation rules | remain manual/non-enforcing |
| Journal precedence | remains required-when-applicable / conditional-manual |
| Step 6 acceptance | CI PENDING |
| Step 7 canonical article PDF | NOT STARTED |
| Step 8 complete phase-end regression | NOT STARTED |

## Integration state

| Fact | State |
|---|---|
| Canonical `main` | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Main README/control-plane reconciliation | PR #288 merged |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation | `85cf22b6fe5d117bb2611a2865911e0d20a19363` |

## What still blocks v3.0.0

| Blocker | Severity | Exit condition |
|---|---|---|
| Scientific Article Step 6 acceptance | P0 | synchronized Static + selected Linux scope green |
| Scientific Article canonical PDF | P0 | real provenance-bound article PDF + complete visual review |
| Scientific Article phase-end regression | P0 | Static + `complete` Linux + article gates on one immutable SHA |
| PR #286 / issue #280 | P0 | close after Scientific Article phase acceptance |
| Final Certification | P0 | final immutable candidate passes all profiles, engines, literal fonts, Unicode, embedding, PDF/A and distribution checks |
| Issue #18 release-PDF reproducibility | P0 | pinned epoch/`SOURCE_DATE_EPOCH`, controlled rebuilds and stable digest evidence |
| Release phase | P0 | final docs, bundles, checksums, `v3.0.0` tag, GitHub Release and publication verification |
| Librarian item 33 | explicit authority gap | remain fail-closed unless authoritative current NBR 6023:2025 evidence is obtained |

Item 33 is an explicit `NORMATIVE-REVIEW`, not permission to invent behavior. Current release readiness permits it to remain documented/fail-closed; obtaining authoritative text would allow resolution but absence of that text must never trigger speculative runtime changes.

## Active documentation authority

| Surface | Role |
|---|---|
| `release/v3-roadmap.json` | machine state |
| `docs/HANDOFF-V3.0.0.md` | canonical execution handoff |
| `docs/ROADMAP-V3.0.0.md` | readable phase roadmap |
| `docs/V3-SCIENTIFIC-ARTICLE.md` | active article execution plan |
| `docs/ARTICLE-NORMATIVE-CONTRACT.md` | source/authority/modality contract |
| `standards/coverage-rules-article.json` | retained 18-rule source contract |
| `standards/article-evidence-map.json` | current article-specific evidence ownership/disposition |
| `docs/LINUX-INTEGRATION-SCOPES.md` | scoped Linux policy |
| `docs/UFC-LIBRARIAN-REVIEW.md` | protected 34-point shared review contract |

## Mandatory closeout rule

Every **material advance** updates the relevant operational documents in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA. Scoped intermediate Linux runs never close a phase.
