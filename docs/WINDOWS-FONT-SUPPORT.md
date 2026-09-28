# Windows literal-font support tools

Status: **KEEP — CI-smoked maintainer support**

The following scripts are intentionally retained:

- `tools/prepare-windows-fonts.ps1`;
- `tools/convert-encoding-to-unicode.ps1`;
- `tools/convert-unicode-encoding-to-glyphs.ps1`.

They form one manual Windows preparation pipeline. `prepare-windows-fonts.ps1` calls both encoding-conversion scripts and builds local T1/TS1 metrics, virtual fonts, maps and font-definition files for Times New Roman and Arial without redistributing Microsoft font binaries.

## Boundary

These scripts remain outside the normal Linux release build and public distribution build. They prepare a Windows TeX environment so the existing strict font/PDF-A proof can exercise literal Microsoft fonts where legally installed. Phase 7 adds a bounded Windows CI smoke around this same pipeline; it does not create a second full release matrix.

The certification consumers remain:

- `tests/integration/layout/font-poc.sh`;
- `tests/integration/layout/windows-font-pdfa.sh`;
- shared embedding/PDF-A checks.

No Microsoft font file is tracked or distributed by this repository.

## Maintenance rule

Do not delete one of these three scripts independently. If the Windows literal-font route is retired in the future, retire the three-script preparation pipeline and its dedicated certification path together through a separate regression-tested change.

## CI smoke boundary

`.github/workflows/windows-smoke.yml` runs only for the Windows/font-portability surfaces it owns, plus manual dispatch.

The Windows job is pinned to Windows Server 2025 and provisions TeX Live 2026 through `zauguin/install-texlive` pinned to commit `6671d0c62046c7e349fe154d5208fe746b07e037` (v4.4.0). The repository's pinned `abntexto` 1.1 source is materialized through `tools/fetch-abntexto.py`. The job then verifies the runner-provided Times New Roman/Arial files, runs `prepare-windows-fonts.ps1`, and executes the existing `font-poc.sh` in compile-only mode. It uploads exactly four strict class PDFs: Times New Roman and Arial under pdfLaTeX and LuaLaTeX.

A dependent Ubuntu job certifies those exact Windows-produced PDFs through `windows-font-pdfa.sh`, which reuses the existing literal-font identity, Unicode extraction, embedding and PDF/A-2b gates.

The workflow never uploads or redistributes the Microsoft font binaries themselves.
