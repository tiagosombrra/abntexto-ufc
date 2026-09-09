# CTAN / GitHub Release Guide — abntexto-ufc 3.0.0

Updated: 2026-09-09

This document defines the repository-controlled publication procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of GitHub or CTAN publication.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — final human/publication gates** |
| Canonical branch | `main`; resolve current SHA dynamically from Git |
| Post-hardening baseline | `25c6ab09dc38be9257d2912652074a48886d28f9` — complete post-merge engineering evidence |
| Previous candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Package id | `abntexto-ufc` |
| CTAN runtime shape | **one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files** |
| GitHub `v3.0.0` tag/Release | not yet published |
| CTAN upload/acceptance | not yet performed/claimed |
| Human visual gate | **required before tag; pending explicit maintainer approval** |

The publication-hardening PR has already been merged. Exact-main run `34355988612` completed `SCOPE=complete PASS=38 FAIL=0 SKIP=0` and regenerated the distribution successfully from `25c6ab09...`. The final candidate will be the exact `main` SHA after this last control/documentation synchronization is merged and recertified.

## Prior CTAN feedback and v3 resolution

The earlier `ufctex` submission exposed publication problems explicitly addressed by v3:

1. **Deprecated `tex` suffix:** the package id is now `abntexto-ufc`.
2. **UFC logo licensing:** no UFC logo, coat of arms, institutional mark asset or proprietary Microsoft font file is redistributed.
3. **Excess package scope:** repository engineering infrastructure is excluded from the CTAN archive.
4. **Runtime fragmentation:** repository sources stay modular, while the CTAN package exposes one generated class with all project-owned `.def` modules inlined.

This deliberately follows the compact CTAN-facing shape used by `abntexto-uece` where appropriate.

## Canonical distribution contract

Release 3.0.0 produces exactly these public assets:

| Asset | Purpose | CTAN upload? |
|---|---|---|
| `abntexto-ufc-3.0.0.zip` | canonical CTAN-grade package | **YES — only CTAN upload archive** |
| `abntexto-ufc-template-3.0.0.zip` | editable local project | no |
| `abntexto-ufc-overleaf-3.0.0.zip` | self-contained Overleaf project with pinned `abntexto.cls` | no |
| `SHA256SUMS` | integrity manifest | GitHub Release only |

The CTAN ZIP contains exactly:

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

Hard failures include any project `.def` in the CTAN ZIP, nested runtime directory, vendored `abntexto.cls`, UFC mark, proprietary font, auxiliary/development file, unsafe filename, CRLF/BOM text or stale `ufctex`/v2/development-candidate wording.

## Monolithic-class equivalence gate

The generated CTAN class must satisfy all of the following:

- every tracked project-owned runtime `.def` module incorporated exactly once;
- no project module `\input` remains;
- no module-level `\ProvidesFile{abntexto-ufc/...}` remains;
- zero `.def` files in the CTAN ZIP;
- isolated CTAN example compiles with generated class plus external `abntexto.cls` only;
- two distribution builds at the same SHA/epoch are byte-identical.

The current implementation has 14 tracked project runtime modules and the post-hardening baseline passed this gate with all 14 inlined.

## pkgcheck is a pre-tag gate

The current announced CTAN `pkgcheck` is **4.1.0 (2026-08-05)** as of 2026-09-09. The CTAN package catalogue page can lag announcements, so final certification must confirm the current announced version immediately before execution.

Run the current version against the extracted top-level package directory from the **exact canonical ZIP intended for publication**. Preserve:

- `pkgcheck --version` output;
- complete `pkgcheck` output;
- SHA-256 of the checked ZIP;
- final disposition of every warning.

`pkgcheck -d <package-directory>` returns nonzero on errors. Any error blocks release; warnings require explicit review rather than silent waiver.

## Mandatory human visual gate

Before hashes are frozen and before `v3.0.0` is created, show the maintainer the rendered PDF and corresponding `.tex` source for every supported document profile:

1. undergraduate capstone;
2. specialization capstone;
3. master's thesis;
4. doctoral thesis;
5. research project;
6. anonymized research project;
7. scientific article.

The six non-article examples derive from the profile-matrix contract; the article uses the canonical scientific-article source. Each final pair must be generated from the same exact source SHA that will be tagged, use the pinned release dependency set, and pass at minimum A4, PDF/A-2b, embedded-font and recognized-warning/overflow checks.

The gate closes only after an **explicit maintainer approval in the release conversation/workflow evidence**. Automated regression does not imply visual approval.

## Final certification and publication sequence

The required order is:

1. merge all remaining tracked release-control/documentation changes through protected `main`;
2. resolve the resulting exact canonical `main` SHA;
3. run Static and the complete Linux release contract on that exact SHA;
4. decide Windows/literal-font recertification by scope; rerun it if font/engine/certification-relevant runtime changed;
5. generate and physically audit the deterministic three-ZIP distribution + `SHA256SUMS` from that exact SHA;
6. run the current CTAN `pkgcheck` on the exact canonical CTAN package;
7. generate the seven final source/PDF review pairs from that exact SHA and obtain explicit maintainer visual approval;
8. freeze hashes and retained evidence; from this point publication-byte rebuilding is forbidden;
9. create immutable tag `v3.0.0` pointing to the same certified and visually approved SHA;
10. create GitHub Release with exactly the frozen three ZIPs plus `SHA256SUMS`;
11. re-download Release assets and verify their hashes;
12. submit only `abntexto-ufc-3.0.0.zip` through CTAN;
13. preserve submission receipt and later CTAN acceptance/install evidence;
14. only then close Release/publication state.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

If any tracked file changes before tagging — including shipped documentation or release-control documentation — resolve the new candidate SHA and rerun exact-SHA gates as applicable.

## Proposed CTAN metadata

```text
Package id: abntexto-ufc
Version: 3.0.0
Author/Maintainer: Tiago Guimarães Sombra
License: LPPL 1.3c or later
Repository: https://github.com/tiagosombrra/abntexto-ufc
Bug tracker: https://github.com/tiagosombrra/abntexto-ufc/issues
Dependency: abntexto >= 1.1
```

Suggested summary:

> Unofficial, community-maintained LaTeX class built on abntexto for academic works at the Federal University of Ceará (UFC), including academic-work, research-project and scientific-article profiles. The package distributes one generated class file for its runtime and does not redistribute UFC institutional marks or proprietary Microsoft fonts.

Suggested administrative note:

> This submission replaces the previously attempted `ufctex` package name. The package has been renamed to `abntexto-ufc` to follow current CTAN package-id guidance. No UFC logo or other institutional mark is distributed. `abntexto` is an external dependency and is not vendored in the CTAN archive. The upload contains one top-level `abntexto-ufc/` directory, and all project-owned runtime modules are incorporated into the single `abntexto-ufc.cls`; no project-owned `.def` files are distributed.

Building, tagging or submitting a candidate is not CTAN acceptance. CTAN publication may be recorded only after explicit acceptance/install evidence exists.