# V3 Scientific Article — Execution Plan

Updated: 2026-09-06  
Status: ACTIVE — STEP 3 OPTIONAL FOREIGN ELEMENTS

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. The phase realizes the retained 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.

## Accepted entry evidence

| Entry requirement | Evidence | State |
|---|---|---|
| Regression Audit closed | `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2` + green audit regression | PASS |
| Core Corrections closed | `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042` | PASS |
| Reference PDF Validation closed | `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798` | PASS |
| Canonical shared PDF visually accepted | 55/55 pages, 0 unexplained visual FAIL | PASS |
| Article authority contract retained | 18 source-backed `article.*` rules | PASS |
| Shared librarian review | 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW | PASS / EXPLICIT AUTHORITY GAP |
| Shared foundation integrated into `main` | PR #285 merge `e6833ed5cf07aaf1021c690260cecfacec1a119a` | PASS |

## Step 1 — Profile and metadata surface — ACCEPTED

| Evidence | Result |
|---|---|
| Technical implementation | `b46ba2051f8c9c712a7b5d25748b81baa52b920a` |
| Synchronized acceptance | `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1` |
| Static | `34001350884` — SUCCESS |
| Linux | `34001350953` — SUCCESS, `PASS=31 FAIL=0 SKIP=0` |
| Article profile | `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2 ... presentation_rules_promoted=0` |

Step 1 added one canonical `scientific-article` profile and the article-specific metadata keys `submission-date` and `article-author-note`. No article presentation rule or proof state was promoted.

## Step 2 — Required article front block — ACCEPTED

The bounded runtime adds `abntexto-ufc/articles.def`, loaded through `abntexto-ufc.cls`, and exposes `\ufcPrintArticleFrontMatter{...}` only for `type=scientific-article`.

| Surface | Accepted behavior |
|---|---|
| Primary title | required; reuses `title`; centered, uppercase, bold, 12 pt, single-spaced |
| Primary authorship | required; reuses `author` |
| Authorship metadata | required; `article-author-note` routed through genuine LaTeX `\footnote`; rendered 10 pt |
| Submission date | required; `submission-date` |
| Approval date | required; reuses `approval-date` |
| Primary summary | required argument to `\ufcPrintArticleFrontMatter` |
| Foreign title/summary | not implemented in Step 2; owned by Step 3 |
| Article body typography | not activated; owned by Step 4 |
| Recommendations | not converted into hard failures |

### Step 2 failure history and final acceptance

| Checkpoint | Gate | Result | Classification |
|---|---|---|---|
| `768d355eda11f47b4cebbb6864247e9fc2aa728f` | Static `34003576066` | FAIL | stale pre-activation normative-currency coupling |
| `6587636f8550dcd68b3feec5bbd145551775eb4b` | Static `34003838489` | PASS | currency reconciliation accepted |
| `6587636f8550dcd68b3feec5bbd145551775eb4b` | Linux `34003838521` | FAIL, `PASS=29 FAIL=1 SKIP=1` | validator imposed unsupported `note_y >= 65%` physical-page predicate |
| `0947669c2c096dca93991e042d8ae245754688ba` | Static `34026680871` | **PASS** | synchronized corrected validator |
| `0947669c2c096dca93991e042d8ae245754688ba` | Linux `34026680882` | **PASS, `31/31`** | required front block accepted on both engines |

Final Step 2 evidence includes:

- `ARTICLE-PROFILE-EVIDENCE status=PASS engines=2`;
- `ARTICLE-FRONT-BLOCK-EVIDENCE status=PASS` on pdfLaTeX and LuaLaTeX;
- title 12 pt/centered/bold calibration;
- genuine footnote route and rendered 10 pt author note;
- no optional foreign-element promotion;
- no recommendation promotion;
- no article proof-state promotion.

Step 2 is therefore **ACCEPTED**. Its validator correction removed an unsupported geometric strengthening; it did not weaken the source-backed footnote requirement.

## Step 3 — Optional foreign elements — ACTIVE

Rules owned by this Step:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

### Runtime contract

Step 3 must provide one explicit article-only surface for foreign elements while preserving independent optionality.

| Scenario | Foreign title | Foreign summary | Required result |
|---|---|---|---|
| neither | absent | absent | compile cleanly; render neither |
| title only | present | absent | render title only |
| summary only | absent | present | render summary only |
| both | present | present | render both |

Implementation constraints:

- keep `\ufcPrintArticleFrontMatter{primary summary}` unchanged;
- add an explicit article foreign-elements route rather than infer semantics from shared `title-variant`;
- each foreign element must be independently blank-safe;
- absence must never be a compilation or validation failure;
- do not promote optional rules to required;
- do not freeze unsupported typography as new normative values;
- do not activate Step 4 body typography;
- do not modify the 18-rule proof state during ordinary Step 3 implementation.

### Step 3 evidence contract

The bounded gate must exercise all four scenarios under pdfLaTeX and LuaLaTeX and emit structured article-specific evidence. The source/evidence layer must also prove that `title-variant` was not repurposed and that body-typography activation remains absent.

Expected evidence shape:

`ARTICLE-FOREIGN-ELEMENTS-EVIDENCE status=PASS engines=2 scenarios=4 title_optional=true summary_optional=true independent=true title_variant_reused=false presentation_rules_promoted=0`

Step 3 becomes **ACCEPTED** only after a synchronized checkpoint passes Static and full Linux with this evidence and the six accepted non-article profiles remain green.

## Remaining sequence

| Step | Work | Current state | Acceptance |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static/Linux green |
| 2 | Required article front block | **ACCEPTED** | `0947669...`; Static `34026680871`; Linux `34026680882`, 31/31 PASS |
| 3 | Optional foreign elements | **ACTIVE** | four independent optionality scenarios, both engines, synchronized Static/full Linux |
| 4 | Textual structure and body typography | QUEUED | required article structure + 12 pt/justified/2 cm/single-spaced body |
| 5 | Recommendations and conditional applicability | QUEUED | advisory semantics remain advisory; journal boundary remains conditional |
| 6 | Evidence hardening | QUEUED | rule-specific positive/negative evidence and truthful proof-state promotion |
| 7 | Canonical article PDF | QUEUED | provenance-bound real PDF with complete visual inspection |
| 8 | Phase-end regression | QUEUED | Static + full Linux + article-specific acceptance on one immutable SHA |

## Non-negotiable boundaries

- One canonical `scientific-article` profile; no compatibility aliases.
- Preserve all accepted non-article profiles and the shared academic-work reference-PDF baseline.
- Reuse cross-cutting bibliography, citation, section, object and summary machinery.
- Required, optional, recommended and conditional semantics remain distinguishable in runtime and evidence.
- Recommendations never become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Item 33 remains fail-closed.
- Issue #18 remains a Final Certification/Release blocker, not an article-semantics reason.
- Every **material advance** updates handoff, roadmap, machine state, release readiness and this plan in the same work cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Current branch and next action

- Canonical base: `main` at `e6833ed5cf07aaf1021c690260cecfacec1a119a`.
- Active branch: `feat/v3-scientific-article`.
- Active PR: #286.

Next: implement Step 3 optional foreign elements and four-case evidence, synchronize all operational documentation in the same material advance, run Static and full Linux, classify any failure without weakening the article contract, and only after both are green activate Step 4.
