# abntexto-ufc

LaTeX class and reference template for academic works at the Federal University of Ceará (UFC), built on top of `abntexto`.

The canonical project identity is `abntexto-ufc`. The active `main` branch carries the unreleased v3 reconstruction. The last certified public baseline remains v2.1.0 and is recoverable through immutable tags, releases, Git history, and the verified external backup.

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

Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. During R1 the current runtime API remains unchanged while engineering surfaces are rebaselined; direct runtime/API internationalization belongs to R2.

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

`check` runs the PR-oriented integration suite and may compile or inspect generated documents. `release-check` includes the release-only integration checks. B7-C1 certified `make check` on a clean TeX Live 2026 Linux runner (`PASS=30 FAIL=0 SKIP=0`). B7-C2 then certified the permanent `.github/workflows/linux-integration.yml` workflow through PR #222: its stable `Linux integration` status always evaluates PR scope, skips the expensive TeX step for drafts and a narrow documentation/control-plane-only allowlist, runs full integration for every other or unknown path, cancels superseded PR runs, delegates the heavy gate to `make check`, and forces full integration on `workflow_dispatch`; its first full permanent run also closed `PASS=30 FAIL=0 SKIP=0`. B7-C3 is active and adds the permanent `.github/workflows/linux-release-check.yml` workflow with stable workflow/job name `Linux release check`. It runs after technical changes land on `main` and on manual dispatch, delegates the gate to `make release-check`, ignores documentation/control-plane-only main pushes, cancels superseded release runs, mirrors the repository validation report into the job summary, and retains `artifacts/validation/**` for 14 days. The Linux release mode contains 32 checks, including release-only `pdfa` and `profile-pdfa`; B7-C3 closure still requires the first permanent main run to pass all 32. This Linux evidence does not replace final B8 Windows/literal-font/PDF-A certification.

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
