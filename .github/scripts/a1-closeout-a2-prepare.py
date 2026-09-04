from __future__ import annotations

import json
import re
from pathlib import Path

BASE = "4d018a92697e8f39e3a53b034c451e55996c84fb"
A1_ENTRY = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
FOUNDATION = "c79f3c73f1d51a30175e8259269504d029442a1c"
A1_ISSUE = 275
A2_ISSUE = 280
A1_PR = 279
A1_HEAD = "83aed74af6ba966a0db63c093cafdfc2fd74a619"
A1_SOURCE_RUN = 33894907220
A1_STATIC = 33895016834
A1_LINUX = 33895016774
A1_LINUX_JOB = 101095498647
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
        text = re.sub(r"^Updated: \d{4}-\d{2}-\d{2}$", f"Updated: {TODAY}", text, count=1, flags=re.M)
        write(path, text)


# Machine state: A1 is validated/merged, but A2 must remain blocked until this
# checkpoint itself is merged and its immutable SHA is known.
roadmap = load_json("release/v3-roadmap.json")
if roadmap.get("phase") != "V3-A1" or roadmap.get("stage") != "V3-A1":
    raise SystemExit("unexpected canonical phase/stage")

roadmap["updated_at"] = TODAY
roadmap["phase"] = "V3-A1"
roadmap["stage"] = "V3-A1"
roadmap["stage_name"] = "scientific-article normative contract closeout"
roadmap["active_implementation_lot"] = {
    "phase": "V3-A1",
    "stage": "V3-A1",
    "issue": A1_ISSUE,
    "entry_main_sha": A1_ENTRY,
    "certified_foundation_product_sha": FOUNDATION,
    "name": "scientific-article normative contract closeout",
    "id": "V3-A1",
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "source_contract_merge_main_sha": BASE,
    "runtime_implementation_allowed": False,
}

a1 = roadmap.setdefault("a1", {})
a1.update({
    "status": "VALIDATED_PENDING_CANONICAL_CLOSEOUT",
    "issue": A1_ISSUE,
    "entry_main_sha": A1_ENTRY,
    "source_reconfirmation_status": "DONE",
    "source_reconfirmation_reviewed_at": TODAY,
    "normative_contract_status": "VALIDATED",
    "source_contract_pr": A1_PR,
    "source_contract_head_sha": A1_HEAD,
    "source_contract_merge_main_sha": BASE,
    "source_contract_run_id": A1_SOURCE_RUN,
    "static_contract_run_id": A1_STATIC,
    "linux_integration_run_id": A1_LINUX,
    "linux_integration_job_id": A1_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "article_rule_count": 18,
    "article_manual_rules": 17,
    "article_conditional_manual_rules": 1,
    "runtime_implementation_started": False,
})

candidate = roadmap.setdefault("a1_contract_candidate", {})
candidate.update({
    "status": "VALIDATED_MERGED_PENDING_CLOSEOUT",
    "issue": A1_ISSUE,
    "pr": A1_PR,
    "implementation_head_sha": A1_HEAD,
    "merge_main_sha": BASE,
    "source_validation_run_id": A1_SOURCE_RUN,
    "static_contract_run_id": A1_STATIC,
    "linux_integration_run_id": A1_LINUX,
    "linux_integration_job_id": A1_LINUX_JOB,
    "linux_integration_result": "PASS=31 FAIL=0 SKIP=0",
    "article_rule_count": 18,
    "manual_rules": 17,
    "conditional_manual_rules": 1,
    "runtime_files_added": 0,
    "public_runtime_api_changed": False,
    "certified_foundation_changed": False,
    "proof_state_promoted": False,
    "a2_activation_pending": True,
})

roadmap["a2_preparation"] = {
    "status": "PREPARED_BLOCKED",
    "issue": A2_ISSUE,
    "name": "implement and validate scientific-article profile",
    "source_contract_main_sha": BASE,
    "entry_main_sha": None,
    "blocked_until_exact_a1_closeout": True,
    "runtime_implementation_started": False,
}
roadmap["next_stage"] = "V3-A1"
roadmap["next_issue"] = A1_ISSUE
save_json("release/v3-roadmap.json", roadmap)

# Handoff is intentionally concise and authoritative.
write("docs/HANDOFF-V3.0.0.md", f"""# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: {TODAY}

## Checkpoint

- Repository: `tiagosombrra/abntexto-ufc`.
- V3-R1 through V3-R5: **DONE**.
- Certified non-article foundation: `{FOUNDATION}`.
- V3-A1/#275 exact entry: `{A1_ENTRY}`.
- V3-A1 source contract: **VALIDATED AND MERGED; canonical closeout pending**.
- A1 PR #279 merged at `{BASE}`.
- A1 source-only validation: `{A1_SOURCE_RUN}` — PASS.
- A1 Static contract: `{A1_STATIC}` — PASS.
- A1 Linux integration: `{A1_LINUX}` / job `{A1_LINUX_JOB}` — `PASS=31 FAIL=0 SKIP=0`.
- Article contract: 18 rules = 17 manual + 1 conditional-manual; no article runtime/proof promotion in A1.
- Full contract observed by the PR gate: 199 rules; 188 normative; all normative rules locator-classified; zero UNASSESSED/unclassified evidence IDs.
- V3-A2/#280: **PREPARED / BLOCKED** until this A1 closeout checkpoint is merged and its immutable SHA is recorded.

Git facts, `release/v3-roadmap.json`, this handoff, `docs/ROADMAP-V3.0.0.md`, and `AGENTS.md` must agree. Disagreement fails closed.

## Immediate action

Merge the A1 closeout checkpoint, capture its immutable main SHA, then perform one minimal exact-entry activation that marks V3-A1/#275 DONE and activates V3-A2/#280 from that predecessor. Do not start article runtime before that activation is canonical.

## Hard boundaries

Preserve certified foundation `{FOUNDATION}` and the closed v3 API. Do not change the reconfirmed article authority, modality, rule IDs, locators, applicability or proof state without new current evidence. Do not restore historical machine identifiers or runtime aliases. Do not redistribute proprietary Microsoft fonts or perform CTAN submission. A2 must implement only the bounded `scientific-article` profile defined by `docs/ARTICLE-NORMATIVE-CONTRACT.md` and issue #280.
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
    "**V3-R1 DONE. V3-R2 DONE. V3-R3 DONE. V3-R4 DONE. V3-R5/#272 DONE through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` with certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged. V3-A1/#275 is ACTIVE from exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; article runtime implementation is not allowed in A1.**",
    f"**V3-R1 through V3-R5 DONE. V3-A1/#275 source contract VALIDATED and MERGED through PR #279 at `{BASE}`; canonical A1 closeout is pending. V3-A2/#280 is PREPARED/BLOCKED until the immutable A1 closeout predecessor is recorded.**",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "| V3-A1 | ACTIVE — CONTRACT CANDIDATE | issue #275; exact entry `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; implementation base `e40a56deeca8c22797398b0c95835964aefd2b15`; certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` | current article sources reconfirmed; 18 source-backed rules; 17 manual + 1 conditional-manual; runtime still absent | validate/merge A1 source contract, then record exact A2 entry |\n| V3-A2 | BLOCKED | — | article runtime/test implementation | after A1 source contract closes |",
    f"| V3-A1 | VALIDATED — CLOSEOUT PENDING | issue #275; entry `{A1_ENTRY}`; PR #279 → `{BASE}` | 18 source-backed rules; source run `{A1_SOURCE_RUN}` PASS; Static `{A1_STATIC}` PASS; Linux `{A1_LINUX}` = `31/0/0`; runtime absent | merge canonical closeout and record exact A2 entry |\n| V3-A2 | PREPARED / BLOCKED | issue #280; A1 contract `{BASE}` | bounded `scientific-article` runtime/test scope defined | activate only after exact A1 closeout predecessor is known |",
)
regex_once(
    "docs/ROADMAP-V3.0.0.md",
    r"## V3-A1 source-contract candidate\n\n.*?\n\n## Immediate action\n\n.*?$",
    f"""## V3-A1 validated source contract

A1 reconfirmed the corrected UFC article guide, NBR 6022:2018 and current cross-cutting NBR 10520:2023, NBR 6023:2025, NBR 6024:2012, NBR 6028:2021 and IBGE tabular basis. PR #279 merged the 18-rule conservative contract at `{BASE}` without article runtime/profile code. Seventeen article rules remain manual and one conditional-manual; unavailable licensed ABNT clause locators remain `PARTIAL_WITH_REASON` rather than guessed.

Source-only run `{A1_SOURCE_RUN}` passed. PR Static `{A1_STATIC}` passed. PR Linux `{A1_LINUX}` / job `{A1_LINUX_JOB}` passed `PASS=31 FAIL=0 SKIP=0`. The full gate observed 199 rules, 188 normative rules with complete locator classification, zero UNASSESSED/unclassified evidence IDs, and final current-run contribution `113/113` bounded-positive, 37 enforced-automatic, 14 support-only, 11 conditional-review, 23 manual-review and 1 not-applicable. None of that promotes an article rule before article-specific A2 evidence exists.

V3-A2 implementation scope is now issue #280 and the contract in `docs/ARTICLE-NORMATIVE-CONTRACT.md`. A2 remains blocked until this closeout is canonical and its exact immutable SHA is recorded.

## Immediate action

Merge this A1 closeout checkpoint, capture its immutable main SHA, then perform the minimal exact-entry activation: V3-A1/#275 DONE and V3-A2/#280 ACTIVE from that predecessor. Do not start article runtime before the activation checkpoint is canonical. CTAN submission remains a future explicit release action.""",
    flags=re.S,
)

replace_once(
    "README.md",
    "**V3-R1 through V3-R5 are DONE. R5/#272 closed through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` with certified foundation `c79f3c73f1d51a30175e8259269504d029442a1c` unchanged. V3-A1/#275 is ACTIVE from `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` and is limited to reconfirming the scientific-article normative/source contract before any runtime implementation.**",
    f"**V3-R1 through V3-R5 are DONE. V3-A1/#275 source/normative work is VALIDATED and MERGED through PR #279 at `{BASE}`; canonical closeout is pending. V3-A2/#280 is prepared but remains blocked until the exact A1 closeout predecessor is recorded.**",
)
replace_once(
    "README.md",
    "The current A1 candidate reconfirms the UFC article guide and applicable current ABNT/cross-cutting sources, then registers 18 article rules without implementing an article runtime profile. Seventeen rules are manual and one is conditional-manual; inaccessible licensed ABNT clause locators remain explicitly partial rather than inferred. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
    f"The A1 contract merged through PR #279 at `{BASE}` and reconfirms the UFC article guide plus applicable current ABNT/cross-cutting sources. It registers 18 article rules without article runtime behavior: 17 manual and 1 conditional-manual, with inaccessible licensed ABNT clause locators explicitly partial rather than inferred. A2/#280 owns the bounded `scientific-article` implementation after exact-entry activation. See `docs/ARTICLE-NORMATIVE-CONTRACT.md`.",
)

replace_once(
    "AGENTS.md",
    "- V3-R3, V3-R4 and V3-R5 are DONE. R5/#272 preserved certified product `c79f3c73f1d51a30175e8259269504d029442a1c`, passed release gate `33866258865` = `PASS=33 FAIL=0 SKIP=0`, package audit `33869888601`, and PR #276 gates, then closed at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`. V3-A1/#275 is ACTIVE from that exact SHA. Its current candidate reconfirms the article source set and registers 18 rules as source-only manual/conditional evidence. No article runtime/profile implementation or proof promotion is allowed before A1 closes canonically.",
    f"- V3-R3, V3-R4 and V3-R5 are DONE. V3-A1/#275 source/normative work is validated and merged through PR #279 at `{BASE}`: source run `{A1_SOURCE_RUN}` PASS, Static `{A1_STATIC}` PASS, Linux `{A1_LINUX}` / job `{A1_LINUX_JOB}` = `PASS=31 FAIL=0 SKIP=0`. The 18 article rules remain source-only (17 manual, 1 conditional-manual), with no article runtime or proof promotion. V3-A2/#280 is PREPARED/BLOCKED until the A1 closeout checkpoint is merged and its immutable predecessor recorded.",
)
replace_once(
    "AGENTS.md",
    "V3-R5/#272 is DONE through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9`; V3-A1/#275 is ACTIVE from that exact entry and must reconfirm article authority before runtime implementation.",
    f"V3-R5/#272 is DONE through PR #276 at `{A1_ENTRY}`; V3-A1/#275 source authority/contract work is validated through PR #279 at `{BASE}` and awaits canonical closeout; V3-A2/#280 remains blocked until exact-entry activation.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    "`articles.def` is introduced only when V3-A1 becomes active. It is not pre-staged as a dormant foundation module.",
    "`articles.def` is introduced only in V3-A2 after the V3-A1 source contract closes canonically. It is not pre-staged as a dormant foundation module.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "Scientific-article normative/runtime material is reintroduced only in V3-A1 after current sources are reconfirmed.",
    "Scientific-article normative material was reintroduced in V3-A1 from current sources; runtime/profile material remains V3-A2-owned and may start only after exact-entry activation.",
)

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "V3-A1/#275 is ACTIVE from that exact entry; its new scientific-article engineering identifiers must remain canonical English while official/academic Portuguese stays protected.",
    f"V3-A1/#275 source/normative work is validated through PR #279 at `{BASE}`; V3-A2/#280 will own runtime implementation after exact-entry activation. Scientific-article engineering identifiers remain canonical English while official/academic Portuguese stays protected.",
)

# Keep CTAN blocked and make the current article checkpoint explicit.
replace_once(
    "docs/CTAN-RELEASE.md",
    "R5 closed through PR #276 at `908ee2eb2ec04c030d74a9a4b146fba38fb745a9` and V3-A1/#275 is now ACTIVE from that exact entry. Actual CTAN upload remains a separate explicit release action and has not occurred; A1/A2 scientific-article work is not CTAN submission.",
    f"R5 closed through PR #276 at `{A1_ENTRY}`. V3-A1/#275 source/normative work is validated and merged through PR #279 at `{BASE}`, while V3-A2/#280 remains blocked pending exact-entry activation. Actual CTAN upload remains a separate explicit release action and has not occurred; A1/A2 scientific-article work is not CTAN submission.",
)

# Record validation and the prepared A2 issue in the article contract without
# pretending A2 is active yet.
article = read("docs/ARTICLE-NORMATIVE-CONTRACT.md")
if "## V3-A1 validation closeout" in article:
    raise SystemExit("article closeout section already exists")
article += f"""

## V3-A1 validation closeout

PR #279 merged this source-backed contract at `{BASE}` after source-only run `{A1_SOURCE_RUN}`, Static `{A1_STATIC}`, and Linux integration `{A1_LINUX}` / job `{A1_LINUX_JOB}` all passed; Linux closed `PASS=31 FAIL=0 SKIP=0`. No article runtime/profile code was introduced and no article proof state was promoted. V3-A2 implementation is bounded by issue #280, but remains blocked until the A1 closeout checkpoint is merged and its immutable entry predecessor is recorded.
"""
write("docs/ARTICLE-NORMATIVE-CONTRACT.md", article)
