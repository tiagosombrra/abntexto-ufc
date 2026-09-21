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
| 3 | `standards/` taxonomy | in progress — issue #362; slices 3A–3C, path-consistency follow-up and 3D1 complete; 3D2 in progress |
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

### Slice 3B final receipt

Slice 3B is complete. PR #364 merged as `c80e205e67b008b1daa4a9005cbbfff36aa7cf6c` after Static Contract #706 and Linux Integration #610 passed. Post-merge `main` then passed Static Contract #707 and Linux Release Check #245. The public API authority exists only at `standards/api/public-api.json`.

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


### Slice 3C final receipt

Slice 3C is complete. PR #365 merged as `79ffaddbd0ed9616b809a06d9e3fc198b951486b` after Static Contract #713 and Linux Integration #616 passed. Post-merge `main` passed Static Contract #714 and Linux Release Check #246. The eight rule authorities exist only under `standards/rules/`, with no compatibility copies.

### Path-consistency follow-up

The post-3C forward audit found active textual references to already-moved standards authorities in `validator/README.md`, `docs/NORMATIVE-CURRENCY.md` and `standards/article-evidence-map.json`. This follow-up corrects those references before slice 3D and strengthens `tests/checks/path_resolution_contract.py` so every JSON authority already nested below `standards/` automatically rejects an active `standards/<basename>` reference.

Controlled history, `CHANGELOG.md` and this maintenance roadmap are excluded from that active-path scan because they intentionally preserve historical moved-from paths as audit evidence. No runtime, public API, normative value or published v3.0.4 byte changes in this follow-up.


The first Static Contract run for this follow-up, #715, failed before the new stale-path scan could complete because the guard implementation itself contained generic history-root string literals rather than using concrete path ancestry. The pre-existing repository contract correctly rejected those unapproved generic history-root references. The exclusion logic now uses concrete `Path` ancestry instead, preserving both controls without weakening either one. The failed #715 run remains part of the audit trail.


Static Contract #717 then failed because this maintenance receipt itself described the historical exclusions using generic history-root text instead of the approved controlled v3 namespaces. The prose now names only `docs/history/v3/` and `release/history/v3/`. No repository-history policy was relaxed; #717 is retained as a documentation-regression receipt.


Static Contract #718 then exercised the generic moved-authority guard and correctly found eight remaining active stale references: two in catalog/rule metadata, six diagnostic/generator/generated-catalog references. These were classified as real taxonomy drift rather than guard false positives. The references now use the canonical semantic paths; no exemptions were added for them. Failed run #718 remains part of the audit trail.


### Path-consistency validation receipt

The post-3C consistency follow-up in PR #366 passed Static Contract #724 and Linux Integration #626 after the stale authority references identified by #718 were corrected. The generic moved-authority guard remains fail-closed and no compatibility copies or exemptions were introduced for active stale references. PR #366 merged as `68b6ec1619fdaa379543fa6fb68b56df5f0a3fd3`; post-merge Linux Release Check #247 passed. The generic stale-authority guard is therefore certified on current `main` and slice 3D is unblocked.


### Slice 3D execution map

Slice 3D is split internally to keep evidence semantics separate from final-PDF measurement policy while retaining one roadmap checkbox.

#### Slice 3D1 — evidence semantics and proof ownership

The following unique authorities move to `standards/evidence/`:

- `article-evidence-map.json`;
- `evidence-contribution-policy.json`;
- `evidence-registry.json`;
- `false-coverage-policy.json`;
- `proof-policy.json`;
- `test-surface-policy.json`;
- `validation-overrides.json`.

Direct consumers resolve these resources through `tools/repository_paths.py::standard_file`. No flat compatibility copies are permitted. The path-resolution contract requires every moved basename to resolve only under `standards/evidence/`.

#### Slice 3D2 — final-PDF measurement policy

`validation-reference-policy.json` and `vector-rule-validation-extension.json` remain a separate bounded move because they have a broader consumer surface across geometry, typography, objects and final-PDF validation. Their internal path binding must be updated atomically.

Slice 3D changes taxonomy only: no normative values, proof states, runtime behavior or public API are changed.


### Slice 3D1 validation incident and correction

Initial PR #367 validation produced Static Contract #729 PASS but Linux Integration #630 FAIL. The Linux failure was caused by a residual composed path in `tests/checks/normative_typography.py`:

`ROOT / "standards" / "evidence-registry.json"`

After `evidence-registry.json` moved to `standards/evidence/`, that consumer failed to load the authority. The negative-path suite then reported a secondary failure because its positive typography baseline depends on the same integration gate.

The correction replaces that direct path with `repository_paths.standard_file("evidence-registry.json")` and strengthens `tests/checks/path_resolution_contract.py` so moved-authority checks reject both literal `standards/<file>` references and composed `ROOT / "standards" / "<file>"` references. The failed #630 run remains part of the audit trail. The first strengthened-guard rerun, Static Contract #732, then failed on intentional retired-path strings inside `tests/checks/path_resolution_contract.py` itself. That file is now excluded only from the generic textual stale-path scan because it must name retired paths to assert that compatibility copies do not exist; its explicit semantic assertions remain active. Subsequent reruns certify the corrected guard and consumer set.


### Slice 3D1 final receipt

Slice 3D1 is complete. PR #367 merged as `2e71bed633e35ad84d653357354dd8b08cc9360e` after Static Contract #734 and Linux Integration #635 passed. Post-merge `main` passed Static Contract #735 and Linux Release Check #248. The seven evidence/proof authorities exist only under `standards/evidence/`, with no flat compatibility copies.

### Slice 3D2 execution map

Slice 3D2 moves exactly two final-PDF measurement authorities into `standards/evidence/`: `validation-reference-policy.json` and `vector-rule-validation-extension.json`.

The move includes all direct Python consumers plus internal path bindings in final-PDF scenarios. Consumers must resolve these authorities through `tools/repository_paths.py::standard_file`. The validation policy's vector-extension binding must point to `standards/evidence/vector-rule-validation-extension.json`. No flat compatibility copies are permitted.

Slice 3D2 changes taxonomy and path bindings only. It does not change normative values, tolerances, proof states, runtime behavior, public API or any published v3.0.4 artifact.


### Slice 3D2 validation incident

Initial Static Contract #736 failed after the two final-PDF measurement authorities moved because the generic stale-path guard found 23 remaining active references to the former flat `standards/validation-reference-policy.json` path. The findings included one scenario binding and 22 Python evidence/validation consumers across front matter, sections, quotations, objects and PDF validation.

No exception was added. Every Python consumer now resolves `validation-reference-policy.json` through `tools/repository_paths.py::standard_file`, and the scenario binding points to `standards/evidence/validation-reference-policy.json`. Failed run #736 remains part of the audit trail; fresh Static and Linux validation is required before merge.
