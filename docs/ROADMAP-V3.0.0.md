# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 5 — scoped orchestration inference is corrected; rendered keyword-sentinel hardening is the remaining acceptance blocker.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 5** | Steps 1–4 accepted; Step 5 article evidence green in complete regression; orchestration correction now selects `article`; short-sentinel evidence correction pending |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425`; `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| 5 | Recommendations and conditional applicability | **EVIDENCE HARNESS CORRECTION ACTIVE** | `6507da...` complete 36/36 article evidence green; `02e1ea...` Static `34129625390` PASS and auto scope=`article`; Linux `34129625475` PASS=5/6 with only long keyword sentinel extraction failure |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 5 evidence and failure classification

The complete Linux run `34126602083` on `6507da00275d8a69093541d6e6cb119a1b6f6cb3` passed all 36 repository checks, including all six article gates. The later correction `02e1ea6e25c008c93f8ec3ba26af7f3cea03cf14` fixed the independent suite-inference defect: Static `34129625390` passed and Linux `34129625475` automatically selected bounded scope `article`.

In that bounded run, validator source, article profile, front block, foreign elements and body all passed. The recommendation contract checker also passed and preserved `recommended`/`conditional-manual` modality with zero proof-state promotion. The only failure was exact `pdftotext -layout` extraction of the long third synthetic keyword token in the recommended pdfLaTeX scenario.

The failure is classified as an evidence-sentinel robustness defect unless a shorter controlled sentinel also fails. No article runtime or normative rule is changed at this stage.

## Current correction

Use short synthetic keyword sentinels in the two Step 5 fixtures and require extraction of all three recommended markers plus the single outside-recommendation marker. This maintains stronger rendered-output evidence while reducing brittleness caused by long artificial tokens at PDF line boundaries.

## Current Step 5 acceptance gate

| Gate | Required result |
|---|---|
| Static | PASS |
| Automatic inference | bounded `article` |
| Linux `article` | `PASS=6 FAIL=0 SKIP=0` |
| Recommended PDF evidence | both engines render summary marker + 3/3 controlled keyword markers |
| Outside-recommendation evidence | both engines render both paragraphs + controlled keyword marker |
| Semantics | recommendations remain advisory; journal precedence remains conditional |
| Steps 1–4 | remain green |
| Proof state | no promotion from shared/default behavior |

Only after those results are recorded does Step 6 activate.

## Shared state

| Fact | State |
|---|---|
| Canonical base | `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Item 33 | fail-closed pending authoritative current NBR 6023:2025 evidence |
| Release blocker | issue #18 |

Machine authority: `release/v3-roadmap.json`. Canonical handoff: `docs/HANDOFF-V3.0.0.md`. Scientific Article plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Operating discipline

Every **material advance** updates the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase, acceptance, evidence, Linux-scope policy, current batch or branch/checkpoint facts update this roadmap and machine state.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Step checks do not replace this gate; Scientific Article Step 8 requires `complete` Linux.

## Gate before Final Certification

Scientific Article must complete Steps 5–7 and pass Step 8 on one immutable SHA. The canonical article PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.
