# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-28

Checkpoint: **N15-B2R-B1 is DONE and fully post-merge re-certified; the documentation state-sync PR is the only gate before B2R-B2**.

Certified B2R-B1 `main`: `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`.

Current state-sync branch: `docs/n15-b2r-b1-post-merge-sync`.

Always read the live repository head, PR state and GitHub Actions receipts before mutation or merge. This file is the canonical continuation state; live Git/CI remains the execution authority.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate, not optional housekeeping.

The active B2R state documents are:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — human naming/API ledger;
3. `release/n15-b2r-b-public-api.json` — active B2R-B machine ledger;
4. `docs/NAMING.md` — naming and compatibility policy.

`release/n15-b2r-a-naming-inventory.json` is historical B2R-A/N12-sensitive evidence. Do not simplify, repurpose or rewrite it merely to reflect B2R-B state.

A B2R subphase must not be treated as fully handed off while these active documents disagree with live Git/PR/CI state.

## Guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording/locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- no supported Portuguese public-API removal in v2.x;
- B2R public-API migration is additive;
- no scientific-article runtime before all B2R-B subphases close and the resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- physical branch cleanup remains deferred until final certification/tag.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness/authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146 |
| N15-B2R-A2 | user/example/distribution layout naming | DONE — PR #148 + state sync |
| N15-B2R-B1 | public-API inventory + executable baseline checker | DONE — PR #150; post-merge re-certified |
| N15-B2R-B2 | additive canonical-English setup keys/values + Portuguese aliases | BLOCKED only by B1 state-sync merge/re-certification |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | BLOCKED by B2 |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | BLOCKED by B3 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## B2R-A closure

B2R-A1 normalized internal module names. B2R-A2 normalized repository/example/distribution-facing engineering paths while preserving Portuguese academic leaf filenames and public API semantics.

The certified base used to start B2R-B1 was:

`3a7d5e55d0bbd8df279e3e3f6eecb72b98af709b`.

## N15-B2R-B1 — DONE

PR #150 (`audit: establish B2R-B public API baseline`) was squash-merged with exact-head protection from:

`6d51593e1a167ae657c8dd019f913dc947c34250`

and produced:

`main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`.

B1 introduced no canonical-English runtime aliases. It froze and classified the pre-migration API/export surface before additive migration.

The machine contract records:

- 2 class entrypoints;
- 67 `\ufcsetup` keys;
- 45 enumerated values scoped by `(setup key, value)`;
- 47 exported commands;
- 6 UFC environments;
- 2 explicit extension hooks;
- upstream compatibility overrides separately from project-owned API;
- `type=article` / `tipo=artigo` only as reserved future surfaces, with article runtime disabled.

`tests/checks/public_api_contract.py` rejects baseline removals, duplicate identities and unreviewed public additions, and verifies the frozen N12 workflow blob. `tests/run.py` makes `public-api` a dependency of `repository`, so the frozen workflow enforces it without workflow edits.

### B1 diagnostic history

The first implementation head proved the new API checker itself was correct but exposed an older canonical-identity boundary around the machine ledger. That boundary was corrected narrowly. A later documentation-sync diagnostic proved that narrative repetition of the deprecated legacy identity was also rejected. The final solution confines that exact legacy identity to the two structured inventory fields rather than broadening scanner exemptions.

No public API behavior, normative contract, formatting intent, pagination intent or article runtime changed in B1.

## B1 certification receipts

### Final PR head before merge

Head `6d51593e1a167ae657c8dd019f913dc947c34250`:

- Normative Source Contract #422 — SUCCESS, run `33226621307`;
- LaTeX preflight #1090 — SUCCESS, run `33226621382`;
- `behind_by=0` immediately before merge;
- frozen N12 workflow blob preserved.

### Resulting merged main

`main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4`:

- Normative Source Contract #423 — SUCCESS, run `33227898818`;
- LaTeX preflight push #1091 — SUCCESS, run `33227898801`;
- exact/dispatched Gate T #1092 — SUCCESS, run `33227902517`;
- Distribution #244 — SUCCESS, run `33227898819`.

Gate T #1092 certified structure, reference/PDF-A, 12 profiles/PDF-A, objects/bibliography, post-textuals, Overleaf proxy, Windows literal Times New Roman/Arial build and literal-font identity/Unicode/embedding/PDF-A.

Distribution #244 passed release preflight, release PDF/A-2b, deterministic bundles, Overleaf import proxy, candidate upload and aggregate distribution-preflight. `Publish GitHub Release` was correctly skipped because this commit is not a tag.

Therefore **B2R-B1 is DONE**.

## N15-B2R-B2 — next implementation phase

B2R-B2 begins only from the re-certified `main` produced after this documentation state-sync PR.

Implement setup aliases additively and forward to certified Portuguese behavior wherever practical. Already-reviewed canonical key direction includes:

- `tipo` → `type`;
- `impressao` → `print-mode` (key name reviewed; values still unresolved);
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

Reviewed profile values are `undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project` and `anonymized-research-project`. Canonical booleans are `true` / `false`; existing `sim` / `nao` remain compatibility forms.

Do not mechanically translate unresolved metadata, print-mode values, optional-module values, commands or environments. Do not activate `article` runtime in B2R-B2.

## Next executable action

1. Finish the four-file B2R-B1 state-sync branch.
2. Open and exact-head certify its PR.
3. Squash-merge the state-sync PR.
4. Re-certify the resulting `main` with Source Contract, push preflight, Gate T and Distribution.
5. Create a fresh `refactor/n15-b2r-b2-setup-aliases` branch from that exact certified `main`.
