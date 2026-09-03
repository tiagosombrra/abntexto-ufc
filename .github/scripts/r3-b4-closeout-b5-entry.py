#!/usr/bin/env python3

import json
from pathlib import Path

B4_ENTRY = "f0b3df319501bef0a6257ac23d42f28c59ad73a0"
B4_HEAD = "4c22a9444db6720c0c8ae59ec8cec4bff6344672"
B4_MAIN = "59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390"
B4_BOUNDED_RUN = 33814870180
B4_STATIC_RUN = 33814977737
B4_LINUX_RUN = 33814977730
B4_LINUX_JOB = 100844995945
B4_RELEASE_RUN = 33816137774
B4_RELEASE_JOB = 100848593542


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def replace_required(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"required replacement missing: {label}")
    return text.replace(old, new, 1)


# AGENTS.md
path = "AGENTS.md"
text = read(path)
text = replace_required(
    text,
    "- R3-B4/#255 is ACTIVE. R3-B5/#256 remains pending. Do not start R4 until B5 records the immutable certification entry.",
    "- R3-B4/#255 is DONE through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. Permanent engineering-language enforcement reports zero Portuguese project-owned technical diagnostics, zero retired profile IDs, zero closed unconsumed migration contracts and two live API-migration consumers; residual scope is 305 sources (134 LaTeX + 171 engineering), test/check reachability is 148/148 with zero orphans, PR Linux passed `PASS=31 FAIL=0 SKIP=0`, and post-merge release run `33816137774` passed `PASS=33 FAIL=0 SKIP=0`. R3-B5/#256 is ACTIVE and owns R3 closeout plus the immutable R4 entry. Do not start R4 certification before B5 closes.",
    "AGENTS B4/B5 state",
)
write(path, text)

# README.md
path = "README.md"
text = read(path)
text = replace_required(
    text,
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A and R3-B1 through R3-B3 are DONE; R3-B4 engineering-language enforcement/contract consolidation is ACTIVE through issue #255.**",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE: R3-A and R3-B1 through R3-B4 are DONE; R3-B5 hardening closeout/R4 entry is ACTIVE through issue #256.**",
    "README headline",
)
text = replace_required(
    text,
    "R3-B4/#255 is active. The certified R1 candidate remains",
    "R3-B4/#255 closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`: the executable engineering-language contract is green, the permanent residual scope is 305 sources (134 LaTeX + 171 engineering), retained test/check reachability is 148/148 with zero orphans, PR Linux passed `PASS=31 FAIL=0 SKIP=0`, and post-merge Linux release `33816137774` / job `100848593542` passed `PASS=33 FAIL=0 SKIP=0`. R3-B5/#256 is active. The certified R1 candidate remains",
    "README B4 facts",
)
text = replace_required(
    text,
    "R3-B3/#254 is complete; R3-B4/#255 is active and R3-B5/#256 remains ordered after it.",
    "R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 is active and owns final R3 reconciliation plus the exact R4 certification entry.",
    "README policy state",
)
write(path, text)

# docs/ARCHITECTURE.md
path = "docs/ARCHITECTURE.md"
text = read(path)
text = replace_required(
    text,
    "R3-B4/#255 is active. Remaining R3 architecture work is engineering-language/closed-contract enforcement followed by B5 closeout/R4 entry.",
    "R3-B4/#255 is DONE through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`; the permanent engineering-language checker, canonical technical profile IDs and closed-contract consumer audit are part of the source-only contract. Its B4 baseline is 305 residual-scanned sources, 148/148 retained scripts reachable and zero orphans. R3-B5/#256 is ACTIVE and owns only R3 closeout/R4 entry.",
    "ARCHITECTURE state",
)
text = replace_required(
    text,
    "R3-B4 now owns executable engineering-language enforcement and closed-contract consolidation.",
    "R3-B4 made engineering-language enforcement and closed-contract consolidation executable without changing normative semantics, proof-state defaults or the public runtime API. R3-B5 now owns final cross-surface reconciliation and the immutable R4 entry checkpoint.",
    "ARCHITECTURE B5 ownership",
)
write(path, text)

# docs/CTAN-RELEASE.md
path = "docs/CTAN-RELEASE.md"
text = read(path)
text = replace_required(
    text,
    "R3-B4/#255 is active and B5 remains required before R4.",
    "R3-B4/#255 is complete through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`; post-merge release run `33816137774` passed `PASS=33 FAIL=0 SKIP=0`. R3-B5/#256 is active and remains required before R4.",
    "CTAN development gate",
)
write(path, text)

# docs/ENGINEERING-LANGUAGE.md
path = "docs/ENGINEERING-LANGUAGE.md"
text = read(path)
text = replace_required(
    text,
    "R3-B4/#255 still owns the scoped permanent language-enforcement repair.",
    "R3-B4/#255 closed the scoped permanent language-enforcement repair through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`.",
    "ENGINEERING-LANGUAGE ownership",
)
text = text.replace("expanding removed-v2 residual enforcement across 303 behavior-relevant sources", "expanding removed-v2 residual enforcement across 302 behavior-relevant sources")
text = replace_required(
    text,
    "R3-B4/#255 is now active and owns the scoped permanent engineering-language source checker, technical identifier migration, and closed-contract audit.",
    "R3-B4/#255 is DONE. The permanent B4 contract reports zero Portuguese project-owned technical diagnostics, zero retired profile IDs, zero closed unconsumed contracts and two live `release/v3-api-migration.json` consumers. The current B4 residual baseline is 305 sources (134 LaTeX + 171 engineering), retained test/check reachability is 148/148 with zero orphans, and rendered academic Portuguese remains explicitly protected. R3-B5/#256 is ACTIVE and owns R3 closeout/R4 entry; it must not broaden this policy or change the public runtime API.",
    "ENGINEERING-LANGUAGE B4 closeout",
)
write(path, text)

# docs/HANDOFF-V3.0.0.md -- rewrite as exact current continuation point.
write(
    "docs/HANDOFF-V3.0.0.md",
    f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-03

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **ACTIVE — R3-A and R3-B1 through R3-B4 DONE; R3-B5 ACTIVE**.
- R3-B4/#255 implementation head: `{B4_HEAD}`.
- R3-B4 PR #264 merge/main SHA: `{B4_MAIN}`.
- R3-B4 bounded validation: `{B4_BOUNDED_RUN}` — engineering-language self-test/audit and `make static-check` PASS.
- R3-B4 PR Static contract: `{B4_STATIC_RUN}` — PASS.
- R3-B4 PR Linux integration: `{B4_LINUX_RUN}` / job `{B4_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`.
- R3-B4 post-merge Linux release: `{B4_RELEASE_RUN}` / job `{B4_RELEASE_JOB}` — `PASS=33 FAIL=0 SKIP=0`.
- R3-B4 permanent baseline: 305 residual-scanned sources (134 LaTeX + 171 engineering); 148/148 retained test/check scripts reachable; zero orphans; zero Portuguese project-owned technical diagnostics; zero retired profile IDs; zero closed unconsumed migration contracts; two live `v3-api-migration` consumers.
- Active stage: **R3-B5 — R3 closeout and exact R4 certification entry**.
- Active issue: **#256**.
- B5 entry product checkpoint: `{B4_MAIN}`; the canonical B5 control-plane checkpoint is the merge produced by this B4→B5 reconciliation.
- Certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md` and `AGENTS.md` must agree. Disagreement fails closed.

## What R3-B4 established

The English-first engineering-language policy is executable rather than aspirational. `tests/checks/engineering_language.py` is part of `make static-check`, project-owned technical profile/scenario IDs use canonical v3 English values, and technical diagnostics/comments are English while rendered academic Portuguese, official/normative wording, bibliography data, literal output under test and genuine upstream boundaries remain protected.

The consumer audit retained `release/v3-api-migration.json` because permanent checks consume it and removed the closed, unconsumed `release/v3-test-migration.json` and `release/v3-path-migration.json` contracts. No normative authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered-format requirement or public runtime API changed.

## R3 lots

| Lot | Issue | Status | Purpose |
|---|---:|---|---|
| R3-B1 | #252 | DONE | front-matter evidence truthfulness and fail-closed enforcement |
| R3-B2 | #253 | DONE | normative proof-state and coverage semantics |
| R3-B3 | #254 | DONE | semantic test integrity and expanded residual enforcement |
| R3-B4 | #255 | DONE | engineering-language enforcement and closed-contract consolidation |
| R3-B5 | #256 | ACTIVE | R3 closeout and exact R4 certification entry |

## Immediate action

Execute issue #256 from the canonical B4→B5 control-plane checkpoint. Reconcile every control-plane surface, prove that evidence semantics remain truthful, run `make static-check` and full `make check` on the final R3 candidate, verify temporary workflows/executors and cleanup-only migration artifacts are absent, and record the exact immutable R4 entry SHA. Do not perform the R4 Windows/literal-font certification inside B5.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative rule IDs, values, locators, tolerances, applicability or proof state without current evidence. `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain unchanged because B4 introduced no new normative source/currency facts. `docs/MIGRATING-TO-V3.md` remains unchanged because B4 changed no public runtime API. Do not start R4 certification, R5 foundation freeze, V3-A1/A2 scientific-article work or CTAN submission before their recorded entry conditions.
""",
)

# docs/ROADMAP-V3.0.0.md
path = "docs/ROADMAP-V3.0.0.md"
text = read(path)
text = replace_required(
    text,
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 DONE; R3-B4 ACTIVE.**",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 DONE; R3-B4 DONE; R3-B5 ACTIVE.**",
    "ROADMAP headline",
)
text = replace_required(
    text,
    "Active implementation issue: #255. Machine authority: `release/v3-roadmap.json`.",
    f"R3-B4/#255 closed through PR #264 at `{B4_MAIN}`: bounded run `{B4_BOUNDED_RUN}` PASS; Static `{B4_STATIC_RUN}` PASS; Linux `{B4_LINUX_RUN}` / job `{B4_LINUX_JOB}` = `PASS=31 FAIL=0 SKIP=0`; post-merge release `{B4_RELEASE_RUN}` / job `{B4_RELEASE_JOB}` = `PASS=33 FAIL=0 SKIP=0`. Permanent B4 baseline is 305 sources (134 LaTeX + 171 engineering), 148/148 retained scripts reachable, zero orphans, zero Portuguese technical diagnostics, zero retired profile IDs and zero closed unconsumed contracts. Active implementation issue: #256. Machine authority: `release/v3-roadmap.json`.",
    "ROADMAP status paragraph",
)
text = replace_required(
    text,
    "| R3-B4 | ACTIVE | issue #255; entry `fbee5bd329f98a389c2880932af40547c8d1674e` | engineering-language enforcement + contract consolidation | enforce scoped English engineering policy; migrate technical profile IDs; audit closed migration-contract consumers |\n| R3-B5 | PENDING | issue #256 | R3 closeout and immutable R4 entry | after B4 |",
    f"| R3-B4 | DONE | issue #255; PR #264; canonical entry `{B4_ENTRY}`; merge `{B4_MAIN}` | permanent engineering-language enforcement; canonical profile IDs; closed-contract consolidation; PR `31/0/0`; release `33/0/0` | None |\n| R3-B5 | ACTIVE | issue #256; entry `{B4_MAIN}` | R3 closeout and immutable R4 entry | reconcile final candidate; run Static + full Linux; record exact R4 entry SHA |",
    "ROADMAP table",
)
text = replace_required(
    text,
    "## R3-B4 entry",
    "## R3-B4 closeout",
    "ROADMAP B4 heading",
)
old_b4_para = "R3-B4/#255 starts from product checkpoint `fbee5bd329f98a389c2880932af40547c8d1674e`. It owns executable engineering-language enforcement, consumer-safe migration of project-owned Portuguese technical profile/scenario identifiers to canonical English terminology, translation of project-owned technical diagnostics/comments/UI while protecting rendered Brazilian academic content and genuine upstream boundaries, and the consumer audit/consolidation of closed migration contracts. `release/v3-api-migration.json` remains retained because the permanent residual gate consumes it."
new_b4_para = f"R3-B4/#255 entered canonically from `{B4_ENTRY}`, implemented on `{B4_HEAD}` and squash-merged through PR #264 at `{B4_MAIN}`. `tests/checks/engineering_language.py` is now a permanent static contract; project-owned technical profile IDs use canonical v3 values; academic/normative/bibliographic Portuguese remains protected; `release/v3-api-migration.json` is retained for its two permanent consumers; and the two closed unconsumed migration contracts were removed. The permanent baseline is 305 residual-scanned sources and 148/148 reachable retained scripts with zero orphans. Static, PR Linux and post-merge release are green, and no normative semantics, proof-state defaults or public runtime API changed."
text = replace_required(text, old_b4_para, new_b4_para, "ROADMAP B4 paragraph")
text = replace_required(
    text,
    "## Immediate action\n\nExecute **R3-B4 / issue #255** from `fbee5bd329f98a389c2880932af40547c8d1674e`. Inventory the remaining project-owned Portuguese engineering vocabulary and consumers of `release/v3-test-migration.json` / `release/v3-path-migration.json`, then implement a scoped permanent language gate with explicit academic/normative/upstream exemptions. Do not start R3-B5, R4, R5, V3-A1/A2, or CTAN submission before their recorded entry conditions.",
    f"## R3-B5 entry\n\nR3-B5/#256 starts after this B4→B5 control-plane checkpoint, from product SHA `{B4_MAIN}`. It owns final R3 reconciliation, truthful-evidence confirmation, `make static-check`, full `make check`, temporary-executor/migration-artifact absence, and recording the exact immutable R4 certification entry. It must not perform R4 certification.\n\n## Immediate action\n\nExecute **R3-B5 / issue #256** from the canonical B4→B5 checkpoint. Do not start R4 final certification, R5, V3-A1/A2, or CTAN submission before B5 records the immutable R4 entry.",
    "ROADMAP immediate action",
)
write(path, text)

# docs/R3-HARDENING-INVENTORY.md
path = "docs/R3-HARDENING-INVENTORY.md"
text = read(path)
text = replace_required(
    text,
    "R3-B4/#255 is active.",
    f"R3-B4/#255 is closed through PR #264 at `{B4_MAIN}`. R3-B5/#256 is active.",
    "R3 inventory intro",
)
insert_after = "- normative semantics / proof-state defaults / public runtime API changed: **no**.\n\n## Findings resolved"
b4_section = f"- normative semantics / proof-state defaults / public runtime API changed: **no**.\n\n## R3-B4 closeout evidence\n\n- canonical B4 entry/control-plane checkpoint: `{B4_ENTRY}`;\n- final implementation head: `{B4_HEAD}`;\n- merge/main SHA: `{B4_MAIN}`;\n- issue / PR: #255 / #264;\n- bounded validation run: `{B4_BOUNDED_RUN}` — PASS;\n- PR Static contract: `{B4_STATIC_RUN}` — PASS;\n- PR Linux integration: `{B4_LINUX_RUN}` / job `{B4_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`;\n- post-merge Linux release: `{B4_RELEASE_RUN}` / job `{B4_RELEASE_JOB}` — `PASS=33 FAIL=0 SKIP=0`;\n- engineering-language audit: Portuguese technical diagnostics=0, retired profile IDs=0, closed unconsumed contracts=0, live API-contract consumers=2;\n- permanent residual scope: 134 LaTeX + 171 engineering = 305 sources;\n- test surface: 148/148 retained scripts reachable, zero orphaned;\n- normative semantics / proof-state defaults / public runtime API changed: **no**.\n\n## Findings resolved"
text = replace_required(text, insert_after, b4_section, "R3 inventory B4 evidence")
text = replace_required(text, "## Findings still open", "## Findings resolved in R3-B4", "R3 inventory findings heading")
text = text.replace("| Engineering-language diagnostics gap | R3-B4 | #255 | ACTIVE | Enforce English technical diagnostics/comments/UI without touching rendered academic Portuguese. |", "| Engineering-language diagnostics gap | R3-B4 | #255 | RESOLVED | Permanent checker enforces English project-owned technical diagnostics/comments/UI while protecting rendered academic Portuguese. |")
text = text.replace("| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | ACTIVE | Migrate project-owned machine identifiers where consumer-safe and preserve genuine content/upstream boundaries. |", "| Engineering profile identifiers remain Portuguese | R3-B4 | #255 | RESOLVED | Project-owned profile/scenario machine IDs use canonical v3 English values; protected content/upstream boundaries remain unchanged. |")
text = text.replace("| Closed migration contract cleanup | R3-B4 | #255 | ACTIVE | Prove consumers before consolidating/removing closed R2 contracts. |", "| Closed migration contract cleanup | R3-B4 | #255 | RESOLVED | `v3-api-migration.json` retained for two live consumers; closed unconsumed test/path contracts removed. |")
text = replace_required(
    text,
    "| R3-B4/#255 | ACTIVE | entry `fbee5bd329f98a389c2880932af40547c8d1674e` |\n| R3-B5/#256 | PENDING | after B4; closes R3 and records immutable R4 entry |",
    f"| R3-B4/#255 | DONE | entry `{B4_ENTRY}`; PR #264 → `{B4_MAIN}`; PR `PASS=31 FAIL=0 SKIP=0`; release `PASS=33 FAIL=0 SKIP=0` |\n| R3-B5/#256 | ACTIVE | entry product `{B4_MAIN}`; closes R3 and records immutable R4 entry |",
    "R3 inventory lot table",
)
text = replace_required(text, "## R3-B4 entry contract", "## R3-B5 entry contract", "R3 inventory entry heading")
start = text.index("B4 starts from `fbee5bd329f98a389c2880932af40547c8d1674e`.")
end_marker = "No source/currency fact changed in B3, so `docs/NORMATIVE-BASE.md` and `docs/NORMATIVE-CURRENCY.md` remain intentionally unchanged. The v3 migration guide also remains unchanged because B3 changed no public runtime API."
end = text.index(end_marker, start) + len(end_marker)
replacement = f"B5 starts only after the B4→B5 control-plane checkpoint merges. Its product entry is `{B4_MAIN}`. It must reconcile all canonical control-plane surfaces against Git facts, confirm that no unclassified FAIL/UNASSESSED is represented as proof-contributing PASS, confirm proof/coverage/residual/language gates remain green, run `make static-check` and full `make check`, verify temporary executors and cleanup-only migration artifacts are absent, and record the exact immutable R4 certification entry. R4 Windows/literal-font certification is explicitly out of scope.\n\nNo source/currency fact or public runtime API changed in B4, so `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md` and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged."
text = text[:start] + replacement + text[end:]
write(path, text)

# release/v3-r3-inventory.json
path = "release/v3-r3-inventory.json"
data = json.loads(read(path))
data["stage"] = "R3-B5"
data["status"] = "ACTIVE"
data["reviewed_at"] = "2026-09-03"
ev = data.setdefault("evidence", {})
ev.update({
    "r3_b4_control_plane_entry_sha": B4_ENTRY,
    "r3_b4_product_main_sha": B4_MAIN,
    "r3_b4_bounded_run_id": B4_BOUNDED_RUN,
    "r3_b4_static_run_id": B4_STATIC_RUN,
    "r3_b4_linux_run_id": B4_LINUX_RUN,
    "r3_b4_linux_job_id": B4_LINUX_JOB,
    "r3_b4_linux_result": "PASS=31 FAIL=0 SKIP=0",
    "r3_b4_post_merge_release_run_id": B4_RELEASE_RUN,
    "r3_b4_post_merge_release_job_id": B4_RELEASE_JOB,
    "r3_b4_post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
})
for finding in data.get("findings", []):
    if finding.get("owner") == "R3-B4":
        finding["status"] = "RESOLVED"
        finding["resolved_by"] = "R3-B4"
        finding["closure_sha"] = B4_MAIN
        resolutions = {
            "engineering-language-diagnostics-gap": "Permanent engineering-language enforcement reports zero Portuguese project-owned technical diagnostics while protecting academic/normative/bibliographic Portuguese.",
            "engineering-profile-identifiers-portuguese": "Project-owned technical profile/scenario identifiers use canonical v3 English values without changing applicability semantics.",
            "closed-migration-contract-cleanup": "v3-api-migration remains for two live consumers; closed unconsumed test/path migration contracts were removed.",
        }
        finding["resolution"] = resolutions.get(finding.get("id"), "Resolved in R3-B4.")
lots = data.setdefault("lots", {})
lots["R3-B4"] = {
    "issue": 255,
    "status": "DONE",
    "name": "engineering-language enforcement and closed-contract consolidation",
    "entry_product_main_sha": B4_ENTRY,
    "implementation_head_sha": B4_HEAD,
    "pr": 264,
    "merge_main_sha": B4_MAIN,
    "bounded_validation_run_id": B4_BOUNDED_RUN,
    "static_contract_run_id": B4_STATIC_RUN,
    "linux_integration_run_id": B4_LINUX_RUN,
    "linux_integration_job_id": B4_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_merge_release_run_id": B4_RELEASE_RUN,
    "post_merge_release_job_id": B4_RELEASE_JOB,
    "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
    "residual_sources": {"latex": 134, "engineering": 171, "total": 305},
    "test_surface": {"retained": 148, "reachable": 148, "orphaned": 0},
    "engineering_language": {"portuguese_technical_diagnostics": 0, "retired_profile_ids": 0, "closed_unconsumed_contracts": 0, "live_api_contract_consumers": 2},
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
lots["R3-B5"] = {
    "issue": 256,
    "status": "ACTIVE",
    "name": "R3 closeout and R4 certification entry",
    "entry_product_main_sha": B4_MAIN,
}
data["retained_contracts"] = {
    "release/v3-api-migration.json": "live dependency of permanent residual/engineering-language enforcement",
    "release/v3-roadmap.json": "canonical machine state",
}
data["contracts_pending_consumer_audit"] = []
data["next_stage"] = "R3-B5"
data["next_issue"] = 256
data["current_entry_main_sha"] = B4_MAIN
data["r3_b4_closeout"] = lots["R3-B4"]
write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

# release/v3-roadmap.json -- preserve historical structure, mutate active R3 state generically.
path = "release/v3-roadmap.json"
data = json.loads(read(path))
data["updated_at"] = "2026-09-03"
data["status"] = "ACTIVE"
data["phase"] = "V3-R3"
data["stage"] = "R3-B5"
data["stage_name"] = "R3 closeout and R4 certification entry"

# Update common top-level active-lot shapes without depending on one historical schema spelling.
for key in ("active_implementation_lot", "active_lot", "current_lot"):
    if key in data and isinstance(data[key], dict):
        data[key].update({"id": "R3-B5", "issue": 256, "status": "ACTIVE", "entry_main_sha": B4_MAIN})
for key in ("next_stage", "next_lot"):
    if key in data:
        data[key] = "R3-B5"
if "next_issue" in data:
    data["next_issue"] = 256

# Recursively update explicit R3-B4/R3-B5 lot dictionaries wherever the schema keeps them.
def update_lots(node):
    if isinstance(node, dict):
        for key, value in node.items():
            if key == "R3-B4" and isinstance(value, dict):
                value.update({
                    "status": "DONE",
                    "issue": 255,
                    "pr": 264,
                    "entry_main_sha": B4_ENTRY,
                    "implementation_head_sha": B4_HEAD,
                    "merge_main_sha": B4_MAIN,
                    "static_contract_run_id": B4_STATIC_RUN,
                    "linux_integration_run_id": B4_LINUX_RUN,
                    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
                    "post_merge_release_run_id": B4_RELEASE_RUN,
                    "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
                })
            elif key == "R3-B5" and isinstance(value, dict):
                value.update({"status": "ACTIVE", "issue": 256, "entry_main_sha": B4_MAIN})
            update_lots(value)
    elif isinstance(node, list):
        for value in node:
            update_lots(value)

update_lots(data)
data["r3_b4_closeout"] = {
    "issue": 255,
    "pr": 264,
    "entry_main_sha": B4_ENTRY,
    "implementation_head_sha": B4_HEAD,
    "merge_main_sha": B4_MAIN,
    "bounded_validation_run_id": B4_BOUNDED_RUN,
    "static_contract_run_id": B4_STATIC_RUN,
    "linux_integration_run_id": B4_LINUX_RUN,
    "linux_integration_job_id": B4_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_merge_release_run_id": B4_RELEASE_RUN,
    "post_merge_release_job_id": B4_RELEASE_JOB,
    "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
    "residual_sources": 305,
    "reachable_test_scripts": 148,
    "orphaned_test_scripts": 0,
    "portuguese_technical_diagnostics": 0,
    "retired_profile_ids": 0,
    "closed_unconsumed_contracts": 0,
    "live_api_contract_consumers": 2,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")

print("R3-B4 closeout documentation reconciled; R3-B5 activated.")
