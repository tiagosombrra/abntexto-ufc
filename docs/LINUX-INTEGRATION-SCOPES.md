# Linux Integration Scopes

Updated: 2026-09-06  
Status: IMPLEMENTED — RUNNER IMPORT CORRECTION / CI ACCEPTANCE PENDING

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | Pull requests; infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | Shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | validator-source + article profile/front-block/foreign-elements | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference, layout, typography, front/back matter, objects, bibliography | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout, fonts, PDF core/geometry, math, normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry, code typography, IBGE tables, objects, minted, algorithms, documentary sources | No |
| `bibliography` | references/citation evidence | bibliography, reference spacing, normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted non-article profile compatibility | six-profile matrix, build path, multivolume, catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke | No |

## Automatic selection

For pull requests, `auto` evaluates the relevant changed-path window after checkout.

- On `synchronize`, compare the previous PR head (`before`) with the new PR head (`after`).
- On opened/reopened/ready-for-review events, use the full PR diff.
- Documentation-only changes skip heavy Linux integration.
- Known domain paths select their bounded suite.
- Multiple known domains run a deduplicated union.
- Workflow/runner orchestration files do not force `complete` when they accompany a known bounded-domain change; orchestration-only changes select `smoke`.
- Shared/core surfaces, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` fails closed to `complete`.

## First-class article and profile gates

Article checks are not hidden inside the non-article profile matrix or recursively chained from the profile gate. The coordinated runner owns them independently.

The `article` suite contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`.

The `profiles` suite contains only the six accepted non-article profiles and compatibility checks. `profile-matrix.sh` must reject accidental inclusion of `scientific-article` and emit `PROFILE-MATRIX-EVIDENCE`.

As Scientific Article Steps 4–7 add executable gates, each new article gate joins `article` in the same **material advance**.

## Runner importability invariant

The coordinated runner is consumed in two ways:

- direct execution: `python3 tests/run.py ...`;
- dynamic loading by normative traceability/false-coverage checks.

Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts. A direct-execution-only import path is a static-contract defect, not a reason to weaken traceability.

Migration checkpoint `336bc982d8442d572b52c4b9b78028e197c178b3` demonstrated this boundary: scope inference correctly selected `profiles,article`, and seven of eight bounded checks passed, but both Static `34030098936` and Linux `34030098924` failed `validator-source` because dynamically loaded `tests/run.py` could not resolve `integration_suites.py`.

Technical correction `4068414a2c2e1f919246438b516a6092f677925f` makes `tests/run.py` add its own directory to the module search path before importing its sibling suite definition. It also strengthens profile-separation and two-pass foreign-element evidence. No article runtime or normative rule changes.

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

## Current acceptance requirement

The synchronized correction checkpoint must pass:

- Static contract, including dynamic runner loading and `LINUX-SUITE-EVIDENCE`;
- Linux `profiles,article` on the same SHA;
- article profile/front-block/foreign-elements evidence;
- non-article `PROFILE-MATRIX-EVIDENCE` and six-profile compatibility.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
