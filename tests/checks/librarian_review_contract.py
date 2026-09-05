#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REVIEW = ROOT / "docs" / "UFC-LIBRARIAN-REVIEW.md"
AUDIT = ROOT / "docs" / "V3-REGRESSION-AUDIT.md"

ROW_RE = re.compile(
    r"^\|\s*(?P<number>\d+)\s*\|(?P<requirement>.*?)\|(?P<status>.*?)\|(?P<surfaces>.*?)\|\s*$"
)
ALLOWED_STATUS_PREFIXES = ("PASS", "PARTIAL", "FAIL", "NORMATIVE-REVIEW")


def fail(message: str) -> int:
    print(f"Librarian review contract failed: {message}")
    return 1


def main() -> int:
    if not REVIEW.is_file():
        return fail("missing docs/UFC-LIBRARIAN-REVIEW.md")
    if not AUDIT.is_file():
        return fail("missing docs/V3-REGRESSION-AUDIT.md")

    review_text = REVIEW.read_text(encoding="utf-8")
    audit_text = AUDIT.read_text(encoding="utf-8")

    rows: list[tuple[int, str, str, str]] = []
    for line in review_text.splitlines():
        match = ROW_RE.match(line)
        if match is None:
            continue
        number = int(match.group("number"))
        rows.append(
            (
                number,
                match.group("requirement").strip(),
                match.group("status").strip(),
                match.group("surfaces").strip(),
            )
        )

    expected_numbers = list(range(1, 35))
    numbers = [row[0] for row in rows]
    if numbers != expected_numbers:
        return fail(f"expected review rows 1..34 exactly once, got {numbers}")

    for number, requirement, status, surfaces in rows:
        if not requirement:
            return fail(f"review item {number} has no requirement")
        if not surfaces:
            return fail(f"review item {number} has no owning surface")
        if not status.startswith(ALLOWED_STATUS_PREFIXES):
            return fail(f"review item {number} has unsupported status: {status}")

    if "34-item review contract" not in audit_text:
        return fail("regression audit does not bind itself to the 34-item review contract")
    if "Phase 1" not in audit_text or "Regression Audit" not in audit_text:
        return fail("regression audit does not expose the readable active phase model")

    normative_review_count = sum(
        status.startswith("NORMATIVE-REVIEW") for _, _, status, _ in rows
    )
    fail_count = sum(status.startswith("FAIL") for _, _, status, _ in rows)
    partial_count = sum(status.startswith("PARTIAL") for _, _, status, _ in rows)
    pass_count = sum(status.startswith("PASS") for _, _, status, _ in rows)

    print(
        "LIBRARIAN-REVIEW-EVIDENCE status=PASS "
        f"items={len(rows)} pass={pass_count} partial={partial_count} "
        f"fail={fail_count} normative_review={normative_review_count}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
