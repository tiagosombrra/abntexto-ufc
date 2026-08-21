# ufctex

`ufctex` is a LaTeX class for academic works at the Federal University of Ceará (UFC), Brazil. It is based on `abntexto` and provides institutional profiles for undergraduate works, specialization works, dissertations, theses, and research proposals.

Version: 2.1.0

## Requirements

- LaTeX2e
- `abntexto` 1.1 or newer
- `biblatex` with `biber` for references
- TeX Live 2026 is the reference distribution used by the project CI

Optional modules are loaded only when requested by the document configuration.

## Fonts

UFC documents may use Times New Roman or Arial. Literal Microsoft font files are not distributed by this package.

LuaLaTeX can use locally installed Times New Roman and Arial through `fontspec`. For pdfLaTeX, the package includes PowerShell helpers under `scripts/` that prepare local metrics from Microsoft fonts already installed on Windows.

The class also provides portable fallback fonts when strict literal-font mode is disabled.

## Documentation

The package includes:

- a complete reference document in PDF;
- the source of the reference document;
- the normative implementation matrix in `NORMAS.md`;
- a separate template distribution in the project releases.

## License

This material is subject to the LaTeX Project Public License 1.3c or any later version, as stated in the `LICENSE` file.

The pinned `abntexto` class used only by the dedicated Overleaf compatibility bundle is upstream software and is not included in this CTAN package.

## Project

Repository: https://github.com/tiagosombrra/modelo-latex-ufc

Issues and source releases are maintained in the repository above.
