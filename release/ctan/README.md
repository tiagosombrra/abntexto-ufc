# abntexto-ufc

Version: 3.0.0
Release date: 2026-09-09
Maintainer: Tiago Guimarães Sombra
License: LaTeX Project Public License 1.3c or later
Repository: https://github.com/tiagosombrra/abntexto-ufc
Bug tracker: https://github.com/tiagosombrra/abntexto-ufc/issues
Upstream dependency: https://ctan.org/pkg/abntexto (version 1.1 or newer)

`abntexto-ufc` is an unofficial, community-maintained LaTeX class for academic works at the Federal University of Ceará (UFC), Brazil. It is built on top of the `abntexto` class and provides UFC-oriented front matter, academic-work profiles, research-project and scientific-article profiles, bibliography integration, objects, and related formatting support.

## Requirements

- LaTeX2e;
- `abntexto` 1.1 or newer;
- `biblatex` and `biber` for bibliography workflows;
- additional LaTeX packages required by optional features selected by the document.

Version 3.0.0 is certified primarily against TeX Live 2026.

## Installation

When installed through a TeX distribution, use:

```tex
\documentclass{abntexto-ufc}
```

For manual installation, keep `abntexto-ufc.cls` together with the accompanying `abntexto-ufc/` module directory in a location visible to TeX. Install the external `abntexto` dependency separately.

See `abntexto-ufc.pdf` for the package manual and `abntexto-ufc-example.tex` / `abntexto-ufc-example.pdf` for a minimal example.

## Institutional marks and fonts

No UFC logo, coat of arms, trademark asset, or other institutional mark is distributed with this package. Users who are authorized to use such an asset must provide it locally.

The package also does not redistribute proprietary Microsoft Arial or Times New Roman font files.

## Status

This project is not an official or UFC-homologated template unless the University explicitly grants that status. It is maintained as a community project and tracks applicable UFC and ABNT requirements through the project's documented evidence model.

## License

This work may be distributed and/or modified under the conditions of the LaTeX Project Public License, version 1.3c or later. See `LICENSE` for the full license text.