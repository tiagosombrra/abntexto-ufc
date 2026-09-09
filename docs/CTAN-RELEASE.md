# CTAN Release Candidate Guide

Updated: 2026-09-09

This document defines the repository-controlled CTAN/GitHub release procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of CTAN acceptance.

## Current Release state

| Fact | State |
|---|---|
| Roadmap phase | **Release** |
| Canonical branch | `main`; current SHA is resolved dynamically from Git |
| Release PR #293 | merged |
| Publication-closeout PR #294 | merged |
| Continuation synchronization PR #295 | merged; canonical post-merge Static `34335044265` SUCCESS |
| Release work branch | `release/v3-release`, aligned to canonical `main` after PR #295 |
| Superseded PR #292 | closed; historical evidence only |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — accepted |
| Linux release check | `34303586773` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| GitHub `v3.0.0` Release | not yet published |
| CTAN upload/acceptance | not yet claimed; explicit evidence required |

## Certified retained candidate assets

Publication archives must come from retained Actions artifact ID `10086299397` (`abntexto-ufc-v3.0.0-distribution-34303586773`), produced from candidate `75ead435...`. Its artifact digest is `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`.

The artifact was independently downloaded without rebuilding; inner checksums and ZIP integrity passed.

| Asset | Accepted SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |

Do not rerun the distribution builder to manufacture publication bytes after this acceptance point.

## CTAN candidate requirements

The CTAN ZIP contains one top-level directory `abntexto-ufc/` with the package documentation, class, runtime modules and example. It must not contain proprietary fonts, institutional mark assets, workflows/tests/validators, auxiliary build files, validation evidence, temporary executors, or a vendored external upstream class.

Only the separate Overleaf bundle may vendor the pinned upstream dependency as already covered by the accepted distribution contract.

## Before actual CTAN upload

1. start from the latest `origin/main` and read `docs/V3-CONTINUATION.md`;
2. extract the retained `abntexto-ufc-ctan-3.0.0.zip`;
3. run the **current** CTAN `pkgcheck`;
4. confirm package name/version, maintainer metadata, LPPL license, repository/issue tracker and external dependency declaration;
5. preserve the pkgcheck output;
6. perform an upload only as an explicit publication action;
7. preserve submission receipt and later acceptance evidence before claiming CTAN publication.

Current CTAN references remain `https://ctan.org/help/upload-pkg?lang=en`, `https://ctan.org/help/submit`, and `https://ctan.org/pkg/pkgcheck`.

## Final Release checklist

1. Preserve immutable Release candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` and its accepted **phase-end regression** evidence.
2. Start publication work from the latest `origin/main`; do not resume superseded PR #292.
3. Create `v3.0.0` tag and GitHub Release, attaching the exact retained candidate-produced files.
4. Verify every published GitHub asset hash against the accepted checksums.
5. Run current CTAN `pkgcheck` on the retained CTAN candidate.
6. Perform actual CTAN upload only as an explicit action and preserve evidence.
7. Update roadmap, handoff, readiness, continuation handoff and machine state after every **material advance**.
8. Perform final Release verification before marking Release `CLOSED`.

Building or validating a candidate is not CTAN acceptance.
