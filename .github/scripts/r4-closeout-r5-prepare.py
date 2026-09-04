from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "438217d004ab0b6fdc430131082b4d749adc5266"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
R4_ENTRY = "d90a675a844724c33a5727d8d980027c46291eb0"
R4_ISSUE = 267
R5_ISSUE = 272
RUN = 33855800767
PREFLIGHT_JOB = 100968686875
WINDOWS_JOB = 100968747942
LINUX_JOB = 100970109387
CLEANUP_JOB = 100970307670
EVIDENCE_ARTIFACT = 9930304564
EVIDENCE_DIGEST = "sha256:ca21bf1771c45e2003b2448ea019b6eb7b93c8468eff1330df76340a943eeca2"
PDF_ARTIFACT = 9930280624
PDF_DIGEST = "sha256:934044738f21261137014984114d33516b8601c0710107687903ad2f59a6b565"
TODAY = "2026-09-04"

CASES = [
    {"engine": "pdflatex", "family": "times", "sha256": "aa9657e43ab3d1dd46e1f93b6ea1366854735a5807a5f8b643b4fde846bfc84b", "math_font_policy": "NEW-TX-MATH"},
    {"engine": "pdflatex", "family": "arial", "sha256": "91d013843d4d7241ef7d07e8ae06ed47fb68f91249789214101c18701de751c9", "math_font_policy": "NEW-TX-MATH"},
    {"engine": "lualatex", "family": "times", "sha256": "a1616beb5035841895bfbf9483ead1a210671ce897e08444adece81824f71a85", "math_font_policy": "OPEN-TYPE-MATH"},
    {"engine": "lualatex", "family": "arial", "sha256": "5905b02bfb56f7b434e89d099d38c262e428b49a18dfb986c4ff22c0103f83d2", "math_font_policy": "OPEN-TYPE-MATH"},
]
for case in CASES:
    case.update({
        "literal_text_family": "PASS",
        "unexpected_text_substitution": "ABSENT",
        "unicode_extraction": "PASS",
        "font_embedding": "PASS",
        "pdfa_2b": "PASS",
    })


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"expected one match in {path}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected one regex match in {path}: {pattern!r}; found {count}")
    p.write_text(updated, encoding="utf-8")


def set_updated(path: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    text, count = re.subn(r"^Updated: \d{4}-\d{2}-\d{2}$", f"Updated: {TODAY}", text, count=1, flags=re.M)
    if count:
        p.write_text(text, encoding="utf-8")


cert = {
    "status": "DONE",
    "issue": R4_ISSUE,
    "product_candidate_main_sha": PRODUCT,
    "r4_entry_predecessor_sha": R4_ENTRY,
    "certification_launch_main_sha": BASE,
    "workflow_run_id": RUN,
    "preflight_job_id": PREFLIGHT_JOB,
    "windows_job_id": WINDOWS_JOB,
    "linux_job_id": LINUX_JOB,
    "cleanup_job_id": CLEANUP_JOB,
    "workflow_conclusion": "success",
    "product_equivalence_to_launch_main": "PASS",
    "windows_matrix_result": "PASS",
    "linux_final_inspection_result": "PASS",
    "evidence_artifact_id": EVIDENCE_ARTIFACT,
    "evidence_artifact_digest": EVIDENCE_DIGEST,
    "windows_pdf_artifact_id": PDF_ARTIFACT,
    "windows_pdf_artifact_digest": PDF_DIGEST,
    "cases": CASES,
    "temporary_certification_workflow_removed": True,
    "runtime_api_changed": False,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "proprietary_fonts_redistributed": False,
    "inspection_note": "TeXGyreTermesX-Regular is accepted only as part of the pdfLaTeX newtxmath stack; literal institutional text-family identity is certified independently.",
}

roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-R4" or roadmap.get("stage") != "V3-R4":
    raise SystemExit("unexpected roadmap stage")
r4 = roadmap.get("r4", {})
if r4.get("status") != "ACTIVE" or r4.get("product_candidate_main_sha") != PRODUCT:
    raise SystemExit("unexpected R4 state")
if r4.get("certification_started") is not False:
    raise SystemExit("R4 certification state was already reconciled")

roadmap["updated_at"] = TODAY
roadmap["stage_name"] = "R4 certification closeout and R5 entry"
roadmap["active_implementation_lot"] = {
    "phase": "V3-R4",
    "stage": "V3-R4",
    "issue": R4_ISSUE,
    "entry_product_main_sha": PRODUCT,
    "name": "R4 certification closeout and R5 entry",
    "id": "V3-R4",
    "status": "ACTIVE",
    "entry_main_sha": R4_ENTRY,
    "certification_status": "DONE",
    "exact_r5_entry_activation_pending": True,
}
r4.update({
    "status": "ACTIVE",
    "certification_started": True,
    "certification_status": "DONE",
    "certification_run_id": RUN,
    "exact_r5_entry_activation_pending": True,
})
roadmap["r4_certification"] = cert
roadmap["r4_preparation"].update({
    "status": "ACTIVE",
    "certification_started": True,
    "certification_status": "DONE",
})
roadmap["r5_preparation"] = {
    "status": "PREPARED",
    "issue": R5_ISSUE,
    "certified_product_candidate_main_sha": PRODUCT,
    "entry_main_sha": None,
    "blocked_until_exact_r4_closeout": True,
    "foundation_freeze_started": False,
}
roadmap["next_stage"] = "V3-R4"
roadmap["next_issue"] = R4_ISSUE
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
if inventory.get("status") != "DONE":
    raise SystemExit("R3 inventory must already be DONE")
inventory["reviewed_at"] = TODAY
inventory["r4_transition"] = {
    "status": "CERTIFIED_PENDING_CANONICAL_CLOSEOUT",
    "issue": R4_ISSUE,
    "r5_issue": R5_ISSUE,
    "product_candidate_main_sha": PRODUCT,
    "r4_entry_predecessor_sha": R4_ENTRY,
    "certification_run_id": RUN,
    "certification_result": "PASS",
    "evidence_artifact_id": EVIDENCE_ARTIFACT,
    "evidence_artifact_digest": EVIDENCE_DIGEST,
    "exact_r5_entry_activation_pending": True,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
save_json("release/v3-r3-inventory.json", inventory)

for path in [
    "docs/ROADMAP-V3.0.0.md", "docs/HANDOFF-V3.0.0.md", "docs/R3-HARDENING-INVENTORY.md",
    "docs/ARCHITECTURE.md", "docs/ENGINEERING-LANGUAGE.md"
]:
    set_updated(path)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE — R3-A and R3-B1 through R3-B5 complete. V3-R4/#267 ACTIVE from exact predecessor `{R4_ENTRY}`; certification has not started yet.**",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 ACTIVE — final certification PASSED on `{PRODUCT}`; exact R5 entry activation is pending. V3-R5/#272 is PREPARED / BLOCKED.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"| V3-R4 | ACTIVE | issue #267; entry predecessor `{R4_ENTRY}`; product candidate `{PRODUCT}` | certification scope active; certification not started | run Windows literal-font matrix, Unicode/embedding and PDF/A-2b certification |\n| V3-R5 | BLOCKED | — | foundation freeze and final docs | after R4 |",
    f"| V3-R4 | ACTIVE — CERTIFIED | issue #267; entry predecessor `{R4_ENTRY}`; product candidate `{PRODUCT}`; run `{RUN}` | exact candidate passed Windows Times/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding, independent math policy and PDF/A-2b; temporary executor removed | merge certification closeout, record its immutable SHA, then close R4 |\n| V3-R5 | PREPARED / BLOCKED | issue #272; certified product `{PRODUCT}` | foundation-freeze contract defined | activate only after exact R4 closeout entry is recorded |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## Immediate action\n\nExecute V3-R4/#267 final certification.*?$",
    f"""## V3-R4 certification result

V3-R4/#267 certification run `{RUN}` completed successfully against exact product candidate `{PRODUCT}`. Preflight job `{PREFLIGHT_JOB}` proved the launch `main` differed from the product only in the expected ten documentation/control-plane files and passed `make static-check`. Windows job `{WINDOWS_JOB}` compiled the strict four-cell Times New Roman/Arial × pdfLaTeX/LuaLaTeX matrix. Linux job `{LINUX_JOB}` verified literal institutional text-family identity independently from math-font policy, Unicode extraction, complete font embedding and PDF/A-2b for all four artifacts. Cleanup job `{CLEANUP_JOB}` removed the temporary certification workflow.

The evidence artifact is `{EVIDENCE_ARTIFACT}` with digest `{EVIDENCE_DIGEST}`; the Windows PDF matrix artifact is `{PDF_ARTIFACT}` with digest `{PDF_DIGEST}`. pdfLaTeX correctly uses `NEW-TX-MATH`; `TeXGyreTermesX-Regular` is accepted only as part of that math stack and is not treated as institutional text fallback. LuaLaTeX uses the independent OpenType math route. No runtime API, normative semantics or proof-state default changed, and proprietary Microsoft fonts were not redistributed.

R4 is therefore technically certified but remains canonically ACTIVE until the closeout checkpoint itself is merged and its immutable SHA can be recorded as the exact R5 entry. V3-R5/#272 is prepared and blocked on that SHA.

## Immediate action

Merge this R4 certification closeout, capture its immutable main SHA, then perform one minimal exact-entry activation that marks V3-R4/#267 DONE, activates V3-R5/#272 from that predecessor, and closes #267. Do not start R5 foundation-freeze work before that activation is canonical. V3-A1/A2 and CTAN submission remain blocked.""",
    flags=re.S,
)

Path("docs/HANDOFF-V3.0.0.md").write_text(f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **TECHNICALLY CERTIFIED; exact R5 entry activation pending**.
- R4 entry predecessor: `{R4_ENTRY}`.
- Certified product candidate: `{PRODUCT}`.
- R4 certification workflow: `{RUN}` — SUCCESS.
- Preflight job: `{PREFLIGHT_JOB}` — PASS.
- Windows strict matrix job: `{WINDOWS_JOB}` — PASS.
- Linux final font/PDF-A job: `{LINUX_JOB}` — PASS.
- Cleanup job: `{CLEANUP_JOB}` — PASS; temporary workflow absent from final certification branch.
- Evidence artifact: `{EVIDENCE_ARTIFACT}` / `{EVIDENCE_DIGEST}`.
- Windows PDF artifact: `{PDF_ARTIFACT}` / `{PDF_DIGEST}`.
- Four matrix cells: literal text family PASS; Unicode extraction PASS; font embedding PASS; PDF/A-2b PASS; unexpected text substitution ABSENT.
- pdfLaTeX math policy: `NEW-TX-MATH`; LuaLaTeX math policy: independent OpenType math.
- V3-R5/#272: **PREPARED / BLOCKED** until the immutable R4 closeout merge SHA exists.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Why R4 is not marked DONE yet

The certification itself is complete, but R5 requires one exact immutable entry checkpoint. That SHA cannot be known before the closeout PR is merged. This checkpoint therefore records the real certification receipts without inventing a future SHA.

## Immediate action

Merge the validated R4 certification closeout, capture its immutable main SHA, and perform the minimal exact-entry activation that closes #267 and activates V3-R5/#272. Do not begin R5 work before that activation is canonical.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. Do not redistribute proprietary Microsoft fonts. V3-A1/A2 scientific-article work and CTAN submission remain blocked until R5 closes.
""", encoding="utf-8")

replace_once(
    "README.md",
    f"**V3-R1, V3-R2 and V3-R3 are DONE. V3-R4/#267 is ACTIVE from exact predecessor `{R4_ENTRY}`, bound to product candidate `{PRODUCT}`; certification execution has not started.**",
    f"**V3-R1, V3-R2 and V3-R3 are DONE. V3-R4/#267 is technically CERTIFIED on `{PRODUCT}` by run `{RUN}`; exact R5 entry activation remains pending. V3-R5/#272 is prepared but blocked.**",
)
replace_once(
    "README.md",
    "R3-B5 closed through PR #268 at `d90a675a844724c33a5727d8d980027c46291eb0`; issue #267 is now the active R4 certification lot and certification execution has not started. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; current-candidate Windows/literal-font recertification remains R4-owned.",
    f"R3-B5 closed through PR #268 at `{R4_ENTRY}`. R4/#267 then certified exact product `{PRODUCT}` in run `{RUN}`: preflight, Windows strict matrix, Linux literal-font/Unicode/embedding/PDF-A inspection and cleanup all passed. Exact R5 entry activation remains pending; #272 is prepared/blocked. The historical R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380` only as historical certification evidence.",
)
replace_once(
    "README.md",
    "R4/#267 is active and owns current-candidate Windows/literal-font/Unicode/embedding/PDF-A certification.",
    f"R4/#267 has completed current-candidate Windows/literal-font/Unicode/embedding/PDF-A certification in run `{RUN}` and now owns only canonical closeout/R5-entry activation; R5/#272 is prepared but blocked.",
)

replace_once(
    "AGENTS.md",
    f"- V3-R3 is DONE. R3-A/#250 and R3-B1 through R3-B5 are complete; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` preserve the closed evidence-driven sequence. V3-R4/#267 is ACTIVE from exact predecessor `{R4_ENTRY}`.",
    f"- V3-R3 is DONE. R3-A/#250 and R3-B1 through R3-B5 are complete; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` preserve the closed sequence. V3-R4/#267 is technically certified on `{PRODUCT}` by run `{RUN}` and remains ACTIVE only for exact R5 entry closeout; V3-R5/#272 is PREPARED/BLOCKED.",
)
replace_once(
    "AGENTS.md",
    f"V3-R4/#267 is ACTIVE; certification execution has not started.",
    f"V3-R4/#267 certification run `{RUN}` passed the exact Times/Arial × pdfLaTeX/LuaLaTeX matrix, Unicode extraction, embedding and PDF/A-2b; the temporary executor was removed. R4 remains ACTIVE only until its closeout merge SHA is recorded as the exact V3-R5/#272 entry.",
)

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    f"R3-B5/#256 is DONE through PR #268 at `{R4_ENTRY}`; V3-R4/#267 is ACTIVE and must preserve this policy and the closed public runtime API during certification.",
    f"R3-B5/#256 is DONE through PR #268 at `{R4_ENTRY}`. V3-R4/#267 certification run `{RUN}` passed on `{PRODUCT}` without changing this policy or the closed public runtime API; only exact R5 entry closeout remains.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    f"R3-B5/#256 and V3-R3 are DONE through validated closeout PR #268 at `{R4_ENTRY}`. V3-R4/#267 is ACTIVE on product candidate `{PRODUCT}`; certification execution has not started.",
    f"R3-B5/#256 and V3-R3 are DONE through validated closeout PR #268 at `{R4_ENTRY}`. V3-R4/#267 certification run `{RUN}` passed on exact product `{PRODUCT}` across the strict four-cell font/engine matrix plus Unicode, embedding and PDF/A-2b; canonical closeout/R5-entry activation remains pending.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    f"R4/#267 must now certify the current candidate rather than relying on the historical R1 certification alone.",
    f"R4/#267 has now independently certified the current candidate in run `{RUN}` rather than relying on the historical R1 evidence. The product architecture remains unchanged; only the control-plane closeout that establishes the exact R5 entry is pending.",
)

regex_once(
    "docs/CTAN-RELEASE.md",
    r"^- Development gate: .*?$",
    f"- Development gate: V3-R1, V3-R2 and V3-R3 are complete. V3-R4/#267 has technically certified exact product `{PRODUCT}` in run `{RUN}` across Times New Roman/Arial × pdfLaTeX/LuaLaTeX, Unicode extraction, embedding and PDF/A-2b; its canonical closeout/R5 entry is still pending. V3-R5/#272 is prepared but blocked. A v3.0.0 CTAN upload remains forbidden until R4 closes canonically, R5 foundation freeze/final documentation closes, and the roadmap explicitly reaches release-ready state.",
    flags=re.M,
)

replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    f"R4 issue #267 is active from exact predecessor `{R4_ENTRY}`. This R3 closeout did not perform Windows/literal-font certification; that certification is now the bounded R4 responsibility on product candidate `{PRODUCT}`.",
    f"R4 issue #267 entered from exact predecessor `{R4_ENTRY}` and has now technically certified product `{PRODUCT}` in run `{RUN}`. All four strict Times/Arial × pdfLaTeX/LuaLaTeX cases passed literal text-family identity, Unicode extraction, embedding and PDF/A-2b; exact R5 entry closeout remains outside the closed R3 inventory.",
)

print("R4 closeout documentation and machine state reconciled")
