# abntexto-ufc v3 — Regression Audit Baseline

Updated: 2026-09-04
Status: ACTIVE AUDIT
Baseline branch: `main`
Baseline SHA: `c4bf51b574647226ee488440579ec2a204c16c79`

## Objective

Before continuing scientific-article runtime work, regress the current v3 foundation from repository state, normative contracts, implementation, tests, and canonical rendered output. The goal is not to preserve every current behavior blindly; it is to determine which behavior is actually justified, which review findings are already resolved, which are only partially covered, and which current assumptions must be corrected.

This audit is intentionally inserted before the previously active `V3-A2` runtime implementation because that implementation had not started at the baseline checkpoint.

## Control-plane baseline

At the audit entry point:

- Git `main` is `c4bf51b574647226ee488440579ec2a204c16c79`.
- `release/v3-roadmap.json`, `docs/HANDOFF-V3.0.0.md`, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` agree that the previous active work item was `V3-A2`.
- The previous A2 scientific-article runtime implementation had not started.
- The exact-main `Static contract` run `33902329629` passed.
- The canonical current `template/main.tex` compiles successfully in the repository's TeX Live 2026 CI environment and produces a 55-page A4 PDF.

Therefore the repository is in a safe state for a regression/replanning checkpoint. No partially implemented article runtime needs to be preserved.

## What is already strong

### Repository and engineering structure

The v3 repository reconstruction has meaningful engineering value and should not be discarded. Current strengths include:

- canonical `abntexto-ufc` physical identity and modular ownership;
- no active legacy class entrypoint remains;
- fail-closed source and repository contracts;
- direct ownership of public setup/front-matter/object/back-matter APIs;
- permanent static, Linux integration, and Linux release workflows;
- literal Times New Roman/Arial certification on Windows plus Unicode/embedding/PDF/A evidence from the completed certification stage;
- current ABNT/UFC source catalog and explicit precedence policy;
- large retained test surface with reachability/orphan controls;
- current NBR 10520 capitalization behavior and an explicit NBR 6023:2025 compatibility layer;
- canonical academic-work and research-project profiles already compiled and tested.

These are retained unless the regression finds a concrete defect.

## Regression findings requiring action

### F1 — Review feedback was not a first-class tracked contract

The prior engineering roadmap contains extensive machine/test history, but the librarian review findings were not represented as one bounded acceptance contract. This allowed the code and tests to become internally consistent while still leaving reviewed presentation details unresolved.

**Action:** `docs/UFC-LIBRARIAN-REVIEW.md` is now the 34-item review contract. Every item must map to authority, implementation, evidence, and closure state.

### F2 — Green tests are not sufficient evidence of visual/normative correctness

The current test architecture is strong, but several rules prove internal consistency rather than agreement with the newly recovered review evidence. Regression must therefore distinguish:

- implementation correctness;
- current normative authority;
- institutional/reviewer evidence;
- visual parity/acceptance.

**Action:** add a review-to-rule traceability layer and final canonical-PDF visual gate.

### F3 — Object-caption font policy has a concrete conflict

Current implementation uses `\abntsmall\singlesp` for object legends. Current machine catalog places `illustration-caption` inside the 10 pt reduced-font policy. The librarian review repeatedly requests 12 pt, equal to body text.

**Classification:** `NORMATIVE-REVIEW`, not an immediate code change.

**Action:** re-open the exact current UFC/ABNT authority for figure/table title, source, legend, and note typography; then update catalog, runtime, tests, and reference guide atomically if the review is confirmed.

### F4 — Current title-page advisor line still misses reviewed punctuation

The current title-page implementation prints the advisor/co-advisor lines without the reviewed final punctuation.

**Classification:** implementation/reference defect, subject to quick source confirmation.

### F5 — Optional department works in runtime but the canonical example communicates the wrong contract

The runtime already omits blank optional lines. However, `template/main.tex` still uses `Nome do Departamento ou Unidade Acadêmica` without communicating `se houver`.

**Classification:** reference/documentation defect.

### F6 — Full-name requirement is not communicated by the canonical placeholder

The canonical template uses `Nome Sobrenome`; the reviewed document explicitly calls for `NOME COMPLETO`.

**Classification:** reference/documentation defect.

### F7 — Committee institution acronym presentation is not encoded as a consistent example contract

Committee institution strings are printed verbatim. The review requests `Instituição (sigla)`. The current template commonly supplies `Universidade Federal do Ceará` without `(UFC)`.

**Classification:** partial; decide whether this remains author-provided content or gains an institutional acronym helper.

### F8 — Annex source guidance remains incomplete

The current annex example explains that the material is external but does not explicitly demonstrate the reviewed `Fonte:` requirement.

**Classification:** reference/documentation defect with possible fixture addition.

### F9 — Current V3 reference document contains stale V2 language

The V3 reference corpus still contains rendered policy text such as `Na V2...` and `A V2...` in `template/chapters/formatting-examples.tex`.

**Classification:** clear regression/documentation defect unrelated to the 34 review items.

**Action:** replace product-version-specific stale language with V3/current-policy wording or version-neutral wording.

### F10 — Reference template still exposes retired Portuguese profile vocabulary

The current introduction says the PDF is configured with profile `tccgraduacao`, even though the v3 public profile is `undergraduate-capstone`.

**Classification:** clear documentation/API regression.

### F11 — Human control documents are too history-heavy for active execution

`AGENTS.md`, `docs/ROADMAP-V3.0.0.md`, and `release/v3-roadmap.json` preserve extensive implementation history inline. This is useful as evidence but makes the current work state unnecessarily difficult to read and encourages opaque names such as `R3-B2`, `V3-A1`, and `A1.2a`-style subdivisions.

**Action:** simplify the active plan. Historical SHAs/PRs remain available in Git, releases, issues, and closed PRs. The active control plane should retain only the certified checkpoints required to validate the current state.

### F12 — The scientific-article feature should not continue before foundation corrections close

A2 had not begun, so there is no benefit in layering a new profile on top of unresolved core/reference inconsistencies.

**Action:** defer scientific-article runtime until regression corrections and reference-PDF validation are green.

## Preliminary 34-point result

The consolidated review currently classifies the 34 items as:

- strong/pass: subtitle, co-advisor, concentration, committee capacity, CAPES guidance, summary position, acronym/symbol alignment, TOC exclusion, direct appendix/annex flow, citation capitalization, object single spacing, alínea mechanics, paragraph indent, and several modern bibliography behaviors;
- partial/reference gaps: department placeholder, full-name placeholder, committee acronym presentation, object sentence case, first UFC acronym introduction, long-quote locators/punctuation fixtures, source page guidance, heading examples, bibliography edge-case fixtures, and annex source guidance;
- direct implementation defect: title-page advisor punctuation;
- normative reconciliation required: object caption size, font-consistency interpretation, and selected NBR 6023 edge cases.

The authoritative item-by-item state is `docs/UFC-LIBRARIAN-REVIEW.md`.

## New readable execution plan

The opaque historical IDs remain historical references only. New active work should use the following human-readable phases and names.

| Phase | Name | Purpose | Exit condition |
|---|---|---|---|
| Phase 1 | **Regression Audit** | Revalidate current foundation, map all 34 review findings, identify untested or unjustified behavior. | Every finding has classification, owner, authority path, and acceptance evidence. |
| Phase 2 | **Core Corrections** | Correct foundation/template/test/normative defects found by Phase 1. | All non-deferred core findings are green; no unresolved authority conflict silently encoded. |
| Phase 3 | **Reference PDF Validation** | Compile canonical V3 reference and compare structure/presentation against the accepted UFC/V2.1 baseline and review contract. | Page-level visual checklist passes and every presentation rule has evidence. |
| Phase 4 | **Scientific Article** | Resume the previously planned scientific-article profile using the already reconstructed A1 authority contract. | Article profile runtime + article-specific positive/negative evidence pass. |
| Phase 5 | **Final Certification** | Re-run complete profile/engine/font/PDF/A/distribution certification on the corrected product. | Full certification matrix green on one immutable candidate SHA. |
| Phase 6 | **Release** | Prepare final documentation, bundles, release assets, and only then CTAN/release publication. | Release checklist complete; no unresolved roadmap or normative item. |

### Naming rule

New work items use descriptive names, for example:

- `Regression Audit — Front Matter`
- `Core Corrections — Object Typography`
- `Core Corrections — References`
- `Reference PDF Validation — Pre-textual Pages`
- `Scientific Article — Runtime Profile`

Do not create new opaque identifiers such as `A1.2a`, `B3-C2b`, or similar nested codes. A short internal issue number/PR number is sufficient for traceability.

Historical labels (`R1`, `R2`, `R3`, `R4`, `R5`, `A1`, `A2`) may be mentioned only to map old evidence to the new plan; they are not the naming system for new work.

## Phase 1 work packages

### Regression Audit — Control Plane

- verify branch/HEAD and machine/handoff/roadmap agreement;
- inventory active control files and remove stale current-state prose;
- define the atomic migration from old active stage names to the readable phase model;
- preserve only essential certified checkpoint references in active control files.

### Regression Audit — Normative Authority

- reconfirm current UFC institutional sources;
- reconfirm current applicable ABNT editions already catalogued;
- reconcile the 34 review items with current source precedence;
- specifically resolve object-caption 10 pt vs 12 pt and disputed NBR 6023 cases.

### Regression Audit — Front Matter

- cover/title/approval metadata and optional-line behavior;
- author/full-name placeholder;
- department optionality;
- subtitle;
- advisor/co-advisor punctuation;
- concentration;
- committee membership/institution acronym;
- summary/list/TOC positioning.

### Regression Audit — Text and Structure

- paragraph indentation and spacing;
- heading capitalization;
- acronym first use;
- alíneas/subalíneas;
- long quotations and citation punctuation;
- appendices/annexes.

### Regression Audit — Objects

- caption/title/source/note typography;
- single spacing;
- object-width binding;
- source and page locator;
- figures, tables, charts, code, algorithms.

### Regression Audit — References

- NBR 6023:2025 compatibility layer;
- thesis/dissertation fixtures;
- online unknown-place/publisher handling;
- standards and multivolume cases;
- DOI/URL/availability cases;
- repeated-author/entity cases.

### Regression Audit — Tests and Evidence

For each automatically enforceable requirement:

- positive fixture;
- negative fixture where practical;
- current-run evidence tied to the exact rule;
- canonical reference-PDF visual check for presentation requirements.

## Gate before Phase 2

Do not start broad corrective implementation until Phase 1 produces a closed audit matrix. Small obvious documentation defects may be prepared, but normative conflicts must remain fail-closed until authority is reconciled.

## Gate before Scientific Article

The scientific-article phase remains deferred until:

1. the 34-point review contract has no unexplained `FAIL` or `NORMATIVE-REVIEW` state affecting shared infrastructure;
2. stale V2/runtime-vocabulary reference defects are removed;
3. canonical V3 reference PDF passes the Phase 3 visual validation;
4. the control plane has been atomically migrated to the readable phase model.
