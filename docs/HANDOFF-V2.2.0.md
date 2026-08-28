# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-A2 implementation candidate — PR #147 (`refactor/n15-b2r-a2-user-layout`)**.

Certified stable `main`: `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

Always read the live PR head and GitHub Actions receipts before mutation or merge. This handoff records the continuation state, but live Git/CI remains the execution authority.

This is the canonical continuation document for v2.2.0. Detailed historical evidence remains in `normativa/`, `release/`, `tests/`, pull requests, GitHub Actions and `docs/history/`.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

The following active state documents must be updated whenever a phase changes materially, CI exposes a new blocker, a blocker is resolved, a PR is opened/merged, or the next continuation action changes:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. the active phase-specific human ledger, currently `docs/B2R-NAMING-INVENTORY.md`;
3. the corresponding machine-readable ledger under `release/`, currently `release/n15-b2r-a-naming-inventory.json`;
4. user-facing or policy documentation such as `README.md`, `docs/NORMAS.md`, `docs/VIGENCIA-NORMATIVA.md` and `docs/NAMING.md` whenever the surfaces they describe change.

A phase must not be marked DONE if these documents disagree with the live repository/PR/CI state. Before ending a work session or handing the project to a new conversation, the handoff must contain the current phase, stable-main SHA, active branch/PR, known CI receipts/blockers and the next executable action.

## Source-of-truth hierarchy

1. `normativa/*.json` — normative sources, predicates, locators, precedence and proof policy;
2. `tests/` + GitHub Actions — executable evidence and regression results;
3. `docs/NORMAS.md` — current human-readable normative map;
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy;
5. `docs/NAMING.md` — engineering naming/compatibility policy;
6. `release/*.json` — technical phase/release ledgers;
7. this handoff — current roadmap state and next action;
8. Git/PR/Actions history — detailed historical receipts.

Green CI alone never creates a normative requirement or promotes a rule to `PROVEN`.

## Guardrails

- use current authoritative norms and UFC requirements according to the recorded precedence model;
- do not invent inaccessible ABNT wording or exact locators;
- recommendation language remains recommendation language;
- N12 `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- no claim of official UFC/SiBi approval unless such status actually exists;
- no public Portuguese API removal in v2.x; canonical English public surfaces are additive compatibility work;
- no article runtime work before B2R is closed and re-certified;
- UFC institutional mark and proprietary Microsoft font files remain excluded from public bundles according to the established distribution policy;
- bulk branch cleanup remains deferred until final certification/tag;
- documentation synchronization is mandatory before phase closure and before project handoff.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness and authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146; resulting main re-certified |
| N15-B2R-A2 | user-example/distribution-facing layout | ACTIVE — PR #147 draft; exact-head CI repair/certification |
| N15-B2R-B | canonical English public API + Portuguese compatibility aliases | BLOCKED by A2 |
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

B2A later added the article contract without rewriting that historical baseline.

## N15-B1 — DONE

PR #144 closed source-authority reconciliation.

Certified resulting main `bc7b3bbe0e7ac21aa16efb1f0bab9a4dfb8e912e`:

- Source Contract #345 — SUCCESS;
- PDF Validator #134 — SUCCESS;
- LaTeX preflight #1005 — SUCCESS;
- Gate T #1006 — SUCCESS;
- Distribution #237 — SUCCESS.

## N15-B2A — DONE

PR #145 promoted the scientific-article source/contract while leaving article runtime absent.

Current article authority model:

- UFC guide: `ufc-guia-artigos-2022`, bibliographic edition 2022, corrected file date 2023-04-27;
- previous `ufc-guia-artigos-2021` retained only as superseded history;
- technical source: `abnt-nbr-6022-2018` under the conservative evidence model;
- 13 `article.*` predicates were added with dedicated locators/phase metadata;
- 150–250 abstract words, minimum three keywords and Arial/Times wording remain recommendations where the source says `convém`/`recomenda-se`.

Certified resulting main `7699ed205d4554df28fc46908fff3be0b92a38f7`:

- Source Contract #361 — SUCCESS;
- PDF Validator #135 — SUCCESS;
- LaTeX preflight #1022 — SUCCESS;
- Gate T #1023 — SUCCESS;
- Distribution #238 — SUCCESS.

## N15-B2R-A1 — DONE

PR #146 normalized internal package-module filenames only:

- `fontes.def` → `fonts.def`;
- `modulos.def` → `modules.def`;
- `pretextuais.def` → `frontmatter.def`;
- `institucional.def` → `institutional.def`;
- `trabalhos.def` → `academic-works.def`;
- `projetos.def` → `research-projects.def`;
- `objetos.def` → `objects.def`;
- `bibliografia.def` → `bibliography.def`;
- `postextuais.def` → `backmatter.def`.

Public API, normative predicates and article runtime were unchanged. A historical N12 hash bridge was added only to map renamed `\ProvidesFile` identities back to the frozen N12 manifest during verification.

Certified resulting main `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`:

- Source Contract #367 — SUCCESS;
- LaTeX preflight push #1030 — SUCCESS;
- exact Gate T #1031 — SUCCESS;
- Distribution #239 — SUCCESS.

This SHA is the certified base of A2.

## N15-B2R-A2 — ACTIVE

Branch: `refactor/n15-b2r-a2-user-layout`  
PR: #147 (draft)  
Base: certified main `eefa06598b9c99e0e27e70ecad0d2bbe99aa70b1`.

### Implemented canonical layout

| Previous | Canonical |
| --- | --- |
| `documento.tex` | `main.tex` |
| `1-pre-textuais/` | `frontmatter/` |
| `2-textuais/` | `chapters/` |
| `3-pos-textuais/` | `backmatter/` |
| `figuras/` | `figures/` |
| `assets/institucional/` | `assets/institutional/` |
| `assets/institucional/brasao-ufc.PNG` | `assets/institutional/ufc-coat-of-arms.png` |

Repository template and generated complete template/Overleaf bundles intentionally use the same canonical content layout. Overleaf keeps `main.tex` at archive root.

Portuguese leaf academic-content filenames remain intentionally unchanged in A2, for example `frontmatter/resumo.tex`, `backmatter/apendices/` and `backmatter/anexos/`.

### Synchronized A2 consumers

A2 has synchronized:

- Makefile default entrypoint;
- `main.tex` inputs and bibliography;
- example-image/listing references;
- institutional default asset path;
- image downloader;
- coordinated validation runner;
- reference/corpus/PDF-validator/PDF-A checks;
- Overleaf stable/import-bundle checks;
- deterministic bundle builder and release-package checker;
- auxiliary reference/distribution workflows;
- README and active B2R documentation;
- `tests/smoke/perfil-base.tex` after CI exposed stale frontmatter paths;
- `normativa/reference-guide-map.json` source-file trace paths after CI exposed stale chapter paths.

The last item is a secondary documentation/rastreability map. Its own policy remains `normative_contract_changed=false`; no predicate, value, source authority or normative locator was changed.

`tests/v2-distribution-check.sh` rejects reintroduction of old A2 top-level paths and scans active tracked text for stale path references, while allowing explicit migration/history ledgers to record old names.

### N12 frozen boundary

`.github/workflows/latex-preflight.yml` remains byte-identical at:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`

A2 adapts scripts called by that workflow rather than editing the workflow itself.

### Exact-head CI findings and repairs

First cycle, head `1f80043139ae9fabe68c554c264ef7d8c5087cd8`:

- Source Contract #368 — SUCCESS;
- Reference Preview #22 — `main.tex` reference build SUCCESS before later PDF/A/proxy steps;
- LaTeX preflight #1032 — FAILED in two jobs due to stale path consumers.

Repairs:

1. `normativa/reference-guide-map.json`: `source_file` traces moved from `2-textuais/...` to `chapters/...`;
2. `tests/smoke/perfil-base.tex`: summary/abstract paths moved from `1-pre-textuais/...` to `frontmatter/...`.

Second documented cycle, head `8b1a0a8013c10cc73ad43115b25d0beca567e529`:

- Source Contract #376 — FAILED in `normative_currency.py` because the rewritten human currency document no longer exposed the exact full strings required for supersession pairs such as `ABNT NBR 14724:2011` → `ABNT NBR 14724:2024`;
- catalog, precedence, source audit, source references and locator audit all passed before that documentation assertion failed.

Repair:

3. `docs/VIGENCIA-NORMATIVA.md` now preserves the corrected B2A article state **and** explicitly lists every exact superseded/current ABNT reference required by `normativa/version-policy.json`, plus the exact CEPE authority markers expected by the checker. The repair commit before this documentation sync is `5539e5370447fd97e844dfbadf4663992ab0e176`.

The failed #1032 and #376 runs remain historical evidence. Neither failure indicates runtime formatting drift; both exposed stale or incomplete migration/documentation consumers and were fixed without changing normative predicates, values, locators or authority.

### A2 invariants

- no public `\ufcsetup` key/value change;
- no article runtime change;
- no formatting/pagination intent change;
- no normative predicate/value/locator/authority change;
- N12 workflow byte-identical;
- UFC institutional mark remains excluded from public bundles;
- reference image hashes/licensing unchanged.

### A2 closure criteria

A2 can be marked DONE only when all are true on one exact PR head:

1. Source Contract green;
2. Reference Preview/reference corpus/PDF-A green;
3. LaTeX preflight green, including twelve-profile matrix and PDF/A;
4. Overleaf compatibility/import checks green;
5. required Windows literal-font certification green under Gate T;
6. deterministic Distribution preflight green;
7. N12 workflow blob unchanged;
8. no active stale A2 path references;
9. PR `behind_by=0` immediately before merge;
10. `HANDOFF`, B2R inventory, release ledger, README/NORMAS/VIGENCIA/NAMING as applicable synchronized with the exact candidate;
11. squash merge completed;
12. resulting `main` re-certified before B2R-B starts.

## Next executable action

1. treat the new live PR head produced by this documentation synchronization as the sole certification candidate;
2. inspect its Source Contract, Reference Preview and LaTeX preflight runs;
3. fix only reproducible remaining A2 path/packaging/documentation regressions and record each finding here/ledger;
4. once those checks are green, run exact-head Gate T and Distribution certification;
5. verify `behind_by=0`;
6. synchronize documentation one final time without changing implementation semantics;
7. squash-merge PR #147;
8. re-certify resulting `main`;
9. only then create B2R-B from certified main.

## Later phases

### N15-B2R-B

Create a machine-readable public API inventory; introduce canonical English project-owned keys/values/commands where justified; preserve current Portuguese API as compatibility aliases throughout v2.x; prove semantic/output equivalence.

### N15-B2B

Implement the scientific-article runtime directly on the final naming architecture, preferably through profile capabilities rather than scattered article conditionals. Article baseline must preserve single spacing, continuous primary-section flow and first-page-visible pagination as required by the reconciled contract.

### N15-B2C

Close article evidence with positive fixtures, final-PDF measurements, bounded negatives/sensitivity cases, canonical-English/Portuguese compatibility proof and complete documentation.

### N15-B3

Resolve remaining pre-release items including deterministic production-reference experiment/issue #18 and any blockers exposed by B2R/B2B/B2C.

### N15-C / N15-D

Promote version metadata only after prior phases close; build final deterministic class/template/Overleaf/CTAN candidates; certify exact final head; then decide tag/release. Historical rehearsal branches/PRs are evidence only.
