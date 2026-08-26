# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #107
Audited base: `555b538d7ef05eebfde88a3a3f1e92961f605019`
N6 technical closure head: `5d1d9ba4aecba5519b600bfba4114009f551ea52`
N7 technical closure merge: `555b538d7ef05eebfde88a3a3f1e92961f605019`

This is the single dynamic continuation document for the v2.2.0 audit and release. Future work must read this file before relying on chat history. Detailed implementation evidence remains in Git history, pull requests, Actions runs, `normativa/` and `tests/`.

The current stable audited base for N8 is the squash-merge of PR #112 on `main`, recorded above. Resolve later evidence merge SHAs from Git history instead of adding documentation-only commits merely to record hashes.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, source status, locators, precedence and proof policy.
2. `tests/` and GitHub Actions — executable evidence and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and next action.
6. Git/PR/Actions history — detailed historical evidence.

Historical release audits live under `docs/history/`. Distribution-only documents remain `docs/README-CTAN.md`, `docs/CHANGELOG-CTAN.md` and `docs/ctan-example.tex`.

## Governing audit policy

Keep three states separate:

- **positive coverage**: an exact predicate was exercised/measured;
- **phase gate**: all exit criteria of that roadmap phase were reconciled;
- **proof-state**: normative confidence classification under `normativa/proof-policy.json`.

A green CI job, a positive fixture or a closed phase does not by itself promote a rule to `PROVEN`.

Conservative rules remain mandatory:

- unavailable authoritative/licensed text stays unavailable or partial;
- evidence-only work does not silently change normative values, locators, N5 tolerances or compatibility mappings;
- fixture observations do not strengthen stored predicates;
- broad regressions count as support, not bounded phase closure, until mapped to the exact predicate;
- implementation defects exposed by evidence are fixed separately while preserving the evidence predicate;
- evidence is merged only on the exact audited head with `behind_by=0`;
- no closed scope is reopened without a changed source, changed predicate or regression.

## Canonical N0–N15 roadmap

The phase meanings come from the original planning branch `planning/v2.2.0-normative-verification` and are restored here as the canonical sequence:

| Phase | Scope | Gate status |
| --- | --- | --- |
| N0 | freeze / baseline | DONE |
| N1 | normative sources and exact locators | DONE |
| N2 | UFC × current-ABNT reconciliation | DONE |
| N3 | classify/resolve 46 explicit atomicity gaps | DONE |
| N4 | false-coverage audit and safe proof policy | DONE |
| N5 | final-PDF oracle construction/calibration | DONE |
| N6 | pre-textual elements | DONE |
| N7 | layout, pagination, sections and footnotes | DONE |
| N8 | citations and references | ACTIVE — 13/19 bounded after current reduced-size mapping |
| N9 | objects, tables, equations and code | PENDING |
| N10 | post-textual elements and multivolume | PENDING |
| N11 | research-project profile / NBR 15287 | PENDING |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is therefore **8/16 phases = 50%**, with **50% of phase gates remaining**. This is a gate-count metric only; it is not a conformity or proof percentage.

Historical fixture names and log prefixes containing `n6` / `N6-EVIDENCE` remain valid evidence identifiers. They are not renamed merely to repair roadmap labels.

## Baseline preserved from N0–N5 and N6 reconciliation

- full atomic rules: 181;
- normative rules: 170;
- N1 locator coverage: 170/170;
- N2 unknown-review relationships: 0;
- N3 explicit gaps resolved/classified: 46/46;
- N4 unsafe `PROVEN`: 0;
- current proof-state baseline after N6 validation-boundary reconciliation: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`;
- evidence origins: `atomic-parent=8`, `parent-inherited=91`, `rule-local-override=1`, `rule-local-promotion=81`;
- the sole current `rule-local-override` is `font.size.reduced.catalog-card`; it remains normatively 10 pt but is validated manually because the catalog card is supplied as an external PDF.

N5 tools: `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo`, `pdffonts`.

N5 tolerances remain unchanged:

- page size: 1 pt;
- horizontal position: 5 pt;
- vertical position: 5 pt;
- font size: 1 pt.

Key baseline PRs: #55 (N1), #56 (N2), #57 (N4), #58 (N5) and #107 (N6 closure reconciliation).

## Checkpoint audit findings

### N6 — pre-textuals — DONE

N6 is formally closed after reconciling the complete pre-textual scope against the existing bounded campaign and the remaining deposit/catalog-card boundaries.

Bounded positive evidence covers the planned pre-textual families: dedication, acknowledgements, short/long epigraph, summary/abstract/keywords, cover, title page, approval page, errata, optional lists, TOC, pre-textual pagination/start-side behavior and catalog-card interaction. The historical campaign remains represented by PRs #59–#75; PR #107 closes the remaining catalog-card classification boundary.

The closure classification is intentionally conservative:

- `deposit.catalog-card`: bounded positive evidence now exercises enabled and disabled routes across pdfLaTeX/LuaLaTeX and anverso/frente-verso;
- `font.size.reduced.catalog-card = 10 pt`: **MANUAL / external-pdf**. `\imprimirfichacatalografica` includes a supplied PDF with `pdfpages`; the class controls inclusion, physical placement and pagination but cannot restyle the PDF's internal typography;
- `deposit.approval-signatures`: **MANUAL** deposit evidence; no automatic proof is inferred from approval-page rendering;
- `deposit.capes`: **CONDITIONAL** on CAPES funding and retained as a deposit requirement rather than promoted by pre-textual rendering;
- research-project-specific cover/title-page/anonymization observations are support evidence only for the later N11 gate and do not close N11;
- no project-policy or later-phase predicate was promoted merely because a broad N6 fixture exercised it.

The N4 guardrail was extended, not weakened: `rule-local-override` is a whitelisted evidence-origin class and cannot independently yield `PROVEN`. The normative contract on the N6 closure head reports `unsafe-proven=0` and `PROVEN=0`.

N6 final technical validation on head `5d1d9ba4aecba5519b600bfba4114009f551ea52`:

- Normative source contract run `32957583127`: SUCCESS;
- LaTeX preflight run `32957582998`: all five effective jobs SUCCESS;
- structural job: `PASS=14 FAIL=0 SKIP=0`;
- catalog-card evidence: `deposit.catalog-card status=PASS measured=enabled-and-disabled-routes`;
- aggregate `latex-preflight`: SUCCESS;
- Windows literal-font and Overleaf-proxy jobs remained expected conditional skips.

Closing N6 changes the phase gate only. It does not promote any normative rule to `PROVEN`.

### N7 — layout, pagination, sections and footnotes — DONE

N7 was rederived against the full current contract as an exact **39-predicate** bounded work map and is formally closed at **39/39 positive bounded coverage**.

The pre-existing section, paragraph and pagination campaign was retained only where it measured the exact predicate. Subsequent bounded evidence completed footnotes, page/margin geometry, typography and the remaining pagination geometry without changing normative values or N5 tolerances.

Final N7 campaign details include:

- page A4 and recto/verso physical margins: PR #110;
- text color, body font family/size, body spacing and 10 pt pagination: PR #111;
- final six recto/verso pagination position and physical offset predicates: PR #112;
- literal Arial/Times New Roman identity remains certified by the dedicated Windows font path rather than inferred from Linux TeX Gyre fallback;
- final pagination offsets use the glyph box directly. The vertical measurement was `53.373 pt` against `56.6929 pt` expected, delta `3.3199 pt`, within the unchanged N5 vertical tolerance of `5 pt`; lateral offsets were effectively exact.

N7 final technical validation for PR #112:

- Normative source contract: SUCCESS;
- LaTeX preflight run `32968822105`: SUCCESS;
- structural job `98177477428`: `PASS=14 FAIL=0 SKIP=0`;
- exact audited head `32bd4be52ee85d22b86531d4c92337587efd65c4` was `behind_by=0` before merge;
- squash merge on `main`: `555b538d7ef05eebfde88a3a3f1e92961f605019`.

Closing N7 changes the phase gate and bounded coverage only. It does not promote any normative rule to `PROVEN`.

### N8 — citations and references — ACTIVE

The N8 scope was rederived against the current full contract after N7 closure. It contains exactly **19 predicates**:

- 7 citation-specific predicates previously exercised by PRs #94, #96, #98, #100, #102 and #104;
- 5 atomic `quotation.long.*` predicates already measured directly from final PDF;
- `font.size.reduced.long-quote` as a distinct cross-cutting predicate over the same 10 pt long-quotation context;
- 4 reference-layout predicates: `references.font.size`, `references.line-spacing`, `references.alignment`, `references.entry-spacing`;
- `references.doi.when-present`;
- `references.online.url-access`.

Before the current N8 branch, bounded positive coverage was **12/19 = 63.2%**: the 7 citation predicates plus the 5 direct long-quotation predicates.

The current bounded branch maps `font.size.reduced.long-quote` to the already measured `quotation.long.font.size` final-PDF samples while explicitly recording `independent_physical_sample=false`. It also binds the source evidence path and commit SHA, requires the two current normative contracts to agree at 10 pt, and preserves the historical N6 long-quotation oracle unchanged. When this branch is merged, bounded N8 coverage becomes **13/19 = 68.4%**, leaving **6/19**, all reference-specific.

The six residual reference predicates have different evidence types and should not be collapsed into one broad regression claim:

- the four layout predicates require bounded final-PDF geometry/typography measurement using N5 tolerances;
- DOI requires an applicable entry whose final rendered reference includes the DOI;
- online access requires final rendered availability plus access-date data when required.

Existing broad bibliography regressions remain support only until mapped to these exact IDs. `tests/v2-reference-spacing-check.sh` reports TeX/runtime dimensions but is not final-PDF N5 evidence. `tests/v2-references-6023-check.sh` already observes DOI and several NBR 6023 compatibility cases, but it does not by itself close both semantic predicates.

`abntexto-ufc/compat-nbr6023-2025.def` remains active temporary compatibility code. It must be explicitly audited during the final N8 semantic block rather than assumed correct because bibliography regressions pass. The compatibility layer currently adjusts specific missing-data/event/jurisdiction behaviors; general DOI/URL output remains largely delegated to `biblatex-abnt`, except where a driver explicitly invokes `doi+eprint+url`.

Do not use the earlier `12/18` count.

### Normative currency

The current repository state correctly records `ABNT NBR 14724:2024` with the corrected version dated 2025-04-01. No N1/N2 reopening is required for this point.

Current technical-edition policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`.

### M1 — validator Pages migration

M1 is **DONE**.

The current workflow uses Node 24 and the intended Pages actions. Main-branch run `32922391042` completed both `check` and `deploy`; the deployment log reports success and evaluates the environment URL as `https://tiagosombrra.github.io/modelo-latex-ufc/`.

### Distribution / CTAN track

- D0–D4: DONE.
- D5 rehearsal: validated historically in PR #36 only.
- D5 final: BLOCKED by N15.
- D6 CTAN resubmission: BLOCKED by final D5.

PR #36 must not become the final release branch. It is an old rehearsal and is far behind current `main`; create a fresh D5 final branch from the N15-approved SHA.

Issue #18 (bit-reproducible reference PDF metadata/ID) remains open and must receive an explicit release-blocking/non-blocking decision before final D5.

The UFC institutional mark remains in the source repository but is excluded from generated public/CTAN bundles. Documentation should say **externalized from public/CTAN bundles**, not removed from the repository.

## Documentation maintenance policy

Keep the active documentation surface small:

- `README.md` — user-facing usage and project entry point;
- `docs/NORMAS.md` — normative human map;
- `docs/VIGENCIA-NORMATIVA.md` — normative currency/precedence;
- `docs/HANDOFF-V2.2.0.md` — only dynamic roadmap/audit state document;
- `docs/README-CTAN.md`, `docs/CHANGELOG-CTAN.md`, `docs/ctan-example.tex` — distribution artifacts;
- `docs/history/` — immutable historical audits that still have archival value.

Do not add separate progress, checkpoint, status, roadmap or generic audit Markdown files when the information belongs in this handoff. Detailed evidence belongs in machine-readable files, tests, PRs and Actions logs.

## Commit and PR discipline

For roadmap work:

1. branch from the exact stable `main`;
2. define one bounded scope and its exact rule IDs;
3. add/update scenario, fixture, checker and gate only as required;
4. run the relevant source contract and CI;
5. verify the final PR head did not move and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. update this handoff only when the roadmap state or next action materially changes.

Do not create a documentation checkpoint after every evidence PR merely to record its merge SHA. PR history and Git already provide that detail.

## Next action

N7 is closed. The only active roadmap gate is **N8 — citations and references**.

After merging the current reduced-size mapping, create the smallest next bounded scope for the four reference-layout predicates only: 12 pt font size, simple internal spacing, left alignment and one blank simple-spaced line between entries. Use an isolated bibliography fixture and direct final-PDF measurement with the unchanged N5 tolerances; do not count existing log-level spacing checks as final-PDF proof.

Then close the two remaining semantic predicates (`references.doi.when-present` and `references.online.url-access`) with exact rendered-entry evidence and an explicit audit of `abntexto-ufc/compat-nbr6023-2025.def` boundaries.

Do not open N9 until N8 is formally closed. After N8: N9 → N10 → N11 → N12 → N13 → N14 → N15 → D5 final → D6.
