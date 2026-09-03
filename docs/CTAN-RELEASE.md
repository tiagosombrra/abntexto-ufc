# CTAN Release Candidate Guide

This document describes how `abntexto-ufc` prepares and validates a CTAN submission candidate. It is a maintainer/release guide, not a claim that a given version has already been accepted by CTAN.

## Package identity

- CTAN package name: `abntexto-ufc`.
- Project repository: `https://github.com/tiagosombrra/abntexto-ufc`.
- Current development target: `3.0.0`.
- License: LaTeX Project Public License 1.3c or later.
- Upstream dependency: `abntexto` 1.1 or newer (`https://ctan.org/pkg/abntexto`).
- Status: unofficial, community-maintained UFC-oriented class. Do not describe it as official or UFC-homologated unless the University explicitly grants that status.
- Development gate: V3-R2 runtime/API migration is complete through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its canonical closeout baseline is `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A/#250, R3-B1/#252 and R3-B2/#253 are complete; B2 merged through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` with Linux `33768911126` = `PASS=31 FAIL=0 SKIP=0` and 113/113 `automatic-partial` rule contributions. R3-B3/#254 is complete through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`; its PR Linux gate passed `PASS=31 FAIL=0 SKIP=0` and post-merge release run `33794112546` passed `PASS=33 FAIL=0 SKIP=0`. R3-B4/#255 is active and B5 remains required before R4. A v3.0.0 CTAN upload must not be performed during R3: publication remains a later explicit action after R3 hardening, R4 certification, and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.

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

`docs/ctan-example.tex` is the live source used to stage `abntexto-ufc-example.tex` in the CTAN candidate. It must use the canonical v3 setup surface; it is not historical documentation. The public-bundle producer must likewise stage `coat-of-arms = false` from canonical `coat-of-arms = true` when constructing redistributable template/Overleaf archives and must not depend on removed v2 `brasao = sim/nao` setup vocabulary.

A version mismatch among `Makefile`, `abntexto-ufc.cls`, the CTAN README, and the manual fails closed.

## Linux release validation

Before building or submitting a release candidate, run the coordinated repository release gate:

```bash
make release-check
```

B7-C3 established and certified the permanent `.github/workflows/linux-release-check.yml` workflow, named `Linux release check`. It runs the repository-owned `make release-check` entry point after technical changes land on `main` and on manual dispatch, publishes `artifacts/validation/validation-report.md` in the Actions job summary, and retains `artifacts/validation/**` as short-lived engineering evidence for 14 days. PR #225 merged at `d7327db7efd5cc1e0ff9255195bcb9767d853d3e`; the first permanent merged-main release run `33566835570` passed all 32 checks (`PASS=32 FAIL=0 SKIP=0`), including release-only `pdfa` and `profile-pdfa`. This Linux evidence is not final B8 Windows/literal-font/PDF-A certification and is not CTAN acceptance.

R1-BLOCK-7 and R1-BLOCK-8 are complete. B7-D confirmed the permanent workflow inventory and recorded `Static contract` plus `Linux integration` as the recommended required PR checks; `Linux release check` remains post-merge/manual. B8 certified complete candidate `9b1752565ac217c04ffa22a9ef272cdf078af380`: Windows run `33649620219` passed Times New Roman/Arial × pdfLaTeX/LuaLaTeX, and final Linux inspection run `33655108349` passed literal text-family identity, expected math-font policy, Unicode extraction, embedding and PDF/A-2b. This engineering certification is not CTAN acceptance. CTAN packaging and current `pkgcheck` validation remain separate release procedures below. Validation/B8 evidence is not a distribution artifact and must not be inserted into public bundles.

After R2-B2 merged at `8e3e0f2a165e488a00f08a0031ba6fb4a01f9949`, merged-main `Linux release check` run `33687588772` passed `PASS=32 FAIL=0 SKIP=0`. During the subsequent B2→B3 closeout, targeted release-source audit run `33696155771`, job `100465339990`, compiled the live CTAN example and manual, validated deterministic public and complete distribution bundles, verified safe paths and institutional/proprietary asset exclusions, scanned for stale v2 setup tokens, removed downloaded reference photographs and the temporary workflow, and passed `git diff --check` plus `make static-check`. This additional audit is engineering evidence for the active release path; it is not CTAN submission or acceptance.

## Automated validation

The repository checker is:

```bash
python3 tests/checks/distribution_bundles.py --abntexto /path/to/pinned/abntexto.cls
```

It validates the complete five-artifact set, SHA-256 metadata, reproducibility, safe paths, expected class and CTAN layouts, CTAN README metadata, documentation PDF presence, external `abntexto` semantics, and asset exclusions.

The public-bundle checker additionally verifies that redistributed `main.tex` uses the canonical v3 setup and disables the institutional mark via `coat-of-arms = false`; removed v2 `brasao = sim/nao` forms are rejected.

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
3. Confirm that the intended release commit is still covered by, or has proportionally re-established, the completed Windows/literal-font/PDF-A certification baseline from R1-BLOCK-8.
4. Run `make distribution-bundles`.
5. Verify `SHA256SUMS` and the exact artifact names.
6. Run the repository distribution checker.
7. Extract the CTAN candidate and compile the shipped example with the external `abntexto` dependency.
8. Run the current CTAN `pkgcheck` on the extracted `abntexto-ufc/` directory.
9. Confirm the README/manual/example use the intended canonical release API and version metadata.
10. Confirm that no institutional/proprietary assets, validation evidence, temporary workflows, downloaded reference photographs, or generated auxiliary files are present in public bundles or the release commit.
11. Confirm the GitHub release/tag and user-facing release notes are final when that release stage is reached.
12. Only then perform the explicit CTAN upload and preserve the submission/acceptance receipt in the release record.
