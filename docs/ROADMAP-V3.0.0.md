# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 5 — first-class recommendation/conditional evidence implemented, synchronized CI pending.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 5** | Steps 1–4 accepted; Step 5 synchronized implementation candidate now requires Static + six-check Linux `article` |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425`; `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| 5 | Recommendations and conditional applicability | **IMPLEMENTED — CI PENDING** | dedicated checker + recommended/outside fixtures + two-engine gate + first-class article registration |
| 6 | Evidence hardening | QUEUED | rule-specific evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 5 evidence contract

| Retained rule | Modality | Executable preservation |
|---|---|---|
| `article.authorship.alignment.recommended` | recommended | right alignment remains generic default; no validity rejection predicate |
| `article.summary.word-count.recommended` | recommended | controlled short summary must compile |
| `article.summary.keywords.minimum.recommended` | recommended | controlled fewer-than-three-keyword case must compile |
| `article.summary.single-paragraph.recommended` | recommended | controlled two-paragraph summary must compile |
| `article.journal-guidelines.precedence` | required-when-applicable | static contract preserves `conditional-manual` and `target-journal-submission` applicability |

The Step 5 implementation intentionally adds evidence, not new normative runtime validation. The retained rule registry remains unchanged and proof state remains unpromoted.

The fixture-only checkpoint `f4453337d2de94260d7ebda4cead9803a6a9cb64` passed Static `34124565217` and Linux `34124565158`, but that Linux run contained only the five Step 1–4 checks. It is preflight evidence, not Step 5 acceptance.

## Current Step 5 acceptance gate

1. the synchronized implementation commit passes Static;
2. Linux `article` runs **six** first-class checks and passes all of them;
3. recommendation-outside-range scenarios compile under pdfLaTeX and LuaLaTeX;
4. Steps 1–4 remain green;
5. no shared non-article behavior, rule IDs, modality, locators, applicability or proof state changes;
6. only after results are recorded does Step 6 activate.

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

Scientific Article must complete Steps 5–7 and pass Step 8 on one immutable SHA. The canonical article PDF must be provenance-bound and visually inspected. No unresolved article runtime/evidence failure may remain.

## Gate before Release

Final Certification must pass and issue #18 must be resolved with deterministic release-reference-PDF hash evidence. CTAN/publication actions remain blocked until **Release**.
