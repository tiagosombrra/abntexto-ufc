# Linux Integration Scopes

Updated: 2026-09-06  
Status: IMPLEMENTED — CI ACCEPTANCE PENDING

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | Pull requests; infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | Shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, when combined with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | authority/source contract + article profile + required front block + optional foreign elements | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference, layout, typography, front/back matter, objects and bibliography surfaces | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout, fonts, PDF core/geometry, math and normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry, code typography, IBGE tables, objects, minted, algorithms, documentary sources | No |
| `bibliography` | references/citation evidence | bibliography, reference spacing, normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted non-article profile compatibility | six-profile matrix, build path, multivolume and catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke surface | No |

## Automatic selection

For pull requests, `auto` evaluates the relevant changed-path window after checkout.

- On `synchronize`, it compares the previous PR head (`before`) with the new PR head (`after`). This prevents an old long-lived PR diff from forcing a complete run after every new commit.
- On opened, reopened and ready-for-review events, it uses the full PR diff.
- Documentation-only changes skip heavy Linux integration.
- Known domain paths select their bounded suite.
- Multiple known domains run the union of their checks without duplicates.
- Workflow/runner orchestration files do not force `complete` when they accompany a known bounded-domain change; orchestration-only changes select `smoke`.
- Shared/core surfaces, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` also fails closed to `complete`, because no PR-diff scope is authoritative.

## First-class article gates

Article checks are no longer hidden inside the non-article profile matrix or chained recursively from the article profile gate. The coordinated runner owns them independently:

1. `scientific-article-profile`;
2. `scientific-article-front-block`;
3. `scientific-article-foreign-elements`.

The `article` suite also includes `validator-source`. As Steps 4–7 add article-specific executable checks, each new gate must be added to `article` in the same **material advance**.

## Manual use

GitHub Actions -> `Linux integration` -> `Run workflow` exposes the `scope` choice. The same suites are available locally:

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite objects
python3 tests/run.py --mode pr --suite bibliography
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Current Step 3 failure classification

Linux `34028373060` on synchronized Step 3 head `567a5b2d21a16b653d7704639bdd5012d7c2f99b` ran the former complete 31-check integration path. All checks before `profiles` passed, including the six accepted non-article profile builds. The failure occurred only when the profile matrix recursively entered the article gates: the first foreign-elements scenario inspected warnings after a single LaTeX pass and encountered expected unresolved cross-reference/Biber rerun warnings.

The correction is bounded to evidence orchestration:

- foreign-element fixtures now receive two LaTeX passes before warning inspection, matching the accepted front-block pattern;
- the non-article profile matrix no longer invokes article validation;
- the article profile gate no longer recursively invokes Step 2/3 gates;
- the coordinated runner exposes all three article gates directly.

No article runtime, article authority, rule modality or proof state changes in this correction.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
