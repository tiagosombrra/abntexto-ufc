#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

ALREADY_ENFORCED = (
    "tests/integration/frontmatter-evidence.sh",
    "tests/integration/frontmatter-alignment-evidence.sh",
    "tests/integration/frontmatter-acknowledgments-evidence.sh",
    "tests/integration/frontmatter-summary-evidence.sh",
    "tests/integration/frontmatter-cover-evidence.sh",
    "tests/integration/frontmatter-title-page-evidence.sh",
    "tests/integration/frontmatter-approval-evidence.sh",
    "tests/integration/frontmatter-errata-evidence.sh",
)


def replace_exact(path: Path, old: str, new: str) -> None:
    # Fail closed when the audited source shape has changed.
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one repair target in {path}, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


for relative in ALREADY_ENFORCED:
    text = (ROOT / relative).read_text(encoding="utf-8")
    if text.count("  --enforce\n") != 1:
        raise SystemExit(f"expected exactly one enforced invocation in {relative}")

pagination = (ROOT / "tests/checks/normative_frontmatter_pagination.py").read_text(encoding="utf-8")
if 'if result != "PASS":\n        raise SystemExit(1)' not in pagination:
    raise SystemExit("pagination checker is no longer intrinsically fail-closed")

for checker_rel, label in (
    ("tests/checks/normative_frontmatter_lists.py", "optional-list"),
    ("tests/checks/normative_frontmatter_toc.py", "TOC"),
):
    checker = ROOT / checker_rel
    replace_exact(
        checker,
        '    parser.add_argument("--commit-sha")\n',
        '    parser.add_argument("--commit-sha")\n    parser.add_argument("--enforce", action="store_true")\n',
    )
    replace_exact(
        checker,
        '        "source_commit_sha": args.commit_sha,\n',
        '        "source_commit_sha": args.commit_sha,\n        "mode": "enforce" if args.enforce else "audit",\n',
    )
    replace_exact(
        checker,
        '\n\nif __name__ == "__main__":\n    main()\n',
        f'\n\n    if args.enforce and result != "PASS":\n        fail("enforcement requested with unresolved {label} findings")\n\n\nif __name__ == "__main__":\n    main()\n',
    )

for runner_rel in (
    "tests/integration/frontmatter-lists-evidence.sh",
    "tests/integration/frontmatter-toc-evidence.sh",
):
    runner = ROOT / runner_rel
    replace_exact(
        runner,
        '  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}"\n',
        '  --commit-sha "${SOURCE_COMMIT_SHA:-${GITHUB_SHA:-}}" \\\n  --enforce\n',
    )

frontmatter = ROOT / "tests/integration/frontmatter.sh"
replace_exact(
    frontmatter,
    "sh tests/integration/frontmatter-alignment-evidence.sh\n",
    "sh tests/integration/frontmatter-alignment-evidence.sh\n"
    "sh tests/integration/frontmatter-enforcement-negative.sh\n",
)

print(
    "R3-B1 enforcement completed: 10 explicit enforced evidence runners, "
    "pagination intrinsic fail-closed, negative rejection registered."
)
