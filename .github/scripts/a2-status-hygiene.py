from pathlib import Path

BASE = "1b6d4e2a5857541047955014b73ad76739e78eb4"
A1_ENTRY = "908ee2eb2ec04c030d74a9a4b146fba38fb745a9"
A1_CONTRACT = "4d018a92697e8f39e3a53b034c451e55996c84fb"
A1_CLOSEOUT = "7a7562d23e8bf6c92abb635718639d617a2ed6ff"


def replace_once(path: str, old: str, new: str) -> None:
    p = Path(path)
    text = p.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one match in {path}, found {count}: {old!r}")
    p.write_text(text.replace(old, new), encoding="utf-8")


replace_once(
    "README.md",
    "R4 closeout PR #273 merged at `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; V3-R4/#267 is DONE and V3-R5/#272 is ACTIVE from that exact predecessor.",
    "R4 closeout PR #273 merged at `0b0f5d989163dc6b1429feeb2d8a7c66988647bb`; V3-R4/#267 and V3-R5/#272 are DONE.",
)
replace_once(
    "README.md",
    f"R5 is closed at `{A1_ENTRY}`. V3-A1/#275 is active from that exact entry; no article runtime work has started because A1 owns source/normative-contract reconstruction only.",
    f"R5 is closed at `{A1_ENTRY}`. V3-A1/#275 is DONE through closeout `{A1_CLOSEOUT}`; V3-A2/#280 is ACTIVE from that exact predecessor and owns the scientific-article runtime/test implementation.",
)
replace_once(
    "README.md",
    f"V3-R4 and V3-R5 are DONE; V3-A1/#275 is ACTIVE from `{A1_ENTRY}`.",
    f"V3-R4, V3-R5 and V3-A1/#275 are DONE; V3-A2/#280 is ACTIVE from `{A1_CLOSEOUT}`.",
)

replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "Active foundation-freeze issue: #272 (V3-R5). Machine authority: `release/v3-roadmap.json`.",
    "Active implementation issue: #280 (V3-A2). Machine authority: `release/v3-roadmap.json`.",
)

replace_once(
    "docs/ARCHITECTURE.md",
    f"V3-A1/#275 is ACTIVE from that exact entry and is restricted to source/normative-contract reconstruction; article runtime implementation belongs to V3-A2 after A1 closes.",
    f"V3-A1/#275 is DONE through source-contract `{A1_CONTRACT}` and closeout `{A1_CLOSEOUT}`; V3-A2/#280 is ACTIVE from that exact predecessor and owns the bounded article runtime/evidence implementation.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "Only canonical R5 closeout remains before V3-A1/#275 may begin.",
    f"R5 closed at `{A1_ENTRY}`; A1 closed at `{A1_CLOSEOUT}`; V3-A2/#280 is now active.",
)
replace_once(
    "docs/ARCHITECTURE.md",
    "V3-A1/#275 is source/normative work and remains blocked until the R5 closeout merge supplies its immutable entry SHA.",
    f"The R5 closeout supplied A1 entry `{A1_ENTRY}`; A1 completed and closeout `{A1_CLOSEOUT}` is the exact A2 entry predecessor.",
)

replace_once(
    "docs/ENGINEERING-LANGUAGE.md",
    "The A1 machine namespace is `article.*` and the future profile name is `scientific-article`.",
    "The article rule namespace is `article.*` and the canonical profile name is `scientific-article`.",
)

# Fail closed if known stale current-state formulations remain.
checks = {
    "README.md": [
        "V3-R5/#272 is ACTIVE",
        "V3-A1/#275 is active from that exact entry",
        f"V3-A1/#275 is ACTIVE from `{A1_ENTRY}`",
    ],
    "docs/ROADMAP-V3.0.0.md": ["Active foundation-freeze issue: #272"],
    "docs/ARCHITECTURE.md": [
        "V3-A1/#275 is ACTIVE from that exact entry",
        "Only canonical R5 closeout remains before V3-A1/#275 may begin",
        "V3-A1/#275 is source/normative work and remains blocked",
    ],
    "docs/ENGINEERING-LANGUAGE.md": ["future profile name is `scientific-article`"],
}
for path, needles in checks.items():
    text = Path(path).read_text(encoding="utf-8")
    for needle in needles:
        if needle in text:
            raise SystemExit(f"stale status wording remains in {path}: {needle}")
