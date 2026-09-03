#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

PAIRS = (
    ("tests/integration/frontmatter-evidence.sh", "tests/checks/frontmatter_evidence.py"),
    ("tests/integration/frontmatter-alignment-evidence.sh", "tests/checks/normative_frontmatter_alignment.py"),
    ("tests/integration/frontmatter-acknowledgments-evidence.sh", "tests/checks/normative_frontmatter_acknowledgments.py"),
    ("tests/integration/frontmatter-summary-evidence.sh", "tests/checks/normative_frontmatter_summary.py"),
    ("tests/integration/frontmatter-cover-evidence.sh", "tests/checks/normative_frontmatter_cover.py"),
    ("tests/integration/frontmatter-title-page-evidence.sh", "tests/checks/normative_frontmatter_title_page.py"),
    ("tests/integration/frontmatter-approval-evidence.sh", "tests/checks/normative_frontmatter_approval.py"),
    ("tests/integration/frontmatter-errata-evidence.sh", "tests/checks/normative_frontmatter_errata.py"),
    ("tests/integration/frontmatter-lists-evidence.sh", "tests/checks/normative_frontmatter_lists.py"),
    ("tests/integration/frontmatter-toc-evidence.sh", "tests/checks/normative_frontmatter_toc.py"),
    ("tests/integration/frontmatter-pagination-evidence.sh", "tests/checks/normative_frontmatter_pagination.py"),
)


def patch_runner(runner_rel: str, checker_rel: str) -> None:
    # Require the checker to own enforcement before changing its integration runner.
    checker = ROOT / checker_rel
    checker_text = checker.read_text(encoding="utf-8")
    if '"--enforce"' not in checker_text or "args.enforce" not in checker_text:
        raise SystemExit(f"checker does not expose enforcement semantics: {checker_rel}")

    runner = ROOT / runner_rel
    text = runner.read_text(encoding="utf-8")
    if "  --enforce\n" in text:
        raise SystemExit(f"runner is already enforced: {runner_rel}")
    needle = '  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"\n'
    if text.count(needle) != 1:
        raise SystemExit(f"expected one commit-sha tail in {runner_rel}, found {text.count(needle)}")
    runner.write_text(
        text.replace(
            needle,
            '  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \\\n  --enforce\n',
        ),
        encoding="utf-8",
    )


for runner_rel, checker_rel in PAIRS:
    patch_runner(runner_rel, checker_rel)

frontmatter = ROOT / "tests/integration/frontmatter.sh"
text = frontmatter.read_text(encoding="utf-8")
anchor = "sh tests/integration/frontmatter-alignment-evidence.sh\n"
addition = anchor + "sh tests/integration/frontmatter-enforcement-negative.sh\n"
if text.count(anchor) != 1:
    raise SystemExit("frontmatter negative-test insertion point changed")
if "frontmatter-enforcement-negative.sh" in text:
    raise SystemExit("frontmatter negative test is already registered")
frontmatter.write_text(text.replace(anchor, addition), encoding="utf-8")

print(f"R3-B1 enforcement enabled for {len(PAIRS)} front-matter evidence runners.")
