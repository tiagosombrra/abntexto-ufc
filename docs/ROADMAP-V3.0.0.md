# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**ACTIVE — V3-R1 complete repository rebaseline.**

Certified v2 baseline: `main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`.

Clean v3 planning baseline: `ca2ab12163d16e5eef80c0c8ce9fea543064ab10`.

Active implementation branch: `refactor/v3-r1-rebaseline`.

Latest completed implementation checkpoint before this authority synchronization: `36375e94ce9c6e2048eff2ec9cdcb9f8573b05b7`.

Superseded branches are evidence only and must not be used as implementation sources:

- `refactor/n15-b2r-c-full-english-canonicalization`;
- `refactor/v3-full-internationalization`;
- `refactor/v3-foundation-cleanup`;
- `refactor/v3-r1-rebaseline-temp`.

## Authorities

Read in this order:

1. `release/v3-roadmap.json` — machine phase authority;
2. `docs/HANDOFF-V3.0.0.md` — exact continuation checkpoint;
3. `docs/ROADMAP-V3.0.0.md` — human phase plan;
4. `docs/ARCHITECTURE.md`;
5. `docs/ENGINEERING-LANGUAGE.md`;
6. `release/v3-path-migration.json`;
7. `release/v3-api-migration.json`;
8. `release/v3-test-migration.json`.

A subgate cannot close while these authorities disagree.

## Non-negotiable policies

- target release: `3.0.0`;
- target physical repository identity: `abntexto-ufc`;
- project-controlled engineering language: English;
- project-controlled filenames, paths, code identifiers, LaTeX API, internal state, comments, diagnostics, scripts, tests, workflows, validator code/UI and technical documentation: English;
- Portuguese is allowed only as academic/rendered document content, bibliography data, official UFC/ABNT wording, test payload text when the Portuguese output itself is under test, or a genuinely required upstream identifier at an explicit integration boundary;
- no Portuguese project runtime compatibility API;
- no active `oracle` terminology: use `test`, `validation`, `expected` or another precise semantic name;
- no active v2/N-phase identifiers as engineering names;
- no known debt in a phase scope crosses that phase gate;
- no temporary migration workflow, rewrite script, compatibility shim or path bridge survives V3-R1;
- V3-R4 is certification only, never cleanup or migration.

## CI execution policy

The earlier CI policy generated excessive, low-value GitHub Actions runs. The v3 policy is therefore deliberately staged:

1. **R1 reconstruction branch:** no automatic workflows. Structural edits must not generate heavy CI or email noise.
2. **Foundation/static gate, when restored:** syntax, JSON/schema validity, repository topology, inventory, engineering-language policy, plan consistency and static API/path checks only.
3. Every restored automatic workflow must use path filters where practical and `concurrency` with `cancel-in-progress: true`.
4. Integration jobs run only for affected surfaces, final pull-request validation, or explicit manual dispatch.
5. Windows literal-font Gate T, Overleaf proxy, PDF/A certification, distribution/CTAN packaging and full multi-engine regression are heavy certification jobs. They do not run on every intermediate commit.
6. No workflow may mutate the repository, commit migration changes or trigger a chain of heavy workflows during reconstruction.
7. Final certification uses the sequence: static gate → affected integration gates → one full candidate suite on the exact candidate SHA.

`main` remains the certified v2 baseline and is not modified merely to optimize v3 development CI. The optimized policy is implemented when v3 workflows are deliberately restored near the end of R1.

## Target repository architecture

```text
.
├── abntexto-ufc.cls
├── abntexto-ufc/
│   ├── core.def
│   ├── fonts.def
│   ├── layout.def
│   ├── modules.def
│   ├── frontmatter.def
│   ├── institutional.def
│   ├── academic-works.def
│   ├── research-projects.def
│   ├── articles.def                 # introduced only in V3-A1
│   ├── objects.def
│   ├── bibliography.def
│   ├── backmatter.def
│   ├── integrations/abntexto.def
│   └── standards/nbr6023-2025.def
├── template/
│   ├── main.tex
│   ├── frontmatter/
│   ├── chapters/
│   ├── backmatter/
│   └── figures/
├── assets/institutional/
├── standards/
├── tests/
│   ├── checks/
│   ├── documents/
│   ├── fixtures/
│   ├── integration/
│   └── smoke/
├── tools/
├── validator/
├── docs/
├── release/
└── .github/workflows/               # restored only after deliberate migration
```

Repository and public distribution layouts intentionally differ. Editable sources live under `template/`; template and Overleaf bundles flatten that directory to archive root.

## V3-R0 — Architecture and deterministic migration contracts

Status: **DONE**.

Contract commit: `f512268661acbb79137cdcdacc94b82fa3dc1746`.

Frozen contracts:

- `release/v3-path-migration.json`;
- `release/v3-api-migration.json`;
- `release/v3-test-migration.json`.

## V3-R1 — Complete repository rebaseline

Status: **ACTIVE**.

R1 closes the complete structural/path/tool/test/workflow/distribution surface before R2.

### Completed structural work through checkpoint `36375e94...`

- workflows disabled on the reconstruction branch;
- repository document source moved under `template/`;
- template frontmatter, chapters, backmatter and figure filenames migrated to English paths;
- `normativa/` moved to `standards/`;
- current runtime integration moved to `abntexto-ufc/integrations/abntexto.def`;
- current NBR 6023 adapter moved to `abntexto-ufc/standards/nbr6023-2025.def`;
- test roots established as `tests/checks/`, `tests/documents/`, `tests/fixtures/`, `tests/integration/` and `tests/smoke/`;
- many test documents, checkers and runners physically moved to semantic roots;
- `template/main.tex` and class module load paths updated for the new physical topology.

### Remaining R1 work — fixed order

1. eliminate obsolete active test/standards terminology (`oracle`, `textual`, `pretextual`, `posttextual`, v2/N-phase names) and update all references atomically;
2. isolate v2/N15/B2R evidence under history namespaces while preserving immutable evidence;
3. migrate all residual active path references and orchestration (`tests/run.py`, checkers, integration scripts, standards JSON references);
4. migrate `Makefile`, `tools/` and validator path assumptions;
5. rebuild distribution staging for repository `template/` versus flattened public bundles;
6. rebuild permanent repository/path and plan-consistency checks from the v3 contracts;
7. restore workflows deliberately using the optimized CI policy above;
8. prepare all repository URLs/metadata for the physical GitHub rename `modelo-latex-ufc` → `abntexto-ufc`;
9. perform the physical repository rename before final v3 certification;
10. execute the R1 exhaustive structural audit and synchronize roadmap/JSON/handoff.

R1 does **not** perform the full runtime API ownership rewrite. That is R2.

### R1 exit gate

- zero obsolete physical paths;
- zero stale path references in the active tree;
- zero project-owned Portuguese technical filenames/directories;
- zero active `oracle`, `textual`, `pretextual`, `posttextual`, v2 or historical N-phase engineering names;
- zero active dependencies on historical evidence paths;
- every active tool/test/restored workflow uses canonical v3 paths;
- `template/main.tex` resolves from its repository location;
- `abntexto-ufc.cls` loads only canonical repository paths;
- public template/Overleaf staging flattens `template/` correctly;
- no generated artifacts or temporary migration scaffolding are tracked;
- permanent repository/path and plan-consistency audits pass;
- optimized CI triggers are installed without heavy automatic reconstruction runs;
- roadmap, machine roadmap and handoff are synchronized.

Only then may R1 become DONE and R2 become ACTIVE.

## V3-R2 — English-only canonical runtime

Status: **BLOCKED by V3-R1**.

Authority: `release/v3-api-migration.json`.

R2 rewrites runtime ownership directly into English: setup keys/values, public commands/environments, internal control sequences/state, comments and diagnostics. Portuguese project aliases are removed, forwarding-only `public-api.def` is dismantled after ownership absorption, and `ufctex.cls` is removed. `article` remains reserved for V3-A1.

## V3-R3 — Standards, tests and engineering-language semantic hardening

Status: **BLOCKED by V3-R2**.

Authority: `release/v3-test-migration.json`.

R3 semantically reviews standards and tests, removes obsolete compatibility assumptions, preserves or strengthens regression coverage and enforces the permanent language contract. Validator implementation, UI, diagnostics and technical identifiers are English. Portuguese may appear in validator data only when it is literal academic content/marker text expected inside a Brazilian academic PDF.

## V3-R4 — Certification only

Status: **BLOCKED by V3-R3**.

Certify the already-clean result on Linux/Windows, applicable TeX engines, Windows literal Times New Roman/Arial Gate T, PDF/A-2b technical target, template/Overleaf/CTAN bundles, deterministic distribution and independent clean builds. R4 cannot absorb migration or cleanup debt.

## V3-R5 and later phases

R5 freezes the certified foundation and migration/user/maintainer documentation. Article work resumes only afterward:

- V3-A1 — scientific article runtime architecture;
- V3-A2 — article deep evidence;
- V3-H1 — post-article hardening;
- V3-RC — release candidate;
- V3-FINAL — exact-head release decision;
- V3-CLEANUP — post-release branch/history cleanup.

N15-B2A remains authoritative scientific input for article requirements; old competing B2B implementations are not merged wholesale.

## Release guardrails

- never claim official/homologated UFC status;
- public bundles exclude the UFC institutional mark and proprietary Microsoft fonts unless policy explicitly changes;
- literal Times New Roman/Arial identity is certified only by Windows Gate T;
- portable fallback does not prove literal font identity;
- PDF/A-2b is the project's technical target satisfying the broader UFC PDF/A requirement;
- no tag/release from an uncertified head;
- historical Git tags/releases remain immutable evidence.

## Immediate action

Continue V3-R1 on `refactor/v3-r1-rebaseline` with workflows disabled. The next implementation block is the atomic cleanup of obsolete active test/standards terminology and its references; no heavy GitHub Actions are restored during that block.
