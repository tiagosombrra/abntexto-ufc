# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-08-30

## Checkpoint

**V3-R0 is DONE. V3-R1 is ACTIVE under a clean rebaseline.**

Certified v2 baseline:

`main` `ce659b578b4fc9cc929af4aadc3e613df469ba77`

Clean v3 planning baseline:

`ca2ab12163d16e5eef80c0c8ce9fea543064ab10`

Active implementation branch:

`refactor/v3-r1-rebaseline`

Superseded/frozen implementation branches:

- `refactor/v3-full-internationalization`;
- `refactor/v3-foundation-cleanup`;
- `refactor/n15-b2r-c-full-english-canonicalization`.

Do not copy implementation wholesale from superseded branches. They are evidence only.

## Read first

1. `docs/HANDOFF-V3.0.0.md`;
2. `docs/ROADMAP-V3.0.0.md`;
3. `release/v3-roadmap.json`;
4. `docs/ARCHITECTURE.md`;
5. `docs/ENGINEERING-LANGUAGE.md`;
6. `release/v3-path-migration.json`;
7. `release/v3-api-migration.json`;
8. `release/v3-test-migration.json`;
9. current branch/head and CI state.

Machine phase authority: `release/v3-roadmap.json`.

## Execution rule

No known active-tree debt may cross a phase gate.

For V3-R1 specifically:

- GitHub Actions begin disabled on the reconstruction branch;
- no heavy automatic CI is enabled during structural reconstruction;
- no temporary path-rewrite workflow is allowed to become infrastructure;
- historical files may preserve old names, but active code, tests, tools, workflows, distribution, validator and engineering docs must not depend on them;
- every structural/path/tool/test/workflow/distribution dependency is closed before R2;
- R4 is certification only and is not a future cleanup bucket.

## Frozen architecture

- target version `3.0.0`;
- engineering language English;
- Portuguese academic output allowed;
- official UFC/ABNT wording may remain in its source language;
- no Portuguese project runtime compatibility in v3;
- `ufctex.cls` removed;
- `abntexto-ufc.cls` sole class entry point;
- English API/state directly owns behavior;
- forwarding-only `public-api.def` removed after ownership absorption;
- editable document source under `template/`;
- user/Overleaf bundles flatten `template/`;
- `normativa/` → `standards/`;
- current upstream integration under `abntexto-ufc/integrations/`;
- current standard adapters under `abntexto-ufc/standards/`;
- active tests use semantic names;
- upstream non-English identifiers may remain only at explicit integration boundaries.

## V3-R1 — complete repository rebaseline

R1 is not a partial file move. Before it closes, all of these must be resolved:

1. final physical structure;
2. English project-owned technical paths and filenames;
3. all path references;
4. `template/main.tex`;
5. `abntexto-ufc.cls` module paths;
6. `Makefile`;
7. `tools/`;
8. validator path assumptions;
9. every active GitHub workflow, including `latex-preflight.yml`;
10. test documents, fixtures, runners, checkers and smoke tests;
11. distribution staging;
12. Overleaf flattening;
13. historical evidence isolation;
14. permanent repository/path contract audit;
15. removal of temporary migration scaffolding.

R1 must not intentionally perform the full runtime API semantic rewrite; that belongs to R2.

R1 gate requires:

- zero obsolete physical paths;
- zero stale active-tree path references;
- zero project-owned Portuguese technical paths;
- zero active version/phase-coded technical filenames such as `v2-*` or historical N-phase names;
- zero active dependencies on history namespaces;
- all tools/tests/workflows use canonical v3 paths;
- template build path is coherent;
- distribution and Overleaf layouts are correct;
- no generated artifacts are tracked;
- no temporary migration workflow/script remains;
- permanent structural audit passes;
- human/machine roadmaps and this handoff agree.

## V3-R2 — English-only runtime

Blocked by R1. R2 converts runtime ownership to English directly: setup keys/values, public commands/environments, internal state/control sequences, source diagnostics and comments. Portuguese project aliases are removed, `public-api.def` is dismantled after ownership absorption, and `ufctex.cls` is removed. `article` remains reserved until V3-A1.

## V3-R3 — semantic hardening

Blocked by R2. R3 hardens standards semantics, test architecture and the permanent engineering-language contract. Obsolete PT↔EN compatibility-equivalence tests are removed while functional regression coverage is retained or strengthened.

## V3-R4 — certification only

Blocked by R3. Certify Linux/Windows, applicable TeX engines, Windows literal font Gate T, PDF/A-2b, template/Overleaf/CTAN bundles, distribution inspection, independent builds and reproducibility. Do not move migration work here.

## V3-R5 and article sequence

R5 freezes the certified foundation and migration/user/maintainer documentation. Article work resumes only after R5:

- V3-A1 — article runtime architecture;
- V3-A2 — article evidence;
- V3-H1 — hardening;
- V3-RC — release candidate;
- V3-FINAL — exact-head release decision;
- V3-CLEANUP — post-release cleanup.

N15-B2A remains the authoritative scientific input for article requirements. Do not merge either old B2B implementation wholesale.

## Guardrails

- never claim official/homologated UFC status;
- public bundles exclude the UFC institutional mark and proprietary Microsoft fonts unless policy changes;
- literal Times New Roman/Arial identity is certified only by Windows Gate T;
- portable fallback is not evidence of literal font identity;
- PDF/A-2b is the project's technical target satisfying the broader UFC PDF/A requirement;
- no tag/release from an uncertified head;
- branch cleanup is post-release only;
- historical Git tags/releases are immutable evidence.

## Immediate next action

Continue V3-R1 on `refactor/v3-r1-rebaseline` with Actions disabled. Rebuild the repository structure directly from the frozen path contract in bounded commits. Restore workflows only after each one is migrated to canonical v3 paths; keep heavy automatic triggers disabled until the R1 gate is complete.
