# CTAN Release Candidate Guide

This document describes how `abntexto-ufc` prepares and validates a CTAN submission candidate. It is a maintainer/release guide, not a claim that a given version has already been accepted by CTAN.

## Package identity

- CTAN package name: `abntexto-ufc`.
- Project repository: `https://github.com/tiagosombrra/abntexto-ufc`.
- Current development target: `3.0.0`.
- License: LaTeX Project Public License 1.3c or later.
- Upstream dependency: `abntexto` 1.1 or newer (`https://ctan.org/pkg/abntexto`).
- Status: unofficial, community-maintained UFC-oriented class. Do not describe it as official or UFC-homologated unless the University explicitly grants that status.

## Acceptance benchmark

`abntexto-uece` is used as a practical Brazilian institutional-class benchmark because it was accepted by CTAN in August 2025 and is distributed through TeX Live. Its repository uses a small browsing-friendly package layout with a top-level README, class source, example source/PDF, and package manual source/PDF while keeping `abntexto` as an external dependency.

This benchmark is evidence of a workable packaging pattern, not an acceptance guarantee for `abntexto-ufc`. Current CTAN upload guidance and the current CTAN `pkgcheck` utility remain the authoritative technical references for the submission candidate.

References:

- `https://ctan.org/pkg/abntexto-uece`
- `https://github.com/ElaysonAbreu/abntexto-uece`
- `https://ctan.org/help/upload-pkg?lang=en`
- `https://ctan.org/help/submit`
- `https://ctan.org/pkg/pkgcheck`

## Build the candidate

From a canonical Git checkout:

```bash
make distribution-bundles
```

This generates:

- `dist/abntexto-ufc-3.0.0.zip` — class/runtime archive;
- `dist/abntexto-ufc-ctan-3.0.0.zip` — CTAN submission candidate;
- `dist/abntexto-ufc-template-3.0.0.zip` — editable flattened template;
- `dist/abntexto-ufc-overleaf-3.0.0.zip` — flattened self-contained Overleaf import bundle;
- `dist/SHA256SUMS` — SHA-256 digests for all four ZIP archives.

`make public-bundles` remains the narrower B5-B interface and generates only the template and Overleaf archives.

## CTAN candidate layout

The CTAN ZIP contains one top-level directory named exactly `abntexto-ufc/`. The candidate deliberately uses the browsing-friendly layout recommended for modest packages instead of an internal TDS `tex/`/`doc/` hierarchy.

Required top-level package files include:

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

The candidate must not contain:

- `abntexto.cls`; it is an external CTAN/TeX dependency;
- UFC institutional mark assets;
- Times New Roman or Arial font files from Microsoft;
- repository development surfaces such as workflows, tests, validators or reconstruction documentation;
- generated LaTeX auxiliary files.

Only the separate Overleaf bundle vendors the pinned upstream `abntexto.cls` for self-contained import.

## Package README and manual

`release/ctan/README.md` is the CTAN-facing README. It is intentionally separate from the repository README and includes the package purpose, maintainer/contact channel, version, license, external dependency, platform/font constraints, installation information, and unofficial-project status.

`release/ctan/abntexto-ufc.tex` is the source for the package manual. `tools/build-distribution-bundles.py` builds `abntexto-ufc.pdf` deterministically and inserts the tracked source plus generated PDF into the CTAN candidate.

A version mismatch among `Makefile`, `abntexto-ufc.cls`, the CTAN README, and the manual fails closed.

## Linux release validation

Before building or submitting a release candidate, run the coordinated repository release gate:

```bash
make release-check
```

B7-C3 established and certified the permanent `.github/workflows/linux-release-check.yml` workflow, named `Linux release check`. It runs the repository-owned `make release-check` entry point after technical changes land on `main` and on manual dispatch, publishes `artifacts/validation/validation-report.md` in the Actions job summary, and retains `artifacts/validation/**` as short-lived engineering evidence for 14 days. PR #225 merged at `d7327db7efd5cc1e0ff9255195bcb9767d853d3e`; the first permanent merged-main release run `33566835570` passed all 32 checks (`PASS=32 FAIL=0 SKIP=0`), including release-only `pdfa` and `profile-pdfa`. This Linux evidence is not final B8 Windows/literal-font/PDF-A certification and is not CTAN acceptance.

R1-BLOCK-7 is complete. Its Linux result is an engineering gate, not final release certification. B7-D confirmed the permanent workflow inventory and recorded `Static contract` plus `Linux integration` as the recommended required PR checks; `Linux release check` remains post-merge/manual. R1-BLOCK-8 is now ACTIVE via issue #227 for literal Times New Roman/Arial identity and final Windows/font/PDF-A certification. CTAN packaging and current `pkgcheck` validation remain separate release procedures below. Validation evidence under `artifacts/validation/` is not a distribution artifact and must not be inserted into public bundles.

## Automated validation

The repository checker is:

```bash
python3 tests/checks/distribution_bundles.py --abntexto /path/to/pinned/abntexto.cls
```

It validates the complete five-artifact set, SHA-256 metadata, reproducibility, safe paths, expected class and CTAN layouts, CTAN README metadata, documentation PDF presence, external `abntexto` semantics, and asset exclusions.

The CTAN candidate must also be checked with the current CTAN `pkgcheck` release. B5-C certification used `pkgcheck 4.1.0` against the extracted candidate and received no error or warning diagnostics.

For a release candidate, use the current package from:

`https://ctan.org/pkg/pkgcheck`

Do not freeze an old `pkgcheck` version into permanent release policy without a reason; CTAN may update its automated checks.

## Submission-form metadata

The archive alone does not replace the CTAN upload form. Before an actual submission, confirm at least:

- package name: `abntexto-ufc`;
- version matches the release being submitted;
- author/maintainer information;
- uploader name and current email;
- concise English summary/description;
- LPPL 1.3c-or-later license selection;
- project repository and issue tracker;
- dependency on `abntexto`;
- appropriate CTAN topics/categories;
- archive file is the certified `abntexto-ufc-ctan-<version>.zip` candidate.

The actual CTAN submission is an explicit release action. Building or certifying the candidate must never be recorded as CTAN acceptance.

## Final pre-upload checklist

1. Build from the intended release commit/tag, not from an unrecorded local modification.
2. Run or confirm a successful `make release-check` / `Linux release check` for that candidate commit and preserve its validation evidence.
3. Complete the separate B8 Windows/literal-font/PDF-A certification required for the release candidate.
4. Run `make distribution-bundles`.
5. Verify `SHA256SUMS` and the exact artifact names.
6. Run the repository distribution checker.
7. Extract the CTAN candidate and compile the shipped example with the external `abntexto` dependency.
8. Run the current CTAN `pkgcheck` on the extracted `abntexto-ufc/` directory.
9. Confirm the README/manual version and release metadata.
10. Confirm that no institutional/proprietary assets, validation evidence, or generated auxiliary files are present in public bundles.
11. Confirm the GitHub release/tag and user-facing release notes are final when that release stage is reached.
12. Only then perform the explicit CTAN upload and preserve the submission/acceptance receipt in the release record.
