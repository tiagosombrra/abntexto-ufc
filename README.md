# abntexto-ufc

LaTeX class and reference template for academic works at the Federal University of Ceará (UFC), built on top of `abntexto`.

The canonical project identity is `abntexto-ufc`. The active `main` branch carries the unreleased v3 reconstruction. The last certified public baseline remains v2.1.0 and is recoverable through immutable tags, releases, Git history, and the verified external backup.

## Current v3 status

**V3-R1, V3-R2, V3-R3 and V3-R4 are DONE. V3-R5/#272 is TECHNICALLY VALIDATED from exact entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` with certified foundation product `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged; canonical closeout is pending so the future V3-A1 entry SHA is not yet invented.**

R2 closed through B5/PR #249 at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and its control plane was reconciled at `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A classified the remaining foundation gaps; R3-B1 closed front-matter evidence truthfulness through PR #258 at `afb9f16403aafd8752a0aa8b0713f85c41204d1b`. R3-B2/#253 then closed through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea`: Static `33768911131` passed and Linux `33768911126` passed `PASS=31 FAIL=0 SKIP=0` with 113/113 `automatic-partial` rules contributing bounded-positive evidence and zero automation gaps. Post-merge Linux release `33772854355` passed `PASS=33 FAIL=0 SKIP=0`. No normative semantics, proof-state defaults or public runtime API changed. R3-B3/#254 closed through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`: Static `33792280764` passed, Linux `33792280797` / job `100771483526` passed `PASS=31 FAIL=0 SKIP=0`, and post-merge Linux release `33794112546` / job `100777542613` passed `PASS=33 FAIL=0 SKIP=0`. The permanent residual gate now covers 134 LaTeX and 168 behavior-affecting engineering sources (302 total), retained test/check reachability is 147/147 with zero orphaned scripts, and negative paths require positive evidence for the same `rule_id`. R3-B4/#255 closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`: the executable engineering-language contract is green, the permanent residual scope is 305 sources (134 LaTeX + 171 engineering), retained test/check reachability is 148/148 with zero orphans, PR Linux passed `PASS=31 FAIL=0 SKIP=0`, and post-merge Linux release `33816137774` / job `100848593542` passed `PASS=33 FAIL=0 SKIP=0`. R3-B5/#256 entered from the canonical B4->B5 checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`: PR #266 Linux passed `PASS=31 FAIL=0 SKIP=0`, exact-main Static passed, and exact-main release passed `PASS=33 FAIL=0 SKIP=0`. R3-B5 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. R4/#267 then certified exact product `c79f3c73f1d51a30175e8259269504d029442a1c` in run `33855800767`: preflight, Windows strict matrix, Linux literal-font/Unicode/embedding/PDF-A inspection and cleanup all passed. R4 closeout PR #273 merged at `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; V3-R4/#267 is DONE and V3-R5/#272 is ACTIVE from that exact predecessor. The historical R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380` only as historical certification evidence.

See `docs/ROADMAP-V3.0.0.md` for the consolidated roadmap/status table and `docs/HANDOFF-V3.0.0.md` for the exact continuation point.

## Current v3 repository layout

```text
abntexto-ufc.cls
abntexto-ufc/
  core.def
  fonts.def
  layout.def
  modules.def
  frontmatter.def
  institutional.def
  academic-works.def
  research-projects.def
  objects.def
  bibliography.def
  backmatter.def
  integrations/abntexto.def
  standards/nbr6023-2025.def
template/
  main.tex
  frontmatter/
  chapters/
  backmatter/
  figures/
assets/institutional/
standards/
tests/
tools/
validator/
docs/
release/
  ctan/
```

The editable repository example lives under `template/`. Public template and Overleaf bundles flatten the contents of `template/` to the archive root so the user receives `main.tex` at the project root.

## Engineering policy

Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 rebuilt and certified the foundation. R2-A and R2-B1 through R2-B5 are complete. The v3 public/runtime API is directly owned, the forwarding-only layer is absent, `docs/MIGRATING-TO-V3.md` documents the breaking migration, and `tests/checks/v3_api_residual.py` permanently rejects removed project API in its current source scope. R3-A, R3-B1 and R3-B2 are complete; `docs/R3-HARDENING-INVENTORY.md` records the resolved evidence findings and remaining lots. R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 and V3-R3 are complete through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. R4/#267 is DONE. R5/#272 has completed foundation-freeze validation: full release gate `PASS=33 FAIL=0 SKIP=0` in run `33866258865`, and package validation run `33869888601` passed public/distribution bundle reproducibility, checksums and asset exclusions with zero workspace residue. R5 remains open only until its canonical closeout produces the immutable V3-A1/#275 entry; A1 is prepared but blocked and no article runtime work has started.

Historical implementation evidence is kept by Git history, tags, releases, pull requests, issues, and certified SHAs rather than by archive directories inside the active tree.

See:

- `docs/ARCHITECTURE.md`
- `docs/ENGINEERING-LANGUAGE.md`
- `docs/CTAN-RELEASE.md`
- `docs/ROADMAP-V3.0.0.md`
- `docs/HANDOFF-V3.0.0.md`
- `docs/R3-HARDENING-INVENTORY.md`

## Requirements

Development targets TeX Live 2026 and `abntexto` 1.1 or newer. The class also uses `biblatex`/`biber`; optional modules load their own dependencies only when enabled.

Literal Times New Roman and Arial certification is performed on Windows. Portable environments may use allowed fallback families when strict literal-font mode is not requested. Proprietary Microsoft font files are never distributed by this repository.

## Build

The repository development document is `template/main.tex`.

```bash
make compile
```

## Validation

Use the permanent source-only gate during routine development:

```bash
make static-check
```

`static-check` validates tracked Python, JSON, shell and JavaScript sources, repository/canonical identity, the aggregate normative/validator source contract, object-scope metadata and the reference-guide contract. It does not compile TeX/PDF documents, fetch network resources or generate distribution artifacts, and it fails if its own execution changes the repository status.

The permanent remote fast workflow is `.github/workflows/static-contract.yml`. Its stable workflow/job name is `Static contract`, and it delegates the complete product validation contract to `make static-check` rather than duplicating checks in workflow YAML.

The broader validation entry points remain separate:

```bash
make check
make release-check
```

`check` runs the PR-oriented integration suite and may compile or inspect generated documents. `release-check` includes the release-only integration checks.

R1-BLOCK-7 is DONE: B7-C1 certified `make check` on clean TeX Live 2026 (`PASS=30 FAIL=0 SKIP=0`); B7-C2 permanently established `Linux integration`; and B7-C3 permanently established `Linux release check`, whose first merged-main run `33566835570` closed `PASS=32 FAIL=0 SKIP=0`, including release-only `pdfa` and `profile-pdfa`, with 14-day evidence retention. B7-D audited exactly three permanent workflows, read-only permissions, pinned actions, bounded concurrency, and no temporary executors.

The current `Stable branches` ruleset does not yet require statuses; the recorded recommendation is `Static contract` plus `Linux integration`, while `Linux release check` remains post-merge/manual.

R1-BLOCK-8 is DONE. In source workflow run `33649620219`, Windows full-candidate-matrix job `100313006509` passed the complete Times New Roman/Arial × pdfLaTeX/LuaLaTeX candidate matrix. The workflow-level conclusion was failure because its Linux inspection job failed; separate final Linux inspection run `33655108349` / job `100331601354` subsequently passed literal text-family identity, expected independent math-font policy, Unicode extraction, embedding and PDF/A-2b. `TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. R2-A and R2-B1 through R2-B5 are complete. B5 PR #249 merged at `ecd5926760080003148e8b1621dc8d4e4e8c7e5e` and R2 closeout PR #251 established `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`. R3-A/#250, R3-B1/#252 and R3-B2/#253 are complete. B2 merged through PR #260 at `1d9e6373ed674fb7503b968b3e852e4be5fc14ea` after Static `33768911131` and Linux `33768911126` = `PASS=31 FAIL=0 SKIP=0`; R3-B3/#254 is complete through PR #262 at `fbee5bd329f98a389c2880932af40547c8d1674e`; R3-B4/#255 is complete through PR #264; R3-B5/#256 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4/#267 is the active certification stage.

The narrow public delivery interface builds the editable template and Overleaf bundles:

```bash
make reference-assets
make public-bundles
```

The complete distribution candidate interface builds all current release artifacts and their checksums:

```bash
make distribution-bundles
```

The current v3 distribution set is:

- `dist/abntexto-ufc-3.0.0.zip` — class/runtime archive;
- `dist/abntexto-ufc-ctan-3.0.0.zip` — CTAN submission candidate;
- `dist/abntexto-ufc-template-3.0.0.zip` — version-rooted editable template;
- `dist/abntexto-ufc-overleaf-3.0.0.zip` — root-flat self-contained Overleaf import;
- `dist/SHA256SUMS` — SHA-256 digests for all four ZIP archives.

The template and Overleaf archives flatten `template/`. Only the Overleaf archive vendors the project-pinned upstream `abntexto.cls`; the class/runtime and CTAN candidates keep `abntexto` as an external dependency. Public distribution disables/excludes the undistributed UFC institutional mark and rejects proprietary Microsoft fonts. The CTAN candidate contains a dedicated English README, package manual source/PDF and minimal example in a browsing-friendly top-level `abntexto-ufc/` directory. See `docs/CTAN-RELEASE.md` for the release checklist and CTAN-specific validation contract.

## Institutional assets

The source repository may contain the UFC coat-of-arms asset for local development and validation. Public bundles must not redistribute institutional marks unless their distribution status has been explicitly cleared. The build must remain usable when the user provides an approved institutional asset locally.

## Standards and certification

The project tracks current applicable UFC and ABNT requirements through the `standards/` evidence model. PDF/A-2b is the project's technical certification target for generated candidate documents; this does not mean UFC specifically requires the PDF/A-2b conformance level.

The project must not be described as an official or UFC-homologated template unless the University explicitly grants that status.

## License

Project code and documentation are distributed under the terms stated in `LICENSE` (LPPL 1.3c or later). Third-party and institutional assets have separate provenance and licensing rules.
