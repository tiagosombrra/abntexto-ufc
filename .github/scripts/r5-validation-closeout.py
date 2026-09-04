from __future__ import annotations

import json
import re
from pathlib import Path

MAIN = "ff833d814133d33887df8971f6a0af702d6c2143"
R5_ENTRY = "0b0f5d989163dc6b1429feeb2d8a7c66988647bb"
PRODUCT = "c79f3c73f1d51a30175e8259269504d029442a1c"
R4_RUN = 33855800767
R5_RELEASE_RUN = 33866258865
R5_RELEASE_JOB = 101001704635
R5_PACKAGE_RUN = 33869888601
R5_PACKAGE_JOB = 101013093747
R5_ISSUE = 272
A1_ISSUE = 275
TODAY = "2026-09-04"


def load_json(path: str) -> dict:
    return json.loads(Path(path).read_text(encoding="utf-8"))


def save_json(path: str, data: dict) -> None:
    Path(path).write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")


def replace_once(path: str, old: str, new: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one match in {path}: {count}: {old!r}")
    target.write_text(text.replace(old, new), encoding="utf-8")


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    updated, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected exactly one regex match in {path}: {count}: {pattern!r}")
    target.write_text(updated, encoding="utf-8")


def set_updated(path: str) -> None:
    target = Path(path)
    text = target.read_text(encoding="utf-8")
    updated, count = re.subn(r"^Updated: \d{4}-\d{2}-\d{2}$", f"Updated: {TODAY}", text, count=1, flags=re.M)
    if count == 1:
        target.write_text(updated, encoding="utf-8")


roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-R5" or roadmap.get("stage") != "V3-R5":
    raise SystemExit("unexpected canonical roadmap stage")
if roadmap.get("r5_preparation", {}).get("entry_main_sha") != R5_ENTRY:
    raise SystemExit("unexpected R5 entry")
if roadmap.get("r5_preparation", {}).get("certified_product_candidate_main_sha") != PRODUCT:
    raise SystemExit("unexpected certified product candidate")

validation = {
    "status": "DONE",
    "issue": R5_ISSUE,
    "entry_main_sha": R5_ENTRY,
    "control_plane_validation_base_main_sha": MAIN,
    "certified_product_candidate_main_sha": PRODUCT,
    "r4_certification_run_id": R4_RUN,
    "full_release_run_id": R5_RELEASE_RUN,
    "full_release_job_id": R5_RELEASE_JOB,
    "full_release_gate_result": "PASS=33 FAIL=0 SKIP=0",
    "full_release_workflow_conclusion": "failure-after-green-release-gate-during-initial-packaging-precondition",
    "package_validation_run_id": R5_PACKAGE_RUN,
    "package_validation_job_id": R5_PACKAGE_JOB,
    "package_validation_result": "PASS",
    "public_bundles_passed": True,
    "distribution_bundles_passed": True,
    "checksums_passed": True,
    "institutional_assets_excluded": True,
    "proprietary_assets_excluded": True,
    "product_tree_unchanged_since_certification": True,
    "normative_base_changed": False,
    "normative_currency_changed": False,
    "migration_guide_changed": False,
    "temporary_executor_residue": 0,
    "normative_semantics_changed": False,
    "proof_state_changed": False,
    "public_runtime_api_changed": False,
    "ctan_submission_started": False,
    "scientific_article_work_started": False,
}

roadmap["updated_at"] = TODAY
roadmap["r5_validation"] = validation
roadmap["r5_preparation"].update({
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "foundation_freeze_started": True,
    "technical_validation_status": "DONE",
    "exact_a1_entry_activation_pending": True,
    "validation_run_id": R5_PACKAGE_RUN,
    "validation_job_id": R5_PACKAGE_JOB,
})
roadmap["r5"].update({
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "foundation_freeze_started": True,
    "technical_validation_status": "DONE",
    "exact_a1_entry_activation_pending": True,
    "validation_run_id": R5_PACKAGE_RUN,
    "validation_job_id": R5_PACKAGE_JOB,
})
roadmap["active_implementation_lot"].update({
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "foundation_freeze_started": True,
    "technical_validation_status": "DONE",
    "exact_a1_entry_activation_pending": True,
})
roadmap["a1_preparation"] = {
    "status": "PREPARED",
    "issue": A1_ISSUE,
    "name": "reconfirm scientific-article authority and normative contract",
    "certified_foundation_product_sha": PRODUCT,
    "entry_main_sha": None,
    "blocked_until_exact_r5_closeout": True,
    "work_started": False,
    "runtime_implementation_allowed": False,
    "ctan_submission_allowed": False,
}
roadmap["next_stage"] = "V3-R5"
roadmap["next_issue"] = R5_ISSUE
save_json("release/v3-roadmap.json", roadmap)

inventory = load_json("release/v3-r3-inventory.json")
if inventory.get("status") != "DONE":
    raise SystemExit("R3 inventory is not closed")
inventory["reviewed_at"] = TODAY
inventory["r5_validation"] = validation
inventory["r5_preparation"].update({
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "foundation_freeze_started": True,
    "technical_validation_status": "DONE",
    "exact_a1_entry_activation_pending": True,
    "validation_run_id": R5_PACKAGE_RUN,
    "validation_job_id": R5_PACKAGE_JOB,
})
inventory["a1_preparation"] = {
    "status": "PREPARED",
    "issue": A1_ISSUE,
    "entry_main_sha": None,
    "blocked_until_exact_r5_closeout": True,
    "work_started": False,
}
save_json("release/v3-r3-inventory.json", inventory)

for path in (
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "docs/R3-HARDENING-INVENTORY.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
):
    set_updated(path)

replace_once(
    "README.md",
    f"**V3-R1, V3-R2, V3-R3 and V3-R4 are DONE. V3-R5/#272 is ACTIVE from exact predecessor `{R5_ENTRY}`; the certified foundation product remains `{PRODUCT}`.**",
    f"**V3-R1, V3-R2, V3-R3 and V3-R4 are DONE. V3-R5/#272 is TECHNICALLY VALIDATED from exact entry `{R5_ENTRY}` with certified foundation product `{PRODUCT}` unchanged; canonical closeout is pending so the future V3-A1 entry SHA is not yet invented.**",
)
replace_once(
    "README.md",
    f"R4/#267 has completed current-candidate Windows/literal-font/Unicode/embedding/PDF-A certification in run `{R4_RUN}` and now owns only canonical closeout/R5-entry activation; R5/#272 is prepared but blocked.",
    f"R4/#267 is DONE. R5/#272 has completed foundation-freeze validation: full release gate `PASS=33 FAIL=0 SKIP=0` in run `{R5_RELEASE_RUN}`, and package validation run `{R5_PACKAGE_RUN}` passed public/distribution bundle reproducibility, checksums and asset exclusions with zero workspace residue. R5 remains open only until its canonical closeout produces the immutable V3-A1/#275 entry; A1 is prepared but blocked and no article runtime work has started.",
)

replace_once(
    "AGENTS.md",
    f"- V3-R3 is DONE. R3-A/#250 and R3-B1 through R3-B5 are complete; `docs/R3-HARDENING-INVENTORY.md` and `release/v3-r3-inventory.json` preserve the closed sequence. V3-R4/#267 is DONE: run `{R4_RUN}` certified `{PRODUCT}`, and closeout PR #273 merged at exact R5 predecessor `{R5_ENTRY}`. V3-R5/#272 is ACTIVE from that predecessor; foundation-freeze execution has not started yet.",
    f"- V3-R3 and V3-R4 are DONE. R4 run `{R4_RUN}` certified `{PRODUCT}`, and PR #273 established exact R5 entry `{R5_ENTRY}`. V3-R5/#272 is TECHNICALLY VALIDATED: release gate run `{R5_RELEASE_RUN}` passed `PASS=33 FAIL=0 SKIP=0`, package run `{R5_PACKAGE_RUN}` passed reproducible public/distribution bundles, checksums, asset exclusions and zero residue, and the certified product is unchanged. R5 must remain open until a canonical closeout merge yields the immutable V3-A1/#275 entry; A1 is PREPARED/BLOCKED and must not start early.",
)
replace_once(
    "AGENTS.md",
    f"R4 closed through PR #273 at `{R5_ENTRY}`; V3-R5/#272 is ACTIVE from that exact immutable entry.",
    f"R4 closed through PR #273 at `{R5_ENTRY}`. V3-R5/#272 has completed technical freeze/package validation and is pending only canonical closeout; V3-A1/#275 is prepared but blocked until that future closeout SHA exists.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    f"R4 closeout `{R5_ENTRY}` establishes the exact R5 entry; V3-R5 now owns foundation freeze and final release-documentation validation without modifying the certified product.",
    f"R4 closeout `{R5_ENTRY}` establishes the exact R5 entry. V3-R5 has now validated foundation freeze without modifying certified product `{PRODUCT}`: source-only and release gates are green, public/distribution bundles are reproducible with valid checksums and asset exclusions, and temporary validation residue is zero. Only canonical R5 closeout remains before V3-A1/#275 may begin.",
)
insert_marker = "\n## Validator\n"
arch = Path("docs/ARCHITECTURE.md").read_text(encoding="utf-8")
if arch.count(insert_marker) != 1:
    raise SystemExit("unexpected architecture validator marker")
r5_arch = f"""
## R5 certified-foundation freeze

The frozen foundation product is `{PRODUCT}`, certified by R4 run `{R4_RUN}` and entered into R5 through `{R5_ENTRY}`. R5 validation does not create a new runtime candidate: run `{R5_RELEASE_RUN}` completed the 33-check release gate with `PASS=33 FAIL=0 SKIP=0`, while run `{R5_PACKAGE_RUN}` independently proved public and complete distribution reproducibility, checksum integrity, external-`abntexto` packaging semantics, institutional/proprietary asset exclusion and a clean workspace. `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md` remain unchanged because no source/currency/API fact changed. V3-A1/#275 is source/normative work and remains blocked until the R5 closeout merge supplies its immutable entry SHA.
"""
Path("docs/ARCHITECTURE.md").write_text(arch.replace(insert_marker, "\n" + r5_arch + insert_marker), encoding="utf-8")

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    f"R4 closed through PR #273 at `{R5_ENTRY}`, and V3-R5/#272 is ACTIVE without broadening this policy.",
    f"R4 closed through PR #273 at `{R5_ENTRY}`. V3-R5/#272 has completed technical foundation-freeze validation in run `{R5_PACKAGE_RUN}` without broadening this policy, changing the certified runtime, or introducing new engineering-language debt; V3-A1/#275 is prepared but blocked until canonical R5 closeout.",
)

regex_once(
    "docs/CTAN-RELEASE.md",
    r"^- Development gate: .*?$",
    f"- Development gate: V3-R1 through V3-R4 are complete. V3-R4/#267 certified exact product `{PRODUCT}` in run `{R4_RUN}` and closed through PR #273 at `{R5_ENTRY}`. V3-R5/#272 has completed technical freeze/release validation: the 33-check release gate passed in run `{R5_RELEASE_RUN}`, and package run `{R5_PACKAGE_RUN}` passed reproducible public/distribution bundles, SHA-256 checksums, external-upstream semantics and institutional/proprietary asset exclusions. Canonical R5 closeout is still required before V3-A1/#275 may start. Actual CTAN upload remains a separate explicit release action and has not occurred.",
    flags=re.M,
)

handoff = f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1: **DONE**.
- V3-R2: **DONE**.
- V3-R3: **DONE**.
- V3-R4/#267: **DONE**.
- R4 certified product: `{PRODUCT}`; certification run `{R4_RUN}` — SUCCESS.
- Exact V3-R5 entry: `{R5_ENTRY}` from R4 closeout PR #273.
- V3-R5/#272: **TECHNICALLY VALIDATED; canonical closeout pending**.
- Certified product invariance: **PASS** — no product-affecting path changed after `{PRODUCT}`.
- Full release gate: run `{R5_RELEASE_RUN}` / job `{R5_RELEASE_JOB}` completed `PASS=33 FAIL=0 SKIP=0`; that workflow later failed only during its initial packaging-precondition sequence, not in the release gate.
- Final package/freeze validation: run `{R5_PACKAGE_RUN}` / job `{R5_PACKAGE_JOB}` — SUCCESS.
- Public bundles: **PASS**; complete distribution bundles: **PASS**; reproducibility/checksums: **PASS**; institutional/proprietary asset exclusions: **PASS**.
- Tracked/untracked validation residue: **0**.
- `docs/NORMATIVE-BASE.md`, `docs/NORMATIVE-CURRENCY.md`, and `docs/MIGRATING-TO-V3.md`: intentionally unchanged; no source/currency/API fact required an edit.
- V3-A1/#275: **PREPARED / BLOCKED**. Its exact entry SHA does not exist until R5 closes canonically.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Promote the validated R5 documentation/control-plane checkpoint through the permanent PR gates. After its squash merge, capture the real immutable main SHA and perform one minimal exact-entry activation that marks V3-R5 DONE and activates V3-A1/#275 from that SHA. Do not invent the A1 entry before the merge and do not start article runtime work in A1.

## Hard boundaries

Preserve certified foundation `{PRODUCT}` and the closed v3 API; no runtime aliases. Do not change normative authority, precedence, rule IDs, values, locators, tolerances, applicability, proof-state defaults, or rendered requirements without current evidence. Do not redistribute proprietary Microsoft fonts or claim UFC homologation/CTAN acceptance. V3-A2 and actual CTAN submission remain blocked.
"""
Path("docs/HANDOFF-V3.0.0.md").write_text(handoff, encoding="utf-8")

replace_once(
    "docs/R3-HARDENING-INVENTORY.md",
    f"R4 then closed through PR #273 at `{R5_ENTRY}`, which is the exact V3-R5/#272 entry; R3 remains closed and unchanged.",
    f"R4 then closed through PR #273 at `{R5_ENTRY}`, which is the exact V3-R5/#272 entry; R3 remains closed and unchanged. R5 technical freeze validation subsequently passed release gate `{R5_RELEASE_RUN}` (`PASS=33 FAIL=0 SKIP=0`) and package run `{R5_PACKAGE_RUN}` (reproducible public/distribution bundles, checksums, asset exclusions and zero residue) without modifying certified product `{PRODUCT}`. V3-A1/#275 is prepared but remains blocked pending the future canonical R5 closeout SHA.",
)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 DONE. V3-R5/#272 ACTIVE from exact predecessor `{R5_ENTRY}`; certified foundation product `{PRODUCT}` is frozen as the R5 product baseline.**",
    f"**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4/#267 DONE. V3-R5/#272 TECHNICALLY VALIDATED from exact entry `{R5_ENTRY}` against frozen product `{PRODUCT}`; canonical closeout is pending. V3-A1/#275 is PREPARED / BLOCKED until the real R5 closeout SHA exists.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"| V3-R5 | ACTIVE | issue #272; entry `{R5_ENTRY}`; certified product `{PRODUCT}` | foundation-freeze/final-documentation contract active | freeze product baseline; reconcile release docs; validate bundles/checksums/assets/metadata and proportional release gates |\n| V3-A1/A2 | BLOCKED | — | scientific-article work | after certified foundation |",
    f"| V3-R5 | VALIDATED — CLOSEOUT PENDING | issue #272; entry `{R5_ENTRY}`; frozen product `{PRODUCT}` | release gate `{R5_RELEASE_RUN}` = `33/0/0`; package run `{R5_PACKAGE_RUN}` PASS; bundles/checksums/assets/residue PASS | merge validated closeout and record immutable A1 entry |\n| V3-A1 | PREPARED / BLOCKED | issue #275; entry SHA pending R5 closeout | source/normative article contract only; no runtime work started | activate only from real canonical R5 closeout SHA |\n| V3-A2 | BLOCKED | — | article runtime/test implementation | after A1 source contract closes |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## Immediate action\n\n.*?$",
    f"""## V3-R5 foundation-freeze validation

V3-R5/#272 is bound to exact entry `{R5_ENTRY}` and preserves R4-certified product `{PRODUCT}` unchanged. The R5 audit proved product-tree invariance and unchanged normative-base, normative-currency and migration-guide files. The full repository release gate completed `PASS=33 FAIL=0 SKIP=0` in run `{R5_RELEASE_RUN}` / job `{R5_RELEASE_JOB}`. That workflow later failed only because the first packaging sequence lacked its runtime preparation; no product check failed. Final package run `{R5_PACKAGE_RUN}` / job `{R5_PACKAGE_JOB}` then passed the complete freeze contract: source-only validation, licensed reference-asset preparation with cleanup, reproducible public bundles, reproducible complete distribution set, SHA-256 checksums, expected class/CTAN layouts, external `abntexto` semantics, institutional/proprietary asset exclusions and zero tracked/untracked residue.

No public runtime API, normative semantics, source/currency fact, locator/tolerance/applicability rule, proof-state default or rendered requirement changed. The foundation is therefore technically frozen, but R5 is intentionally not marked DONE before the closeout merge produces the immutable successor SHA required as V3-A1 entry.

## Immediate action

Merge the validated R5 closeout checkpoint after permanent `Static contract` and `Linux integration` gates pass. Capture the resulting immutable main SHA, then perform a minimal exact-entry activation: mark V3-R5/#272 DONE and activate V3-A1/#275 from that real SHA. A1 must reconfirm scientific-article authority/normative sources before any article runtime implementation. V3-A2 and actual CTAN submission remain blocked.""",
    flags=re.S,
)

print("R5 validation closeout reconciliation prepared successfully.")
