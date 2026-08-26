# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-26
Checkpoint PR: #107
Audited base: `756f844f1606da9184ac66f300db4aefd4a38fe5`
N6 technical closure head: `5d1d9ba4aecba5519b600bfba4114009f551ea52`

This is the single dynamic continuation document for the v2.2.0 audit and release. Future work must read this file before relying on chat history. Detailed implementation evidence remains in Git history, pull requests, Actions runs, `normativa/` and `tests/`.

After this checkpoint is merged, the stable checkpoint is the squash-merge of PR #107 on `main`; resolve its exact SHA from Git history instead of adding a follow-up documentation-only commit merely to record the hash.

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
| N7 | layout, pagination, sections and footnotes | ACTIVE — residual rederivation required |
| N8 | citations and references | OPEN — partially executed ahead of sequence |
| N9 | objects, tables, equations and code | PENDING |
| N10 | post-textual elements and multivolume | PENDING |
| N11 | research-project profile / NBR 15287 | PENDING |
| N12 | profile, engine and font matrix | PENDING |
| N13 | negative fixtures / negative-path validation | PENDING |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure is therefore **7/16 phases = 43.75%**, with **56.25% of phase gates remaining**. This is a gate-count metric only; it is not a conformity or proof percentage.

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

### N7 — layout, pagination, sections and footnotes — ACTIVE

Last reconciled bounded positive coverage before N6 closure: **15/39 = 38.5%**. This count must now be rederived against the current full contract before any new N7 evidence PR is opened.

Already covered:

- section family: PRs #77, #79/#80, #82, #84, #86, #88, #90;
- body paragraph: #92;
- three core pagination predicates inherited from the pre-textual pagination scenario.

The 39-rule work map includes A4, recto/verso margins, text color, body font family/size, body spacing, paragraph behavior, reduced-size footnote/pagination contexts, section rules, pagination rules and footnotes.

Footnote provenance/classification work in PRs #46/#47 belongs to N1 evidence and does **not** substitute for bounded final-PDF N7 evidence. Explicit footnote predicates include simple spacing, the 5 cm separator and hanging alignment; rederive the full N7 residual before assuming these are the only missing rules.

Do not use the earlier `15/34` count.

### N8 — citations and references

Current bounded positive coverage: **12/19 = 63.2%**.

Citation predicates were executed ahead of canonical sequence by PRs #94, #96, #98, #100, #102 and #104. They remain valid evidence and are classified as N8 work; they do not alter the N7 gate.

References still require bounded reconciliation for layout, DOI and online-access predicates. The cross-cutting reduced-size long-quotation rule is also part of the N8 work map.

`abntexto-ufc/compat-nbr6023-2025.def` is active temporary compatibility code and must be explicitly audited during N8 rather than assumed correct because bibliography regressions pass.

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

N6 is closed. The only active roadmap gate is **N7 — layout, pagination, sections and footnotes**.

Before creating new N7 evidence, rederive the complete current N7 rule set from the full atomic contract and existing bounded evidence. Produce an exact covered/residual classification, reuse existing evidence only where it measures the exact predicate, and identify the smallest genuine residual scope for the next PR.

Do not open new N8 or N9 work until N7 is formally closed. After N7: N8 → N9 → N10 → N11 → N12 → N13 → N14 → N15 → D5 final → D6.
