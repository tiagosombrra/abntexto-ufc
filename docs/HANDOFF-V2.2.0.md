# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R-B2 is DONE. N15-B2R-B3 is ACTIVE on the exact fully certified B2 main. Canonical command/environment aliases are implemented and are being prepared for exact-head PR certification.**

Certified B3 base `main`:

`cb0df822401a926c4c5987f904b29f5898fb1775`

Active branch:

`refactor/n15-b2r-b3-command-environment-aliases`

Live Git/PR/CI state is the execution authority. Do not add receipt-only commits merely to record a transient branch head.

## Mandatory guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- v2.x public API migration is additive;
- supported Portuguese setup keys/values/commands/environments remain supported;
- canonical aliases forward to certified behavior instead of rewriting normative/runtime semantics;
- B3 must not change the 132 setup keys, 79 scoped setup values or 2 extension hooks established before it;
- full EN/PT semantic and rendered equivalence remains B2R-B4 scope;
- scientific-article runtime remains disabled until B2R-B4 closes and the resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- class version remains v2.1.0 until N15-C;
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
| N15-B2R-B1 | public-API baseline + executable contract | DONE — PR #150 + PR #151 |
| N15-B2R-B2 | canonical setup keys/values + Portuguese compatibility | DONE — PR #152 + PR #153 |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | ACTIVE |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | BLOCKED by B3 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## B2R-B1 — DONE

PR #150 froze the pre-migration API baseline and checker; PR #151 synchronized that state. Frozen B1 contract:

- `release/n15-b2r-b-public-api.json`;
- blob `c1f545e0e707822959db851a74d29f4068dff731`;
- 67 setup keys;
- 45 scoped setup values;
- 47 commands;
- 6 UFC environments;
- 2 extension hooks.

## B2R-B2 — DONE

B2 introduced canonical-English `\ufcsetup` aliases in `abntexto-ufc/public-api.def` while preserving certified Portuguese behavior.

Final setup inventory:

- legacy setup keys: 67;
- canonical setup keys added: 65;
- setup keys total: 132;
- legacy scoped values: 45;
- canonical scoped values added: 34;
- scoped values total: 79;
- commands remained 47;
- environments remained 6;
- extension hooks remained 2;
- article runtime remained false.

PR #152 exact-head implementation certification:

- head `2fd3bc28cc37e6c05f4e37f0b0315adb99765573`;
- Source #426 — SUCCESS, run `33247218637`;
- preflight #1096 — SUCCESS, run `33247218623`;
- 65-key forwarding smoke — PASS;
- `behind_by=0` before merge.

PR #152 produced `main` `f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`, which passed Source #427, Gate T #1097 and Distribution #246.

PR #153 was the bounded B2 state sync. It was exact-head certified and squash-merged, producing the current B3 base:

`cb0df822401a926c4c5987f904b29f5898fb1775`.

Final B2 closure certification on that SHA:

- Normative Source Contract #429 — SUCCESS, run `33249228729`;
- LaTeX preflight/Gate T #1100 — SUCCESS, run `33249228669`;
- Distribution #247 — SUCCESS, run `33249228670`;
- reference + PDF/A-2b — SUCCESS;
- 12-profile matrix + PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structure/layout/fonts/pre-textuals/projects — SUCCESS;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build — SUCCESS;
- Windows identity/Unicode/embedding/PDF-A-2b certification — SUCCESS;
- release PDF/A-2b, deterministic bundles, Overleaf import proxy, candidate upload and aggregate distribution-preflight — SUCCESS;
- GitHub Release publication — correctly SKIPPED because no tag exists.

Therefore B2R-B2 is closed. No additional B2 receipt-only state-sync PR is allowed.

## B2R-B3 — ACTIVE

### Machine contract

B3 is recorded in:

`release/n15-b2r-b3-command-environment-aliases.json`

It freezes both prior contracts:

- B1 blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 blob `19df208fb59af5ea37556d962e5986a43094c7f5`.

B3 owns command/environment naming only. Setup surfaces, normative behavior, article runtime and the N12 workflow are outside its change authority.

### Command classification

The 47 B1 commands are now fully classified with no unresolved entry:

- 7 already-canonical project commands remain unchanged;
- 9 exported English helpers remain unchanged;
- upstream `\keywords` remains upstream API and is not renamed for local style;
- 25 Portuguese compatibility commands receive canonical English wrappers;
- 5 project public commands still using Portuguese/lowercase naming receive canonical wrappers.

Therefore B3 adds exactly **30 canonical commands**, producing **77 commands total** while preserving all 47 prior commands.

Important semantic decisions:

- `\imprimirabstract` → `\ufcPrintAbstract` remains the B1-approved English-language abstract surface;
- `\imprimirresumo` → `\ufcPrintSummary`; it must never alias to `\ufcPrintAbstract`;
- `\palavraschave` → `\ufcSummaryKeywords`; upstream `\keywords` remains the English-keyword surface;
- `\imprimirepigrafe[curta|longa]` → `\ufcPrintEpigraph[short|long]` with explicit value forwarding;
- `\imprimirlistadequadros` → `\ufcPrintListOfTextTables`, keeping the UFC/ABNT `quadro` object distinct from statistical tables and charts;
- `\ufcbibliografia` → `\ufcAddBibliographyResource`;
- `\ufcfonte` / `\ufcnota` → `\ufcSource` / `\ufcNote`;
- optional `\ufcInputListing` and `\ufcInputMinted` exist only when their certified legacy module surface exists.

All canonical wrappers live in `abntexto-ufc/public-api.def`; the certified behavior modules remain untouched.

### Environment classification

The six B1 environments are fully classified:

- `ufclisting` is already English and remains canonical as-is;
- `ufcalineas` → `ufclettereditems`;
- `ufcsubalineas` → `ufcdashedsubitems`;
- `ufclistadefinicoes` → `ufcdefinitionlist`;
- `ufcobjeto` → `ufcobject`;
- `ufcalgoritmo` → `ufcalgorithm`.

B3 therefore adds exactly **5 canonical environments**, producing **11 environments total**. Optional algorithm/listing surfaces remain conditional on their selected modules.

### Executable evidence

`tests/checks/public_api_contract.py` now validates B1+B2+B3 as layered contracts. It requires:

- B1 and B2 blob identity;
- setup inventory still exactly 132/79;
- complete 30-command migration-source coverage;
- B1-approved command targets unchanged;
- unique/live canonical command targets and reviewed signatures;
- complete 5-environment migration plus retained `ufclisting`;
- exactly 77 commands, 11 environments and 2 hooks;
- article runtime false;
- frozen N12 workflow blob exact;
- B2 setup alias smoke still passing;
- B3 command/environment smoke passing.

B3 smoke evidence:

- `tests/normativa/public-api-command-environment-aliases.tex`;
- `tests/v2-public-api-command-environment-check.sh`;
- checks all non-optional canonical commands/environments;
- activates `code=listings` and `algorithms=algpseudocodex` to verify conditional aliases;
- asserts that the minted alias is not live under `code=listings`.

### B3 closure gate

Before B3 can be marked DONE:

1. synchronize the active naming documents and set the B3 ledger to PR-certification-pending;
2. inspect the complete branch diff against certified base `cb0df822...` and require `behind_by=0`;
3. open the B3 PR and freeze its final head;
4. require Source and LaTeX preflight SUCCESS on that exact head;
5. squash-merge with expected-head protection;
6. re-certify resulting `main` through Source, full push Gate T/preflight and Distribution, including Windows and Overleaf;
7. perform at most one bounded state sync if B3 final receipts require it;
8. start B2R-B4 only from the resulting certified `main`.

Do not start B2R-B4 or scientific-article runtime before this closure completes.
