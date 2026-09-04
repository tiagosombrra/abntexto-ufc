from __future__ import annotations

import json
from pathlib import Path

BASE = "d90a675a844724c33a5727d8d980027c46291eb0"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
TODAY = "2026-09-04"


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path}: {old!r}; found {count}")
    target.write_text(text.replace(old, new), encoding="utf-8")


def update_date(path: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    old = "Updated: 2026-09-03"
    if text.count(old) != 1:
        raise SystemExit(f"unexpected Updated header in {path}")
    target.write_text(text.replace(old, f"Updated: {TODAY}", 1), encoding="utf-8")


for path in (
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "docs/R3-HARDENING-INVENTORY.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
):
    update_date(path)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "Active implementation issue: #256. Machine authority: `release/v3-roadmap.json`.",
    "Active certification issue: #267 (V3-R4). Machine authority: `release/v3-roadmap.json`.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "The Linux observations are engineering evidence; final Windows/literal-font/PDF-A certification remains B8-owned.",
    "The Linux observations are engineering evidence. Historical R1 final Windows/literal-font/PDF-A certification was B8-owned; current-candidate recertification is V3-R4/#267-owned.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    "A v3.0.0 CTAN upload must not be performed during R3: publication remains a later explicit action after R3 hardening, R4 certification, and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
    "A v3.0.0 CTAN upload must not be performed during R4: publication remains a later explicit action after R4 certification and R5 foundation freeze/final documentation reach the roadmap's release-ready state and the intended candidate is revalidated proportionally.",
)
replace_once(
    "docs/CTAN-RELEASE.md",
    "This Linux evidence is not final B8 Windows/literal-font/PDF-A certification and is not CTAN acceptance.",
    "This Linux evidence is not final current-candidate V3-R4 Windows/literal-font/PDF-A certification and is not CTAN acceptance.",
)
replace_once(
    "docs/CTAN-RELEASE.md",
    "3. Confirm that the intended release commit is still covered by, or has proportionally re-established, the completed Windows/literal-font/PDF-A certification baseline from R1-BLOCK-8.",
    "3. Confirm that the intended release commit is covered by the completed current-candidate V3-R4 Windows/literal-font/PDF-A certification; the historical R1-BLOCK-8 baseline alone is insufficient for v3.0.0 release readiness.",
)

roadmap_path = Path("release/v3-roadmap.json")
roadmap = json.loads(roadmap_path.read_text(encoding="utf-8"))
if roadmap.get("phase") != "V3-R4" or roadmap.get("stage") != "V3-R4":
    raise SystemExit("release/v3-roadmap.json is not at V3-R4")
active = roadmap.get("active_implementation_lot", {})
if active.get("issue") != 267 or active.get("entry_main_sha") != BASE or active.get("entry_product_main_sha") != PRODUCT:
    raise SystemExit("unexpected active V3-R4 lot")
if roadmap.get("r3", {}).get("status") != "DONE":
    raise SystemExit("R3 is not DONE in machine state")
if roadmap.get("r3", {}).get("lots", {}).get("R3-B5", {}).get("status") != "DONE":
    raise SystemExit("R3-B5 is not DONE in machine state")
if roadmap.get("r4_preparation", {}).get("entry_main_sha") != BASE:
    raise SystemExit("R4 predecessor does not match exact closeout main")
roadmap["updated_at"] = TODAY
roadmap["next_action"] = (
    "Execute V3-R4/#267 final certification on product candidate " + PRODUCT +
    " from exact control-plane predecessor " + BASE +
    ": certify Times New Roman/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, font embedding, independent math-font policy, and PDF/A-2b; keep temporary certification executors atomic and do not start V3-R5, V3-A1/A2, or CTAN submission before R4 closes."
)
roadmap["next_stage"] = "V3-R4"
roadmap["next_issue"] = 267
roadmap_path.write_text(json.dumps(roadmap, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

inventory_path = Path("release/v3-r3-inventory.json")
inventory = json.loads(inventory_path.read_text(encoding="utf-8"))
if inventory.get("status") != "DONE":
    raise SystemExit("R3 inventory is not DONE")
if inventory.get("lots", {}).get("R3-B5", {}).get("status") != "DONE":
    raise SystemExit("R3-B5 inventory lot is not DONE")
if inventory.get("r4_preparation", {}).get("entry_main_sha") != BASE:
    raise SystemExit("R3 inventory R4 predecessor mismatch")
inventory["reviewed_at"] = TODAY
inventory["next_stage"] = "V3-R4"
inventory["next_issue"] = 267
inventory_path.write_text(json.dumps(inventory, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")

roadmap_text = Path("docs/ROADMAP-V3.0.0.md").read_text(encoding="utf-8")
if "Active implementation issue: #256" in roadmap_text:
    raise SystemExit("stale active issue #256 remains in roadmap")
if "| R3-B5 | DONE |" not in roadmap_text or "| V3-R4 | ACTIVE |" not in roadmap_text:
    raise SystemExit("roadmap table does not reflect R3 DONE / R4 ACTIVE")
if "V3-R4/#267: **ACTIVE**" not in Path("docs/HANDOFF-V3.0.0.md").read_text(encoding="utf-8"):
    raise SystemExit("handoff does not expose active R4")

print("R3/R4 final control-plane reconciliation passed")
