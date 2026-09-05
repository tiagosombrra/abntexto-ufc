# V3 Scientific Article — Execution Plan

Updated: 2026-09-05  
Status: ACTIVE — ENTRY / RUNTIME NOT YET IMPLEMENTED

## Purpose

Implement and validate one canonical `scientific-article` profile on top of the corrected, visually accepted shared V3 foundation. This phase must realize the 18-rule source-backed article contract without forking cross-cutting infrastructure or weakening already accepted non-article behavior.

Authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `standards/coverage-rules-article.json`.

## Accepted entry evidence

| Entry requirement | Evidence | State |
|---|---|---|
| Regression Audit closed | `ee2ab6e6404cbeb15447f694e998c78a9d5d8dc2` + green audit regression | PASS |
| Core Corrections closed | `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`; Static `33982156041`; Linux `33982156042` | PASS |
| Reference PDF Validation closed | `b64074c64941895f97fbe0f795ce826c798d17ce`; Static `33985595790`; Linux `33985595798` | PASS |
| Canonical shared PDF visually accepted | 55/55 pages, 0 unexplained visual FAIL | PASS |
| Article authority contract retained | 18 source-backed `article.*` rules | PASS |
| Shared librarian review state | 33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW | PASS / EXPLICIT AUTHORITY GAP |
| Temporary executors | none active | PASS |

## Initial runtime inspection

`abntexto-ufc/core.def` currently defines the six accepted non-article document types but has no `type / scientific-article` choice. Therefore article runtime is not silently present and no article rule may be treated as implemented at phase entry.

The article rules are still `manual` / `conditional-manual`. Shared green mechanisms are reusable infrastructure, not article proof.

## Non-negotiable boundaries

- Add one canonical `scientific-article` profile; no compatibility aliases or retired Portuguese machine identifiers.
- Preserve all accepted non-article profiles and the shared academic-work reference-PDF baseline.
- Reuse bibliography, citation, section, summary and object machinery rather than fork it.
- Do not change article rule IDs, authority, modality, expected values, locators or applicability without new current source evidence and a separately documented source correction.
- Required, optional, recommended and conditional rules must remain distinguishable in runtime and evidence.
- Recommendations must not become hard compilation/validation failures.
- Journal-specific instructions remain a conditional applicability boundary.
- Item 33 of the librarian review remains fail-closed; article work must not resolve it by inference.
- Every material advance updates handoff, roadmap, machine state and this plan in the same cycle.
- The phase ends only after a complete **phase-end regression** on one immutable candidate.

## Implementation sequence

### 1. Profile and metadata surface

Goal: introduce the canonical profile without changing unrelated behavior.

Work:

- add `type / scientific-article` to the current direct-owned V3 type system;
- determine the minimal article metadata keys required by the 18-rule contract;
- avoid duplicate metadata when an existing generic field already satisfies the article meaning;
- add a minimal positive compile fixture proving profile selection and routing;
- add residual/static protection against aliases and retired identifiers.

Acceptance:

- profile compiles through the supported current architecture;
- existing six non-article profiles remain green;
- no article presentation/proof state is promoted merely from profile registration.

### 2. Required article front block

Goal: implement required article elements before textual-body rules.

Rules:

- `article.title.primary.required`;
- `article.authorship.required`;
- `article.summary.primary.required`;
- `article.dates.submission-approval.required`;
- `article.title.primary.typography`;
- `article.authorship.metadata.footnote`.

Acceptance:

- article-specific positive fixtures/rendered evidence exist for every required element;
- title presentation is measured/observed against the frozen 12 pt, bold, uppercase, centered, single-spaced contract;
- complementary author metadata is demonstrably placed in a footnote;
- submission/approval dates are present in the article route without contaminating non-article front matter.

### 3. Optional foreign elements

Goal: support optional foreign-language surfaces without making them mandatory.

Rules:

- `article.title.foreign.optional`;
- `article.summary.foreign.optional`.

Acceptance:

- article compiles with both elements absent;
- article compiles with one or both present;
- absence is not reported as failure.

### 4. Textual structure and body typography

Goal: implement required textual structure while reusing shared infrastructure.

Rules:

- `article.introduction.required`;
- `article.development.required`;
- `article.final-considerations.required`;
- `article.references.required`;
- `article.body.typography`.

Acceptance:

- controlled article fixture contains the required sections/references;
- body typography is article-specific 12 pt, justified, 2 cm first-line indent, single-spaced;
- citations/references/objects continue through current shared machinery;
- no duplicate article-only bibliography or section implementation is introduced.

### 5. Recommendations and conditional applicability

Goal: encode guidance truthfully rather than over-enforce it.

Rules:

- `article.authorship.alignment.recommended`;
- `article.summary.word-count.recommended`;
- `article.summary.keywords.minimum.recommended`;
- `article.summary.single-paragraph.recommended`;
- `article.journal-guidelines.precedence`.

Acceptance:

- recommendation evidence is advisory and distinguishable from hard failure;
- article documents outside recommended ranges can still compile unless another actual required rule is violated;
- journal-specific precedence remains conditional/manual and is never represented as generic-profile supremacy.

### 6. Evidence hardening

Goal: make article proof fail-closed and rule-specific.

Work:

- register article-specific runner gates only for predicates actually implemented;
- add positive evidence for every promoted rule;
- add controlled negative evidence where a safe machine-rejectable case exists;
- couple negative rejection to positive PASS for the same rule;
- update coverage/contribution/proof classifications only from real article evidence;
- keep unsupported/manual rules manual.

Acceptance:

- no mechanism-only or shared-evidence proof promotion;
- source/currency/precedence/locator/traceability checks remain green;
- non-article `make check` behavior remains green.

### 7. Canonical article PDF

Goal: validate the article as a rendered document.

Work:

- build a real canonical article PDF from one Git-bound SHA using TeX Live 2026;
- record provenance, digest, engine, page geometry and font embedding;
- render every page and perform complete visual inspection;
- inspect title/authorship/footnote/dates/summary/body/references plus optional routes;
- classify any defect before modifying runtime or tests;
- remove any temporary build executor before checkpoint acceptance.

Acceptance:

- provenance-bound article artifact;
- complete visual PASS or explicitly classified/corrected defects followed by rebuild/re-render;
- no unexplained regression against the accepted shared foundation.

### 8. Phase-end regression

Freeze one immutable Scientific Article candidate and require on the same SHA:

1. Static contract;
2. full Linux integration;
3. complete article-specific positive/negative evidence;
4. existing non-article regression suite green;
5. accepted canonical article PDF and visual review;
6. synchronized documentation/machine state;
7. no temporary executor.

Only after those results are recorded may **Scientific Article** become `CLOSED` and **Final Certification** become `ACTIVE`.

## First concrete action

Start with **Profile and metadata surface**. Before writing presentation macros, inspect the current public metadata fields and reuse them where possible. The first technical commit should be deliberately narrow: canonical profile routing + minimal compile fixture + static residual protection, with no speculative proof-state promotion.
