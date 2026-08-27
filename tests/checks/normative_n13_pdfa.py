#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import shutil
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
MECHANISM_ID = "pdf-pdfa-validation"
SOURCE_MARKER = b"<pdfaid:part>2</pdfaid:part>"
MUTATED_MARKER = b"<pdfaid:part>3</pdfaid:part>"
TARGET_RULE = {
    "specification": "ISO 19005-2:2011",
    "clause": "6.6.4",
    "testNumber": "2",
}
POPLER_CONTAINER = "ghcr.io/xu-cheng/texlive-debian:latest"


def fail(message: str) -> None:
    raise SystemExit(f"N13 PDF/A negative validation failed: {message}")


def run(command: list[str]) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        command,
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        errors="replace",
        check=False,
    )


def local_name(tag: str) -> str:
    return tag.rsplit("}", 1)[-1]


def load_xml(path: Path, *, diagnostic: str = "") -> ET.Element:
    try:
        return ET.parse(path).getroot()
    except (OSError, ET.ParseError) as exc:
        suffix = f"; veraPDF stderr: {diagnostic[-1600:]}" if diagnostic.strip() else ""
        fail(f"invalid veraPDF XML report {path}: {exc}{suffix}")


def validation_report(root: ET.Element) -> ET.Element:
    matches = [element for element in root.iter() if local_name(element.tag) == "validationReport"]
    if len(matches) != 1:
        fail(f"expected exactly one validationReport element; found {len(matches)}")
    return matches[0]


def require_positive_report(path: Path) -> None:
    report = validation_report(load_xml(path))
    if report.attrib.get("isCompliant") != "true":
        fail("positive baseline report is not PDF/A-2b compliant")


def repository_relative(path: Path) -> str:
    resolved = path.resolve()
    try:
        return resolved.relative_to(ROOT.resolve()).as_posix()
    except ValueError:
        fail(f"container path must stay inside the repository: {path}")


def local_readable_text(pdf: Path) -> str:
    info = run(["pdfinfo", str(pdf)])
    if info.returncode != 0:
        fail(f"pdfinfo rejected readable-PDF requirement for {pdf}: {info.stdout[-1200:]}")
    text = run(["pdftotext", "-layout", str(pdf), "-"])
    if text.returncode != 0:
        fail(f"pdftotext rejected readable-PDF requirement for {pdf}: {text.stdout[-1200:]}")
    if not text.stdout.strip():
        fail(f"pdftotext produced empty text for {pdf}")
    return text.stdout


def verify_readability_and_text_identity(source: Path, mutated: Path) -> str:
    if shutil.which("pdfinfo") and shutil.which("pdftotext"):
        source_text = local_readable_text(source)
        mutated_text = local_readable_text(mutated)
        if mutated_text != source_text:
            fail("controlled XMP mutation changed extracted document text")
        return "local-poppler"

    if not shutil.which("docker"):
        fail("pdfinfo/pdftotext or Docker is required for readable-PDF validation")

    source_rel = repository_relative(source)
    mutated_rel = repository_relative(mutated)
    script = r"""
set -eu
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq --no-install-recommends poppler-utils >/dev/null
pdfinfo "$1" >/tmp/source.info
pdfinfo "$2" >/tmp/mutated.info
pdftotext -layout "$1" /tmp/source.txt
pdftotext -layout "$2" /tmp/mutated.txt
test -s /tmp/source.txt
test -s /tmp/mutated.txt
cmp -s /tmp/source.txt /tmp/mutated.txt
"""
    completed = run(
        [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{ROOT}:/data:ro",
            POPLER_CONTAINER,
            "/bin/bash",
            "-lc",
            script,
            "n13-poppler",
            f"/data/{source_rel}",
            f"/data/{mutated_rel}",
        ]
    )
    if completed.returncode != 0:
        fail(f"containerized Poppler readability/text-identity check failed: {completed.stdout[-2000:]}")
    return "containerized-poppler"


def mutate_pdf(source: Path, target: Path) -> None:
    data = source.read_bytes()
    occurrences = data.count(SOURCE_MARKER)
    if occurrences != 1:
        fail(f"expected exactly one PDF/A part-2 XMP marker; found {occurrences}")
    if len(SOURCE_MARKER) != len(MUTATED_MARKER):
        fail("PDF/A metadata mutation must preserve byte length")
    mutated = data.replace(SOURCE_MARKER, MUTATED_MARKER, 1)
    if len(mutated) != len(data):
        fail("controlled PDF/A mutation changed file length")
    target.write_bytes(mutated)
    target.chmod(0o644)


def run_verapdf(pdf: Path, report: Path) -> tuple[str, int, str]:
    if shutil.which("verapdf"):
        command = ["verapdf", "-f", "2b", str(pdf)]
        runner = "local"
    elif shutil.which("docker"):
        relative = repository_relative(pdf)
        command = [
            "docker",
            "run",
            "--rm",
            "-v",
            f"{ROOT}:/data:ro",
            "verapdf/cli:v1.30.2",
            "-f",
            "2b",
            f"/data/{relative}",
        ]
        runner = "docker-verapdf-1.30.2"
    else:
        fail("veraPDF or Docker is required for N13 PDF/A negative validation")

    with report.open("w", encoding="utf-8") as handle:
        completed = subprocess.run(
            command,
            cwd=ROOT,
            stdout=handle,
            stderr=subprocess.PIPE,
            text=True,
            errors="replace",
            check=False,
        )
    return runner, completed.returncode, completed.stderr


def failed_rules(root: ET.Element) -> list[dict[str, str]]:
    result: list[dict[str, str]] = []
    for element in root.iter():
        if local_name(element.tag) != "rule" or element.attrib.get("status") != "failed":
            continue
        result.append(
            {
                "specification": element.attrib.get("specification", ""),
                "clause": element.attrib.get("clause", ""),
                "testNumber": element.attrib.get("testNumber", ""),
            }
        )
    return result


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Exercise a readable controlled PDF/A-2b metadata violation against veraPDF."
    )
    parser.add_argument("source", type=Path)
    parser.add_argument("--positive-report", type=Path, required=True)
    parser.add_argument(
        "--json",
        type=Path,
        default=Path("/tmp/abntexto-ufc-n13-pdfa.json"),
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    source = args.source
    if not source.is_file():
        fail(f"source PDF not found: {source}")
    require_positive_report(args.positive_report)

    with tempfile.TemporaryDirectory(prefix=".n13-pdfa-", dir=ROOT) as temp_dir_name:
        temp_dir = Path(temp_dir_name)
        temp_dir.chmod(0o755)
        mutated = temp_dir / "documento-pdfa-part3-negative.pdf"
        negative_report = temp_dir / "verapdf-negative.xml"

        mutate_pdf(source, mutated)
        readability_runner = verify_readability_and_text_identity(source, mutated)

        runner, vera_exit, vera_stderr = run_verapdf(mutated, negative_report)
        root = load_xml(negative_report, diagnostic=vera_stderr)
        report = validation_report(root)
        if report.attrib.get("isCompliant") != "false":
            fail(f"veraPDF did not reject controlled PDF/A mutation (exit {vera_exit})")

        rules = failed_rules(root)
        if TARGET_RULE not in rules:
            fail(f"veraPDF rejection did not include target rule {TARGET_RULE}; observed {rules}")

    payload: dict[str, Any] = {
        "schema_version": 1,
        "phase": "N13",
        "mechanism": MECHANISM_ID,
        "source_commit_sha": os.environ.get("SOURCE_COMMIT_SHA", os.environ.get("GITHUB_SHA", "")),
        "result": "PASS",
        "mutation": "pdfaid-part-2-to-3",
        "same_length_mutation": True,
        "source_marker_occurrences": 1,
        "readability_runner": readability_runner,
        "pdfinfo_readable": True,
        "pdftotext_readable": True,
        "extracted_text_unchanged": True,
        "verapdf_runner": runner,
        "verapdf_exit_code": vera_exit,
        "verapdf_is_compliant": False,
        "target_failed_rule": TARGET_RULE,
        "failed_rules": rules,
        "compile_failure_counted_as_rejection": False,
        "normative_contract_changed": False,
        "locator_policy_changed": False,
        "oracle_tolerances_changed": False,
        "proof_state_changed": False,
    }
    args.json.parent.mkdir(parents=True, exist_ok=True)
    args.json.write_text(json.dumps(payload, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")

    print(
        "N13-EVIDENCE mechanism=pdf-pdfa-validation status=PASS "
        "mutation=pdfaid-part-2-to-3 readable=true text_unchanged=true "
        "verapdf_compliant=false specification=ISO_19005_2 clause=6.6.4 test=2 "
        "compile_failure_counted_as_rejection=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()
