# Linux Integration Scopes

Updated: 2026-09-07  
Status: ACTIVE — MIXED ORCHESTRATION/DOMAIN INFERENCE CORRECTION PENDING CI

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

For pull requests, `auto` evaluates the relevant changed-path window after checkout. Synchronize events prefer the previous-head to new-head range when both commits are available and otherwise fail closed to the full PR range. Documentation-only changes skip heavy integration.

The corrected domain-selection rule is:

| Changed-path class | Scope behavior |
|---|---|
| orchestration only | `smoke` |
| orchestration + one recognized domain | ignore orchestration paths for domain selection; run that bounded domain |
| orchestration + multiple recognized domains | run the deduplicated bounded union |
| orchestration + unknown non-orchestration technical path | `complete` |
| force-complete shared/core/standards path | `complete` |
| unknown technical path without orchestration | `complete` |

This preserves the intended policy that orchestration changes do not accidentally broaden a known bounded domain, while fail-closed handling remains intact for unknown or shared technical surfaces.

## Step 5 failure classification

At `6507da00275d8a69093541d6e6cb119a1b6f6cb3`, complete Linux `34126602083` passed all 36 checks, including all six article gates. Static `34126602062` correctly failed because `tests/run.py` combined with an article path was still processed as an unmatched technical path and therefore returned `complete`.

`tests/checks/linux_integration_suites.py` is the correct guard and is not weakened. The fix is confined to inference semantics plus extra self-test cases for mixed orchestration/domain and orchestration/unknown-path behavior.

## First-class article gates

The `article` suite contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`;
5. `scientific-article-body`;
6. `scientific-article-recommendations`.

The `profiles` suite remains exactly the six accepted non-article profiles plus compatibility checks.

## Step 5 evidence hardening

`scientific-article-recommendations` compiles a recommendation-following scenario and an outside-recommendation scenario with pdfLaTeX and LuaLaTeX. The current correction adds unique rendered keyword sentinels to both scenarios. Successful extraction must demonstrate not only compilation and paragraph rendering but also keyword rendering while the outside scenario remains valid despite being below the advisory keyword count.

Recommendations remain `recommended` + `manual`; journal precedence remains `required-when-applicable`, `conditional-manual`, applicability `target-journal-submission`; no proof-state promotion occurs.

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

The synchronized Step 5 correction candidate must pass Static and automatically select bounded Linux `article`, with all six checks green and both two-engine recommendation scenarios producing their controlled rendered markers. Only after those results are recorded may Step 5 close and Step 6 activate.

## Phase-end rule

Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence. Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix.
