# Linux Integration Scopes

Updated: 2026-09-07  
Status: PLANNED — IMPLEMENTATION NEXT

## Purpose

The permanent `Linux integration` workflow may use bounded suites for intermediate work so known local changes do not wait for the complete repository regression. Scoped suites are optimization/evidence tools only; they do not weaken phase acceptance.

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

## Manual use

After implementation, GitHub Actions -> `Linux integration` -> `Run workflow` exposes the `scope` choice. The same suites are available locally through:

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite objects
python3 tests/run.py --mode pr --suite bibliography
python3 tests/run.py --mode pr --suite complete
python3 tests/run.py --mode pr --suite objects,bibliography
```

`python3 tests/run.py --list-suites` lists the current mapping.

## Scientific Article rule

While Scientific Article is active, `article` must contain executable article evidence, not only source review. At implementation entry the bounded suite must include `scientific-article-profile` and `validator-source`. As Steps 2–7 add article-specific executable gates, those gates must join the `article` suite in the same material-advance cycle.

The accepted non-article profile matrix remains separate compatibility evidence. Complete regression exercises both.

## Acceptance plan for this infrastructure batch

1. open a documentation-only PR from `ci/scoped-linux-integration` so the current workflow records documentation-only behavior;
2. push the technical orchestration as a `synchronize` event;
3. require Static to validate suite mappings and workflow contract;
4. require the technical synchronize run to choose bounded `smoke` for orchestration-only changes;
5. record the technical checkpoint and workflow run IDs;
6. merge the infrastructure PR;
7. create `feat/v3-scientific-article` from updated `main` and continue Step 2.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.
