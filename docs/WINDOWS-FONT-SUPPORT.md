# Windows literal-font support tools

Status: **KEEP — manual maintainer support**

The following scripts are intentionally retained:

- `tools/prepare-windows-fonts.ps1`;
- `tools/convert-encoding-to-unicode.ps1`;
- `tools/convert-unicode-encoding-to-glyphs.ps1`.

They form one manual Windows preparation pipeline. `prepare-windows-fonts.ps1` calls both encoding-conversion scripts and builds local T1/TS1 metrics, virtual fonts, maps and font-definition files for Times New Roman and Arial without redistributing Microsoft font binaries.

## Boundary

These scripts are **not** part of the normal Linux CI or public distribution build. They prepare a maintainer's local Windows TeX environment so the existing strict font/PDF-A proof can exercise literal Microsoft fonts where legally installed.

The certification consumers remain:

- `tests/integration/layout/font-poc.sh`;
- `tests/integration/layout/windows-font-pdfa.sh`;
- shared embedding/PDF-A checks.

No Microsoft font file is tracked or distributed by this repository.

## Maintenance rule

Do not delete one of these three scripts independently. If the Windows literal-font route is retired in the future, retire the three-script preparation pipeline and its dedicated certification path together through a separate regression-tested change.
