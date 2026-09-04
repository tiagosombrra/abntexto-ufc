from __future__ import annotations

import json
import re
from pathlib import Path

CANDIDATE = "c79f3c73f1d51a30175e8259269504d029442a1c"
B5_ENTRY = "e5d6ab1962ee04935ee68a6ae36f268350d59a3b"
B4_PRODUCT = "59b2bce7fa2eb1ef6cbb418ca12d8c08b9339390"
PR_RECONCILE = 266
PR_RECONCILE_HEAD = "268f515c0b9b1f9d3d563925fc68d3f65b85c76d"
PR_RECONCILE_STATIC = 33822238687
PR_RECONCILE_LINUX = 33822238656
PR_RECONCILE_LINUX_JOB = 100867206797
MAIN_STATIC = 33824038991
MAIN_RELEASE = 33824039033
MAIN_RELEASE_JOB = 100872747975
R4_ISSUE = 267
TODAY = "2026-09-03"

CONTRIBUTION = {
    "rules": 181,
    "automatic_partial": 113,
    "automatic_partial_bounded_positive": 113,
    "enforced_automatic": 37,
    "support_only": 14,
    "conditional_review": 10,
    "manual_review": 6,
    "not_applicable": 1,
    "automation_gap": 0,
}


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
roadmap["updated_at"] = TODAY
roadmap["phase"] = "V3-R3"
roadmap["stage"] = "R3-B5"
roadmap["stage_name"] = "R3 closeout and R4 certification entry"
roadmap["status"] = "ACTIVE"
active = roadmap["active_implementation_lot"]
active.update({
    "phase": "V3-R3",
    "stage": "R3-B5",
    "issue": 256,
    "id": "R3-B5",
    "name": "R3 closeout and R4 certification entry",
    "status": "ACTIVE",
    "entry_product_main_sha": B4_PRODUCT,
    "entry_main_sha": B5_ENTRY,
    "final_r3_candidate_main_sha": CANDIDATE,
    "technical_validation_status": "DONE",
    "exact_r4_entry_activation_pending": True,
})
roadmap["r4_preparation"] = {
    "status": "PREPARED",
    "issue": R4_ISSUE,
    "product_candidate_main_sha": CANDIDATE,
    "entry_main_sha": None,
    "certification_started": False,
    "blocked_until_exact_entry_activation": True,
}
r3 = roadmap["r3"]
r3.update({"status": "ACTIVE", "stage": "R3-B5", "stage_name": "R3 closeout and R4 certification entry", "issue": 256, "active_issue": 256, "next_issue": 256})
b5 = r3["lots"]["R3-B5"]
b5.update({
    "status": "ACTIVE",
    "issue": 256,
    "entry_main_sha": B5_ENTRY,
    "entry_product_main_sha": B4_PRODUCT,
    "control_plane_reconciliation_pr": PR_RECONCILE,
    "control_plane_reconciliation_main_sha": CANDIDATE,
    "final_r3_candidate_main_sha": CANDIDATE,
    "technical_validation_status": "DONE",
    "exact_r4_entry_activation_pending": True,
})
r3["b5_validation"] = {
    "status": "DONE",
    "candidate_main_sha": CANDIDATE,
    "control_plane_reconciliation_pr": PR_RECONCILE,
    "control_plane_reconciliation_head_sha": PR_RECONCILE_HEAD,
    "static_contract_run_id": PR_RECONCILE_STATIC,
    "linux_integration_run_id": PR_RECONCILE_LINUX,
    "linux_integration_job_id": PR_RECONCILE_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "post_merge_static_run_id": MAIN_STATIC,
    "post_merge_release_run_id": MAIN_RELEASE,
    "post_merge_release_job_id": MAIN_RELEASE_JOB,
    "post_merge_release_result": "PASS=33 FAIL=0 SKIP=0",
    "contribution": CONTRIBUTION,
    "residual_sources": {"latex": 134, "engineering": 171, "total": 305},
    "test_surface": {"retained": 148, "reachable": 148, "orphaned": 0},
    "engineering_language": {
        "portuguese_technical_diagnostics": 0,
        "retired_profile_ids": 0,
        "closed_unconsumed_contracts": 0,
        "live_api_contract_consumers": 2,
    },
    "temporary_executor_residue": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
}
roadmap["next_stage"] = "R3-B5"
roadmap["next_issue"] = 256
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
inventory.update({"stage": "R3-B5", "status": "ACTIVE", "reviewed_at": TODAY, "current_entry_main_sha": CANDIDATE, "next_stage": "R3-B5", "next_issue": 256})
inv_b5 = inventory["lots"]["R3-B5"]
inv_b5.update({
    "status": "ACTIVE",
    "entry_product_main_sha": B4_PRODUCT,
    "entry_main_sha": B5_ENTRY,
    "control_plane_reconciliation_pr": PR_RECONCILE,
    "control_plane_reconciliation_main_sha": CANDIDATE,
    "final_r3_candidate_main_sha": CANDIDATE,
    "technical_validation_status": "DONE",
    "exact_r4_entry_activation_pending": True,
})
inventory["r3_b5_validation"] = roadmap["r3"]["b5_validation"]
inventory["r4_preparation"] = roadmap["r4_preparation"]
save_json("release/v3-r3-inventory.json", inventory)

set_updated("docs/ROADMAP-V3.0.0.md")
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A DONE; R3-B1 DONE; R3-B2 DONE; R3-B3 DONE; R3-B4 DONE; R3-B5 ACTIVE.**",
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 ACTIVE — R3-A and R3-B1 through R3-B4 DONE; R3-B5/#256 TECHNICALLY VALIDATED; exact R4 entry activation pending. V3-R4/#267 is PREPARED but not started.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| R3-B5 | ACTIVE | issue #256; control-plane entry `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` | R3 closeout and immutable R4 entry | reconcile final candidate; run Static + full Linux; record exact R4 entry SHA |\n| V3-R4 | BLOCKED | — | final certification | after R3-B5 |",
    "| R3-B5 | ACTIVE — VALIDATED | issue #256; candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | final tree: Static PASS; PR Linux `31/0/0`; post-merge release `33/0/0`; all R3 findings resolved | merge exact-entry checkpoint and close R3 |\n| V3-R4 | PREPARED / BLOCKED | issue #267; product candidate `c79f3c73f1d51a30175e8259269504d029442a1c` | certification scope defined; certification not started | activate only after exact R3 closeout entry is recorded |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## R3-B5 entry\n\n.*?\n\n## Immediate action\n\n.*?$",
    """## R3-B5 validation checkpoint

R3-B5/#256 entered through the canonical B4→B5 control-plane checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b`. PR #266 then repaired stale nested machine-state pointers and squash-merged as candidate `c79f3c73f1d51a30175e8259269504d029442a1c`. Its Static contract `33822238687` passed; Linux integration `33822238656` / job `100867206797` passed `PASS=31 FAIL=0 SKIP=0`; exact-main Static `33824038991` passed; exact-main Linux release `33824039033` / job `100872747975` passed `PASS=33 FAIL=0 SKIP=0`. The final contribution remains 113/113 `automatic-partial` bounded-positive, 37 enforced-automatic, 14 support-only, 10 conditional-review, 6 manual-review, 1 not-applicable, and zero automation gaps.

All R3-A findings are resolved. The permanent residual baseline is 305 sources (134 LaTeX + 171 engineering), retained test/check reachability is 148/148 with zero orphans, Portuguese project-owned technical diagnostics are zero, retired profile IDs are zero, closed unconsumed migration contracts are zero, and `release/v3-api-migration.json` retains exactly two live consumers. No normative authority, precedence, rule ID, expected value, locator, tolerance, applicability, proof-state default, rendered requirement, source/currency fact, or public runtime API changed. Temporary executor residue is absent.

R4 planning issue #267 exists only as a prepared contract. No Windows/literal-font certification has started. Because a squash merge SHA cannot be recorded before it exists, the exact R4 entry is intentionally left pending for a second, minimal control-plane activation checkpoint after this validated B5 closeout is merged.

## Immediate action

Merge the validated R3-B5 closeout checkpoint, obtain its immutable main SHA, then perform one minimal exact-entry activation that marks V3-R3/R3-B5 DONE and V3-R4/#267 ACTIVE from that recorded predecessor. Do not run R4 certification before that activation. R5, V3-A1/A2, and CTAN submission remain blocked.""",
    flags=re.S,
)

Path("docs/HANDOFF-V3.0.0.md").write_text(f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **ACTIVE only for exact-entry closeout**.
- R3-A and R3-B1 through R3-B4: **DONE**.
- R3-B5/#256: **TECHNICALLY VALIDATED; exact R4 entry activation pending**.
- Canonical B5 entry: `{B5_ENTRY}` from PR #265.
- Final R3 product/control-plane candidate: `{CANDIDATE}` from PR #266.
- PR #266 Static: `{PR_RECONCILE_STATIC}` — PASS.
- PR #266 Linux: `{PR_RECONCILE_LINUX}` / job `{PR_RECONCILE_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`.
- Exact-main Static: `{MAIN_STATIC}` — PASS.
- Exact-main release: `{MAIN_RELEASE}` / job `{MAIN_RELEASE_JOB}` — `PASS=33 FAIL=0 SKIP=0`.
- Evidence contribution: 113/113 `automatic-partial` bounded-positive; 37 enforced-automatic; 14 support-only; 10 conditional-review; 6 manual-review; 1 not-applicable; zero automation gaps.
- Residual baseline: 305 sources (134 LaTeX + 171 engineering).
- Retained test/check reachability: 148/148; zero orphans.
- Engineering-language baseline: zero Portuguese technical diagnostics; zero retired profile IDs; zero closed unconsumed contracts; two live `v3-api-migration` consumers.
- All R3-A findings: **RESOLVED**.
- R4 planning issue: **#267 PREPARED; certification not started**.
- Certified R1 historical candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; current-candidate literal-font recertification remains R4-owned.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Why R3 is not marked DONE yet

The final R3 candidate is technically green, but the roadmap requires an exact immutable R4 entry. A squash-merge SHA does not exist before the merge that creates it. Therefore this checkpoint records completed B5 validation without inventing a future SHA. After this closeout merges, one minimal control-plane activation records that real predecessor SHA, marks R3-B5 and V3-R3 DONE, and activates V3-R4/#267.

## Immediate action

Merge this validated B5 closeout, capture its immutable main SHA, then perform the exact-entry activation. Do not start Windows/literal-font/PDF-A certification before the activation checkpoint is canonical.

## Hard boundaries

Preserve the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged. R5 foundation freeze, V3-A1/A2 scientific-article work, and CTAN submission remain blocked.
""", encoding="utf-8")

set_updated("docs/R3-HARDENING-INVENTORY.md")
regex_once(
    "docs/R3-HARDENING-INVENTORY.md",
    r"\| R3-B5/#256 \| ACTIVE \|.*?\|",
    "| R3-B5/#256 | ACTIVE — VALIDATED | candidate `c79f3c73f1d51a30175e8259269504d029442a1c`; PR Linux `31/0/0`; release `33/0/0`; exact-entry activation pending |",
)
regex_once(
    "docs/R3-HARDENING-INVENTORY.md",
    r"## R3-B5 entry contract\n\n.*?$",
    """## R3-B5 validation closeout

B5 entered canonically at `e5d6ab1962ee04935ee68a6ae36f268350d59a3b`, reconciled stale control-plane state through PR #266, and produced final candidate `c79f3c73f1d51a30175e8259269504d029442a1c`. PR Static `33822238687` passed; PR Linux `33822238656` / job `100867206797` passed `PASS=31 FAIL=0 SKIP=0`; exact-main Static `33824038991` passed; exact-main release `33824039033` / job `100872747975` passed `PASS=33 FAIL=0 SKIP=0`. All 12 R3-A findings are resolved; no proof-contributing FAIL/UNASSESSED is represented as PASS; automation-gap is zero; residual/language/test-surface contracts remain green; no temporary executor or closed cleanup-only migration residue remains.

R4 issue #267 is prepared but blocked. This checkpoint deliberately does not perform Windows/literal-font certification and does not invent the future merge SHA required as the exact R4 entry. The next action is a minimal exact-entry activation after this validated closeout merges.

No source/currency fact, normative semantics, proof-state default, locator/tolerance/applicability policy, rendered requirement, or public runtime API changed in B5; `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain intentionally unchanged.""",
    flags=re.S,
)

regex_once(
    "README.md",
    r"\*\*V3-R1 and V3-R2 are DONE\..*?\*\*",
    "**V3-R1 and V3-R2 are DONE. V3-R3 is ACTIVE only for exact-entry closeout: R3-B5/#256 is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`; V3-R4/#267 is prepared but certification has not started.**",
)
replace_once(
    "README.md",
    "R3-B5/#256 is active from the canonical B4->B5 control-plane checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` (PR #265). The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; final Windows/literal-font recertification remains R4-owned.",
    "R3-B5/#256 entered from the canonical B4->B5 checkpoint `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`: PR #266 Linux passed `PASS=31 FAIL=0 SKIP=0`, exact-main Static passed, and exact-main release passed `PASS=33 FAIL=0 SKIP=0`. Exact R4 entry activation remains pending; issue #267 is prepared and no certification has started. The certified R1 candidate remains `9b1752565ac217c04ffa22a9ef272cdf078af380`; current-candidate Windows/literal-font recertification remains R4-owned.",
)
replace_once(
    "README.md",
    "R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 is active from `e5d6ab1962ee04935ee68a6ae36f268350d59a3b` and owns final R3 reconciliation plus the exact R4 certification entry.",
    "R3-B3/#254 and R3-B4/#255 are complete; R3-B5/#256 has completed technical validation on `c79f3c73f1d51a30175e8259269504d029442a1c` and now owns only the exact-entry closeout. R4/#267 is prepared but remains blocked until that checkpoint is canonical.",
)

replace_once(
    "AGENTS.md",
    "R3-B5/#256 is ACTIVE from that canonical checkpoint and owns R3 closeout plus the immutable R4 entry. Do not start R4 certification before B5 closes.",
    "R3-B5/#256 is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`: PR #266 Linux passed `PASS=31 FAIL=0 SKIP=0`, exact-main Static passed, and exact-main release passed `PASS=33 FAIL=0 SKIP=0`. It remains ACTIVE only until the exact immutable R4 entry is recorded. R4/#267 is PREPARED but certification must not start before that activation checkpoint is canonical.",
)

for path in ["docs/ARCHITECTURE.md", "docs/ENGINEERING-LANGUAGE.md", "docs/CTAN-RELEASE.md"]:
    set_updated(path)

regex_once(
    "docs/ARCHITECTURE.md",
    r"R3-B5/#256 is ACTIVE and owns only R3 closeout/R4 entry\.",
    "R3-B5/#256 has completed technical validation on `c79f3c73f1d51a30175e8259269504d029442a1c` and remains active only for the exact-entry checkpoint; R4/#267 is prepared but certification has not started.",
)
regex_once(
    "docs/ARCHITECTURE.md",
    r"R3-B5 now owns final cross-surface reconciliation and the immutable R4 entry checkpoint\.",
    "R3-B5 has completed final cross-surface validation; only the exact immutable R4 entry activation remains. R4/#267 must certify the current candidate after that checkpoint rather than relying on the historical R1 certification alone.",
)
regex_once(
    "docs/ENGINEERING-LANGUAGE.md",
    r"R3-B5/#256 is ACTIVE and owns R3 closeout/R4 entry; it must not broaden this policy or change the public runtime API\.",
    "R3-B5/#256 is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`; only exact-entry activation remains. R4/#267 is prepared but not started, and neither stage may broaden this policy or change the public runtime API without separately justified evidence.",
)
regex_once(
    "docs/CTAN-RELEASE.md",
    r"R3-B5/#256 is active and remains required before R4\.",
    "R3-B5/#256 is technically validated on `c79f3c73f1d51a30175e8259269504d029442a1c`; exact-entry activation remains required before R4/#267 certification can start.",
)

for protected in ["docs/NORMATIVE-BASE.md", "docs/NORMATIVE-CURRENCY.md", "docs/MIGRATING-TO-V3.md"]:
    if not Path(protected).exists():
        raise SystemExit(f"missing protected document: {protected}")

print("R3-B5 preparation reconciliation complete")
