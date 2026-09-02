# abntexto-ufc v3 Architecture

Updated: 2026-09-02

This document defines the target engineering architecture for `abntexto-ufc` v3.0.0. It governs repository organization and project-owned module/API ownership; it does not create academic formatting requirements.

## Design principles

The v3 tree must be explicit, English-first for engineering surfaces, easy to navigate, free of duplicate ownership, testable, distribution-safe, and free of runtime compatibility layers whose only purpose is preserving removed v2 project API.

The repository is an active product tree, not an archive. Historical evidence belongs to Git commits, tags, releases, issues, pull requests, and certified SHAs. No `history/` museum directories or dormant future-phase ledgers are part of the active architecture.

## Top-level layout

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
.github/
  workflows/static-contract.yml
  workflows/linux-integration.yml
  workflows/linux-release-check.yml
assets/institutional/
standards/
tests/
  static.py
  checks/
  documents/
  fixtures/
  integration/
  smoke/
tools/
validator/
docs/
release/
  ctan/
```

`articles.def` is introduced only when V3-A1 becomes active. It is not pre-staged as a dormant foundation module.

## Runtime ownership

`abntexto-ufc.cls` is the only canonical class entry point. v3 does not ship `ufctex.cls`.

Runtime responsibilities are separated as follows:

- `core.def`: setup keys, document/profile state, shared metadata, common conditionals;
- `fonts.def`: font selection, strict-font policy, engine-specific font resolution;
- `layout.def`: page geometry, section/page-break policy, structural layout primitives;
- `modules.def`: optional feature selection and initialization;
- `frontmatter.def`: front-matter rendering capabilities;
- `institutional.def`: UFC institutional presentation/assets;
- `academic-works.def`: capstone/dissertation/thesis behavior;
- `research-projects.def`: research-project behavior;
- `objects.def`: figures, charts, tables, listings, algorithms, captions, source/note handling;
- `bibliography.def`: citation/reference integration and public bibliography surface;
- `backmatter.def`: appendices, annexes, glossary, index, and back-matter behavior.

A project-owned internal control sequence has one behavior owner. Public commands are implemented directly by the module that owns the behavior; no forwarding-only compatibility layer is part of the final v3 runtime. `public-api.def` is therefore transitional R2 debt and must disappear after direct ownership is absorbed.

## R2 migration sequencing

The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A classified the forwarding surface and direct owners. R2-B1 is complete: canonical setup/state vocabulary is directly owned and all live setup/state consumers use it. R2-B2 is active and migrates academic/front-matter rendering commands plus layout-hook consumers; later lots migrate structural/object APIs, bibliography/back-matter APIs, and finally remove `public-api.def`. Template and test consumers move atomically with each behavior owner.

## Upstream boundaries

`abntexto-ufc/integrations/` contains current adapters to external package/class behavior. These are not legacy compatibility layers. An upstream identifier may remain non-English when it is genuinely owned by the dependency and must be called at an explicit integration boundary, but it must not be re-exported as canonical project API.

`abntexto-ufc/standards/` contains narrow runtime adaptations required for a current technical-standard behavior, such as the current NBR 6023:2025 bibliography adapter.

## Editable template and distribution bundles

The source repository keeps the editable example under `template/`:

```text
template/main.tex
```

Template and Overleaf bundles flatten `template/` so the user receives:

```text
main.tex
frontmatter/
chapters/
backmatter/
figures/
```

Flattening is a distribution staging responsibility; it must not distort the repository architecture. `tools/build-public-bundles.py`, exposed through `make public-bundles`, produces a version-rooted template archive and a root-flat Overleaf import archive. The latter alone vendors the pinned upstream `abntexto.cls`. Public staging excludes the UFC institutional asset and proprietary Microsoft fonts, and `tests/checks/public_bundles.py` proves archive structure, safe paths and reproducibility.

`tools/build-distribution-bundles.py`, exposed through `make distribution-bundles`, composes that public delivery with a class/runtime archive, a CTAN submission candidate, and `SHA256SUMS`. The class/runtime archive contains only the current class, runtime modules, project README and license under a versioned root. It keeps `abntexto` external.

The CTAN candidate uses a browsing-friendly top-level `abntexto-ufc/` directory rather than exposing internal TDS `tex/` and `doc/` staging. `release/ctan/README.md` is the package-facing README. `release/ctan/abntexto-ufc.tex` is the tracked manual source; the distribution producer builds its deterministic PDF and places source and PDF together with the current class/runtime, example and license. `tests/checks/distribution_bundles.py` proves the complete artifact set, checksum integrity, deterministic outputs, expected class/CTAN layouts, package metadata, external-upstream semantics, and asset exclusions.

The accepted `abntexto-uece` package is retained only as a practical CTAN packaging benchmark. Current CTAN guidance and the current `pkgcheck` release govern the technical submission check. See `docs/CTAN-RELEASE.md` for the maintainer procedure. CTAN acceptance is an external release event, not an architectural state inferred from local or CI validation.

## Standards data

Top-level `standards/` contains the current machine-readable source catalog, precedence, rules, locators, and normative evidence metadata needed by the active product. Process ledgers from completed campaigns are not retained merely as historical records.

Scientific-article normative/runtime material is reintroduced only in V3-A1 after current sources are reconfirmed.

## Tests, validation, and workflow orchestration

- `tests/static.py`: canonical cheap/source-only fail-closed gate. It validates tracked Python/JSON/shell/JavaScript syntax, diff integrity, canonical/repository identity, the aggregate validator/normative source contract, object-scope metadata and reference-guide contract. It snapshots repository status before/after and fails if its own execution changes that state. It must not compile TeX/PDF, access the network, generate distribution bundles or run evidence-producing/platform-certification checks;
- `tests/checks/`: static and machine-readable contract checks, some of which are source-only and some of which consume generated evidence;
- `tests/run.py`: coordinated broad integration/release runner. It remains separate from the cheap gate and may compile or inspect generated documents;
- `tests/documents/`: LaTeX validation documents;
- `tests/fixtures/`: supporting test data;
- `tests/integration/`: executable build/inspection runners;
- `tests/smoke/`: minimal compilation cases;
- `tools/`: developer/release tooling;
- `.github/workflows/static-contract.yml`: permanent fast remote orchestration. It exposes the stable workflow/job name `Static contract` and delegates validation to `make static-check`; workflow YAML does not own or duplicate the gate internals;
- `.github/workflows/linux-integration.yml`: permanent bounded PR integration orchestration. It exposes the stable workflow/job name `Linux integration`, keeps a status on relevant PR lifecycle events, suppresses the expensive TeX step for drafts and a narrow documentation/control-plane-only allowlist, treats unknown paths fail-closed as integration-relevant, cancels superseded PR runs, forces full execution on manual dispatch, and delegates heavy validation to `make check`.;
- `.github/workflows/linux-release-check.yml`: bounded permanent Linux release orchestration. It exposes the stable workflow/job name `Linux release check`, runs after technical changes land on `main` and on manual dispatch, ignores documentation/control-plane-only main pushes, cancels superseded runs, delegates release validation to `make release-check`, mirrors the repository report into the job summary, and retains `artifacts/validation/**` for 14 days. The Linux observations are engineering evidence; final Windows/literal-font/PDF-A certification remains B8-owned.

`make static-check` is the permanent local source-only entry point. `make check` and `make release-check` retain their broader integration semantics. Workflow orchestration is a separate layer and must consume these entry points rather than redefine their ownership.

R1-BLOCK-7 and R1-BLOCK-8 are DONE. The permanent orchestration surface is exactly `Static contract`, `Linux integration`, and `Linux release check`, each delegating to its repository-owned entry point (`make static-check`, `make check`, and `make release-check`). B7-D confirmed read-only permissions, immutable action pins, bounded concurrency, stable status semantics, and zero temporary workflow residue. The current `Stable branches` ruleset has no required-status rule; the recorded recommendation is to require `Static contract` and `Linux integration`, while `Linux release check` remains a post-merge/manual release gate. B8 certified complete candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX with final literal text-family, math-policy, Unicode, embedding and PDF/A-2b inspection. V3-R2 is active; `public-api.def` remains transitional R2 debt until canonical public behavior is absorbed directly by responsibility-owning modules.

Active path names must not encode retired major-version or N-phase identities.

## Validator

`validator/` is project-owned engineering software. Its implementation, controls, technical labels, and diagnostics are English. Portuguese text extracted from or evaluated inside a Brazilian academic PDF is document data, not validator engineering nomenclature.

## Documentation and release state

`docs/` contains current engineering and maintainer documentation. `release/` contains current machine-readable migration/release state plus source material required to construct current release candidates, such as `release/ctan/`. A migration contract remains tracked only while an active migration consumes it; after use it is removed or consolidated.

## Breaking v3 API policy

v3 provides one canonical project API. Removed Portuguese v2 project API is not retained through runtime aliases. Migration support is documentation-only and is written when the migration surface is final; it is not pre-staged as dormant files during R1/R2.

## Architecture gates

The final foundation must prove at least:

- one canonical class entry point;
- deprecated v2 class wrapper absent;
- forwarding-only public API module absent;
- unique runtime ownership;
- required runtime modules loaded exactly once;
- explicitly scoped upstream integrations;
- English project-owned engineering paths;
- one permanent side-effect-free cheap/source-only validation entry point distinct from integration/release validation;
- permanent fast remote orchestration that delegates to the repository-owned cheap gate rather than duplicating it;
- clean-runner-safe repository-owned integration/release entry points before permanent heavy orchestration is activated;
- valid repository template layout and valid flattened public bundle layout;
- deterministic class/runtime and CTAN distribution candidates with checksum metadata;
- no institutional/proprietary assets in public distribution;
- no generated artifacts, archive directories, or unused migration scaffolding tracked.
