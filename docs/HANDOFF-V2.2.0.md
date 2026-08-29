# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-B1 public-API baseline/checker is certified on PR #150; documentation-sync head must pass before merge**.

Certified base `main`: `3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

Current B2R-B branch: `refactor/n15-b2r-b-public-api`.

Last technically certified B2R-B1 head before this documentation-sync commit: `1438d85e22a787ce7ab92bcd7abd06e259afa05d`.

Always read the live repository head, PR state and GitHub Actions receipts before mutation or merge. This file is the canonical continuation state; live Git/CI remains the execution authority.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

Update these active state documents whenever scope changes materially, CI exposes or resolves a blocker, a PR is opened/merged, certification changes, or the next executable action changes:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — active B2R human ledger;
3. `release/n15-b2r-b-public-api.json` — active B2R-B machine ledger;
4. `docs/NAMING.md` — naming/compatibility policy and migration state when applicable.

`release/n15-b2r-a-naming-inventory.json` is the historical B2R-A/N12-sensitive ledger. Do not simplify or repurpose it for B2R-B state.

A B2R subphase must not be marked DONE if the active documents disagree with repository/PR/CI state.

## Source-of-truth hierarchy

1. `normativa/*.json` — normative sources, predicates, locators, precedence and proof policy;
2. `tests/` + GitHub Actions — executable evidence;
3. `docs/NORMAS.md` and `docs/VIGENCIA-NORMATIVA.md` — human normative map/currency policy;
4. `docs/NAMING.md` — naming/compatibility policy;
5. `release/*.json` — technical phase ledgers;
6. this handoff — current roadmap and next action;
7. Git/PR/Actions history — detailed historical receipts.

Green CI never creates a normative requirement or silently promotes proof state.

## Guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording/locators;
- recommendations remain recommendations;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- no supported Portuguese public-API removal in v2.x;
- B2R public-API migration is additive;
- no article runtime before B2R closes and the resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- physical branch cleanup remains deferred until final certification/tag;
- documentation synchronization is mandatory before phase closure and project handoff.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness/authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146 |
| N15-B2R-A2 | user-example/distribution-facing layout | DONE — PR #148; resulting `main` re-certified |
| N15-B2R-B1 | public-API inventory + executable baseline checker | CERTIFIED ON PR #150; doc-sync gate pending |
| N15-B2R-B2 | additive canonical-English setup keys/values + Portuguese aliases | BLOCKED by B1 merge/re-certification |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | BLOCKED by B2 |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | BLOCKED by B3 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## Completed checkpoints

### N15-B2A — DONE

PR #145 promoted the scientific-article authority/contract without runtime. Resulting `main` `7699ed205d4554df28fc46908fff3be0b92a38f7` was certified by Source #361, PDF Validator #135, preflight #1022, Gate T #1023 and Distribution #238.

### N15-B2R-A1 — DONE

PR #146 normalized internal module names to English without public-API or runtime behavior change. Resulting `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` was certified by Source #367, preflight #1030, Gate T #1031 and Distribution #239.

### N15-B2R-A2 — DONE

A2 normalized user-example and distribution-facing repository paths only:

| Previous | Canonical |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository template, complete-template bundle and Overleaf bundle use this canonical content layout; Overleaf keeps `main.tex` at archive root. Portuguese academic leaf filenames remain intentionally unchanged by A2.

The final A2 merge candidate `22e9e4e872aca8aca16b143b249d62fe516c3359` passed Source #408, Reference Preview #62, preflight #1073, Gate T #1074 and Distribution #241. PR #148 was squash-merged, producing `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`, which then passed Source #410, preflight #1076, Gate T #1077, Distribution #242 and PDF Validator #136.

The later B2R-A2 documentation-sync closure advanced `main` to the certified base now used by B2R-B: `3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

## N15-B2R-B1 — current closure state

PR #150 (`audit: establish B2R-B public API baseline`) starts B2R-B without changing runtime semantics.

B1 introduced:

- `release/n15-b2r-b-public-api.json` as the active pre-migration public/exported API ledger;
- setup-value identity scoped by `(setup key, value)`, avoiding collisions for repeated values such as `true`, `false`, `sim` and `nao`;
- inventory of 2 class entrypoints, 67 setup keys, 45 scoped setup values, 47 exported commands, 6 UFC environments and 2 explicit extension hooks;
- classification of canonical project API, Portuguese compatibility API, exported helpers and upstream compatibility surfaces;
- reservation of `type=article` / `tipo=artigo` without activating article runtime;
- `tests/checks/public_api_contract.py`, which rejects removals/unreviewed additions and verifies the frozen N12 workflow blob;
- integration of `public-api` as a dependency of the existing `repository` validation check, with no change to `.github/workflows/latex-preflight.yml`.

### CI-discovered blocker and correction

Initial head `d3f55442e22eced43784089c24b5423f092123f2` passed the new public-API checker itself, but preflight #1081 failed only in the older canonical-identity scanner because the new ledger necessarily documents the deprecated `ufctex` wrapper.

The correction at head `1438d85e22a787ce7ab92bcd7abd06e259afa05d` added a narrow classification exception for exactly the ledger lines that identify `ufctex` and `ufctex.cls`. It does not exempt the whole ledger or permit additional unclassified legacy identities.

### Certified technical head receipts

Head `1438d85e22a787ce7ab92bcd7abd06e259afa05d` passed:

- Normative Source Contract #414 — SUCCESS;
- LaTeX preflight #1082 — SUCCESS;
- structure job — SUCCESS, including `public-api`, repository audit, distribution source, layout, fonts, normative complement, pre-textuals, projects, build path, multi-volume and catalog card;
- reference document + PDF/A-2b — SUCCESS;
- 12-profile matrix + profile PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS.

The `public-api` evidence on the prior diagnostic run already reported `keys=67 values=45 commands=47 environments=6 hooks=2`, `value_identity=setup-key/value`, `article_runtime=false` and the frozen N12 blob.

No public API behavior, article runtime, normative contract, formatting intent or pagination intent changed in B1.

## Next executable action

1. Let the final B2R-B1 documentation-sync head pass Source Contract and LaTeX preflight.
2. Confirm PR #150 remains mergeable and `behind_by=0`.
3. Squash-merge PR #150 with the exact expected head SHA.
4. Re-certify the resulting `main` before beginning public aliases.
5. Start N15-B2R-B2 from that re-certified `main`.

B2R-B2 must introduce setup aliases additively. The safest first implementation is for the already-reviewed mappings such as `type`, `cover`, `catalog-card`, `coat-of-arms`, `font`, `strict-font`, `tables`, `code`, `algorithms`, `glossary`, `index`, `author`, `title`, `subtitle`, `approval-date`, `advisor` and `coadvisor`. English aliases should forward to the certified Portuguese behavior wherever possible.

Terms still marked `review_required` — especially print-mode vocabulary, detailed academic metadata, module values, commands and environments — must be resolved semantically before implementation. Do not introduce `article` runtime in B2R-B2.

## Later phases

### N15-B2B

Implement scientific-article runtime on the final naming architecture, preferably via profile capabilities, preserving the reconciled article contract.

### N15-B2C

Close article evidence with positive fixtures, final-PDF measurements, bounded negatives/sensitivity cases and EN/PT compatibility proof.

### N15-B3 → C → D

Resolve remaining pre-release items, promote v2.2.0 metadata, build deterministic candidates and certify the exact release head before tag/release.
