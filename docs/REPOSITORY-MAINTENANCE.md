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
| 0 | v3.0.4 CTAN external closeout | complete — PR #425 merged as `88503ea5ce3fae2aa614a17437225ccd86d08b9d`; #356 closed |
| 1 | metadata consistency and anti-drift | complete — PR #360 merged as `496f893627b1d2211161b8408e44026a2b66b157` |
| 2 | recursive discovery and path-decoupling preparation | complete — PR #361 merged as `603c06c5d347d5857d5b5661d489a7c3d6e80211` |
| 3 | `standards/` taxonomy | complete — PR #377 merged as `f36797cbc34715e9ed9b82af9ddbd8d8d299fd88`; issue #362 closeout |
| 4 | `tests/` taxonomy | complete — issues #375/#400; 84 checks nested, 86 integrations nested, `tests/documents/` intentionally flat after #399 evaluation |
| 5 | supporting repository structure (`release/`, CTAN example, tools, examples) | complete — #430; 5A release ownership complete, 5B tools and 5C template/examples retained by documented no-move decisions |
| 6 | self-contained Web/Lite hardening | complete — #437; local PDF.js + network-denied/CSP certification complete via #439/#441 |
| 7 | cross-platform portability smoke coverage | in progress — #442; 7A Windows certified, 7B macOS ARM64 active under #445 |
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

### Phase 4D validation incident

Initial Static Contract #850 failed on PR #421 after the non-domain integration move because `tests/checks/repository/canonical_identity.py` still keyed its controlled legacy-identity exemption to the retired path `tests/integration/distribution-bundles.sh`.

The integration intentionally contains a negative assertion for the historical pre-v3 class identity; the exemption key follows the moved file to `tests/integration/distribution/distribution-bundles.sh` without changing that assertion. The failed run is retained as audit evidence. No compatibility copy or broad legacy exemption is introduced. Fresh Static and Linux Integration gates are required before merge.

### Phase 4D second validation incident

Corrected-head validation exposed two additional residuals. Static Contract #851 failed because the Phase 4D incident receipt itself reintroduced the retired pre-v3 class-identity token into an active documentation surface audited by `canonical_identity.py`. The receipt is reworded generically; no new documentation exemption is added.

Linux Integration #726 and Linux Release Check #273 both failed check `[03/38] Reference document` because `tests/integration/reference-document.sh` still invoked the retired flat path `tests/integration/reference-guide-contract.sh` after that integration moved to `tests/integration/core/reference-guide-contract.sh`. The operational call follows the moved integration. The failed runs remain audit evidence and the generic stale-integration scanner remains the exhaustive backstop for any further active consumer.

Fresh Static, Linux Integration and Linux Release gates are required before merge.

### Phase 4D third validation incident

Static Contract #852 advanced past the earlier canonical-identity and reference-document corrections and exposed three remaining active stale integration references. `standards/scenarios/negative/negative-paths.json` still named the retired flat paths for `negative-paths.sh` and `pdf-validator.sh`, and `validator/README.md` still documented the retired flat path for `web-lite-e2e.py`.

These are path-only consumer updates: the controlled negative-scenario inventory continues to reference the same validation mechanisms, and the validator documentation continues to describe the same Web/Lite E2E command. The references follow their canonical `tests/integration/core/` and `tests/integration/validator/` locations. Static #852 is retained as audit evidence; no stale-path exemption or compatibility copy is added. Fresh Static, Linux Integration and Linux Release gates are required before merge.

### Phase 4D final receipt

Phase 4D is complete. PR #421 merged as `de75e4fd729a5e83776988695b148ea56bbb3ac4` after Static Contract #853, Linux Integration #728 and Linux Release Check #275 passed on the final PR head. Earlier Static #850/#851/#852, Linux Integration #726 and Linux Release #273 remain preserved as evidence of legitimate stale-path, documentation-token and operational-consumer regressions discovered and corrected during the move.

Post-merge `main` passed Static Contract #854, Linux Integration #729, Linux Release Check #276 and Pages #7. Ten non-domain integrations now live under `tests/integration/core/`, `distribution/`, `release/` and `validator/`, while all 86 integration basenames remain recursively unique and no compatibility copies remain.

### Phase 4E1 execution map

Issue #398 begins domain integration taxonomy with the smallest family. Exactly four integrations move to `tests/integration/backmatter/`:

- `appendix-annex-final-pdf-evidence.sh` (mode `100644`);
- `backmatter.sh` (mode `100755`);
- `duplex-backmatter.sh` (mode `100755`);
- `index-glossary-final-pdf-evidence.sh` (mode `100644`).

None of the four derives repository root from script depth, so no bootstrap/root-search change is required. `backmatter.sh` follows the two moved evidence-script paths atomically; document and fixture paths remain unchanged.

The existing `moved_integration_paths` authority gains the four backmatter basenames and canonical paths. Flat compatibility copies and active stale flat integration references remain fail-closed through the same Phase 4D scanner. Suite inference needs no `PATH_RULES` edit because movable integration paths are normalized by basename before matching.

Expected topology after this slice: 14 nested integrations + 72 flat integrations = 86 total identities. No validation semantics, runtime/public API, normative meaning, release metadata or published artifact behavior changes.

### Phase 4E1 final receipt

Phase 4E1 is complete. PR #422 merged as `a657197903c9d642b3bf42a82c249e0d2fce9479` after Static Contract #855 and Linux Integration #730 passed. Post-merge `main` passed Static Contract #856 and Linux Release Check #277 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Final certification retained canonical class identity, checksums, archive integrity, source rebuild identity, cross-bundle equality and CTAN pkgcheck success.

The four backmatter integrations now live only under `tests/integration/backmatter/`. The integration topology is 14 nested + 72 flat = 86 identities, with modes preserved exactly and no compatibility copies.

### Phase 4E2 execution map

Phase 4E2 moves exactly 21 layout/geometry/sections/fonts integrations into `tests/integration/layout/`. Six files preserve executable mode `100755` and fifteen preserve mode `100644`.

Only `font-poc.sh` derives repository root from script depth. It adopts the already-certified POSIX upward sentinel search for both `abntexto-ufc.cls` and `tests/path_resolver.py`; the other twenty move without root-bootstrap changes. The path-resolution contract adds `font-poc.sh` to the existing root-sensitive shell guard.

Known intra-family and cross-family consumers follow the canonical layout paths atomically: aggregate layout and geometry scripts, font/PDF-A helpers, reference-document, duplex frontmatter, object/code typography consumers and profile/article PDF-A consumers. Suite inference requires no PATH_RULE rewrite because integration identities normalize by basename before matching.

The existing `moved_integration_paths` authority gains all 21 layout basenames -> `tests/integration/layout/<basename>`; flat compatibility copies and stale retired paths remain fail-closed through the same scanner. Target topology after this slice is 35 nested + 51 flat = 86 identities. No validation semantics, runtime/public API, normative meaning, release metadata or published artifact behavior changes.

### Phase 4E2 validation incident

Initial validation on PR #423 head `b3eae960e83d92c7c73304d83cfbd59a8a3dee29` failed in both required gates.

Static Contract #857 failed because the fail-closed stale-integration scanner found active flat references to moved layout integrations in `docs/WINDOWS-FONT-SUPPORT.md`, `standards/evidence/evidence-registry.json`, `standards/evidence/test-surface-policy.json`, `standards/scenarios/negative/negative-paths.json`, `tests/integration/distribution/overleaf-stable.sh`, `tests/integration/release/release-reference-reproducibility.sh` and `tests/integration/release/release-review-pairs.sh`.

Linux Integration #731 exposed the operational effect of the same stale paths. Validator traceability could not find the moved `font-config.sh` evidence target, and controlled negative paths for page margins and typography could not execute their positive baselines. The complete run ended with `SCOPE=complete PASS=35 FAIL=2 SKIP=1`.

The failed runs are retained as audit evidence. Each active consumer follows its canonical `tests/integration/layout/` path. No compatibility copy, stale-path exemption or guard weakening is introduced. Fresh Static and Linux Integration gates are required before merge.

### Phase 4E2 final receipt

Phase 4E2 is complete. PR #423 merged as `9bfb446b0ddbdc5059fa25b6e143e3a1c22c3406` after Static Contract #858 and Linux Integration #732 passed on corrected head `edadf1108b45993f0a318de60b3393cdd0264428`. Initial Static #857 and Linux Integration #731 remain preserved as evidence of active stale layout-integration consumers discovered by the fail-closed contracts.

Post-merge `main` passed Static Contract #859 and Linux Release Check #278. The 21 layout/geometry/sections/fonts integrations now live only under `tests/integration/layout/`; topology is 35 nested + 51 flat = 86 integration identities, with original Git modes preserved and no compatibility copies.

### Phase 4E3 execution map

Issue #398 next moves exactly 14 citation/reference/bibliography integrations to `tests/integration/citations/`:

- `apud-evidence.sh`;
- `bibliography.sh`;
- `capes-guidance.sh`;
- `direct-citation-source-evidence.sh`;
- `indirect-citation-source-evidence.sh`;
- `long-quotation-citation-evidence.sh`;
- `long-quotation-evidence.sh`;
- `reference-corpus.sh`;
- `reference-document.sh`;
- `reference-layout-evidence.sh`;
- `reference-spacing.sh`;
- `references-6023.sh`;
- `short-direct-citation-evidence.sh`;
- `ufc-citation-system-evidence.sh`.

Exact Git modes are preserved: `direct-citation-source-evidence.sh`, `long-quotation-citation-evidence.sh`, `long-quotation-evidence.sh`, `reference-document.sh` and `references-6023.sh` remain executable; the other nine remain mode `100644`.

Only `capes-guidance.sh` and `reference-corpus.sh` derive repository root from fixed script depth. They adopt the already-certified POSIX upward sentinel search for both `abntexto-ufc.cls` and `tests/path_resolver.py`, and the root-sensitive shell contract gains both basenames.

Intra-family callers follow the new namespace atomically: `bibliography.sh` follows six citation integrations, `long-quotation-evidence.sh` follows `long-quotation-citation-evidence.sh`, and `reference-spacing.sh` follows `reference-layout-evidence.sh`. `reference-document.sh` keeps its already-canonical cross-family calls to `core/reference-guide-contract.sh` and `layout/font-embedding.sh`.

Known external consumers also follow the canonical paths: `frontmatter.sh` and `standards/evidence/evidence-registry.json` follow `citations/capes-guidance.sh`; `standards/scenarios/negative/negative-paths.json` follows `citations/short-direct-citation-evidence.sh`. No stale-path exemption or compatibility copy is introduced.

The existing `moved_integration_paths` authority gains exactly these 14 basenames. Suite inference remains basename-normalized, so no `PATH_RULES` rewrite is required. Expected topology after 4E3 is 49 nested + 37 flat = 86 identities. No runtime/public API/normative meaning/release metadata/published artifact behavior changes.

### Phase 4E3 validation incident

Initial Static Contract #860 failed on PR #424 head `c844e93f42034e1596623d1f06236b5c64213887` because the fail-closed stale-integration scanner found two active consumers that still named retired flat citation integrations:

- `docs/UFC-LIBRARIAN-REVIEW.md` still referenced `tests/integration/references-6023.sh` in the item-33 evidence narrative and table;
- `tests/integration/core/normative-complement.sh` still invoked `tests/integration/long-quotation-evidence.sh`.

Both consumers follow the canonical `tests/integration/citations/` locations without changing librarian evidence meaning or normative-complement behavior. Static #860 is retained as audit evidence. No compatibility copy, stale-path exemption or scanner weakening is introduced; fresh required gates must pass before merge.



### Phase 4E3 final receipt

Phase 4E3 is complete. PR #424 merged as `4070e1a6b286738c208a107309b67cb3239fc6db` after final PR head `bbf4b915eae6161c9f9ef1713434c09deb4538a5` passed Static Contract #862 and Linux Integration #735. Initial Static #860 is retained as evidence of two active stale citation-integration consumers; correction `2a647e9e85c1280147c7be441893f16fb24af415` updated only those consumers without compatibility copies or scanner exemptions.

Post-merge `main` passed Static Contract #863 and Linux Release Check #279 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`. Distribution/public bundle integrity, canonical-reference reproducibility, CTAN pkgcheck and seven-profile review-pair certification all passed. The final integration topology is 49 nested + 37 flat = 86 identities, with exact Git modes preserved and no compatibility copies.

### Phase 0 CTAN publication reconciliation

The official CTAN-ann update dated 2026-09-22 confirms publication of `abntexto-ufc` version 3.0.4. Issue #356 owns the bounded repository-control reconciliation from the stale current-state marker `SUBMITTED/PENDING` to the final external receipt `PUBLISHED/ACCEPTED`.

This reconciliation changes only current control metadata and its fail-closed governance assertions. It preserves the published source SHA `7e176fd5472925b519d469a9a756330f4851f0b3`, annotated tag, GitHub Release ID `392476983`, release assets, historical receipts, submitted CTAN archive and SHA-256 `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec` exactly.


### Phase 0 final receipt

The v3.0.4 external CTAN closeout is complete. PR #425 merged as `88503ea5ce3fae2aa614a17437225ccd86d08b9d` after Static Contract #864, Linux Integration #736 and Linux Release Check #280 passed on its final head. Post-merge `main` passed Static Contract #865, Linux Integration #737 and Linux Release Check #281 on the exact merge SHA. Issue #356 is closed.

This reconciliation changed only current repository-control metadata from the prior submitted/pending state to the externally confirmed `PUBLISHED/ACCEPTED` state dated 2026-09-22. Published source, annotated tag, GitHub Release assets, exact CTAN archive bytes/checksum and historical receipts remain immutable.

### Phase 4E4 execution map

Phase 4E4 moves exactly 14 frontmatter integrations into `tests/integration/frontmatter/`: `duplex-frontmatter.sh`, twelve `frontmatter-*-evidence/negative.sh` scripts, and the aggregate `frontmatter.sh`.

Exact Git modes are preserved: `frontmatter-cover-evidence.sh`, `frontmatter-title-page-evidence.sh` and `frontmatter.sh` remain executable mode `100755`; the other eleven remain mode `100644`. None of the fourteen derives repository root from script depth, so no root-bootstrap change is required.

`frontmatter.sh` follows its twelve intra-family calls into the new namespace while retaining the canonical cross-family `tests/integration/citations/capes-guidance.sh` call. `duplex-frontmatter.sh` retains its canonical cross-family `tests/integration/layout/section-primary-recto-duplex-evidence.sh` call. The existing `moved_integration_paths` authority gains all fourteen frontmatter basenames, with no compatibility copies.

Expected topology after this slice is 63 nested + 23 flat = 86 integration identities. Suite inference remains basename-normalized, so no PATH_RULE rewrite is required. No validation semantics, runtime/public API, normative meaning, release metadata or published artifact behavior changes.


### Phase 4E4 validation incident

Initial Static Contract #866 failed on PR #426 head `aefc16d9068a2b14113132f64bcb66152488a9a5` because the fail-closed stale-integration scanner found one active consumer in `tests/checks/repository/engineering_language.py` still naming the retired flat `frontmatter-approval-evidence.sh` path.

The engineering-language machine-source inventory follows the canonical `tests/integration/frontmatter/frontmatter-approval-evidence.sh` location without changing language-policy semantics or its controlled source set. Static #866 remains audit evidence. No compatibility copy, stale-path exemption or scanner weakening is introduced; fresh required gates must pass before merge.


### Phase 4E4 final receipt

Phase 4E4 is complete. PR #426 merged as `a93b329258b53c616824cb41f7ffaf35330a37b4` after final head `9efcce31ca67cd0033c387d58117203b055beb3c` passed Static Contract #867 and Linux Integration #739. Initial Static #866 remains preserved as evidence of one active stale `engineering_language.py` consumer; the corrected head updated only that path without compatibility copies or scanner exemptions.

Post-merge `main` passed Static Contract #868 and Linux Release Check #282. The fourteen frontmatter integrations now live only under `tests/integration/frontmatter/`; topology is 63 nested + 23 flat = 86 integration identities, with exact Git modes preserved and no compatibility copies.

### Phase 4E5 execution map

Phase 4E5 moves exactly eleven academic-object integrations into `tests/integration/objects/`: `algorithm-numbering.sh`, `code-typography.sh`, `documentary-source.sh`, `illustration-evidence.sh`, `minted.sh`, `object-geometry.sh`, `object.sh`, `table-ibge-vector-evidence.sh`, `table-ibge.sh`, `table-typography-equation-evidence.sh` and `vector-rule-validation.sh`.

Exact Git modes are preserved: nine scripts remain executable mode `100755`; `illustration-evidence.sh` and `object.sh` remain mode `100644`. None derives repository root from script depth, so no root-bootstrap change is required.

`object-geometry.sh` follows its three object-family evidence calls into the new namespace, and `table-ibge-vector-evidence.sh` follows `vector-rule-validation.sh`. Existing cross-family calls from `code-typography.sh`, `minted.sh` and `table-ibge.sh` retain the canonical `tests/integration/layout/font-embedding.sh` path.

The existing `moved_integration_paths` authority gains all eleven object basenames. Flat compatibility copies and active stale flat references remain fail-closed. Suite inference remains basename-normalized, so no PATH_RULE rewrite is required. Expected topology after 4E5 is 74 nested + 12 flat = 86 identities. No validation semantics, runtime/public API, normative meaning, release metadata or published artifact behavior changes.


### Phase 4E5 validation incident

Initial Static Contract #869 failed on PR #427 head `6f1abee6d925650f3ffeb6b0f94222c5ef8c595e` because the fail-closed stale-integration scanner found two active consumers still naming retired flat object integrations:

- `docs/UFC-LIBRARIAN-REVIEW.md` referenced the retired flat `code-typography.sh` path;
- `standards/scenarios/negative/negative-paths.json` referenced the retired flat `table-ibge-vector-evidence.sh` path.

Both consumers follow the canonical `tests/integration/objects/` locations without changing librarian-review evidence meaning or controlled negative-scenario semantics. Static #869 remains audit evidence. No compatibility copy, stale-path exemption or scanner weakening is introduced; fresh required gates must pass before merge.


### Phase 4E5 final receipt

Phase 4E5 is complete. PR #427 merged as `d0bca8f8891ffa95fbe1b8c9764189aeb0bddc18` after final head `b9474490486001acefecf0e2aefcb11397cd9ef9` passed Static Contract #870 and Linux Integration #741. Initial Static #869 remains preserved as evidence of two active stale object-integration consumers; the corrected head updated only those paths without compatibility copies or scanner exemptions.

Post-merge `main` passed Static Contract #871 and Linux Release Check #283. The eleven academic-object integrations now live only under `tests/integration/objects/`; topology is 74 nested + 12 flat = 86 integration identities, with exact Git modes preserved and no compatibility copies.

### Phase 4E6 execution map

Phase 4E6 moves the final twelve flat profiles/article integrations into `tests/integration/profiles/`: `build-path.sh`, `catalog-card.sh`, `multivolume.sh`, `profile-matrix.sh`, `profile-pdfa.sh`, `research-project.sh`, `scientific-article-body.sh`, `scientific-article-foreign-elements.sh`, `scientific-article-front-block.sh`, `scientific-article-pdfa.sh`, `scientific-article-profile.sh` and `scientific-article-recommendations.sh`.

Exact Git modes are preserved: nine scripts remain executable mode `100755`; `build-path.sh`, `profile-pdfa.sh` and `research-project.sh` remain mode `100644`. None derives repository root from script depth and there are no intra-family integration calls, so the move itself is byte-identical.

Existing cross-family calls remain unchanged and canonical: `profile-matrix.sh` uses `tests/integration/layout/font-embedding.sh`; `profile-pdfa.sh` uses `tests/integration/layout/pdfa.sh`; `scientific-article-pdfa.sh` uses both canonical layout helpers.

The existing `moved_integration_paths` authority gains all twelve profile/article basenames. Flat compatibility copies and active stale flat references remain fail-closed. Suite inference remains basename-normalized, so no PATH_RULE rewrite is required. Target topology after 4E6 is 86 nested + 0 flat = 86 identities. No validation semantics, runtime/public API, normative meaning, release metadata or published artifact behavior changes.


### Phase 4E6 validation incident

Initial Static Contract #872 failed on PR #428 head `303fd5796b67faa19673ab2679989c2770f27618` because the fail-closed stale-integration scanner found active consumers still naming retired flat profiles/article integrations.

The residuals were confined to current control/evidence surfaces: `Makefile`, `standards/evidence/article-evidence-map.json`, `standards/evidence/evidence-registry.json`, `standards/scenarios/negative/negative-paths.json`, `tests/checks/profiles/profile_matrix_contract.py` and `tests/checks/profiles/scientific_article_evidence_map.py`. Each reference follows the canonical `tests/integration/profiles/` location without changing build targets, evidence semantics, negative-scenario meaning or profile/article validation behavior.

Static #872 remains audit evidence. No compatibility copy, stale-path exemption or scanner weakening is introduced; fresh required gates must pass before merge.


### Phase 4E6 second validation incident

After the stale-path correction, Static Contract #873 failed on corrected head `f0b48b40fb3bcb7945d7a620532667437b4b5716` in `tests/checks/profiles/scientific_article_evidence_map.py`. The stale-path scanner itself passed, but the article evidence-map contract still recognized an article-specific executable owner by the retired flat prefix `tests/integration/scientific-article-`.

The contract remains fail-closed and equally strict after the taxonomy move: an article-specific owner must now reside exactly under `tests/integration/profiles/`, have a basename beginning `scientific-article-`, and retain the `.sh` suffix. This is a path-taxonomy adaptation only; evidence ownership, proof disposition, normativity and article validation semantics are unchanged.

Static #873 remains audit evidence. Fresh required gates must pass on the corrected head before merge.


### Phase 4E6 final receipt

Phase 4E6 is complete. PR #428 merged as `9bc2ecb87dba10867569da3b636cd49e2aefa711` after final head `0103af617db5fe7dec0c794856b36f41e1a619e8` passed Static Contract #874 and Linux Integration #744.

Two validation incidents remain preserved as audit evidence:
- Static #872 found active consumers still naming retired flat profiles/article integration paths;
- Static #873 found the scientific-article evidence-owner contract still recognizing owners through the retired flat path prefix.

Corrections `f0b48b40fb3bcb7945d7a620532667437b4b5716` and `0103af617db5fe7dec0c794856b36f41e1a619e8` updated only canonical taxonomy paths and strict owner recognition. No compatibility copies, scanner exemptions or semantic weakening were introduced.

Post-merge `main` passed Static Contract #875 and Linux Release Check #284 on the exact merge SHA. The final integration topology is 86 nested + 0 flat identities; the Python check topology is 84 nested + 0 flat identities.

### Phase 4F document-layout decision

Issue #399 evaluated whether the 90 controlled LaTeX documents under `tests/documents/` should follow the new nested check/integration taxonomy. The decision is intentionally **no move**.

The current descriptive basename families already provide semantic ownership: frontmatter (26), mainmatter (20), scientific article (10), academic objects (12), layout/font/PDF (10), backmatter (4), research project (2) and six cross-cutting/general documents.

A physical move would require updates to at least 72 direct code/test consumers already measured: 68 integration scripts and four Python checks, before counting metadata/documentation/CI surfaces. Suite inference already normalizes movable document paths by basename, and `test_surface_integrity.py` already treats `tests/documents/` as governed assets and fails closed on unreachable assets. Static #875 reports test assets 115/115 reachable with `asset_orphaned=0`.

Therefore nesting the documents would add migration/stale-path risk without adding correctness, coverage, evidence ownership or runtime/release capability. Descriptive basenames remain the intentional document taxonomy. A future physical move requires a new concrete ownership/navigation problem whose benefit materially exceeds the consumer churn.

### Phase 4 final certification

The finished tests taxonomy was certified on `main` `9bc2ecb87dba10867569da3b636cd49e2aefa711` before this documentation-only closeout sync.

Static Contract #875 proves:
- 84 check identities and 86 integration identities;
- recursive unique basename resolution with ambiguity fail-closed;
- flat Python check root = 0 and flat integration identity root = 0;
- retained test scripts 170/170 reachable, `orphaned=0`;
- test assets 115/115 reachable, `asset_orphaned=0`;
- technical controls 27/27 reachable, `technical_orphaned=0`;
- Linux suite inference keeps unknown-path fallback at `complete`.

Linux Release Check #284 proves the complete regression on the same SHA:
- `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- distribution/public bundles PASS;
- canonical reference reproducibility PASS;
- CTAN pkgcheck PASS;
- seven-profile release review-pair generation PASS;
- no runtime/public API/normative/release behavior or published v3.0.4 byte was changed solely by the taxonomy work.

Phase 4 is structurally complete. This closeout change only synchronizes durable maintenance documentation with the already-certified repository state; the next roadmap phase is Phase 5 supporting repository structure.


### Phase 5A execution map

Phase 5A establishes explicit release-source ownership without changing release content or published v3.0.4 artifacts.

The minimal CTAN example source moves byte-identically from `docs/ctan-example.tex` to `release/ctan/abntexto-ufc-example.tex`. This matches the existing `release/ctan/` ownership of the package README and manual and matches the archive member name already emitted by `tools/build-distribution-bundles.py`.

Active consumers are updated atomically:
- `tools/build-distribution-bundles.py` reads the canonical release source;
- `tests/checks/distribution/distribution_bundles.py` compares the generated archive example against the canonical release source.

Both builder and distribution contract reject a compatibility copy at the retired `docs/ctan-example.tex` path. The integration distribution gate continues to validate the same archive member `abntexto-ufc/abntexto-ufc-example.tex`; no generated member name changes.

A new `release/README.md` documents ownership of `release/ctan/`, `release/history/v3/`, current release control and stable build entry points. Historical references under `docs/history/v3/` remain untouched because they describe past repository state.

This slice deliberately does not edit the already-published v3.0.4 CTAN README/manual content, tags, GitHub Release assets, submitted archive or historical receipts.


### Phase 5A validation incident

Initial Static Contract #878 failed on PR #432 head `c04b0efd8276837a91ecf93c065a3aaa949a8655` because the new release ownership prose referenced unversioned history roots. The repository contract intentionally permits only the controlled v3 history namespaces and rejects generic history-root references in active documentation.

The correction changes documentation wording only, naming `release/history/v3/` and `docs/history/v3/` explicitly. No history policy, exemption or scan rule is weakened. Static #878 remains preserved as audit evidence; fresh required gates must pass before merge.


### Phase 5A second validation incident

Static Contract #879 failed on corrected head `60e7e7d39d2fa393b1291a0a117e17c96d477d91` because the first validation-incident receipt itself repeated the forbidden unversioned history-root literals. The repository contract therefore continued to fail exactly as designed.

The receipt now describes those roots without reproducing the forbidden literals and names only the approved `docs/history/v3/` and `release/history/v3/` namespaces. No policy or scanner exception is added. Static #879 remains preserved as audit evidence; fresh required gates are required before merge.


### Phase 5A final receipt

Phase 5A is complete. PR #432 merged as `ff7537cbc2d9f9f41a25a6c86e3345401e74397d` from final head `cdf1e0de0e1fb38374153a3d344618f176481dca`.

The CTAN example source moved byte-identically from its retired documentation path to `release/ctan/abntexto-ufc-example.tex`; the destination blob retains SHA `64ea4bc3d1504d4b6496fb6f2f4859b7e4b1e8c0`. The distribution builder and distribution contract now consume the canonical release source and both reject a compatibility copy at the retired path. The generated archive member remains `abntexto-ufc/abntexto-ufc-example.tex`.

Two Static incidents are preserved:
- #878 rejected active documentation that named generic unversioned history roots;
- #879 rejected the first incident receipt because it repeated the same forbidden generic literals.

Both corrections were wording-only and retained the approved `docs/history/v3/` and `release/history/v3/` namespaces without weakening repository policy.

Final PR gates Static #880 + Linux Integration #748 passed. Post-merge `main` passed Static #881 and Linux Release #285 with `SCOPE=complete PASS=38 FAIL=0 SKIP=0`; distribution bundles, canonical-reference reproducibility, CTAN pkgcheck and seven-profile review-pair generation all passed. Published v3.0.4 source/tag/GitHub Release assets/submitted CTAN archive and historical receipts were not rewritten.

### Phase 5B tools-ownership decision

Issue #433 evaluates `tools/` organization after 5A certification. The decision is intentionally **no physical move**.

The current `tools/ci/` namespace already cleanly owns workflow-specific helpers. The root `tools/` surface contains stable build/release/CLI entry points plus shared repository Python modules. A fresh scan of all 84 Python checks found **77/84** directly dependent on the root tools surface or named tool entry points. Makefile and GitHub Actions also consume stable paths directly.

Moving high-fanout helpers such as `normative_atomic.py`, `normative_catalog.py`, `normative_full.py`, `pdf_measurement.py`, `pdf_vector_measurement.py` or `repository_paths.py` would create broad import/path churn without adding correctness or ownership capability.

Phase 5B therefore keeps all current tool paths and adds `tools/README.md` as the durable ownership contract. It classifies stable build/release entry points, shared normative/path libraries, PDF measurement modules, the PDF validator CLI, Windows support utilities and the existing `tools/ci/` namespace. No compatibility wrappers are needed because no path moves.


### Phase 5B final receipt

Phase 5B is complete. PR #434 merged as `565a7e3654074989283487f97101daea17ec83e3` from final head `25c789f71c56aa760782956babf75ba2aad40a58`.

The decision is intentionally **no physical tool move**. `tools/README.md` is now the durable ownership contract for stable Makefile/release entry points, high-fanout shared normative/repository libraries, PDF measurement modules, the PDF validator CLI, Windows support utilities and workflow-owned helpers under the existing `tools/ci/` namespace.

The current paths are retained because a fresh scan found 77/84 Python checks directly dependent on the root tools surface or named tool entry points, in addition to direct Makefile/workflow consumers. Moving those files would create broad import/path churn without adding validation capability or clearer ownership. No compatibility wrappers are needed because no paths moved.

Post-merge `main` passed Static Contract #883 and Linux Release Check #286 on the exact merge SHA, including `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, distribution bundle certification, canonical-reference reproducibility, CTAN pkgcheck and seven-profile release review-pair generation.

### Phase 5C template/examples decision

Issue #435 evaluated whether non-TCC/profile examples should move into a dedicated `examples/` namespace. The decision is intentionally **no move**.

`template/main.tex` is not a loose example: it is the documented canonical executable TCC tutorial and the canonical public-bundle `main.tex` source consumed by `tools/build-public-bundles.py`. `template/scientific-article.tex` is likewise a release-certification source consumed directly by `tests/integration/release/release-review-pairs.sh`.

The rest of `template/` is already organized around the canonical tutorial under `frontmatter/`, `chapters/`, `backmatter/` and `figures/`. Creating `examples/` or moving either root entry point would add documentation/builder/release-path churn without adding validation capability, lifecycle separation or ownership clarity.

No `template/README.md` is added solely for this decision because the public bundle builder would distribute it, changing generated bundle contents without a demonstrated user requirement. Existing root/user documentation already defines the template/tutorial ownership.

### Phase 5 final certification

Phase 5 leaves the supporting repository structure in the following intentional state:

- release ownership is explicit under `release/README.md`;
- the CTAN example source lives canonically at `release/ctan/abntexto-ufc-example.tex`, with the retired documentation path rejected fail-closed;
- 5A / PR #432 is certified by Static #881 + Linux Release #285;
- root `tools/` remains the stable shared-library/entry-point surface, with CI-specific helpers under `tools/ci/`; 5B / PR #434 is certified by Static #883 + Linux Release #286;
- `template/` remains the canonical executable/template namespace by the 5C no-move decision;
- no published v3.0.4 source/tag/GitHub Release asset/submitted CTAN archive or historical release receipt was rewritten.

This closeout update is documentation-only. The next roadmap phase is Phase 6 Web/Lite self-contained hardening.


### Phase 6A execution map

Phase 6A removes the Web/Lite validator's runtime CDN dependency without changing the PDF.js version or validation semantics.

The existing `pdfjs-dist` 6.2.108 dependency is vendored under `validator/vendor/pdfjs/`. Provenance is bound to the official Mozilla PDF.js `v6.2.108` release, tag commit `0365cbde028bd92e58f2dab1bb70cd30ac7acfd7`, release asset `pdfjs-6.2.108-dist.zip` (GitHub asset ID `493114690`) and published asset SHA-256 `7bf642d59582b475e8c48447da9b02b0108fad9742d7c2a35cb4ed6dd45e95ba`.

The import preserves exact upstream bytes:
- `pdf.mjs`: 853537 bytes, SHA-256 `e0ccc62fbfa69942eb7dd46c89d4b3ea8fc08f61b234e65f32e6d5c76efc04c8`;
- `pdf.worker.mjs`: 2222991 bytes, SHA-256 `1a7607f28cfbc63f0e4e0a41927c89f991e353e4f3fb4565ecfd621ac5975089`;
- `LICENSE`: 10174 bytes, SHA-256 `0d542e0c8804e39aa7f37eb00da5a762149dc682d7829451287e11b938e94594`.

`validator/app.js` follows the local main module and worker only. `validator_source.py` independently pins the upstream identity, asset digest and each tracked file digest/size, and rejects jsDelivr/unpkg or external JavaScript module imports. The Pages builder requires the complete local runtime/provenance set in the generated static package.

The productive validation schema, check IDs, verdict semantics and local PDF processing behavior are unchanged. Explicit browser network denial and CSP hardening remain the separate 6B slice after this local runtime is certified.

### Phase 6A bootstrap incident

A temporary branch-only GitHub Actions bootstrap was used because PDF.js generic browser modules are generated release assets and are not blobs in the source tag. Bootstrap run #1 downloaded the official asset and verified its published SHA-256 successfully, then failed before commit because the first extraction guard incorrectly required a single shallow `LICENSE` match across the archive.

No vendor file was committed by the failed run. The bootstrap was corrected to derive the package root from the unique `build/pdf.mjs` match and require the worker and LICENSE under that same package root. Bootstrap run #2 passed and committed the verified upstream files plus machine-readable provenance.

The temporary bootstrap workflow is removed from the final feature tree. Permanent reproducibility is carried by the recorded upstream release/asset identity and fail-closed tracked-file hashes rather than by a standing networked workflow.


### Phase 6A validation incident

Initial Static Contract #886 failed on PR #439 head `50b934e739ef0425d8199e773fceb0e7b68429f7` because `tests/checks/evidence/normative_validator_contract.py` still defined the Web/Lite PDF.js boundary through the retired jsDelivr package literal `pdfjs-dist@6.2.108`.

The runtime had already moved to the verified local vendor tree, so the old marker no longer represented the intended contract. The normative validator contract now requires the canonical local main-module and worker paths and explicitly forbids jsDelivr/unpkg runtime dependencies. Exact version, release-asset provenance and file hashes remain independently fail-closed in `tests/checks/validator/validator_source.py`.

Static #886 remains audit evidence. No validation semantics, check IDs, verdict logic or PDF.js version changes; fresh required gates must pass on the corrected head.


### Phase 6A final receipt

Phase 6A is complete. PR #439 merged as `11e3a4f50d3e39d966d736568c4c586c0680a231` after final head `59880edef434c2e8977832b5cfd6ffd6531f689f` passed Static #887 and Linux Integration #752, including productive Web/Lite browser E2E.

Initial Static #886 remains preserved as evidence that the normative validator contract still encoded the retired jsDelivr package literal after the runtime moved local. The correction made the contract require the canonical local PDF.js main/worker paths and reject jsDelivr/unpkg while preserving version 6.2.108 and all validation semantics.

Post-merge `main` passed Static #888, Pages #8 (build + deploy) and Linux Release #287. Static records `pdfjs_local=true`, exact provenance PASS and zero orphaned test/technical surfaces. Release #287 completed `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, distribution bundles, canonical-reference reproducibility, CTAN pkgcheck and seven-profile review-pair generation on the exact merge SHA. Published v3.0.4 release/tag/archive bytes remain unchanged.

### Phase 6B execution map

Phase 6B certifies that the assembled Web/Lite Pages package is genuinely network-independent and applies a bounded browser CSP without changing validator semantics.

The productive Linux browser E2E now assembles `_site/validator` through `tools/ci/build-pages-site.sh` and serves that package rather than the source directory. Chrome runs behind a loopback deny proxy with background/external DNS disabled. Performance logs fail closed on any HTTP(S) request outside the local test origin; browser logs fail on CSP violations. The existing positive canonical/reference PDF and negative non-A4 PDF still pass through the same productive UI/analyze path.

`validator/index.html` gains an enforced meta CSP restricting default/script/worker/connect to same origin and denying objects, frames, base changes and form submission. `style-src 'unsafe-inline'` is deliberately bounded to the one existing tracked style block; Static rejects additional style attributes, inline scripts and inline event handlers.

Static also requires the deny-proxy/performance-log E2E markers and requires the CI runner to exercise the assembled Pages package. The Pages builder requires the CSP markers in the copied artifact. PDF.js vendor bytes/provenance, validation schema/check IDs, mandatory/deep boundaries and verdict semantics remain unchanged.

### Phase 7A execution map

Phase 7A turns the retained Windows literal-font maintainer path into a bounded CI portability proof without creating a full Windows release matrix.

The Windows job is pinned to `windows-2025`. The workflow provisions TeX Live 2026 through `zauguin/install-texlive` pinned to commit `6671d0c62046c7e349fe154d5208fe746b07e037` (v4.4.0), then materializes the repository-pinned `abntexto` 1.1 source through `tools/fetch-abntexto.py`.

The job reuses the repository-owned Windows support pipeline:
- verifies the eight Times New Roman/Arial system font files already present on the Windows runner;
- runs `tools/prepare-windows-fonts.ps1` and its two encoding converters;
- runs `tests/integration/layout/font-poc.sh` with `UFC_FONT_POC_COMPILE_ONLY=1`;
- requires the four strict class PDFs for Times/Arial under pdfLaTeX/LuaLaTeX;
- uploads only generated PDFs, never Microsoft font binaries.

A dependent `ubuntu-24.04` job downloads those exact PDFs and runs `tests/integration/layout/windows-font-pdfa.sh`, reusing existing literal font identity, Unicode extraction, embedding and PDF/A-2b certification semantics.

`tests/checks/repository/windows_portability_contract.py` fails closed if the workflow loses its explicit Windows runner, pinned TeX Live setup/version, pinned `abntexto` materialization, preparation pipeline, compile-only proof, artifact handoff or Linux certification gate. A floating `windows-latest` runner and `continue-on-error` bypass are explicitly rejected.

This is a portability smoke only. Linux remains the authoritative complete release regression, and published v3.0.4 release/tag/archive bytes remain immutable.


### Phase 7A initial validation incidents

The first PR #444 head `517d203dc94c1791fd5ea25e81cd6ca3525a9385` exposed two independent bootstrap defects before any merge:

- Static Contract #891 failed because the newly added `windows_portability_contract.py` had not yet been registered in `tests/static.py::SOURCE_CHECK_NAMES`. The existing test-surface integrity check correctly rejected it as an unreachable retained check. Correction `5394f7d62766a0419b7b74cd15097af9c1a49e9e` registers the check instead of exempting it.
- Windows portability smoke #1 failed during Chocolatey MiKTeX provisioning before any repository font preparation or compilation ran. The Chocolatey installer reached `miktexsetup_standalone` but timed out contacting `https://api2.miktex.org/hello` (curl code 28). The failure is preserved as infrastructure evidence; it is not hidden with retries or `continue-on-error`.

The corrected workflow replaces that network-specific MiKTeX bootstrap with TeX Live 2026 through `zauguin/install-texlive` v4.4.0 pinned by commit SHA. The action's implementation has an explicit Windows platform path using `install-tl-windows.bat`; the repository still verifies required TeX commands and then uses its existing Windows preparation/compile proof. Fresh Static, Linux and Windows gates are required on the corrected head.


### Phase 7A TeX Live dependency incident

Windows portability smoke #5 proved that TeX Live 2026 installation itself succeeds on `windows-2025`, but the initial bounded package set omitted `ttf2tfm`. The workflow stopped in the explicit command-verification step before font preparation or document compilation.

TeX Live packages the `ttf2tfm` binary in `ttfutils`. The corrected package set adds only `ttfutils`; it does not widen the installation to a full TeX Live scheme. Windows smoke #5 remains audit evidence of the missing explicit dependency. Fresh Static/Linux/Windows gates are required on the corrected head.


### Phase 7A virtual-font utility dependency incident

Windows portability smoke #7 on PR #444 head `2dad651d851fe7aa542b028089df1f0d8ed83256` successfully installed TeX Live 2026 on `windows-2025`, but stopped in the explicit command-verification step because `vptovf` was absent. Font preparation and PDF compilation therefore did not run.

The failure is a real bounded dependency gap, not a reason to weaken the proof. `prepare-windows-fonts.ps1` requires `vptovf` to convert the generated VPL metrics into VF/TFM files. TeX Live owns this utility under the `fontware` package (with the Windows executable supplied by `fontware.windows`).

The corrected workflow adds only `fontware` to the explicit TeX Live package set. The portability contract now requires that package token and rejects the stale `miktex=` evidence marker. The successful evidence line identifies `texlive=2026` instead. Windows smoke #7 remains preserved as audit evidence; fresh Static/Linux/Windows gates are required before merge.


### Phase 7A Brazilian Portuguese language dependency incident

Windows portability smoke #8 on PR #444 head `7c21203dd21c7a57c81d547e722f8480cb28bb22` proved the prior `fontware` correction: TeX Live installation, required command verification, pinned `abntexto` materialization and `prepare-windows-fonts.ps1` all passed. The strict pdfLaTeX proof then stopped because Babel could not load the `brazilian` language definition.

The failure is an explicit bounded TeX dependency gap. TeX Live provides Brazilian Portuguese Babel support in `babel-portuges`, including `brazilian.ldf`. The corrected workflow adds only `babel-portuges` to the package set, and the portability contract requires that token so the language dependency cannot silently disappear.

Windows smoke #8 remains audit evidence. No document/class semantics, language selection or failure policy is weakened; fresh Static/Linux/Windows gates are required before merge.


### Phase 7A newtx transitive dependency incident

Windows portability smoke #9 on PR #444 head `4fd5255cfdae31c3c360a107d60dad129da04087` proved the previous bounded corrections: TeX Live 2026 installation, required command verification, pinned `abntexto` materialization, Windows literal-font preparation and Brazilian Portuguese Babel loading all passed. The strict Times New Roman pdfLaTeX proof then stopped while loading `newtxtext.sty` because `xpatch.sty` was absent.

This is a transitive package dependency exposed by the deliberately bounded TeX Live installation, not a class/font-policy failure. The corrected workflow adds only the TeX Live `xpatch` package, and the portability contract requires that package token so the dependency cannot silently disappear.

Windows smoke #9 remains audit evidence. No document semantics, font strictness, engine coverage or failure policy is weakened; fresh Static/Linux/Windows gates are required before merge.


### Phase 7A validation incident — Windows smoke #10

Windows portability smoke #10 on PR #444 head `a3cf3c023ba77f107602478c1cb50c1aaade10fa` proved the prior bounded corrections: TeX Live 2026 installation, explicit command verification, pinned `abntexto` materialization, Windows literal-font preparation, Brazilian Portuguese Babel support and `xpatch` loading all passed. The strict Times New Roman pdfLaTeX proof then stopped while loading `newtxtext.sty` because `xstring.sty` was absent.

This is another explicit transitive dependency exposed by the deliberately bounded TeX Live package set, not a font/class-policy failure. The corrected workflow adds only the TeX Live `xstring` package. The fail-closed Windows portability contract requires that package token so it cannot silently disappear.

Windows smoke #10 remains preserved as audit evidence. No proof, font identity, PDF/A requirement, runner generation or artifact-certification step is weakened. Fresh Static/Linux/Windows gates are required before merge.


### Phase 7A validation incident — Windows smoke #11

Windows portability smoke #11 on PR #444 head `1f5f7ba2655244880bf900a441f804f64f335d7d` proved the `xstring` correction and progressed through TeX Live setup, pinned `abntexto`, Windows font preparation and the earlier `newtxtext` dependencies. The strict Times New Roman pdfLaTeX proof then stopped because `fontaxes.sty` was absent.

The failure is another bounded transitive dependency from the intentionally minimal TeX Live installation. The corrected workflow adds only the TeX Live `fontaxes` package, and the fail-closed Windows portability contract requires that token.

Smoke #11 remains preserved as portability evidence. No runner, font identity, compile proof, artifact transfer, Unicode extraction, embedding or PDF/A-2b requirement is weakened. Fresh Static/Linux/Windows gates are required before merge.


### Phase 7A validation incident — Windows smoke #12

Windows portability smoke #12 on PR #444 head `56d97da3ddd3b982f06ef68f07037d763983c577` proved the `fontaxes` correction and progressed through the strict Times New Roman pdfLaTeX proof into bibliography initialization. Compilation then failed because BibLaTeX could not find style `abnt`.

The missing style is provided by the TeX Live `biblatex-abnt` package. The corrected workflow adds only that explicit package and the fail-closed Windows portability contract requires its token.

Smoke #12 remains preserved as portability evidence. No bibliography semantics, class behavior, font identity, artifact transfer, Unicode extraction, embedding or PDF/A-2b requirement is weakened. Fresh Static/Linux/Windows gates are required before merge.


### Phase 6 final receipt

Phase 6 is complete. Web/Lite uses the pinned local PDF.js 6.2.108 runtime and the assembled Pages package is certified with external network denied and the bounded CSP enforced.

- 6A / PR #439 merged as `11e3a4f50d3e39d966d736568c4c586c0680a231`; post-merge Static #888, Pages #8 and Linux Release #287 PASS.
- 6B / PR #441 merged as `e0bfdf1e9a419125b112248dc6365ea8fe33f848`; post-merge Static #890, Pages #9, Linux Integration #754 and Linux Release #288 PASS.
- Productive browser evidence reports external network denied, zero external HTTP requests, CSP PASS and local PDF processing.
- Validator schema/check IDs/verdict semantics and published v3.0.4 artifacts remain unchanged.


### Phase 7A final receipt

Phase 7A is complete. PR #444 merged as `524b593544854abd2ee10c29d1566da95508c318` after final head `4fc0465684938dd18bbf85a2da5a3c268ebc32fd` passed Static #903, Windows portability smoke #13 and Linux Integration #767.

Post-merge `main` passed Static #904, Windows smoke #14 and Linux Release #289. Windows Server 2025 generated four strict Times New Roman/Arial PDFs across pdfLaTeX and LuaLaTeX; the dependent Ubuntu job certified literal font identity, Unicode extraction, embedding and PDF/A-2b. Release #289 completed `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.

All intermediate Windows bootstrap/dependency failures remain preserved in #443 and the maintenance audit trail. No Microsoft font binary is tracked or redistributed.


### Phase 7B execution map

Phase 7B adds only the portability proof that is distinct from Linux x64 and Windows x64: Darwin on Apple Silicon/ARM64.

A bounded `.github/workflows/macos-smoke.yml` job is pinned to `macos-26` and requires `uname -s = Darwin` plus `uname -m = arm64`. It provisions explicit TeX Live 2026 through the same SHA-pinned setup action already certified by 7A, materializes pinned `abntexto`, and compiles the canonical public tutorial `template/main.tex` with pdfLaTeX and LuaLaTeX through the Makefile.

Exactly two PDFs are transferred to a dependent Ubuntu job. That job reuses `tests/integration/layout/font-embedding.sh` and `tests/integration/layout/pdfa.sh` rather than introducing parallel validation semantics. `tests/checks/repository/macos_portability_contract.py` fails closed if the explicit runner/architecture, pinned TeX toolchain, both engines, artifact transfer or Linux certification is removed.

The macOS smoke is not a second release matrix and does not reproduce the Windows literal Microsoft-font path. Linux remains the full release-grade authority.


### Phase 7B validation incident — macOS smoke #1

Initial macOS portability smoke #1 on PR #446 head `220d2a6403f5362f42deeb4b5a9b9799c8020c51` failed during the pinned TeX Live 2026 installation before repository compilation.

The bounded package list requested `lmodern`, but the TeX Live 2026 repository on the `macos-26` universal-darwin platform exposes the Latin Modern package as `lm`. The installer recorded `tlmgr install: package lmodern not present in repository` and exited nonzero after completing the remaining package work. The public template build and dependent Linux certification therefore did not run.

The correction changes only the explicit macOS TeX Live package token from `lmodern` to `lm`. The fail-closed macOS portability contract now requires `lm` and rejects reintroduction of `lmodern`. No runner, architecture, engine, template, artifact-transfer, font-embedding or PDF/A requirement is weakened.

Smoke #1 remains preserved as portability evidence. Fresh Static, Linux and macOS gates are required on the corrected head before merge.


### Phase 7B validation incident — macOS smoke #2

macOS portability smoke #2 on PR #446 head `f71b5e52aa857c53401cb41b6c2a57ebcbad657b` proved the `lm` correction: TeX Live 2026 installation completed, the runner asserted Darwin/ARM64, pinned `abntexto` was materialized, and compilation entered the canonical public `template/main.tex` path.

The pdfLaTeX build then failed because `tabularray-abnt.sty` requires `tabularray.sty`, but the deliberately bounded TeX Live package set listed `tabularray-abnt` without its base `tabularray` package.

The correction adds only the explicit `tabularray` package and makes the fail-closed macOS portability contract require it. No template, engine, architecture, artifact-transfer, font-embedding or PDF/A requirement is weakened.

Smoke #2 remains preserved as portability evidence. Fresh Static, Linux and macOS gates are required on the corrected head before merge.
