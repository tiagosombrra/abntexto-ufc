# Linux Integration Scopes

Updated: 2026-09-08  
Status: ACCEPTED — RELEASE PHASE-END SCOPE GUARD PREPARED

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so small changes receive faster feedback. Scoped suites optimize feedback time; they do not weaken phase acceptance. Every phase transition/closeout requires `complete` Linux on the same immutable phase-end candidate.

## Available scopes

| Scope | Intended use | Can close a phase? |
|---|---|---|
| `auto` | infer narrowest safe suite from changed paths | No |
| `complete` | shared/core/standards, unknown technical paths, certification/release markers and phase-end regression | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | No |
| `reference-document` | canonical reference source/corpus | No |
| `reference-pdf` | presentation-sensitive reference PDF | No |
| `frontmatter` | cover/title/approval/pre-textual | No |
| `layout` | page/body/geometry/math/quotation | No |
| `objects` | figures/tables/code/algorithms/documentary sources | No |
| `bibliography` | references/citation evidence | No |
| `backmatter` | appendices/annexes/index/glossary | No |
| `research-project` | research-project profile | No |
| `profiles` | non-article profile compatibility | No |
| `smoke` | orchestration-only changes | No |

## Automatic selection

For pull requests, `auto` evaluates the relevant changed-path window after checkout. Synchronize events prefer previous-head to new-head when both commits are available; otherwise selection fails closed to the full PR range. Documentation-only changes skip heavy integration.

| Changed-path class | Scope behavior |
|---|---|
| orchestration only | `smoke` |
| orchestration + recognized domain | bounded domain/union |
| orchestration + unknown technical path | `complete` |
| force-complete shared/core/standards path | `complete` |
| `release/final-certification-candidate.json` | `complete` — historical Final Certification candidate transport |
| `release/v3-release-candidate.json` | **`complete` — Release phase-end candidate transport** |
| unknown technical path | `complete` |

## Candidate-marker provenance

Final Certification exposed an orchestration defect when a phase-end candidate workflow concluded `success` while heavy Linux was skipped. The accepted correction established a tracked force-complete marker and self-tests.

Release preserves that lesson without reusing Final Certification identity:

1. `release/final-certification-candidate.json` remains historical Final Certification transport;
2. `release/v3-release-candidate.json` is the Release-specific transport;
3. both marker-only and marker-plus-orchestration cases must infer `complete`;
4. the permanent `Linux release check` PR path filter includes the Release marker;
5. the marker is provenance/orchestration only and does not alter product or normative behavior.

`docs/V3-RELEASE-PHASE-END.md` defines the Release candidate and acceptance semantics.

## Runner importability invariant

The coordinated runner is consumed through direct execution and dynamic loading by normative traceability/false-coverage checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Phase-end rule

Every phase closeout requires `complete` Linux integration on the same immutable **phase-end regression** candidate SHA together with Static and phase-specific acceptance evidence. Release additionally requires the permanent `Linux release check`. Workflow `success` with heavy integration skipped never satisfies a `complete`-scope phase predicate.
