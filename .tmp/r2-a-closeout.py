from __future__ import annotations

import json
from pathlib import Path

MAIN_SHA = "0a2c2c3879986ca27b731f54b974db12524258df"
R1_CANDIDATE = "9b1752565ac217c04ffa22a9ef272cdf078af380"
R2_A_ISSUE = 232
R2_B1_ISSUE = 234


def replace_once(path: str, old: str, new: str) -> None:
    file_path = Path(path)
    text = file_path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{path}: expected one literal match, found {count}")
    file_path.write_text(text.replace(old, new, 1), encoding="utf-8")


def write_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


# API migration contract.
api_path = Path("release/v3-api-migration.json")
api = json.loads(api_path.read_text(encoding="utf-8"))
api["phase"] = "V3-R2"
api["status"] = "R2_A_DONE_R2_B1_ACTIVE"
api["current_stage"] = "R2-B1"
api["current_stage_goal"] = "canonical setup and internal state vocabulary"
api["r2_a_inventory"] = {
    "status": "DONE",
    "completed_at": "2026-09-02",
    "canonical_main_sha": MAIN_SHA,
    "r1_certified_candidate_sha": R1_CANDIDATE,
    "operational_issue": R2_A_ISSUE,
    "ownership_document": "docs/R2-API-OWNERSHIP.md",
    "findings": [
        "public-api.def is a forwarding-only canonical-English-to-Portuguese project API layer loaded last by the class",
        "behavior ownership is already distributed across responsibility modules and can be absorbed without adding another compatibility layer",
        "template/main.tex remains a Portuguese project-API consumer and must migrate atomically with each behavior lot",
        "integrations/abntexto.def overrides the project definition-list environment and must move atomically with that environment",
        "rendered Portuguese academic labels are domain content and are not migration targets",
        "genuine upstream non-English identifiers are retained only at explicit integration boundaries",
    ],
    "implementation_lots": {
        "R2-B1": {
            "status": "ACTIVE",
            "issue": R2_B1_ISSUE,
            "name": "canonical setup and internal state vocabulary",
        },
        "R2-B2": {
            "status": "PENDING",
            "name": "academic and front-matter public rendering API",
        },
        "R2-B3": {
            "status": "PENDING",
            "name": "structural/object environments optional object API and extension hooks",
        },
        "R2-B4": {
            "status": "PENDING",
            "name": "bibliography back-matter API and plumbing internalization",
        },
        "R2-B5": {
            "status": "PENDING",
            "name": "final consumer migration forwarding-layer removal and migration documentation",
        },
    },
}
write_json(str(api_path), api)

# Path migration contract remains live only for R2 runtime absorption.
path_file = Path("release/v3-path-migration.json")
path_contract = json.loads(path_file.read_text(encoding="utf-8"))
path_contract["phase"] = "V3-R2"
path_contract["status"] = "R1_PATHS_DONE_R2_RUNTIME_ABSORPTION_PENDING"
path_contract["current_stage"] = "R2-B1"
path_contract["r1_path_restructuring_status"] = "DONE"
path_contract["remaining_runtime_path_action"] = {
    "path": "abntexto-ufc/public-api.def",
    "action": "remove-after-absorption",
    "planned_lot": "R2-B5",
    "owner_inventory": "docs/R2-API-OWNERSHIP.md",
}
write_json(str(path_file), path_contract)

# Test migration contract now follows API-consumer migration.
test_file = Path("release/v3-test-migration.json")
test_contract = json.loads(test_file.read_text(encoding="utf-8"))
test_contract["phase"] = "V3-R2"
test_contract["status"] = "ACTIVE_R2_API_CONSUMER_MIGRATION"
test_contract["current_stage"] = "R2-B1"
test_contract["r1_reconciliation_status"] = "DONE"
test_contract["r2_api_consumer_policy"] = {
    "owner_inventory": "docs/R2-API-OWNERSHIP.md",
    "active_setup_consumer_migration_lot": "R2-B1",
    "final_portuguese_api_residual_closeout_lot": "R2-B5",
    "template_and_tests_move_atomically_with_runtime_owner": True,
    "compatibility_alias_tests_allowed": False,
}
write_json(str(test_file), test_contract)

# Machine roadmap.
road_file = Path("release/v3-roadmap.json")
road = json.loads(road_file.read_text(encoding="utf-8"))
road["updated_at"] = "2026-09-02"
road["phase"] = "V3-R2"
road["stage"] = "R2-B1"
road["stage_name"] = "canonical setup and internal state vocabulary"
road["active_branch"] = "main"
road["r2"] = {
    "status": "ACTIVE",
    "stage": "R2-B1",
    "stage_name": "canonical setup and internal state vocabulary",
    "entry_main_sha": MAIN_SHA,
    "r1_certified_candidate_sha": R1_CANDIDATE,
    "r2_a": {
        "status": "DONE",
        "issue": R2_A_ISSUE,
        "ownership_document": "docs/R2-API-OWNERSHIP.md",
        "result": "all current project-owned API/runtime surfaces classified by direct behavior owner and bounded implementation lot",
    },
    "lots": {
        "R2-B1": {"status": "ACTIVE", "issue": R2_B1_ISSUE, "name": "canonical setup and internal state vocabulary"},
        "R2-B2": {"status": "PENDING", "name": "academic and front-matter public rendering API"},
        "R2-B3": {"status": "PENDING", "name": "structural/object environments optional object API and extension hooks"},
        "R2-B4": {"status": "PENDING", "name": "bibliography back-matter API and plumbing internalization"},
        "R2-B5": {"status": "PENDING", "name": "final consumer migration forwarding-layer removal and migration documentation"},
    },
    "constraints": [
        "no blind global replacement",
        "producer state consumer template and tests move atomically",
        "preserve rendered Portuguese academic and official wording",
        "retain genuine upstream non-English identifiers only at explicit integration boundaries",
        "preserve normative rule IDs values tolerances locators and proof state absent new evidence",
        "do not add another runtime compatibility layer",
        "do not perform actual CTAN submission",
        "do not redistribute proprietary Microsoft fonts",
    ],
}
road["next_action"] = (
    "Execute V3-R2 / R2-B1 through issue #234 from canonical main. Move canonical English setup keys and values "
    "plus project-owned internal state/metadata vocabulary into their responsibility-owning modules, migrate every live "
    "state consumer/template/test atomically, and remove the migrated setup forwarding entries from public-api.def."
)
write_json(str(road_file), road)

roadmap = f"""# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-02

## Status

**V3-R1 DONE. V3-R2 ACTIVE — R2-B1 canonical setup and internal state vocabulary.**

Canonical `main` after R1 closeout: `{MAIN_SHA}`. Certified R1 product candidate: `{R1_CANDIDATE}`.

R2-A ownership inventory is DONE through issue #{R2_A_ISSUE}. Active implementation issue: #{R2_B1_ISSUE}. Machine authority: `release/v3-roadmap.json`.

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
| R1-B8 | DONE | candidate `{R1_CANDIDATE}` | Complete Windows/font/Unicode/embedding/PDF-A-2b certification | None |
| V3-R1 closeout | DONE | PR #233 → `{MAIN_SHA}` | R1 control plane closed; #227 completed | None |
| R2-A | DONE | issue #{R2_A_ISSUE}; `docs/R2-API-OWNERSHIP.md` | Direct owners, upstream boundaries and migration lots classified | None |
| R2-B1 | ACTIVE | issue #{R2_B1_ISSUE} | Canonical setup/internal state migration | Implement and validate |
| R2-B2 | PENDING | — | Academic/front-matter public rendering API | After B1 |
| R2-B3 | PENDING | — | Structural/object environments, optional object API and hooks | After B2 |
| R2-B4 | PENDING | — | Bibliography/back-matter API and plumbing internalization | After B3 |
| R2-B5 | PENDING | — | Final consumer migration, `public-api.def` removal and migration documentation | After B4 |
| V3-R3 | BLOCKED | — | Standards/tests/language semantic hardening | After R2 |
| V3-R4 | BLOCKED | — | Final certification | After R3 |
| V3-R5 | BLOCKED | — | Foundation freeze and final user/maintainer docs | After R4 |
| V3-A1/A2 | BLOCKED | — | Scientific-article work | After certified foundation |

## R1 certification record

R1-B8 certified the complete `template/main.tex` matrix on Windows run `33649620219` and final Linux inspection run `33655108349`. Literal institutional text-family identity, engine-appropriate math-font policy, Unicode extraction, full embedding and PDF/A-2b all passed. The final R1→R2 control-plane PR #233 passed `Static contract` run `33656361564` and `Linux integration` run `33656361474` with `PASS=30 FAIL=0 SKIP=0`, then merged at `{MAIN_SHA}`. Issue #227 is closed completed.

## R2 ownership result

`public-api.def` is confirmed as transitional forwarding debt rather than a true behavior owner. Canonical surfaces must move into the module that already owns the underlying behavior. `template/main.tex` and test consumers still use the Portuguese project API, so consumer migration is part of each behavioral lot rather than a final bulk replacement.

See `docs/R2-API-OWNERSHIP.md` for the direct-owner matrix, upstream-boundary classification and exact R2-B1…B5 sequence.

## Immediate action

Execute **R2-B1 issue #{R2_B1_ISSUE}**. Migrate canonical setup keys/values and internal state vocabulary with all live consumers atomically. Do not migrate unrelated public rendering commands, add runtime compatibility aliases, change normative semantics without new evidence, redistribute proprietary fonts, or perform actual CTAN submission.
"""
Path("docs/ROADMAP-V3.0.0.md").write_text(roadmap, encoding="utf-8")

handoff = f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-02

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- Canonical trunk: `main` at `{MAIN_SHA}` entering the R2-A closeout documentation lot.
- Phase: **V3-R2 ACTIVE**.
- Active stage: **R2-B1 — canonical setup and internal state vocabulary**.
- Active implementation issue: **#{R2_B1_ISSUE}**.
- R2-A inventory issue #{R2_A_ISSUE}: **DONE pending merge of this documentation closeout**.
- V3-R1 / R1-B8: **DONE**; issue #227 closed completed.
- Certified R1 product candidate: `{R1_CANDIDATE}`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, `AGENTS.md`, and `release/v3-api-migration.json` must agree. Disagreement fails closed.

## Stable foundation

All R1 structural, distribution, static-gate, permanent-workflow and Windows/literal-font/PDF-A certification blocks are complete. Permanent validation remains `make static-check`, `make check`, and `make release-check`, orchestrated by `Static contract`, `Linux integration`, and `Linux release check`.

The final R1→R2 PR #233 passed `Static contract` run `33656361564` and `Linux integration` run `33656361474` (`PASS=30 FAIL=0 SKIP=0`) before merging at `{MAIN_SHA}`.

## R2-A result

The ownership inventory is recorded in `docs/R2-API-OWNERSHIP.md`.

Key findings:

- `public-api.def` is loaded last and forwards canonical English surfaces to Portuguese project-owned behavior; it is transitional debt, not a final owner.
- Direct behavior already resides in responsibility modules.
- `core.def` owns the central Portuguese setup/state vocabulary consumed by layout, front matter and profile modules.
- `template/main.tex` remains a Portuguese API consumer, so template/tests migrate atomically with each owner lot.
- `integrations/abntexto.def` must move with the canonical definition-list environment because it overrides that environment for current LaTeX/ABNTexto behavior.
- Rendered Portuguese academic labels remain protected content.
- Genuine upstream non-English identifiers remain only at explicit integration boundaries.

## R2 implementation sequence

1. **R2-B1 / #234 — canonical setup and internal state vocabulary.** Direct English setup ownership; canonical document/profile state and metadata vocabulary; all state consumers/template/tests move atomically.
2. **R2-B2 — academic and front-matter public rendering API.** Direct canonical rendering commands plus layout-hook rebinding.
3. **R2-B3 — structural/object environments, optional object API and hooks.** Direct canonical environments, object APIs, extension hooks and project-owned object IDs; preserve upstream boundaries.
4. **R2-B4 — bibliography/back-matter API and plumbing internalization.** Direct bibliography/glossary/index commands and internal helper cleanup.
5. **R2-B5 — final consumer migration and forwarding-layer removal.** Remove `public-api.def`, finish residual scans, reconcile tests, and generate `docs/MIGRATING-TO-V3.md` without runtime aliases.

## Hard boundaries

- No blind global replacement.
- Producer/state consumer/template/test changes move together.
- No new compatibility alias layer.
- Preserve rendered Portuguese academic and official wording.
- Preserve normative rule IDs, expected values, tolerances, locators and proof state absent explicit new evidence.
- Do not rename genuine upstream identifiers solely for cosmetic consistency.
- Do not redistribute proprietary Microsoft fonts.
- Do not perform actual CTAN submission during R2 implementation.

## Immediate action

Execute R2-B1 through issue #234 from canonical `main` after this R2-A closeout merges. Start with a complete consumer inventory for core setup/state vocabulary, then change producers and consumers atomically and validate with the permanent gates.
"""
Path("docs/HANDOFF-V3.0.0.md").write_text(handoff, encoding="utf-8")

# Bootstrap state.
replace_once(
    "AGENTS.md",
    "- V3-R2 is ACTIVE in R2-A via issue #232. R2-A is inventory/classification and migration planning before behavioral changes.\n- `public-api.def` is transitional R2 debt. Final canonical public behavior must be implemented directly by responsibility-owning modules; removed Portuguese v2 project API is not retained through runtime aliases.\n- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state during R2-A unless explicit new evidence authorizes a normative change.",
    "- V3-R2 is ACTIVE in R2-B1 via issue #234. R2-A ownership inventory is complete and recorded in `docs/R2-API-OWNERSHIP.md`.\n- R2-B1 owns canonical setup keys/values and project-owned internal state/metadata vocabulary. Producers, state consumers, `template/`, and tests must move atomically; do not perform a blind global replacement.\n- `public-api.def` is transitional R2 debt. Remove migrated forwarding entries as each owner absorbs them; do not add a reverse compatibility layer. The file is removed completely in R2-B5.\n- Preserve rendered behavior and normative rule IDs, values, tolerances, locators and proof state during R2 unless explicit new evidence authorizes a normative change."
)
replace_once("AGENTS.md", "- Do not perform actual CTAN submission during R2-A.", "- Do not perform actual CTAN submission during R2 implementation.")

# README status.
replace_once(
    "README.md",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-A — runtime/API ownership inventory and migration plan, tracked by issue #232.**",
    "**V3-R1 is DONE. V3-R2 is ACTIVE in R2-B1 — canonical setup and internal state vocabulary, tracked by issue #234.**"
)
replace_once(
    "README.md",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 preserved the runtime/API while rebuilding and certifying the foundation. R2 is now active; R2-A performs ownership inventory and migration planning before any direct runtime/API migration.",
    "Project-owned technical surfaces use English. Brazilian academic content may remain in Portuguese where appropriate. R1 rebuilt and certified the foundation. R2-A has completed the runtime/API ownership inventory; R2-B1 now begins direct canonical setup/state migration through responsibility-owning modules. See `docs/R2-API-OWNERSHIP.md` for the bounded migration sequence."
)
replace_once(
    "README.md",
    "`TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. V3-R2/R2-A is active through issue #232.",
    "`TeXGyreTermesX-Regular` under pdfLaTeX is a legitimate `newtxmath` component, not institutional text fallback. R2-A ownership inventory is complete; V3-R2/R2-B1 is active through issue #234."
)

# Architecture sequencing without changing the target architecture.
arch_path = Path("docs/ARCHITECTURE.md")
arch = arch_path.read_text(encoding="utf-8")
marker = "## Upstream boundaries\n"
if marker not in arch:
    raise SystemExit("ARCHITECTURE.md: upstream boundary marker missing")
sequencing = """## R2 migration sequencing\n\nThe target architecture above is implemented through bounded owner-based lots documented in `docs/R2-API-OWNERSHIP.md`. R2-A classified the current forwarding surface and direct owners. R2-B1 migrates setup/state vocabulary first because those values are consumed across layout and profile modules; later lots migrate rendering commands, structural/object APIs, bibliography/back-matter APIs, and finally remove `public-api.def`. Template and test consumers move atomically with each behavior owner.\n\n"""
if "## R2 migration sequencing" not in arch:
    arch = arch.replace(marker, sequencing + marker, 1)
arch_path.write_text(arch, encoding="utf-8")

# CTAN guide current-development guard.
ctan_path = Path("docs/CTAN-RELEASE.md")
ctan = ctan_path.read_text(encoding="utf-8")
needle = "- Status: unofficial, community-maintained UFC-oriented class. Do not describe it as official or UFC-homologated unless the University explicitly grants that status.\n"
if needle not in ctan:
    raise SystemExit("CTAN-RELEASE.md: package status marker missing")
addition = needle + "- Development gate: V3-R2 runtime/API migration is active. A v3.0.0 CTAN upload must not be performed from an intermediate R2 lot; release publication remains a later explicit action after the roadmap reaches its release-ready stage and the intended release candidate is revalidated proportionally.\n"
ctan = ctan.replace(needle, addition, 1)
ctan_path.write_text(ctan, encoding="utf-8")
