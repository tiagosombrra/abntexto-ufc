# Linux Integration Scopes

Updated: 2026-09-08  
Status: ACCEPTED — FINAL CERTIFICATION STEP 8 SCOPE GUARD ACTIVE

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so small changes receive faster feedback. Scoped suites optimize feedback time; they do not weaken phase acceptance. Every phase transition requires `complete` Linux on the same immutable phase-end candidate.

## Available scopes

| Scope | Intended use | Can close a phase? |
|---|---|---|
| `auto` | infer narrowest safe suite from changed paths | No |
| `complete` | shared/core/standards, unknown technical paths, certification marker and phase-end regression | **Yes, with all other phase-end gates** |
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
| `release/final-certification-candidate.json` | **`complete`** |
| unknown technical path | `complete` |

## Final Certification Step 8 scope defect and correction

Candidate `fc907856ac4ba0febf4d44fb408407a0fc2e94d4` exposed an orchestration gap. Static `34239113996` passed, and Linux workflow `34239114066` concluded `success`, but the synchronize diff from the immediately previous head to `fc907856...` contained only documentation/control-plane changes because the candidate marker had been introduced in an earlier intermediate commit. Automatic inference returned `none`, so heavy integration was skipped as `documentation-only`.

That workflow result does **not** satisfy the Final Certification phase-end predicate, which requires `complete` Linux. The candidate is rejected fail-closed.

The retry makes the intent machine-explicit:

1. `release/final-certification-candidate.json` is in `FORCE_COMPLETE_EXACT`;
2. `tests/integration_suites.py --self-test` contains marker-only and marker+orchestration cases expecting `complete`;
3. each retry candidate changes the marker itself, so the incremental synchronize window contains the force-complete path.

This is an orchestration-scope correction only; no product runtime, normative predicate or accepted validation tolerance changes.

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

Every phase transition requires `complete` Linux integration on the same immutable **phase-end regression** candidate SHA together with Static and phase-specific acceptance evidence. Final Certification additionally requires the permanent Linux release check / release matrix. Workflow `success` with heavy integration skipped never satisfies a `complete`-scope phase predicate.
