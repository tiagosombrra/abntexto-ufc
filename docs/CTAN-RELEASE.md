# CTAN / GitHub Release Guide — abntexto-ufc 3.0.1 Recovery

Updated: 2026-09-10

This document defines the repository-controlled publication procedure for the recovered `abntexto-ufc` 3.0.1 release. It is a maintainer/release guide, not a claim of CTAN publication.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release — 3.0.1 recovery / final exact-main recertification** |
| Canonical branch | `main`; resolve the exact candidate SHA dynamically from Git |
| Recovery work branch | `release/v3.0.1-recovery` — short-lived |
| Publication hardening | merged via PR #297 |
| Post-hardening control synchronization | merged via PR #298 |
| Final pkgcheck/human-gate controls | merged via PR #301 as `395899e1b2336ed268335d68e59e03452880c15e` |
| Post-v3.0.0 runtime correction | PR #302 merged as `6d06d4ed42b2187b1483ea219ee055cfe975ece2` and included in the 3.0.1 candidate |
| Pre-recovery Linux release evidence | run `34419086322`: `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck` PASS |
| Public `v3.0.0` | exists on `05399473827da7cf6b6c8bac36edc7115481773f`; premature/superseded for final publication |
| Recovery target | `3.0.1`; existing `v3.0.0` must not be silently retargeted |
| Package id | `abntexto-ufc` |
| CTAN runtime shape | one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files |
| Human visual gate | seven PDF/`.tex` pairs; explicit maintainer approval required before `v3.0.1` tag |
| Final GitHub `v3.0.1` tag/Release | not yet published |
| CTAN upload/acceptance | not yet claimed; explicit evidence required |

`docs/V3-RELEASE-RECOVERY.md` records the recovery decision. The historical `v3.0.0` GitHub assets are not eligible for recovered final CTAN submission.

## Prior publication problems and v3 resolution

The earlier package/submission work exposed publication problems that v3 explicitly resolves:

1. package identity is `abntexto-ufc`, avoiding the deprecated generic `tex` suffix;
2. no UFC logo, coat of arms, institutional mark asset or proprietary Microsoft font is redistributed;
3. the CTAN upload excludes repository engineering infrastructure and remains intentionally small;
4. the CTAN-facing runtime is one generated class file, while the development repository remains modular;
5. the release pipeline requires exact-SHA technical, `pkgcheck` and human visual acceptance before the final tag;
6. already-public tags are not silently retargeted when recovery is required.

## Canonical distribution contract

Release 3.0.1 produces exactly these public assets:

| Asset | Purpose | CTAN upload? |
|---|---|---|
| `abntexto-ufc-3.0.1.zip` | canonical CTAN-grade package with one generated runtime class + concise documentation + minimal example | **YES — only CTAN upload archive** |
| `abntexto-ufc-template-3.0.1.zip` | editable local project; may preserve modular sources | no |
| `abntexto-ufc-overleaf-3.0.1.zip` | self-contained Overleaf project with pinned `abntexto.cls`; may preserve modular sources | no |
| `SHA256SUMS` | integrity manifest | GitHub Release only |

There is no separate CTAN archive variant.

The workflow and distribution regression must derive the release number from the canonical `Makefile` version using recursion-safe output rather than duplicating literal archive versions where practical.

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

The CTAN archive must contain zero `.def` files, no nested project runtime directory, no vendored `abntexto.cls`, no institutional mark assets, no proprietary Microsoft fonts, no repository control-plane/development infrastructure and no generated TeX auxiliaries.

## Monolithic-class equivalence gate

The release gate requires:

- every tracked project-owned runtime module incorporated exactly once;
- no project-owned module remains referenced through `\input`;
- no module-level `\ProvidesFile{abntexto-ufc/...}` remains in the generated class;
- no `.def` file is present in the CTAN ZIP;
- generated class compiles the CTAN example with only external `abntexto.cls` available;
- modular runtime directory absent during isolated compilation;
- two independent distribution builds produce byte-identical archives.

Historical evidence already demonstrated `1 cls / 0 def` with all 14 tracked runtime modules inlined. Final 3.0.1 certification must reproduce the contract on the exact recovered candidate SHA containing PR #302.

## pkgcheck is an executable pre-tag gate

Never create `v3.0.1` before the current CTAN `pkgcheck` has processed the exact canonical archive intended for publication and all warnings have been explicitly classified.

The Linux release gate downloads the current CTAN `pkgcheck` package at execution time and preserves:

- `pkgcheck --version` output;
- complete `pkgcheck` output;
- SHA-256 of the checked `abntexto-ufc-3.0.1.zip`;
- an explicit evidence marker tied to the exact source SHA.

A nonzero `pkgcheck` result blocks Release. A zero exit status does not silently waive warnings; any warning visible in the retained output must receive an explicit disposition before freeze.

The PASS on pre-recovery SHA `395899e1...` is baseline evidence only because PR #302 and the 3.0.1 recovery change package bytes.

## Mandatory seven-profile human visual gate

Before hashes are frozen and before `v3.0.1` is created, the maintainer must receive the rendered PDF and corresponding `.tex` source for every supported document profile:

1. `undergraduate-capstone`;
2. `specialization-capstone`;
3. `masters-thesis`;
4. `doctoral-thesis`;
5. `research-project`;
6. `anonymized-research-project`;
7. `scientific-article`.

Every final pair must be generated from the same exact 3.0.1 candidate SHA, use the pinned release dependency set, and pass A4, PDF/A-2b, embedded-font and recognized-warning/overflow preflight.

The gate closes only after explicit maintainer approval. Automated regression and assistant visual inspection are supporting evidence, not a substitute for that approval.

## Historical v3.0.0 disposition

A public `v3.0.0` tag/Release already exists for the earlier SHA `05399473827da7cf6b6c8bac36edc7115481773f`.

Recovery policy:

- do not silently move `v3.0.0` to another commit;
- do not treat its existing public assets as final recovered publication bytes;
- do not submit `abntexto-ufc-3.0.0.zip` to CTAN as the recovered final package;
- preserve auditability of that public state;
- publish recovered final bytes under `v3.0.1` only after the complete release sequence passes.

Editing, deleting or visibly marking the historical GitHub Release is a separate explicit publication-state action and does not replace source-tree recovery.

## Final certification and publication sequence

1. complete deterministic metadata/orchestration preflight before another expensive CI cycle;
2. merge the 3.0.1 recovery/version/control changes to canonical `main` only after the combined PR gates pass;
3. resolve the resulting exact canonical `main` SHA;
4. run Static, automatic complete Linux integration and Linux release check on that exact SHA;
5. run any change-impact-required heavy Windows/font/PDF-A checks;
6. build the three deterministic 3.0.1 public archives + `SHA256SUMS` from that exact SHA;
7. validate checksums, ZIP integrity, monolithic-class equivalence and CTAN structural/semantic gates;
8. physically audit the retained canonical CTAN ZIP;
9. require current CTAN `pkgcheck` evidence for those exact bytes and classify every warning;
10. regenerate all seven exact-candidate PDF/`.tex` review pairs and obtain explicit maintainer approval;
11. freeze hashes/evidence; rebuilding publication bytes is then forbidden;
12. create immutable `v3.0.1` pointing to the same certified and visually approved SHA;
13. create GitHub 3.0.1 Release and attach exactly the frozen three ZIPs + `SHA256SUMS`;
14. re-download GitHub Release assets and verify hashes;
15. submit only `abntexto-ufc-3.0.1.zip` to CTAN;
16. preserve submission receipt and later acceptance/install evidence;
17. update post-publication documentation/state and close Release only after verification.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

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

Building or validating a candidate is not CTAN acceptance. A successful GitHub Release is not CTAN acceptance. CTAN status is recorded as published only after explicit acceptance/install evidence exists. Any tracked change after final acceptance requires a new exact-candidate cycle before tagging.

Every **material advance** updates affected control documents and machine state. Deterministic release errors must be caught before expensive CI where practical. Targeted checks never replace the mandatory **phase-end regression**.
