# abntexto-ufc

Community LaTeX class and reference template for academic works at the Federal University of Ceará (UFC), built on top of `abntexto`.

> **Development status:** v3.0.0 is not released yet. The last public release is **v2.1.0**. The v3 shared academic-work foundation has completed Regression Audit, Core Corrections and Reference PDF Validation. **Scientific Article** is the active development phase and is not yet a released profile.

This project is community maintained. It must not be described as an official or UFC-homologated template unless the University explicitly grants that status.

## Current v3 roadmap

| Phase | Status | Evidence |
|---|---|---|
| Regression Audit | CLOSED | 34-point librarian-review contract reconstructed and regression baseline accepted |
| Core Corrections | CLOSED | Candidate `5f67560a...`; Static `33982156041`; Linux `33982156042`, `PASS=31 FAIL=0 SKIP=0` |
| Reference PDF Validation | CLOSED | Candidate `b64074c...`; 55/55-page visual PASS; Static `33985595790`; Linux `33985595798` |
| Scientific Article | **ACTIVE** | Source-backed 18-rule article contract; runtime/evidence implementation starts from the corrected shared foundation |
| Final Certification | QUEUED | Full profile/engine/literal-font/Unicode/embedding/PDF-A/distribution matrix |
| Release | QUEUED | Release assets, checksums and publication actions |

The consolidated librarian-review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains intentionally fail-closed pending authoritative current NBR 6023:2025 evidence for disputed edge cases.

See `docs/ROADMAP-V3.0.0.md`, `docs/HANDOFF-V3.0.0.md` and `release/v3-roadmap.json` for the current execution state.

## Current profiles

The v3 runtime currently supports:

- `undergraduate-capstone`
- `specialization-capstone`
- `masters-thesis`
- `doctoral-thesis`
- `research-project`
- `anonymized-research-project`

The canonical `scientific-article` profile is the active implementation target and must not be treated as available until its phase closes.

## Repository layout

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

The editable development example lives under `template/`. Public template and Overleaf bundles flatten that directory so users receive `main.tex` at the archive root.

## Requirements

Development targets TeX Live 2026 and `abntexto` 1.1 or newer. The class also uses `biblatex`/`biber`; optional modules load their own dependencies only when enabled.

Literal Times New Roman and Arial certification is performed on Windows. Portable environments may use approved fallback families when strict literal-font mode is not requested. Proprietary Microsoft font files are never distributed by this repository.

## Build the reference document

```bash
make compile
```

The development document is `template/main.tex`.

Optional reference photographs used by the documentation can be fetched separately:

```bash
make reference-assets
```

When those optional licensed assets are absent, the canonical reference document intentionally renders labeled fallback boxes instead of failing the build.

## Validation

Routine source-only validation:

```bash
make static-check
```

Full PR-oriented integration validation:

```bash
make check
```

Release-oriented integration validation:

```bash
make release-check
```

The permanent GitHub Actions workflows are:

- `Static contract`
- `Linux integration`
- `Linux release check`

Every material development advance must keep the execution documentation synchronized. Every roadmap phase ends with a mandatory **phase-end regression** on one immutable candidate SHA; targeted checks never replace that gate.

## Canonical V3 reference PDF

The corrected academic-work reference PDF was rebuilt with TeX Live 2026 from Git-bound source and inspected page by page.

- build source SHA: `da02f17df4d2d0a1568edbbe8bfbbfffb7208966`
- build run: `33983729996`
- pages: 55, A4
- PDF version: 1.7
- visual review: **55/55 PASS, 0 unexplained visual failures**
- phase-end candidate: `b64074c64941895f97fbe0f795ce826c798d17ce`
- phase-end Static: `33985595790` — SUCCESS
- phase-end Linux: `33985595798` — SUCCESS

Detailed evidence is in `docs/V3-REFERENCE-PDF-VALIDATION.md` and `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`.

## Scientific Article development

The active phase is **Scientific Article**. Its source-backed contract contains 18 rules derived from the current article-specific authority set and preserves the distinction between required, optional, recommended and conditional requirements.

Implementation must:

- add one canonical `scientific-article` profile without compatibility aliases;
- reuse shared citation, bibliography, section, summary and object infrastructure rather than fork it;
- add article-specific positive and negative evidence before proof-state promotion;
- preserve recommendations as recommendations rather than converting them into hard failures;
- keep journal-specific submission instructions as an applicability boundary;
- preserve the already validated non-article foundation.

See `docs/ARTICLE-NORMATIVE-CONTRACT.md` and `docs/V3-SCIENTIFIC-ARTICLE.md`.

## Public bundles

Editable template and Overleaf bundles:

```bash
make reference-assets
make public-bundles
```

Complete distribution candidate:

```bash
make distribution-bundles
```

The current v3 distribution layout produces:

- `dist/abntexto-ufc-3.0.0.zip`
- `dist/abntexto-ufc-ctan-3.0.0.zip`
- `dist/abntexto-ufc-template-3.0.0.zip`
- `dist/abntexto-ufc-overleaf-3.0.0.zip`
- `dist/SHA256SUMS`

These are development/release-candidate outputs until the **Release** phase closes. Actual CTAN submission is blocked until that phase.

## Standards and evidence

The repository maintains a machine-readable standards/evidence model under `standards/`. Current cross-cutting work includes, among others, UFC institutional guidance and the applicable ABNT standards tracked by the project, including NBR 14724:2024, NBR 10520:2023, NBR 6023:2025, NBR 6024:2012 and NBR 6028:2021. The scientific-article profile additionally uses NBR 6022:2018 with the UFC article guide and current cross-cutting citation/reference rules.

PDF/A-2b is a project certification target for generated candidates; this does not mean UFC specifically mandates that conformance level.

Reviewer comments are treated as evidence, not automatic normative authority. When current authority is insufficient, the project records the gap and fails closed instead of guessing runtime behavior.

## Migration and project documentation

Useful documents:

- `docs/MIGRATING-TO-V3.md`
- `docs/ARCHITECTURE.md`
- `docs/ROADMAP-V3.0.0.md`
- `docs/HANDOFF-V3.0.0.md`
- `docs/UFC-LIBRARIAN-REVIEW.md`
- `docs/V3-REFERENCE-PDF-VALIDATION.md`
- `docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md`
- `docs/ARTICLE-NORMATIVE-CONTRACT.md`
- `docs/V3-SCIENTIFIC-ARTICLE.md`
- `docs/ENGINEERING-LANGUAGE.md`
- `docs/CTAN-RELEASE.md`

Historical implementation evidence is retained through Git history, immutable tags, GitHub Releases, issues, pull requests and certified SHAs rather than archive directories inside the active tree.

## Institutional assets

The source repository may contain UFC institutional assets for local development and validation. Public bundles must not redistribute institutional marks unless their distribution status has been explicitly cleared. Builds must remain usable when users provide an approved institutional asset locally.

## License

Project code and documentation are distributed under the terms stated in `LICENSE` (LPPL 1.3c or later). Third-party and institutional assets have separate provenance and licensing rules.
