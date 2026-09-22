# Linux Integration Scopes

Updated: 2026-09-19

## Purpose

The permanent `Linux integration` workflow supports bounded suites for fast pull-request feedback while preserving fail-closed behavior for changes whose impact is broad or unknown.

Scoped suites are an optimization. They do not replace complete release-grade validation when the change affects the canonical runtime, standards authority, release control or another force-complete surface.

## Available scopes

| Scope | Intended use |
|---|---|
| `auto` | infer the safest scope from the complete PR diff |
| `complete` | run all PR integration checks |
| `article` | scientific-article behavior/evidence |
| `reference-document` | canonical reference source/corpus |
| `reference-pdf` | presentation-sensitive reference PDF |
| `frontmatter` | cover/title/approval/pre-textual behavior |
| `layout` | page/body/geometry/math/quotation |
| `objects` | figures/tables/code/algorithms/documentary sources |
| `bibliography` | references/citation behavior |
| `backmatter` | appendices/annexes/index/glossary |
| `research-project` | research-project profile |
| `profiles` | supported non-article profile compatibility |
| `distribution` | public/distribution bundle behavior |
| `web-lite` | browser validator source + E2E preparation |
| `smoke` | orchestration-only changes |

## Automatic pull-request selection

For non-draft pull requests, `auto` classifies the **complete PR diff** rather than only the last synchronize window. This prevents a later documentation-only commit from replacing a required technical run with a superficial skip.

Current behavior:

- documentation-only changes may skip heavy Linux integration;
- orchestration-only changes select `smoke`;
- recognized test/domain paths select the relevant bounded suite or union;
- unknown technical paths fail closed to `complete`;
- `Makefile`, the canonical `abntexto-ufc.cls`, controlled standards paths and the active release marker force `complete`;
- if `release/v3-release-candidate.json` changes anywhere in the PR, `complete` dominates all narrower scope decisions.

The exact mapping is implemented by `tests/integration_suites.py` and protected by `tests/checks/repository/linux_integration_suites.py`.

## Main-branch release-marker behavior

A push to `main` that changes `release/v3-release-candidate.json` forces complete Linux integration.

This ensures that a control transition such as development-state change or candidate freeze receives validation on the exact post-merge `main` SHA rather than relying only on a PR-head result.

The marker is release/development-state provenance and orchestration. It does not by itself alter document formatting semantics.

## Complete validation

Use complete Linux integration when:

- the canonical runtime changes;
- standards/current authority changes;
- the release marker changes;
- an unknown technical path changes;
- a bounded scope cannot safely represent the impact;
- release-grade certification is required.

A successful workflow where heavy integration was skipped is not evidence of a complete validation run.

Linux Release Check is a distinct release-grade workflow and is not interchangeable with Linux Integration.

## Runner importability

The coordinated runner is used both through direct execution and dynamic loading by evidence/traceability checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use:

```sh
python3 tests/run.py --list-suites
```

to inspect the current suite/check mapping.

## Acceptance rule

A material change is accepted only with the validation scope required by its actual impact.

When complete validation is required, Static Contract, complete Linux Integration and any required release-grade checks must all refer to the intended candidate/source state. A narrow green suite cannot be substituted for a required complete run.
