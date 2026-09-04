from __future__ import annotations

import json
from pathlib import Path

BASE = "e40a56deeca8c22797398b0c95835964aefd2b15"
R4_CLOSEOUT = "0b0f5d989163dc6b1429feeb2d8a7c66988647bb"
R5_CLOSEOUT = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
R4_RUN = 33855800767
A1_ISSUE = 275
TODAY = "2026-09-04"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path}: {old!r}; found {count}")
    p.write_text(text.replace(old, new), encoding="utf-8")


roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
    raise SystemExit("unexpected canonical roadmap stage")
if roadmap.get("active_implementation_lot", {}).get("issue") != A1_ISSUE:
    raise SystemExit("unexpected active implementation lot")
if roadmap.get("r5", {}).get("status") != "DONE":
    raise SystemExit("R5 must already be DONE")
if roadmap.get("a1", {}).get("status") != "ACTIVE":
    raise SystemExit("A1 must already be ACTIVE")

roadmap["next_action"] = (
    f"Execute V3-A1/#{A1_ISSUE} from exact entry {R5_CLOSEOUT}: reconfirm current UFC scientific-article guidance and applicable ABNT authorities, "
    "currency, precedence, locators, applicability and requirement/recommendation distinctions; derive a conservative article normative contract and a bounded V3-A2 implementation contract before any article runtime work. "
    f"Keep certified foundation {PRODUCT} unchanged unless current evidence proves a separately bounded cross-cutting conflict; keep CTAN submission blocked."
)

r4prep = roadmap["r4_preparation"]
r4prep.update({
    "status": "DONE",
    "certification_started": True,
    "certification_status": "DONE",
    "blocked_until_exact_entry_activation": False,
})

r4 = roadmap["r4"]
r4.update({
    "status": "DONE",
    "certification_started": True,
    "certification_status": "DONE",
    "exact_r5_entry_activation_pending": False,
    "closeout_pr": 273,
    "closeout_merge_main_sha": R4_CLOSEOUT,
})

roadmap["active_implementation_lot"]["work_started"] = False
roadmap["a1_preparation"]["status"] = "ACTIVE"
roadmap["a1_preparation"]["entry_main_sha"] = R5_CLOSEOUT
roadmap["a1_preparation"]["blocked_until_exact_r5_closeout"] = False
roadmap["a1_preparation"]["work_started"] = False
roadmap["a1"]["work_started"] = False
roadmap["next_stage"] = "V3-A1"
roadmap["next_issue"] = A1_ISSUE
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
if inventory.get("status") != "DONE" or inventory.get("phase") != "V3-R3":
    raise SystemExit("unexpected historical R3 inventory state")

inventory["r3_b5_activation"]["status"] = "DONE"
inventory["r4_preparation"].update({
    "status": "DONE",
    "certification_started": True,
    "certification_status": "DONE",
    "blocked_until_exact_entry_activation": False,
})
inventory["r4_transition"].update({
    "status": "DONE",
    "exact_r5_entry_activation_pending": False,
    "closeout_pr": 273,
    "closeout_merge_main_sha": R4_CLOSEOUT,
})
inventory["r5_preparation"].update({
    "status": "DONE",
    "technical_validation_status": "DONE",
    "exact_a1_entry_activation_pending": False,
    "closeout_pr": 276,
    "closeout_merge_main_sha": R5_CLOSEOUT,
    "a1_entry_main_sha": R5_CLOSEOUT,
})
inventory["a1_preparation"].update({
    "status": "ACTIVE",
    "entry_main_sha": R5_CLOSEOUT,
    "blocked_until_exact_r5_closeout": False,
    "work_started": False,
})
inventory["post_foundation_state"].update({
    "r5_status": "DONE",
    "r5_closeout_main_sha": R5_CLOSEOUT,
    "a1_status": "ACTIVE",
    "a1_entry_main_sha": R5_CLOSEOUT,
})
save_json("release/v3-r3-inventory.json", inventory)

replace_once(
    "README.md",
    f"R4 closeout PR #273 merged at `{R4_CLOSEOUT}`; V3-R4/#267 is DONE and V3-R5/#272 is ACTIVE from that exact predecessor.",
    f"R4 closeout PR #273 merged at `{R4_CLOSEOUT}`; V3-R4/#267 is DONE. V3-R5/#272 subsequently closed through PR #276 at `{R5_CLOSEOUT}`, and V3-A1/#275 is ACTIVE from that exact entry.",
)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "Active foundation-freeze issue: #272 (V3-R5). Machine authority: `release/v3-roadmap.json`.",
    "Active implementation issue: #275 (V3-A1). Machine authority: `release/v3-roadmap.json`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"The immutable predecessor required by R4 is therefore `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R3 and R3-B5 are DONE. V3-R4/#267 is ACTIVE, bound to product candidate `{PRODUCT}`; certification execution has not started.",
    f"The immutable predecessor required by R4 is therefore `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R3 and R3-B5 are DONE. R4 subsequently certified product candidate `{PRODUCT}` in run `{R4_RUN}` and closed through PR #273 at `{R4_CLOSEOUT}`; R5 later closed through PR #276 at `{R5_CLOSEOUT}`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"R4 closed canonically through PR #273 at `{R4_CLOSEOUT}`. This immutable closeout SHA is the exact V3-R5 entry. V3-R4/#267 is DONE; V3-R5/#272 is ACTIVE. The certified product remains `{PRODUCT}` and must not be modified merely for release-documentation cleanup.",
    f"R4 closed canonically through PR #273 at `{R4_CLOSEOUT}`. This immutable closeout SHA became the exact V3-R5 entry. V3-R5 subsequently completed its foundation freeze and closed through PR #276 at `{R5_CLOSEOUT}`. The certified product remains `{PRODUCT}`, and V3-A1/#275 is the current active stage.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "`articles.def` is introduced only when V3-A1 becomes active. It is not pre-staged as a dormant foundation module.",
    "Article runtime implementation remains absent during V3-A1. If the reconfirmed A1 source contract requires a dedicated `articles.def` module, introducing and wiring that runtime belongs to V3-A2 rather than A1.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "The Linux observations are engineering evidence; final Windows/literal-font/PDF-A certification remains B8-owned.",
    f"The Linux observations are engineering evidence; the current hardened foundation was independently re-certified by V3-R4 run `{R4_RUN}` across the strict Windows font/engine matrix plus Linux Unicode, embedding and PDF/A inspection.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "Only canonical R5 closeout remains before V3-A1/#275 may begin.",
    f"R5 has since closed canonically through PR #276 at `{R5_CLOSEOUT}`. V3-A1/#275 is ACTIVE from that exact entry; article runtime/profile implementation remains deferred to V3-A2.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "V3-A1/#275 is source/normative work and remains blocked until the R5 closeout merge supplies its immutable entry SHA.",
    f"V3-A1/#275 is source/normative work and is ACTIVE from immutable R5 closeout `{R5_CLOSEOUT}`. A1 must not introduce article runtime/profile behavior; that implementation is deferred to V3-A2 after the source contract closes.",
)

replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "R3-B5/#256 is closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R3 is DONE and V3-R4/#267 is active.",
    f"R3-B5/#256 is closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R3 is DONE. V3-R4/#267 subsequently closed through PR #273 at `{R4_CLOSEOUT}`, V3-R5/#272 closed through PR #276 at `{R5_CLOSEOUT}`, and V3-A1/#275 is ACTIVE.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "3. Confirm that the intended release commit is still covered by, or has proportionally re-established, the completed Windows/literal-font/PDF-A certification baseline from R1-BLOCK-8.",
    f"3. Confirm that the intended release commit is still covered by the current V3-R4 certification of `{PRODUCT}` (run `{R4_RUN}`), or has proportionally re-established equivalent Windows/literal-font/Unicode/embedding/PDF-A evidence after any product-affecting change.",
)

# Canonical surfaces that were already correct must remain semantically current.
checks = {
    "AGENTS.md": "V3-A1/#275 is ACTIVE",
    "docs/HANDOFF-V3.0.0.md": "V3-A1/#275: **ACTIVE**",
    "docs/ENGINEERING-LANGUAGE.md": "V3-A1/#275 is ACTIVE",
}
for path, marker in checks.items():
    text = Path(path).read_text(encoding="utf-8")
    if marker not in text:
        raise SystemExit(f"expected current A1 marker missing from {path}")

print("A1 control-plane/documentation reconciliation completed")
