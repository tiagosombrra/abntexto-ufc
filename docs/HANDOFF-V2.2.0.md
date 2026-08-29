# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-29

Checkpoint: **N15-B2R-B2 is ACTIVE. B2R-B1 and its documentation state sync are merged and fully re-certified. Canonical-English setup aliases are implemented on the active B2 branch and are awaiting exact-head PR certification.**

Certified B2R-B2 base `main`:

`1a3731575f9fe06a7f7d9a132f5152998edc6cee`

Active branch:

`refactor/n15-b2r-b2-setup-aliases`

Live Git/PR/CI state is always the execution authority. Do not record a transient implementation head here merely to create another documentation-only commit.

## Mandatory documentation-sync policy

Documentation synchronization is a release gate. The active B2R state set is:

1. `docs/HANDOFF-V2.2.0.md` — canonical continuation point;
2. `docs/B2R-NAMING-INVENTORY.md` — human naming/API ledger;
3. `release/n15-b2r-b-public-api.json` — frozen B1 baseline contract;
4. `release/n15-b2r-b2-setup-aliases.json` — active B2 delta contract;
5. `docs/NAMING.md` — naming and compatibility policy.

`release/n15-b2r-a-naming-inventory.json` remains historical B2R-A/N12-sensitive evidence and must not be repurposed.

## Guardrails

- current technical standard > compatible UFC institutional requirement > implementation;
- no invented inaccessible ABNT wording or locators;
- `.github/workflows/latex-preflight.yml` remains frozen unless N12 is explicitly reopened;
- frozen N12 workflow blob: `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`;
- public API migration in v2.x is additive;
- supported Portuguese setup keys/values remain accepted throughout v2.x;
- B2 must forward to certified behavior rather than rewrite normative/runtime semantics;
- scientific-article runtime remains disabled until all B2R-B subphases close and resulting `main` is re-certified;
- UFC institutional mark and proprietary Microsoft fonts remain excluded from public bundles;
- class version remains v2.1.0 until N15-C release-candidate promotion;
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
| N15-B2R-B1 | public-API baseline + executable contract | DONE — PR #150 + PR #151 state sync |
| N15-B2R-B2 | canonical-English setup keys/values + Portuguese compatibility | ACTIVE |
| N15-B2R-B3 | canonical commands/environments + compatibility wrappers | BLOCKED by B2 |
| N15-B2R-B4 | EN/PT semantic/output equivalence + exact-head closure | BLOCKED by B3 |
| N15-B2B | scientific-article runtime | BLOCKED by B2R-B |
| N15-B2C | scientific-article evidence closure | BLOCKED by B2B |
| N15-B3 | remaining pre-release corrections | BLOCKED by B2C |
| N15-C | v2.2.0 release candidate | BLOCKED by B3 |
| N15-D | final exact-head certification/release decision | BLOCKED by N15-C |

N15 remains ACTIVE.

## B2R-B1 — DONE

PR #150 established the pre-migration API baseline and executable checker. Its exact pre-merge head was:

`6d51593e1a167ae657c8dd019f913dc947c34250`

The merge produced `main` `4d9483ea6acd1dbb86622999a1f289fd6f67bce4` and passed Source #423, preflight #1091, Gate T #1092 and Distribution #244.

PR #151 synchronized the active B2R documentation with that certified state and produced the current B2 base:

`main` `1a3731575f9fe06a7f7d9a132f5152998edc6cee`

Post-#151 certification on this SHA:

- Normative Source Contract #425 — SUCCESS, run `33245817659`;
- LaTeX preflight/Gate T #1094 — SUCCESS, run `33245817721`;
- Distribution #245 — SUCCESS, run `33245817632`;
- reference + PDF/A — SUCCESS;
- 12-profile matrix + PDF/A — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- Overleaf stable proxy — SUCCESS;
- Windows literal Times New Roman/Arial build and identity/Unicode/embedding/PDF-A certification — SUCCESS;
- release PDF/A, deterministic bundles, Overleaf import proxy and candidate upload — SUCCESS.

Therefore `1a373157...` is the formal certified starting point for B2R-B2.

## N15-B2R-B2 — ACTIVE

### Architecture

B2 uses one canonical API layer:

`abntexto-ufc/public-api.def`

It is loaded after the existing runtime modules and defines canonical-English `l3keys` aliases that forward to the already-certified Portuguese behavior. Existing internals remain unchanged. This keeps the migration additive and gives B3 a single extension point for later command/environment wrappers.

### Machine contracts

The B1 baseline remains immutable during B2 and is verified by blob identity:

- path: `release/n15-b2r-b-public-api.json`;
- certified blob: `c1f545e0e707822959db851a74d29f4068dff731`.

B2 additions are recorded separately in:

`release/n15-b2r-b2-setup-aliases.json`

The executable checker validates the frozen B1 snapshot plus the B2 delta.

### Surface counts

B2 preserves the entire B1 surface and adds only setup aliases:

- legacy setup keys: 67;
- canonical setup keys added: 65;
- total setup keys: 132;
- legacy enumerated `(key,value)` identities: 45;
- canonical enumerated `(key,value)` identities added: 34;
- total enumerated setup-value identities: 79;
- exported commands: 47, unchanged;
- UFC environments: 6, unchanged;
- explicit extension hooks: 2, unchanged;
- article runtime: false.

`volume` remains the same canonical identifier and therefore does not create a duplicate English alias. The project-specific coat-of-arms compatibility key remains compatibility-only and does not gain a second canonical key.

### Canonical value decisions

- profile values: `undergraduate-capstone`, `specialization-capstone`, `masters-thesis`, `doctoral-thesis`, `research-project`, `anonymized-research-project`;
- `print-mode`: `single-sided`, `double-sided`;
- booleans: `true`, `false`;
- `cover`: `auto`, `true`, `false`;
- `font`: `times`, `arial`;
- `tables`: `native`, `tabularray`;
- `code`: `none`, `listings`, `minted`;
- `algorithms`: `none`, `algpseudocodex`;
- `glossary`: `none`, `glossaries`;
- `index`: `none`, `imakeidx`.

Package names remain package names rather than being translated.

### Semantic metadata decisions

Detailed metadata names are semantic rather than mechanical translations. Examples include:

- `masters-graduate-program` versus `masters-program`;
- `masters-degree-field` versus `masters-concentration`;
- doctorate analogues with the same distinction;
- `project-nature-statement` for the full nature statement;
- `advisor-feminine-label` / `coadvisor-feminine-label` for the grammatical-label switches;
- `examiner-N`, `examiner-N-unit`, `examiner-N-institution` for committee members.

No B2 setup key/value remains `review_required` in the active delta.

### Executable evidence

`tests/checks/public_api_contract.py` now verifies:

- the B1 ledger blob is unchanged;
- additive setup-key/value sets exactly match the B2 delta;
- every legacy setup key has a reviewed canonical disposition;
- every legacy enumerated value maps to a live canonical `(key,value)` identity;
- command/environment/hook counts remain unchanged;
- article runtime remains disabled;
- the frozen N12 workflow blob remains exact;
- the canonical setup alias smoke test passes.

Functional smoke evidence:

- fixture: `tests/normativa/public-api-aliases.tex`;
- runner: `tests/v2-public-api-alias-check.sh`;
- all 65 canonical setup keys are exercised with side-effect-safe values;
- the fixture asserts the resulting certified legacy state for document type, print mode, cover/catalog/coat booleans, metadata, font/module settings, coat-of-arms file and initial pagination.

Rendered EN/PT equivalence remains intentionally reserved for B2R-B4; B2 validates forwarding semantics, not final paired-PDF identity.

## B2 completion gate

Before B2 can be marked DONE:

1. inspect the complete branch diff against certified `main` `1a373157...`;
2. ensure `behind_by=0`;
3. open the B2 PR;
4. freeze its final implementation/documentation head;
5. require Normative Source Contract and LaTeX preflight SUCCESS on that exact head;
6. squash-merge with exact-head protection;
7. re-certify the resulting `main` with Source, push preflight/Gate T and Distribution;
8. perform a bounded post-merge state sync if receipts must be recorded;
9. only then create B2R-B3 from the resulting certified `main`.

Do not start B2R-B3 or N15-B2B before this closure completes.
