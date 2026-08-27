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
| N13 | negative fixtures / negative-path validation | ACTIVE — typography PR #130 validated, blocked by distribution hotfix #135 |
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

1. machine-bind `configuration-strict-rejection` using structured receipt/evidence from the existing strict font checks; `font-config` already executes before `negative-paths`, so the receipt can be consumed in the same coordinated gate without rerunning the expensive font matrix;
2. implement host-side PDF/A negative validation using a structurally readable PDF with controlled XMP non-conformity and veraPDF-specific rejection evidence;
3. rederive the complete mechanism inventory;
4. close N13 only if every declared mechanism is represented or explicitly reconciled;
5. only then advance to N14.

## Editorial v2.2 reference guide and compatibility baseline

PR #133 converted the v2.2 reference PDF into the commented UFC academic-work guide while preserving class behavior and normative values. It squash-merged as `2cbd6d00318ba906e225fa37a4efb724300c3b4e`.

The post-#133 full preflight #933 / run id `33076301572` exposed one LuaLaTeX/TeX Live 2025 overflow in the long direct CAPES Portaria nº 206/2018 URL. All other Linux, PDF/A, structural and Windows surfaces were green.

PR #134 fixed only that compatibility issue:

- final exact head: `05bf4c87ac4a7b711be71015c4b33222b53e67a2`;
- squash merge / current stable main: `d10d28607487c5a8d7bca325f48201c6deea8a77`;
- the bibliography uses the shorter official CAPES administrative-act catalog URL;
- no warning suppression or tolerance relaxation was introduced;
- the N12-certified `latex-preflight.yml` was not modified.

Full stable-main preflight #941 / run id `33080352548` is fully green, including reference/PDF-A, 12 profile PDFs/PDF-A, objects/bibliography, post-textuals, structural suite, Overleaf stable proxy, Windows literal-font build/certification and aggregate `latex-preflight`.

## PR #135 — distribution reference-corpus hotfix — ACTIVE

PR #135 is an isolated test-contract repair. It changes only `tests/v2-reference-corpus-check.sh` plus this canonical handoff. It must not alter class implementation, document rendering, normative values, locators, N5 tolerances, proof-state or the N12-certified workflow.

### Failure 1 — stale subsection case

Stable-main Distribution preflight #219 / run id `33080343888` exposed the first stale corpus expectation:

- Gate T prerequisite — SUCCESS;
- full `make preflight` — PASS=30, FAIL=1;
- only `Reference corpus` failed;
- checker expected `BASE NORMATIVA ADOTADA` although the guide source defines `\subsection{Base normativa adotada}`.

The first #135 repair changed only the obsolete body marker to the exact subsection title `Base normativa adotada`.

Normal PR preflight #943 passed. The ephemeral branch `release/v2.2.0-corpus-check` then ran the real distribution path on exact head `16d89a738d2c71f38d7e534a293229dd28a9dc70`:

- Gate T #944 / run id `33084632832` — fully SUCCESS, including Overleaf/TeX Live 2025 and Windows literal-font certification;
- Distribution #220 / run id `33084622421` — again PASS=30, FAIL=1, proving that the subsection-marker repair itself passed.

### Failure 2 — leader required on same physical line

The only #220 failure was:

`Corpus V2 falhou: líder pontilhado espaçado ausente em LISTA DE TABELAS: Tabela 1 — Organização didática dos componentes exercitados pelo documento de referência`

The long list entry wraps. The checker used `marker + [^\n]* + leader`, which incorrectly required marker, leader and page on one `pdftotext -layout` physical line.

The second repair bounded the search to one list entry and allowed continuation lines, preserving the rule that the failed entry cannot borrow the dotted leader from a following entry.

### Failure 3 — long marker itself required on one physical line

The second repair was tested on exact head `1c53ca774e4dcb20b8e5876d9c604a4d9304e226`.

Evidence on that SHA:

- normal PR LaTeX preflight #946 / run id `33086792227` — SUCCESS, including reference/PDF-A, 12 profile PDFs/PDF-A, objects/bibliography, post-textuals, structural suite and aggregate;
- Gate T #947 / run id `33087104736`, first attempt — every Linux job and Overleaf/TeX Live 2025 passed; Windows failed before template compilation because both configured CTAN installer sources failed to download `install-tl.zip`;
- #947 selective Windows rerun on the same SHA — SUCCESS; literal Times New Roman/Arial build passed, Unicode/embedding/PDF-A certification passed, and aggregate `latex-preflight` finished SUCCESS. This confirms the first Windows failure was transient external infrastructure, not a repository regression;
- Distribution #221 / run id `33087095185` — again PASS=30, FAIL=1. All checks except `Reference corpus` passed.

The exact #221 corpus failure was:

`Corpus V2 falhou: esperado exatamente uma entrada para LISTA DE TABELAS: Tabela 1 — Organização didática dos componentes exercitados pelo documento de referência; encontradas 0.`

Diagnosis: although the second repair allowed the dotted leader to appear on a continuation line, it still located the target by requiring the entire long marker to occur on one physical line. The long title itself wraps, so the target locator remained formatting-sensitive.

### Current robust parser design

Functional checker commit before this handoff synchronization: `0f00957e0a091f089cb40ea23916f8fe1d59295f`.

`require_dotted_entry` now treats each list item as a record rather than a physical line:

1. delimit the intended list block;
2. detect each entry start with `Figura|Tabela|Código|Algoritmo N — ...`;
3. collect all physical continuation lines until the next entry start;
4. normalize the complete entry record with the same PDF-text normalizer used elsewhere;
5. require exactly one normalized entry containing the exact expected marker;
6. require the spaced dotted leader plus page number inside that same normalized entry.

This supports wrapping in both the title and the leader while keeping entry boundaries strict. A target cannot borrow the leader or page number from the next entry. The requirement is not weakened; only the accidental dependency on `pdftotext` physical line wrapping is removed.

The current final PR head after this handoff synchronization must be read from PR #135 before validation/merge; do not reuse `1c53ca...` as final evidence because the checker has changed since that run.

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
2. validate the final #135 head through normal PR preflight;
3. point ephemeral `release/v2.2.0-corpus-check` to that exact head and run the real distribution path;
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
