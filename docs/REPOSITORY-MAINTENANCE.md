# Repository maintenance roadmap

This document is the current durable map for repository-wide maintenance and organization work. The authoritative tracking issue is #359.

It does not redefine release state. Publication and development-line facts remain owned by `release/v3-release-candidate.json` and `docs/RELEASE-STATE.md`.

## Invariants

- Published v3.0.4 source, annotated tag, GitHub Release assets and checksums remain immutable.
- CTAN follow-up remains tracked by issue #356 until external acceptance/publication is confirmed.
- `abntexto-ufc.cls` remains the canonical project-owned runtime at repository root.
- Historical evidence under `docs/history/v3/` and `release/history/v3/` is not reorganized retroactively merely for aesthetics.
- Every material phase uses a bounded branch/PR, records checks and carries unresolved findings forward.
- Structural changes must reduce path coupling before moving large groups of files.

## Phase map

| Phase | Scope | Current state |
|---|---|---|
| 0 | v3.0.4 CTAN external closeout | waiting for external CTAN acceptance under #356 |
| 1 | metadata consistency and anti-drift | complete — PR #360 merged as `496f893627b1d2211161b8408e44026a2b66b157` |
| 2 | recursive discovery and path-decoupling preparation | complete — PR #361 merged as `603c06c5d347d5857d5b5661d489a7c3d6e80211` |
| 3 | `standards/` taxonomy | in progress — issue #362; slices 3A and 3B merged, slice 3C in validation |
| 4 | `tests/` taxonomy | pending |
| 5 | supporting repository structure (`release/`, CTAN example, tools, examples) | pending |
| 6 | self-contained Web/Lite hardening | pending |
| 7 | Windows-first portability smoke coverage | pending |
| 8 | provenance, LPPL/asset metadata and archival integration | pending |
| 9 | tagged-PDF/PDF-UA experiment | pending |
| 10 | next release certification and publication | pending |

## Phase 1 receipt

Phase 1 is complete. PR #360 merged as `496f893627b1d2211161b8408e44026a2b66b157` after Static Contract #685 and Linux Integration #592 passed. Linux Release Check was not selected on the PR by its scoped trigger; after merge, `main` passed Static Contract #686 and Linux Release Check #242. The durable receipt is also recorded in issue #359.

## Phase 1 acceptance criteria

Phase 1 implementation is carried by PR #360. It is complete only when:

1. `CITATION.cff` identifies published v3.0.4 and its publication date;
2. `docs/ARCHITECTURE.md` no longer duplicates volatile current release/development-line values;
3. `docs/RELEASE-STATE.md` records issue #353 as completed and closed;
4. Static Contract executes an explicit metadata-consistency check;
5. the phase PR passes all required repository checks;
6. issue #359 receives the merge/check receipt.

## Phase 2 receipt

Phase 2 is complete. PR #361 merged as `603c06c5d347d5857d5b5661d489a7c3d6e80211` after Static Contract #688 and Linux Integration #594 passed. Linux Release Check was not selected on the PR by its scoped trigger; after merge, `main` passed Static Contract #689 and Linux Release Check #243. The durable receipt is also recorded in issue #359.

## Phase 2 current design

Phase 2 prepares structural moves without moving taxonomy yet.

The repository now uses two fail-closed resolution surfaces:

- `tests/path_resolver.py` resolves check/integration entrypoints recursively by unique filename identity;
- `tools/repository_paths.py` resolves machine-readable normative authorities recursively under `standards/`.

Ambiguous identities are errors. `tests/checks/path_resolution_contract.py` enforces basename uniqueness, recursive discovery and the absence of flat-path reintroduction in the core runners/loaders.

The Linux suite selector normalizes nested check, integration and document paths to stable test identities before scope classification. This allows later taxonomy changes such as `tests/integration/profiles/article/scientific-article-profile.sh` without silently changing the selected regression suite.

### Phase 2 acceptance criteria

Phase 2 is complete only when:

1. Static checks resolve recursively and retain an auditable resolved `SOURCE_CHECKS` surface;
2. integration runner commands resolve recursively by unique identity;
3. Linux suite inference preserves the same suite for nested test paths;
4. normative catalog/atomic/full loaders no longer require the relevant JSON files to remain directly under `standards/`;
5. an explicit path-resolution contract fails on missing or ambiguous identities;
6. Static and Linux Integration regressions pass;
7. issue #359 receives the merge/check receipt.

## Next-phase gate

Phase 3 may move `standards/` only after Phase 2 is merged and reconciled on current `main`. Direct-path consumers discovered during the Phase 2 audit must either adopt the canonical standards resolver or be migrated atomically with the file they own; no compatibility duplicate of a normative JSON authority may be introduced.


## Phase 3 execution map

Phase 3 is tracked by issue #362 and is intentionally split into bounded slices. Slice 3A moves only source-authority/catalog data into `standards/catalog/`. Later slices will handle API, rules, evidence, audits, scenarios and migrations separately. No slice may introduce duplicate compatibility copies of normative JSON authorities.

### Slice 3A final receipt

Slice 3A is complete. PR #363 merged as `f4363a7cc5ea10f749b2625bedfd7d6f29e0e862` after Static Contract #704 and Linux Integration #609 passed. Post-merge `main` passed Static Contract #705 and Linux Release Check #244. The six catalog/source-authority files exist only under `standards/catalog/`.

### Slice 3B execution map

Slice 3B moves the single current project-owned API authority from `standards/public-api.json` to `standards/api/public-api.json`. Current documentation and repository contracts must point to the nested authority, while historical release notes may preserve the old path as historical evidence. The path-resolution contract must reject any flat compatibility copy.

### Slice 3A regression receipt

The first Linux Integration run for slice 3A, #602, failed after the complete 38/38 repository regression had passed because the Web/Lite E2E harness still opened `standards/catalog.json` directly. The slice was not merged. The harness now resolves `catalog.json` through the canonical recursive standards resolver, and the path-resolution contract enforces the new location and no-duplicate rule for the catalog authorities moved by this slice. The failed run remains part of the audit trail.

A subsequent Static Contract run, #700, also failed because the first anti-regression scan was intentionally tested fail-closed but proved broader than slice 3A: it rejected existing direct-path consumers for standards resources scheduled for later slices. The contract was narrowed to the six catalog authorities moved by 3A plus the Web/Lite catalog consumer. This preserves the phase rule that each later resource is migrated atomically with its owning slice rather than forcing an unreviewed bulk migration.

### Slice 3C execution map

Slice 3C moves exactly eight current rule authorities into `standards/rules/`: `atomic-rules.json` and the seven `coverage-rules*.json` manifests. `atomicity-plan.json` remains reserved for slice 3G because it is a decomposition/migration control artifact. Evidence and validation policy resources remain reserved for slice 3D.

The canonical standards resolver continues to locate these resources recursively by unique filename identity. The path-resolution contract requires every moved rule authority to resolve under `standards/rules/` and forbids any flat compatibility copy. Slice 3C must pass Static Contract and Linux Integration before merge, and it must not merge until slice 3B post-merge certification is complete.

### Slice 3C regression receipt

Static Contract #708 failed after the eight rule authorities moved because three scientific-article source checks still opened the former flat `standards/coverage-rules-article.json` path directly. No merge occurred. The three checks now resolve `coverage-rules-article.json` through the canonical recursive standards resolver. The failed #708 run remains part of the audit trail and a fresh validation run is required.
