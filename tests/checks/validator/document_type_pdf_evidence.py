#!/usr/bin/env python3
"""Bounded CLI/Deep evidence from five distinct project-class-rendered PDFs."""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
import tempfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CLI = ROOT / "tools" / "validate-ufc-pdf.py"
SCENARIOS = {
    "scientific-article": {
        "document_type": "scientific-article",
        "expected": {
            "structure.cover": "NOT APPLICABLE",
            "structure.approval": "NOT APPLICABLE",
            "structure.toc": "NOT APPLICABLE",
            "structure.resumo": "PASS",
            "structure.refs": "PASS",
            "structure.keywords": "PASS",
        },
        "negative": False,
    },
    "research-project": {
        "document_type": "research-project",
        "expected": {
            "structure.approval": "NOT APPLICABLE",
            "structure.resumo": "NOT APPLICABLE",
            "structure.abstract": "NOT APPLICABLE",
            "structure.toc": "PASS",
            "structure.refs": "PASS",
        },
        "negative": False,
    },
    "anonymized-research-project": {
        "document_type": "anonymized-research-project",
        "expected": {
            "structure.approval": "NOT APPLICABLE",
            "structure.resumo": "NOT APPLICABLE",
            "structure.abstract": "NOT APPLICABLE",
            "structure.toc": "PASS",
            "structure.refs": "PASS",
        },
        "negative": False,
    },
    "scientific-article-missing": {
        "document_type": "scientific-article",
        "expected": {
            "structure.approval": "NOT APPLICABLE",
            "structure.resumo": "FAIL",
            "structure.refs": "FAIL",
            "structure.keywords": "FAIL",
        },
        "negative": True,
    },
    "research-project-missing-refs": {
        "document_type": "research-project",
        "expected": {
            "structure.approval": "NOT APPLICABLE",
            "structure.resumo": "NOT APPLICABLE",
            "structure.refs": "FAIL",
        },
        "negative": True,
    },
}


def fail(message: str) -> None:
    raise SystemExit("Document-type PDF evidence: " + message)


def check_report(report: dict, scenario: str) -> None:
    spec = SCENARIOS[scenario]
    if report.get("document_type") != spec["document_type"]:
        fail(f"{scenario}: document type mismatch")
    if report.get("mode") != "cli-deep-local":
        fail(f"{scenario}: CLI route mismatch")
    checks = report.get("checks")
    if not isinstance(checks, list):
        fail(f"{scenario}: missing checks")
    by_id = {item["id"]: item for item in checks}
    if len(by_id) != len(checks):
        fail(f"{scenario}: duplicate checks")
    if by_id.get("pdf.open", {}).get("status") != "PASS":
        fail(f"{scenario}: actual PDF could not be opened")
    for key, expected in spec["expected"].items():
        actual = by_id.get(key, {}).get("status")
        if actual != expected:
            fail(f"{scenario}: {key}: expected {expected}, got {actual}")
    expected_verdict = "FAIL" if spec["negative"] else None
    if expected_verdict and report.get("verdict") != expected_verdict:
        fail(f"{scenario}: negative did not yield FAIL verdict")
    if not spec["negative"] and report.get("verdict") == "FAIL":
        failures = [c["id"] for c in checks if c["status"] == "FAIL" and c["mandatory"]]
        fail(f"{scenario}: correctly typed real PDF has mandatory failures: {failures}")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--pdf-dir", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    parser.add_argument("--source-sha", required=True)
    args = parser.parse_args()

    records = {}
    digests = set()
    with tempfile.TemporaryDirectory(prefix="ufc-document-type-cli-") as work:
        for scenario, spec in SCENARIOS.items():
            pdf = args.pdf_dir / (scenario + ".pdf")
            if not pdf.is_file() or not pdf.stat().st_size:
                fail(f"compiled PDF missing: {pdf}")
            digest = hashlib.sha256(pdf.read_bytes()).hexdigest()
            if digest in digests:
                fail(f"duplicate PDF bytes in {scenario}")
            digests.add(digest)
            report_file = Path(work) / (scenario + ".json")
            result = subprocess.run(
                [
                    sys.executable, str(CLI), str(pdf),
                    "--profile", "portable",
                    "--document-type", spec["document_type"],
                    "--format", "json", "--output", str(report_file),
                ],
                cwd=ROOT, text=True, capture_output=True, check=False,
            )
            if result.returncode not in (0, 1) or not report_file.is_file():
                fail(f"{scenario}: validator did not produce a usable report: "
                     f"exit={result.returncode}, stderr={result.stderr[-800:]}")
            report = json.loads(report_file.read_text(encoding="utf-8"))
            check_report(report, scenario)
            by_id = {entry["id"]: entry for entry in report["checks"]}
            records[scenario] = {
                "document_type": spec["document_type"],
                "pdf_sha256": digest,
                "bytes": pdf.stat().st_size,
                "verdict": report["verdict"],
                "expected_checks": {
                    check_id: by_id[check_id]["status"]
                    for check_id in spec["expected"]
                },
                "negative_control": spec["negative"],
            }
            print(
                "DOCUMENT-TYPE-PDF-EVIDENCE "
                f"surface=cli-deep scenario={scenario} "
                f"checks={len(spec['expected'])} status=PASS "
                f"negative_control={str(spec['negative']).lower()}"
            )

    output = {
        "schema_version": 1,
        "component": "document-type-final-pdf",
        "status": "PASS",
        "source_commit_sha": args.source_sha,
        "proof_state": "automatic-partial",
        "pdfs": records,
        "limits": [
            "Detected PDF text does not prove correct semantic placement.",
            "Project identity, anonymity and periodical conditions need separate evidence.",
            "The Web/Lite and CLI/Deep measurement backends are not assumed identical.",
        ],
    }
    args.evidence.parent.mkdir(parents=True, exist_ok=True)
    args.evidence.write_text(
        json.dumps(output, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )
    print("DOCUMENT-TYPE-PDF-EVIDENCE surface=cli-deep status=PASS "
          "real_pdfs=5 positive=3 negative=2 proof_state=automatic-partial")


if __name__ == "__main__":
    main()
