# Linux Integration Scopes

Updated: 2026-09-07  
Status: IMPLEMENTED — IMPORT-BOUNDARY FIX PENDING CI

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

## First technical synchronize result

PR #287 technical checkpoint `d089215e540b1e63bc8921cd5b4ab69497e8bc42` correctly selected `smoke`, proving the incremental orchestration path was active. Static remained green, but Linux run `34137588237` failed with `SCOPE=smoke PASS=3 FAIL=1 SKIP=0`.

The sole failure was `validator-source`. `tests/checks/normative_traceability.py` loads `tests/run.py` through `importlib.util.spec_from_file_location`; after `run.py` gained the sibling import `from integration_suites import SUITES`, that file-spec import no longer had the `tests/` directory on `sys.path`, producing `ModuleNotFoundError: No module named 'integration_suites'`.

This is an orchestration/import-boundary defect, not a normative, LaTeX, article-runtime, reference-PDF, or validator-predicate failure. The correction makes `tests/run.py` self-contained when loaded by file spec and adds a Static regression probe that loads the runner from an isolated Python interpreter. No suite, evidence predicate, authority rule or runtime requirement is weakened.

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

While Scientific Article is active, `article` must contain executable article evidence, not only source review. The bounded suite includes `scientific-article-profile` and `validator-source`. As later article steps add executable gates, those gates join the `article` suite in the same material-advance cycle.

The accepted non-article profile matrix remains separate compatibility evidence. Complete regression exercises both.

## Acceptance plan for this infrastructure batch

1. PR #287 is open from `ci/scoped-linux-integration` to `main`;
2. the first technical synchronize selected `smoke` but exposed the runner file-spec import defect in Linux `34137588237`;
3. publish the bounded import fix together with this failure classification;
4. require Static and the next synchronize Linux run to pass with `smoke`;
5. record the accepted checkpoint and run IDs in all control documents;
6. merge PR #287;
7. reconcile the existing `feat/v3-scientific-article` PR branch with updated `main` before continuing article runtime work.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.
