# abntexto-ufc

`abntexto-ufc` is a LaTeX class for academic works at the Federal University of Ceará (UFC), Brazil. It is based on `abntexto` and provides institutional profiles for undergraduate works, specialization works, dissertations, theses, and research proposals.

Version: 2.1.0

Maintainer: Tiago Sombra (`tiagosombrra`)

## Requirements

Core requirements:

- LaTeX2e;
- `abntexto` 1.1 or newer;
- `babel`, `iftex`, `microtype`, `etoolbox`, `pdfpages`, `ragged2e`;
- `biblatex` with the ABNT style and `biber`;
- pdfLaTeX: `fontenc`, `newtxtext`, `newtxmath`;
- LuaLaTeX/XeLaTeX: `fontspec`, `unicode-math`, TeX Gyre Termes/Heros and a compatible math font.

Optional modules may additionally use `xcolor`, `listings`, `minted`, `algpseudocodex`, `glossaries` and `imakeidx`. The `tabularray` table module requires `tabularray-abnt` dated 2025-08-08 or newer. `minted` also requires its external Python/Pygments toolchain.

TeX Live 2026 is the reference distribution used by the project CI.

## Fonts

UFC documents may use Times New Roman or Arial. Literal Microsoft font files are not distributed by this package.

LuaLaTeX can use locally installed Times New Roman and Arial through `fontspec`. For pdfLaTeX, the project repository provides optional PowerShell helpers that prepare local metrics from Microsoft fonts already installed on Windows; those project-specific helpers are not part of the CTAN archive.

Portable fallback fonts are available when strict literal-font mode is disabled, but they are not presented as literal Times New Roman or Arial.

## Documentation

The CTAN archive is intentionally limited to the installable class surface and essential documentation. It contains:

- the canonical `abntexto-ufc` class and its handwritten runtime modules;
- the normative implementation matrix in `doc/NORMAS.md`;
- a minimal portable example in `doc/abntexto-ufc-example.tex`;
- this README, the changelog, and the LPPL license.

The full editable UFC template, reference document, photographs, validation infrastructure, and platform-specific helper scripts are maintained in the project repository and release bundles, not in the CTAN archive.

The generated project reference PDF is distributed separately from the CTAN archive because it contains the UFC institutional mark.

The deprecated `ufctex` compatibility entry point is retained only in project/template distributions and is not part of the CTAN package.

## License and assets

The `abntexto-ufc` source code and project documentation are subject to the LaTeX Project Public License 1.3c or any later version, as stated in `LICENSE`.

The CTAN archive contains no institutional image assets. The UFC coat of arms is not distributed in the CTAN archive and is not declared to be covered by the LPPL. When `brasao = sim` is enabled, obtain the official mark from the Federal University of Ceará and provide it locally with `brasao-arquivo = {path/to/file}`. The compatibility default is `assets/institutional/ufc-coat-of-arms.png`.

Official visual identity source: https://www.ufc.br/a-universidade/identidade-visual-da-ufc

The pinned `abntexto` class used by the dedicated Overleaf compatibility bundle is upstream public-domain software and is not included in this CTAN package.

## History and provenance

The historical UFC template was developed by Ednardo Moreira Rodrigues and Alan Batista de Oliveira, with institutional reviewers and collaborators recorded in the earlier project sources. That template was historically adapted in part from `ueceTeX2` by Thiago Nascimento. The current V2 architecture was redesigned and is maintained by Tiago Guimarães Sombra. This lineage is LPPL-compatible; the current repository preserves the full Git history and prior releases.

## Release state

Version 2.1.0 completed the normative and visual audits, Gate T, Windows literal-font certification, deterministic distribution preflight, the real Overleaf import smoke test, and the final unrestricted Gate F audit.

The CTAN package id is `abntexto-ufc`. Catalogue availability is reconfirmed immediately before upload.

## Project

Repository: https://github.com/tiagosombrra/modelo-latex-ufc

Issues and source releases are maintained in the repository above.
