# Linux Integration Scopes

Updated: 2026-09-06  
Status: IMPLEMENTED — MISSING-BEFORE FALLBACK / CI ACCEPTANCE PENDING

## Purpose

The permanent `Linux integration` workflow supports bounded suites for intermediate work so a small change does not wait for the complete repository regression. Scoped suites optimize feedback time; they do not weaken phase acceptance.

## Available scopes

| Scope | Intended use | Main checks | Can close a phase? |
|---|---|---|---|
| `auto` | infer the narrowest safe suite from changed paths | one or more inferred suites | No |
| `complete` | shared/core changes, unknown technical paths and phase-end regression | all PR integration checks + normative contribution | **Yes, with all other phase-end gates** |
| `article` | Scientific Article implementation/evidence | validator-source + article profile/front-block/foreign-elements | No |
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
- If either synchronize endpoint is unavailable, the workflow keeps the full PR `base -> head` range and records `missing-before-full-pr`. It must not terminate with a Git object error.
- On opened/reopened/ready-for-review events, it uses the full PR diff.
- Documentation-only changes skip heavy Linux integration.
- Known domain paths select their bounded suite.
- Multiple known domains run a deduplicated union.
- Workflow/runner orchestration files do not force `complete` when they accompany a known bounded-domain change; orchestration-only changes select `smoke`.
- Shared/core surfaces, standards/integration infrastructure and unknown technical paths fail closed to `complete`.
- Manual `workflow_dispatch` with `auto` fails closed to `complete`.

The fallback is intentionally conservative. A full PR diff may select `complete`; correctness and provenance take precedence over scoped-runtime savings.

## First-class article and profile gates

Article checks are not hidden inside the non-article profile matrix or recursively chained from the profile gate. The coordinated runner owns them independently.

The `article` suite contains:

1. `validator-source`;
2. `scientific-article-profile`;
3. `scientific-article-front-block`;
4. `scientific-article-foreign-elements`.

The `profiles` suite contains exactly six accepted non-article profiles and compatibility checks. `profile-matrix.sh` rejects accidental inclusion of `scientific-article` and emits `PROFILE-MATRIX-EVIDENCE` with the measured profile count.

As Scientific Article Steps 4–7 add executable gates, each new article gate joins `article` in the same **material advance**.

## Runner importability invariant

The coordinated runner is consumed through direct execution and dynamic loading by normative traceability/false-coverage checks. Runner-owned sibling modules such as `tests/integration_suites.py` must resolve in both contexts.

Checkpoint `336bc982...` exposed the dynamic-import gap. Technical fix `4068414...` repaired it, and Static `34030827665` on synchronized checkpoint `4f1c9a1...` confirmed the import path is now green.

Linux `34030827664` on that same checkpoint exposed a second orchestration boundary before any integration check ran: the synchronize `before` SHA was unavailable, and scope calculation terminated with `fatal: bad object`. Technical correction `0a48d72...` adds the endpoint-existence check and full-PR fallback. This fallback is now part of the static suite contract.

## Step 3 evidence contract

Foreign-element scenarios use two LaTeX passes before warning inspection. Evidence records both `convergence_passes=2` and `warnings_checked_after_final_pass=true` so the convergence fix remains visible and testable.

## Manual use

```sh
python3 tests/run.py --mode pr --suite article
python3 tests/run.py --mode pr --suite profiles,article
python3 tests/run.py --mode pr --suite complete
```

Use `python3 tests/run.py --list-suites` to inspect the current mapping.

## Current acceptance requirement

The synchronized correction checkpoint must pass:

- Static contract, including dynamic runner loading, `LINUX-SUITE-EVIDENCE`, and missing-before fallback tokens;
- Linux `profiles,article` on the same SHA under a normal reachable incremental range;
- article profile/front-block/foreign-elements evidence;
- `PROFILE-MATRIX-EVIDENCE`, exactly six non-article profiles, and six-profile compatibility.

## Phase-end rule

A scoped green run never closes a phase. Every phase transition still requires `complete` Linux integration on the same immutable phase-end candidate SHA together with Static and phase-specific acceptance evidence.

Final Certification may additionally require the heavier literal-font/PDF-A/distribution matrix; scoped PR suites do not replace that certification.
