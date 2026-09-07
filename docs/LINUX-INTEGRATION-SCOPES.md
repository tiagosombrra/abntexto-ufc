# Linux Integration Scopes

Updated: 2026-09-07  
Status: ACTIVE — STEP 5 ARTICLE GATE REGISTERED / ACCEPTANCE CI PENDING

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | validator-source + article profile/front-block/foreign-elements/body/**recommendations** | No |
| `reference-document` | canonical reference source/corpus changes | reference build, corpus and PDF validator | No |
| `reference-pdf` | presentation-sensitive reference-PDF work | reference, layout, typography, front/back matter, objects, bibliography | No |
| `frontmatter` | cover/title/approval/pre-textual changes | front matter + duplex front matter | No |
| `layout` | page/body/geometry/math/quotation changes | layout, fonts, PDF core/geometry, math, normative complement | No |
| `objects` | figures/tables/code/algorithms/documentary sources | object geometry, code typography, IBGE tables, objects, minted, algorithms, documentary sources | No |
| `bibliography` | references/citation evidence | bibliography, reference spacing, normative complement | No |
| `backmatter` | appendices/annexes/index/glossary | back matter + duplex back matter | No |
| `research-project` | research-project profile changes | research-project integration | No |
| `profiles` | accepted non-article profile compatibility | exactly six profiles, build path, multivolume, catalog card | No |
| `smoke` | orchestration-only changes | repository/source/reference/PDF-validator smoke | No |

## Automatic selection and provenance fallback

For pull requests, `auto` evaluates the relevant changed-path window after checkout.

- On `synchronize`, it prefers the previous PR head (`before`) -> new PR head (`after`) incremental range.
- Before using that range, both endpoint commits must be present in the checkout (`git cat-file -e ...^{commit}`).
- If either synchronize endpoint is unavailable, the workflow keeps the full PR `base -> head` range and records `missing-before-full-pr`; it must not terminate with a Git object error.
- On opened/reopened/ready-for-review events, it uses the full PR diff.
- Documentation-only changes skip heavy Linux integration.
- Known domain paths select their bounded suite.
- Multiple known domains run a deduplicated union.
- Workflow/runner orchestration files do not force `complete` when they accompany a known bounded-domain change; orchestration-only changes select `smoke`.
- Shared/core surfaces, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` fails closed to `complete`.

Correctness and provenance take precedence over scoped-runtime savings.

## First-class article gates

Article checks are independently owned by the coordinated runner. They are not hidden inside the six-profile non-article matrix and are not recursively chained from the article profile gate.

The `article` suite now contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`;
5. `scientific-article-body`;
6. `scientific-article-recommendations`.

`tests/checks/linux_integration_suites.py` requires all six checks whenever the phase is Scientific Article or later, verifies Step 5 paths infer `article`, and prevents the article profile gate from hiding later Step gates.

The `profiles` suite remains exactly the six accepted non-article profiles plus compatibility checks. `profile-matrix.sh` rejects accidental inclusion of `scientific-article`.

As later Scientific Article Steps add executable gates, each new gate joins `article` in the same **material advance**.

## Step 5 evidence contract

`scientific-article-recommendations` has two controlled article scenarios and compiles both under pdfLaTeX and LuaLaTeX:

- a recommendation-following scenario inside the 150–250-word guidance, one paragraph and at least three keywords;
- an outside-recommendation scenario with a short summary, two paragraphs and fewer than three keywords.

Successful compilation of the second scenario proves those recommendations are not hard class/validator rejection boundaries. A companion static checker preserves the four recommendation rules as `recommended` + `manual`, preserves the generic right-aligned author default, and preserves `article.journal-guidelines.precedence` as `required-when-applicable`, `conditional-manual`, applicability context `target-journal-submission`.

Step 5 does not promote proof state and does not change runtime normative semantics.

The earlier fixture-only checkpoint `f445333...` passed Static and Linux, but its `article` run still contained only five checks; therefore it cannot accept Step 5.

## Runner importability invariant

The coordinated runner is consumed through direct execution and dynamic loading by normative traceability/false-coverage checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Current acceptance requirement

The synchronized Step 5 implementation candidate must pass:

- Static contract, including recommendation modality checker and six-check suite registration;
- bounded Linux `article` on the same SHA;
- all accepted Step 1–4 gates;
- both two-engine Step 5 scenarios;
- no recommendation hard rejection;
- unchanged journal conditional applicability and proof-state semantics.

A scoped green run accepts only Step 5 after its result is documented. It never closes the Scientific Article phase.

## Phase-end rule

Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
