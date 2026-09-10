# Post-v3.0.1 regression and simplification plan

## 1. Baseline and boundary

This plan starts from the certified v3.0.1 candidate at `111680cd934a4ea55b02f6ffe730ff5260077565`.

The v3.0.1 source and distribution bytes remain frozen. Work described here belongs to a post-v3.0.1 branch and must not be merged into `main` before the v3.0.1 tag/publication sequence is completed. The next semantic version is deliberately left undecided until the audit classifies whether the resulting changes are documentation/distribution-only or alter public runtime behavior/API.

The release invariant remains:

`certified source SHA == visually approved source SHA == tagged release SHA == publication source SHA`.

## 2. Confirmed findings from the first regression pass

### 2.1 Canonical example source identity drift

`template/main.tex` currently loads:

```tex
\input{chapters/1-introduction}
\input{chapters/2-theoretical-framework}
\input{chapters/related-work}
\input{chapters/3-methodology}
\input{chapters/4-results}
\input{chapters/formatting-examples}
\input{chapters/5-conclusion}
```

The inconsistency is real, but it is broader than two missing numeric prefixes. Several filenames no longer describe their contents:

- `2-theoretical-framework.tex` renders "Estrutura do trabalho acadêmico";
- `related-work.tex` renders "Elementos pré-textuais em detalhe";
- `3-methodology.tex` renders "Formatação geral e organização da parte textual";
- `4-results.tex` renders "Citações, notas e referências";
- `formatting-examples.tex` renders "Ilustrações, tabelas e outros objetos acadêmicos";
- `5-conclusion.tex` renders "Recursos do abntexto-ufc, elementos pós-textuais e revisão final".

The post-release work must therefore rebuild the chapter/file identity rather than merely rename two files. The canonical example should be a TCC-style pedagogical document whose source organization is sequential and whose filenames describe the actual subject of each section.

A provisional source sequence is:

1. `1-introduction.tex`;
2. `2-academic-work-structure.tex`;
3. `3-front-matter.tex`;
4. `4-general-formatting.tex`;
5. `5-citations-notes-references.tex`;
6. `6-academic-objects.tex`;
7. `7-abntexto-ufc-resources-and-final-review.tex`.

The final naming must be decided together with the TCC pedagogical outline, not independently.

### 2.2 The seven release-review PDFs are not the full example

The seven exact-SHA review PDFs have a specific release-gate purpose. Six are generated from `tests/smoke/base-profile.tex`; the scientific article uses `template/scientific-article.tex`. They validate profile-specific rendering and preflight, but they are not the reviewer-corrected full reference TCC.

This explains why they appear to have "lost" the content previously present in the full example: the release review artifact changed purpose. The error is not that smoke PDFs exist; the error is allowing them to become the only prominent compiled examples.

The next cycle must keep both concepts separate:

- **profile smoke/review PDFs**: small, focused release-gate fixtures;
- **canonical TCC/reference PDF**: complete pedagogical document explaining the normative rules and how the project implements them.

### 2.3 Distribution omits the full compiled reference PDF

The certified distribution contains three archives. The template and Overleaf archives contain the editable `template/` sources, but no compiled full TCC/reference PDF. The CTAN archive contains `abntexto-ufc-example.pdf`, but that PDF is compiled from `docs/ctan-example.tex`, which is intentionally a minimal example.

The next distribution contract must add a deterministic full reference PDF, with a stable public name such as `abntexto-ufc-reference.pdf` or `abntexto-ufc-tcc-example.pdf`. The exact name is part of P2/P3 acceptance.

The minimal CTAN example should not be removed simply because the full example is restored. A small compile smoke example and a complete pedagogical reference solve different problems.

Whether the full PDF is also placed inside the CTAN upload must be decided against the existing distribution constraint that institutional marks and proprietary Microsoft fonts are not redistributed. At minimum it must be a first-class GitHub release/template distribution artifact.

### 2.4 CI workflow count is already small; branch count is not

The active certified tree has exactly three GitHub Actions workflows:

- `static-contract.yml` - cheap repository/source contract;
- `linux-integration.yml` - scoped or complete TeX/integration validation;
- `linux-release-check.yml` - complete release, distribution, reproducibility, pkgcheck and review-artifact gate.

The first-pass conclusion is **do not remove a workflow merely because the repository feels crowded**. These three have distinct execution costs and responsibilities. P6 must still test whether common setup can be factored out or whether release/integration duplication is excessive, but there is no evidence today that the repository contains a large set of active legacy workflows.

The branch namespace is different: GitHub's first 100-branch page is full and a second page is non-empty. Numerous `tmp/`, `noop`, historical `docs/`, `audit/`, `cert/`, `ci/`, `fix/`, `refactor/` and old release branches remain. Branch cleanup is therefore a real repository-hygiene task, but it must use a generated keep/delete manifest and explicit approval before deletion.

### 2.5 Release control-plane state is stale by construction

The frozen `release/v3-roadmap.json` still records several recovery steps as pending even though the recovery PR was merged and the exact-main Static, complete Linux Integration, complete Linux Release Check and current CTAN pkgcheck have all passed.

This is a consequence of the current invariant: committing an updated "we are certified" state after certification would itself create a new source SHA and invalidate the certification target.

P7 must remove this self-referential control-plane design. Candidate policy/state belongs in source; immutable post-build/publication receipts should live in a mechanism that can refer to the certified SHA without changing it (for example tag/release metadata or separately versioned release evidence). No implementation choice is frozen by this plan yet.

### 2.6 Web/Lite validator has an unresolved deployment defect

`validator/app.js` imports:

```js
import {normativeCatalog,normativeRules,normativeSources} from "./normative-catalog.js";
```

But the certified `validator/` tree contains only:

- `app.js`;
- `index.html`;
- `validation-contract.json`;
- `validation-vectors.json`.

There is no tracked `validator/normative-catalog.js`. A static deployment of that directory therefore does not have a complete module graph.

This must be treated as a confirmed post-release defect. P5 must establish one deterministic source-to-Web catalog generation step, include it in the deployed site/package, and add a clean-deployment test that follows every local browser import and fails on missing files.

### 2.7 The generated PDF is proven by CLI/Deep, not by a real Web/Lite E2E test

The certified release reference PDF passes the CLI/Deep validator and the release reproducibility gate records `pdf_validator=PASS`. The Web/Lite and CLI contracts are also synchronized at the schema/check/verdict level.

However, the current `tests/checks/normative_cross_surface.py` runs synthetic verdict/schema vectors extracted from selected expressions in `validator/app.js`. It does **not** run the actual canonical PDF through `analyze(file, profile)` using PDF.js in a browser-equivalent execution.

Therefore the current defensible statement is:

- CLI/Deep: canonical generated PDF **passes**;
- Web/Lite contract identity: **passes**;
- actual canonical PDF through the deployed browser validator: **not yet proven**, and the missing local module currently prevents treating the source directory as a complete deployment.

P5 closes this gap with an actual end-to-end test.

### 2.8 Active documentation and utility surfaces need a consumer audit

`docs/` currently contains 31 active files. Many are durable documents, but many others are phase-end, continuation, hardening, certification, recovery or internal process records. `tools/` contains 13 utilities. Two encoding-conversion PowerShell scripts are not invoked by the primary Makefile entrypoints and require a consumer audit; this does not yet authorize removal.

Git history already retains historical process detail. The active tree should ultimately keep only documentation and tooling that has a current operational, user-facing, normative, migration, build, test or maintenance purpose.

## 3. Whole-repository audit method

The next regression must cover all 472 tracked files from the certified baseline. Every tracked file receives one row in a machine-readable inventory with:

- path and category;
- current purpose;
- owning entrypoint or subsystem;
- direct and indirect consumers;
- whether it is shipped to CTAN/template/Overleaf/site/none;
- checker or evidence that protects it;
- lifecycle classification: `KEEP`, `CONSOLIDATE`, `REVIEW`, `REMOVE_CANDIDATE`;
- decision rationale.

The audit is reachability-plus-semantics, not grep-only. A file is not removable merely because no literal reference is found: dynamic TeX inputs, generated files, fixtures, shell-discovered files and GitHub configuration must be resolved using their actual loading mechanism.

The required audit order is:

1. root/build entrypoints and GitHub Actions;
2. runtime class and all project `.def` modules;
3. `template/` complete editable example, front matter, chapters, back matter and figures;
4. `validator/` browser surface and `tools/validate-ufc-pdf.py` deep surface;
5. `tools/` generators, fetchers, measurement helpers and Windows utilities;
6. `tests/` runner, suite selector, static checks, integration gates, documents, fixtures and smoke inputs;
7. `standards/` rules, sources, scenarios, measurements and evidence ownership;
8. `release/` machine state and CTAN metadata;
9. `docs/` durable documentation versus transient process records;
10. `assets/` provenance, licensing and redistribution boundaries;
11. Git branches/tags/releases that remain operationally visible.

## 4. Canonical TCC/reference requirements

The rebuilt reference must be a real TCC-shaped teaching document, not a collection of disconnected validation paragraphs. It should still be synthetic enough to distribute safely, but complete enough that a student can use it as the primary example.

Each normative topic must answer four questions in the document/source pair:

1. what the ABNT/UFC requirement is and which current authority governs it;
2. what the expected rendered result is;
3. which `abntexto-ufc` command/key/environment implements it;
4. where the repository validates that behavior.

Coverage must include, when applicable to a TCC profile: paper and margins, font family/size, line spacing, paragraphs, pagination, cover, title page, approval page, catalog-card policy, dedication, acknowledgements, epigraph, resumo/abstract and keywords, optional lists, table of contents, section hierarchy, direct/indirect/apud citations, long quotations, footnotes, equations, illustrations, tables/IBGE presentation, source/notes, algorithms/code where supported, bibliography/NBR 6023:2025, appendices, annexes, glossary/index, PDF/A/deposit guidance, accessibility boundaries and project-specific portability/font behavior.

The document must distinguish normative requirements, UFC institutional requirements, project policy, recommendations and examples. It must not present a convenience choice as an ABNT rule.

## 5. Distribution acceptance after the rebuild

The full reference PDF must be generated from the same source used in `template/main.tex`, not maintained as an independently edited binary. Its build must be deterministic under the release `SOURCE_DATE_EPOCH` policy and must pass:

- compile convergence;
- warning/overflow gate;
- A4/layout validation;
- font embedding;
- PDF/A-2b where the selected distribution profile claims it;
- CLI/Deep validator;
- Web/Lite E2E shared checks;
- checksum recording;
- explicit visual review.

The distribution tests must assert both source and PDF presence where intended and verify the PDF hash/provenance against the exact candidate SHA.

## 6. Validator repair and certification

P5 is not complete until all of the following are true:

- the site has a declared deployment source and reproducible build/deploy path;
- every relative browser import resolves from a clean artifact;
- `normative-catalog.js` is generated deterministically from the canonical standards catalog or replaced by an equally explicit build-time mechanism;
- the browser site opens without console/module/network errors apart from declared CDN dependencies;
- the canonical TCC/reference PDF is analyzed by the real Web/Lite `analyze` path;
- all shared check IDs, normative metadata and verdict semantics remain aligned with CLI/Deep;
- Web/Lite continues to return review rather than false PASS for deep-only font-embedding/PDF-A capabilities;
- a negative PDF proves that the Web/Lite path actually rejects at least one violated shared predicate;
- privacy remains local-processing, with no upload API introduced.

## 7. CI, test and tool simplification criteria

A workflow/test/tool may be consolidated or removed only if its protected behavior remains covered by another independently understandable gate. The simplification audit must explicitly identify duplicated environment setup, duplicated compiles, overlapping checkers and fixtures that differ only accidentally.

The desired end state is not the smallest possible test suite. It is the smallest suite that still makes each release guarantee independently observable. Cheap static checks should remain separated from expensive TeX/release checks if that preserves fast feedback and avoids unnecessary CI cost.

## 8. Documentation simplification criteria

Documents fall into four classes:

- durable public/developer contract - retain;
- current operator/release procedure - retain/consolidate;
- immutable release receipt - relocate to an appropriate immutable release-evidence mechanism;
- transient phase narrative already preserved by Git history - remove candidate after cross-reference audit.

The post-release tree should not require reading multiple phase-end and continuation files to discover current truth.

## 9. Work packages and gates

### P0 - Close v3.0.1 without mutation

No code/doc commit on `main`. Finish the mandatory human visual acceptance on the exact seven-pair artifact, then tag/publish only the already certified bytes.

### P1 - Whole-repository census

Produce a complete 472-file inventory plus live-branch inventory. No deletions yet.

### P2 - Canonical TCC/reference reconstruction

Approve the pedagogical outline, rename/reorganize sources, restore complete didactic content and compile one canonical full PDF.

### P3 - Distribution redesign

Add the generated full reference PDF to the selected public bundles, preserve the minimal CTAN smoke example, and enforce artifact contents/hashes.

### P4 - Runtime/API/normative regression

Re-walk class loading, all 14 runtime modules, public API ownership, profiles, bibliography, all normative catalog rules/evidence and negative paths from initial source assumptions forward.

### P5 - Web/Lite validator repair and E2E

Repair the missing module/deploy contract and prove the actual canonical PDF and negative fixtures through the browser implementation.

### P6 - CI/tests/tools simplification

Use the consumer graph to consolidate/remove only proven redundancy. Create a separate proposed branch-deletion manifest; do not delete branches during the source audit.

### P7 - Documentation/control-plane simplification

Reduce current-source state duplication and redesign immutable certification/publication receipts.

### P8 - Clean-room final regression

Fresh candidate, supported engines/platform scopes, complete test matrix, distributions, canonical TCC PDF, seven profiles, both validator surfaces, pkgcheck and visual review. Only after this gate is the next version classified and prepared for release.

## 10. Immediate next state

The executable machine companion to this document is `release/post-v3.0.1-regression-audit.json`.

No finding in this document changes the frozen v3.0.1 source SHA. The current release should be closed first; implementation begins from this branch afterward.
