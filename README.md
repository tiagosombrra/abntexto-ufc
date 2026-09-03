# abntexto-ufc

LaTeX class and reference template for academic works at the Federal University of Ceará (UFC), built on top of `abntexto`.

The canonical project identity is `abntexto-ufc`. The active `main` branch carries the unreleased v3 reconstruction. The last certified public baseline remains v2.1.0 and is recoverable through immutable tags, releases, Git history, and the verified external backup.

## Current v3 status

**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B3 — structural and object API ownership, tracked by issue #238.**

The canonical R2-B3 entry checkpoint is `0650845b922271fc134d20ef2a8c36ebb999ef91` after green closeout PR #243. The certified R1 candidate is `9b1752565ac217c04ffa22a9ef272cdf078af380`. Windows run `33649620219` built the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX `template/main.tex` matrix. Final Linux inspection run `33655108349` passed literal institutional text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b for all four artifacts. No runtime/API, normative semantics or proof-state change was required, and no proprietary Microsoft font was redistributed.

See `docs/ROADMAP-V3.0.0.md` for the consolidated roadmap/status table and `docs/HANDOFF-V3.0.0.md` for the exact continuation point.

## Current v3 repository layout

```text
abntexto-ufc.cls
abntexto-ufc/
  core.def
  fonts.def
  layout.def
  modules.def
  frontmatter.def
  institutional.def
  academic-works.def
  research-projects.def
  objects.def
  bibliography.def
  backmatter.def
  integrations/abntexto.def
  standards/nbr6023-2025.def
template/
  main.tex
  frontmatter/
  chapters/
  backmatter/
  figures/
assets/institutional/
standards/
tests/
tools/
validator/
docs/
release/
  ctan/
```

The editable repository example lives under `template/`. Public template and Overleaf bundles flatten the contents of `template/` to the archive root so the user receives `main.tex` at the project root.

## Engineering policy

Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 rebuilt and certified the foundation. R2-A completed the runtime/API ownership inventory, R2-B1 completed direct canonical setup/state migration, and R2-B2 completed direct academic/front-matter rendering ownership. R2-B3 now moves structural/object environments, object APIs, hooks and project-owned object identifiers directly into responsibility-owning modules. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.

Historical implementation evidence is kept by Git history, tags, releases, pull requests, issues, and certified SHAs rather than by archive directories inside the active tree.

See:

- `docs/ARCHITECTURE.md`
- `docs/ENGINEERING-LANGUAGE.md`
- `docs/CTAN-RELEASE.md`
- `docs/ROADMAP-V3.0.0.md`
- `docs/HANDOFF-V3.0.0.md`

## Requirements

Development targets TeX Live 2026 and `abntexto` 1.1 or newer. The class also uses `biblatex`/`biber`; optional modules load their own dependencies only when enabled.

Literal Times New Roman and Arial certification is performed on Windows. Portable environments may use allowed fallback families when strict literal-font mode is not requested. Proprietary Microsoft font files are never distributed by this repository.

## Build

The repository development document is `template/main.tex`.

```bash
make compile
```

## Validation

Use the permanent source-only gate during routine development:

```bash
make static-check
```

`static-check` validates tracked Python, JSON, shell and JavaScript sources, repository/canonical identity, the aggregate normative/validator source contract, object-scope metadata and the reference-guide contract. It does not compile TeX/PDF documents, fetch network resources or generate distribution artifacts, and it fails if its own execution changes the repository status.

The permanent remote fast workflow is `.github/workflows/static-contract.yml`. Its stable workflow/job name is `Static contract`, and it delegates the complete product validation contract to `make static-check` rather than duplicating checks in workflow YAML.

The broader validation entry points remain separate:

```bash
make check
make release-check
```

`check` runs the PR-oriented integration suite and may compile or inspect generated documents. `release-check` includes the release-only integration checks.

R1-BLOCK-7 is DONE: B7-C1 certified `make check` on clean TeX Live 2026 (`PASS=30 FAIL=0 SKIP=0`); B7-C2 permanently established `Linux integration`; and B7-C3 permanently established `Linux release check`, whose first merged-main run `33566835570` closed `PASS=32 FAIL=0 SKIP=0`, including release-only `pdfa` and `profile-pdfa`, with 14-day evidence retention. B7-D audited exactly three permanent workflows, read-only permissions, pinned actions, bounded concurrency, and no temporary executors.

The current `Stable branches` ruleset does not yet require statuses; the recorded recommendation is `Static contract` plus `Linux integration`, while `Linux release check` remains post-merge/manual.

R1-BLOCK-8 is DONE. Windows run `33649620219` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. Final Linux inspection run `33655108349` passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b. `TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. R2-A ownership inventory, R2-B1 setup/state migration and R2-B2 academic/front-matter migration are complete; V3-R2/R2-B3 is active through issue #238. B2 merged through PR #242 at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949` after final `Linux integration` run `33680378846` closed `PASS=30 FAIL=0 SKIP=0`; closeout PR #243 then passed final `30/0/0` integration and produced canonical B3 entry `0650845b922271fc134d20ef2a8c36ebb999ef91`.

The narrow public delivery interface builds the editable template and Overleaf bundles:

```bash
make reference-assets
make public-bundles
```

The complete distribution candidate interface builds all current release artifacts and their checksums:

```bash
make distribution-bundles
```

The current v3 distribution set is:

- `dist/abntexto-ufc-3.0.0.zip` — class/runtime archive;
- `dist/abntexto-ufc-ctan-3.0.0.zip` — CTAN submission candidate;
- `dist/abntexto-ufc-template-3.0.0.zip` — version-rooted editable template;
- `dist/abntexto-ufc-overleaf-3.0.0.zip` — root-flat self-contained Overleaf import;
- `dist/SHA256SUMS` — SHA-256 digests for all four ZIP archives.

The template and Overleaf archives flatten `template/`. Only the Overleaf archive vendors the project-pinned upstream `abntexto.cls`; the class/runtime and CTAN candidates keep `abntexto` as an external dependency. Public distribution disables/excludes the undistributed UFC institutional mark and rejects proprietary Microsoft fonts. The CTAN candidate contains a dedicated English README, package manual source/PDF and minimal example in a browsing-friendly top-level `abntexto-ufc/` directory. See `docs/CTAN-RELEASE.md` for the release checklist and CTAN-specific validation contract.

## Institutional assets

The source repository may contain the UFC coat-of-arms asset for local development and validation. Public bundles must not redistribute institutional marks unless their distribution status has been explicitly cleared. The build must remain usable when the user provides an approved institutional asset locally.

## Standards and certification

The project tracks current applicable UFC and ABNT requirements through the `standards/` evidence model. PDF/A-2b is the project's technical certification target for generated candidate documents; this does not mean UFC specifically requires the PDF/A-2b conformance level.

The project must not be described as an official or UFC-homologated template unless the University explicitly grants that status.

## License

Project code and documentation are distributed under the terms stated in `LICENSE` (LPPL 1.3c or later). Third-party and institutional assets have separate provenance and licensing rules.
