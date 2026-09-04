from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "7a7562d23e8bf6c92abb635718639d617a2ed6ff"
A1_ENTRY = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
A1_CONTRACT = "4d018a92697e8f39e3a53b034c451e55996c84fb"
FOUNDATION = "c79f3c73f1d51a30175e8259269504d029442a1c"
A1_ISSUE = 275
A2_ISSUE = 280
A1_PR = 279
A1_CLOSEOUT_PR = 281
A1_SOURCE_RUN = 33894907220
A1_STATIC = 33895016834
A1_LINUX = 33895016774
A1_LINUX_JOB = 101095498647
A1_CLOSEOUT_STATIC = 33901640982
A1_CLOSEOUT_LINUX = 33901640967
TODAY = "2026-09-04"


def read(path: str) -> str:
    return Path(path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    Path(path).write_text(text, encoding="utf-8")


def load_json(path: str) -> dict:
    return json.loads(read(path))


def save_json(path: str, data: dict) -> None:
    write(path, json.dumps(data, indent=2, ensure_ascii=False) + "\n")


def replace_once(path: str, old: str, new: str) -> None:
    text = read(path)
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one match in {path}, found {count}: {old!r}")
    write(path, text.replace(old, new))


def regex_once(path: str, pattern: str, replacement: str, flags: int = 0) -> None:
    text = read(path)
    new, count = re.subn(pattern, replacement, text, count=1, flags=flags)
    if count != 1:
        raise SystemExit(f"expected one regex match in {path}, found {count}: {pattern!r}")
    write(path, new)


def set_updated(path: str) -> None:
    text = read(path)
    if re.search(r"^Updated: \d{4}-\d{2}-\d{2}$", text, flags=re.M):
        write(path, re.sub(r"^Updated: \d{4}-\d{2}-\d{2}$", f"Updated: {TODAY}", text, count=1, flags=re.M))


roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
    raise SystemExit("unexpected phase/stage before A2 activation")
prep = roadmap.get("a2_preparation", {})
if prep.get("status") != "PREPARED_BLOCKED" or prep.get("entry_main_sha") is not None:
    raise SystemExit("A2 preparation is not in the expected blocked state")

roadmap.update({
    "updated_at": TODAY,
    "status": "ACTIVE",
    "phase": "V3-A2",
    "stage": "V3-A2",
    "stage_name": "implement and validate scientific-article profile",
})
roadmap["active_implementation_lot"] = {
    "phase": "V3-A2",
    "stage": "V3-A2",
    "issue": A2_ISSUE,
    "entry_main_sha": BASE,
    "source_contract_main_sha": A1_CONTRACT,
    "certified_foundation_product_sha": FOUNDATION,
    "name": "implement and validate scientific-article profile",
    "id": "V3-A2",
    "status": "ACTIVE",
    "runtime_implementation_started": False,
}

a1 = roadmap.setdefault("a1", {})
a1.update({
    "status": "DONE",
    "issue": A1_ISSUE,
    "entry_main_sha": A1_ENTRY,
    "source_contract_pr": A1_PR,
    "source_contract_merge_main_sha": A1_CONTRACT,
    "closeout_pr": A1_CLOSEOUT_PR,
    "closeout_merge_main_sha": BASE,
    "source_contract_run_id": A1_SOURCE_RUN,
    "static_contract_run_id": A1_STATIC,
    "linux_integration_run_id": A1_LINUX,
    "linux_integration_job_id": A1_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "closeout_static_contract_run_id": A1_CLOSEOUT_STATIC,
    "closeout_linux_integration_run_id": A1_CLOSEOUT_LINUX,
    "runtime_implementation_started": False,
    "a2_entry_main_sha": BASE,
})

candidate = roadmap.setdefault("a1_contract_candidate", {})
candidate.update({
    "status": "DONE",
    "merge_main_sha": A1_CONTRACT,
    "closeout_merge_main_sha": BASE,
    "a2_activation_pending": False,
    "a2_entry_main_sha": BASE,
})

roadmap["a1_closeout"] = {
    "status": "DONE",
    "issue": A1_ISSUE,
    "source_contract_pr": A1_PR,
    "source_contract_merge_main_sha": A1_CONTRACT,
    "closeout_pr": A1_CLOSEOUT_PR,
    "closeout_merge_main_sha": BASE,
    "source_validation_run_id": A1_SOURCE_RUN,
    "static_contract_run_id": A1_STATIC,
    "linux_integration_run_id": A1_LINUX,
    "linux_integration_job_id": A1_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "article_rule_count": 18,
    "manual_rules": 17,
    "conditional_manual_rules": 1,
    "runtime_files_added": 0,
    "proof_state_promoted": False,
    "certified_foundation_changed": False,
}
roadmap["a2_preparation"].update({
    "status": "ACTIVE",
    "entry_main_sha": BASE,
    "blocked_until_exact_a1_closeout": False,
    "runtime_implementation_started": False,
})
roadmap["a2"] = {
    "status": "ACTIVE",
    "issue": A2_ISSUE,
    "name": "implement and validate scientific-article profile",
    "entry_main_sha": BASE,
    "source_contract_main_sha": A1_CONTRACT,
    "certified_foundation_product_sha": FOUNDATION,
    "runtime_implementation_started": False,
    "article_rule_count": 18,
    "constraints": [
        "implement only the canonical scientific-article profile defined by the A1 source contract",
        "reuse cross-cutting citation reference section summary and tabular machinery",
        "preserve required optional recommended and conditional modalities",
        "promote proof only from current article-specific rule evidence",
        "do not add runtime compatibility aliases or retired Portuguese machine identifiers",
        "do not perform CTAN submission during A2",
    ],
}
roadmap["next_stage"] = "V3-A2"
roadmap["next_issue"] = A2_ISSUE
save_json("release/v3-roadmap.json", roadmap)

write("docs/HANDOFF-V3.0.0.md", f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1 through V3-R5: **DONE**.
- Certified non-article foundation: `{FOUNDATION}`.
- V3-A1/#275: **DONE**.
- A1 exact entry: `{A1_ENTRY}`.
- A1 source-contract PR #279: `{A1_CONTRACT}`.
- A1 closeout PR #281: `{BASE}`.
- A1 source-only validation `{A1_SOURCE_RUN}` PASS; Static `{A1_STATIC}` PASS; Linux `{A1_LINUX}` / job `{A1_LINUX_JOB}` = `PASS=31 FAIL=0 SKIP=0`.
- Scientific-article source contract: 18 rules = 17 manual + 1 conditional-manual; no runtime/proof promotion occurred in A1.
- V3-A2/#280: **ACTIVE** from exact predecessor `{BASE}`.
- A2 runtime implementation has not started yet.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Begin V3-A2/#280 from `{BASE}`. Implement only the canonical `scientific-article` profile bounded by `docs/ARTICLE-NORMATIVE-CONTRACT.md`: reuse cross-cutting infrastructure, preserve required/optional/recommended/conditional semantics, and add article-specific fail-closed evidence before any proof-state promotion.

## Hard boundaries

Preserve certified foundation `{FOUNDATION}` and the closed v3 API. Do not change article authority, modality, rule IDs, locators, applicability or proof state without new current evidence. No runtime aliases or retired Portuguese machine identifiers. No proprietary-font redistribution. CTAN submission remains a separate future release action.
""")

for path in [
    "docs/ROADMAP-V3.0.0.md",
    "docs/ARTICLE-NORMATIVE-CONTRACT.md",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
]:
    set_updated(path)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"**V3-R1 through V3-R5 DONE. V3-A1/#275 source contract VALIDATED and MERGED through PR #279 at `{A1_CONTRACT}`; canonical A1 closeout is pending. V3-A2/#280 is PREPARED/BLOCKED until the immutable A1 closeout predecessor is recorded.**",
    f"**V3-R1 through V3-R5 DONE. V3-A1/#275 DONE through source-contract PR #279 at `{A1_CONTRACT}` and closeout PR #281 at `{BASE}`. V3-A2/#280 is ACTIVE from exact predecessor `{BASE}`; runtime implementation has not started yet.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    f"| V3-A1 | VALIDATED — CLOSEOUT PENDING | issue #275; entry `{A1_ENTRY}`; PR #279 → `{A1_CONTRACT}` | 18 source-backed rules; source run `{A1_SOURCE_RUN}` PASS; Static `{A1_STATIC}` PASS; Linux `{A1_LINUX}` = `31/0/0`; runtime absent | merge canonical closeout and record exact A2 entry |\n| V3-A2 | PREPARED / BLOCKED | issue #280; A1 contract `{A1_CONTRACT}` | bounded `scientific-article` runtime/test scope defined | activate only after exact A1 closeout predecessor is known |",
    f"| V3-A1 | DONE | issue #275; entry `{A1_ENTRY}`; PR #279 → `{A1_CONTRACT}`; closeout PR #281 → `{BASE}` | current article authority reconfirmed; 18-rule conservative contract; source/Static/Linux gates green; no runtime in A1 | None |\n| V3-A2 | ACTIVE | issue #280; exact entry `{BASE}`; A1 contract `{A1_CONTRACT}` | bounded `scientific-article` implementation/test contract active | implement runtime/profile + article-specific evidence; keep CTAN blocked |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"V3-A2 implementation scope is now issue #280.*?## Immediate action\n\n.*?$",
    f"""V3-A2 implementation scope is issue #280 and the contract in `docs/ARTICLE-NORMATIVE-CONTRACT.md`. The exact immutable A2 entry is `{BASE}`. V3-A1/#275 is DONE; V3-A2/#280 is ACTIVE and runtime implementation has not started yet.

## V3-A2 entry

A2 begins from exact predecessor `{BASE}` and source-contract product `{A1_CONTRACT}` while preserving certified non-article foundation `{FOUNDATION}`. A2 may implement only the canonical `scientific-article` profile. Required predicates may become enforceable only with article-specific positive evidence and safe negative rejection where applicable. Optional/recommended predicates remain non-mandatory, and journal-specific instructions remain a conditional applicability boundary.

## Immediate action

Implement V3-A2/#280 in bounded lots: profile/runtime ownership first, then article-specific fixtures/evidence, then contribution/proof reconciliation and full PR gates. Reuse existing citation/reference/section/summary/table machinery and do not fork cross-cutting behavior. CTAN submission remains blocked until the post-A2 release decision.""",
    flags=re.S,
)

replace_once(
    "README.md",
    f"**V3-R1 through V3-R5 are DONE. V3-A1/#275 source/normative work is VALIDATED and MERGED through PR #279 at `{A1_CONTRACT}`; canonical closeout is pending. V3-A2/#280 is prepared but remains blocked until the exact A1 closeout predecessor is recorded.**",
    f"**V3-R1 through V3-R5 and V3-A1/#275 are DONE. A1 closed through PR #281 at `{BASE}` after source-contract PR #279 at `{A1_CONTRACT}`. V3-A2/#280 is ACTIVE from exact predecessor `{BASE}` and owns the canonical `scientific-article` runtime/test implementation.**",
)
replace_once(
    "README.md",
    f"The A1 contract merged through PR #279 at `{A1_CONTRACT}` and reconfirms the UFC article guide plus applicable current ABNT/cross-cutting sources. It registers 18 article rules without article runtime behavior: 17 manual and 1 conditional-manual, with inaccessible licensed ABNT clause locators explicitly partial rather than inferred. A2/#280 owns the bounded `scientific-article` implementation after exact-entry activation. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
    f"A1 closed through PR #281 at `{BASE}` after PR #279 established the current source-backed 18-rule article contract. V3-A2/#280 is now active and owns the bounded `scientific-article` implementation: required, optional, recommended and conditional semantics must remain distinct, and article proof may advance only from article-specific evidence. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
)

replace_once(
    "AGENTS.md",
    f"- V3-R3, V3-R4 and V3-R5 are DONE. V3-A1/#275 source/normative work is validated and merged through PR #279 at `{A1_CONTRACT}`: source run `{A1_SOURCE_RUN}` PASS, Static `{A1_STATIC}` PASS, Linux `{A1_LINUX}` / job `{A1_LINUX_JOB}` = `PASS=31 FAIL=0 SKIP=0`. The 18 article rules remain source-only (17 manual, 1 conditional-manual), with no article runtime or proof promotion. V3-A2/#280 is PREPARED/BLOCKED until the A1 closeout checkpoint is merged and its immutable predecessor recorded.",
    f"- V3-R3, V3-R4, V3-R5 and V3-A1 are DONE. A1/#275 source contract merged through PR #279 at `{A1_CONTRACT}` and closed through PR #281 at exact A2 predecessor `{BASE}`. V3-A2/#280 is ACTIVE from that SHA; runtime implementation has not started yet. A2 must implement only canonical `scientific-article`, reuse cross-cutting infrastructure, preserve modality, and require article-specific evidence before proof promotion.",
)
replace_once(
    "AGENTS.md",
    f"V3-R5/#272 is DONE through PR #276 at `{A1_ENTRY}`; V3-A1/#275 source authority/contract work is validated through PR #279 at `{A1_CONTRACT}` and awaits canonical closeout; V3-A2/#280 remains blocked until exact-entry activation.",
    f"V3-R5/#272 is DONE through PR #276 at `{A1_ENTRY}`; V3-A1/#275 is DONE through PR #281 at `{BASE}`; V3-A2/#280 is ACTIVE from that exact entry.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "`articles.def` is introduced only in V3-A2 after the V3-A1 source contract closes canonically. It is not pre-staged as a dormant foundation module.",
    "`articles.def` is V3-A2-owned and may now be introduced from the canonical A2 entry. It must directly own scientific-article behavior rather than act as a compatibility/forwarding layer.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "Scientific-article normative material was reintroduced in V3-A1 from current sources; runtime/profile material remains V3-A2-owned and may start only after exact-entry activation.",
    "Scientific-article normative material was reintroduced in V3-A1 from current sources. V3-A2 is now active and owns only the bounded runtime/profile and article-specific evidence needed to realize that contract.",
)

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    f"V3-A1/#275 source/normative work is validated through PR #279 at `{A1_CONTRACT}`; V3-A2/#280 will own runtime implementation after exact-entry activation. Scientific-article engineering identifiers remain canonical English while official/academic Portuguese stays protected.",
    f"V3-A1/#275 is DONE through PR #281 at `{BASE}` and V3-A2/#280 is ACTIVE. The canonical profile identifier is `scientific-article`; `article.*` remains the project-owned rule namespace. Runtime implementation must keep these engineering identifiers in English while official/academic Portuguese stays protected.",
)

replace_once(
    "docs/CTAN-RELEASE.md",
    f"R5 closed through PR #276 at `{A1_ENTRY}`. V3-A1/#275 source/normative work is validated and merged through PR #279 at `{A1_CONTRACT}`, while V3-A2/#280 remains blocked pending exact-entry activation. Actual CTAN upload remains a separate explicit release action and has not occurred; A1/A2 scientific-article work is not CTAN submission.",
    f"R5 closed through PR #276 at `{A1_ENTRY}`. V3-A1/#275 closed through PR #281 at `{BASE}` after source-contract PR #279 at `{A1_CONTRACT}`. V3-A2/#280 is ACTIVE from that exact entry. Actual CTAN upload remains a separate explicit release action and has not occurred; A2 scientific-article implementation is not CTAN submission.",
)

article = read("docs/ARTICLE-NORMATIVE-CONTRACT.md")
if "## V3-A2 canonical entry" in article:
    raise SystemExit("A2 canonical entry already recorded")
article += f"""

## V3-A2 canonical entry

V3-A1/#275 closed through PR #281 at exact predecessor `{BASE}`. V3-A2/#280 is ACTIVE from that SHA and owns only the bounded `scientific-article` runtime/test implementation described above. The source-contract product remains `{A1_CONTRACT}` and the certified non-article foundation remains `{FOUNDATION}`. No article runtime implementation had started at the activation checkpoint.
"""
write("docs/ARTICLE-NORMATIVE-CONTRACT.md", article)
