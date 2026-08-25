#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
import sys
import xml.etree.ElementTree as ET
from collections import Counter
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract
from pdf_measurement import normalize

SCENARIO = ROOT / "normativa" / "pretextual-approval-scenario.json"


def fail(message: str) -> None:
    raise SystemExit(f"Approval-page oracle failed: {message}")


def local(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path} must contain an object")
    return value


def run(command: list[str]) -> bytes:
    completed = subprocess.run(
        command,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.decode("utf-8", errors="replace").strip()
        fail(f"command failed: {' '.join(command)}: {stderr}")
    return completed.stdout


def bbox_pages(pdf: Path) -> list[ET.Element]:
    payload = run(["pdftotext", "-bbox-layout", str(pdf), "-"])
    try:
        root = ET.fromstring(payload)
    except ET.ParseError as exc:
        fail(f"invalid pdftotext XML for {pdf.name}: {exc}")
    pages = [node for node in root.iter() if local(node.tag) == "page"]
    if not pages:
        fail(f"PDF extractor returned no pages for {pdf.name}")
    return pages


def words(node: ET.Element) -> list[ET.Element]:
    return [item for item in node.iter() if local(item.tag) == "word"]


def lines(node: ET.Element) -> list[ET.Element]:
    return [
        item
        for item in node.iter()
        if local(item.tag) == "line"
        and any(local(child.tag) == "word" for child in item)
    ]


def word_text(node: ET.Element) -> str:
    return "".join(node.itertext()).strip()


def line_text(node: ET.Element) -> str:
    return " ".join(word_text(item) for item in words(node))


def normalized_page_text(page: ET.Element) -> str:
    return normalize(" ".join(line_text(line) for line in lines(page)))


def normalized_document_text(pages: list[ET.Element]) -> str:
    return normalize(" ".join(normalized_page_text(page) for page in pages))


def find_line(page: ET.Element, marker: str) -> ET.Element | None:
    wanted = normalize(marker)
    matches = [line for line in lines(page) if wanted in normalize(line_text(line))]
    return matches[0] if len(matches) == 1 else None


def y_min(node: ET.Element | None) -> float | None:
    if node is None:
        return None
    try:
        return float(node.attrib["yMin"])
    except (KeyError, ValueError):
        return None


def marker_page(pages: list[ET.Element], marker: str) -> int | None:
    wanted = normalize(marker)
    hits = [
        index
        for index, page in enumerate(pages, start=1)
        if wanted in normalized_page_text(page)
    ]
    return hits[0] if len(hits) == 1 else None


def parse_profile_pdfs(values: list[str]) -> dict[str, Path]:
    result: dict[str, Path] = {}
    for value in values:
        profile, separator, raw_path = value.partition("=")
        if not separator or not profile or not raw_path:
            fail(f"invalid profile PDF mapping: {value}")
        if profile in result:
            fail(f"duplicate profile PDF mapping: {profile}")
        path = Path(raw_path)
        if not path.is_file():
            fail(f"PDF not found for {profile}: {path}")
        result[profile] = path
    return result


def record(
    rule_id: str,
    status: str,
    expected: Any,
    measured: Any,
    tool: str,
) -> dict[str, Any]:
    return {
        "rule_id": rule_id,
        "status": status,
        "expected": expected,
        "measured": measured,
        "tool": tool,
    }


def academic_measurement(
    profile: str,
    pdf: Path,
    markers: dict[str, str],
) -> dict[str, Any]:
    pages = bbox_pages(pdf)
    sentinel_page = marker_page(pages, markers["sentinel"])
    approval_marker_names = [
        "author",
        "title",
        "subtitle",
        "nature",
        "approval_date",
        "committee_heading",
        "advisor",
        "member",
    ]
    marker_pages = {
        name: marker_page(pages, markers[name]) for name in approval_marker_names
    }
    approval_pages = {page for page in marker_pages.values() if page is not None}
    approval_page = next(iter(approval_pages)) if len(approval_pages) == 1 else None
    present = (
        approval_page is not None
        and all(page == approval_page for page in marker_pages.values())
        and sentinel_page is not None
        and approval_page < sentinel_page
    )

    order: dict[str, Any] = {
        "profile": profile,
        "page_count": len(pages),
        "approval_page": approval_page,
        "sentinel_page": sentinel_page,
        "marker_pages": marker_pages,
        "present": present,
    }
    if approval_page is None:
        order["order_pass"] = False
        return order

    page = pages[approval_page - 1]
    nodes = {name: find_line(page, markers[name]) for name in approval_marker_names}
    positions = {name: y_min(node) for name, node in nodes.items()}
    title_line = nodes["title"]
    title_line_text = normalize(line_text(title_line)) if title_line is not None else ""
    title_before_subtitle = (
        normalize(markers["title"]) in title_line_text
        and normalize(markers["subtitle"]) in title_line_text
        and title_line_text.find(normalize(markers["title"]))
        < title_line_text.find(normalize(markers["subtitle"]))
    )

    sequence_names = [
        "author",
        "title",
        "nature",
        "approval_date",
        "committee_heading",
        "advisor",
        "member",
    ]
    sequence = [positions[name] for name in sequence_names]
    numeric_sequence = all(value is not None for value in sequence)
    strictly_increasing = (
        numeric_sequence
        and all(
            float(left) < float(right)
            for left, right in zip(sequence, sequence[1:])
            if left is not None and right is not None
        )
    )
    subtitle_same_line = (
        positions["title"] is not None
        and positions["subtitle"] is not None
        and abs(float(positions["title"]) - float(positions["subtitle"])) <= 1.0
    )

    order.update(
        {
            "positions_y_pt": positions,
            "title_before_subtitle": title_before_subtitle,
            "subtitle_same_line": subtitle_same_line,
            "order_pass": bool(
                present
                and strictly_increasing
                and subtitle_same_line
                and title_before_subtitle
            ),
        }
    )
    return order


def non_applicable_measurement(
    profile: str,
    pdf: Path,
    markers: dict[str, str],
) -> dict[str, Any]:
    pages = bbox_pages(pdf)
    text = normalized_document_text(pages)
    approval_markers = [
        markers["author"],
        markers["title"],
        markers["subtitle"],
        markers["nature"],
        markers["approval_date"],
        markers["committee_heading"],
        markers["advisor"],
        markers["member"],
    ]
    present = {marker: normalize(marker) in text for marker in approval_markers}
    sentinel_page = marker_page(pages, markers["sentinel"])
    return {
        "profile": profile,
        "page_count": len(pages),
        "sentinel_page": sentinel_page,
        "approval_marker_presence": present,
        "current_route_suppressed": sentinel_page is not None and not any(present.values()),
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure N6 approval-page final-PDF evidence.")
    parser.add_argument("profile_pdf", nargs="+")
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    scenario = load_json(SCENARIO)
    if scenario.get("schema_version") != 1 or scenario.get("phase") != "N6":
        fail("invalid approval scenario schema/phase")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    expected_scope = {rule_id for rule_id in rules if rule_id.startswith("approval.")}
    scenario_scope = set(scenario.get("rules", []))
    if scenario_scope != expected_scope or len(expected_scope) != 2:
        fail(
            "approval scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )

    academic_profiles = list(scenario.get("academic_profiles", []))
    non_applicable_profiles = list(scenario.get("suppressed_profiles", []))
    required_rule = rules["approval.element.required"]
    expected_applicability = sorted(required_rule.get("applicability", {}).get("profiles", []))
    if sorted(academic_profiles) != expected_applicability:
        fail(
            "approval applicability mismatch: "
            f"scenario={sorted(academic_profiles)} contract={expected_applicability}"
        )

    profile_pdfs = parse_profile_pdfs(args.profile_pdf)
    expected_profiles = set(academic_profiles) | set(non_applicable_profiles)
    if set(profile_pdfs) != expected_profiles:
        fail(
            "approval PDF profile mismatch: "
            f"missing={sorted(expected_profiles - set(profile_pdfs))} "
            f"extra={sorted(set(profile_pdfs) - expected_profiles)}"
        )

    markers = scenario.get("markers")
    if not isinstance(markers, dict):
        fail("approval markers are required")

    academic = {
        profile: academic_measurement(profile, profile_pdfs[profile], markers)
        for profile in academic_profiles
    }
    non_applicable = {
        profile: non_applicable_measurement(profile, profile_pdfs[profile], markers)
        for profile in non_applicable_profiles
    }

    required_expected = {
        "required": bool(required_rule["values"]["required"]),
        "profiles": academic_profiles,
    }
    required_measured = {
        profile: {
            "present": data["present"],
            "approval_page": data["approval_page"],
            "sentinel_page": data["sentinel_page"],
        }
        for profile, data in academic.items()
    }
    required_pass = required_expected["required"] and all(
        data["present"] for data in academic.values()
    )

    order_rule = rules["approval.fields.order"]
    order_expected = order_rule["values"]["order"]
    order_measured = {
        profile: {
            "positions_y_pt": data.get("positions_y_pt"),
            "title_before_subtitle": data.get("title_before_subtitle"),
            "subtitle_same_line": data.get("subtitle_same_line"),
            "order_pass": data.get("order_pass", False),
        }
        for profile, data in academic.items()
    }
    order_pass = all(data.get("order_pass", False) for data in academic.values())

    evidence = [
        record(
            "approval.element.required",
            "PASS" if required_pass else "FAIL",
            required_expected,
            required_measured,
            "pdftotext -bbox-layout",
        ),
        record(
            "approval.fields.order",
            "PASS" if order_pass else "FAIL",
            order_expected,
            order_measured,
            "pdftotext -bbox-layout",
        ),
    ]
    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "approval-page",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "academic_profiles": academic,
        "supplemental_non_applicable_profiles": non_applicable,
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N6-EVIDENCE approval-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" academic_profiles={len(academic_profiles)}"
        + f" supplemental_profiles={len(non_applicable_profiles)}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )
    print(
        "N6-EVIDENCE approval-non-applicable-observation "
        + json.dumps(non_applicable, ensure_ascii=False, sort_keys=True)
    )

    if args.enforce and result != "PASS":
        failed = [item["rule_id"] for item in evidence if item["status"] != "PASS"]
        fail("measured normative mismatches: " + ", ".join(failed))


if __name__ == "__main__":
    main()
