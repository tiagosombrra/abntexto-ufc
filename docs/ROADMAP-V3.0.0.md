# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-08-30

## Status

**ACTIVE — V3-R0 planning and architecture reset.**

Certified source baseline:

`main` at `ce659b578b4fc9cc929af4aadc3e613df469ba77`

Active implementation branch:

`refactor/v3-full-internationalization`

The previous experimental branch `refactor/n15-b2r-c-full-english-canonicalization` is superseded and must not be used as an implementation source.

## Why v3

The current v2.x line introduced an additive English API while retaining Portuguese technical identifiers and compatibility wrappers. The new architectural decision is stricter:

- one canonical engineering language: English;
- one canonical public API: English;
- one canonical internal runtime vocabulary: English;
- no Portuguese compatibility API in the v3 runtime;
- no deprecated `ufctex.cls` compatibility entry point;
- no forwarding layer whose only purpose is to preserve the old Portuguese API;
- project-owned paths, scripts, fixtures, diagnostics, comments, and technical documentation use English;
- academic/example content may remain in Portuguese because the template targets UFC academic documents in Brazil;
- official institutional and normative wording may remain in its authoritative language when quoted, displayed, or semantically required.

Removing an already published public API is a breaking change. Therefore this work targets **v3.0.0**, not v2.2.0.

## Non-negotiable language boundary

### Must be English

- repository directory names;
- project-owned filenames;
- LaTeX public commands, environments, setup keys, and technical values;
- LaTeX internal control sequences and state values owned by this project;
- source-code comments;
- `.def`, `.cls`, `.py`, `.sh`, `.ps1`, workflow and Makefile technical comments;
- test names, fixture names, checker names and diagnostics;
- JSON schema/field names owned by this project;
- active engineering documentation;
- CI job and step names owned by this project;
- release tooling and distribution metadata owned by this project.

### May remain in Portuguese

- academic prose rendered in the reference/template document;
- sample author, title, advisor, institution, course and program values when intentionally demonstrating a Portuguese-language UFC document;
- headings that must appear in Portuguese in a Portuguese-language academic document, such as `RESUMO`, `AGRADECIMENTOS`, `REFERÊNCIAS`, and institutional wording;
- bibliography content;
- official names of UFC units, acts, resolutions, guides and Brazilian standards;
- direct normative/institutional wording where translation would alter the source;
- test fixture payload text when Portuguese text itself is the behavior under test.

The language rule applies to **engineering identifiers and explanations**, not to the language of the academic document produced by the template.

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
│   ├── articles.def                 # introduced only in the article phase
│   ├── objects.def
│   ├── bibliography.def
│   ├── backmatter.def
│   ├── integrations/
│   │   └── abntexto.def
│   └── standards/
│       └── nbr6023-2025.def
├── template/
│   ├── main.tex
│   ├── frontmatter/
│   ├── chapters/
│   ├── backmatter/
│   └── figures/
├── assets/
│   └── institutional/
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
└── .github/workflows/
```

### Distribution boundary

The repository is optimized for maintainability. User-facing template and Overleaf bundles may flatten `template/` so that end users still receive an ergonomic project root containing `main.tex`, `frontmatter/`, `chapters/`, `backmatter/`, and `figures/`.

Repository structure and distribution structure are intentionally allowed to differ.

## Architectural principles

1. **Single ownership.** Every public behavior and internal policy has exactly one runtime owner.
2. **No compatibility indirection.** v3 does not preserve Portuguese project API aliases or the deprecated `ufctex` class.
3. **No cosmetic wrappers.** A public command exists because it expresses a supported semantic capability, not to mirror another command.
4. **English-first implementation.** Canonical English identifiers are implemented directly rather than forwarding to Portuguese state.
5. **Content/runtime separation.** Portuguese academic output is data/content, not engineering nomenclature.
6. **Repository/distribution separation.** Maintainable source layout does not force an inconvenient user bundle layout.
7. **Machine-enforced invariants.** Naming, path language, module ownership, stale references, generated artifacts, workflow pinning and release metadata are checked automatically.
8. **Historical evidence is immutable history.** Previous releases and Git history remain evidence; active runtime code must not carry obsolete compatibility architecture merely to represent history.
9. **No phase closes on documentation alone.** Runtime phases require executable evidence and exact-head CI.
10. **No release from an uncertified head.** Final release requires exact-head source, preflight, Gate T and distribution certification.

## Phase plan

### V3-R0 — Architecture and migration contract

Status: **ACTIVE**

Goals:

- freeze `ce659b...` as the certified v2 source baseline;
- define the v3 language boundary;
- define the target repository layout;
- identify obsolete compatibility-only surfaces;
- map all previous N15 unfinished work into the v3 sequence;
- create machine-readable migration inventory and path/API maps;
- ensure no implementation starts from the superseded experimental branch.

Deliverables:

- `docs/ROADMAP-V3.0.0.md`;
- `docs/ARCHITECTURE.md`;
- `docs/ENGINEERING-LANGUAGE.md`;
- `release/v3-roadmap.json`;
- complete old-path → new-path inventory;
- complete old-API → v3 canonical API inventory;
- removal inventory for compatibility-only artifacts.

Exit criteria:

- every tracked path classified as retain / rename / move / remove;
- every project-owned public API identifier classified;
- no unresolved architectural naming decision;
- migration can be executed deterministically from the certified baseline.

### V3-R1 — Physical repository restructuring

Status: **BLOCKED by V3-R0**

Scope:

- move the editable reference project into `template/`;
- rename all project-owned Portuguese paths to English;
- rename `normativa/` to `standards/`;
- rename `tests/normativa/` to `tests/documents/`;
- move low-level test runners into `tests/integration/`;
- remove version prefixes such as `v2-` from active test runner names where the test is not inherently version-specific;
- move upstream integration/adaptation modules into explicit `integrations/` and `standards/` namespaces;
- update every path reference atomically.

Exit criteria:

- zero stale references to moved paths;
- repository structure checker passes;
- distribution staging still reconstructs the intended end-user bundle layout;
- no generated artifacts are tracked.

### V3-R2 — Canonical English runtime

Status: **BLOCKED by V3-R1**

Scope:

- make English setup keys direct runtime owners;
- make canonical English values direct internal state values;
- make English commands/environments direct implementations;
- rename project-owned internal control sequences to English;
- convert project-owned comments and technical diagnostics to English;
- remove `abntexto-ufc/public-api.def` as a forwarding-only layer after its canonical responsibilities are moved to owning modules;
- remove Portuguese public API commands, keys, values and environments;
- remove `ufctex.cls`;
- remove compatibility-only PT↔EN equivalence fixtures/checkers.

Important boundary:

`abntexto` upstream commands are not renamed by this project. Upstream integration code may legitimately reference upstream identifiers. Only project-owned identifiers are subject to the v3 English rule.

Exit criteria:

- one public project API only;
- zero project-owned Portuguese API identifiers in active runtime;
- zero Portuguese project-owned internal identifiers;
- no compatibility forwarding layer;
- all supported document profiles compile through the canonical API.

### V3-R3 — Engineering-language enforcement

Status: **BLOCKED by V3-R2**

Scope:

- translate all project-owned source comments to English;
- translate technical shell/Python/LaTeX diagnostics to English;
- translate CI step/job labels owned by the project;
- translate active engineering documentation to English;
- keep academic example content in Portuguese;
- create a repository language checker with explicit semantic exemptions rather than a broad Portuguese allowlist.

Exit criteria:

- project-owned paths in Portuguese: 0;
- project-owned technical comments in Portuguese: 0;
- project-owned technical diagnostics in Portuguese: 0;
- canonical examples using removed Portuguese API: 0;
- academic Portuguese content remains valid and intentional.

### V3-R4 — Test architecture and regression reconstruction

Status: **BLOCKED by V3-R3**

Scope:

- reorganize tests by responsibility;
- replace B2R alias/equivalence gates with canonical-v3 API contract gates;
- update fixture names and internal comments;
- preserve all normative/layout/font/PDF-A assertions that remain semantically valid;
- re-establish module ownership audit;
- update repository audit for the new tree;
- update distribution tests for the `template/` source layout;
- update workflow path filters.

Exit criteria:

- all retained v2 behavior that is still part of v3 has regression coverage;
- removed compatibility behavior is not tested as active functionality;
- canonical API inventory is machine-checked;
- test suite has no broken path/version assumptions.

### V3-R5 — Documentation and distribution redesign

Status: **BLOCKED by V3-R4**

Scope:

- rewrite README English-first;
- document Portuguese-language academic output separately from engineering language;
- update CTAN documentation;
- update Overleaf bundle staging;
- update licensing/reference-image documentation filenames and technical prose;
- document migration from v2 for users as a one-time breaking-change guide rather than runtime compatibility code;
- maintain a clean `MIGRATION-V2-TO-V3.md` mapping old API to new API for human users only.

Exit criteria:

- every canonical example uses v3 API;
- distribution bundles contain no removed runtime compatibility layer;
- migration guidance is documentation, not executable legacy code;
- local/Overleaf/CTAN bundle smoke tests pass.

### V3-A1 — Scientific article runtime architecture

Status: **BLOCKED by V3-R5**

This supersedes the implementation stage previously called N15-B2B.

Source authority remains the already reviewed article contract from N15-B2A. The runtime must be reimplemented against the new v3 architecture rather than merging either old competing B2B PR wholesale.

Scope:

- add `articles.def` with canonical English API/state only;
- preserve module ownership boundaries;
- implement required article metadata semantically;
- avoid compatibility aliases;
- keep target-journal instructions as an explicit boundary.

Exit criteria:

- all mandatory article runtime predicates implemented;
- advisory predicates remain advisory;
- module ownership audit passes;
- article profile compiles under pdfLaTeX and LuaLaTeX.

### V3-A2 — Scientific article deep evidence

Status: **BLOCKED by V3-A1**

This supersedes N15-B2C.

Scope:

- certify all 13 `article.*` predicates at the strongest justified evidence level;
- final-PDF geometry, typography, pagination and structure checks;
- source → predicate → implementation → evidence linkage;
- negative-path tests where practical.

Exit criteria:

- no mandatory article rule remains unimplemented;
- no recommendation is misrepresented as mandatory;
- evidence ledger matches runtime and final PDF.

### V3-H1 — Release hardening

Status: **BLOCKED by V3-A2**

This absorbs the remaining former N15-B3 work.

Scope:

- resolve reference-PDF bit reproducibility issue #18;
- audit obsolete workflows such as `reference-validation.yml` and retain only demonstrably unique value;
- remove stale v2 planning surfaces from active documentation;
- verify licenses and distribution manifests;
- run unrestricted repository audit again;
- confirm no historical compatibility architecture leaked back into v3.

Exit criteria:

- deterministic production build or explicitly documented/justified blocker;
- no stale active workflow/documentation state;
- unrestricted audit has no open release-blocking findings.

### V3-RC — v3.0.0 release candidate

Status: **BLOCKED by V3-H1**

Scope:

- atomically promote version surfaces to 3.0.0;
- generate local/template/Overleaf/CTAN candidates;
- controlled double build for reproducibility;
- verify bundle contents and exclusion rules;
- exact-head source and preflight certification.

Exit criteria:

- candidate artifacts are reproducible as required;
- no version drift;
- no removed compatibility files in bundles;
- all release-candidate checks green on exact head.

### V3-FINAL — Exact-head certification and release decision

Status: **BLOCKED by V3-RC**

Required gates on the exact release head:

- Normative Source Contract;
- repository/source audit;
- LaTeX preflight;
- reference/profile PDF/A checks;
- Gate T / Windows literal fonts;
- Overleaf import proxy;
- Distribution preflight;
- `behind_by=0` before protected merge/tag decision.

Only after all required gates succeed:

- merge using the repository's protected-branch policy;
- certify resulting `main` once;
- create immutable `v3.0.0` tag;
- create GitHub Release;
- prepare/submit the verified CTAN candidate.

### V3-CLEANUP — Post-release repository cleanup

Status: **BLOCKED by V3-FINAL**

Scope:

- delete superseded implementation/audit branches only after the immutable release exists;
- preserve genuinely useful historical records in Git history and concise release notes;
- do not carry active compatibility runtime merely for historical reasons.

## Mapping from the previous plan

| Previous work | v3 treatment |
| --- | --- |
| N0–N14 | certified historical evidence; do not repeat blindly |
| N15-A | historical unrestricted audit input to V3-R0/H1 |
| N15-B1 | source/authority work retained |
| N15-B2A | article normative contract retained as source authority |
| N15-B2R A/B | historical migration evidence; additive compatibility architecture superseded |
| N15-B2B | superseded by V3-A1 |
| N15-B2C | superseded by V3-A2 |
| N15-B3 | absorbed by V3-H1 |
| N15-C | superseded by V3-RC |
| N15-D | superseded by V3-FINAL |

## Continuation protocol

Any future work session must begin by reading, in this order:

1. `docs/ROADMAP-V3.0.0.md`;
2. `release/v3-roadmap.json`;
3. `docs/ARCHITECTURE.md`;
4. `docs/ENGINEERING-LANGUAGE.md`;
5. current Git branch/head and open PR state;
6. the phase-specific contract/ledger for the active phase.

Do not infer the active phase from branch names alone. The machine-readable roadmap is the phase authority; this document is its human-readable counterpart.

Every phase-closing change must update both the human roadmap and the machine-readable roadmap in the same change set.

## Current next action

Finish **V3-R0** by producing the exhaustive tree inventory and migration maps before modifying runtime implementation.
