#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

CHECKPOINT = "4bc0f544020234bc14a8f2261927f65721b6eddb"

handoff = Path("docs/HANDOFF-V3.0.0.md")
text = handoff.read_text(encoding="utf-8")
text = text.replace(
    "- Active B6 work item: **B6-A — validation inventory and dependency classification**.\n- Active B6 focus: **classify current validation checks by dependency/runtime cost before designing the permanent cheap/static gate**.",
    "- Active B6 work item: **B6-B — canonical cheap/static validation gate**.\n- Active B6 focus: **implement one side-effect-free source-only gate from the completed B6-A dependency/runtime classification**.",
)
old = """## R1-BLOCK-6 — Permanent Cheap/Static Fail-Closed Gates

**ACTIVE.** Operational issue #207. Entry certified implementation checkpoint: `4bc0f544020234bc14a8f2261927f65721b6eddb`.

B6 begins with B6-A inventory/classification. The target is one permanent source-only/static gate contract that is deterministic and inexpensive enough for routine development and later B7 workflow reuse. Current integration-heavy validation remains separate. No GitHub Actions restoration belongs to B6.

- **B6-A ACTIVE / NEXT:** inventory current checks and measure runtime/dependencies/side effects; classify cheap/static vs bounded/heavy.
- **B6-B PENDING:** implement and reconcile the canonical cheap/static gate from the proven inventory.
- **B6-C PENDING:** residual audit, close B6 and hand orchestration to B7.
"""
new = """## R1-BLOCK-6 — Permanent Cheap/Static Fail-Closed Gates

**ACTIVE.** Operational issue #207. Entry certified implementation checkpoint: `4bc0f544020234bc14a8f2261927f65721b6eddb`.

B6 establishes one permanent source-only/static validation contract for routine development and later B7 workflow reuse while preserving the integration-heavy runner separately. GitHub Actions orchestration remains B7-owned.

- **B6-A DONE:** run `33525282652` inventoried 69 Python checkers, 74 shell integrations, four validator files and 26 broad-runner checks. Universal Python/JSON/shell/JS source syntax passed in about 2.6 s combined. Refinement run `33525499620` failed closed only to classify two exclusions: `frontmatter_definition_list_alignment.py` requires generated PDFs and `normative_configuration.py` writes evidence. Nineteen other measured candidates passed without working-tree side effects. Redundancy review proved `validator_source.py` already aggregates the central normative source/contract chain and its validator contract executes cross-surface vectors.
- **B6-B ACTIVE / NEXT:** issue #209; implement one canonical gate containing tracked Python/JSON/shell/JS syntax, `git diff --check`, canonical identity, repository contract, aggregate `validator_source.py`, normative objects scope and reference-guide contract, with before/after repository-status protection against gate-introduced side effects.
- **B6-C PENDING:** residual audit, close B6 and hand orchestration to B7.
"""
if old not in text:
    raise SystemExit("handoff B6 section did not match expected state")
text = text.replace(old, new)
text = text.replace(
    "- **R1-B6 ACTIVE** — permanent cheap/static fail-closed gates; B6-A inventory/classification.",
    "- **R1-B6 ACTIVE** — permanent cheap/static fail-closed gates; B6-A done, B6-B active.",
)
text = text.replace(
    "Start B6-A from canonical remote `main` using `4bc0f544020234bc14a8f2261927f65721b6eddb` as the latest certified implementation checkpoint and issue #207 as the operational log. Inventory `tests/checks/`, source-only portions of `tests/integration/`, `tests/run.py`, Makefile check/preflight entry points, validator/source contracts and syntax/static helpers. Measure dependencies/runtime and classify before designing the permanent cheap/static gate. Keep permanent workflow restoration in B7, final Windows/font/PDF-A certification in B8, actual CTAN submission outside B6, and V3-R2 runtime/API work out of scope.",
    "Start B6-B from canonical remote `main` using `4bc0f544020234bc14a8f2261927f65721b6eddb` as the latest certified implementation checkpoint, issue #207 as the Block 6 log and issue #209 as the implementation lot. Implement only the proven source-only composition from B6-A, keep the broad integration runner intact, and fail closed on any gate-introduced working-tree side effect. Keep permanent workflow orchestration in B7, final Windows/font/PDF-A certification in B8, actual CTAN submission outside B6, and V3-R2 runtime/API work out of scope.",
)
handoff.write_text(text, encoding="utf-8")

roadmap = Path("docs/ROADMAP-V3.0.0.md")
text = roadmap.read_text(encoding="utf-8")
text = text.replace(
    "**V3-R1 ACTIVE — R1-BLOCK-5 done; R1-BLOCK-6 active; B6-A inventory active.**",
    "**V3-R1 ACTIVE — R1-BLOCK-5 done; R1-BLOCK-6 active; B6-A done; B6-B active.**",
)
text = text.replace(
    "**ACTIVE / NEXT.** Inventory `tests/checks/`, source-only portions of `tests/integration/`, `tests/run.py`, Makefile check/preflight entry points, validator/source contracts and syntax/static helpers. Classify each candidate as cheap/static, bounded deterministic, or heavy/runtime/platform-dependent. No permanent workflow is created in this lot.",
    "**DONE.** Run `33525282652` inventoried 69 Python checkers, 74 shell integrations, four validator files and 26 broad-runner checks; universal tracked Python/JSON/shell/JS source syntax passed in about 2.6 s combined. Refinement run `33525499620` intentionally failed closed on two non-static candidates: `frontmatter_definition_list_alignment.py` requires generated PDF inputs and `normative_configuration.py` writes an evidence artifact. Nineteen other measured candidates passed without working-tree side effects. `validator_source.py` already aggregates the central normative source/contract chain and the validator contract executes cross-surface vectors, so B6-B must not duplicate those checks individually.",
)
text = text.replace(
    "**PENDING.** Implement the minimal fail-closed source-only gate and reconcile its producers/consumers/evidence based on B6-A findings.",
    "**ACTIVE / NEXT.** Issue #209. Implement one canonical side-effect-free source-only gate: tracked Python/JSON/shell/JS syntax, `git diff --check`, canonical identity, repository contract, aggregate validator-source contract, normative objects scope and reference-guide contract. Preserve `tests/run.py` as the broad integration runner and do not add permanent workflow orchestration in B6.",
)
text = text.replace(
    "- **R1-B6 ACTIVE** — permanent cheap/static fail-closed gates; B6-A inventory/classification.",
    "- **R1-B6 ACTIVE** — permanent cheap/static fail-closed gates; B6-A done, B6-B active.",
)
text = text.replace(
    "Start **B6-A** from canonical remote `main` with certified implementation checkpoint `4bc0f544020234bc14a8f2261927f65721b6eddb` and issue #207. Inventory and classify the current validation surface by dependency/runtime cost before changing any permanent gate: source-only/static checks belong to B6 candidates; TeX/PDF/network/Windows/font/final-certification work stays outside the cheap gate. B7 owns permanent workflow orchestration, B8 owns final Windows/font/PDF-A certification, and V3-R2 owns runtime/API migration.",
    "Start **B6-B** from canonical remote `main` with certified implementation checkpoint `4bc0f544020234bc14a8f2261927f65721b6eddb`, Block 6 issue #207 and implementation issue #209. Implement the proven source-only composition from B6-A with explicit no-side-effect protection and preserve the broad integration runner separately. B7 owns permanent workflow orchestration, B8 owns final Windows/font/PDF-A certification, and V3-R2 owns runtime/API migration.",
)
roadmap.write_text(text, encoding="utf-8")

machine = Path("release/v3-roadmap.json")
state = json.loads(machine.read_text(encoding="utf-8"))
block = state["blocks"]["R1-BLOCK-6"]
block["active_work_item"] = "B6-B"
block["active_sub_item"] = "B6-B"
block["planned_lots"]["B6-A"] = "DONE - validation inventory dependency measurement and cheap/static classification"
block["planned_lots"]["B6-B"] = "ACTIVE - canonical permanent cheap/static gate implementation and consumer reconciliation"
block["b6_a_status"] = "DONE"
block["b6_b_status"] = "ACTIVE"
block["b6_b_issue"] = 209
block["b6_a_validation_runs"] = [
    {
        "run_id": 33525282652,
        "conclusion": "success",
        "finding": "inventory classified 69 Python checkers, 74 shell integrations, four validator files and 26 broad-runner checks; universal source syntax/data candidates passed",
    },
    {
        "run_id": 33525499620,
        "conclusion": "failure",
        "finding": "classification failed closed only because one candidate requires generated PDF inputs and one candidate writes evidence; 19 other measured candidates passed without working-tree side effects",
    },
]
block["b6_a_results"] = {
    "python_checkers": 69,
    "shell_integrations": 74,
    "validator_files": 4,
    "broad_runner_registered_checks": 26,
    "raw_source_only_checker_candidates": 15,
    "raw_bounded_checker_candidates": 7,
    "raw_runtime_platform_checker_candidates": 47,
    "measured_candidate_count": 21,
    "measured_side_effect_free_pass_count": 19,
    "excluded_generated_pdf_input_check": "tests/checks/frontmatter_definition_list_alignment.py",
    "excluded_evidence_writer_check": "tests/checks/normative_configuration.py",
    "validator_source_is_aggregate": True,
    "validator_contract_executes_cross_surface": True,
    "permanent_workflow_added": False,
    "runtime_api_changed": False,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
}
state["next_action"] = (
    "Start R1-BLOCK-6 B6-B from canonical remote main using " + CHECKPOINT
    + " as the latest certified implementation checkpoint, issue #207 as the Block 6 log and issue #209 as the implementation lot. "
    "Implement one permanent side-effect-free source-only gate containing tracked Python/JSON/shell/JS syntax, git diff --check, canonical identity, repository contract, aggregate validator_source, normative objects scope and reference-guide contract. "
    "Preserve the broad integration runner separately. Keep permanent workflow orchestration in B7, final Windows/font/PDF-A certification in B8, actual CTAN submission outside B6 and V3-R2 runtime/API migration out of scope."
)
machine.write_text(json.dumps(state, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
