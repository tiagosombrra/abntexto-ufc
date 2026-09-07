# V3 Scientific Article — Execution Plan

Updated: 2026-09-07  
Status: ACTIVE — STEP 6 IMPLEMENTED / CI ACCEPTANCE PENDING

## Entry and current state

Core Corrections and Reference PDF Validation are closed. Canonical `main` is `fbf7cc4839ce318024a7d1ed517dd50fab5773ac`; PR #288 corrected the stale root README and main control-plane documentation. Active article work remains PR #286 on `feat/v3-scientific-article`, reconciled with current main through `85cf22b6fe5d117bb2611a2865911e0d20a19363`.

The retained article authority product remains `4d018a92697e8f39e3a53b034c451e55996c84fb`, represented by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`. There are exactly 18 source-backed article rules.

## Progress

| Step | Work | State | Evidence / next gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | ACCEPTED | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| 2 | Required article front block | ACCEPTED | `0947669...`; Static `34026680871`; Linux `34026680882` |
| 3 | Optional foreign title and summary | ACCEPTED | `82d20fa...`; Static `34031144114`; Linux `34031144269` |
| 4 | Textual structure and body typography | ACCEPTED | `005956bd...`; Static `34119007413`; Linux `34119007425` |
| 5 | Recommendations and conditional applicability | ACCEPTED | `55fa1c8...`; Static `34132291198`; Linux `34132291304`; article scope `PASS=6 FAIL=0 SKIP=0` |
| 6 | Evidence hardening | **IMPLEMENTED — CI PENDING** | exact 18-rule map + dedicated Static checker; zero validation-mode promotions |
| 7 | Canonical article PDF | QUEUED | real TeX Live 2026 PDF + provenance + complete page-level visual inspection |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific evidence on one immutable SHA |

## Step 6 implementation

Step 6 adds `standards/article-evidence-map.json` and `tests/checks/scientific_article_evidence_map.py`, wired into `tests/static.py`.

The map covers exactly all 18 retained IDs and records, for each rule:

- source-contract normativity;
- current validation mode;
- direct article-specific owner when one exists;
- evidence kind;
- conservative proof disposition;
- whether validation was promoted.

The Step 6 implementation intentionally promotes **zero** validation modes. The source contract remains unchanged. Direct article-specific executable support is recorded as support, not manufactured normative proof.

### Evidence families

| Rule family | Current direct article evidence | Step 6 disposition |
|---|---|---|
| primary title, authorship, primary summary, dates, title typography, author metadata footnote | `scientific-article-front-block` | article-specific executable support; still manual in source contract |
| introduction, development, final considerations, references, body typography | `scientific-article-body` | article-specific executable support; development also has controlled negative evidence |
| foreign title / foreign summary | `scientific-article-foreign-elements` | optional present/absent matrix; optionality preserved |
| author alignment and summary recommendations | `scientific-article-recommendations` | advisory non-enforcing support only |
| target-journal precedence | source/applicability boundary | remains required-when-applicable + conditional-manual; no generic executable owner |

The dedicated checker rejects missing/duplicate/unknown IDs, normativity or validation-mode drift, nonexistent/non-article owners, recommendation enforcement, optionality loss, and journal-precedence automation.

## Step 6 acceptance gate

Step 6 becomes ACCEPTED only after the synchronized technical checkpoint passes:

1. Static contract, including `ARTICLE-EVIDENCE-MAP-EVIDENCE status=PASS rules=18`;
2. Linux scope selected by changed-path policy;
3. existing Steps 1–5 remain green;
4. no unauthorized source-contract/modality/locator/applicability change.

## Step 7 canonical article PDF

After Step 6 acceptance, produce a real article PDF from the accepted branch using project build/runtime and TeX Live 2026. Bind the artifact to Git provenance and inspect every page. Review must cover article-specific front block, optional elements, typography, body structure, citations/references, footnotes and absence of academic-work front-matter leakage.

Synthetic PDFs do not satisfy Step 7.

## Step 8 phase-end regression

Scientific Article closes only when one immutable candidate passes Static contract, Linux integration with **complete** scope, all article-specific executable gates and accepted canonical article PDF visual/provenance evidence.

Scoped article checks are intermediate evidence only and never replace Step 8.

## What remains after Scientific Article

Final Certification must still cover the complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must establish deterministic release-reference-PDF reproducibility with pinned epoch/SOURCE_DATE_EPOCH and stable hash evidence. Release then finalizes bundles, checksums, tag/GitHub Release and any external publication action.

Librarian review remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Documentation discipline

Every **material advance** updates the relevant execution documentation in the same work cycle. Every phase ends with a complete **phase-end regression** on one immutable SHA.
