# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R-B3 is DONE. N15-B2R-B4 is ACTIVE from the exact fully certified B3 `main`. B4 is evidence-only: it must prove Portuguese/canonical-English semantic and rendered equivalence without changing the certified public-API runtime.**

Certified B4 base `main`:

`92f17418dfeee4d2d45456912af9f8c399457cc1`

Active branch:

`refactor/n15-b2r-b4-en-pt-equivalence`

Live Git/PR/CI state is the execution authority. Do not add receipt-only commits merely to record a transient branch head.

## Mandatory guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- v2.x public API migration is additive;
- supported Portuguese setup keys/values/commands/environments remain supported;
- B4 must not change the public API surface, normative behavior or `abntexto-ufc/public-api.def`;
- B4 frozen public-API runtime blob: `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- setup inventory remains exactly 132 keys / 79 scoped values;
- command/environment inventory remains exactly 77 commands / 11 environments / 2 extension hooks;
- scientific-article runtime remains disabled until B2R-B4 closes and the resulting `main` is fully re-certified;
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
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | DONE — PR #154 |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | ACTIVE |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B4 |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by N15-B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## B2R-B1/B2 — frozen prerequisites

B1 froze the pre-migration API baseline; B2 added reviewed canonical-English `\ufcsetup` aliases while preserving Portuguese compatibility.

Frozen contracts:

- B1: `release/n15-b2r-b-public-api.json`, blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2: `release/n15-b2r-b2-setup-aliases.json`, blob `19df208fb59af5ea37556d962e5986a43094c7f5`.

B2 final setup inventory:

- 67 legacy setup keys + 65 canonical keys = 132 live keys;
- 45 legacy scoped values + 34 canonical scoped values = 79 live `(key,value)` identities;
- Portuguese compatibility remains supported;
- `type=article` and its compatibility form remain reserved-only, not runtime support.

## B2R-B3 — DONE

B3 added canonical command/environment wrappers in `abntexto-ufc/public-api.def` without rewriting certified behavior modules.

Final inventory:

- 47 prior commands preserved;
- 30 canonical commands added;
- 77 commands total;
- 6 prior UFC environments preserved;
- 5 canonical environments added;
- 11 environments total;
- 2 extension hooks unchanged;
- setup surface unchanged at 132/79;
- article runtime remained false.

Important semantic decisions remain frozen:

- `\ufcPrintSummary` and `\ufcPrintAbstract` are distinct;
- `\ufcPrintEpigraph[short|long]` forwards to compatibility values `[curta|longa]`;
- `\ufcPrintListOfTextTables` preserves the distinct `quadro` concept;
- optional listing/minted/algorithm aliases exist only when their certified module surface is live;
- upstream `\keywords` remains upstream API.

B3 machine contract:

`release/n15-b2r-b3-command-environment-aliases.json`

Frozen B3 blob for B4:

`bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`

### B3 exact-head closure

PR #154 final exact head:

`0630d19cb6ba3274d0e2e1a738343f8c74afe148`

Before merge:

- `behind_by=0`;
- Normative Source Contract #432 — SUCCESS, run `33252829652`;
- LaTeX preflight #1104 — SUCCESS, run `33252829650`.

PR #154 was squash-merged with expected-head protection, producing:

`main` `92f17418dfeee4d2d45456912af9f8c399457cc1`

Post-merge certification on that exact SHA:

- Normative Source Contract #433 — SUCCESS, run `33253212796`;
- LaTeX preflight push #1105 — SUCCESS, run `33253212823`;
- exact/dispatched Gate T #1106 — SUCCESS, run `33253216564`;
- Distribution #248 — SUCCESS, run `33253212813`;
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

B3 is closed. No standalone receipt-only B3 state-sync PR is allowed.

## B2R-B4 — ACTIVE

### Authority and machine contract

B4 starts only from certified `main` `92f17418...` and is recorded in:

`release/n15-b2r-b4-en-pt-equivalence.json`

B4 freezes:

- B1 contract blob `c1f545e0e707822959db851a74d29f4068dff731`;
- B2 contract blob `19df208fb59af5ea37556d962e5986a43094c7f5`;
- B3 contract blob `bfcbf8aca3fba3fd602f62895f10fa2d6277b5a4`;
- public-API runtime blob `7b61fe70dd85ed895140f846272e097e3ded72cf`;
- N12 workflow blob `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

B4 has no authority to add/remove aliases or change formatting/runtime semantics. Any mismatch must first be classified as evidence/fixture defect versus a previously undetected API defect; runtime changes would require an explicit scope decision rather than silent repair.

### Equivalence model

Raw PDF byte identity is deliberately not required because document metadata/internal identifiers may vary. Observable behavior must be equivalent.

B4 proves:

1. static forwarding integrity for the complete reviewed B2/B3 mappings;
2. exact normalized internal state after equivalent Portuguese and canonical-English setup;
3. exact `pdftotext -layout` output;
4. equal page count and page size;
5. equal generated TOC/list/bibliography artifacts when present;
6. equal per-page raster SHA-256 at fixed rendering parameters;
7. PDF/A-2b declaration for both outputs.

The paired fixture exercises representative pre-textuals, lists, objects, code, algorithms and references with identical content. Full existing Gate T/Distribution remains mandatory after merge and supplies the broader profile/engine/Overleaf/Windows coverage.

### B4 executable evidence

New evidence surfaces:

- `tests/checks/public_api_equivalence_contract.py` — freezes B1/B2/B3/runtime/N12 identities, validates static forwarding and invokes the paired gate;
- `tests/normativa/public-api-equivalence.tex` — one source template compiled as Portuguese compatibility mode and canonical-English mode;
- `tests/fixtures/public-api-equivalence-summary.tex` — neutral summary content for paired execution;
- `tests/v2-public-api-equivalence-check.sh` — compiles both variants and compares state/text/geometry/auxiliary artifacts/raster/PDF-A;
- `tests/run.py` — `repository` now depends on `public-api-equivalence`, so the existing frozen structural workflow runs B4 automatically without editing `.github/workflows/latex-preflight.yml`.

Expected B4 inventory is unchanged: 132 setup keys, 79 scoped values, 77 commands, 11 environments and 2 hooks.

### B4 closure gate

Before B4 can be marked DONE:

1. finish executable evidence and documentation synchronization;
2. set the B4 ledger to `PR_CERTIFICATION_PENDING`;
3. inspect complete branch diff against `92f17418...` and require `behind_by=0`;
4. open the B4 PR and freeze its final head;
5. require Normative Source and LaTeX preflight SUCCESS on that exact head, including the B4 equivalence gate;
6. squash-merge with expected-head protection;
7. re-certify the resulting `main` through Source, full push preflight/Gate T and Distribution;
8. require Windows literal-font certification and Overleaf stable proxy SUCCESS through the normal Gate T;
9. only then mark B2R-B4 DONE and unblock N15-B2B scientific-article runtime.

Do not start scientific-article runtime before this closure completes.
