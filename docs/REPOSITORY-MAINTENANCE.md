# Repository maintenance roadmap

This document is the current durable map for repository-wide maintenance and organization work. The authoritative tracking issue is #359.

It does not redefine release state. Publication and development-line facts remain owned by `release/v3-release-candidate.json` and `docs/RELEASE-STATE.md`.

## Working policy — pragmatic mode

This roadmap is a continuity aid, not a ceremony checklist. Historical receipts below are kept for auditability, but their detailed step-by-step wording is not a mandatory template for new work.

Use the lightest process that still protects correctness:

- reconcile current remote `main` at the start of a material work item and again before merge only when the base may have changed; do not repeat the same repository-wide audit before every small edit;
- keep one material code PR active at a time, but fold related documentation and tracking updates into that PR instead of creating extra documentation-only phases;
- for taxonomy, path-only and documentation changes, require the repository's normal PR checks (Static Contract plus the selected Linux Integration scope); do not wait for an additional full release-grade run before starting the next low-risk taxonomy slice unless the previous merge produced a failure or changed runtime, normative meaning, release/distribution behavior, or published artifacts;
- use the full Linux Release Check when the change affects runtime behavior, normative/release/distribution semantics, release preparation, or when CI/contract evidence indicates that broader certification is needed;
- record decisions, meaningful failures, merge SHAs and unresolved risks; routine green reruns do not need repetitive prose receipts;
- exact file/count reconciliations are regression aids, not independent approval gates unless the change specifically depends on them;
- create separate issues only for meaningful workstreams or dependencies; small follow-ups may stay in the parent issue/PR;
- failed checks remain visible in GitHub history, but documentation only needs to explain failures that changed the implementation or revealed a real defect.

## Core invariants

- Published v3.0.4 source, annotated tag, GitHub Release assets and checksums remain immutable.
- `abntexto-ufc.cls` remains the canonical project-owned runtime at repository root.
- Historical v3 evidence is not rewritten merely for aesthetics.
- No force-push, tag retargeting, release-asset replacement or history rewriting.
- Structural moves must preserve test identity, behavior and source-of-truth ownership; no compatibility copies are introduced to hide stale paths.

## Phase map

| Phase | Scope | Current state |
|---|---|---|
| 0 | v3.0.4 CTAN external closeout | waiting for external CTAN acceptance under #356 |
| 1 | metadata consistency and anti-drift | complete — PR #360 merged as `496f893627b1d2211161b8408e44026a2b66b157` |
| 2 | recursive discovery and path-decoupling preparation | complete — PR #361 merged as `603c06c5d347d5857d5b5661d489a7c3d6e80211` |
| 3 | `standards/` taxonomy | complete — PR #377 merged as `f36797cbc34715e9ed9b82af9ddbd8d8d299fd88`; issue #362 closeout |
| 4 | `tests/` taxonomy | in progress — issue #375; check taxonomy complete through 4C6; 4D non-domain integration taxonomy in progress under #397 |
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

### Phase 3 final receipt

Phase 3 is complete. Its final slice, 3G, merged through PR #377 as `f36797cbc34715e9ed9b82af9ddbd8d8d299fd88` after Static Contract #805 and Linux Integration #698 passed. Post-merge `main` passed Static Contract #806 and Linux Release Check #256 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

The final standards taxonomy invariants are:

- `standards/` contains only `README.md` as a root file; every machine-readable authority is under a semantic directory;
- the final 3G moves preserve the original Git blobs for `atomicity-plan.json` and `rule-migrations.json`;
- movable standards consumers resolve authorities recursively by unique basename and fail closed on ambiguity;
- flat compatibility copies are forbidden by the path-resolution contract;
- no normative value, migration mapping, proof state, runtime behavior, public API, release metadata, published v3.0.4 byte or CTAN-submitted byte changed during the taxonomy phase;
- the complete post-merge certification retained canonical class identity, checksum/archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

Issue #362 is the detailed Phase 3 audit trail. Phase 4 is tracked by #375 and begins with resolver/path hardening before any test file is moved.

### Phase 4A execution map

Phase 4 begins with path hardening before any test file move. The certified entry baseline contains 84 Python checks under `tests/checks/` and 86 executable `.py`/`.sh` integration surfaces under `tests/integration/`.

At entry, `tests/run.py` has exactly three direct movable check paths: `repository_contract.py`, `validator_source.py`, and `normative_evidence_contribution.py`. Slice 4A resolves those identities through `tests/path_resolver.py::check_file` while preserving their current interpreter, arguments, check names and execution ordering.

The path-resolution contract must reject any future hard-coded `tests/checks/...` path in `tests/run.py`. Existing recursive integration resolution and suite-inference behavior remain unchanged, including nested validator/article path invariance. No check, integration script, document or fixture is moved in 4A.

Acceptance requires the 84/86 identity baseline to remain unique and reachable, test-surface integrity to retain zero orphaned scripts/assets/technical controls, Static Contract to pass, and the applicable Linux integration scope to pass before taxonomy slice 4B can begin.

### Phase 4A final receipt

Phase 4A is complete. PR #379 merged as `c366ed6cbe3ba738f2f4743c8274f968a257dac7` after Static Contract #809 and Linux Integration #700 passed. Post-merge `main` passed Static Contract #810 and Linux Release Check #257. No test file moved in this slice. The three direct movable check commands in `tests/run.py` now resolve by unique basename through `check_file(...)`, and the path-resolution contract rejects a reintroduced hard-coded `tests/checks/...` runner path.

### Phase 4A2 execution map

Pre-move audit found that movable checks commonly derive repository root through the fixed-depth expression `Path(__file__).resolve().parents[2]`. This is correct only while a check is an immediate child of `tests/checks/`; a semantic subdirectory would change the resolved parent and silently point at `tests/` instead of the repository root. Issue #380 owns this prerequisite hardening.

Phase 4A2 moves no files. It prepares the initial repository/control check family — `canonical_identity.py`, `engineering_language.py`, `librarian_review_contract.py`, `linux_integration_suites.py`, `metadata_consistency.py`, `path_resolution_contract.py`, `phase_governance.py`, and `repository_contract.py` — to locate the stable `tests/path_resolver.py` ancestor and import canonical `ROOT` from that module.

The path-resolution contract records the prepared family and rejects fixed-depth repository-root derivation in any nested `tests/checks/**` script. This creates a fail-closed prerequisite for later taxonomy moves without bulk-editing unrelated checks before their own bounded slice. Runtime behavior, public API, normative state, release state and published artifacts remain unchanged.

### Phase 4A2 final receipt

Phase 4A2 is complete. PR #381 merged as `0081adac3a88822f4bb8f3f779f8336c5635f862` after Static Contract #811 and Linux Integration #701 passed. Post-merge `main` passed Static Contract #812 and Linux Release Check #258 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. No test file moved in 4A2.

The certified pre-move baseline remains 84 Python checks, 86 integration identities, 170/170 retained test scripts reachable, 115/115 test assets reachable and 27/27 technical controls reachable. Eight repository/control checks are location-independent; the remaining fixed-depth checks remain deliberately flat until their own bounded family preparation.

### Phase 4B1 execution map

Issue #382 moves exactly the prepared repository/control family into `tests/checks/repository/`:

- `canonical_identity.py`;
- `engineering_language.py`;
- `librarian_review_contract.py`;
- `linux_integration_suites.py`;
- `metadata_consistency.py`;
- `path_resolution_contract.py`;
- `phase_governance.py`;
- `repository_contract.py`.

Four files move as blob-identical renames. Four files receive only the path-key updates required to preserve their existing negative/self-exemption semantics. Historical forbidden paths for already removed checks remain historical and are not rewritten.

The path-resolution contract binds all eight basenames to `tests/checks/repository/`, forbids flat compatibility copies and scans active non-historical text surfaces for stale `tests/checks/<basename>.py` references. Basename identity, runner names, suite inference, test counts, reachability, runtime/public API, normative state, release state and published artifacts must remain unchanged.

### Phase 4B1 validation incident

Initial Static Contract #813 failed on PR #383 after the repository/control checks moved because the new stale-check-path guard found three active consumers still naming retired flat paths:

- `docs/ENGINEERING-LANGUAGE.md` referenced `tests/checks/engineering_language.py`;
- `docs/LINUX-INTEGRATION-SCOPES.md` referenced `tests/checks/linux_integration_suites.py`;
- `tests/integration_suites.py` retained `tests/checks/linux_integration_suites.py` in the orchestration exact-path set.

The failure is retained as audit evidence. No compatibility copy or guard exemption was added. Those consumers are updated to the repository namespace, preserving engineering-language policy and Linux suite-selection semantics. Fresh Static and Linux Integration gates are required before merge.

### Phase 4B1 final receipt

Phase 4B1 is complete. PR #383 merged as `99fabe32b4eea2d93ef3c696e882001b9916d17a` after Static Contract #814 and Linux Integration #703 passed. Initial Static #813 is retained as evidence of three active stale flat-path consumers; Linux #702 is retained as a superseded concurrency-cancelled run. Post-merge `main` passed Static Contract #815 and Linux Release Check #259 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The eight repository/control checks now exist only under `tests/checks/repository/`. The certified 84-check / 86-integration identity baseline and zero-orphan script/asset/technical-control invariants remain unchanged.

### Phase 4B2a execution map

Issue #384 moves exactly two release-packaging checks into `tests/checks/distribution/`: `distribution_bundles.py` and `public_bundles.py`.

Before moving, each check replaces fixed `Path(__file__).resolve().parents[2]` root discovery with the canonical `tests/path_resolver.py` bootstrap. The two standalone release-candidate entries in `standards/evidence/test-surface-policy.json` and the active `distribution_bundles.py` exemption in `tests/checks/repository/canonical_identity.py` follow the new paths without changing their classification or semantics.

The generic stale-check-path contract is extended from a repository-only filename set to an explicit basename-to-canonical-path mapping, allowing one fail-closed mechanism to protect both `tests/checks/repository/` and `tests/checks/distribution/`. Flat compatibility copies remain forbidden. Bundle-validation behavior, evidence identity, runtime/public API, normative state, release metadata and published artifacts must remain unchanged.

### Phase 4B2a final receipt

Phase 4B2a is complete. PR #385 merged as `bc5c5107ce6751330754df7ac865024ea1718b7f` after Static Contract #816 and Linux Integration #704 passed. Post-merge `main` passed Static Contract #817 and Linux Release Check #260 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The two release-packaging checks now exist only under `tests/checks/distribution/`. Their entries in `standards/evidence/test-surface-policy.json` changed only by path: class, owner stage, purpose and retention reason remained semantically identical. The certified 84-check / 86-integration identity and zero-orphan baselines remain unchanged.

### Phase 4B2b execution map

Issue #386 moves exactly `validator_source.py` and `pdf_validation_core.py` into `tests/checks/validator/`.

Both checks replace fixed `Path(__file__).resolve().parents[2]` root discovery with the canonical `tests/path_resolver.py` bootstrap. `validator_source.py` replaces its direct flat binding to `pdf_validation_core.py` with `check_file("pdf_validation_core.py")`, preserving stable basename identity before and after the move. Its direct paths to normative checks remain unchanged until those normative families move in Phase 4C.

The generic moved-check mapping gains the two validator basenames and canonical `tests/checks/validator/` paths; stale flat paths and compatibility copies remain fail-closed. No validator application, Web/Lite E2E, CLI, integration script, normative semantics, runtime/public API, release metadata or published artifact changes in this slice.

### Phase 4B2b validation incident

Initial Static Contract #818 failed on PR #389 after the validator/PDF checks moved because the fail-closed moved-check guard found three active consumers still naming retired flat paths:

- `tests/integration/pdf-validation-core.sh` referenced `tests/checks/pdf_validation_core.py`;
- `tests/integration_suites.py` referenced `tests/checks/validator_source.py`;
- `validator/README.md` referenced `tests/checks/validator_source.py`.

The failure is retained as audit evidence. No compatibility copy or stale-path exemption was added. Those consumers are updated to the validator namespace while preserving integration-suite selection and validator documentation semantics. Fresh Static and Linux Integration gates are required before merge.

### Phase 4B2b final receipt

Phase 4B2b is complete. PR #389 merged as `7ef23716867b3725548c21ee0e64b27316e5acc6` after Static Contract #819 and Linux Integration #706 passed. Initial Static #818 is retained as evidence of three active stale validator/PDF paths; Linux #705 is retained as a superseded concurrency-cancelled run. Post-merge `main` passed Static Contract #820, Pages #6 and Linux Release Check #261 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The validator/PDF checks now exist only under `tests/checks/validator/`. The certified 84-check / 86-integration identity baseline remains unchanged, with 8 repository checks, 2 distribution checks and 2 validator checks represented by the moved-check path contract and zero orphaned scripts, assets or technical controls.

### Phase 4B2c execution map

Issue #387 moves exactly six profile/article checks into `tests/checks/profiles/`:

- `profile_matrix_contract.py`;
- `scientific_article_body.py`;
- `scientific_article_evidence_map.py`;
- `scientific_article_front_block.py`;
- `scientific_article_profile_contract.py`;
- `scientific_article_recommendations_contract.py`.

All six replace fixed `Path(__file__).resolve().parents[2]` root discovery with the canonical `tests/path_resolver.py` bootstrap. `profile_matrix_contract.py` needs only canonical `ROOT`; the five scientific-article checks retain their existing `ROOT/tools` helper imports after location-independent bootstrap.

Known active consumers follow the new paths in `scientific-article-front-block.sh`, `scientific-article-body.sh` and `scientific-article-recommendations.sh`. The profile and foreign-elements integration scripts contain no direct check-path invocation and remain unchanged.

The moved-check mapping gains the six profile basenames and canonical `tests/checks/profiles/` paths. Flat compatibility copies and stale flat references remain fail-closed. Linux suite selection requires no proactive `PATH_RULES` edit because movable check paths are normalized by basename before scope matching. File modes are preserved exactly across the move. Expected flat-root check count after this slice is 66.

### Phase 4B2c validation incident

Initial Static Contract #821 failed on PR #390 after the profile/article checks moved because the fail-closed moved-check guard found one active semantic consumer still naming the retired flat path: `tests/checks/repository/engineering_language.py` referenced `tests/checks/profile_matrix_contract.py`.

That reference is not incidental text: the engineering-language contract verifies that the profile-matrix check remains a live consumer of `release/history/v3/v3-api-migration.json`. The consumer path is updated to `tests/checks/profiles/profile_matrix_contract.py` while preserving the same migration-contract assertion. The failed run is retained as audit evidence; no compatibility copy or stale-path exemption is added. Fresh Static and Linux Integration gates are required before merge.

### Phase 4B2c final receipt

Phase 4B2c is complete. PR #390 merged as `43ef38bae5cf0df23327f60976ca9ae8d2779fd0` after Static Contract #822 and Linux Integration #708 passed. Initial Static #821 is retained as evidence of one active semantic stale path in `tests/checks/repository/engineering_language.py`; Linux #707 is retained as superseded-head history. Post-merge `main` passed Static Contract #823 and Linux Release Check #262 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The six profile/article checks now exist only under `tests/checks/profiles/`. The certified 84-check / 86-integration identity baseline remains unchanged, the moved-check path contract reports 6 profile checks, and the flat `tests/checks/` root contains exactly 66 Python checks.

### Phase 4B2d execution map

Issue #388 moves exactly `v3_api_residual.py` into `tests/checks/api/`.

The check preserves executable mode `100755`, adds `sys` only for the canonical `tests/path_resolver.py` bootstrap, and replaces fixed `Path(__file__).resolve().parents[2]` root discovery with imported canonical `ROOT`. Its controlled engineering self-exemption follows the new `tests/checks/api/v3_api_residual.py` path without changing residual/negative-test semantics.

The live migration-contract consumer entry in `tests/checks/repository/engineering_language.py` follows the moved API check while preserving the assertion that both the API-residual check and profile-matrix check consume `release/history/v3/v3-api-migration.json`.

The moved-check path contract gains one API basename mapped to `tests/checks/api/v3_api_residual.py`; stale flat paths and compatibility copies remain fail-closed. No runtime/public API, normative values, release metadata or published artifact changes in this slice. Expected flat-root check count after the move is the certified pre-4C target of 65.

### Phase 4B2d final receipt

Phase 4B2d is complete. PR #401 merged as `6f0aecd9956e8d2cb8707d802098c7ded51adffe` after Static Contract #824 and Linux Integration #709 passed. Post-merge `main` passed Static Contract #825 and Linux Release Check #263 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The API residual check now exists only under `tests/checks/api/`, executable mode is preserved, and the flat `tests/checks/` root contains exactly 65 Python checks. This satisfies the Phase 4C entry invariant.

### Phase 4C1a execution map

Issue #407 moves exactly 10 governance/source-authority checks into `tests/checks/governance/`:

- `normative_configuration.py`;
- `normative_currency.py`;
- `normative_locators.py`;
- `normative_negative_paths.py`;
- `normative_precedence.py`;
- `normative_proof_state.py`;
- `normative_rule_migrations.py`;
- `normative_source_references.py`;
- `normative_sources.py`;
- `reference_guide_contract.py`.

All 10 replace fixed `Path(__file__).resolve().parents[2]` root discovery with the canonical `tests/path_resolver.py` bootstrap. Existing `ROOT/tools` imports remain semantically unchanged. `normative_proof_state.py` additionally resolves the directory of `normative_traceability.py` through `check_file("normative_traceability.py")` instead of relying on the flat `tests/checks/` directory; this is required so 4C1b can later move traceability into `tests/checks/evidence/` without breaking the governance check.

The moved-check path contract gains the 10 governance basenames and canonical paths. Flat compatibility copies and stale flat references remain fail-closed. `normative_locators.py` preserves executable mode `100755`; the other nine governance checks preserve mode `100644`. Expected flat-root check count after this slice is 55. No normative value, source-authority decision, runtime/public API, release metadata or published artifact changes.

### Phase 4C1a validation incident

Initial Static Contract #826 failed on PR #409 after the governance/source-authority checks moved because the fail-closed moved-check guard found four active retired flat-path references across three consumers:

- `standards/scenarios/negative/negative-paths.json` referenced `tests/checks/normative_configuration.py`;
- `tests/integration/negative-paths.sh` referenced both `tests/checks/normative_configuration.py` and `tests/checks/normative_negative_paths.py`;
- `tests/integration/reference-guide-contract.sh` referenced `tests/checks/reference_guide_contract.py`.

Those paths are updated to the canonical `tests/checks/governance/` namespace while preserving negative-path and reference-guide validation semantics. The failed run is retained as audit evidence. No compatibility copy or stale-path exemption is added. Fresh Static and Linux Integration gates are required before merge.

### Phase 4C1a second validation incident

Static Contract #827 passed the generic moved-check stale-path contract but then failed inside `tests/checks/validator/validator_source.py`. That validator contract still constructed movable normative check paths through `ROOT / "tests" / "checks" / <filename>`, so it attempted to open the retired flat `normative_currency.py` path after the governance move.

The correction replaces every validator-source binding to a movable check — frontmatter evidence plus normative coverage, governance, traceability, evidence, atomic/full and validator contracts — with `check_file("<basename>")`. This is a resolver hardening change only: execution labels, check order and validation semantics remain unchanged. It also prevents the same hidden flat-path dependency from recurring in 4C1b and later 4C moves.

The path-resolution contract now rejects reintroduction of `ROOT / "tests" / "checks"` in `validator_source.py`. Failed Static #827 remains part of the audit trail; no compatibility copies are introduced.

### Phase 4C1a third validation incident

Static Contract #828 passed the moved-check path contract and the resolver-hardened validator source, then exposed one remaining Python module dependency: `tests/checks/normative_false_coverage.py` imported `normative_proof_state` through the former flat `tests/checks/` module search path.

A complete audit of all 55 checks still in the flat root found no other direct Python import of the ten governance modules moved in 4C1a. The correction keeps `normative_false_coverage.py` in the flat root for its planned 4C1b move, but resolves the directories for both `normative_proof_state.py` and `normative_traceability.py` through `check_file(...)` before importing them. This preserves proof/evidence semantics and prepares the file for the subsequent evidence move without introducing duplicate modules or compatibility packages.

Failed Static #828 remains part of the audit trail.

### Phase 4C1a final receipt

Phase 4C1a is complete. PR #409 merged as `2ad4273605d8ab4d7764d698f8515625dd49ad67` after Static Contract #829 and Linux Integration #713 passed. Static #826/#827/#828 remain retained as legitimate migration evidence and superseded Linux #710/#711/#712 remain in workflow history. Post-merge `main` passed Static Contract #830 and Linux Release Check #264 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The ten governance/source-authority checks now exist only under `tests/checks/governance/`. The flat `tests/checks/` root contains exactly 55 Python checks, while total check/integration identities and zero-orphan invariants remain unchanged.

### Phase 4C1b execution map

Issue #408 moves exactly ten evidence/coverage/contract-integrity checks into `tests/checks/evidence/`:

- `normative_atomic_contract.py`;
- `normative_atomicity.py`;
- `normative_coverage.py`;
- `normative_cross_surface.py`;
- `normative_evidence_contribution.py`;
- `normative_false_coverage.py`;
- `normative_full_contract.py`;
- `normative_traceability.py`;
- `normative_validator_contract.py`;
- `test_surface_integrity.py`.

All ten replace fixed-depth repository-root discovery with the canonical tests-root bootstrap. Intra-family imports of traceability/cross-surface use the current script directory rather than the retired flat `tests/checks/` directory. `normative_false_coverage.py` keeps its resolver-backed dependency directories for governance proof state and evidence traceability, preserving cross-namespace import semantics.

The moved-check map gains the ten evidence basenames and canonical paths. Flat compatibility copies and stale flat paths remain fail-closed. Executable mode `100755` is preserved for `normative_full_contract.py`, `normative_validator_contract.py` and `test_surface_integrity.py`; the other seven remain `100644`. Expected flat-root check count after this slice is 45. No normative values, proof/evidence ownership, runtime/public API, release metadata or published artifact behavior changes.

### Phase 4C1b final receipt

Phase 4C1b is complete. PR #410 merged as `0077a794ee8262860f211c37a82c715e0a410cef` after Static Contract #831 and Linux Integration #714 passed. Post-merge `main` passed Static Contract #832 and Linux Release Check #265 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The ten evidence/coverage/contract-integrity checks now exist only under `tests/checks/evidence/`. Together with the certified governance slice, Phase 4C1 owns 20 nested checks and the flat `tests/checks/` root contains exactly 45 Python checks. Child issues #407/#408 and umbrella #391 are closed.

### Phase 4C2 execution map

Issue #392 moves exactly 13 frontmatter checks/helpers into `tests/checks/frontmatter/`. `frontmatter_definition_alignment.py` is already repository-depth independent and moves byte-identically. The other twelve replace fixed `Path(__file__).resolve().parents[2]` discovery with the canonical tests-root bootstrap while retaining their existing `ROOT/tools` helper dependency.

Fourteen known active consumers carry fifteen retired flat-path occurrences: thirteen frontmatter integration scripts account for fourteen occurrences and `tests/checks/repository/engineering_language.py` accounts for the title-page contract occurrence. All are updated atomically while preserving their existing semantic assertions and Git modes.

The moved-check contract adds thirteen frontmatter basenames mapped to `tests/checks/frontmatter/`. Because one moved helper intentionally has no repository-root dependency, the contract explicitly records it in a bounded `root_independent_moved_checks` set instead of forcing an artificial `ROOT` import. Flat compatibility copies, fixed-depth nested checks and stale flat paths remain fail-closed.

Suite selection requires no `PATH_RULES` edit because movable check paths normalize by basename before matching. Expected flat-root count after this slice is exactly 32; total check/integration identity remains 84/86. No normative value, PDF tolerance, runtime/public API, release metadata or published artifact behavior changes.

### Phase 4C2 final receipt

Phase 4C2 is complete. PR #412 merged as `a82a3fbe3ce388ee4a20e94490e452921e5f95e1` after Static Contract #833 and Linux Integration #715 passed. Post-merge `main` passed Static Contract #834 and Linux Release Check #266 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The thirteen frontmatter checks/helpers now exist only under `tests/checks/frontmatter/`, all preserve mode `100644`, and the flat `tests/checks/` root contains exactly 32 Python checks. The total 84-check / 86-integration identity and zero-orphan invariants remain unchanged.

### Phase 4C3 execution map

Issue #393 moves exactly nine citation/reference checks into `tests/checks/citations/`:

- `normative_apud_presentation.py`;
- `normative_direct_citation_source.py`;
- `normative_indirect_citation_source.py`;
- `normative_long_quotation.py`;
- `normative_long_quote_reduced_size.py`;
- `normative_reference_layout.py`;
- `normative_reference_semantics.py`;
- `normative_short_direct_citation.py`;
- `normative_ufc_citation_system.py`.

All nine preserve mode `100644`, replace fixed repository-depth discovery with the canonical tests-root bootstrap and retain the existing `ROOT/tools` helper dependency. Eight known integration consumers follow the new paths; `long-quotation-evidence.sh` updates both the main long-quotation and reduced-size check invocations. Consumer executable bits are preserved exactly.

The moved-check contract gains the nine citation basenames mapped to `tests/checks/citations/`. Flat compatibility copies, fixed-depth nested checks and stale flat references remain fail-closed. Suite selection requires no `PATH_RULES` edit because movable check paths normalize by basename before matching. Expected flat-root count after this slice is exactly 23. No citation/reference normative value, evidence semantics, runtime/public API, release metadata or published artifact behavior changes.

### Phase 4C3 validation incident

Initial Static Contract #835 failed on PR #413 after the citation/reference checks moved because the fail-closed moved-check guard found one active negative-scenario consumer still naming the retired flat path: `standards/scenarios/negative/negative-paths.json` referenced `tests/checks/normative_short_direct_citation.py`.

That path is part of a controlled negative assertion rather than incidental documentation. The scenario is updated to `tests/checks/citations/normative_short_direct_citation.py` while preserving the same negative-test semantics. The failed run is retained as audit evidence; no compatibility copy or stale-path exemption is introduced. Fresh Static and Linux Integration gates are required before merge.

### Phase 4C3 final receipt

Phase 4C3 is complete. PR #413 merged as `cecf6b78a4408b5df94cf3b9a9ba390d5f57a19d` after Static Contract #836 and Linux Integration #717 passed. Initial Static #835 is retained as evidence of one controlled negative-scenario stale path; Linux #716 is retained as a superseded concurrency-cancelled run. Post-merge `main` passed Static Contract #837 and Linux Release Check #267 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The nine citation/reference checks now exist only under `tests/checks/citations/`. The flat `tests/checks/` root contains exactly 23 Python checks, while total check/integration identities and zero-orphan invariants remain unchanged.

### Phase 4C4a execution map

Issue #414 moves exactly seven layout/typography/PDF-A checks into `tests/checks/layout/`:

- `normative_body_paragraph.py`;
- `normative_footnote_separator.py`;
- `normative_footnote_text.py`;
- `normative_page_margins.py`;
- `normative_pagination_geometry.py`;
- `normative_pdfa.py`;
- `normative_typography.py`.

Six checks preserve mode `100644`, replace fixed repository-depth discovery with the canonical tests-root bootstrap and retain their existing `ROOT/tools` helper dependency. `normative_pdfa.py` preserves executable mode `100755` and uses only the canonical ROOT bootstrap because it has no tools-module dependency.

Seven known integration consumers follow the new canonical paths one-to-one. `pdfa.sh` preserves mode `100755`; the other six consumer scripts preserve mode `100644`. The moved-check map gains seven layout basenames mapped to `tests/checks/layout/`. Flat compatibility copies, fixed-depth nested checks and stale retired paths remain fail-closed. Suite inference requires no `PATH_RULES` edit because movable check paths normalize by basename before matching.

Expected flat-root count after this slice is exactly 16. No normative value, geometry tolerance, PDF/A behavior, runtime/public API, release metadata or published artifact changes.

### Phase 4C4a validation incident

Initial Static Contract #838 failed on PR #416 after the layout/typography/PDF-A checks moved because the fail-closed moved-check guard found three controlled negative-scenario paths in `standards/scenarios/negative/negative-paths.json` that still named retired flat checks:

- `tests/checks/normative_page_margins.py`;
- `tests/checks/normative_pdfa.py`;
- `tests/checks/normative_typography.py`.

These are active negative-path assertions rather than incidental text. Each path is updated to its canonical `tests/checks/layout/` location while preserving the same negative-test semantics. The failed run is retained as audit evidence. No compatibility copy or stale-path exemption is added. Fresh Static and Linux Integration gates are required before merge.

### Phase 4C4a final receipt

Phase 4C4a is complete. PR #416 merged as `2f9138bc674d105528caa5d1dcbc7e113260967e` after Static Contract #839 and Linux Integration #719 passed. Initial Static #838 is retained as evidence of three controlled negative-scenario stale paths; Linux #718 is retained as a superseded concurrency-cancelled run. Post-merge `main` passed Static Contract #840 and Linux Release Check #268 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The seven layout/typography/PDF-A checks now exist only under `tests/checks/layout/`. The flat `tests/checks/` root contains exactly 16 Python checks, while total check/integration identities and zero-orphan invariants remain unchanged.

### Phase 4C4b execution map

Issue #415 moves exactly seven section hierarchy/spacing checks into `tests/checks/sections/`:

- `normative_section_hierarchy.py`;
- `normative_section_indicator.py`;
- `normative_section_multiline_hanging.py`;
- `normative_section_primary_after_spacing.py`;
- `normative_section_primary_recto_duplex.py`;
- `normative_section_unnumbered_centered.py`;
- `normative_subsection_spacing.py`.

All seven preserve mode `100644`, replace fixed repository-depth discovery with the canonical tests-root bootstrap and retain their existing `ROOT/tools` helper dependency. Seven one-to-one integration consumers follow the new canonical paths while preserving mode `100644`.

The moved-check map gains the seven section basenames mapped to `tests/checks/sections/`. Flat compatibility copies, fixed-depth nested checks and stale retired paths remain fail-closed. Suite inference requires no `PATH_RULES` edit because movable check paths normalize by basename before matching.

Expected flat-root count after this slice is exactly 9. No section hierarchy, spacing, recto/duplex or indicator normative value, evidence tolerance, runtime/public API, release metadata or published artifact behavior changes.

### Phase 4C4b final receipt

Phase 4C4b is complete. PR #417 merged as `f8adcc06b42453217157e128a8c0db98be588366` after Static Contract #841 and Linux Integration #720 passed. Post-merge `main` passed Static Contract #842 and Linux Release Check #269 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The seven section hierarchy/spacing checks now exist only under `tests/checks/sections/`. Together with 4C4a, the 14 layout/section checks are fully nested and umbrella #394 is closed. The flat `tests/checks/` root contains exactly 9 Python checks; total 84-check / 86-integration identity and zero-orphan invariants remain unchanged.

### Phase 4C5 execution map

Issue #395 moves exactly six academic-object checks into `tests/checks/objects/`:

- `normative_equation_display.py`;
- `normative_illustration.py`;
- `normative_objects_scope.py`;
- `normative_table_ibge_vector.py`;
- `normative_table_typography.py`;
- `normative_vector_rule_validation.py`.

All six preserve mode `100644`, replace fixed repository-depth discovery with the canonical tests-root bootstrap and retain their existing `ROOT/tools` helper dependency. Five known integration consumers follow the new canonical paths: `illustration-evidence.sh`, `object-geometry.sh`, `table-ibge-vector-evidence.sh`, `table-typography-equation-evidence.sh` and `vector-rule-validation.sh`. Their existing Git modes are preserved.

The controlled negative scenario path for `normative_table_ibge_vector.py` follows the new objects namespace without changing negative-test semantics. The moved-check map gains six object basenames mapped to `tests/checks/objects/`. Flat compatibility copies, fixed-depth nested checks and stale retired paths remain fail-closed.

Expected flat-root count after this slice is exactly 3. No equation/illustration/table/vector normative value, measurement tolerance, runtime/public API, release metadata or published artifact behavior changes.

### Phase 4C5 validation incident

Initial Static Contract #843 failed on PR #418 after the academic-object checks moved because the fail-closed moved-check guard found one active validation-extension path still naming the retired flat check: `standards/evidence/vector-rule-validation-extension.json` referenced `tests/checks/normative_vector_rule_validation.py`.

The extension is controlled validation metadata rather than incidental documentation. Its path is updated to `tests/checks/objects/normative_vector_rule_validation.py` while preserving the same additive vector-rule calibration policy and proof-state semantics. The failed run is retained as audit evidence. No compatibility copy or stale-path exemption is added. Fresh Static and Linux Integration gates are required before merge.

### Phase 4C5 final status

PR #418 merged as `404ac70fc81be6dbbefcd5ea4d84f2e43ef81d3f`; Static #845 and Linux Release Check #270 passed. The six academic-object checks live under `tests/checks/objects/`, leaving exactly three flat-root checks.

### Phase 4C6 — final check taxonomy

Issue #396 moves the final three flat-root checks to their semantic destinations:

- `normative_appendix_annex.py` and `normative_index_glossary.py` -> `tests/checks/backmatter/`;
- `normative_research_project_structure.py` -> `tests/checks/profiles/`.

The three checks adopt the canonical tests-root bootstrap while preserving existing `ROOT/tools` behavior and mode `100644`. The three known integration consumers and the controlled research-project negative paths follow the new locations. The moved-check contract adds two backmatter identities and the research-project profile identity.

Target result: zero Python checks directly under `tests/checks/`, while all 84 check identities remain recursively discoverable. This is a taxonomy/path-only change; normal required PR checks are sufficient under the current pragmatic maintenance policy.

### Phase 4C6 final receipt

Phase 4C6 is complete. PR #420 merged as `7a5cd14d8e7a6e0b024a1b5c64321bbf0007e319` after Static Contract #848 and Linux Integration #724 passed. Post-merge `main` passed Static Contract #849 and Linux Release Check #271 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The final three flat checks now exist only under `tests/checks/backmatter/` and `tests/checks/profiles/`. The flat `tests/checks/` root contains zero Python checks, while all 84 check identities remain recursively discoverable with no compatibility copies. Issue #396 is closed and the check-taxonomy portion of Phase 4 is complete.

### Phase 4D execution map

Issue #397 moves exactly ten non-domain integration identities:

- `tests/integration/core/`: `negative-paths.sh`, `normative-complement.sh`, `reference-guide-contract.sh`;
- `tests/integration/distribution/`: `distribution-bundles.sh`, `overleaf-stable.sh`;
- `tests/integration/release/`: `release-reference-reproducibility.sh`, `release-review-pairs.sh`;
- `tests/integration/validator/`: `pdf-validation-core.sh`, `pdf-validator.sh`, `web-lite-e2e.py`.

Six files move byte-identically. `web-lite-e2e.py` adopts the canonical tests-root bootstrap. `overleaf-stable.sh` and both release scripts replace fixed script-depth repository-root derivation with a self-contained POSIX upward sentinel search. `release-reference-reproducibility.sh` follows the moved PDF validator path.

Operational consumers follow the new locations in `Makefile`, `tools/ci/run-web-lite-e2e.sh`, `tools/ci/certify-ctan-package.sh` and the repository path/suite contracts. The Overleaf standalone test-surface policy changes path only; classification semantics remain unchanged.

The path-resolution contract introduces explicit moved-integration canonical paths, flat-copy rejection, fixed-depth rejection for nested Python integrations, and active stale-flat-integration scanning. `tests/integration_suites.py` and `tests/checks/repository/linux_integration_suites.py` are controlled exclusions from that text scan because they intentionally store normalized flat identities; their self-tests and real helper-content assertions remain fail-closed.

Target result: 10 nested integrations + 76 flat integrations = 86 identities, with original Git modes preserved. No runtime/public API/normative/release-asset behavior changes.
