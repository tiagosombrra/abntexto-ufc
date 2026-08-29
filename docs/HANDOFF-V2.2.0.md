# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A2 merged and post-merge re-certified; B2R-B is the next executable phase**.

Certified `main`: `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`.

Always read the live repository head and GitHub Actions receipts before mutation or merge. This file is the canonical continuation state; live Git/CI remains the execution authority.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

Update these active state documents whenever scope changes materially, CI exposes or resolves a blocker, a PR is opened/merged, certification changes, or the next executable action changes:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — active B2R human ledger;
3. `release/n15-b2r-a-naming-inventory.json` — active machine ledger;
4. user/policy documents when the surfaces they describe change.

A phase must not be marked DONE if these documents disagree with repository/PR/CI state.

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
- no supported Portuguese public-API removal in v2.x;
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
| N15-B2R-B | canonical English public API + Portuguese aliases | READY — next executable phase |
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

A2 did not change public `\ufcsetup` semantics, article runtime, normative predicates/values/locators/authority, formatting intent or pagination intent.

The frozen N12 workflow blob remains:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

#### Final pre-merge certification

The replacement PR #148 pointed to the same certified content SHA as draft PR #147, because #147 could not be transitioned from draft through the automation connector. The final merge candidate was `22e9e4e872aca8aca16b143b249d62fe516c3359`.

Exact-head receipts before merge:

- Source Contract #408 — SUCCESS;
- Reference Preview #62 — SUCCESS;
- PR LaTeX preflight #1073 — SUCCESS;
- Gate T #1074 — SUCCESS, including Windows literal Times New Roman/Arial certification and Overleaf proxy;
- Distribution #241 — SUCCESS;
- `behind_by=0` before merge;
- frozen N12 workflow blob preserved.

PR #148 was squash-merged, producing `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`. PR #147 was closed without merge and is retained only as historical draft context.

#### Post-merge certification

The resulting `main` was re-certified successfully:

- Normative Source Contract #410 — SUCCESS;
- LaTeX preflight push #1076 — SUCCESS;
- exact Gate T #1077 — SUCCESS;
- Distribution preflight #242 — SUCCESS;
- PDF Validator #136 — SUCCESS.

Therefore all A2 closure requirements are satisfied. No B2R-A2 implementation work remains.

## Next executable action — N15-B2R-B

Begin B2R-B on a fresh branch from certified `main` `c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e`.

B2R-B must proceed additively and in this order:

1. create a machine-readable inventory of the current public API before changing it;
2. classify setup keys, values, commands, environments, class entrypoints and upstream-owned surfaces;
3. define canonical English names for project-owned public surfaces;
4. preserve every supported Portuguese v2.x surface as a compatibility alias/wrapper;
5. add an executable checker that prevents accidental removal of compatibility aliases or introduction of unreviewed public identifiers;
6. add semantic/output equivalence fixtures for canonical-English versus Portuguese configuration;
7. re-certify exact-head Source Contract, Reference Preview, full preflight, Gate T and Distribution before closing B2R-B.

Initial implementation target is `abntexto-ufc/core.def`, where `\ufcsetup` is currently Portuguese-centric. Inventory/checker creation must precede or accompany any alias implementation; do not begin scientific-article runtime in this phase.

## Later phases

### N15-B2B

Implement scientific-article runtime on the final naming architecture, preferably via profile capabilities, preserving the reconciled article contract.

### N15-B2C

Close article evidence with positive fixtures, final-PDF measurements, bounded negatives/sensitivity cases and EN/PT compatibility proof.

### N15-B3 → C → D

Resolve remaining pre-release items, promote v2.2.0 metadata, build deterministic candidates and certify the exact release head before tag/release.
