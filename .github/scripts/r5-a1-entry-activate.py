from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
R5_ENTRY = "0b0f5d989163dc6b1429feeb2d8a7c66988647bb"
R5_ISSUE = 272
R5_PR = 276
A1_ISSUE = 275
TODAY = "2026-09-04"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path}, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected exactly one regex match in {path}, found {count}: {pattern!r}")
    p.write_text(updated, encoding="utf-8")


roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-R5" or roadmap.get("stage") != "V3-R5":
    raise SystemExit("unexpected roadmap phase/stage")
if roadmap.get("r5", {}).get("status") != "VALIDATED_PENDING_CANONICAL_CLOSEOUT":
    raise SystemExit("R5 is not at validated closeout state")
if roadmap.get("a1_preparation", {}).get("entry_main_sha") is not None:
    raise SystemExit("A1 entry already exists")

roadmap.update({
    "updated_at": TODAY,
    "status": "ACTIVE",
    "phase": "V3-A1",
    "stage": "V3-A1",
    "stage_name": "reconfirm scientific-article authority and normative contract",
    "next_stage": "V3-A1",
    "next_issue": A1_ISSUE,
})
roadmap["active_implementation_lot"] = {
    "phase": "V3-A1",
    "stage": "V3-A1",
    "issue": A1_ISSUE,
    "id": "V3-A1",
    "name": "reconfirm scientific-article authority and normative contract",
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "entry_product_main_sha": PRODUCT,
    "runtime_implementation_allowed": False,
    "work_started": False,
}
for key in ("r5_preparation", "r5"):
    state = roadmap[key]
    state.update({
        "status": "DONE",
        "technical_validation_status": "DONE",
        "exact_a1_entry_activation_pending": False,
        "closeout_pr": R5_PR,
        "closeout_merge_main_sha": BASE,
        "a1_entry_main_sha": BASE,
    })
roadmap["r5_closeout"] = {
    "status": "DONE",
    "issue": R5_ISSUE,
    "pr": R5_PR,
    "entry_main_sha": R5_ENTRY,
    "merge_main_sha": BASE,
    "certified_product_candidate_main_sha": PRODUCT,
    "full_release_run_id": 33866258865,
    "full_release_result": "PASS=33 FAIL=0 SKIP=0",
    "package_validation_run_id": 33869888601,
    "package_validation_job_id": 101013093747,
    "package_validation_result": "PASS",
    "pr_static_contract_run_id": 33872118250,
    "pr_linux_integration_run_id": 33872118241,
    "pr_linux_integration_job_id": 101020688121,
    "pr_linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "product_tree_unchanged_since_certification": True,
    "public_bundles_passed": True,
    "distribution_bundles_passed": True,
    "checksums_passed": True,
    "institutional_assets_excluded": True,
    "proprietary_assets_excluded": True,
    "temporary_executor_residue": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
roadmap["a1_preparation"].update({
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "blocked_until_exact_r5_closeout": False,
    "work_started": False,
    "runtime_implementation_allowed": False,
    "ctan_submission_allowed": False,
})
roadmap["a1"] = {
    "status": "ACTIVE",
    "issue": A1_ISSUE,
    "name": "reconfirm scientific-article authority and normative contract",
    "entry_main_sha": BASE,
    "certified_foundation_product_sha": PRODUCT,
    "runtime_implementation_allowed": False,
    "work_started": False,
    "ctan_submission_allowed": False,
}
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
inventory["reviewed_at"] = TODAY
inventory["post_foundation_state"] = {
    "r5_status": "DONE",
    "r5_issue": R5_ISSUE,
    "r5_closeout_pr": R5_PR,
    "r5_closeout_main_sha": BASE,
    "certified_foundation_product_sha": PRODUCT,
    "a1_status": "ACTIVE",
    "a1_issue": A1_ISSUE,
    "a1_entry_main_sha": BASE,
    "r3_inventory_remains_historical": True,
}
save_json("release/v3-r3-inventory.json", inventory)

Path("docs/HANDOFF-V3.0.0.md").write_text(f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **DONE**.
- V3-R5/#272: **DONE** through PR #276 at `{BASE}`.
- Certified foundation product: `{PRODUCT}`; unchanged throughout R5.
- R5 release gate: run `33866258865` / job `101001704635` — `PASS=33 FAIL=0 SKIP=0`.
- R5 package/freeze validation: run `33869888601` / job `101013093747` — SUCCESS.
- R5 PR gates: Static `33872118250` — PASS; Linux `33872118241` / job `101020688121` — `PASS=31 FAIL=0 SKIP=0`.
- Public/distribution bundles, reproducibility, SHA-256 checksums, external-upstream semantics and institutional/proprietary asset exclusions: **PASS**.
- Validation residue: **0**.
- `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md`: unchanged through R5.
- V3-A1/#275: **ACTIVE** from exact entry `{BASE}`.
- A1 is source/normative-contract work only; article runtime implementation is forbidden in A1.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Execute V3-A1/#275 from exact entry `{BASE}`. Reconfirm current UFC scientific-article guidance and applicable ABNT authorities, currency, precedence, locators, applicability and requirement/recommendation distinctions. Build a conservative article normative contract before any article runtime implementation. Historical pre-v3 article research is discovery evidence only, never authority to restore blindly.

## Hard boundaries

Preserve certified foundation `{PRODUCT}` and the closed v3 API. Do not implement article runtime/profile behavior in A1. Do not restore historical rule values, locators, source status, proof state or retired machine identifiers without current evidence. Do not redistribute proprietary Microsoft fonts or perform CTAN submission. V3-A2 remains blocked until A1 closes with a bounded implementation contract.
""", encoding="utf-8")

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 DONE. V3-R5/#272 TECHNICALLY VALIDATED from exact entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` against frozen product `c79f3c73f1d51a30175e8259269504d029442a1c`; canonical closeout is pending. V3-A1/#275 is PREPARED / BLOCKED until the real R5 closeout SHA exists.**",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4 DONE. V3-R5/#272 DONE through PR #276 at `{BASE}` with certified foundation `{PRODUCT}` unchanged. V3-A1/#275 is ACTIVE from exact entry `{BASE}`; article runtime implementation is not allowed in A1.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| V3-R5 | VALIDATED — CLOSEOUT PENDING | issue #272; entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; frozen product `c79f3c73f1d51a30175e8259269504d029442a1c` | release gate `33866258865` = `33/0/0`; package run `33869888601` PASS; bundles/checksums/assets/residue PASS | merge validated closeout and record immutable A1 entry |\n| V3-A1 | PREPARED / BLOCKED | issue #275; entry SHA pending R5 closeout | source/normative article contract only; no runtime work started | activate only from real canonical R5 closeout SHA |",
    f"| V3-R5 | DONE | issue #272; entry `{R5_ENTRY}`; PR #276 → `{BASE}`; frozen product `{PRODUCT}` | release `33/0/0`; package/bundle/checksum/asset audit PASS; PR Linux `31/0/0`; zero residue | None |\n| V3-A1 | ACTIVE | issue #275; exact entry `{BASE}`; certified foundation `{PRODUCT}` | source/normative article contract only; runtime work not started | reconfirm article authorities/currency/precedence and derive conservative rule contract |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## V3-R5 foundation-freeze validation\n\n.*?\n\n## Immediate action\n\n.*?$",
    f"""## V3-R5 foundation-freeze closeout

V3-R5/#272 entered from `{R5_ENTRY}` and preserved R4-certified product `{PRODUCT}` unchanged. The full release gate completed `PASS=33 FAIL=0 SKIP=0` in run `33866258865` / job `101001704635`; final package/freeze run `33869888601` / job `101013093747` passed source-only validation, reproducible public and complete distribution bundles, SHA-256 checksums, expected class/CTAN layouts, external `abntexto` semantics, institutional/proprietary asset exclusions and zero tracked/untracked residue. PR #276 then passed Static `33872118250` and Linux `33872118241` / job `101020688121` at `PASS=31 FAIL=0 SKIP=0` and squash-merged at `{BASE}`.

No product-affecting path, public runtime API, normative semantics, source/currency fact, locator/tolerance/applicability policy, proof-state default or rendered requirement changed in R5. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain unchanged. V3-R5 is DONE and `{BASE}` is the exact immutable V3-A1 entry.

## V3-A1 entry

V3-A1/#275 is ACTIVE from `{BASE}`. A1 must reconfirm the current authoritative source set for the UFC scientific-article profile and applicable ABNT standards, derive current predicates/locators/applicability and requirement-versus-recommendation distinctions, integrate them with current currency/precedence/traceability/proof-state machinery, and define a bounded V3-A2 implementation contract. Historical pre-v3 article research is discovery evidence only. No article runtime/profile implementation is allowed in A1.

## Immediate action

Execute V3-A1/#275 source reconciliation. Keep the certified non-article foundation `{PRODUCT}` unchanged unless current source evidence demonstrates a separately bounded cross-cutting conflict. V3-A2 and actual CTAN submission remain blocked.""",
    flags=re.S,
)

replace_once(
    "AGENTS.md",
    "- V3-R3 and V3-R4 are DONE. R4 run `33855800767` certified `c79f3c73f1d51a30175e8259269504d029442a1c`, and PR #273 established exact R5 entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`. V3-R5/#272 is TECHNICALLY VALIDATED: release gate run `33866258865` passed `PASS=33 FAIL=0 SKIP=0`, package run `33869888601` passed reproducible public/distribution bundles, checksums, asset exclusions and zero residue, and the certified product is unchanged. R5 must remain open until a canonical closeout merge yields the immutable V3-A1/#275 entry; A1 is PREPARED/BLOCKED and must not start early.",
    f"- V3-R3, V3-R4 and V3-R5 are DONE. R5/#272 preserved certified product `{PRODUCT}`, passed release gate `33866258865` = `PASS=33 FAIL=0 SKIP=0`, package audit `33869888601`, and PR #276 gates, then closed at `{BASE}`. V3-A1/#275 is ACTIVE from that exact SHA. A1 is source/normative-contract work only: no article runtime/profile implementation is allowed before A1 closes.",
)
replace_once(
    "AGENTS.md",
    "V3-R5/#272 has completed technical freeze/package validation and is pending only canonical closeout; V3-A1/#275 is prepared but blocked until that future closeout SHA exists.",
    f"V3-R5/#272 is DONE through PR #276 at `{BASE}`; V3-A1/#275 is ACTIVE from that exact entry and must reconfirm article authority before runtime implementation.",
)

replace_once(
    "README.md",
    "**V3-R1, V3-R2, V3-R3 and V3-R4 are DONE. V3-R5/#272 is TECHNICALLY VALIDATED from exact entry `0b0f5d989163dc6b1429feeb2d8a7c66988647bb` with certified foundation product `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged; canonical closeout is pending so the future V3-A1 entry SHA is not yet invented.**",
    f"**V3-R1 through V3-R5 are DONE. R5/#272 closed through PR #276 at `{BASE}` with certified foundation `{PRODUCT}` unchanged. V3-A1/#275 is ACTIVE from `{BASE}` and is limited to reconfirming the scientific-article normative/source contract before any runtime implementation.**",
)
replace_once(
    "README.md",
    "R5 remains open only until its canonical closeout produces the immutable V3-A1/#275 entry; A1 is prepared but blocked and no article runtime work has started.",
    f"R5 is closed at `{BASE}`. V3-A1/#275 is active from that exact entry; no article runtime work has started because A1 owns source/normative-contract reconstruction only.",
)
replace_once(
    "README.md",
    "R3-B5/#256 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4/#267 is the active certification stage.",
    f"R3-B5/#256 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4 and V3-R5 are DONE; V3-A1/#275 is ACTIVE from `{BASE}`.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "V3-R5/#272 is ACTIVE from that exact entry.",
    f"V3-R5/#272 is DONE through PR #276 at `{BASE}`. V3-A1/#275 is ACTIVE from that exact entry and is restricted to source/normative-contract reconstruction; article runtime implementation belongs to V3-A2 after A1 closes.",
)
replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "V3-R5/#272 has completed technical foundation-freeze validation in run `33869888601` without broadening this policy, changing the certified runtime, or introducing new engineering-language debt; V3-A1/#275 is prepared but blocked until canonical R5 closeout.",
    f"V3-R5/#272 completed without broadening this policy, changing the certified runtime, or introducing new engineering-language debt and closed through PR #276 at `{BASE}`. V3-A1/#275 is ACTIVE from that exact entry; its new scientific-article engineering identifiers must remain canonical English while official/academic Portuguese stays protected.",
)
replace_once(
    "docs/CTAN-RELEASE.md",
    "Canonical R5 closeout is still required before V3-A1/#275 may start. Actual CTAN upload remains a separate explicit release action and has not occurred.",
    f"R5 closed through PR #276 at `{BASE}` and V3-A1/#275 is now ACTIVE from that exact entry. Actual CTAN upload remains a separate explicit release action and has not occurred; A1/A2 scientific-article work is not CTAN submission.",
)
replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "V3-A1/#275 is prepared but remains blocked pending the future canonical R5 closeout SHA.",
    f"V3-R5/#272 subsequently closed through PR #276 at `{BASE}` with the certified foundation unchanged. V3-A1/#275 is ACTIVE from that exact entry; R3 remains historical and closed.",
)
