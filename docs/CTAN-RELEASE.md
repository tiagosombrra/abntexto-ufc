# CTAN / GitHub Release Guide — abntexto-ufc 3.0.0

Updated: 2026-09-09

This document defines the repository-controlled publication procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of GitHub or CTAN publication.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — final exact-main recertification** |
| Canonical branch | `main`; resolve candidate SHA dynamically from Git after this control-plane synchronization is merged |
| Publication hardening | **MERGED** via PR #297 |
| Integration anchor | `25c6ab09dc38be9257d2912652074a48886d28f9` |
| Prior Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **SUPERSEDED FOR PUBLICATION** |
| Package id | `abntexto-ufc` |
| CTAN runtime shape | **one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files** |
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

Release 3.0.0 produces exactly these public archives:

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

PR #297 final-head evidence already demonstrated this shape, including manual inspection of the real retained artifact. Final certification must reproduce the same contract on the exact post-sync canonical `main` SHA.

## pkgcheck is a pre-tag gate

Never create `v3.0.0` before the current CTAN `pkgcheck` has accepted or produced explicitly reviewed warnings for the exact package archive intended for publication.

As of 2026-09-09, the currently announced `pkgcheck` version is **4.1.0 (2026-08-05)**. Final certification must confirm the current version rather than treating this number as permanent.

Preserve:

- `pkgcheck --version` output;
- complete `pkgcheck` output;
- SHA-256 of the checked ZIP;
- disposition of every warning.

Fatal/error output blocks the release.

## Final certification and publication sequence

1. merge this control-plane synchronization through protected `main`;
2. resolve the resulting exact canonical `main` SHA;
3. run Static and complete Linux/release contract on **that exact SHA**;
4. run any change-impact-required heavy Windows/font/PDF-A checks;
5. build the three deterministic public archives + `SHA256SUMS` from that exact SHA;
6. validate checksums, ZIP integrity, monolithic-class equivalence and CTAN structural/semantic gate;
7. manually audit the retained canonical CTAN ZIP;
8. run current CTAN `pkgcheck` against that exact `abntexto-ufc-3.0.0.zip`;
9. freeze hashes/evidence; rebuilding publication bytes is then forbidden;
10. create immutable `v3.0.0` pointing to the same certified SHA;
11. create GitHub Release and attach exactly the frozen three ZIPs + `SHA256SUMS`;
12. re-download GitHub Release assets and verify hashes;
13. submit **only `abntexto-ufc-3.0.0.zip`** to CTAN;
14. preserve submission receipt and later acceptance/install evidence;
15. update post-publication documentation/state and close Release only after verification.

Invariant:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
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

Building or validating a candidate is not CTAN acceptance. A successful GitHub Release is not CTAN acceptance. CTAN status is recorded as published only after explicit acceptance/install evidence exists. Any package-content change after final `pkgcheck` requires a new candidate cycle before tagging.
