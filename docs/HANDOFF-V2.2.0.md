# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R-B2 implementation is DONE and fully post-merge certified. A bounded documentation state sync is the only remaining B2 closure action before B2R-B3 starts.**

Certified B2 implementation `main`:

`f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`

State-sync branch:

`docs/n15-b2r-b2-post-merge-sync`

Live Git/PR/CI state is always the execution authority. This bounded state sync records the completed B2 implementation. After this branch is merged and the resulting `main` is certified once, do **not** open another receipt-only synchronization PR; begin B2R-B3 from that certified `main` and update active state there.

## Mandatory guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- public API migration in v2.x is additive;
- supported Portuguese setup keys/values remain accepted throughout v2.x;
- canonical aliases forward to certified behavior rather than rewriting normative/runtime semantics;
- scientific-article runtime remains disabled until B2R-B closes and the resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- class version remains v2.1.0 until N15-C release-candidate promotion;
- branch cleanup remains deferred until final certification/tag.

## Canonical roadmap

| Phase | Scope | Status |
| --- | --- | --- |
| N0–N14 | normative/runtime/evidence baseline | DONE |
| N15-A | unrestricted final audit | DONE — PR #143 |
| N15-B1 | source completeness/authority reconciliation | DONE — PR #144 |
| N15-B2A | scientific-article source + normative contract | DONE — PR #145 |
| N15-B2R-A1 | internal module English naming | DONE — PR #146 |
| N15-B2R-A2 | user/example/distribution layout naming | DONE — PR #148 + state sync |
| N15-B2R-B1 | public-API baseline + executable contract | DONE — PR #150 + PR #151 state sync |
| N15-B2R-B2 | canonical-English setup keys/values + Portuguese compatibility | DONE IMPLEMENTATION — state sync pending |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | BLOCKED only by B2 state-sync merge/re-certification |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | BLOCKED by B3 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## B2R-B1 — DONE

PR #150 established the pre-migration public/exported API baseline and executable checker. PR #151 synchronized that result. Its resulting certified `main` was:

`1a3731575f9fe06a7f7d9a132f5152998edc6cee`

That SHA passed Source #425, preflight/Gate T #1094 and Distribution #245, including reference/PDF-A, 12-profile matrix/PDF-A, objects/bibliography, post-textuals, Overleaf, Windows literal-font certification and deterministic distribution.

## B2R-B2 — implementation DONE

### Architecture

B2 added one canonical public API layer:

`abntexto-ufc/public-api.def`

It is loaded after the existing runtime modules and defines canonical-English `l3keys` aliases that forward to the already-certified Portuguese behavior. Existing internals remain unchanged. No command/environment alias and no article runtime were introduced.

### Machine contracts

The B1 baseline remains frozen:

- `release/n15-b2r-b-public-api.json`;
- certified blob: `c1f545e0e707822959db851a74d29f4068dff731`.

B2 additions are recorded in:

`release/n15-b2r-b2-setup-aliases.json`

### Final B2 surface

- legacy setup keys: 67;
- canonical setup keys added: 65;
- total setup keys: 132;
- legacy enumerated `(key,value)` identities: 45;
- canonical enumerated identities added: 34;
- total enumerated setup-value identities: 79;
- exported commands: 47, unchanged;
- UFC environments: 6, unchanged;
- explicit extension hooks: 2, unchanged;
- article runtime: false.

`volume` remains canonical as-is and therefore does not gain a duplicate alias. The project-specific coat-of-arms compatibility key remains compatibility-only.

### Canonical setup decisions

Profiles:

- `undergraduate-capstone`;
- `specialization-capstone`;
- `masters-thesis`;
- `doctoral-thesis`;
- `research-project`;
- `anonymized-research-project`.

Other choices:

- `print-mode`: `single-sided`, `double-sided`;
- booleans: `true`, `false`;
- `cover`: `auto`, `true`, `false`;
- `font`: `times`, `arial`;
- `tables`: `native`, `tabularray`;
- `code`: `none`, `listings`, `minted`;
- `algorithms`: `none`, `algpseudocodex`;
- `glossary`: `none`, `glossaries`;
- `index`: `none`, `imakeidx`.

Detailed metadata names were reviewed semantically, including graduate-program/program/degree-field/concentration distinctions, project nature statements, grammatical advisor/coadvisor labels and examiner metadata.

### Executable evidence

`tests/checks/public_api_contract.py` validates the frozen B1 ledger plus the B2 delta. Functional forwarding is exercised by:

- `tests/normativa/public-api-aliases.tex`;
- `tests/v2-public-api-alias-check.sh`.

Exact PR-head evidence on `2fd3bc28cc37e6c05f4e37f0b0315adb99765573`:

- Normative Source Contract #426 — SUCCESS, run `33247218637`;
- LaTeX preflight #1096 — SUCCESS, run `33247218623`;
- alias smoke: `keys=65 status=PASS`;
- public API evidence: `legacy_keys=67 canonical_keys=65 keys=132 legacy_values=45 canonical_values=34 values=79 commands=47 environments=6 hooks=2 article_runtime=false`;
- `behind_by=0` immediately before merge.

PR #152 was squash-merged with exact-head protection and produced:

`main` `f6ba39bcbe50c324f6ab5f1856595cfcf7f8f0f9`.

Post-merge certification of that exact `main`:

- Normative Source Contract #427 — SUCCESS, run `33247641697`;
- LaTeX preflight/Gate T #1097 — SUCCESS, run `33247641696`;
- Distribution #246 — SUCCESS, run `33247641702`;
- reference + PDF/A-2b — SUCCESS;
- 12-profile matrix + PDF/A-2b — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structure/layout/fonts/pre-textuals/projects — SUCCESS;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build — SUCCESS;
- Windows literal-font identity, Unicode extraction, embedding and PDF/A-2b certification — SUCCESS;
- release preflight + release PDF/A-2b — SUCCESS;
- deterministic release bundles — SUCCESS;
- Overleaf import-bundle proxy — SUCCESS;
- release candidate upload + aggregate distribution-preflight — SUCCESS;
- GitHub Release publication — correctly SKIPPED because no tag exists.

Therefore B2 runtime/API implementation is fully certified.

## B2 bounded state-sync closure

This branch may change only active state/documentation ledgers. It must not change runtime, tests, normative contracts, formatting intent or `.github/workflows/latex-preflight.yml`.

Closure sequence:

1. merge this bounded state-sync PR after exact-head Source/preflight SUCCESS and `behind_by=0`;
2. certify its resulting `main` once through Source, push preflight/Gate T and Distribution;
3. do not create another receipt-only state-sync PR;
4. create `refactor/n15-b2r-b3-command-environment-aliases` from that certified `main`;
5. begin B3 by classifying the 47 exported commands and 6 UFC environments before adding wrappers;
6. keep `type=article` / its compatibility form reserved-only until B2R-B4 closes and N15-B2B begins.

## B2R-B3 design boundary

B3 owns canonical project command/environment names and compatibility wrappers. It must not mechanically rename every exported helper. Before implementation each existing exported surface must be classified as:

- canonical project API;
- Portuguese compatibility API;
- upstream compatibility API;
- exported helper;
- extension hook;
- internal implementation accidentally exported.

Known reviewed command directions from B1 include cover, title page, approval page, catalog card, references and bibliography-resource surfaces. Summary/abstract canonicalization still requires explicit language-role validation so vernacular and foreign-language summaries are never conflated.

Full paired Portuguese/English semantic and rendered-output equivalence remains B2R-B4 scope.
