# CTAN / GitHub Release Guide — abntexto-ufc 3.0.1

Updated: 2026-09-12

This document defines the repository-controlled publication procedure for the recovered `abntexto-ufc` 3.0.1 release. It is a maintainer/release guide, not a claim that 3.0.1 has already been published on GitHub or CTAN.

## Current release state

| Fact | State |
|---|---|
| Active phase | **Release — v3.0.1 final corrections** |
| Canonical branch | `main`; resolve the current SHA dynamically from Git |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; evidence only, superseded as final candidate |
| Active correction branch | `release/v3.0.1-canonical-review-corrections` |
| Tracking issue / PR | #304 / #310 — sole active release transport |
| R0 / R1 / R2 / R3 / R4 | DONE — historical accepted implementation/evidence |
| R5 | ACTIVE_CONSOLIDATED_FINALIZATION — fresh complete certification required on PR #310 |
| R6 | PENDING — maintainer acceptance and immutable publication |
| Public `v3.0.0` | historical/superseded; never retarget silently |
| Recovery target | `3.0.1` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |
| Human visual gate | final full canonical TCC plus seven profile pairs; explicit maintainer approval required |
| Final GitHub `v3.0.1` tag/Release | not yet published |
| CTAN upload/acceptance | not yet claimed; explicit evidence required |

The 2026-09-12 pre-publication regression is recorded in `release/v3.0.1-global-regression.json`; document/tool lifecycle is classified in `docs/V3.0.1-DOCUMENT-LIFECYCLE.md`. PR #310 absorbs the bounded approval-page runtime/test correction from superseded PR #311 and must be fully recertified before R6.

Current continuation state is controlled by `AGENTS.md`, `docs/V3-CONTINUATION.md`, `release/v3.0.1-final-corrections.json` and the active lot evidence document. Older recovery documents are historical evidence when those current files do not point to them.

## Publication problems resolved by the v3 contract

The publication contract addresses the following classes of failure:

1. package identity is `abntexto-ufc`, avoiding the deprecated generic `tex` suffix;
2. no UFC logo, coat of arms, institutional mark asset or proprietary Microsoft font is redistributed;
3. the CTAN upload excludes repository engineering infrastructure and remains intentionally small;
4. the CTAN-facing runtime is one generated class file, while the development repository remains modular;
5. the release pipeline requires exact-SHA technical, current `pkgcheck` and human visual acceptance before the final tag;
6. already-public tags are not silently retargeted when recovery is required;
7. the complete user-facing TCC/reference PDF is distinct from the deliberately minimal CTAN example and is generated from sanitized public source.

## Canonical distribution contract

Release 3.0.1 produces exactly these top-level public release assets:

| Asset | Purpose | CTAN upload? |
|---|---|---|
| `abntexto-ufc-3.0.1.zip` | canonical CTAN-grade package with one generated runtime class, concise documentation and minimal example | **YES — only CTAN upload archive** |
| `abntexto-ufc-template-3.0.1.zip` | editable local project; includes complete sanitized source and generated `abntexto-ufc-reference.pdf`; `abntexto` remains external | no |
| `abntexto-ufc-overleaf-3.0.1.zip` | self-contained Overleaf project with pinned `abntexto.cls`, complete sanitized source and generated `abntexto-ufc-reference.pdf` | no |
| `SHA256SUMS` | integrity manifest for the three ZIPs | GitHub Release only |

There is no separate CTAN archive variant.

The template/Overleaf reference PDF is not copied from a developer build. `tools/build-public-bundles.py` first sanitizes the public `main.tex` to `coat-of-arms = false`, materializes the public source/runtime, compiles it under `SOURCE_DATE_EPOCH` and embeds the resulting `abntexto-ufc-reference.pdf`. The distribution gate extracts both bundles, rebuilds their exact public source using the release dependency contract and requires the rebuilt SHA-256 to equal the embedded PDF SHA-256.

The template bundle intentionally does not vendor `abntexto.cls`; release verification supplies the same pinned upstream used during bundle generation. The Overleaf bundle vendors that pinned upstream by design.

## Two intentionally different example roles

The CTAN package and GitHub usage bundles serve different audiences and must not be conflated.

- `abntexto-ufc-example.tex` / `abntexto-ufc-example.pdf` inside the CTAN ZIP are a small isolated compile/documentation example. They keep `coat-of-arms = false` and validate the monolithic package without the repository runtime tree.
- `abntexto-ufc-reference.pdf` inside template/Overleaf is the complete pedagogical TCC rooted in the same public `main.tex` distributed to users. It demonstrates the full structure, normalization guidance and supported resources.

The complete reference PDF is deliberately not added to the CTAN ZIP unless a concrete CTAN packaging requirement later proves that necessary. Convenience alone is not sufficient to enlarge the CTAN archive.

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

The CTAN archive must contain zero `.def` files, no nested project runtime directory, no vendored `abntexto.cls`, no complete `abntexto-ufc-reference.pdf`, no institutional mark assets, no proprietary Microsoft fonts, no repository control-plane/development infrastructure and no generated TeX auxiliaries.

## Monolithic-class and distribution equivalence gates

The release gate requires:

- every tracked project-owned runtime module incorporated exactly once in the CTAN class;
- no project-owned module remains referenced through `\input`;
- no module-level `\ProvidesFile{abntexto-ufc/...}` remains in the generated class;
- no `.def` file is present in the CTAN ZIP;
- generated class compiles the CTAN example with only external `abntexto.cls` available;
- modular runtime directory absent during isolated CTAN compilation;
- public template and Overleaf sources contain exactly one sanitized `coat-of-arms = false` setup and no enabled institutional mark setup;
- each usage bundle contains exactly one `abntexto-ufc-reference.pdf`;
- rebuilding each extracted public project under the deterministic release environment reproduces the embedded reference PDF SHA-256;
- bundle archives remain deterministic and `SHA256SUMS` validates all three ZIPs;
- no institutional mark asset or proprietary Microsoft font appears in any public archive.

R3 development evidence proves this bounded contract. R5 must repeat the complete release contract on the final immutable canonical candidate.

## `pkgcheck` is an executable pre-tag gate

Never create `v3.0.1` before the current CTAN `pkgcheck` has processed the exact canonical archive intended for publication and all warnings have been explicitly classified.

The Linux release gate downloads the current CTAN `pkgcheck` package at execution time and preserves its version, complete output, the SHA-256 of `abntexto-ufc-3.0.1.zip` and an evidence marker tied to the exact source SHA. A nonzero result blocks release; a zero exit status does not silently waive visible warnings.

Any `pkgcheck` result from a superseded candidate is baseline evidence only. R5 must certify the exact final candidate bytes.

## Mandatory human visual gate

R6 cannot be replaced by CI. Before `v3.0.1` is created, the maintainer must review material generated from the exact immutable R5 SHA:

- the complete canonical TCC/reference PDF;
- the PDF and corresponding `.tex` source for all seven supported profiles: undergraduate capstone, specialization capstone, master's thesis, doctoral thesis, research project, anonymized research project and scientific article.

Every final pair must use the pinned release dependency set and pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight. Assistant/development visual inspection is supporting evidence only; explicit maintainer approval closes R6.

## Historical v3.0.0 disposition

A public `v3.0.0` tag/Release already exists for the earlier SHA `05399473827da7cf6b6c8bac36edc7115481773f`.

Recovery policy: do not move that tag, do not treat its assets as recovered 3.0.1 bytes, do not submit its archive to CTAN, preserve auditability, and publish recovered final bytes only as `v3.0.1` after R0–R6 complete.

## Final certification and publication sequence

1. close R3 distribution repair with exact-SHA development evidence;
2. close R4 Web/Lite static-package and real-PDF E2E blockers;
3. ensure the correction PR contains no unresolved release blocker, update control documents to the pre-R5 freeze state, and merge it to canonical `main`;
4. resolve the resulting exact `main` SHA and freeze it as the R5 candidate;
5. run Static, complete Linux Integration, Linux Release Check, current CTAN `pkgcheck`, canonical full-reference checks, seven profile preflight, CLI/Deep, Web/Lite E2E and distribution hash/inventory checks on that exact SHA;
6. freeze the exact three ZIPs plus `SHA256SUMS`; do not rebuild them;
7. perform R6 maintainer visual review on the full canonical TCC and all seven profile pairs from that same SHA;
8. after explicit approval, create immutable `v3.0.1` pointing to the same SHA without an intervening tracked source commit;
9. create GitHub 3.0.1 Release and attach exactly the frozen three ZIPs + `SHA256SUMS`;
10. re-download GitHub Release assets and verify all hashes;
11. submit only the frozen `abntexto-ufc-3.0.1.zip` to CTAN;
12. preserve submission receipt and later acceptance/install evidence;
13. only after publication may `main` advance with post-publication documentation/control receipts and the deferred repository regression program.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or asset rebuild is permitted between final R5 certification/R6 acceptance and tagging/publication.

## Proposed CTAN metadata

```text
Package id: abntexto-ufc
Version: 3.0.1
Author/Maintainer: Tiago Guimarães Sombra
License: LPPL 1.3c or later
Repository: https://github.com/tiagosombrra/abntexto-ufc
Bug tracker: https://github.com/tiagosombrra/abntexto-ufc/issues
Dependency: abntexto >= 1.1
```

Suggested administrative note:

> This submission uses version 3.0.1 as a publication recovery. The package is named `abntexto-ufc`, distributes no UFC logo or other institutional mark, treats `abntexto` as an external dependency, and contains one generated project-owned runtime file (`abntexto-ufc.cls`) with zero project-owned `.def` files. The earlier public GitHub v3.0.0 assets are superseded and are not the bytes submitted to CTAN.

## Evidence discipline

Building or validating a candidate is not CTAN acceptance. A successful GitHub Release is not CTAN acceptance. CTAN status is recorded as published only after explicit acceptance/install evidence exists.

Every material advance updates the affected control documents and machine state in the same work cycle. Failed development checks remain in the lot evidence after successful reruns. Targeted checks never replace R5 complete phase-end regression.
