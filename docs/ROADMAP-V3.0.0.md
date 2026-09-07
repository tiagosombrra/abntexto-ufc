# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-07

## Current status

**Scientific Article is ACTIVE at Step 5 — recommendations and conditional applicability.**

| Phase | Status | Accepted evidence / exit gate |
|---|---|---|
| Regression Audit | CLOSED | green regression and stable 34-item review contract |
| Core Corrections | CLOSED | `5f67560a...`; Static `33982156041`; Linux `33982156042` |
| Reference PDF Validation | CLOSED | `b64074c...`; Static `33985595790`; Linux `33985595798`; 55/55 visual PASS |
| Scientific Article | **ACTIVE — STEP 5** | Steps 1–4 accepted; Step 4 checkpoint `005956bd...` passed Static `34119007413` and Linux `34119007425`, `SCOPE=article PASS=5 FAIL=0 SKIP=0` |
| Final Certification | QUEUED | full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution/reproducibility certification |
| Release | QUEUED | release assets/checksums/tag/publication and final regression |

## Scientific Article progress

| Step | Work | State | Evidence / gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | **ACCEPTED** | `005956bd...`; Static `34119007413`; Linux `34119007425`; article PASS=5 FAIL=0; both engines 12 pt / justified / 2 cm / 13.800 pt; negative missing-Development predicate PASS |
| 5 | Recommendations and conditional applicability | **ACTIVE** | prove recommended values remain advisory and journal precedence remains conditional/manual |
| 6 | Evidence hardening | QUEUED | rule-specific evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF plus complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 4 accepted result

The accepted Step 4 runtime uses supported `\singlesp` and an article-only `cmd/textual/after` reapplication route. Linux `34119007425` emitted two physical `ARTICLE-BODY-EVIDENCE` PASS records with 12 pt body type, 2 cm first-line indent (`57.125 pt`, delta `0.432 pt`), justified non-final lines, and `13.800 pt` body spacing equal to same-document single-spacing calibration. The negative missing-Development fixture was rejected by the intended rendered-heading predicate. Proof state remained unpromoted.

## Step 5 contract

| Retained rule | Modality | Step 5 acceptance meaning |
|---|---|---|
| `article.authorship.alignment.recommended` | recommended | right alignment may be the generic default but must not be a hard validity condition |
| `article.summary.word-count.recommended` | recommended | 150–250 words must not become a compile/validation rejection boundary |
| `article.summary.keywords.minimum.recommended` | recommended | fewer than three keywords must not become a hard rejection boundary |
| `article.summary.single-paragraph.recommended` | recommended | multi-paragraph summary input must not be rejected solely for violating the recommendation |
| `article.journal-guidelines.precedence` | required-when-applicable | a target journal requires checking its instructions; generic UFC profile remains fallback and cannot assert journal compliance |

Step 5 should favor evidence and documentation over new runtime constraints. If user-facing keyword support is added, it must remain optional in the generic profile unless the retained authority contract is formally expanded with source-backed required-element evidence.

## Current Step 5 acceptance gate

1. executable evidence demonstrates recommendations are advisory, not hard failures;
2. journal precedence remains conditional/manual and applicability-bound;
3. Steps 1–4 stay green in article scope;
4. no shared non-article behavior changes;
5. 18-rule source contract IDs, normativity, locators and proof-state semantics remain stable;
6. synchronized Static and article Linux pass before Step 6 activates.

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
