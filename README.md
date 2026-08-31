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
```

The editable repository example lives under `template/`. Public template and Overleaf bundles flatten the contents of `template/` to the archive root so the user receives `main.tex` at the project root.

## Engineering policy

Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. During R1 the current runtime API remains unchanged while engineering surfaces are rebaselined; direct runtime/API internationalization belongs to R2.

Historical implementation evidence is kept by Git history, tags, releases, pull requests, issues, and certified SHAs rather than by archive directories inside the active tree.

See:

- `docs/ARCHITECTURE.md`
- `docs/ENGINEERING-LANGUAGE.md`
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

Additional validation and distribution targets are being rebaselined during V3-R1. The roadmap is authoritative while this branch is under reconstruction.

## Institutional assets

The source repository may contain the UFC coat-of-arms asset for local development and validation. Public bundles must not redistribute institutional marks unless their distribution status has been explicitly cleared. The build must remain usable when the user provides an approved institutional asset locally.

## Standards and certification

The project tracks current applicable UFC and ABNT requirements through the `standards/` evidence model. PDF/A-2b is the project's technical certification target for generated candidate documents; this does not mean UFC specifically requires the PDF/A-2b conformance level.

The project must not be described as an official or UFC-homologated template unless the University explicitly grants that status.

## License

Project code and documentation are distributed under the terms stated in `LICENSE` (LPPL 1.3c or later). Third-party and institutional assets have separate provenance and licensing rules.
