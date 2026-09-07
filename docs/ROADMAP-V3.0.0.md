# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 5 — recommendation evidence is Linux-green; scoped orchestration correction is the current acceptance blocker.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 5** | Steps 1–4 accepted; Step 5 Linux evidence green at `6507da...`, Static exposed orchestration inference defect that must be corrected before acceptance |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425`; `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| 5 | Recommendations and conditional applicability | **EVIDENCE GREEN / ACCEPTANCE CORRECTION ACTIVE** | `6507da...`; Linux `34126602083` complete 36/36 PASS; Static `34126602062` found mixed orchestration+article scope bug |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 5 evidence already demonstrated

The complete Linux run `34126602083` on `6507da00275d8a69093541d6e6cb119a1b6f6cb3` passed all 36 repository checks, including all six article gates. The recommendation gate proved both recommended and outside-recommendation scenarios compile under pdfLaTeX and LuaLaTeX, while recommendation nonconformance remains non-fatal and journal precedence remains `conditional-manual`. No proof-state promotion occurred.

The checkpoint is not accepted because Static `34126602062` correctly found an orchestration inference defect. This failure does not authorize weakening the Static guard or changing article semantics.

## Current correction

`tests/integration_suites.py` must treat orchestration paths as neutral when at least one recognized domain-specific technical path is present. Orchestration-only remains `smoke`; unknown or force-complete non-orchestration technical paths remain `complete`. The Step 5 runtime gate also gains rendered keyword sentinels so the PDF proves keyword output for both controlled scenarios.

## Current Step 5 acceptance gate

1. corrected synchronized checkpoint passes Static;
2. mixed orchestration + Step 5 paths infer `article`, not `complete`;
3. Linux `article` runs all six first-class checks and passes;
4. both engines render controlled summary and keyword evidence for both scenarios;
5. Steps 1–4 remain green;
6. no shared non-article behavior, rule IDs, modality, locators, applicability or proof state changes;
7. only after results are recorded does Step 6 activate.

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
