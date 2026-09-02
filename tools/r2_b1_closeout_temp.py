#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
B1_MAIN_SHA = "ded5e77733795aa2958606e899d4e27f12f64df4"
B1_HEAD_SHA = "99fb58deaa1594ca19fb3a00ca9418623e5b25aa"


def replace_exact(path: str, old: str, new: str) -> None:
    target = ROOT / path
    text = target.read_text(encoding="utf-8")
    if old not in text:
        raise SystemExit(f"{path}: expected closeout anchor not found: {old!r}")
    target.write_text(text.replace(old, new, 1), encoding="utf-8")


def write(path: str, content: str) -> None:
    (ROOT / path).write_text(content.rstrip() + "\n", encoding="utf-8")


# Machine roadmap: preserve historical evidence and mutate only the active R2 control plane.
replace_exact("release/v3-roadmap.json", '  "stage": "R2-B1",\n  "stage_name": "canonical setup and internal state vocabulary",', '  "stage": "R2-B2",\n  "stage_name": "academic and front-matter public rendering API",')
replace_exact(
    "release/v3-roadmap.json",
    '  "next_action": "Execute V3-R2 / R2-B1 through issue #234 from canonical main. Move canonical English setup keys and values plus project-owned internal state/metadata vocabulary into their responsibility-owning modules, migrate every live state consumer/template/test atomically, and remove the migrated setup forwarding entries from public-api.def.",',
    '  "next_action": "Execute V3-R2 / R2-B2 through issue #237 from canonical main. Move the academic and front-matter public rendering commands into their responsibility-owning modules, rebind layout hooks to canonical commands, migrate template/test consumers atomically, and remove the corresponding Portuguese project commands and forwarding definitions without adding runtime aliases.",',
)
replace_exact("release/v3-roadmap.json", '    "stage": "R2-B1",\n    "stage_name": "canonical setup and internal state vocabulary",', '    "stage": "R2-B2",\n    "stage_name": "academic and front-matter public rendering API",')
replace_exact(
    "release/v3-roadmap.json",
    '      "R2-B1": {\n        "status": "ACTIVE",\n        "issue": 234,\n        "name": "canonical setup and internal state vocabulary"\n      },',
    '      "R2-B1": {\n        "status": "DONE",\n        "issue": 234,\n        "name": "canonical setup and internal state vocabulary",\n        "implementation_head_sha": "99fb58deaa1594ca19fb3a00ca9418623e5b25aa",\n        "merge_pr": 236,\n        "closure_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4",\n        "static_contract_run_id": 33668283912,\n        "linux_integration_run_id": 33668283890,\n        "linux_integration_job_id": 100375428004,\n        "linux_integration_result": "PASS=30 FAIL=0 SKIP=0",\n        "fail_closed_intermediate_run_id": 33665983360,\n        "fail_closed_intermediate_result": "PASS=24 FAIL=6 SKIP=0",\n        "dynamic_consumers_repaired": 6,\n        "runtime_alias_layer_added": false,\n        "normative_semantics_changed": false,\n        "proof_state_changed": false\n      },',
)
replace_exact(
    "release/v3-roadmap.json",
    '      "R2-B2": {\n        "status": "PENDING",\n        "name": "academic and front-matter public rendering API"\n      },',
    '      "R2-B2": {\n        "status": "ACTIVE",\n        "issue": 237,\n        "name": "academic and front-matter public rendering API",\n        "entry_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4"\n      },',
)
replace_exact("release/v3-roadmap.json", '      "R2-B3": {\n        "status": "PENDING",\n        "name": "structural/object environments optional object API and extension hooks"', '      "R2-B3": {\n        "status": "PENDING",\n        "issue": 238,\n        "name": "structural/object environments optional object API and extension hooks"')
replace_exact("release/v3-roadmap.json", '      "R2-B4": {\n        "status": "PENDING",\n        "name": "bibliography back-matter API and plumbing internalization"', '      "R2-B4": {\n        "status": "PENDING",\n        "issue": 239,\n        "name": "bibliography back-matter API and plumbing internalization"')
replace_exact("release/v3-roadmap.json", '      "R2-B5": {\n        "status": "PENDING",\n        "name": "final consumer migration forwarding-layer removal and migration documentation"', '      "R2-B5": {\n        "status": "PENDING",\n        "issue": 240,\n        "name": "final consumer migration forwarding-layer removal and migration documentation"')

# API migration contract: keep the mapping inventory intact and advance only execution state.
replace_exact("release/v3-api-migration.json", '  "status": "R2_A_DONE_R2_B1_ACTIVE",', '  "status": "R2_B1_DONE_R2_B2_ACTIVE",')
replace_exact("release/v3-api-migration.json", '  "current_stage": "R2-B1",\n  "current_stage_goal": "canonical setup and internal state vocabulary",', '  "current_stage": "R2-B2",\n  "current_stage_goal": "academic and front-matter public rendering API",\n  "current_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4",\n  "r2_b1_closeout": {"status": "DONE", "issue": 234, "pr": 236, "implementation_head_sha": "99fb58deaa1594ca19fb3a00ca9418623e5b25aa", "merge_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4", "static_run_id": 33668283912, "linux_integration_run_id": 33668283890, "linux_integration_result": "PASS=30 FAIL=0 SKIP=0", "normative_semantics_changed": false, "proof_state_changed": false},\n  "active_implementation_lot": {"stage": "R2-B2", "issue": 237},')

# Test/consumer contract follows the active behavioral lot.
replace_exact("release/v3-test-migration.json", '  "current_stage": "R2-B1",', '  "current_stage": "R2-B2",\n  "r2_b1_closeout": {"status": "DONE", "merge_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4", "linux_integration_run_id": 33668283890, "result": "PASS=30 FAIL=0 SKIP=0"},')
replace_exact("release/v3-test-migration.json", '"active_lot": "R2-B1"', '"active_lot": "R2-B2"')

# Path contract remains structurally complete; only runtime absorption advances.
replace_exact("release/v3-path-migration.json", '  "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_PENDING",', '  "status": "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_ACTIVE",')
replace_exact("release/v3-path-migration.json", '  "current_stage": "R2-B1",', '  "current_stage": "R2-B2",\n  "r2_b1_closeout": {"status": "DONE", "merge_main_sha": "ded5e77733795aa2958606e899d4e27f12f64df4", "next_lot": "R2-B2", "next_issue": 237},')

roadmap = r'''# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B2 academic and front-matter public rendering API.**

Canonical R2-B1 implementation checkpoint on `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`. Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

R2-A ownership inventory is DONE through issue #232. R2-B1 is DONE through issue #234 / PR #236. Active implementation issue: #237. Machine authority: `release/v3-roadmap.json`.

## Roadmap summary

| Stage | Status | Checkpoint / issue | Result | Remaining work |
|---|---|---|---|---|
| R1-S0 | DONE | repository sanitation | History governance rebaselined | None |
| R1-S1 | DONE | `1c7291592689f10a0e6fb043d404597ae8e53c02` | Control plane repaired | None |
| R1-S2 | DONE | `d7d4b9d2c04a032b76795cbdcae45c566fe3f7f1` | v3 promoted to `main` | None |
| R1-B1 | DONE | `f8509ba01a208b634c63a28b3c20cbf7ab8c75dd` | Canonical physical naming | None |
| R1-B2 | DONE | `03d7f5ceb1a325d26c712ba5e619ee85530a022b` | Legacy purge/minimization | None |
| R1-B3 | DONE | `7a3b018a43630ed46b375117790acc732ae67b40` | Semantic/path-consumer closure | None |
| R1-B4 | DONE | `1a126c37653728941ce1ada762376c5fec69cb02` | Tools/validator/metadata/language rebaseline | None |
| R1-B5 | DONE | `4bc0f544020234bc14a8f2261927f65721b6eddb` | Deterministic release/public bundles | Actual CTAN submission is a later explicit action |
| R1-B6 | DONE | `4c25c27b758e4b99db11187b34b9043776566871` | Permanent `make static-check` | None |
| R1-B7 | DONE | `d7327db7efd5cc1e0ff9255195bcb9767d853d3e` | Permanent optimized workflows | Optional branch-rule enforcement |
| R1-B8 | DONE | candidate `9b1752565ac217c04ffa22a9ef272cdf078af380` | Complete Windows/font/Unicode/embedding/PDF-A-2b certification | None |
| V3-R1 closeout | DONE | PR #233 → `0a2c2c3879986ca27b731f54b974db12524258df` | R1 control plane closed; #227 completed | None |
| R2-A | DONE | issue #232; `docs/R2-API-OWNERSHIP.md` | Direct owners, upstream boundaries and migration lots classified | None |
| R2-B1 | DONE | issue #234; PR #236 → `ded5e77733795aa2958606e899d4e27f12f64df4` | Canonical setup/internal state directly owned; final integration `PASS=30 FAIL=0 SKIP=0` | None |
| R2-B2 | ACTIVE | issue #237 | Academic/front-matter public rendering API | Direct ownership, consumer migration and validation |
| R2-B3 | PENDING | issue #238 | Structural/object environments, optional object API and hooks | After B2 |
| R2-B4 | PENDING | issue #239 | Bibliography/back-matter API and plumbing internalization | After B3 |
| R2-B5 | PENDING | issue #240 | Final consumer migration, `public-api.def` removal and migration documentation | After B4 |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final user/maintainer docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, full embedding and PDF/A-2b all passed. The final R1→R2 control-plane PR #233 passed `Static contract` run `33656361564` and `Linux integration` run `33656361474` with `PASS=30 FAIL=0 SKIP=0`, then merged at `0a2c2c3879986ca27b731f54b974db12524258df`. Issue #227 is closed completed.

## R2 progress record

R2-A established direct behavior ownership and the bounded B1–B5 sequence. `public-api.def` is transitional forwarding debt rather than a behavior owner.

R2-B1 moved canonical setup keys/values, project-owned document/profile state, metadata vocabulary, font/module state and all live setup/state consumers into direct ownership. The first complete integration run `33665983360` failed closed at `PASS=24 FAIL=6 SKIP=0`, exposing six dynamically generated legacy setup consumers. They were repaired before merge. Final head `99fb58deaa1594ca19fb3a00ca9418623e5b25aa` passed `Static contract` run `33668283912` and `Linux integration` run `33668283890`, job `100375428004`, at `PASS=30 FAIL=0 SKIP=0`; PR #236 then squash-merged to `main` at `ded5e77733795aa2958606e899d4e27f12f64df4`. Issue #234 is closed completed.

The pre-existing observational `FRONTMATTER-EVIDENCE` FAIL records remain baseline evidence behavior inside a passing aggregate gate and were not changed in B1 because no new normative evidence authorized a semantic change.

See `docs/R2-API-OWNERSHIP.md` for the direct-owner matrix, upstream-boundary classification and exact R2-B1…B5 sequence.

## Immediate action

Execute **R2-B2 issue #237** from canonical `main`. Move academic/front-matter canonical public rendering commands directly into `academic-works.def`, `research-projects.def`, and `frontmatter.def`; rebind `layout.def` hooks to canonical commands; migrate template/test consumers atomically; remove the corresponding Portuguese project commands and forwarding definitions. Preserve rendered Portuguese academic content, upstream boundaries and the normative proof state. Do not add runtime compatibility aliases, redistribute proprietary fonts or perform actual CTAN submission.
'''
write("docs/ROADMAP-V3.0.0.md", roadmap)

handoff = r'''# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- R2-B1 merged checkpoint on `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B2 — academic and front-matter public rendering API**.
- Active implementation issue: **#237**.
- R2-B1 issue #234: **DONE through PR #236**.
- R2-A inventory issue #232: **DONE through ownership inventory and closeout PR #235**.
- V3-R1 / R1-B8: **DONE**; issue #227 closed completed.
- Certified R1 product candidate: `9b1752565ac217c04ffa22a9ef272cdf078af380`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and `release/v3-api-migration.json` must agree. Disagreement fails closed.

## Stable foundation

All R1 structural, distribution, static-gate, permanent-workflow and Windows/literal-font/PDF-A certification blocks are complete. Permanent validation remains `make static-check`, `make check`, and `make release-check`, orchestrated by `Static contract`, `Linux integration`, and `Linux release check`.

R2-A classified direct behavior owners and upstream boundaries. R2-B1 then moved the complete canonical setup/internal-state vocabulary into those owners with all live consumers migrated atomically.

## R2-B1 closure evidence

- implementation head: `99fb58deaa1594ca19fb3a00ca9418623e5b25aa`;
- PR: #236;
- merged `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`;
- `Static contract`: run `33668283912`, PASS;
- first complete integration after migration: run `33665983360`, `PASS=24 FAIL=6 SKIP=0`, correctly fail-closed on six stale dynamic setup consumers;
- final `Linux integration`: run `33668283890`, job `100375428004`, `PASS=30 FAIL=0 SKIP=0`;
- issue #234: closed completed;
- no runtime alias layer introduced;
- no normative rule/value/tolerance/locator/proof-state change;
- no proprietary font redistribution;
- no CTAN submission.

The observational `FRONTMATTER-EVIDENCE` internal FAIL records seen inside the passing front-matter gate predate B1 and match the certified green baseline. They are not B1 regressions and remain outside this API migration lot absent new normative evidence.

## Current runtime/API state

`public-api.def` remains transitional R2 debt, but its setup-key forwarding responsibility was removed in B1. Canonical setup/state is now directly owned by `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`, with canonical consumers throughout layout/front matter/profile/template/test paths.

The remaining forwarding surface is bounded to later public commands/environments and helper debt. B2 now owns the academic/front-matter rendering commands and corresponding layout-hook rebinding. B3 owns structural/object environments/APIs/hooks, B4 owns bibliography/back-matter commands and plumbing internalization, and B5 owns the final residual consumer sweep plus removal of `public-api.def`.

## R2 implementation sequence

1. **R2-B1 / #234 — DONE.** Canonical setup and internal state vocabulary directly owned and fully validated.
2. **R2-B2 / #237 — ACTIVE.** Academic and front-matter public rendering API; direct canonical commands plus layout-hook rebinding and atomic consumer migration.
3. **R2-B3 / #238 — PENDING.** Structural/object environments, optional object API, extension hooks and project-owned object IDs.
4. **R2-B4 / #239 — PENDING.** Bibliography/back-matter API and plumbing internalization.
5. **R2-B5 / #240 — PENDING.** Final consumer migration, forwarding-layer removal, residual scan and `docs/MIGRATING-TO-V3.md`.

## Hard boundaries

- No blind global replacement.
- Producer/behavior owner/template/test changes move together.
- No new compatibility alias layer.
- Preserve rendered Portuguese academic and official wording.
- Preserve normative rule IDs, expected values, tolerances, locators and proof state absent explicit new evidence.
- Do not rename genuine upstream identifiers solely for cosmetic consistency.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission during R2 implementation.

## Immediate action

Execute R2-B2 through issue #237 from canonical `main`. Inventory the exact canonical/Portuguese academic and front-matter rendering command pairs plus layout hooks, then migrate each behavior owner and all template/test consumers atomically. Run `make static-check` and the permanent `Linux integration` gate before B2 closure.
'''
write("docs/HANDOFF-V3.0.0.md", handoff)

ownership = r'''# V3-R2 API Ownership Inventory

Updated: 2026-09-02

## Purpose

This document records the completed R2-A ownership inventory, the closed R2-B1 setup/state migration, and the bounded implementation order for the remaining v3 runtime/API migration. It is an engineering ownership map, not a normative formatting source.

R2-A entry checkpoint: `0a2c2c3879986ca27b731f54b974db12524258df`.
R2-B1 merged checkpoint: `ded5e77733795aa2958606e899d4e27f12f64df4`.
Authoritative migration contract: `release/v3-api-migration.json`.

## Current-state finding

`abntexto-ufc/public-api.def` remains a transitional forwarding layer loaded last by `abntexto-ufc.cls`, but B1 removed its setup-key forwarding responsibility. Canonical English setup/state is now directly owned by responsibility modules. The remaining forwarding debt is the public rendering/structural/object/bibliography/back-matter surface scheduled for B2–B5.

The editable reference document and tests have canonical B1 setup/state consumers but still contain Portuguese project rendering commands owned by later lots. Each remaining runtime lot therefore migrates the corresponding `template/` and test consumers atomically with the behavior owner.

## Responsibility ownership

| Runtime surface | Direct/current behavior owner | R2 responsibility/status |
|---|---|---|
| document type, print mode, cover/catalog-card/coat-of-arms policy, metadata, project predicates | `abntexto-ufc/core.def` | B1 DONE — direct canonical setup/state ownership |
| font family and strict-font policy | `abntexto-ufc/fonts.def` | B1 DONE — direct `font` / `strict-font` ownership |
| table/code/algorithm/glossary/index module selection | `abntexto-ufc/modules.def` | B1 DONE — canonical module keys/values |
| page geometry, duplex flow, front-matter breaks, structural list environments | `abntexto-ufc/layout.def` | canonical B1 state consumer; B2 layout-hook rebinding; B3 structural environments |
| approval/dedication/acknowledgments/epigraph/errata/summary/abstract/front-matter lists/TOC | `abntexto-ufc/frontmatter.def` | B2 ACTIVE — direct canonical rendering commands and front-matter API |
| institutional asset path | `abntexto-ufc/institutional.def` | B1 DONE — direct `coat-of-arms-file` ownership |
| academic cover/title/catalog card and initial page | `abntexto-ufc/academic-works.def` | B1 key/state DONE; B2 rendering commands ACTIVE |
| research-project cover/title specialization | `abntexto-ufc/research-projects.def` | canonical B1 state consumer; B2 canonical cover/title specialization ACTIVE |
| figures/charts/text tables/code/algorithms/source/note and optional object APIs | `abntexto-ufc/objects.def` | B3 PENDING |
| bibliography resource registration and reference section | `abntexto-ufc/bibliography.def` | B4 PENDING |
| glossary/index presentation | `abntexto-ufc/backmatter.def` | canonical B1 module-state consumer; B4 PENDING |
| current ABNTexto/LaTeX compatibility | `abntexto-ufc/integrations/abntexto.def` | retain genuine upstream adaptation; update canonical definition-list environment in B3 |
| forwarding-only canonical aliases | `abntexto-ufc/public-api.def` | setup forwarding removed in B1; progressively shrink B2–B4; remove completely in B5 |

## Upstream boundary classification

Non-English identifiers are not migrated merely because they are non-English when they are genuinely owned upstream. Current examples include ABNTexto-facing `grafico` / `quadro` identifiers and upstream public commands such as `\legend`, `\keywords`, `\appendix`, `\annex`, `\pretextual`, and `\textual` where required by the dependency contract.

Project-owned Portuguese identifiers remain migration targets. Portuguese public rendering commands/environments, project-owned object IDs, and project-owned pretextual/posttextual engineering terminology must not survive R2 as active project-owned engineering API. Rendered Portuguese labels remain protected document content.

## Migration lots

### R2-B1 — canonical setup and internal state vocabulary — DONE

Operational issue: #234. Implementation PR: #236. Merged `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`.

B1 moved all canonical setup keys/values into their direct owners in `core.def`, `fonts.def`, `modules.def`, `institutional.def`, and `academic-works.def`; migrated document/profile state, boolean/configuration state, metadata property keys and module state; updated all live consumers; and removed the migrated setup forwarding entries from `public-api.def`.

The first full post-migration integration run `33665983360` failed closed at `PASS=24 FAIL=6 SKIP=0`, exposing six stale dynamic test generators. After bounded repair, final implementation head `99fb58deaa1594ca19fb3a00ca9418623e5b25aa` passed `Static contract` run `33668283912` and `Linux integration` run `33668283890` at `PASS=30 FAIL=0 SKIP=0`. No normative semantics/proof state changed and no compatibility alias layer was introduced.

### R2-B2 — academic and front-matter public rendering API — ACTIVE

Operational issue: #237. Entry `main`: `ded5e77733795aa2958606e899d4e27f12f64df4`.

Move `\ufcPrintCover`, `\ufcPrintTitlePage`, `\ufcPrintApprovalPage`, `\ufcPrintCatalogCard`, dedication/acknowledgments/epigraph/errata, summary/abstract, front-matter lists, list entry and table-of-contents commands into `academic-works.def`, `research-projects.def`, and `frontmatter.def` as appropriate. Rebind `layout.def` command hooks to canonical commands and remove the corresponding Portuguese project commands and forwarding definitions atomically. Migrate template/test consumers with each owner.

### R2-B3 — structural/object environments, optional object API and extension hooks — PENDING

Operational issue: #238.

Make `ufclettereditems`, `ufcdashedsubitems`, `ufcdefinitionlist`, `ufcobject`, `ufclisting`, and `ufcalgorithm` the direct environments in their owners. Update `integrations/abntexto.def` together with `ufcdefinitionlist`. Move source/note/list-of-chart/code/algorithm and optional listing/minted APIs to direct canonical ownership. Rename project extension hooks to `\ufcSectionHook` and `\ufcObjectLegendHook`. Replace project-owned object IDs `codigo` / `algoritmo`; preserve genuine upstream `grafico` / `quadro` only at integration boundaries.

### R2-B4 — bibliography/back-matter API and plumbing internalization — PENDING

Operational issue: #239.

Move `\ufcAddBibliographyResource`, `\ufcPrintReferences`, `\ufcPrintGlossary`, and `\ufcPrintIndex` to direct ownership. Internalize non-semantic plumbing listed by the API contract, including layout/front-matter/back-matter heading and module-setup helpers. Preserve Portuguese rendered academic headings.

### R2-B5 — final consumer migration and forwarding-layer removal — PENDING

Operational issue: #240.

Migrate any remaining template/test/documentation consumers, remove `abntexto-ufc/public-api.def` from the tree and from `abntexto-ufc.cls`, run a fail-closed residual scan for project-owned Portuguese API/internal identifiers, reconcile `release/v3-test-migration.json`, and produce `docs/MIGRATING-TO-V3.md` from the authoritative old-to-new mappings. No runtime aliases are introduced.

## Cross-lot invariants

- Project-owned engineering identifiers are English; rendered Brazilian academic content remains in the language required by the document.
- No normative rule ID, expected value, tolerance, locator, or proof state changes without explicit new normative evidence.
- Producer/behavior owner, state consumer, template consumer and test consumer move together where applicable.
- No blind global replacement.
- No new Portuguese-to-English or English-to-Portuguese runtime compatibility layer.
- Upstream identifiers are changed only when the project owns them.
- Proprietary Microsoft fonts remain external and are never redistributed.
- CTAN submission remains an explicit later release action.
- `make static-check` and the permanent `Linux integration` gate validate each behavioral lot; heavier certification is rerun only when current-state changes require it.

## R2-A exit condition

R2-A is complete. The ownership map, machine contracts and control plane agree on the B1–B5 sequence. B1 is complete and B2/#237 is the sole active implementation lot.
'''
write("docs/R2-API-OWNERSHIP.md", ownership)

# Current repository-facing documentation receives narrow state edits.
replace_exact("README.md", '**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B1 — canonical setup and internal state vocabulary, tracked by issue #234.**', '**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B2 — academic and front-matter public rendering API, tracked by issue #237.**')
replace_exact("README.md", 'R1 rebuilt and certified the foundation. R2-A has completed the runtime/API ownership inventory; R2-B1 now begins direct canonical setup/state migration through responsibility-owning modules. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.', 'R1 rebuilt and certified the foundation. R2-A completed the runtime/API ownership inventory and R2-B1 completed direct canonical setup/state migration. R2-B2 now moves academic/front-matter rendering commands directly into responsibility-owning modules. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence.')
replace_exact("README.md", 'R2-A ownership inventory is complete; V3-R2/R2-B1 is active through issue #234.', 'R2-A ownership inventory and R2-B1 setup/state migration are complete; V3-R2/R2-B2 is active through issue #237. B1 merged through PR #236 at `ded5e77733795aa2958606e899d4e27f12f64df4` after final `Linux integration` `PASS=30 FAIL=0 SKIP=0`.')

replace_exact("AGENTS.md", '- V3-R2 is ACTIVE in R2-B1 via issue #234. R2-A ownership inventory is complete and recorded in `docs/R2-API-OWNERSHIP.md`.\n- R2-B1 owns canonical setup keys/values and project-owned internal state/metadata vocabulary. Producers, state consumers, `template/`, and tests must move atomically; do not perform a blind global replacement.', '- V3-R2 is ACTIVE in R2-B2 via issue #237. R2-A ownership inventory and R2-B1 setup/internal-state migration are complete and recorded in `docs/R2-API-OWNERSHIP.md`.\n- R2-B1 merged through PR #236 at `ded5e77733795aa2958606e899d4e27f12f64df4`; final `Linux integration` run `33668283890` passed `PASS=30 FAIL=0 SKIP=0`.\n- R2-B2 owns academic/front-matter public rendering commands and the corresponding layout-hook rebinding. Behavior owner, template consumers and tests move atomically; do not perform a blind global replacement.')

replace_exact("docs/ARCHITECTURE.md", 'The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A classified the current forwarding surface and direct owners. R2-B1 migrates setup/state vocabulary first because those values are consumed across layout and profile modules; later lots migrate rendering commands, structural/object APIs, bibliography/back-matter APIs, and finally remove `public-api.def`. Template and test consumers move atomically with each behavior owner.', 'The target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A classified the forwarding surface and direct owners. R2-B1 is complete: canonical setup/state vocabulary is directly owned and all live setup/state consumers use it. R2-B2 is active and migrates academic/front-matter rendering commands plus layout-hook consumers; later lots migrate structural/object APIs, bibliography/back-matter APIs, and finally remove `public-api.def`. Template and test consumers move atomically with each behavior owner.')

replace_exact("docs/CTAN-RELEASE.md", '- Development gate: V3-R2 runtime/API migration is active. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; release publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended release candidate is revalidated proportionally.', '- Development gate: V3-R2 runtime/API migration is active in R2-B2. R2-B1 setup/state migration is complete at `ded5e77733795aa2958606e899d4e27f12f64df4`. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; release publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended release candidate is revalidated proportionally.')

print("R2-B1 closeout and R2-B2 activation content prepared.")
