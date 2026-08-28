# N15-B2R naming inventory

Updated: 2026-08-28

Current certified base: `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

Active branch: `refactor/n15-b2r-a2-user-layout`.  
Active PR: #147.

This document is the human-readable companion to `release/n15-b2r-a-naming-inventory.json`. `docs/NAMING.md` remains the naming policy. `docs/HANDOFF-V2.2.0.md` is the canonical continuation point.

## Mandatory synchronization rule

B2R cannot close if this file, the machine ledger and the canonical handoff disagree with live Git/PR/CI state.

Final receipt sync follows an anti-loop rule: record the complete implementation-head certification, then certify the receipt-only documentation head using live checks without editing this file again merely to copy those new run numbers. Otherwise every receipt-only edit would create another uncertified SHA.

## B2R-A1 — DONE

Internal module filenames normalized to English:

| Previous | Canonical |
| --- | --- |
| `abntexto-ufc/fontes.def` | `abntexto-ufc/fonts.def` |
| `abntexto-ufc/modulos.def` | `abntexto-ufc/modules.def` |
| `abntexto-ufc/pretextuais.def` | `abntexto-ufc/frontmatter.def` |
| `abntexto-ufc/institucional.def` | `abntexto-ufc/institutional.def` |
| `abntexto-ufc/trabalhos.def` | `abntexto-ufc/academic-works.def` |
| `abntexto-ufc/projetos.def` | `abntexto-ufc/research-projects.def` |
| `abntexto-ufc/objetos.def` | `abntexto-ufc/objects.def` |
| `abntexto-ufc/bibliografia.def` | `abntexto-ufc/bibliography.def` |
| `abntexto-ufc/postextuais.def` | `abntexto-ufc/backmatter.def` |

PR #146 was squash-merged. Resulting `main` `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1` was certified by Source #367, preflight #1030, Gate T #1031 and Distribution #239.

## B2R-A2 — FINAL DOCUMENTATION-SYNC CANDIDATE

A2 normalizes only user-example and distribution-facing repository paths. It does not change public `\ufcsetup` semantics, article runtime or normative predicates/values/locators/authority.

### Canonical moves

| Previous | Canonical |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository, full-template bundle and Overleaf bundle share this canonical content layout; Overleaf keeps `main.tex` at ZIP root. Portuguese academic leaf filenames remain intentionally retained in A2.

### Key synchronized consumers

- Makefile/default entrypoint and `main.tex` references;
- frontmatter/chapter/backmatter/bibliography/image/listing paths;
- reference-image downloader and validation runner;
- reference/corpus/PDF-A/profile checks;
- Overleaf stable/import bundle checks;
- deterministic release builder and release-package contract;
- distribution-source validation;
- CAPES guidance;
- CTAN README/binary policy;
- `.gitignore` generated/reference-image paths;
- secondary `normativa/reference-guide-map.json` source traces;
- active user/naming/normative documentation.

The stale-path gate is boundary-aware and rejects real legacy path tokens without confusing identifiers such as `imprimirlistadefiguras/before` with a `figuras/` directory reference.

### Frozen N12 boundary

`.github/workflows/latex-preflight.yml` remains byte-identical at:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The historical N12 manifest/hashes are unchanged. Only two authorized path strings in `tests/smoke/perfil-base.tex` are reversed before historical hash comparison:

- `frontmatter/resumo` → `1-pre-textuais/resumo`;
- `frontmatter/abstract` → `1-pre-textuais/abstract`.

### Normative trace clarification

`normativa/reference-guide-map.json` is secondary trace documentation. A2 changed only `source_file` implementation paths to `chapters/...`; `normative_contract_changed=false` remains true and no authority/predicate/value/rule ID/locator changed.

## Migration evidence

CI cycles found and resolved only bounded migration issues:

1. stale reference-map and profile-fixture paths;
2. exact human supersession strings in `VIGENCIA-NORMATIVA.md`;
3. container Git `safe.directory`;
4. bounded N12 historical-content rewrite for two fixture paths;
5. CAPES gratitude-path consumer;
6. stale `.gitignore`, compiled-guide, CTAN README and CTAN binary-policy paths;
7. one scanner substring false positive solved by boundary-aware matching rather than exemption.

No fix changed public API, article runtime, normative contract, formatting intent or pagination intent.

## Certified implementation head before final receipt sync

Implementation head:

`6e2528458e4cf92dda970ecad122054fe9d51f78`

Complete receipts:

- Source Contract **#402 — SUCCESS**;
- Reference Preview **#56 — SUCCESS**;
- PR LaTeX preflight **#1066 — SUCCESS**;
- exact Gate T **#1067 — SUCCESS**, including Overleaf stable proxy, Windows literal Times New Roman/Arial build, independent identity/Unicode/embedding/PDF-A certification, 12-profile matrix/PDF-A, structure, reference, objects/bibliography and post-textual regressions;
- Distribution **#240 — SUCCESS**, including Gate T reuse, release preflight, release PDF/A, deterministic bundles, Overleaf import-bundle proxy, artifact upload and aggregate `distribution-preflight`.

`Publish GitHub Release` was correctly skipped because no release tag was involved.

Non-mutating certification refs used:

- `maintenance/v2.2.0-b2r-a2-gate-t` → `6e252845...`;
- `release/v2.2.0-b2r-a2-dist` → `6e252845...`.

## A2 closure requirements

A2 remains ACTIVE until:

- the current receipt-only documentation-sync PR head itself has live Source + Preview + full PR preflight green;
- the same SHA has exact Gate T and Distribution green;
- N12 blob remains unchanged;
- PR is mergeable and `behind_by=0` immediately before merge;
- PR #147 is squash-merged;
- resulting `main` is fully re-certified;
- the merged/re-certified state is written to the handoff/ledger before B2R-B implementation begins.

## Next executable action

Use the current documentation-sync head as the sole merge candidate. Do not edit receipt documents again solely to copy its future run numbers. Run Source Contract, Reference Preview and full preflight on the exact SHA, then Gate T and Distribution through non-mutating certification refs. Recheck N12, mergeability and `behind_by=0`; mark PR ready and squash-merge only when all live gates are green. Re-certify resulting `main` before B2R-B.

## B2R-B — BLOCKED BY A2

After A2 merge + post-merge recertification:

- create a machine-readable public API inventory;
- introduce canonical English project-owned public API surfaces;
- preserve supported Portuguese keys/values/commands/environments as v2.x aliases;
- prove canonical-English/Portuguese semantic/output equivalence;
- prevent new unreviewed engineering identifiers from bypassing naming policy.