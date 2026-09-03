#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_exact(path: Path, old: str, new: str) -> None:
    # Fail closed if the source shape no longer matches the audited baseline.
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected one repair target in {path}, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def load_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def write_json(path: Path, payload: dict) -> None:
    path.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")


# The explicit-line fixture owns position, indent, font, spacing and quotation marks.
# Paragraph justification is proven independently by normative_frontmatter_alignment.py.
scenarios_path = ROOT / "standards/frontmatter-scenarios.json"
scenarios = load_json(scenarios_path)
for scenario in scenarios["scenarios"]:
    scenario["rules"] = [rule for rule in scenario["rules"] if not rule.endswith(".alignment")]
write_json(scenarios_path, scenarios)

checker = ROOT / "tests/checks/frontmatter_evidence.py"
text = checker.read_text(encoding="utf-8")
for assignment in (
    '        alignment_id = "dedication.alignment"\n',
    '        alignment_id = "epigraph.short.alignment"\n',
    '        alignment_id = "epigraph.long.alignment"\n',
):
    if text.count(assignment) != 1:
        raise SystemExit(f"alignment assignment mismatch in {checker}: {assignment.strip()}")
    text = text.replace(assignment, "")
alignment_block = '''    alignment_rule = rules[alignment_id]\n    evidence.append(\n        record(\n            alignment_id,\n            "UNASSESSED",\n            alignment_rule["values"]["alignment"],\n            None,\n            "isolated explicit-line fixture",\n            reason="Explicit line breaks are suitable for spacing evidence but do not prove paragraph justification.",\n        )\n    )\n\n'''
if text.count(alignment_block) != 1:
    raise SystemExit(f"alignment support-only block mismatch in {checker}")
checker.write_text(text.replace(alignment_block, ""), encoding="utf-8")

# Keep each explicit dedication marker on one physical line so marker gaps are line gaps.
dedication = ROOT / "tests/fixtures/frontmatter/dedication-validation-fixture.tex"
dedication_text = dedication.read_text(encoding="utf-8")
if dedication_text.count(" control line.") != 3:
    raise SystemExit("dedication fixture shape changed")
dedication.write_text(dedication_text.replace(" control line.", ""), encoding="utf-8")

# Short, extraction-stable tokens prevent pdftotext line wrapping from hiding semantic fields.
title_scenario_path = ROOT / "standards/frontmatter-title-page-scenario.json"
title_scenario = load_json(title_scenario_path)
title_markers = title_scenario["academic"]["markers"]
title_markers["nature"] = "TPNATURE"
title_markers["advisor"] = "TPADVISOR"
title_markers["coadvisor"] = "TPCOADVISOR"
write_json(title_scenario_path, title_scenario)

title_fixture = ROOT / "tests/documents/frontmatter-title-page-academic-test.tex"
title_text = title_fixture.read_text(encoding="utf-8")
for old, new in (
    ("UFCFRONTMATTERTPNATUREPROGRAM", "TPNATURE"),
    ("UFCFRONTMATTERTPADVISOR", "TPADVISOR"),
    ("UFCFRONTMATTERTPCOADVISOR", "TPCOADVISOR"),
):
    if title_text.count(old) != 1:
        raise SystemExit(f"title-page fixture marker mismatch: {old}")
    title_text = title_text.replace(old, new)
title_fixture.write_text(title_text, encoding="utf-8")

approval_scenario_path = ROOT / "standards/frontmatter-approval-scenario.json"
approval_scenario = load_json(approval_scenario_path)
approval_scenario["markers"]["nature"] = "APNATURE"
write_json(approval_scenario_path, approval_scenario)

approval_fixture = ROOT / "tests/documents/frontmatter-approval-test.tex"
approval_text = approval_fixture.read_text(encoding="utf-8")
if approval_text.count("UFCFRONTMATTERAPNATURE") != 2:
    raise SystemExit("approval nature marker shape changed")
approval_fixture.write_text(
    approval_text.replace("UFCFRONTMATTERAPNATURE", "APNATURE"),
    encoding="utf-8",
)

# pdftotext can emit a right-edge quotation fragment as a separate line node on the
# same physical line. Coalesce only the geometric signature of that split fragment.
alignment = ROOT / "tests/checks/normative_frontmatter_alignment.py"
insert_after = '''def line_bounds(line: ET.Element) -> tuple[float, float]:\n    try:\n        return float(line.attrib["xMin"]), float(line.attrib["xMax"])\n    except (KeyError, ValueError) as exc:\n        fail(f"invalid line bounds: {line.attrib}")\n        raise AssertionError from exc\n\n\n'''
helper = '''def coalesce_right_edge_fragments(\n    bounds: list[tuple[float, float]],\n    expected_left: float,\n    expected_right: float,\n    tolerance_pt: float,\n) -> list[tuple[float, float]]:\n    result: list[tuple[float, float]] = []\n    for x_min, x_max in bounds:\n        if (\n            result\n            and x_min > expected_left + tolerance_pt\n            and abs(x_max - expected_right) <= tolerance_pt\n            and abs(result[-1][1] - expected_right) > tolerance_pt\n        ):\n            previous_min, previous_max = result[-1]\n            result[-1] = (min(previous_min, x_min), max(previous_max, x_max))\n            continue\n        result.append((x_min, x_max))\n    return result\n\n\n'''
alignment_text = alignment.read_text(encoding="utf-8")
if alignment_text.count(insert_after) != 1:
    raise SystemExit("alignment helper insertion point changed")
alignment_text = alignment_text.replace(insert_after, insert_after + helper)
old_bounds = '''    bounds = [line_bounds(line) for line in lines]\n    left_deltas = [abs(x_min - expected_left) for x_min, _ in bounds]\n    right_deltas = [abs(x_max - expected_right) for _, x_max in bounds[:-1]]\n'''
new_bounds = '''    raw_bounds = [line_bounds(line) for line in lines]\n    bounds = coalesce_right_edge_fragments(\n        raw_bounds, expected_left, expected_right, tolerance_pt\n    )\n    if len(bounds) < minimum_lines:\n        fail(\n            f"{scenario['id']}: expected at least {minimum_lines} physical lines after "\n            f"fragment coalescing, found {len(bounds)}"\n        )\n    left_deltas = [abs(x_min - expected_left) for x_min, _ in bounds]\n    right_deltas = [abs(x_max - expected_right) for _, x_max in bounds[:-1]]\n'''
if alignment_text.count(old_bounds) != 1:
    raise SystemExit("alignment bounds block changed")
alignment_text = alignment_text.replace(old_bounds, new_bounds)
alignment_text = alignment_text.replace(
    '            "line_count": len(lines),\n',
    '            "raw_line_count": len(lines),\n            "line_count": len(bounds),\n',
    1,
)
alignment_text = alignment_text.replace(
    '        "tool": "pdftotext -bbox-layout",\n',
    '        "tool": "pdftotext -bbox-layout + geometric fragment coalescing",\n',
    1,
)
alignment.write_text(alignment_text, encoding="utf-8")

print("R3-B1 evidence repair applied.")
