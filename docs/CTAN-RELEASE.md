# CTAN / GitHub Release Guide — abntexto-ufc 3.0.0

Updated: 2026-09-09

This document defines the repository-controlled publication procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of GitHub or CTAN publication.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — publication hardening** |
| Canonical branch | `main`; resolve current SHA dynamically from Git |
| Previous Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — technically certified, **SUPERSEDED FOR PUBLICATION** |
| Supersession reason | certified package archives contained stale v2/pre-publication README text; CTAN README identified 3.0.0 as a development candidate |
| Current work branch | `release/v3-publication-hardening` |
| Package id | `abntexto-ufc` |
| GitHub `v3.0.0` tag/Release | not yet published |
| CTAN upload/acceptance | not yet claimed; explicit evidence required |

The bytes from retained Actions artifact `10086299397` must not be published as v3.0.0 final. They remain historical regression evidence only.

## Prior CTAN feedback and v3 resolution

The earlier `ufctex` submission exposed three major publication problems that are explicitly addressed by v3:

1. **Deprecated `tex` suffix:** the package id is now `abntexto-ufc`, a purpose-oriented lowercase/hyphenated id aligned with CTAN naming guidance and with the accepted `abntexto-uece` package family.
2. **UFC logo licensing:** no UFC logo, coat of arms, institutional mark asset, or proprietary Microsoft font file is redistributed. Authorized users may provide an institutional asset locally.
3. **Excess package scope:** the CTAN upload is intentionally small. Repository-only engineering infrastructure — workflows, tests, validators, standards evidence, roadmaps, release state and build tooling — is not included in the CTAN archive.

## Canonical distribution contract

Release 3.0.0 produces exactly these public archives:

| Asset | Purpose | CTAN upload? |
|---|---|---|
| `abntexto-ufc-3.0.0.zip` | canonical package: runtime + concise documentation + minimal example | **YES — the only CTAN upload archive** |
| `abntexto-ufc-template-3.0.0.zip` | editable local project | no |
| `abntexto-ufc-overleaf-3.0.0.zip` | self-contained Overleaf project with pinned `abntexto.cls` | no |
| `SHA256SUMS` | release integrity manifest | GitHub Release only |

There is no separate `abntexto-ufc-ctan-3.0.0.zip`: the canonical package archive itself is CTAN-grade. This removes redundant representations of the same package.

## CTAN archive shape

`abntexto-ufc-3.0.0.zip` contains exactly one top-level directory, `abntexto-ufc/`. Its intended surfaces are:

```text
abntexto-ufc/
├── README.md
├── CHANGELOG
├── LICENSE
├── abntexto-ufc.cls
├── abntexto-ufc/
│   └── *.def
├── abntexto-ufc.tex
├── abntexto-ufc.pdf
├── abntexto-ufc-example.tex
└── abntexto-ufc-example.pdf
```

The exact module list below `abntexto-ufc/` is derived from the tracked runtime and may include responsibility subdirectories such as `integrations/` and `standards/`.

The CTAN archive must not contain:

- `abntexto.cls` — `abntexto >= 1.1` remains an external CTAN/TeX Live dependency;
- UFC logos, coats of arms or other institutional mark assets;
- proprietary Arial/Times New Roman files;
- `.github/`, `tests/`, `tools/`, `artifacts/`, repository `release/` state, roadmap documents or CI evidence;
- generated TeX auxiliary files;
- hidden files, empty placeholders, unsafe filenames or CRLF/BOM text files.

The distribution regression fails closed on these conditions.

## CTAN rules encoded by the release gate

The package builder/test enforces the applicable current CTAN upload rules that are machine-checkable:

- ASCII filenames without whitespace or hidden path components;
- one top-level directory named after the package id;
- top-level English UTF-8 README without BOM;
- explicit package version, maintainer, license, repository/bug tracker and dependency metadata;
- PDF documentation included;
- LF-only line endings for text files in the CTAN package;
- no auxiliary/development infrastructure;
- no vendored upstream class in CTAN;
- no institutional marks or proprietary Microsoft fonts;
- no stale `development candidate`, v2-publication or deprecated `ufctex` wording.

The project-local gate complements but does not replace CTAN's own `pkgcheck`.

## pkgcheck is a pre-tag gate

The immutable `v*` tag ruleset makes this ordering mandatory. Never create `v3.0.0` before the current CTAN `pkgcheck` has accepted the exact package archive intended for publication.

As of 2026-09-09, the current announced `pkgcheck` version is **4.1.0 (2026-08-05)**. Do not hard-code that version as a permanent rule: final certification must first confirm the current version published by CTAN and run that version.

Preserve:

- `pkgcheck --version` output;
- complete `pkgcheck` output;
- SHA-256 of the checked ZIP;
- final decision for every warning, if any.

Fatal/error output blocks the release. Warnings must be explicitly reviewed; they are not silently waived.

## Final certification and publication sequence

The required order is:

1. merge publication-hardening changes through the protected `main` branch;
2. resolve the resulting exact canonical `main` SHA;
3. run Static and the complete Linux release contract on **that exact SHA**;
4. run any required Windows/literal-font/PDF-A recertification if runtime or certification-relevant behavior changed;
5. build the three deterministic public archives from that exact SHA;
6. validate `SHA256SUMS`, ZIP integrity and the CTAN structural/semantic gate;
7. run the **current CTAN `pkgcheck`** against `abntexto-ufc-3.0.0.zip`;
8. freeze the package hashes and retained evidence; from this point, rebuilding publication bytes is forbidden;
9. create immutable tag `v3.0.0` pointing to **the same SHA that produced and passed the certified artifacts**;
10. create the GitHub Release and attach exactly the frozen three ZIPs plus `SHA256SUMS`;
11. download the GitHub Release assets and verify their hashes against the frozen manifest;
12. submit **only `abntexto-ufc-3.0.0.zip`** through CTAN's upload mechanism;
13. preserve the CTAN submission receipt and later acceptance/install evidence;
14. only then mark CTAN publication and the Release phase as closed.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

A pull-request head that is later squash-merged is not the final certified/taggable SHA. Final certification therefore runs again on canonical `main` after merge.

## Proposed CTAN form metadata

Use current form fields, with the final contact email already known to CTAN for the maintainer account:

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

> Unofficial, community-maintained LaTeX class built on abntexto for academic works at the Federal University of Ceará (UFC), including academic-work, research-project and scientific-article profiles. The package does not redistribute UFC institutional marks or proprietary Microsoft fonts.

Suggested administrative note:

> This submission replaces the previously attempted `ufctex` package name. The package has been renamed to `abntexto-ufc` to follow current CTAN package-id guidance. No UFC logo or other institutional mark is distributed. `abntexto` is an external dependency and is not vendored in the CTAN archive. The upload contains one top-level `abntexto-ufc/` directory with only runtime files, documentation and a minimal example.

## Evidence discipline

Building or validating a candidate is not CTAN acceptance. A successful GitHub Release is not CTAN acceptance. CTAN status may be recorded as published only after explicit CTAN installation/acceptance evidence exists.

If any package-content file changes after final `pkgcheck`, a new candidate and new hashes are required before tagging. Because CTAN treats documentation as part of the package version, post-freeze edits to shipped documentation are not allowed under the same frozen v3.0.0 bytes.
