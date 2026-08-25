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

SCENARIO = ROOT / "normativa" / "pretextual-errata-scenario.json"


def fail(message: str) -> None:
    raise SystemExit(f"Errata oracle failed: {message}")


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


def marker_page(pages: list[ET.Element], marker: str) -> int | None:
    wanted = normalize(marker)
    hits = [
        index
        for index, page in enumerate(pages, start=1)
        if wanted in normalized_page_text(page)
    ]
    return hits[0] if len(hits) == 1 else None


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


def main() -> None:
    parser = argparse.ArgumentParser(description="Measure N6 errata final-PDF evidence.")
    parser.add_argument("present_pdf", type=Path)
    parser.add_argument("absent_pdf", type=Path)
    parser.add_argument("--json", type=Path, required=True)
    parser.add_argument("--commit-sha")
    parser.add_argument("--enforce", action="store_true")
    args = parser.parse_args()

    for pdf in (args.present_pdf, args.absent_pdf):
        if not pdf.is_file():
            fail(f"PDF not found: {pdf}")

    scenario = load_json(SCENARIO)
    if (
        scenario.get("schema_version") != 1
        or scenario.get("phase") != "N6"
        or scenario.get("component") != "errata"
    ):
        fail("invalid errata scenario schema/phase/component")

    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    expected_scope = {rule_id for rule_id in rules if rule_id.startswith("errata.")}
    scenario_scope = set(scenario.get("rules", []))
    if scenario_scope != expected_scope or len(expected_scope) != 3:
        fail(
            "errata scope mismatch: "
            f"scenario_only={sorted(scenario_scope - expected_scope)} "
            f"contract_only={sorted(expected_scope - scenario_scope)} "
            f"count={len(expected_scope)}"
        )

    markers = scenario.get("markers")
    if not isinstance(markers, dict):
        fail("errata markers are required")
    required_markers = {
        "title_page",
        "errata_heading",
        "reference",
        "correction",
        "sentinel",
    }
    if set(markers) != required_markers:
        fail(
            "errata marker mismatch: "
            f"missing={sorted(required_markers - set(markers))} "
            f"extra={sorted(set(markers) - required_markers)}"
        )

    present_pages = bbox_pages(args.present_pdf)
    absent_pages = bbox_pages(args.absent_pdf)

    present = {
        name: marker_page(present_pages, marker)
        for name, marker in markers.items()
    }
    absent = {
        name: marker_page(absent_pages, marker)
        for name, marker in markers.items()
    }

    optional_rule = rules["errata.element.optional"]
    optional_expected = {"required": bool(optional_rule["values"]["required"])}
    optional_measured = {
        "present_fixture": {
            "title_page": present["title_page"],
            "errata_page": present["errata_heading"],
            "sentinel_page": present["sentinel"],
        },
        "absent_fixture": {
            "title_page": absent["title_page"],
            "errata_page": absent["errata_heading"],
            "reference_page": absent["reference"],
            "correction_page": absent["correction"],
            "sentinel_page": absent["sentinel"],
        },
    }
    optional_pass = (
        optional_expected["required"] is False
        and present["errata_heading"] is not None
        and absent["title_page"] is not None
        and absent["sentinel"] is not None
        and absent["sentinel"] == absent["title_page"] + 1
        and absent["errata_heading"] is None
        and absent["reference"] is None
        and absent["correction"] is None
    )

    position_rule = rules["errata.position"]
    position_expected = {"after": position_rule["values"]["after"]}
    position_measured = {
        "title_page": present["title_page"],
        "errata_page": present["errata_heading"],
        "sentinel_page": present["sentinel"],
        "immediately_after_title_page": (
            present["title_page"] is not None
            and present["errata_heading"] is not None
            and present["errata_heading"] == present["title_page"] + 1
        ),
    }
    position_pass = (
        position_expected["after"] == "title-page"
        and position_measured["immediately_after_title_page"]
        and present["sentinel"] is not None
        and present["errata_heading"] is not None
        and present["errata_heading"] < present["sentinel"]
    )

    contents_rule = rules["errata.contents"]
    contents_expected = {
        "required_parts": contents_rule["values"]["required_parts"],
    }
    contents_measured = {
        "errata_page": present["errata_heading"],
        "work_reference_page": present["reference"],
        "corrections_page": present["correction"],
    }
    contents_pass = (
        set(contents_expected["required_parts"]) == {"work-reference", "corrections"}
        and present["errata_heading"] is not None
        and present["reference"] == present["errata_heading"]
        and present["correction"] == present["errata_heading"]
    )

    evidence = [
        record(
            "errata.element.optional",
            "PASS" if optional_pass else "FAIL",
            optional_expected,
            optional_measured,
            "pdftotext -bbox-layout",
        ),
        record(
            "errata.position",
            "PASS" if position_pass else "FAIL",
            position_expected,
            position_measured,
            "pdftotext -bbox-layout",
        ),
        record(
            "errata.contents",
            "PASS" if contents_pass else "FAIL",
            contents_expected,
            contents_measured,
            "pdftotext -bbox-layout",
        ),
    ]

    status_counts = dict(Counter(item["status"] for item in evidence))
    result = "PASS" if all(item["status"] == "PASS" for item in evidence) else "FAIL"
    payload = {
        "schema_version": 1,
        "phase": "N6",
        "component": "errata",
        "source_commit_sha": args.commit_sha,
        "result": result,
        "status_counts": status_counts,
        "present_fixture": {
            "page_count": len(present_pages),
            "markers": present,
        },
        "absent_fixture": {
            "page_count": len(absent_pages),
            "markers": absent,
        },
        "evidence": evidence,
    }

    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    print(
        "N6-EVIDENCE errata-summary "
        + " ".join(f"{key}={value}" for key, value in sorted(status_counts.items()))
        + f" present_pages={len(present_pages)}"
        + f" absent_pages={len(absent_pages)}"
    )
    for item in evidence:
        print(
            f"N6-EVIDENCE rule={item['rule_id']} status={item['status']} "
            f"expected={json.dumps(item['expected'], ensure_ascii=False, sort_keys=True)} "
            f"measured={json.dumps(item['measured'], ensure_ascii=False, sort_keys=True)}"
        )

    if args.enforce and result != "PASS":
        failed = [item["rule_id"] for item in evidence if item["status"] != "PASS"]
        fail("measured normative mismatches: " + ", ".join(failed))


if __name__ == "__main__":
    main()
