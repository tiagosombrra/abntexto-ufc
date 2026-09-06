# Linux Integration Scopes

Updated: 2026-09-06  
Status: ACTIVE — STEP 4 ARTICLE GATE REGISTERED / ACCEPTANCE PENDING

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | validator-source + article profile/front-block/foreign-elements/**body** | No |
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

The fallback is intentionally conservative. Correctness and provenance take precedence over scoped-runtime savings.

## First-class article and profile gates

Article checks are not hidden inside the non-article profile matrix or recursively chained from the profile gate. The coordinated runner owns them independently.

The `article` suite now contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`;
5. `scientific-article-body`.

The Step 4 body gate was added in the same implementation advance that created it. `tests/checks/linux_integration_suites.py` requires this check whenever the active phase is Scientific Article, Final Certification or Release. It also verifies that orchestration plus Step 4 paths infer `article`, not `complete`.

The `profiles` suite contains exactly six accepted non-article profiles and compatibility checks. `profile-matrix.sh` rejects accidental inclusion of `scientific-article`.

As later Scientific Article Steps add executable gates, each new gate joins `article` in the same **material advance**.

## Step 4 evidence contract

`scientific-article-body` compiles the positive article fixture with pdfLaTeX and LuaLaTeX and measures physical final-PDF evidence for:

- required Introduction, Development, Final Considerations and References;
- 12 pt body typography;
- 2 cm first-line indentation against a same-page margin control;
- justified natural paragraph lines;
- single spacing against a same-document explicit `\singlesp` calibration.

A separate negative fixture intentionally omits Development. The checker must reject it specifically for that missing required structure. Step 4 does not promote the retained source contract proof state; that remains owned by later evidence hardening.

The Step 2/3 gates now assert the accepted profile-scoped Step 4 begin-document route instead of forbidding any article begin-document hook. This preserves isolation coverage after the semantic transition.

## Runner importability invariant

The coordinated runner is consumed through direct execution and dynamic loading by normative traceability/false-coverage checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

Earlier Step 3 defects exposed dynamic-import and unavailable-`before` boundaries; both remain regression-protected by the static suite contract and fail-closed full-PR fallback.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Current acceptance requirement

The synchronized Step 4 checkpoint must pass:

- Static contract, including dynamic runner loading and Step 4 suite registration;
- bounded Linux `article` on the same SHA;
- article profile/front-block/foreign/body evidence;
- positive two-engine physical body measurements;
- deterministic negative structure rejection.

A Step 4 scoped green run accepts only Step 4 after its result is documented. It never closes the Scientific Article phase.

## Phase-end rule

Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
