# abntexto-ufc v2.2.0 — Canonical handoff

Updated: 2026-08-27
Checkpoint: PR #130 re-ported onto post-#135 stable main; exact-head validation pending
Stable main: `eb85ec78980bb3befd8f5d32cc9dd5c3c693fc37`
Stable-main LaTeX preflight: #958 / run id `33095342201` — SUCCESS
Stable-main distribution preflight: #225 / run id `33095333021` — SUCCESS

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
| N13 | negative fixtures / negative-path validation | ACTIVE — PR #130 typography re-port under exact-head validation |
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

## Stable-main compatibility and editorial baseline

PR #131 corrected abbreviation/symbol-list alignment without changing the normative contract.

PR #133 converted the v2.2 reference PDF into the commented UFC academic-work guide while preserving class behavior and normative values. It squash-merged as `2cbd6d00318ba906e225fa37a4efb724300c3b4e`.

PR #134 restored the LuaLaTeX/TeX Live 2025 Overleaf proxy using the stable CAPES catalog URL, without warning suppression or tolerance relaxation. It squash-merged as `d10d28607487c5a8d7bca325f48201c6deea8a77`.

PR #135 repaired only the reference-corpus observer assumptions exposed by real distribution runs #219–#223. It did not alter class implementation, document rendering, normative values, locators, N5 tolerances, proof-state or the N12-certified workflow.

PR #135 final evidence:

- exact audited head: `4c63b6aa9cc40d0b2213e2c67159edd42daa4ee9`;
- changed files: exactly `tests/v2-reference-corpus-check.sh` + this handoff;
- ordinary PR preflight #955 / run `33093045188` — SUCCESS;
- exact-head Gate T #956 / run `33093095476` — SUCCESS, including Overleaf/TeX Live 2025 and Windows literal-font certification;
- Distribution #224 / run `33093085284` — SUCCESS: release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy and candidate upload all green;
- squash merge: `eb85ec78980bb3befd8f5d32cc9dd5c3c693fc37`.

Post-merge stable-main evidence on `eb85ec78980bb3befd8f5d32cc9dd5c3c693fc37`:

- push LaTeX preflight #957 / run `33095333023` — SUCCESS;
- dispatched LaTeX preflight #958 / run `33095342201` — SUCCESS;
- reference document + PDF/A — SUCCESS;
- 12-profile matrix + PDF/A — SUCCESS;
- objects/bibliography — SUCCESS;
- post-textuals — SUCCESS;
- structural suite — SUCCESS;
- Overleaf/TeX Live 2025 proxy — SUCCESS;
- Windows literal Times New Roman/Arial build — SUCCESS;
- Windows literal font Unicode/embedding/PDF-A certification — SUCCESS;
- Distribution #225 / run `33095333021` — SUCCESS: Gate T, release preflight, PDF/A-2b, deterministic bundles, Overleaf import proxy and candidate upload all green.

The #135 regression is therefore closed. Do not reopen it without changed rendering, changed corpus predicate or a new reproducible regression.

## N13 — negative fixtures / validator sensitivity — ACTIVE

N13 tests validator sensitivity and does not create a second normative specification.

### Stable-main evidence already merged

PR #127 established the generic temporary-mutation harness and three controlled negative cases:

1. `page-margins-right` → `margin.recto.right`;
2. `short-direct-citation-quotes` → `citation.direct-short.quotation-marks`;
3. `ibge-table-open-sides` → `table.ibge.open-sides`.

PR #128 added the fourth controlled case and hardened evidence ordering in the N11 observer:

4. `project-required-resources` → `project.textual.required-sections`.

Stable main therefore currently contains four merged N13 negative cases. The fifth case is present only on the active PR #130 branch until that PR is exact-head validated and merged.

### PR #130 — typography negative path — RE-PORTED

Branch: `audit/n13-typography-negative-path`.

Post-#135 base: `eb85ec78980bb3befd8f5d32cc9dd5c3c693fc37`.

The re-port intentionally contains only three functional deltas plus this handoff synchronization:

1. `normativa/n13-negative-paths.json` adds mechanism `text-typography-extraction` as `REPRESENTED` and case `body-font-size`;
2. `tests/checks/normative_n13_campaign.py` expands the expected campaign scope without duplicating the generic executor;
3. `tests/v2-negative-paths-check.sh` routes the gate through the campaign adapter.

The controlled negative case temporarily renders `UFCNSevenBodyAlpha` at 14 pt instead of the normative 12 pt. The fixture must still compile successfully with pdfLaTeX. `tests/checks/normative_typography.py` must then reject the rendered PDF and emit:

`N7-EVIDENCE rule=font.size.body status=FAIL`

with a matching failed evidence record.

The earlier equivalent port on old base `d10d28607487c5a8d7bca325f48201c6deea8a77`, head `6a7835b1a89508a7b5854249660a575972fc4901`, had already produced:

- Normative source contract #311 / run `33081569884` — SUCCESS;
- LaTeX preflight #942 / run `33081569864` — SUCCESS;
- `body-font-size` — PASS with expected rule `font.size.body`;
- N13 summary — `PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
- positive N11 — 5/5 bounded coverage, `proof_state_changed=false`;
- structural suite — 14/14 PASS.

That old-base evidence is historical only. It cannot authorize the current merge. The final post-#135 head must independently reproduce the required evidence.

No class implementation, normative value, locator, N5 tolerance, compatibility mapping, N12-certified workflow or proof-state is changed by this port.

### Current mechanism inventory on PR #130

- `final-pdf-geometry` — REPRESENTED;
- `text-typography-extraction` — REPRESENTED by `body-font-size` on the PR branch;
- `citation-quotation-presentation` — REPRESENTED;
- `vector-rule-geometry` — REPRESENTED;
- `semantic-structural-observers` — REPRESENTED;
- `configuration-strict-rejection` — PREEXISTING_NEGATIVE; still needs machine-bound N13 receipt/evidence;
- `pdf-pdfa-validation` — INVENTORY_PENDING; still needs controlled structurally readable non-conformity and validator-specific rejection evidence.

N13 remains ACTIVE even after #130 unless the two residual mechanisms are reconciled.

### Remaining N13 sequence after #130

1. machine-bind `configuration-strict-rejection` using structured receipt/evidence from the existing strict font/configuration checks;
2. implement host-side PDF/A negative validation using a structurally readable PDF with controlled XMP non-conformity and veraPDF-specific rejection evidence;
3. rederive the complete mechanism inventory;
4. close N13 only if every declared mechanism is represented or explicitly reconciled;
5. only then advance to N14.

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

1. read the final PR #130 head after this handoff synchronization and require the diff against `main` to remain exactly four files;
2. require the three functional deltas to remain byte-equivalent in behavior to the previously audited typography port, with this handoff as the only documentation delta;
3. validate the exact final head through the Normative source contract and ordinary LaTeX preflight;
4. require `N13-EVIDENCE negative-case id=body-font-size status=PASS`;
5. require `N13-EVIDENCE negative-path-summary PASS=5 FAIL=0 selected=5 proof_state_changed=false`;
6. require positive N11 to remain 5/5 with `proof_state_changed=false`;
7. require structural suite green, final head unchanged and `behind_by=0`;
8. mark #130 ready and squash-merge using `expected_head_sha`;
9. inspect the resulting stable-main preflight before continuing N13;
10. add machine-bound `configuration-strict-rejection` evidence;
11. add controlled host-side PDF/A negative evidence;
12. reconcile the final N13 mechanism inventory and close N13 only if every declared mechanism is represented or explicitly reconciled;
13. advance to N14 only after formal N13 closure.
