# Linux Integration Scopes

Updated: 2026-09-08  
Status: ACTIVE — RELEASE PERSISTENT-CANDIDATE GUARD

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so small changes receive faster feedback. Scoped suites optimize feedback time; they do not weaken phase acceptance. Every phase transition requires `complete` Linux on the same immutable phase-end candidate.

## Available scopes

| Scope | Intended use | Can close a phase? |
|---|---|---|
| `auto` | infer narrowest safe suite from changed paths | No |
| `complete` | shared/core/standards, unknown technical paths, active certification/release candidate and phase-end regression | **Yes, with all other phase-end gates** |
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
| `smoke` | orchestration-only changes when no active candidate override applies | No |

## Automatic selection

For ordinary pull-request work, `auto` evaluates the relevant changed-path window after checkout. Synchronize events prefer previous-head to new-head when both commits are available; otherwise selection fails closed to the full PR range. Documentation-only changes normally skip heavy integration.

| Context | Scope behavior |
|---|---|
| documentation only, no active candidate | skip heavy integration |
| orchestration only, no active candidate | `smoke` |
| orchestration + recognized domain | bounded domain/union |
| orchestration + unknown technical path | `complete` |
| force-complete shared/core/standards path | `complete` |
| changed `release/final-certification-candidate.json` | `complete` |
| changed `release/v3-release-candidate.json` | `complete` |
| **active non-temporary V3 Release candidate marker present at HEAD** | **`complete` regardless of incremental changed paths** |
| unknown technical path | `complete` |

## Why Release requires a persistent HEAD-state override

Release transport probe `d1f86db10f1458ed75078239916f0de857671348` exposed a defect that a changed-path rule cannot solve by itself. Static `34253455083` passed, and Linux workflow `34253455068` concluded `success`, but the synchronize window contained only orchestration changes because `release/v3-release-candidate.json` had been introduced on an earlier push. Path inference therefore selected `smoke`, producing `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`.

That result does **not** satisfy the Release phase-end predicate. The machine policy requires `complete` and explicitly rejects workflow success with insufficient scope.

The Release correction changes the selection model from “marker must be in the current diff” to “active marker in the checked-out HEAD is candidate state.” While the marker state is `transport-probe`, `candidate-active` or `candidate-frozen`, it overrides incremental path inference to `complete`. This protects documentation-only and orchestration-only synchronize pushes after candidate activation without changing ordinary scoped behavior outside an active Release candidate.

## Exact-head Release provenance

The permanent `Linux release check` is release-artifact evidence, not merely mergeability evidence. During Release pull requests it therefore checks out the exact PR head candidate (`github.event.pull_request.head.sha`) with full Git history. This prevents deterministic-build/source-date evidence from being attributed to the synthetic PR merge commit.

The ordinary Linux integration workflow may continue testing the pull-request merge checkout; its required Release predicate is the `complete` execution scope associated with the candidate. Exact-head release artifact provenance is supplied by the permanent release-check workflow.

## Static protection

`tests/checks/release_candidate_contract.py` validates the non-temporary marker, Release base, complete-scope policy and exact-head release-check route. `tests/checks/linux_integration_suites.py` additionally proves that active Release candidate state overrides documentation-only and orchestration-only incremental path classes to `complete`.

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

Every phase transition requires `complete` Linux integration on the same immutable **phase-end regression** candidate SHA together with Static and phase-specific acceptance evidence. Release additionally requires the permanent exact-head Linux release check. Workflow `success` with a bounded scope or skipped heavy integration never satisfies a `complete`-scope phase predicate.
