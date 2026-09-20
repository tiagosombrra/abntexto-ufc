abntexto-ufc changelog
======================

3.0.4 — 2026-09-19
------------------

- Consolidates the project-owned runtime into one canonical tracked `abntexto-ufc.cls`, removing the 14 project-owned `.def` runtime modules while preserving the supported public behavior.
- Makes the tracked canonical class the same project-owned runtime tested in the repository and distributed through CTAN, Template and Overleaf; CTAN receives the class byte-for-byte.
- Simplifies distribution builders around the canonical runtime while preserving the packaging contract: CTAN excludes UFC institutional marks, while Template/Overleaf include the authorized project coat-of-arms asset and preserve `coat-of-arms=true`.
- Reconciles active documentation to the current supported architecture, removes active v2→v3 migration guidance, and adds durable repository/contributor surfaces including `docs/README.md`, `tests/README.md`, `standards/README.md`, `CONTRIBUTING.md`, `SECURITY.md` and `CITATION.cff`.
- Moves deterministic CI logic into repository-owned scripts, refreshes pinned GitHub Actions under fail-closed validation, and keeps Static Contract, Linux Integration and Linux Release Check as the release-control gates.
- Defines a conservative boundary for retained v3 historical evidence so historical engineering/release snapshots remain audit evidence rather than current user or maintainer authority.
- Adds `standards/public-api.json` as the machine-readable current project API contract and validates it against the canonical runtime and `docs/COMMAND-REFERENCE.md`; historical migration mappings remain only for negative/residual validation.
- Establishes root `CHANGELOG.md` as the single version-history authority and makes the CTAN builder copy those canonical bytes into the package as `CHANGELOG`.
- Keeps the published v3.0.3 source, tag, immutable GitHub Release assets, checksums and publication evidence unchanged.

3.0.3 — 2026-09-17
------------------

- Corrects the distribution contract so the GitHub Template and Overleaf bundles include `assets/institutional/ufc-coat-of-arms.png` and preserve `coat-of-arms=true` in the canonical example.
- Keeps the CTAN package intentionally sanitized: no UFC institutional mark asset is redistributed and the minimal CTAN example continues to use `coat-of-arms=false`.
- Adds regression coverage that fails when Template/Overleaf omit the expected institutional asset or when CTAN accidentally includes an institutional mark.
- Keeps the v3.0.2 tag, GitHub Release assets, certified checksums and submitted CTAN bytes immutable historical artifacts.
- Preserves the v3 public API, runtime behavior and normative baseline outside this packaging correction.

3.0.2 — 2026-09-14
------------------

- Corrects the References/Glossary table-of-contents alignment while preserving the established five-level section hierarchy and TOC design.
- Restores the UFC institutional coat of arms as the default on research-project and anonymized-research-project covers, while preserving `coat-of-arms=false` as an explicit opt-out.
- Replaces the oversized manual-style canonical reference with a compact five-chapter TCC tutorial and separates workflow guidance and exhaustive API lookup into dedicated user documentation.
- Keeps Template and Overleaf bundles self-contained with the public user guides while continuing to exclude UFC institutional assets and proprietary Microsoft fonts from public archives.
- Closes canonical bibliography references used by the scientific-article review profile and strengthens release/test orchestration so technical PR changes cannot be hidden by later documentation-only commits.
- Preserves the accepted v3 public API, current normative baseline, typography hierarchy and published v3.0.1 historical artifacts.

3.0.1 — 2026-09-10
------------------

- Recovers the v3 publication process after the premature public GitHub v3.0.0 release was found to point to a source SHA that did not satisfy the repository's final exact-SHA release invariant.
- Includes the post-v3.0.0 unified-illustration-list runtime correction from PR #302, fixing populated `l@loii` rendering so it obeys the two-argument `abntexto` list-entry contract and adding a populated regression case.
- Preserves the accepted v3 public API, normative rules, document profiles and typography outside that scoped runtime correction.
- Rebinds release packaging, CTAN metadata and final certification artifacts to version 3.0.1.
- Requires a fresh exact-SHA Static/Linux/pkgcheck/visual-acceptance cycle over the combined PR #302 + release-recovery state before the 3.0.1 tag and CTAN submission.
- The earlier GitHub v3.0.0 assets are historical/superseded publication artifacts and must not be submitted to CTAN as the final package.

3.0.0 — 2026-09-09
------------------

- Introduces the `abntexto-ufc` class as the canonical class entry point.
- Establishes a single canonical English project-owned public API.
- Adds academic-work profiles for undergraduate capstones, specialization capstones, master's theses and doctoral theses.
- Adds research-project and anonymized research-project profiles.
- Adds the UFC scientific-article profile.
- Updates the active technical baseline to current applicable ABNT editions, including NBR 14724:2024, NBR 10520:2023, NBR 6023:2025, NBR 15287:2025 and NBR 12225:2023.
- Provides deterministic release packaging and PDF/A-oriented certification gates.
- Keeps the development sources modular while distributing a single generated `abntexto-ufc.cls` through CTAN; no project-owned `.def` files are included in the CTAN package.
- Keeps `abntexto` as an external CTAN dependency; it is not vendored in the CTAN package.
- Does not redistribute UFC institutional marks or proprietary Microsoft font files.

The current API is documented by the repository command reference and is the only supported project-owned public API.
