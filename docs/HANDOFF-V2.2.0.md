# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A2 final documentation-sync candidate — PR #147 (`refactor/n15-b2r-a2-user-layout`)**.

Certified stable `main`: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

Always read the live PR head and GitHub Actions receipts before mutation or merge. This file is the canonical continuation state; live Git/CI is the execution authority.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

Update these active state documents whenever scope changes materially, CI exposes or resolves a blocker, a PR is opened/merged, certification changes, or the next executable action changes:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — active B2R human ledger;
3. `release/n15-b2r-a-naming-inventory.json` — active machine ledger;
4. user/policy documents when the surfaces they describe change.

A phase must not be marked DONE if these documents disagree with repository/PR/CI state.

### Final-receipt anti-loop rule

The final A2 documentation sync records the complete certification set of the immediately preceding implementation head. Because committing those receipts necessarily creates a new SHA, the documentation-sync head itself must be re-certified using live checks, but the receipt documents are not edited again merely to copy those new run numbers. Otherwise every receipt-only edit would invalidate the SHA it documents. The live checks/statuses attached to the final documentation-sync SHA are the merge authority.

After merge, the resulting `main` certification and the transition to B2R-B must be recorded before new implementation work begins.

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
- no article runtime before B2R closes and resulting `main` is re-certified;
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
| N15-B2R-A1 | internal module English naming | DONE — PR #146; resulting `main` re-certified |
| N15-B2R-A2 | user-example/distribution-facing layout | ACTIVE — PR #147; final docs-sync head awaiting exact-head recertification/merge |
| N15-B2R-B | canonical English public API + Portuguese aliases | BLOCKED by A2 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## Completed checkpoints

### N15-B2A — DONE

PR #145. Article authority/contract promoted without runtime. Current article authority:

- `ufc-guia-artigos-2022`, bibliographic edition 2022, corrected file date 2023-04-27;
- historical `ufc-guia-artigos-2021` retained only as superseded history;
- `abnt-nbr-6022-2018` technical source;
- 13 `article.*` predicates;
- abstract-length/minimum-keyword/font-family wording remains recommendation where the source uses `convém`/`recomenda-se`.

Certified resulting main `7699ed205d4554df28fc46908fff3be0b92a38f7`: Source #361, PDF Validator #135, preflight #1022, Gate T #1023 and Distribution #238 — SUCCESS.

### N15-B2R-A1 — DONE

PR #146 normalized internal module names to English without public-API or runtime behavior change. Certified resulting main `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`: Source #367, preflight #1030, Gate T #1031 and Distribution #239 — SUCCESS.

## N15-B2R-A2 — ACTIVE

Branch: `refactor/n15-b2r-a2-user-layout`  
PR: #147  
Base: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

### Canonical layout

| Previous | Canonical |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository template, complete-template bundle and Overleaf bundle intentionally use the same layout; Overleaf keeps `main.tex` at archive root. Portuguese academic leaf filenames remain intentionally unchanged in A2.

### Behavioral/normative boundaries

A2 changes paths only. It does not change public `\ufcsetup` semantics, article runtime, normative predicates/values/locators/authority, formatting intent or pagination intent.

`normativa/reference-guide-map.json` changed only secondary `source_file` implementation traces and remains `normative_contract_changed=false`.

N12 frozen workflow blob remains:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The N12 historical fixture checker reverses only the two authorized `perfil-base.tex` path strings before historical hash comparison. Manifest and certified hashes remain unchanged.

### Migration blockers resolved

Across PR CI cycles A2 found and fixed only bounded migration consumers:

- secondary guide-trace paths;
- profile fixture frontmatter paths;
- exact human currency markers in `VIGENCIA-NORMATIVA.md`;
- container Git `safe.directory`;
- bounded N12 historical-content path bridge;
- CAPES-guidance path;
- stale generated/reference-image paths, compiled-guide example paths and CTAN asset/binary-policy paths;
- stale-path scanner false positive where `figuras/` occurred inside `imprimirlistadefiguras/before` — solved by boundary-aware matching, not a broad exemption.

No finding required a public-API, article-runtime or normative-contract change.

## Complete implementation-head certification

Implementation head certified before this receipt-only documentation sync:

`6e2528458e4cf92dda970ecad122054fe9d51f78`

Receipts:

- Normative Source Contract **#402 — SUCCESS**;
- Reference PDF Preview **#56 — SUCCESS**;
- PR LaTeX preflight **#1066 — SUCCESS**;
- exact Gate T **#1067 — SUCCESS**, including:
  - Overleaf stable proxy;
  - Windows literal Times New Roman/Arial build;
  - independent literal-font identity/Unicode/embedding/PDF-A certification;
  - reference + PDF/A;
  - 12-profile matrix + 12 PDF/A;
  - structure;
  - objects/bibliography;
  - post-textual;
  - aggregate `latex-preflight` status;
- Distribution preflight **#240 — SUCCESS**, including:
  - Gate T prerequisite reuse;
  - release preflight;
  - release PDF/A-2b;
  - deterministic release bundles;
  - Overleaf import-bundle proxy;
  - release-candidate artifact upload;
  - aggregate `distribution-preflight` status.

`Publish GitHub Release` was correctly skipped because this was a certification branch push, not a release tag.

Gate T was triggered without changing the candidate commit through `maintenance/v2.2.0-b2r-a2-gate-t`; Distribution through `release/v2.2.0-b2r-a2-dist`, both pointing exactly to `6e252845...`.

## A2 closure criteria

A2 is DONE only after all of these are true:

1. current final documentation-sync PR head has live Source Contract, Reference Preview and full PR preflight green;
2. the same final documentation-sync SHA has Gate T green, including Windows literal fonts and Overleaf;
3. the same SHA has Distribution green;
4. N12 workflow blob remains unchanged;
5. no active stale A2 paths;
6. institutional mark remains excluded from public bundles and reference-image hashes/licensing remain unchanged;
7. PR is mergeable and `behind_by=0` immediately before merge;
8. PR #147 is squash-merged;
9. resulting `main` is fully re-certified;
10. handoff/ledger are updated for the merged/re-certified state before B2R-B implementation begins.

## Next executable action

Treat the head created by this final receipt/documentation synchronization as the **sole merge candidate**. Do not edit receipt documents again merely to copy its run numbers. Require live Source Contract + Reference Preview + full PR preflight on that SHA, then exact-head Gate T + Distribution using non-mutating certification refs. Recheck N12 blob, mergeability and `behind_by=0`; mark PR ready and squash-merge only if all are green. Re-certify resulting `main` before opening B2R-B implementation.

## Later phases

### N15-B2R-B

Create a machine-readable public API inventory; introduce canonical English project-owned keys/values/commands/environments; preserve supported Portuguese API as v2.x aliases; prove semantic/output equivalence.

### N15-B2B

Implement scientific-article runtime on the final naming architecture, preferably via profile capabilities, preserving the reconciled article contract.

### N15-B2C

Close article evidence with positive fixtures, final-PDF measurements, bounded negatives/sensitivity cases and EN/PT compatibility proof.

### N15-B3 → C → D

Resolve remaining pre-release items, promote v2.2.0 metadata, build deterministic candidates and certify the exact release head before tag/release.