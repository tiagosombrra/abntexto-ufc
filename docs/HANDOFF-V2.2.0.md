# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A2 implementation candidate — PR #147 (`refactor/n15-b2r-a2-user-layout`)**.

Certified stable `main`: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

Always read the live PR head and GitHub Actions receipts before mutation or merge. This file is the canonical continuation state; live Git/CI is the execution authority.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

Update these active state documents whenever scope changes materially, CI exposes or resolves a blocker, a PR is opened/merged, certification changes, or the next executable action changes:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — active B2R human ledger;
3. `release/n15-b2r-a-naming-inventory.json` — active machine ledger;
4. `README.md`, `docs/NORMAS.md`, `docs/VIGENCIA-NORMATIVA.md`, `docs/NAMING.md`, `docs/README-CTAN.md` when the surfaces they describe change.

A phase must not be marked DONE if these documents disagree with the repository/PR/CI state. Before a conversation handoff, this file must state the current phase, stable-main SHA, active branch/PR, known receipts/blockers and the next executable action.

## Source-of-truth hierarchy

1. `normativa/*.json` — normative sources, predicates, locators, precedence and proof policy;
2. `tests/` + GitHub Actions — executable evidence;
3. `docs/NORMAS.md` — current human normative map;
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition/precedence policy;
5. `docs/NAMING.md` — naming/compatibility policy;
6. `release/*.json` — technical phase ledgers;
7. this handoff — current roadmap and next action;
8. Git/PR/Actions history — detailed historical receipts.

Green CI never creates a normative requirement or silently promotes proof state.

## Guardrails

- use current authoritative norms/UFC requirements under the recorded precedence model;
- do not invent inaccessible ABNT wording or exact locators;
- recommendation language remains recommendation language;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- no claim of official UFC/SiBi approval unless that status actually exists;
- no removal of supported Portuguese public API in v2.x; canonical English API is additive compatibility work;
- no article runtime before B2R closes and resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles under the established policy;
- bulk branch cleanup remains deferred until final certification/tag;
- documentation synchronization is mandatory before phase closure and project handoff.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness/authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146; resulting `main` re-certified |
| N15-B2R-A2 | user-example/distribution-facing layout | ACTIVE — PR #147 draft; exact-head CI repair/certification |
| N15-B2R-B | canonical English public API + Portuguese aliases | BLOCKED by A2 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## Frozen N0–N14 baseline

Historical pre-article baseline:

- full atomic rules: 181;
- normative rules: 170;
- locator coverage: 170/170;
- explicit gaps: 46/46 classified;
- proof state: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`;
- N11: five bounded `project.*` predicates;
- N12 frozen workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- N13: seven negative mechanisms, five rendered negative cases;
- N14: Web/Lite and CLI/Deep semantic closure certified.

B2A later added the article contract without rewriting this historical baseline.

## Completed N15 checkpoints

### N15-B1 — DONE

PR #144. Certified resulting main `bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e`:

- Source Contract #345 — SUCCESS;
- PDF Validator #134 — SUCCESS;
- LaTeX preflight #1005 — SUCCESS;
- Gate T #1006 — SUCCESS;
- Distribution #237 — SUCCESS.

### N15-B2A — DONE

PR #145. Article authority/contract was promoted while runtime remained absent.

Current article authority:

- `ufc-guia-artigos-2022`, bibliographic edition 2022, corrected file date 2023-04-27;
- `ufc-guia-artigos-2021` retained only as superseded history;
- `abnt-nbr-6022-2018` as technical source under the conservative evidence model;
- 13 `article.*` predicates with dedicated locators/phase metadata;
- 150–250 abstract words, minimum three keywords and Arial/Times wording remain recommendations when the source says `convém`/`recomenda-se`.

Certified resulting main `7699ed205d4554df28fc46908fff3be0b92a38f7`:

- Source Contract #361 — SUCCESS;
- PDF Validator #135 — SUCCESS;
- LaTeX preflight #1022 — SUCCESS;
- Gate T #1023 — SUCCESS;
- Distribution #238 — SUCCESS.

### N15-B2R-A1 — DONE

PR #146 normalized internal module filenames only:

- `fontes.def` → `fonts.def`;
- `modulos.def` → `modules.def`;
- `pretextuais.def` → `frontmatter.def`;
- `institucional.def` → `institutional.def`;
- `trabalhos.def` → `academic-works.def`;
- `projetos.def` → `research-projects.def`;
- `objetos.def` → `objects.def`;
- `bibliografia.def` → `bibliography.def`;
- `postextuais.def` → `backmatter.def`.

Public API, normative predicates and article runtime were unchanged. The N12 checker reconstructs historical `\ProvidesFile` identities only for certified renamed modules.

Certified resulting main `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`:

- Source Contract #367 — SUCCESS;
- LaTeX preflight push #1030 — SUCCESS;
- exact Gate T #1031 — SUCCESS;
- Distribution #239 — SUCCESS.

This SHA is the certified base of A2.

## N15-B2R-A2 — ACTIVE

Branch: `refactor/n15-b2r-a2-user-layout`  
PR: #147 (draft)  
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

Repository template and generated complete template/Overleaf bundles intentionally use the same content layout; Overleaf keeps `main.tex` at archive root. Portuguese academic leaf filenames remain intentionally unchanged in A2 (`frontmatter/resumo.tex`, `backmatter/apendices/`, `backmatter/anexos/`, etc.).

### Synchronized A2 consumers

A2 currently synchronizes:

- Makefile and `main.tex` references;
- frontmatter/chapter/backmatter content paths;
- bibliography, figures/listings and license paths;
- source-only institutional asset path;
- reference-image downloader;
- reference/corpus/PDF-validator/PDF-A checks;
- profile fixture and matrix consumers;
- Overleaf stable/import checks;
- deterministic bundle builder/release-package checks;
- reference/distribution workflows other than the frozen N12 workflow;
- CAPES guidance path;
- CTAN README and binary-policy paths;
- `.gitignore` generated/reference-image paths;
- secondary `normativa/reference-guide-map.json` `source_file` traces;
- active human documentation.

`tests/v2-distribution-check.sh` now uses container-safe Git access and a boundary-aware active-path scanner. It rejects genuine legacy A2 paths while not confusing identifiers such as `imprimirlistadefiguras/before` with the directory token `figuras/`.

### Normative/N12 boundaries

`normativa/reference-guide-map.json` changed only secondary `source_file` implementation paths; its policy remains `normative_contract_changed=false`. No predicate, value, source authority, rule ID or normative locator changed.

`.github/workflows/latex-preflight.yml` remains byte-identical at:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

The N12 matrix manifest/certified hashes also remain unchanged. A2 reconstructs only these two historical strings inside `tests/smoke/perfil-base.tex` before validating the frozen historical blob:

- `frontmatter/resumo` → `1-pre-textuais/resumo`;
- `frontmatter/abstract` → `1-pre-textuais/abstract`.

Any unrelated fixture drift still fails.

## A2 exact-head CI history

### Cycle 1 — `1f80043139ae9fabe68c554c264ef7d8c5087cd8`

- Source Contract #368 — SUCCESS;
- Reference Preview #22 — reference build SUCCESS before later steps;
- LaTeX preflight #1032 — path-only failures.

Fixed: `reference-guide-map.json` chapter paths and `perfil-base.tex` frontmatter paths.

### Cycle 2 — `8b1a0a8013c10cc73ad43115b25d0beca567e529`

- Source Contract #376 — failed only the human `normative_currency.py` mapping assertion;
- catalog, precedence, source audit, source references and locator audit had passed.

Fixed: `docs/VIGENCIA-NORMATIVA.md` now preserves exact full ABNT supersession strings/CEPE markers while keeping the corrected current B2A article state.

### Cycle 3 — `a0bf9d060a188aa963d7e7f7002a538ef3dee2e0`

- Source Contract #380 — SUCCESS;
- Reference Preview #34 — SUCCESS including PDF/A + TeX Live 2025 proxy;
- LaTeX preflight #1044 — reference/PDF-A, 12-profile build/PDF-A and post-textual success; structure found three migration consumers.

Fixed:

1. `git ls-files` runs with explicit `safe.directory` inside the TeX Live container;
2. bounded machine-ledger-controlled N12 reverse-content bridge for the two profile-fixture paths;
3. CAPES guidance reads `frontmatter/agradecimentos.tex`.

### Cycle 4 — `3fcd7a6d8cf09567c9e6c79448b8a3f0dbf3899c`

- Source Contract #387 — SUCCESS;
- Reference Preview #41 — SUCCESS including PDF/A + TeX Live 2025 proxy;
- LaTeX preflight #1051:
  - profile matrix 12/12 + 12 PDF/A — SUCCESS;
  - reference document + PDF/A — SUCCESS;
  - post-textual — SUCCESS;
  - objects/bibliography — SUCCESS;
  - `normative-complement` — PASS, confirming N12 path/content bridge;
  - pretextual — PASS, confirming CAPES-path repair;
  - layout/font-config/pdf-geometry/math/project/build-path/multivolume/catalog-card — PASS;
  - structure summary `PASS=13 FAIL=1`, with only `distribution-source` failing.

The stale-path scanner reported nine files. Eight were real stale references and one was a false positive:

- real: `.gitignore`, five compiled-guide chapter references, `docs/README-CTAN.md`, `tests/v2-ctan-policy-check.py`;
- false positive: `abntexto-ufc/layout.def`, where raw `figuras/` occurred only inside `imprimirlistadefiguras/before`.

Repairs after #1051:

- `.gitignore` now uses `main.pdf` and `figures/...`;
- compiled guide references use `main.tex`, `frontmatter/...`, `backmatter/referencias.bib`;
- CTAN README uses `assets/institutional/ufc-coat-of-arms.png`;
- CTAN binary policy uses canonical A2 paths with binary hashes unchanged;
- stale-path scanner is boundary-aware; no broad `layout.def` exemption was added.

These CI findings are migration evidence. None changed public API, article runtime, normative predicates/values/locators/authority, formatting intent or N12 frozen artifacts.

## A2 closure criteria

A2 can be marked DONE only when one exact candidate satisfies all of the following:

1. Source Contract green;
2. Reference Preview/reference corpus/PDF-A green;
3. LaTeX preflight fully green, including 12-profile matrix and PDF/A;
4. Overleaf compatibility/import checks green;
5. required Windows literal-font certification green under Gate T;
6. deterministic Distribution preflight green;
7. N12 workflow blob unchanged;
8. no active stale A2 paths;
9. UFC institutional mark remains excluded from public bundles;
10. reference-image hashes/licensing unchanged;
11. PR `behind_by=0` immediately before merge;
12. active handoff/inventory/ledger/user-policy docs synchronized with the exact candidate;
13. squash merge completed;
14. resulting `main` re-certified before B2R-B starts.

## Next executable action

Use the live PR head produced after the #1051 scanner reconciliation and mandatory documentation sync as the sole certification candidate. Require Source Contract, Reference Preview and full LaTeX preflight green on that exact SHA. Only then run exact-head Gate T and deterministic Distribution, verify `behind_by=0`, perform final receipt-only documentation sync, squash-merge PR #147 and re-certify resulting `main` before B2R-B.

If the current GitHub tool surface cannot dispatch Gate T or Distribution, keep A2 open and record that operational blocker; do not replace either required gate with a weaker check.

## Later phases

### N15-B2R-B

Create a machine-readable public API inventory; introduce canonical English project-owned keys/values/commands where justified; preserve supported Portuguese API as v2.x compatibility aliases; prove semantic/output equivalence.

### N15-B2B

Implement scientific-article runtime directly on the final naming architecture, preferably through profile capabilities. Preserve the reconciled article contract, including single-spacing baseline, continuous primary-section flow and first-page-visible pagination where required.

### N15-B2C

Close article evidence with positive fixtures, final-PDF measurements, bounded negatives/sensitivity cases, canonical-English/Portuguese equivalence proof and complete documentation.

### N15-B3

Resolve remaining pre-release items, including deterministic production-reference experiment/issue #18 and blockers exposed by B2R/B2B/B2C.

### N15-C / N15-D

Promote version metadata only after prior phases close; build deterministic class/template/Overleaf/CTAN candidates; certify exact final head; then decide tag/release. Historical rehearsal branches/PRs remain evidence only.
