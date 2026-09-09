# CTAN / GitHub Release Guide — abntexto-ufc 3.0.0

Updated: 2026-09-09

This document defines the repository-controlled publication procedure and evidence record for `abntexto-ufc` 3.0.0. GitHub publication is claimed only where explicit repository evidence is recorded below; CTAN publication is not claimed until external submission and acceptance/install evidence exists.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — GitHub published; CTAN submission pending** |
| Certified source SHA | `05399473827da7cf6b6c8bac36edc7115481773f` |
| Immutable tag | `v3.0.0` → annotated tag object `7354cf912ffa5abb171128554cabce61392ecd84` → certified source SHA |
| GitHub Release | **PUBLISHED** — [abntexto-ufc 3.0.0](https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0) |
| Release publication time | `2026-09-09T18:14:57Z` |
| Distribution artifact | Actions artifact `10117679639` — `sha256:7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df` |
| Canonical CTAN ZIP | `abntexto-ufc-3.0.0.zip` — `sha256:d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71` |
| CTAN runtime shape | **one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files** |
| `pkgcheck` | **PASS** — 4.1.0, exit 0, 0 warnings, 0 errors/fatals; run `34386932488`, artifact `10118176687` |
| GitHub publication verification | **PASS** — recovery run `34387825056`, evidence artifact `10118391678` |
| CTAN submission | **PENDING — not yet claimed** |
| CTAN acceptance/install | **PENDING — explicit external evidence required** |

The immutable release bytes are frozen. Post-tag documentation commits may move `main`, but they do not change the source or assets identified by `v3.0.0`.

The old Actions artifact `10086299397` remains historical regression evidence only and must never be published as v3.0.0.

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

**PASS on the final publication bytes.** Final certification on `05399473827da7cf6b6c8bac36edc7115481773f` proved:

- all 14 tracked project-owned runtime modules incorporated exactly once;
- no project-owned module remains referenced through `\input`;
- no module-level `\ProvidesFile{abntexto-ufc/...}` remains in the generated class;
- zero `.def` files in the CTAN ZIP;
- isolated example compilation with only the generated class plus external `abntexto.cls`;
- deterministic distribution rebuild and checksum verification;
- no UFC institutional marks or proprietary Microsoft fonts redistributed.

The final distribution artifact is `10117679639` (`sha256:7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df`).

## pkgcheck is a pre-tag gate

**PASS before tag creation.** CTAN `pkgcheck 4.1.0` was run against the exact canonical ZIP with SHA-256 `d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71`.

Evidence: workflow run `34386932488`, artifact `10118176687` (`sha256:e6a4d926d68f68657caca2bab4c1f2ea46cad81bd523c6c55e7f0fa73ea4c4e3`). Result: exit code 0, zero warnings, zero errors/fatals. The only reported diagnostic was informational (`I0002`).

Any future package-content change requires a new candidate/version cycle; the v3.0.0 bytes are frozen.

## Final certification and publication sequence

Completed and evidenced:

1. exact canonical source frozen at `05399473827da7cf6b6c8bac36edc7115481773f`;
2. Static, complete Linux integration and Linux release check passed on that SHA;
3. deterministic three-ZIP distribution + `SHA256SUMS` built and retained as artifact `10117679639`;
4. canonical CTAN ZIP manually audited: one generated class, zero `.def`, isolated compile PASS;
5. CTAN `pkgcheck 4.1.0` passed with zero warnings/errors before tag creation;
6. publication hashes frozen; no rebuild occurred;
7. immutable annotated `v3.0.0` created and verified against the certified SHA;
8. GitHub Release `385743477` created with exactly the frozen assets;
9. draft and published Release assets were re-downloaded and proved byte-identical;
10. GitHub Release published at `2026-09-09T18:14:57Z`.

Pending external CTAN work:

11. submit **only `abntexto-ufc-3.0.0.zip`** to CTAN;
12. preserve the CTAN submission receipt and submitted-file identity;
13. preserve CTAN acceptance/catalog/install evidence;
14. synchronize final post-CTAN state and close Release.

Invariant already satisfied for GitHub publication:

```text
certified source SHA == tagged v3.0.0 SHA == source SHA of published GitHub Release bytes
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
