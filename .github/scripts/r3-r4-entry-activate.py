from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "d90a675a844724c33a5727d8d980027c46291eb0"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
B5_ENTRY = "e5d6ab1962ee04935ee68a6ae36f268350d59a3b"
CLOSEOUT_PR = 268
CLOSEOUT_HEAD = "2a8f80b53113e56f074c62382f7e31c561fe305b"
CLOSEOUT_STATIC = 33825615520
CLOSEOUT_LINUX = 33825615541
CLOSEOUT_LINUX_JOB = 100877511446
R4_ISSUE = 267
TODAY = "2026-09-03"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path!r}, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected exactly one regex match in {path!r}, found {count}: {pattern!r}")
    p.write_text(updated, encoding="utf-8")


def set_updated(path: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if re.search(r"^Updated: \d{4}-\d{2}-\d{2}$", text, flags=re.M):
        text = re.sub(r"^Updated: \d{4}-\d{2}-\d{2}$", f"Updated: {TODAY}", text, count=1, flags=re.M)
        p.write_text(text, encoding="utf-8")


roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-R3" or roadmap.get("stage") != "R3-B5":
    raise SystemExit("unexpected roadmap entry state")
if roadmap.get("r4_preparation", {}).get("entry_main_sha") is not None:
    raise SystemExit("R4 entry was already activated")

roadmap.update({
    "updated_at": TODAY,
    "status": "ACTIVE",
    "phase": "V3-R4",
    "stage": "V3-R4",
    "stage_name": "final certification of hardened v3 foundation",
})
roadmap["active_implementation_lot"] = {
    "phase": "V3-R4",
    "stage": "V3-R4",
    "issue": R4_ISSUE,
    "entry_product_main_sha": PRODUCT,
    "name": "final certification of hardened v3 foundation",
    "id": "V3-R4",
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "certification_started": False,
}

r3 = roadmap["r3"]
r3["status"] = "DONE"
r3["stage"] = "R3-B5"
r3["stage_name"] = "R3 hardening complete"
r3["active_issue"] = None
r3["next_issue"] = R4_ISSUE
b5 = r3["lots"]["R3-B5"]
b5.update({
    "status": "DONE",
    "closeout_pr": CLOSEOUT_PR,
    "closeout_head_sha": CLOSEOUT_HEAD,
    "closeout_merge_main_sha": BASE,
    "closeout_static_contract_run_id": CLOSEOUT_STATIC,
    "closeout_linux_integration_run_id": CLOSEOUT_LINUX,
    "closeout_linux_integration_job_id": CLOSEOUT_LINUX_JOB,
    "closeout_linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "technical_validation_status": "DONE",
    "exact_r4_entry_activation_pending": False,
    "r4_entry_main_sha": BASE,
})

closeout = {
    "status": "DONE",
    "issue": 256,
    "pr": CLOSEOUT_PR,
    "entry_main_sha": B5_ENTRY,
    "product_candidate_main_sha": PRODUCT,
    "closeout_head_sha": CLOSEOUT_HEAD,
    "merge_main_sha": BASE,
    "static_contract_run_id": CLOSEOUT_STATIC,
    "linux_integration_run_id": CLOSEOUT_LINUX,
    "linux_integration_job_id": CLOSEOUT_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_product_release_run_id": 33824039033,
    "post_product_release_result": "PASS=33 FAIL=0 SKIP=0",
    "all_r3_findings_resolved": True,
    "temporary_executor_residue": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
roadmap["r3_b5_closeout"] = closeout
roadmap["r4_preparation"].update({
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "certification_started": False,
    "blocked_until_exact_entry_activation": False,
})
roadmap["r4"] = {
    "status": "ACTIVE",
    "issue": R4_ISSUE,
    "name": "final certification of hardened v3 foundation",
    "entry_main_sha": BASE,
    "product_candidate_main_sha": PRODUCT,
    "certification_started": False,
    "historical_r1_certified_candidate_sha": "9b1752565ac217c04ffa22a9ef272cdf078af380",
    "constraints": [
        "do not redistribute proprietary Microsoft fonts",
        "do not reopen the closed public runtime API",
        "do not change normative semantics or proof-state defaults without current evidence",
        "temporary certification executors must be removed before the canonical checkpoint",
        "do not start V3-R5 V3-A1/A2 or CTAN submission before R4 closes",
    ],
}
roadmap["next_stage"] = "V3-R4"
roadmap["next_issue"] = R4_ISSUE
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
if inventory.get("status") != "ACTIVE" or inventory.get("stage") != "R3-B5":
    raise SystemExit("unexpected R3 inventory state")
inventory.update({
    "status": "DONE",
    "reviewed_at": TODAY,
    "current_entry_main_sha": BASE,
    "next_stage": "V3-R4",
    "next_issue": R4_ISSUE,
})
inv_b5 = inventory["lots"]["R3-B5"]
inv_b5.update({
    "status": "DONE",
    "closeout_pr": CLOSEOUT_PR,
    "closeout_head_sha": CLOSEOUT_HEAD,
    "closeout_merge_main_sha": BASE,
    "closeout_static_contract_run_id": CLOSEOUT_STATIC,
    "closeout_linux_integration_run_id": CLOSEOUT_LINUX,
    "closeout_linux_integration_job_id": CLOSEOUT_LINUX_JOB,
    "closeout_linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "exact_r4_entry_activation_pending": False,
    "r4_entry_main_sha": BASE,
})
inventory["r3_b5_closeout"] = closeout
inventory["r4_preparation"] = {
    "status": "ACTIVE",
    "issue": R4_ISSUE,
    "product_candidate_main_sha": PRODUCT,
    "entry_main_sha": BASE,
    "certification_started": False,
    "blocked_until_exact_entry_activation": False,
}
save_json("release/v3-r3-inventory.json", inventory)

for path in [
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "docs/R3-HARDENING-INVENTORY.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
]:
    set_updated(path)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A and R3-B1 through R3-B4 DONE; R3-B5/#256 TECHNICALLY VALIDATED; exact R4 entry activation pending. V3-R4/#267 is PREPARED but not started.**",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE — R3-A and R3-B1 through R3-B5 complete. V3-R4/#267 ACTIVE from exact predecessor `d90a675a844724c33a5727d8d980027c46291eb0`; certification has not started yet.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| R3-B5 | ACTIVE — VALIDATED | issue #256; candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | final tree: Static PASS; PR Linux `31/0/0`; post-merge release `33/0/0`; all R3 findings resolved | merge exact-entry checkpoint and close R3 |\n| V3-R4 | PREPARED / BLOCKED | issue #267; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | certification scope defined; certification not started | activate only after exact R3 closeout entry is recorded |",
    "| R3-B5 | DONE | issue #256; PR #268 → `d90a675a844724c33a5727d8d980027c46291eb0`; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | final R3 gates green; all findings resolved; immutable R4 predecessor recorded | None |\n| V3-R4 | ACTIVE | issue #267; entry predecessor `d90a675a844724c33a5727d8d980027c46291eb0`; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | certification scope active; certification not started | run Windows literal-font matrix, Unicode/embedding and PDF/A-2b certification |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## R3-B5 validation checkpoint\n\n.*?\n\n## Immediate action\n\n.*?$",
    """## R3-B5 closeout

R3-B5/#256 entered through `e5d6ab1962ee04935ee68a6ae36f268350d59a3b`, validated product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`, and closed canonically through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. PR #268 Static `33825615520` passed and Linux integration `33825615541` / job `100877511446` passed `PASS=31 FAIL=0 SKIP=0`. The underlying exact-main candidate had already passed Static `33824038991` and release `33824039033` / job `100872747975` at `PASS=33 FAIL=0 SKIP=0`.

All R3-A findings are resolved. Permanent evidence remains 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, and zero automation gaps. Residual scope remains 305 sources, retained test/check reachability remains 148/148 with zero orphans, and engineering-language/closed-contract invariants remain green. No normative authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered requirement, source/currency fact, or public runtime API changed.

The immutable predecessor required by R4 is therefore `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R3 and R3-B5 are DONE. V3-R4/#267 is ACTIVE, bound to product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; certification execution has not started.

## Immediate action

Execute V3-R4/#267 final certification on the exact current candidate. Reuse the proven R1-B8 certification architecture where valid, but bind all evidence to the current candidate. Certify Times New Roman/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding and PDF/A-2b. Do not start R5, V3-A1/A2, or CTAN submission until R4 closes.""",
    flags=re.S,
)

Path("docs/HANDOFF-V3.0.0.md").write_text(f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- R3-A and R3-B1 through R3-B5: **DONE**.
- R3-B5/#256 closeout: PR #268 → `{BASE}`.
- Final R3 product candidate: `{PRODUCT}`.
- PR #268 Static: `{CLOSEOUT_STATIC}` — PASS.
- PR #268 Linux: `{CLOSEOUT_LINUX}` / job `{CLOSEOUT_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`.
- Exact-product release: `33824039033` / job `100872747975` — `PASS=33 FAIL=0 SKIP=0`.
- All R3-A findings: **RESOLVED**.
- Residual baseline: 305 sources (134 LaTeX + 171 engineering); retained test/check reachability: 148/148; zero orphans.
- V3-R4/#267: **ACTIVE** from exact predecessor `{BASE}`; certification execution has not started.
- Historical R1 certification remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; R4 must bind new certification evidence to `{PRODUCT}`.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Execute V3-R4/#267 final certification on the exact current candidate. Certify literal Times New Roman and Arial across supported pdfLaTeX/LuaLaTeX routes, Unicode extraction, embedding, independent math-font policy and PDF/A-2b. Any temporary certification executor must be removed before the canonical checkpoint.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. Do not redistribute proprietary Microsoft fonts. R5 foundation freeze, V3-A1/A2 scientific-article work, and CTAN submission remain blocked until R4 closes.
""", encoding="utf-8")

replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "R3-B4/#255 is closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. R3-B5/#256 is active.",
    "R3-B4/#255 is closed through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. R3-B5/#256 is closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R3 is DONE and V3-R4/#267 is active.",
)
replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "| R3-B5/#256 | ACTIVE — VALIDATED | candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; PR Linux `31/0/0`; release `33/0/0`; exact-entry activation pending |",
    "| R3-B5/#256 | DONE | candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; PR #268 → `d90a675a844724c33a5727d8d980027c46291eb0`; PR Linux `31/0/0`; release `33/0/0`; R4 predecessor recorded |",
)
replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "R4 issue #267 is prepared but blocked. This checkpoint deliberately does not perform Windows/literal-font certification and does not invent the future merge SHA required as the exact R4 entry. The next action is a minimal exact-entry activation after this validated closeout merges.",
    "R4 issue #267 is active from exact predecessor `d90a675a844724c33a5727d8d980027c46291eb0`. This R3 closeout did not perform Windows/literal-font certification; that certification is now the bounded R4 responsibility on product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`.",
)

replace_once(
    "README.md",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE only for exact-entry closeout: R3-B5/#256 is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`; V3-R4/#267 is prepared but certification has not started.**",
    "**V3-R1, V3-R2 and V3-R3 are DONE. V3-R4/#267 is ACTIVE from exact predecessor `d90a675a844724c33a5727d8d980027c46291eb0`, bound to product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; certification execution has not started.**",
)
replace_once(
    "README.md",
    "Exact R4 entry activation remains pending; issue #267 is prepared and no certification has started.",
    "R3-B5 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; issue #267 is now the active R4 certification lot and certification execution has not started.",
)
replace_once(
    "README.md",
    "R3-B5/#256 has completed technical validation on `c79f3c73f1d51a30175e8259269504d029442a1c` and now owns only the exact-entry closeout. R4/#267 is prepared but remains blocked until that checkpoint is canonical.",
    "R3-B5/#256 and V3-R3 are complete through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. R4/#267 is active and owns current-candidate Windows/literal-font/Unicode/embedding/PDF-A certification.",
)
replace_once(
    "README.md",
    "R3-B5/#256 is active from `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and is the remaining R3 closeout lot.",
    "R3-B5/#256 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4/#267 is the active certification stage.",
)

replace_once(
    "AGENTS.md",
    "- V3-R3 is ACTIVE. R3-A/#250 is DONE from source baseline `345bbe1384c04b3f2002ac1f456ebbbdf7fc13b5`; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` define the evidence-driven lot sequence.",
    "- V3-R3 is DONE. R3-A/#250 and R3-B1 through R3-B5 are complete; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` preserve the closed evidence-driven sequence. V3-R4/#267 is ACTIVE from exact predecessor `d90a675a844724c33a5727d8d980027c46291eb0`.",
)
regex_once(
    "AGENTS.md",
    r"- R3-B4/#255 is DONE through PR #264.*?R4/#267 is PREPARED but certification must not start before that activation checkpoint is canonical\.",
    "- R3-B4/#255 is DONE through PR #264 at `59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390`. R3-B5/#256 is DONE: product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` passed PR #266 Linux `PASS=31 FAIL=0 SKIP=0` and exact-main release `PASS=33 FAIL=0 SKIP=0`; validated closeout PR #268 passed Static `33825615520` and Linux `33825615541` / job `100877511446` = `PASS=31 FAIL=0 SKIP=0`, then merged at exact R4 predecessor `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R4/#267 is ACTIVE; certification execution has not started.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "R3-B5/#256 has completed technical validation on `c79f3c73f1d51a30175e8259269504d029442a1c` and remains active only for the exact-entry checkpoint; R4/#267 is prepared but certification has not started.",
    "R3-B5/#256 and V3-R3 are DONE through validated closeout PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`. V3-R4/#267 is ACTIVE on product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; certification execution has not started.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "R3-B5 has completed final cross-surface validation; only the exact immutable R4 entry activation remains. R4/#267 must certify the current candidate after that checkpoint rather than relying on the historical R1 certification alone.",
    "R3-B5 completed final cross-surface validation and recorded immutable R4 predecessor `d90a675a844724c33a5727d8d980027c46291eb0`. R4/#267 must now certify the current candidate rather than relying on the historical R1 certification alone.",
)

regex_once(
    "docs/ENGINEERING-LANGUAGE.md",
    r"R3-B5/#256 is ACTIVE from canonical control-plane checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and owns R3 closeout/R4 entry; it must not broaden this policy or change the public runtime API\.",
    "R3-B5/#256 is DONE through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4/#267 is ACTIVE and must preserve this policy and the closed public runtime API during certification.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "R3-B5/#256 is active from canonical control-plane checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and remains required before R4.",
    "R3-B5/#256 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; V3-R4/#267 is now active and certification execution has not started.",
)

print("Exact R4 entry activation reconciliation completed")
