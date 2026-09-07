# Linux Integration Scopes

Updated: 2026-09-07  
Status: ACCEPTED — PR #287 READY TO MERGE

## Purpose

The permanent `Linux integration` workflow uses bounded suites for intermediate work so known local changes do not wait for the complete repository regression. Scoped suites are optimization/evidence tools only; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Transition authority |
|---|---|---|---|
| `auto` | Pull requests; infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | Shared/core changes, unknown technical paths, phase-end regression | all PR integration checks + normative contribution | **Yes — required for phase-end regression** |
| `article` | Scientific Article-specific implementation/evidence | executable article gate + article/source contract | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference/layout/front-back/object/bibliography surfaces | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout/fonts/PDF geometry/math/normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry/code/IBGE/minted/algorithm/source gates | No |
| `bibliography` | references/citation evidence | bibliography/reference spacing/normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted profile compatibility | profile matrix/build path/multivolume/catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke surface | No |

## Accepted orchestration evidence

| Checkpoint | Static | Linux | Result |
|---|---|---|---|
| `d089215e540b1e63bc8921cd5b4ab69497e8bc42` | `34137588226` FAIL | `34137588237` FAIL | Correctly selected `smoke`, but exposed runner file-spec import defect |
| `47ac2e27c5c2f6797269ccc4e1c07caafea1c643` | `34139608322` SUCCESS | `34139608364` SUCCESS | **ACCEPTED** — `SCOPE=smoke PASS=4 FAIL=0 SKIP=0` |

The accepted Static run also emitted:

`LINUX-SUITE-EVIDENCE status=PASS suites=12 checks=33 manual_choices=13 phase=scientific-article unknown_path_fallback=complete article_executable=true runner_file_spec_import=true`

The accepted Linux run proved that a synchronize range containing orchestration-only technical changes selects `smoke`, and all four smoke checks passed: repository contract, validator/source contract, reference document and PDF validator.

## Failure classification and correction

The rejected checkpoint failed because `tests/checks/normative_traceability.py` loads `tests/run.py` through `importlib.util.spec_from_file_location`, while the runner's new sibling import `integration_suites` depended on invocation-path `sys.path` behavior.

The accepted correction:

- makes `tests/run.py` add its own directory before importing the sibling suite module;
- adds an isolated file-spec import probe to the permanent Static orchestration contract;
- changes no suite membership, normative predicate, authority source, LaTeX runtime or article rule.

## Automatic selection contract

For pull requests, `auto` evaluates changed paths after checkout.

- Initial/open/reopen/ready events use the full PR diff.
- `synchronize` events use the incremental pushed range when GitHub supplies `before` and `after`.
- Documentation-only changes skip heavy Linux integration.
- Article-specific runtime/test paths select `article`.
- Known domain paths select the corresponding bounded suite.
- Changes spanning multiple known domains run the union of those suites without duplicate checks.
- Shared/core, standards/integration infrastructure, or unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` fails closed to `complete` because no authoritative PR diff exists.

## Manual use

GitHub Actions -> `Linux integration` -> `Run workflow` exposes the `scope` choice. The same suites are available locally through:

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite objects
python3 tests/run.py --mode pr --suite bibliography
python3 tests/run.py --mode pr --suite complete
python3 tests/run.py --mode pr --suite objects,bibliography
```

`python3 tests/run.py --list-suites` lists the current mapping.

## Scientific Article rule

While Scientific Article is active, `article` contains executable article evidence plus the source/validator contract. As later article steps add executable gates, those gates join the `article` suite in the same material-advance cycle.

The accepted non-article profile matrix remains separate compatibility evidence. Complete regression exercises both.

## Next action

1. merge PR #287 after this acceptance synchronization remains Static-clean;
2. reconcile existing PR #286 / `feat/v3-scientific-article` with updated `main`;
3. obtain executable `article`-scope evidence for its pending Step 4 structural checker state;
4. continue the Scientific Article plan from the reconciled accepted step.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.
