# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 4 — supported single-spacing route implemented after deprecated-API rejection; acceptance rerun pending.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 4 SUPPORTED SINGLE-SPACING CORRECTION PENDING ACCEPTANCE** | latest synchronized Linux rejected deprecated `\\spacing{1}` before physical body validation; correction now uses `\\singlesp` plus `cmd/textual/after` |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **SUPPORTED SINGLE-SPACING CORRECTION IMPLEMENTED — CI PENDING** | `49e7b17...`: Static PASS, complete Linux PASS=32 FAIL=2 SKIP=1 due deprecated `\\spacing` warning; implementation `6a7ef821...` uses supported `\\singlesp` and retains `\\textual` rebound |
| 5 | Recommendations and conditional applicability | BLOCKED | starts only after Step 4 acceptance is recorded |
| 6 | Evidence hardening | QUEUED | rule-specific evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + complete Linux + article-specific evidence on one immutable SHA |

## Step 4 regression trail

| Checkpoint | Static | Linux | Meaning |
|---|---|---|---|
| `8b52ee4...` | `34058435312` PASS | `34058435311` FAIL, article PASS=4 FAIL=1 | body spacing stayed at 1.5: `20.700 pt` vs `13.800 pt` single calibration |
| `177a621...` | `34070809181` PASS | `34070809177` FAIL, article PASS=2 FAIL=3 | stale source guards stopped before physical body validation |
| `bf6c48e...` | `34071163701` PASS | `34071163702` FAIL, article PASS=4 FAIL=1 | begin-document route ineffective; body remained `20.700 pt` |
| `09b870d...` | `34072362333` PASS | `34072362335` FAIL, article PASS=4 FAIL=1 | front-block-only route transient; first numbered section invokes `\\textual` and restores shared state |
| `49e7b17...` | `34111737479` PASS | `34111737488` FAIL, `SCOPE=complete PASS=32 FAIL=2 SKIP=1` | deprecated `\\spacing{1}` warning stopped front-block/body gates before physical Step 4 validation |

The current implementation `6a7ef821875c40b6fe0bbc3cca25e3c0ff4cb307` replaces the obsolete spacing call with supported `\\singlesp` and retains the profile-scoped `cmd/textual/after` reapplication. It also retains activation after the required primary summary for body content before the first numbered section. The physical validator is unchanged, and the source gate now rejects any return to deprecated `\\spacing{1}`.

## Current Step 4 acceptance gate

| Gate | Required before Step 5 |
|---|---|
| Static contract | synchronized correction checkpoint PASS |
| Linux | all five article checks PASS; orchestration may run complete scope |
| Body typography | 12 pt / justified / 2 cm / true single spacing under both engines |
| Transition persistence | single spacing and 2 cm indent survive the automatic `\\textual` route |
| API compatibility | no deprecated spacing warning; supported `\\singlesp` route |
| Required structure | positive structure present and missing-development negative rejected |
| Front block/foreign elements | continue passing under both engines independently of Step 4 source spelling |
| Proof-state boundary | no article rule promoted merely because shared mechanisms are reused |

## Shared state

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.
- Shared librarian-review state: **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.
- Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.
- Issue #18 remains a Release blocker.

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** updates the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase, acceptance, evidence, Linux-scope policy, current batch or branch/checkpoint facts update this roadmap and machine state.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; Scientific Article Step 8 requires `complete` Linux.

## Gate before Final Certification

Scientific Article must complete Steps 4–7 and pass Step 8 on one immutable SHA. The canonical article PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.
