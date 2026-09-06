# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-06

## Current status

**Scientific Article is ACTIVE — Step 1 ACCEPTED; scoped Linux orchestration is the current infrastructure checkpoint before repository integration.**

The shared academic-work foundation is closed and accepted:

- Regression Audit — CLOSED;
- Core Corrections — CLOSED on `5f67560aeded1e6b4f77f4a31e14a91f3181a4da`, Static `33982156041`, Linux `33982156042`;
- Reference PDF Validation — CLOSED on `b64074c64941895f97fbe0f795ce826c798d17ce`, Static `33985595790`, Linux `33985595798`, with 55/55 visual PASS.

Scientific Article Step 1 is accepted on synchronized checkpoint `08b878a21c5b901e47dbf80f5c4dd2fb9043c1a1`: Static `34001350884` SUCCESS and full Linux `34001350953` SUCCESS with `PASS=31 FAIL=0 SKIP=0`.

The librarian-review matrix remains **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.  
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.  
Active phase plan: `docs/V3-SCIENTIFIC-ARTICLE.md`.  
Linux scope contract: `docs/LINUX-INTEGRATION-SCOPES.md`.  
Release readiness: `docs/V3-RELEASE-READINESS.md`.  
Article authority contract: `docs/ARTICLE-NORMATIVE-CONTRACT.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, article proof/evidence state, Linux integration scope policy, acceptance state, current work, artifact provenance, release blockers, temporary-executor lifecycle or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Scoped Linux runs, targeted checks, compile success and visual inspection do not replace that gate. Phase-end Linux uses the `complete` scope.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | Green phase-end regression and stable 34-item contract. |
| **Core Corrections** | CLOSED | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | `5f67560a...` passed Static/full Linux. |
| **Reference PDF Validation** | CLOSED | Validate the corrected canonical academic-work PDF page by page. | `b64074c...` passed Static/full Linux after provenance + 55/55 visual PASS. |
| **Scientific Article** | **ACTIVE — STEP 1 ACCEPTED** | Implement one canonical article profile using the retained 18-rule contract. | Article runtime, article-specific evidence, canonical article rendering and `complete` phase-end regression pass on one immutable SHA. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification and release reproducibility proof. | Heavy certification matrix plus deterministic release-reference-PDF evidence green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Issue #18 resolved; release checklist complete; final regression recorded. |

## Linux integration orchestration

The permanent `Linux integration` workflow now has named scopes instead of treating every technical synchronization as a complete repository run.

| Scope | Primary purpose | Phase-transition authority |
|---|---|---|
| `auto` | infer scope from PR changes | No |
| `article` | article profile/runtime/evidence | No |
| `reference-document` / `reference-pdf` | canonical document/presentation | No |
| `frontmatter` / `layout` / `objects` / `bibliography` / `backmatter` | bounded shared domains | No |
| `research-project` / `profiles` | profile-specific compatibility | No |
| `smoke` | workflow/runner orchestration changes | No |
| `complete` | full PR integration and phase-end regression | **Yes — required at phase end** |

For PR `synchronize`, `auto` uses the incremental push diff rather than the complete historic PR diff. Initial/reopened/ready events use the full PR diff. Unknown technical paths, shared/core surfaces and standards/integration infrastructure fail closed to `complete`. Documentation-only updates skip heavy Linux.

Manual `workflow_dispatch` exposes all named scopes. Manual `auto` resolves to `complete` because no PR-diff scope is authoritative.

## Scientific Article execution state

| Step | Work | State | Acceptance gate |
|---:|---|---|---|
| 1 | Profile and metadata surface | **ACCEPTED** | `08b878a...`; Static `34001350884`; Linux `34001350953` |
| CI | Scoped Linux integration orchestration | **CURRENT** | Static contract + bounded synchronize run prove selection/runner contract |
| 2 | Required article front block | NEXT AFTER BRANCH TRANSITION | Primary title, authorship metadata footnote, submission/approval dates and primary summary have article-specific rendered evidence |
| 3 | Optional foreign elements | QUEUED | Foreign title/summary can be absent or present without becoming mandatory |
| 4 | Textual structure and body typography | QUEUED | Required article structure and body typography validated with shared infrastructure |
| 5 | Recommendations and conditional boundary | QUEUED | Recommendations remain advisory; journal instructions remain conditional |
| 6 | Evidence hardening | QUEUED | Positive/negative article evidence is rule-specific and proof state truthful |
| 7 | Canonical article PDF | QUEUED | Real Git-bound TeX Live 2026 artifact with complete visual review |
| 8 | Phase-end regression | QUEUED | Static + `complete` Linux + article-specific acceptance on one immutable SHA |

The `article` suite currently contains the retained authority/source gate plus the executable two-engine `scientific-article-profile` gate. Every new article-specific executable check added in Steps 2–7 must join this suite in the same material-advance cycle.

## Repository integration and branch plan

PR #285 remains the integration boundary for the corrected shared foundation plus Scientific Article Step 1. The bounded Linux orchestration improvement is being validated on that same transition branch before merge. After merge, create `feat/v3-scientific-article` from updated `main` and continue Step 2 there.

## Known v3.0.0 blockers and tracked debt

| Item | State | Owner / treatment |
|---|---|---|
| Scientific Article phase / #280 | ACTIVE | finish Steps 2–8 and phase-end regression |
| Release reference PDF bit reproducibility / #18 | OPEN — RELEASE BLOCKER | Final Certification/Release must pin release epoch/`SOURCE_DATE_EPOCH` and compare rebuilt hashes |
| Librarian-review item 33 | NORMATIVE-REVIEW | explicit authority gap; no speculative runtime change |
| Historical branch clutter | NON-BLOCKING HYGIENE | provenance only; active work follows `main` + one current task branch |

## Gate before Final Certification

Scientific Article must close with no article runtime FAIL, truthful article proof state, accepted canonical article rendering, synchronized documentation, no temporary executor, and one immutable phase-end candidate green on Static plus `complete` Linux integration and article-specific acceptance.

## Gate before Release

Final Certification must prove the profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix. Issue #18 must also be resolved with deterministic release reference-PDF evidence.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. Historical labels are retained only when identifying old evidence. GitHub issue/PR numbers and immutable SHAs provide traceability.
