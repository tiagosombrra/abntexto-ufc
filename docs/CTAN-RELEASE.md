# CTAN Release Candidate Guide

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
- Actual CTAN upload remains a separate explicit Release action and must never be reported as acceptance before a receipt/acceptance exists.

## Build the candidate

From the intended Release candidate checkout:

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

Before publication, the immutable Release candidate must pass:

```bash
make release-check
```

The permanent GitHub workflow is `Linux release check`. Release phase-end acceptance also requires Static contract and **complete** Linux integration on the same immutable candidate SHA.

The deterministic release-reference-PDF gate is permanent and must remain green.

## Distribution verification

The repository checker is:

```bash
python3 tests/checks/distribution_bundles.py --abntexto /path/to/pinned/abntexto.cls
```

It validates artifact names, SHA-256 metadata, reproducibility, safe paths, package/CTAN layouts, documentation PDF presence, external-upstream semantics and asset exclusions.

The CTAN candidate must additionally be checked with the **current** CTAN `pkgcheck`; do not freeze an old version into permanent policy.

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
- exact certified `abntexto-ufc-ctan-3.0.0.zip`.

## Final Release checklist

1. Work from the intended immutable Release candidate, not unrecorded local modifications.
2. Confirm successful Static contract, **complete** Linux integration and `Linux release check` on that exact candidate.
3. Confirm the candidate remains covered by accepted Final Certification evidence or proportionally re-establish any affected proof.
4. Run `make distribution-bundles`.
5. Verify `dist/SHA256SUMS` and the four exact ZIP names.
6. Run the repository distribution checker.
7. Extract the CTAN candidate and compile the shipped example with external `abntexto`.
8. Run the current CTAN `pkgcheck`.
9. Confirm README/manual/example version and canonical v3 API.
10. Confirm no institutional/proprietary assets, validation evidence, temporary workflows, downloaded reference photographs or auxiliary files are distributed.
11. Only after Release phase-end acceptance create `v3.0.0` tag and GitHub Release with the certified assets/checksums.
12. Verify the published GitHub assets/checksums.
13. Perform an actual CTAN upload only as an explicit action when the required uploader metadata/channel is available; preserve submission/acceptance evidence.
14. Update roadmap, handoff, release readiness and machine state after every **material advance** and run a final Release **phase-end regression** before closing the phase.

Building or validating a candidate is not CTAN acceptance.
