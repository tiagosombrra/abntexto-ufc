# CTAN / GitHub Release Guide — abntexto-ufc 3.0.0

Updated: 2026-09-09

This document defines the repository-controlled publication procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of GitHub or CTAN publication.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — final human / pkgcheck gates** |
| Canonical branch | `main`; resolve final candidate SHA dynamically after the last control-gate merge |
| Publication hardening | **MERGED** via PR #297 |
| Post-hardening control synchronization | **MERGED** via PR #298, anchor `05399473827da7cf6b6c8bac36edc7115481773f` |
| Package id | `abntexto-ufc` |
| CTAN runtime shape | **one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files** |
| Human visual gate | **seven PDF/`.tex` pairs; explicit maintainer approval required before tag** |
| GitHub `v3.0.0` tag/Release | not yet published |
| CTAN upload/acceptance | not yet claimed; explicit evidence required |

The old Actions artifact `10086299397` must never be published as v3.0.0 final. It remains historical regression evidence only.

## Prior CTAN feedback and v3 resolution

The earlier submission exposed major publication problems that v3 explicitly resolves:

1. package identity is `abntexto-ufc`, avoiding the deprecated generic `tex` suffix;
2. no UFC logo, coat of arms, institutional mark asset or proprietary Microsoft font is redistributed;
3. the CTAN upload excludes repository engineering infrastructure and remains intentionally small;
4. the CTAN-facing runtime is one generated class file, while the development repository remains modular.

This intentionally follows the publication shape of `abntexto-uece` where appropriate: a single project-owned class file rather than a project-owned runtime tree.

## Canonical distribution contract

Release 3.0.0 produces exactly these public assets:

| Asset | Purpose | CTAN upload? |
|---|---|---|
| `abntexto-ufc-3.0.0.zip` | canonical CTAN-grade package with one generated runtime class + concise documentation + minimal example | **YES — only CTAN upload archive** |
| `abntexto-ufc-template-3.0.0.zip` | editable local project; may preserve modular sources | no |
| `abntexto-ufc-overleaf-3.0.0.zip` | self-contained Overleaf project with pinned `abntexto.cls`; may preserve modular sources | no |
| `SHA256SUMS` | integrity manifest | GitHub Release only |

There is no separate `abntexto-ufc-ctan-3.0.0.zip`.

## CTAN archive shape

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

The builder recursively replaces project-owned `\input{abntexto-ufc/...def}` statements with module contents, removes module-level wrappers as needed, preserves canonical load order and compiles the example without the modular runtime directory present.

The CTAN archive must contain **zero `.def` files**, no nested project runtime directory, no vendored `abntexto.cls`, no institutional mark assets, no proprietary Microsoft fonts, no repository control-plane/development infrastructure and no generated TeX auxiliaries.

## Monolithic-class equivalence gate

The release gate requires:

- every tracked project-owned runtime module incorporated exactly once;
- no project-owned module remains referenced through `\input`;
- no module-level `\ProvidesFile{abntexto-ufc/...}` remains in the generated class;
- no `.def` file is present in the CTAN ZIP;
- generated class compiles the CTAN example with only external `abntexto.cls` available;
- modular runtime directory absent during isolated compilation;
- two independent distribution builds produce byte-identical archives.

The post-hardening baseline has already demonstrated `1 cls / 0 def` with all 14 tracked runtime modules inlined. Final certification must reproduce the contract on the exact final candidate SHA.

## pkgcheck is an executable pre-tag gate

Never create `v3.0.0` before the current CTAN `pkgcheck` has processed the exact canonical archive intended for publication and all warnings have been explicitly classified.

As of 2026-09-09, the currently announced `pkgcheck` version is **4.1.0 (2026-08-05)**. The release workflow does not permanently pin that number: it downloads the current CTAN `pkgcheck` package at execution time.

The Linux release gate preserves:

- `pkgcheck --version` output;
- complete `pkgcheck` output;
- SHA-256 of the checked `abntexto-ufc-3.0.0.zip`;
- an explicit evidence marker tied to the exact source SHA.

A nonzero `pkgcheck` result blocks the release. A zero exit status does not silently waive warnings; any warning visible in the retained output must receive an explicit disposition before the freeze.

## Mandatory seven-profile human visual gate

Before hashes are frozen and before `v3.0.0` is created, the maintainer must receive the rendered PDF and corresponding `.tex` source for every supported document profile:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

The six non-article examples derive from the profile-matrix contract. The article uses the canonical scientific-article source. Every final pair must be generated from the same exact candidate SHA, use the pinned release dependency set, and pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight.

The gate closes only after **explicit maintainer approval**. Automated regression and assistant visual inspection are supporting evidence, not a substitute for that approval.

## Final certification and publication sequence

1. merge all remaining release-control changes through protected `main`;
2. resolve the resulting exact canonical `main` SHA;
3. run Static, automatic complete Linux integration and Linux release check on **that exact SHA**;
4. run any change-impact-required heavy Windows/font/PDF-A checks;
5. build the three deterministic public archives + `SHA256SUMS` from that exact SHA;
6. validate checksums, ZIP integrity, monolithic-class equivalence and CTAN structural/semantic gates;
7. physically audit the retained canonical CTAN ZIP;
8. require the current CTAN `pkgcheck` evidence for those exact bytes and classify every warning;
9. regenerate all seven exact-candidate PDF/`.tex` review pairs and obtain explicit maintainer approval;
10. freeze hashes/evidence; rebuilding publication bytes is then forbidden;
11. create immutable `v3.0.0` pointing to the same certified and visually approved SHA;
12. create GitHub Release and attach exactly the frozen three ZIPs + `SHA256SUMS`;
13. re-download GitHub Release assets and verify hashes;
14. submit **only `abntexto-ufc-3.0.0.zip`** to CTAN;
15. preserve submission receipt and later acceptance/install evidence;
16. update post-publication documentation/state and close Release only after verification.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
```

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

Suggested administrative note:

> This submission replaces the previously attempted package identity. The package is now named `abntexto-ufc`, distributes no UFC logo or other institutional mark, treats `abntexto` as an external dependency, and contains one generated project-owned runtime file (`abntexto-ufc.cls`) with zero project-owned `.def` files.

## Evidence discipline

Building or validating a candidate is not CTAN acceptance. A successful GitHub Release is not CTAN acceptance. CTAN status is recorded as published only after explicit acceptance/install evidence exists. Any tracked change after final acceptance requires a new exact-candidate cycle before tagging.