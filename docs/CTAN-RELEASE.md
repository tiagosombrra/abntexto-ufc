# CTAN Release Candidate Guide

Updated: 2026-09-09

This document defines the repository-controlled CTAN/GitHub release procedure for `abntexto-ufc` 3.0.0. It is a maintainer/release guide, not a claim of CTAN acceptance.

## Package identity

- CTAN package name: `abntexto-ufc`.
- Project repository: `https://github.com/tiagosombrra/abntexto-ufc`.
- Release target: `3.0.0`.
- License: LaTeX Project Public License 1.3c or later.
- Upstream dependency: `abntexto` 1.1 or newer.
- Status: unofficial, community-maintained UFC-oriented class.
- Current roadmap phase: **Release**.
- Final Certification is closed on candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9`; PR #289 merged to `main` as `e34037f3241aab013b80645b338f38954e02bcda`.
- Release phase-end candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` is **accepted**: Static `34303586782`, complete Linux `34303586778`, Linux release check `34303586773` with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.
- Actual CTAN upload remains a separate explicit Release action and must never be reported as acceptance before a receipt/acceptance exists.

## Certified retained candidate assets

Publication archives must come from retained Actions artifact ID `10086299397` (`abntexto-ufc-v3.0.0-distribution-34303586773`), produced from candidate `75ead435...`. Its GitHub artifact digest is `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222`.

The artifact was independently downloaded without rebuilding. Its archive digest matched GitHub metadata, `SHA256SUMS` passed for all four contained ZIPs, and ZIP integrity checks passed.

| Asset | Accepted SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |

Do not rerun `make distribution-bundles` to manufacture publication bytes after this acceptance point. The build command remains documented below for development/reconstruction only; publication uses the retained artifact above.

## Build the candidate

For development or a future candidate replacement before acceptance:

```bash
make distribution-bundles
```

Expected outputs:

- `dist/abntexto-ufc-3.0.0.zip`
- `dist/abntexto-ufc-ctan-3.0.0.zip`
- `dist/abntexto-ufc-template-3.0.0.zip`
- `dist/abntexto-ufc-overleaf-3.0.0.zip`
- `dist/SHA256SUMS`

`make public-bundles` remains the narrower template/Overleaf interface.

## CTAN candidate layout

The CTAN ZIP contains one top-level directory `abntexto-ufc/` with at least:

```text
abntexto-ufc/
  README.md
  LICENSE
  abntexto-ufc.tex
  abntexto-ufc.pdf
  abntexto-ufc-example.tex
  abntexto-ufc.cls
  abntexto-ufc/
    ... runtime modules ...
```

The CTAN candidate must not contain:

- `abntexto.cls` (external CTAN dependency);
- UFC institutional mark assets;
- Microsoft Times New Roman or Arial font files;
- workflows, tests, validators or reconstruction documentation;
- LaTeX auxiliary files;
- validation evidence or temporary executors.

Only the separate Overleaf bundle may vendor the pinned upstream `abntexto.cls`.

## Release validation

The immutable Release candidate has passed:

- Static contract `34303586782`;
- complete Linux integration `34303586778`;
- `Linux release check` `34303586773`, including `make release-check`, deterministic reference-PDF reproducibility, PDF/A/embedding/Unicode checks and distribution integrity.

The deterministic release-reference-PDF gate is permanent and must remain green for any later candidate replacement.

## Distribution verification

The repository checker is:

```bash
python3 tests/checks/distribution_bundles.py --abntexto /path/to/pinned/abntexto.cls
```

It validates artifact names, SHA-256 metadata, reproducibility, safe paths, package/CTAN layouts, documentation PDF presence, external-upstream semantics and asset exclusions.

Before actual CTAN upload, the certified `abntexto-ufc-ctan-3.0.0.zip` must additionally be checked with the **current** CTAN `pkgcheck`; do not freeze an old version into permanent policy.

Current references:

- `https://ctan.org/help/upload-pkg?lang=en`
- `https://ctan.org/help/submit`
- `https://ctan.org/pkg/pkgcheck`

## Submission-form metadata

Before an actual CTAN submission confirm:

- package name `abntexto-ufc`;
- version `3.0.0`;
- author/maintainer and uploader contact;
- concise English summary/description;
- LPPL 1.3c-or-later license;
- repository and issue tracker;
- dependency on `abntexto`;
- appropriate CTAN topics/categories;
- exact certified `abntexto-ufc-ctan-3.0.0.zip` with SHA-256 `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60`.

## Final Release checklist

1. Preserve immutable Release candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` and its accepted phase-end evidence.
2. Land the documentation synchronization and merge PR #293 to canonical `main`.
3. Create `v3.0.0` tag and GitHub Release using the exact retained candidate-produced files; do not rebuild them.
4. Verify every published GitHub asset hash against the accepted checksums in this document.
5. Extract the retained CTAN candidate and run the current CTAN `pkgcheck`.
6. Confirm README/manual/example version, canonical v3 API, dependency metadata and distribution exclusions.
7. Perform an actual CTAN upload only as an explicit action when required uploader metadata/channel is available; preserve submission and later acceptance evidence.
8. Update roadmap, handoff, release readiness and machine state after every **material advance**.
9. Perform final Release verification before marking the Release phase CLOSED. The accepted immutable **phase-end regression** remains the evidence anchor; publication verification is an additional closeout obligation.

Building or validating a candidate is not CTAN acceptance.
