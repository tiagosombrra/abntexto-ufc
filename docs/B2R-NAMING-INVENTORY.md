# N15-B2R naming inventory

Updated: 2026-08-28

Certified B2R-B1 runtime/checker head: `main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`.

Current state-sync branch: `docs/n15-b2r-b1-post-merge-sync`.

B2R-A is closed. B2R-B is active. **B2R-B1 is DONE, merged via PR #150 and fully post-merge re-certified.**

This document is the human companion to the active machine ledger `release/n15-b2r-b-public-api.json`. `release/n15-b2r-a-naming-inventory.json` remains historical B2R-A/N12-sensitive evidence and must not be repurposed.

## B2R-A — DONE

B2R-A1 normalized internal package module filenames to English. B2R-A2 normalized repository/example/distribution-facing engineering paths, including `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, `figures/` and `assets/institutional/`, while intentionally preserving Portuguese academic leaf filenames.

The frozen N12 workflow remains byte-identical at blob:

`aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

The certified base used to start B2R-B1 was:

`3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

## B2R-B1 — PUBLIC API BASELINE/CHECKER — DONE

PR #150 was squash-merged from exact head:

`6d51593e1a167ae657c8dd019f913dc947c34250`

and produced:

`main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`.

B1 intentionally adds no canonical-English runtime aliases. It freezes and classifies the pre-migration API/export surface.

### Baseline counts

The machine ledger records:

- 2 class entrypoints;
- 67 `\ufcsetup` keys;
- 45 enumerated setup values scoped by `(setup key, value)`;
- 47 exported commands;
- 6 UFC environments;
- 2 explicit extension hooks: `\ufcsectionhook` and `\ufcobjectlegendhook`.

Setup-value identity is explicitly `(setup key, value)`. Values such as `true`, `false`, `sim` and `nao` may legitimately occur under multiple independent keys.

The future `type=article` / `tipo=artigo` pair remains reserved-only; article runtime is still blocked until N15-B2B.

### Checker contract

`tests/checks/public_api_contract.py` fails on missing baseline surfaces, duplicate inventory identities, supported-surface removal, unreviewed new project-owned public identifiers and drift of the frozen N12 workflow blob.

`tests/run.py` makes `public-api` a dependency of `repository`, so the frozen workflow transitively enforces the contract.

### Legacy-identity boundary

The B1 diagnostic cycle proved the new checker was correct and exposed a separate older canonical-identity boundary. The final policy is deliberately narrow: the deprecated legacy compatibility entrypoint's exact identity is confined to the two required structured inventory fields. Narrative or arbitrary new occurrences remain rejected. No broad scanner exemption was introduced.

### Final pre-merge certification

Exact PR head `6d51593e1a167ae657c8dd019f913dc947c34250` passed:

- Normative Source Contract #422 — SUCCESS, run `33226621307`;
- LaTeX preflight #1090 — SUCCESS, run `33226621382`;
- `behind_by=0` before merge;
- frozen N12 workflow preserved.

### Post-merge certification

Resulting `main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4` passed:

- Normative Source Contract #423 — SUCCESS, run `33227898818`;
- LaTeX preflight push #1091 — SUCCESS, run `33227898801`;
- exact/dispatched Gate T #1092 — SUCCESS, run `33227902517`;
- Distribution #244 — SUCCESS, run `33227898819`.

Gate T covered structure/layout/fonts/pre-textuals/projects, reference/PDF-A, complete 12-profile matrix/PDF-A, objects/bibliography, post-textuals, Overleaf stable proxy, Windows literal Times New Roman/Arial build, literal font identity, Unicode extraction, embedding and PDF/A certification.

Distribution #244 passed release preflight, release PDF/A-2b, deterministic bundles, Overleaf import proxy, candidate upload and the aggregate distribution-preflight. GitHub Release publication was correctly skipped because no tag exists.

No B1 change affected public runtime semantics, the normative contract, formatting intent, pagination intent or article runtime.

## B2R-B2 — canonical English setup aliases

B2R-B2 starts only after this B1 state synchronization is merged and its resulting `main` is re-certified.

### Reviewed canonical key direction

- `tipo` → `type`;
- `impressao` → `print-mode`;
- `capa` → `cover`;
- `ficha-catalografica` → `catalog-card`;
- `brasao` → `coat-of-arms`;
- `fonte` → `font`;
- `fonte-estrita` → `strict-font`;
- `tabelas` → `tables`;
- `codigo` → `code`;
- `algoritmos` → `algorithms`;
- `glossario` → `glossary`;
- `indice` → `index`;
- `autor` → `author`;
- `titulo` → `title`;
- `subtitulo` → `subtitle`;
- `data-aprovacao` → `approval-date`;
- `orientador` → `advisor`;
- `coorientador` → `coadvisor`.

### Reviewed profile values

- `tccgraduacao` → `undergraduate-capstone`;
- `tccespecializacao` → `specialization-capstone`;
- `dissertacao` → `masters-thesis`;
- `tese` → `doctoral-thesis`;
- `projeto` → `research-project`;
- `projetoanonimizado` → `anonymized-research-project`.

Canonical booleans use `true` / `false`; existing `sim` / `nao` remain compatibility values.

### Review-required boundary

Do not invent unresolved canonical vocabulary. In particular:

- `print-mode` values remain unresolved;
- detailed academic metadata (`programa-*`, `nome-*`, `titulo-*`, `area-*`, committee/member fields) requires semantic review;
- optional-module values such as current `nativo` / `nenhum` forms require an explicit decision;
- remaining commands and environments require classification/naming review before aliases are introduced.

Distinct fields such as `programa-mestrado`, `nome-mestrado`, `titulo-mestre` and `area-mestrado` must remain semantically distinct rather than being mechanically translated.

## Next executable action

1. Complete the four-file state-sync branch.
2. Open and exact-head certify its PR.
3. Squash-merge it and re-certify the resulting `main`.
4. Create `refactor/n15-b2r-b2-setup-aliases` from that exact certified main.
5. Begin additive setup aliases without scientific-article runtime.
