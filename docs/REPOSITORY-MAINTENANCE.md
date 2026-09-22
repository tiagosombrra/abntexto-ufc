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
| 3 | `standards/` taxonomy | in progress — issue #362; slices 3A–3F5 complete; 3G migrations/final flat-root cleanup in progress |
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

### Slice 3D final receipt

Slice 3D is complete. PR #368 merged as `29376fef85f2ef7655132d368f2cd10c9bd3f867` after Static Contract #760 and Linux Integration #660 passed. Post-merge `main` passed Static Contract #761 and Linux Release Check #249. All nine evidence/validation authorities now exist only under `standards/evidence/`, with no flat compatibility copies.

### Slice 3E execution map

Slice 3E moves the eleven unique `locator-audit*.json` authorities into `standards/audits/locator/`. `source-audit.json` is not part of this slice because slice 3A already classified it as source/catalog authority at `standards/catalog/source-audit.json`.

The preliminary plan mentioned possible 3E sub-slices. The post-3D audit supersedes that provisional split: all eleven locator files form one uniform semantic family, the current branch diff moves them as content-identical renames, and recursive resolution already provides a single fail-closed consumer path. Therefore 3E is executed as one bounded PR rather than artificial sub-slices.

The path-resolution contract must require every locator audit to resolve under `standards/audits/locator/` and must reject any flat compatibility copy. `standards/README.md` documents the new ownership. Slice 3E changes taxonomy only: no locator payload, normative rule, runtime behavior, public API or published v3.0.4 artifact may change.

### Slice 3E validation incident

Initial PR #370 Static Contract #762 failed after the eleven locator audit authorities moved because the generic stale-path guard found 29 active flat references across 25 normative checks. The affected consumers span citations, typography, sections, pagination, references, objects and the consolidated locator audit.

No exception or compatibility copy was introduced. Every affected locator consumer now resolves its authority through `tools/repository_paths.py::standard_file`. The consolidated `normative_locators.py` check resolves `locator-audit.json` canonically and continues to discover its supplements relative to that resolved audit directory. Failed Static #762 remains part of the audit trail; fresh Static and Linux Integration validation is required before merge.

Static Contract #789 then reduced the residual set to one occurrence in `tests/checks/normative_locators.py`: the consolidated `locator-audit.json` path had not matched the bulk replacement pattern used for the domain-suffixed locator filenames. That final consumer now uses `standard_file("locator-audit.json")`; no guard exemption was added. Failed #789 remains part of the audit trail.



### Slice 3E final receipt

Slice 3E is complete. PR #370 merged as `f7735262187fd1850cf222aca424e40203192fb2` after Static Contract #791 and Linux Integration #690 passed. Post-merge Static Contract #792 passed; Linux Release Check #250 is recorded separately when complete. All eleven locator-audit authorities now exist only under `standards/audits/locator/`.

### Slice 3F execution strategy

Scenario migration is divided by observable domain instead of moving the remaining scenario corpus in one large PR. Each sub-slice moves content-identical JSON blobs, updates all direct consumers to `tools/repository_paths.py::standard_file`, binds the family to its semantic directory in the path-resolution contract, updates this roadmap and the standards index, and forbids flat compatibility copies.

#### Slice 3F1 — frontmatter scenarios

Slice 3F1 moves eleven front-matter scenario authorities into `standards/scenarios/frontmatter/`:

- `frontmatter-acknowledgments-scenario.json`;
- `frontmatter-alignment-scenarios.json`;
- `frontmatter-approval-scenario.json`;
- `frontmatter-cover-scenario.json`;
- `frontmatter-errata-scenario.json`;
- `frontmatter-lists-scenario.json`;
- `frontmatter-pagination-scenario.json`;
- `frontmatter-scenarios.json`;
- `frontmatter-summary-scenario.json`;
- `frontmatter-title-page-scenario.json`;
- `frontmatter-toc-scenario.json`.

All eleven moves reuse the exact existing Git blob identities. The corresponding Python evidence checks resolve scenario files recursively by unique basename. No normative payload, runtime behavior, public API, release metadata or published v3.0.4 byte changes in this slice.


### Slice 3F1 final receipt

Slice 3F1 is complete. PR #371 merged as `148851e45c8ab7271b5d73ca4759a9f1e379928f` after Static Contract #793 and Linux Integration #691 passed. Post-merge `main` passed Static Contract #794 and Linux Release Check #251. All eleven front-matter scenarios now exist only under `standards/scenarios/frontmatter/` as content-identical renames.

### Slice 3F2 execution map

Slice 3F2 moves exactly seven citation/quotation scenario authorities into `standards/scenarios/citations/`: `apud-presentation-scenario.json`, `direct-citation-source-scenario.json`, `indirect-citation-source-scenario.json`, `long-quotation-scenario.json`, `long-quote-reduced-size-scenario.json`, `short-direct-citation-scenario.json` and `ufc-citation-system-scenario.json`.

The seven corresponding normative Python checks resolve their scenario through `tools/repository_paths.py::standard_file`. The path-resolution contract requires every basename to resolve under the citations scenario directory and forbids flat compatibility copies. JSON payloads, normative semantics, runtime behavior, public API and published v3.0.4 bytes remain unchanged.

The remaining scenario plan is explicitly mapped as 3F3 layout/typography/sections/footnotes (13 files), 3F4 objects/backmatter/references/research-project (9 files), and 3F5 controlled negative scenarios (`negative-paths.json`). Phase 3G then owns only `atomicity-plan.json` and `rule-migrations.json` as migration/decomposition authorities.

### Slice 3F2 final receipt

Slice 3F2 is complete. PR #372 merged as `af035fd0eae9a3a7c26d47fcd36936d7da0d2296` after Static Contract #795 and Linux Integration #692 passed. Post-merge `main` passed Static Contract #796 and Linux Release Check #252. All seven citation/quotation scenarios now exist only under `standards/scenarios/citations/` as content-identical renames.

### Slice 3F3 execution map

Slice 3F3 moves exactly thirteen remaining layout/typography/footnote/section scenario authorities without changing their JSON payloads:

- `standards/scenarios/layout/`: `body-paragraph-scenario.json`, `page-margins-scenario.json`, `pagination-geometry-scenario.json`;
- `standards/scenarios/typography/`: `typography-scenario.json`;
- `standards/scenarios/footnotes/`: `footnote-separator-scenario.json`, `footnote-text-scenario.json`;
- `standards/scenarios/sections/`: `section-hierarchy-scenario.json`, `section-indicator-scenario.json`, `section-multiline-hanging-scenario.json`, `section-primary-after-spacing-scenario.json`, `section-primary-recto-duplex-scenario.json`, `section-unnumbered-centered-scenario.json`, `subsection-spacing-scenario.json`.

Each corresponding Python evidence consumer resolves the scenario through `tools/repository_paths.py::standard_file`. The path-resolution contract binds each basename to its semantic directory and forbids flat compatibility copies. This slice changes taxonomy only: no normative value, validation tolerance, runtime behavior, public API, release metadata, v3.0.4 published byte or CTAN-submitted byte is changed.


### Slice 3F3 merge receipt

Slice 3F3 merged through PR #373 as `da21d47dd41c1bf529104231487eaa3765917878` after Static Contract #797 and Linux Integration #693 passed. Post-merge Static Contract #798 and Linux Release Check #253 both passed. Slice 3F3 is fully closed.

### Slice 3F4 execution map

Slice 3F4 moves exactly nine remaining domain scenarios without changing their JSON payloads:

- `standards/scenarios/backmatter/`: `appendix-annex-final-pdf-scenario.json`, `index-glossary-final-pdf-scenario.json`;
- `standards/scenarios/objects/`: `equation-display-final-pdf-scenario.json`, `illustration-final-pdf-scenario.json`, `table-ibge-vector-final-pdf-scenario.json`, `table-typography-final-pdf-scenario.json`;
- `standards/scenarios/references/`: `reference-layout-scenario.json`, `reference-semantics-scenario.json`;
- `standards/scenarios/research-project/`: `research-project-structure-final-pdf-scenario.json`.

Every consumer resolves the scenario through `tools/repository_paths.py::standard_file`. The path-resolution contract binds each basename to its semantic directory and forbids flat compatibility copies. This slice is taxonomy-only: normative values, validation tolerances, runtime behavior, public API, release metadata, published v3.0.4 bytes and CTAN-submitted bytes remain unchanged.

After 3F4, only the controlled negative-path scenario remains for 3F5. Phase 3G then owns only `atomicity-plan.json` and `rule-migrations.json`.


### Slice 3F4 merge receipt

Slice 3F4 merged through PR #374 as `ff86f3e99be7df8e286ad8ae84a6dd75f6807c49` after Static Contract #799 and Linux Integration #694 passed. Post-merge Static Contract #800 and Linux Release Check #254 both passed. Slice 3F4 is fully closed.

The nine domain scenarios now exist only under `standards/scenarios/backmatter/`, `objects/`, `references/`, and `research-project/`, with content preserved byte-for-byte.

### Slice 3F5 execution map

Slice 3F5 moves only `negative-paths.json` to `standards/scenarios/negative/`. The manifest payload and rejection semantics remain unchanged. `tests/checks/normative_negative_paths.py` resolves the authority through `standard_file(...)`, and the path-resolution contract forbids a retired flat compatibility copy.

After 3F5, the standards root must contain only `README.md`, `atomicity-plan.json`, and `rule-migrations.json`. Phase 3G then moves those final two migration/decomposition authorities under `standards/migrations/`.

### Slice 3F5 validation incident

Initial Static Contract #801 failed after the controlled negative scenario moved because `tests/checks/test_surface_integrity.py` still bound `NEGATIVE_PATHS` to the retired flat path `standards/negative-paths.json`. The fail-closed stale-path guard correctly rejected that residual consumer.

No compatibility copy or guard exemption was added. The integrity check now resolves `negative-paths.json` through `tools/repository_paths.py::standard_file`, matching the canonical recursive authority used by the negative-path runner. Failed run #801 remains part of the audit trail; fresh Static and Linux Integration validation is required before merge.

### Slice 3F5 final receipt

Slice 3F5 is complete. PR #376 merged as `c812411e28b7f6a705b18c9a88b2d0758bc194db` after Static Contract #803 and Linux Integration #697 passed. The initial fail-closed Static #801 finding remains recorded; the isolated path-resolution correction passed Static #802 before the documented final PR head was certified. Post-merge `main` passed Static Contract #804 and Linux Release Check #255.

The controlled negative-path manifest now exists only at `standards/scenarios/negative/negative-paths.json`, and active consumers resolve it through the canonical recursive standards resolver. No normative payload, runtime behavior, public API, release metadata, published v3.0.4 byte or CTAN-submitted byte changed.

### Slice 3G execution map

Slice 3G closes the standards taxonomy by moving the two remaining decomposition/migration control authorities into `standards/migrations/` as content-identical renames:

- `atomicity-plan.json` -> `standards/migrations/atomicity-plan.json`;
- `rule-migrations.json` -> `standards/migrations/rule-migrations.json`.

All active consumers must resolve these authorities through `tools/repository_paths.py::standard_file`. The path-resolution contract binds both basenames to `standards/migrations/`, forbids flat compatibility copies, and requires the standards root to contain no machine-readable JSON authority after this slice.

This slice changes taxonomy and path bindings only. It must not change migration mappings, atomicity semantics, normative values, proof state, runtime behavior, public API, release metadata, published v3.0.4 bytes or CTAN-submitted bytes. Phase 4 remains blocked until 3G is merged, post-merge certified, issue #362 receives the final Phase 3 closeout receipt, and current `main` is reconciled.
