# Linux Integration Scopes

Updated: 2026-09-07  
Status: ACCEPTED — STEP 5 GREEN / STEP 6 ACTIVE / CURRENT MAIN RECONCILED

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | validator-source + article profile/front-block/foreign-elements/body/recommendations | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference, layout, typography, front/back matter, objects, bibliography | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout, fonts, PDF core/geometry, math, normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry, code typography, IBGE tables, objects, minted, algorithms, documentary sources | No |
| `bibliography` | references/citation evidence | bibliography, reference spacing, normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted non-article profile compatibility | exactly six profiles, build path, multivolume, catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke | No |

## Automatic selection

For pull requests, `auto` evaluates the relevant changed-path window after checkout. Synchronize events prefer the previous-head to new-head range when both commits are locally available. If either endpoint is unavailable, the workflow fails closed to the full PR range. Documentation-only changes skip heavy integration.

| Changed-path class | Scope behavior |
|---|---|
| orchestration only | `smoke` |
| orchestration + one recognized domain | ignore orchestration paths for domain selection; run that bounded domain |
| orchestration + multiple recognized domains | run the deduplicated bounded union |
| orchestration + unknown non-orchestration technical path | `complete` |
| force-complete shared/core/standards path | `complete` |
| unknown technical path without orchestration | `complete` |

## Acceptance history

At `02e1ea6e25c008c93f8ec3ba26af7f3cea03cf14`, Static `34129625390` passed mixed orchestration/domain suite inference. Step 5 acceptance `55fa1c8dc1b503c119d564950d04141cf45ad345` then passed Static `34132291198` and Linux `34132291304`, automatically selecting `article` with `SCOPE=article PASS=6 FAIL=0 SKIP=0`.

Canonical `main` later accepted the scoped orchestration at `789c6f3f4669ae36c3d4fe831ae939a340592568`. The article branch already contained the same domain-selection model plus a stricter missing-endpoint fallback; merge `ae7e2cf2484e0b4329cc30ea80a95d0788e0e9f4` reconciles PR #286 with that current `main` ancestry.

## First-class article gates

The `article` suite contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`;
5. `scientific-article-body`;
6. `scientific-article-recommendations`.

The `profiles` suite remains exactly the six accepted non-article profiles plus compatibility checks.

## Step 6 evidence-hardening boundary

Step 6 may add a static article-evidence-map checker and rule-specific evidence markers to existing article gates. Changes under `standards/` fail closed to `complete` by current path policy. If only article test/check surfaces change without a standards path, `article` is the bounded expected domain. In either case the selected scope is execution evidence only; Step 6 acceptance still requires the synchronized Static/Linux checkpoint defined by the article plan.

Recommendations remain `recommended` + non-enforcing; journal precedence remains `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`. A rule-specific PASS marker must not be emitted for a recommendation as if it were mandatory proof ownership.

## Runner importability invariant

The coordinated runner is consumed through direct execution and dynamic loading by normative traceability/false-coverage checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Current acceptance requirement

Step 6 must preserve all six article gates, add truthful machine protection for the exact 18-rule evidence classification, and pass Static plus the Linux scope selected by changed-path policy. Only after those results are recorded may Step 6 close and Step 7 canonical article PDF work activate.

## Phase-end rule

Every phase transition requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence. Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix.
