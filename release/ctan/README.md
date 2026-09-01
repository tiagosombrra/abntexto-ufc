# abntexto-ufc

`abntexto-ufc` is an unofficial, community-maintained LaTeX class for academic works at the Federal University of Ceará (UFC), Brazil. It is built on top of the `abntexto` class and provides UFC-oriented front matter, academic-work profiles, bibliography integration, objects, and related formatting support.

Version: 3.0.0 (development candidate)

Maintainer: Tiago Guimarães Sombra

Repository and issue tracker: https://github.com/tiagosombrra/abntexto-ufc

Upstream dependency: https://ctan.org/pkg/abntexto

## Requirements

- LaTeX2e;
- `abntexto` 1.1 or newer;
- TeX Live 2026 is the current development target;
- `biblatex`/`biber` for bibliography workflows that use them;
- optional features may require additional packages documented by the class/template.

The package does not redistribute proprietary Microsoft font files. It also does not redistribute UFC institutional marks; users who are authorized to use an institutional asset must provide it locally.

## Installation

After installation through a TeX distribution, use:

```tex
\documentclass{abntexto-ufc}
```

For manual installation, place `abntexto-ufc.cls` and the accompanying `abntexto-ufc/` module directory where TeX can find them, and install the external `abntexto` dependency separately.

See `abntexto-ufc.pdf` for the package overview and `abntexto-ufc-example.tex` for a minimal usage example.

## Status

This project is not an official or UFC-homologated template unless the University explicitly grants that status. The class is maintained as a community project and tracks applicable UFC and ABNT requirements through the project's documented evidence model.

## License

This material may be distributed and/or modified under the conditions of the LaTeX Project Public License, version 1.3c or later. See `LICENSE` for the full license text.
