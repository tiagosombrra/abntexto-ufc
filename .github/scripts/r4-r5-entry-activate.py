from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "0b0f5d989163dc6b1429feeb2d8a7c66988647bb"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
R4_ENTRY = "d90a675a844724c33a5727d8d980027c46291eb0"
R4_RUN = 33855800767
R4_PR = 273
TODAY = "2026-09-04"


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one match in {path}: {old!r}; found {count}")
    p.write_text(text.replace(old, new, 1), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected one regex match in {path}: {pattern!r}; found {count}")
    p.write_text(updated, encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# Machine authority.
roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-R4" or roadmap.get("stage") != "V3-R4":
    raise SystemExit("unexpected roadmap phase/stage before R5 activation")
if roadmap.get("r5_preparation", {}).get("status") != "PREPARED":
    raise SystemExit("R5 is not in prepared state")
if roadmap.get("r5_preparation", {}).get("entry_main_sha") is not None:
    raise SystemExit("R5 entry already recorded")
cert = roadmap.get("r4_certification", {})
if cert.get("status") != "DONE" or cert.get("certification_run_id") != R4_RUN:
    raise SystemExit("R4 certification record is not complete")
if cert.get("product_candidate_main_sha") != PRODUCT:
    raise SystemExit("R4 certified product mismatch")

r4_closeout = {
    "status": "DONE",
    "issue": 267,
    "closeout_pr": R4_PR,
    "closeout_merge_main_sha": BASE,
    "r4_entry_predecessor_sha": R4_ENTRY,
    "certified_product_candidate_main_sha": PRODUCT,
    "certification_run_id": R4_RUN,
    "preflight_job_id": 100968686875,
    "windows_matrix_job_id": 100968747942,
    "linux_final_job_id": 100970109387,
    "cleanup_job_id": 100970307670,
    "matrix_cells_passed": 4,
    "unicode_extraction_passed": True,
    "font_embedding_passed": True,
    "pdfa_2b_passed": True,
    "temporary_executor_residue": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
    "proprietary_fonts_redistributed": False,
}
roadmap.update({
    "updated_at": TODAY,
    "status": "ACTIVE",
    "phase": "V3-R5",
    "stage": "V3-R5",
    "stage_name": "freeze certified foundation and finalize release-ready documentation",
})
roadmap["r4_closeout"] = r4_closeout
roadmap["r5_preparation"].update({
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "blocked_until_exact_r4_closeout": False,
})
roadmap["r5"] = {
    "status": "ACTIVE",
    "issue": 272,
    "name": "freeze certified foundation and finalize release-ready documentation",
    "entry_main_sha": BASE,
    "certified_product_candidate_main_sha": PRODUCT,
    "foundation_freeze_started": False,
    "scientific_article_work_started": False,
    "ctan_submission_started": False,
}
roadmap["active_implementation_lot"] = {
    "phase": "V3-R5",
    "stage": "V3-R5",
    "issue": 272,
    "entry_product_main_sha": PRODUCT,
    "entry_main_sha": BASE,
    "name": "freeze certified foundation and finalize release-ready documentation",
    "id": "V3-R5",
    "status": "ACTIVE",
    "foundation_freeze_started": False,
}
roadmap["next_stage"] = "V3-R5"
roadmap["next_issue"] = 272
roadmap["next_action"] = (
    "Execute V3-R5/#272 from exact entry " + BASE + 
    " without modifying certified product " + PRODUCT + 
    ": freeze the foundation, reconcile release/user/maintainer documentation, verify normative/current migration truthfulness, public/distribution bundles, checksums, asset exclusions and release metadata, run proportional release gates, and prove zero temporary/stale cleanup residue. Keep V3-A1/A2 and CTAN submission blocked until R5 closes."
)
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
if inventory.get("status") != "DONE":
    raise SystemExit("R3 inventory must remain DONE")
inventory["reviewed_at"] = TODAY
inventory["r4_closeout"] = r4_closeout
inventory["r5_preparation"] = {
    "status": "ACTIVE",
    "issue": 272,
    "certified_product_candidate_main_sha": PRODUCT,
    "entry_main_sha": BASE,
    "foundation_freeze_started": False,
}
inventory["next_stage"] = "V3-R5"
inventory["next_issue"] = 272
save_json("release/v3-r3-inventory.json", inventory)

# Canonical handoff is rewritten because its purpose is the exact continuation point.
Path("docs/HANDOFF-V3.0.0.md").write_text(f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **DONE**.
- R4 certified product candidate: `{PRODUCT}`.
- R4 certification workflow: `{R4_RUN}` — SUCCESS.
- Windows strict Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix: **4/4 PASS**.
- Unicode extraction: **PASS**; font embedding: **PASS**; PDF/A-2b: **PASS**.
- R4 closeout PR #273 merged at `{BASE}`; this is the exact immutable V3-R5 entry predecessor.
- V3-R5/#272: **ACTIVE** from `{BASE}`; foundation-freeze execution has not started yet.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Execute V3-R5/#272 from exact entry `{BASE}` without modifying certified product `{PRODUCT}`. Freeze the certified foundation, reconcile release/user/maintainer documentation, verify normative-source/currency and migration truthfulness, validate public/distribution bundles and checksums, confirm exclusion of institutional/proprietary assets, run proportional release gates, and prove zero temporary/stale cleanup residue.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. Do not redistribute proprietary Microsoft fonts or claim UFC homologation/CTAN acceptance. V3-A1/A2 scientific-article work and actual CTAN submission remain blocked until R5 closes canonically.
""", encoding="utf-8")

# Roadmap summary and continuation point.
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 ACTIVE — final certification PASSED on `c79f3c73f1d51a30175e8259269504d029442a1c`; exact R5 entry activation is pending. V3-R5/#272 is PREPARED / BLOCKED.**",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 DONE. V3-R5/#272 ACTIVE from exact predecessor `{BASE}`; certified foundation product `{PRODUCT}` is frozen as the R5 product baseline.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "Active implementation issue: #256. Machine authority: `release/v3-roadmap.json`.",
    "Active foundation-freeze issue: #272 (V3-R5). Machine authority: `release/v3-roadmap.json`.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| V3-R4 | ACTIVE — CERTIFIED | issue #267; entry predecessor `d90a675a844724c33a5727d8d980027c46291eb0`; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; run `33855800767` | exact candidate passed Windows Times/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding, independent math policy and PDF/A-2b; temporary executor removed | merge certification closeout, record its immutable SHA, then close R4 |\n| V3-R5 | PREPARED / BLOCKED | issue #272; certified product `c79f3c73f1d51a30175e8259269504d029442a1c` | foundation-freeze contract defined | activate only after exact R4 closeout entry is recorded |",
    f"| V3-R4 | DONE | issue #267; run `33855800767`; closeout PR #273 → `{BASE}` | 4/4 strict font/engine cells PASS; Unicode, embedding and PDF/A-2b PASS; temporary executor removed | None |\n| V3-R5 | ACTIVE | issue #272; entry `{BASE}`; certified product `{PRODUCT}` | foundation-freeze/final-documentation contract active | freeze product baseline; reconcile release docs; validate bundles/checksums/assets/metadata and proportional release gates |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"R4 is therefore technically certified but remains canonically ACTIVE until.*?\n\n## Immediate action\n\n.*?$",
    f"R4 closed canonically through PR #273 at `{BASE}`. This immutable closeout SHA is the exact V3-R5 entry. V3-R4/#267 is DONE; V3-R5/#272 is ACTIVE. The certified product remains `{PRODUCT}` and must not be modified merely for release-documentation cleanup.\n\n## Immediate action\n\nExecute V3-R5/#272 from `{BASE}`: freeze the certified foundation, reconcile current release/user/maintainer documentation, verify normative-source/currency and migration documentation remain truthful, validate public/distribution bundles, checksums, asset exclusions and release metadata, run proportional release validation, and prove zero temporary/stale cleanup residue. Keep V3-A1/A2 and CTAN submission blocked until R5 closes canonically.",
    flags=re.S,
)

# Bootstrap and user-facing status.
replace_once(
    "AGENTS.md",
    "V3-R4/#267 is technically certified on `c79f3c73f1d51a30175e8259269504d029442a1c` by run `33855800767` and remains ACTIVE only for exact R5 entry closeout; V3-R5/#272 is PREPARED/BLOCKED.",
    f"V3-R4/#267 is DONE: run `33855800767` certified `{PRODUCT}`, and closeout PR #273 merged at exact R5 predecessor `{BASE}`. V3-R5/#272 is ACTIVE from that predecessor; foundation-freeze execution has not started yet.",
)
replace_once(
    "AGENTS.md",
    "R4 remains ACTIVE only until its closeout merge SHA is recorded as the exact V3-R5/#272 entry.",
    f"R4 closed through PR #273 at `{BASE}`; V3-R5/#272 is ACTIVE from that exact immutable entry.",
)
replace_once(
    "README.md",
    "**V3-R1, V3-R2 and V3-R3 are DONE. V3-R4/#267 is technically CERTIFIED on `c79f3c73f1d51a30175e8259269504d029442a1c` by run `33855800767`; exact R5 entry activation remains pending. V3-R5/#272 is prepared but blocked.**",
    f"**V3-R1, V3-R2, V3-R3 and V3-R4 are DONE. V3-R5/#272 is ACTIVE from exact predecessor `{BASE}`; the certified foundation product remains `{PRODUCT}`.**",
)
replace_once(
    "README.md",
    "Exact R5 entry activation remains pending; #272 is prepared/blocked.",
    f"R4 closeout PR #273 merged at `{BASE}`; V3-R4/#267 is DONE and V3-R5/#272 is ACTIVE from that exact predecessor.",
)

# Historical inventory now records the R4 closeout without reopening R3.
replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    "All four strict Times/Arial × pdfLaTeX/LuaLaTeX cases passed literal text-family identity, Unicode extraction, embedding and PDF/A-2b; exact R5 entry closeout remains outside the closed R3 inventory.",
    f"All four strict Times/Arial × pdfLaTeX/LuaLaTeX cases passed literal text-family identity, Unicode extraction, embedding and PDF/A-2b. R4 then closed through PR #273 at `{BASE}`, which is the exact V3-R5/#272 entry; R3 remains closed and unchanged.",
)

# Architecture, language policy, and CTAN guide advance only their control-plane status.
replace_once(
    "docs/ARCHITECTURE.md",
    "V3-R4/#267 certification run `33855800767` passed on exact product `c79f3c73f1d51a30175e8259269504d029442a1c` across the strict four-cell font/engine matrix plus Unicode, embedding and PDF/A-2b; canonical closeout/R5-entry activation remains pending.",
    f"V3-R4/#267 certification run `33855800767` passed on exact product `{PRODUCT}` across the strict four-cell font/engine matrix plus Unicode, embedding and PDF/A-2b; closeout PR #273 merged at `{BASE}`, and V3-R5/#272 is ACTIVE from that exact entry.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "The product architecture remains unchanged; only the control-plane closeout that establishes the exact R5 entry is pending.",
    f"The product architecture remains unchanged. R4 closeout `{BASE}` establishes the exact R5 entry; V3-R5 now owns foundation freeze and final release-documentation validation without modifying the certified product.",
)
replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "V3-R4/#267 certification run `33855800767` passed on `c79f3c73f1d51a30175e8259269504d029442a1c` without changing this policy or the closed public runtime API; only exact R5 entry closeout remains.",
    f"V3-R4/#267 certification run `33855800767` passed on `{PRODUCT}` without changing this policy or the closed public runtime API; R4 closed through PR #273 at `{BASE}`, and V3-R5/#272 is ACTIVE without broadening this policy.",
)
replace_once(
    "docs/CTAN-RELEASE.md",
    "Development gate: V3-R1, V3-R2 and V3-R3 are complete. V3-R4/#267 has technically certified exact product `c79f3c73f1d51a30175e8259269504d029442a1c` in run `33855800767` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding and PDF/A-2b; its canonical closeout/R5 entry is still pending. V3-R5/#272 is prepared but blocked. A v3.0.0 CTAN upload remains forbidden until R4 closes canonically, R5 foundation freeze/final documentation closes, and the roadmap explicitly reaches release-ready state.",
    f"Development gate: V3-R1 through V3-R4 are complete. V3-R4/#267 certified exact product `{PRODUCT}` in run `33855800767` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding and PDF/A-2b, then closed through PR #273 at `{BASE}`. V3-R5/#272 is ACTIVE from that exact entry. A v3.0.0 CTAN upload remains forbidden until R5 foundation freeze/final documentation closes and the roadmap explicitly reaches release-ready state.",
)

# Final consistency assertions.
for path in ("docs/NORMATIVE-BASE.md", "docs/NORMATIVE-CURRENCY.md", "docs/MIGRATING-TO-V3.md"):
    if not Path(path).exists():
        raise SystemExit(f"missing authority document: {path}")

if "V3-R5/#272 is ACTIVE" not in Path("AGENTS.md").read_text(encoding="utf-8"):
    raise SystemExit("AGENTS does not expose active R5")
if "| V3-R4 | DONE |" not in Path("docs/ROADMAP-V3.0.0.md").read_text(encoding="utf-8"):
    raise SystemExit("roadmap does not close R4")
if "| V3-R5 | ACTIVE |" not in Path("docs/ROADMAP-V3.0.0.md").read_text(encoding="utf-8"):
    raise SystemExit("roadmap does not activate R5")

print("R4 closeout / R5 exact-entry activation reconciled")
