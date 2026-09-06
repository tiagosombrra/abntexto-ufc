# Linux Integration Scopes

Updated: 2026-09-06  
Status: ACTIVE — SCOPED ORCHESTRATION CONTRACT

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a change does not wait for the complete repository regression when the affected surface is known. Scoped suites are optimization/evidence tools; they do not weaken the project acceptance model.

## Available scopes

| Scope | Intended use | Main checks | Transition authority |
|---|---|---|---|
| `auto` | Pull requests; infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | Shared/core changes, unknown technical paths, phase-end regression | all PR integration checks + normative contribution | **Yes — required for phase-end regression** |
| `article` | Scientific Article-specific implementation/evidence | article profile executable gate + article/source contract | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference, layout, typography, front/back matter, objects and bibliography surfaces | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout, fonts, PDF core/geometry, math and normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry, code typography, IBGE tables, objects, minted, algorithms, documentary sources | No |
| `bibliography` | references/citation evidence | bibliography, reference spacing, normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted non-article profile compatibility | profile matrix, build path, multivolume and catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke surface | No |

## Automatic selection

For pull requests, `auto` evaluates changed paths after checkout.

- Documentation-only changes skip heavy Linux integration.
- Article-specific test/runtime paths select `article`.
- Known domain paths select the corresponding bounded suite.
- Changes spanning multiple known domains run the union of those suites without duplicate checks.
- Shared/core, standards/integration infrastructure, or unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` also fails closed to `complete` because there is no authoritative PR-diff scope.

## Manual use

GitHub Actions -> `Linux integration` -> `Run workflow` exposes the `scope` choice. The same suites are available locally:

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite objects
python3 tests/run.py --mode pr --suite bibliography
python3 tests/run.py --mode pr --suite complete
python3 tests/run.py --mode pr --suite objects,bibliography
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Scientific Article rule

While Scientific Article is active, `article` must contain an executable article gate, not only static/source review. The current bounded suite includes `scientific-article-profile` and `validator-source`. As Steps 2–7 add article-specific executable checks, those checks must be added to the `article` suite in the same material-advance documentation cycle.

The accepted non-article `profiles` matrix remains a separate compatibility surface. A complete regression still exercises both.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and the phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
