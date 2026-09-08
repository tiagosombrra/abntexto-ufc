# CTAN Release Candidate Guide

Updated: 2026-09-08  
Status: ACTIVE — V3.0.0 RELEASE EXECUTION

This document defines how `abntexto-ufc` prepares and validates a CTAN submission candidate. It is a maintainer/release guide, not a claim that a given version has already been submitted to or accepted by CTAN.

Every **material advance** in this release procedure must be reflected in the Release execution record, handoff, roadmap and machine state in the same work cycle. The final Release candidate must pass the complete Release **phase-end regression** before tag, GitHub Release or external publication finalization.

## Current Release gate

| Fact | Current state |
|---|---|
| Target | `3.0.0` |
| Active phase | **Release** |
| Canonical `main` / Release base | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch | `release/v3.0.0` |
| Final Certification | accepted on `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` |
| Final complete Linux | `34239890614` — `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Final Linux release check | `34239890548` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Release transition | Static `34249182526` + complete Linux `34249182417` SUCCESS |
| CTAN submission | not yet performed |

## Package identity

- CTAN package name: `abntexto-ufc`.
- Project repository: `https://github.com/tiagosombrra/abntexto-ufc`.
- Version: `3.0.0`.
- License: LaTeX Project Public License 1.3c or later.
- Upstream dependency: `abntexto` 1.1 or newer (`https://ctan.org/pkg/abntexto`).
- Status: unofficial, community-maintained UFC-oriented class. Do not describe it as official or UFC-homologated unless the University explicitly grants that status.

Useful external references:

- `https://ctan.org/help/upload-pkg?lang=en`
- `https://ctan.org/help/submit`
- `https://ctan.org/pkg/pkgcheck`
- `https://ctan.org/pkg/abntexto-uece`

The `abntexto-uece` package remains a practical packaging benchmark only. It is not evidence that `abntexto-ufc` will be accepted.

## Build the candidate

From the intended Release candidate checkout:

```bash
make distribution-bundles
```

This generates:

- `dist/abntexto-ufc-3.0.0.zip` — class/runtime archive;
- `dist/abntexto-ufc-ctan-3.0.0.zip` — CTAN submission candidate;
- `dist/abntexto-ufc-template-3.0.0.zip` — editable flattened template;
- `dist/abntexto-ufc-overleaf-3.0.0.zip` — flattened self-contained Overleaf import bundle;
- `dist/SHA256SUMS` — SHA-256 digests for all four ZIP archives.

`make public-bundles` remains the narrower interface that generates only the template and Overleaf archives.

## CTAN candidate layout

The CTAN ZIP must contain one top-level directory named exactly `abntexto-ufc/`.

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

The CTAN candidate must not contain:

- `abntexto.cls`; it remains an external CTAN/TeX dependency;
- UFC institutional mark assets;
- Times New Roman or Arial font files from Microsoft;
- repository development surfaces such as workflows, tests, validators or reconstruction documentation;
- generated LaTeX auxiliary files;
- temporary release/certification evidence not intended for distribution.

Only the separate Overleaf bundle may vendor the pinned upstream `abntexto.cls` for self-contained import.

## Package README, manual and example

- `release/ctan/README.md` is the CTAN-facing README.
- `release/ctan/abntexto-ufc.tex` is the source for the package manual.
- `docs/ctan-example.tex` is the live source staged as `abntexto-ufc-example.tex`.

The README/manual/example must all use the intended v3 API and version metadata. A version mismatch among `Makefile`, `abntexto-ufc.cls`, CTAN README, manual or generated archive fails closed.

The public-bundle producer must stage `coat-of-arms = false` for redistributable template/Overleaf bundles and must reject removed v2 `brasao = sim/nao` setup vocabulary.

## Repository release validation

Before accepting a Release candidate, run:

```bash
make release-check
```

The permanent workflow is `.github/workflows/linux-release-check.yml` (`Linux release check`). For the final Release candidate, a workflow conclusion alone is insufficient: the required Release scope and predicates must actually execute.

The repository distribution checker is:

```bash
python3 tests/checks/distribution_bundles.py --abntexto /path/to/pinned/abntexto.cls
```

It validates the complete artifact set, SHA-256 metadata, reproducibility, safe paths, expected class/CTAN layouts, CTAN README metadata, documentation PDF presence, external `abntexto` semantics and institutional/proprietary asset exclusions.

The permanent deterministic reference-PDF gate also remains part of release verification:

```bash
make release-reference-reproducibility
```

Final Certification already established the heavy literal-font/Unicode/embedding/PDF-A baseline. Release must preserve or proportionally re-establish that evidence if any relevant technical surface changes.

## Validate the extracted CTAN candidate

After `make distribution-bundles`:

1. verify every digest in `dist/SHA256SUMS`;
2. extract `dist/abntexto-ufc-ctan-3.0.0.zip` into a clean directory;
3. verify the exact top-level layout and excluded assets;
4. supply the external pinned/current-compatible `abntexto.cls` dependency outside the archive;
5. compile the shipped `abntexto-ufc-example.tex` from the extracted package;
6. inspect warnings/errors and generated PDF properties required by the release contract.

The extracted package must not rely on repository-only paths or untracked local files.

## CTAN `pkgcheck`

The candidate should be checked with the current CTAN `pkgcheck` release available at:

`https://ctan.org/pkg/pkgcheck`

Do not freeze an old `pkgcheck` version into permanent policy without a reason. Record the version actually used for the `v3.0.0` candidate and preserve its result in the Release record.

A previous package iteration passed `pkgcheck 4.1.0`; that historical result is not a substitute for checking the final v3.0.0 candidate with the current available release.

## Submission-form metadata

Before an actual CTAN submission, confirm at least:

- package name: `abntexto-ufc`;
- version: `3.0.0`;
- author/maintainer information;
- uploader name and current email;
- concise English summary/description;
- LPPL 1.3c-or-later license selection;
- project repository and issue tracker;
- dependency on `abntexto`;
- appropriate CTAN topics/categories;
- archive file is the accepted `abntexto-ufc-ctan-3.0.0.zip` candidate.

Building or certifying the archive is not CTAN submission or acceptance.

## Final Release checklist

| Order | Check | Required result |
|---:|---|---|
| 1 | Build from the immutable intended Release candidate | exact candidate SHA recorded |
| 2 | Run Static contract | SUCCESS |
| 3 | Run complete Linux integration | required complete scope PASS |
| 4 | Run `make release-check` / `Linux release check` | complete release matrix PASS |
| 5 | Confirm literal-font/Unicode/embedding/PDF-A certification is still applicable | ACCEPTED or proportionally re-established |
| 6 | Run `make distribution-bundles` | all four ZIPs + `SHA256SUMS` produced |
| 7 | Verify `SHA256SUMS`, archive names and reproducibility | PASS |
| 8 | Run repository distribution checker | PASS |
| 9 | Extract CTAN candidate and compile shipped example with external `abntexto` | PASS |
| 10 | Run current CTAN `pkgcheck` when executable | no blocking diagnostics |
| 11 | Confirm README/manual/example/API/version consistency | PASS |
| 12 | Confirm no UFC marks, Microsoft font files, temporary workflows/evidence or auxiliary files are distributed | PASS |
| 13 | Accept Release **phase-end regression** | all required predicates green on one immutable candidate |
| 14 | Create/verify `v3.0.0` tag and GitHub Release only after candidate acceptance | published GitHub assets match accepted checksums |
| 15 | Perform explicit CTAN upload only if/when executing the external publication step | submission/acceptance receipt preserved |
| 16 | Record publication verification and close Release | no unresolved blocker |

## Fail-closed boundaries

- Librarian review item 33 remains an authority gap and is not release scope by default.
- Do not change accepted runtime or normative predicates merely to satisfy packaging.
- Do not redistribute proprietary fonts or UFC institutional marks.
- Do not publish/tag from an intermediate or unrecorded state.
- Do not call a locally valid CTAN archive "accepted" until CTAN itself accepts it.
