# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: PR #135 distribution reference-corpus hotfix before final N13 typography merge
Stable main: `d10d28607487c5a8d7bca325f48201c6deea8a77`
Stable-main full preflight: #941 / run id `33080352548` — SUCCESS

This is the single dynamic continuation document for the v2.2.0 normative audit and release. Future work must read this file before relying on chat history. Detailed historical evidence belongs in `normativa/`, `tests/`, Git history, pull requests and GitHub Actions logs.

## Source-of-truth hierarchy

1. `normativa/*.json` — machine-readable requirements, locators, precedence, proof policy and phase manifests.
2. `tests/` + GitHub Actions — executable evidence, negative-path sensitivity and regressions.
3. `docs/NORMAS.md` — human-readable normative map.
4. `docs/VIGENCIA-NORMATIVA.md` — current-edition and precedence policy.
5. this handoff — roadmap state, audit decisions and immediate next action.
6. Git/PR/Actions history — detailed historical evidence.

Do not create generic progress/checkpoint Markdown files. Historical release audits belong under `docs/history/`.

## Governing audit policy

Keep three states separate:

- **positive coverage**: an exact predicate was exercised/measured;
- **phase gate**: all exit criteria of a roadmap phase were reconciled;
- **proof-state**: normative confidence under `normativa/proof-policy.json`.

A green CI job, positive fixture, negative fixture or closed phase does not by itself promote a rule to `PROVEN`.

Guardrails:

- unavailable authoritative/licensed text stays unavailable or partial;
- evidence-only work does not silently change normative values, locators, tolerances or compatibility mappings;
- fixture observations do not strengthen stored predicates;
- implementation defects exposed by evidence are fixed separately while preserving the predicate;
- evidence merges require the exact audited head and `behind_by=0`;
- no closed scope is reopened without changed source, changed predicate or regression;
- in N13, a rendered-PDF fixture that fails to compile is not evidence that an oracle rejected a normative violation;
- negative fixtures are instrumentation, not new normative requirements;
- do not modify the N12-certified `.github/workflows/latex-preflight.yml` during N13 evidence work unless N12 is explicitly reopened.

## Canonical N0–N15 roadmap

| Phase | Scope | Gate status |
| --- | --- | --- |
| N0 | freeze / baseline | DONE |
| N1 | normative sources and exact locators | DONE |
| N2 | UFC × current-ABNT reconciliation | DONE |
| N3 | classify/resolve 46 explicit atomicity gaps | DONE |
| N4 | false-coverage audit and safe proof policy | DONE |
| N5 | final-PDF oracle construction/calibration | DONE |
| N6 | pre-textual elements | DONE |
| N7 | layout, pagination, sections and footnotes | DONE — 39/39 bounded positive coverage |
| N8 | citations and references | DONE — 19/19 bounded positive coverage |
| N9 | objects, tables, equations and code | DONE — 23/23 bounded positive coverage |
| N10 | post-textual elements and multivolume | DONE — 20/20 bounded positive coverage |
| N11 | research-project profile / NBR 15287 | DONE — 5/5 bounded positive coverage |
| N12 | profile, engine and font matrix | DONE — 20-cell factorized certification + orthogonality gate |
| N13 | negative fixtures / negative-path validation | ACTIVE — typography PR #130 validated, blocked by #135 distribution hotfix |
| N14 | Web/Lite and CLI/Deep unification | PENDING |
| N15 | full normative certification and release decision | PENDING |

Formal roadmap closure remains **13/16 phases = 81.25%**. This is a phase-gate metric, not a normative-conformity or proof percentage.

## Frozen baseline and oracle policy

- full atomic rules: 181;
- normative rules: 170;
- N1 locator coverage: 170/170;
- N2 unknown-review relationships: 0;
- N3 explicit gaps resolved/classified: 46/46;
- N4 unsafe `PROVEN`: 0;
- proof-state baseline: `PARTIAL=113`, `NOT_PROVEN=51`, `CONDITIONAL=10`, `MANUAL=6`, `NOT_APPLICABLE=1`, `PROVEN=0`.

Frozen N5 tolerances remain unchanged:

- page size: 1 pt;
- horizontal position: 5 pt;
- vertical position: 5 pt;
- font size: 1 pt.

Core N5 tools remain `pdftotext -bbox-layout`, `pdftohtml -xml -zoom 1.0`, `pdfinfo` and `pdffonts`.

N9 added the calibrated `vector-rule-geometry` extension using `pdftocairo -svg`, no rasterization and same-run calibration. It did not change the N5 tolerances.

## Closed-phase certification notes

### N11 — research-project profile

N11 covers exactly five `project.*` predicates. The positive route remains **5/5 bounded positive coverage**. NBR 15287 locator limitations remain explicit and proof-state was not promoted by the positive campaign.

### N12 — compatibility matrix

N12 is closed as a factorized 20-cell certification:

- six profiles × two engines = 12 cells;
- portable `times`/`arial` × pdfLaTeX/LuaLaTeX = 4 cells;
- literal Windows Times New Roman/Arial × pdfLaTeX/LuaLaTeX = 4 cells.

The static orthogonality gate verifies that profile and font-family selection are independent axes. Literal Windows identity is certified only on the Windows route, never inferred from Linux fallback fonts.

The certified workflow blob `.github/workflows/latex-preflight.yml` remains SHA `aca746454be3ce2e650bd2f50d70b2f42d7d31e1`.

## N13 — negative fixtures / validator sensitivity — ACTIVE

N13 tests validator sensitivity and does not create a second normative specification.

### Stable-main evidence already merged

PR #127 established the generic temporary-mutation harness and three controlled negative cases:

1. `page-margins-right` → `margin.recto.right`;
2. `short-direct-citation-quotes` → `citation.direct-short.quotation-marks`;
3. `ibge-table-open-sides` → `table.ibge.open-sides`.

PR #128 added the fourth controlled case and hardened evidence ordering in the N11 observer:

4. `project-required-resources` → `project.textual.required-sections`.

PR #128 final exact head was `e7c69a4d974779bde5b04f71cf9b97b9f6cdc76c`, squash-merged as `9fee7c4b760bf4aaee5615f63e6b7e5f58e549a2`. Stable-main preflight #895 / run id `33058717022` was fully green, including Overleaf and Windows literal-font certification.

Current mechanism state:

- `final-pdf-geometry` — REPRESENTED;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `semantic-structural-observers` — REPRESENTED;
- `text-typography-extraction` — represented by PR #130 and exact-head validated, pending merge;
- `configuration-strict-rejection` — pre-existing behavior exists, but still needs machine-bound N13 receipt/evidence;
- `pdf-pdfa-validation` — still requires controlled structurally readable non-conformity and validator-specific rejection evidence.

### PR #130 — typography negative path

PR #130, branch `audit/n13-typography-negative-path`, was ported onto stable main `d10d28607487c5a8d7bca325f48201c6deea8a77` as head `6a7835b1a89508a7b5854249660a575972fc4901`. It contains only three N13 functional deltas plus handoff synchronization:

1. `normativa/n13-negative-paths.json` adds mechanism `text-typography-extraction` and case `body-font-size`;
2. `tests/checks/normative_n13_campaign.py` expands the expected campaign scope without duplicating the generic executor;
3. `tests/v2-negative-paths-check.sh` routes the gate through the campaign adapter.

The fifth controlled negative case temporarily renders `UFCNSevenBodyAlpha` at 14 pt, requires successful pdfLaTeX compilation, and requires `normative_typography.py` to reject `font.size.body` with `N7-EVIDENCE rule=font.size.body status=FAIL`.

Exact-head evidence on `6a7835b1a89508a7b5854249660a575972fc4901`:

- Normative source contract #311 / run id `33081569884` — SUCCESS;
- LaTeX preflight #942 / run id `33081569864` — SUCCESS;
- `body-font-size` — PASS with expected rule `font.size.body`;
- N13 summary — `PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
- positive N11 — 5/5 bounded coverage, `proof_state_changed=false`;
- structural suite — 14/14 PASS.

Do not merge #130 yet. PR #135 must change stable main first; #130 must then be ported once more to the resulting stable main and revalidated with `behind_by=0`.

No class implementation, normative values, locators, N5 tolerances, compatibility mappings, N12-certified workflow or proof-state are changed by the typography port.

### Remaining N13 sequence

After PR #130 is merged and confirmed on stable main:

1. machine-bind `configuration-strict-rejection` using structured receipt/evidence from the existing strict font checks;
2. implement host-side PDF/A negative validation using a structurally readable PDF with controlled XMP non-conformity and veraPDF-specific rejection evidence;
3. rederive the complete mechanism inventory;
4. close N13 only if every declared mechanism is represented or explicitly reconciled;
5. only then advance to N14.

## Editorial v2.2 reference guide and compatibility baseline

PR #133 converted the v2.2 reference PDF into the commented UFC academic-work guide while preserving class behavior and normative values. It squash-merged as `2cbd6d00318ba906e225fa37a4efb724300c3b4e`.

PR #134 fixed the LuaLaTeX/TeX Live 2025 overflow in the CAPES Portaria URL:

- final exact head `05bf4c87ac4a7b711be71015c4b33222b53e67a2`;
- squash merge / current stable main `d10d28607487c5a8d7bca325f48201c6deea8a77`;
- no warning suppression or tolerance relaxation;
- N12-certified `latex-preflight.yml` unchanged.

Stable-main full preflight #941 / run id `33080352548` is fully green, including reference/PDF-A, 12 profile PDFs/PDF-A, objects/bibliography, post-textuals, structural suite, Overleaf stable proxy, Windows literal-font build/certification and aggregate `latex-preflight`.

## PR #135 — distribution reference-corpus hotfix — ACTIVE

PR #135 is an isolated test-contract repair. It changes only `tests/v2-reference-corpus-check.sh` plus this canonical handoff. It must not alter class implementation, document rendering, normative values, locators, N5 tolerances, proof-state or the N12-certified workflow.

The real distribution path has successively exposed four formatting-sensitive assumptions in the same reference-corpus checker. In each case, the remaining 30 checks passed and no class/rendering regression was established.

### Failure 1 — stale subsection case

Distribution #219 / run id `33080343888`:

- Gate T — SUCCESS;
- `make preflight` — PASS=30, FAIL=1;
- checker expected obsolete `BASE NORMATIVA ADOTADA` although the guide source defines `\subsection{Base normativa adotada}`.

Repair: require exact current marker `Base normativa adotada`.

### Failure 2 — dotted leader required on same physical line

After failure 1, exact-head Gate T #944 / run id `33084632832` was fully green. Distribution #220 / run id `33084622421` again reached PASS=30, FAIL=1 and exposed a long `Tabela 1` entry whose leader appears on a continuation line.

Repair: bound the search to a single list entry and include its continuation lines, so an entry cannot borrow a leader from the next item.

### Failure 3 — long title itself required on one physical line

On exact head `1c53ca774e4dcb20b8e5876d9c604a4d9304e226`:

- normal PR preflight #946 / run id `33086792227` — SUCCESS;
- Gate T #947 / run id `33087104736` — SUCCESS after a selective Windows rerun; the first Windows attempt failed only because both CTAN installer sources failed before template compilation;
- Distribution #221 / run id `33087095185` — PASS=30, FAIL=1.

Failure: the complete long `Tabela 1 — Organização didática...` marker was still expected on one physical `pdftotext -layout` line.

Repair commit `0f00957e0a091f089cb40ea23916f8fe1d59295f`: parse each `Figura|Tabela|Código|Algoritmo N — ...` item as a bounded record, normalize all continuation lines, require exactly one matching title, and require leader/page within that same record.

### Failure 4 — helper accidentally required at least two leader dots

The bounded-record parser was tested on head `b1c4547c0c79d541116277b32fdb3ce07b1d5a45`.

Evidence:

- normal PR preflight #949 / run id `33089210989` — SUCCESS;
- Gate T #950 / run id `33089315096` — fully SUCCESS, including Overleaf/TeX Live 2025, Windows literal Times/Arial build, Unicode/embedding/PDF-A certification and aggregate;
- Distribution #222 / run id `33089302508` — Gate T SUCCESS, `make preflight` again PASS=30, FAIL=1.

Exact failure:

`Corpus V2 falhou: 1 entrada(s) do sumário sem líder pontilhado espaçado: ANEXO B — ORIENTAÇÃO PARA DOCUMENTO EXTERNO EM PDF .                                    53`

Diagnosis: `spaced_leader_pattern()` was `(?:\.\s+){1,}\.\s*\d+\s*$`, which requires at least two dot tokens because of the extra literal `\.` outside the repeated group. The long `ANEXO B` entry legitimately leaves room for only one leader dot before page 53.

Current repair commit before this handoff synchronization: `314d10a3d07cbbea0d568d3374eaf43474f1b6e3`.

The pattern is now `(?:\.\s+){1,}\d+\s*$`: one or more spaced leader dots followed by the page number. This preserves the dotted-leader requirement while removing the accidental minimum of two dots. It does not accept an entry with no dot.

### Current #135 contract

The checker now:

1. validates the exact current subsection marker;
2. treats list entries as bounded logical records rather than physical PDF-text lines;
3. allows title and leader wrapping within the same record;
4. requires the target title exactly once;
5. requires at least one dotted-leader token plus page number inside that same entry;
6. preserves all existing TOC/list case, alignment, corpus and navigation-file checks.

The final PR head after this handoff commit must be read from PR #135 before validation/merge. Do not reuse earlier SHAs as final evidence.

## Normative currency

The repository records `ABNT NBR 14724:2024`, corrected version dated 2025-04-01. Current-edition and precedence policy remains governed by `normativa/version-policy.json` and `docs/VIGENCIA-NORMATIVA.md`. No N1/N2 reopening is required at this checkpoint.

## M1 — validator Pages migration

M1 is DONE. The workflow uses Node 24 and the intended Pages actions.

## Distribution / CTAN track

- D0–D4: DONE;
- D5 rehearsal: historical PR #36 only;
- D5 final: BLOCKED by N15;
- D6 CTAN resubmission: BLOCKED by final D5.

Issue #18, bit-reproducible reference PDF metadata/ID, remains open and requires an explicit blocking/non-blocking release decision before final D5.

The UFC institutional mark remains in the source repository but is externalized from public/CTAN bundles; do not describe it as removed from the repository.

## PR discipline

For roadmap PRs:

1. branch from exact stable `main`;
2. derive exact bounded rule IDs, matrix cells or validator-mechanism cells from the current contract/implementation;
3. add only required scenario/fixture/checker/gate changes;
4. validate source contract and CI;
5. require final head unchanged and `behind_by=0`;
6. squash merge using `expected_head_sha`;
7. inspect the full stable-main push, including Overleaf and Windows literal fonts when applicable;
8. update this handoff whenever roadmap state, stable-main evidence or the immediate next action materially changes.

## Immediate next action

1. read PR #135 final head after this handoff commit and require the diff to remain exactly two files;
2. validate that exact head through normal PR preflight;
3. point ephemeral `release/v2.2.0-corpus-check` to the same SHA and run the real distribution path;
4. require Gate T fully green on that exact SHA, including Overleaf/TeX Live 2025 and Windows literal-font build/certification;
5. require distribution `make preflight` **31/31**, then release PDF/A, deterministic bundles, Overleaf import proxy and artifact upload all green;
6. require `behind_by=0`, mark #135 ready and squash-merge with `expected_head_sha`;
7. inspect resulting stable-main full preflight and distribution runs;
8. port only PR #130's three audited N13 functional deltas onto the resulting stable main and synchronize this handoff there;
9. on final #130 head require source contract green, `body-font-size` PASS, N13 summary 5/5, positive N11 5/5, ordinary preflight green and `behind_by=0`;
10. squash-merge #130 and inspect stable main;
11. continue N13 with machine-bound configuration-strict evidence;
12. add host-side PDF/A negative evidence;
13. perform final mechanism-inventory reconciliation and close N13 only if all declared mechanisms are represented or explicitly reconciled;
14. advance to N14 only after N13 closure.
