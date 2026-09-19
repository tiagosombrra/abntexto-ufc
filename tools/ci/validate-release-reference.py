#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path

PDF_PATH = Path("artifacts/validation/release-reference-pdf.pdf")
EVIDENCE_PATH = Path("artifacts/validation/release-reference-reproducibility.json")


def fail(message: str) -> None:
    raise SystemExit(message)


def main() -> None:
    if not PDF_PATH.is_file() or PDF_PATH.stat().st_size == 0:
        fail("Canonical release reference PDF is missing or empty.")
    if not EVIDENCE_PATH.is_file():
        fail("Canonical release reference reproducibility evidence is missing.")

    evidence = json.loads(EVIDENCE_PATH.read_text(encoding="utf-8"))
    source_sha = os.environ["SOURCE_COMMIT_SHA"]

    if evidence.get("status") != "PASS":
        fail("Canonical release reference evidence is not PASS.")
    if evidence.get("source_sha") != source_sha:
        fail(
            "Canonical release reference source SHA mismatch: "
            f"expected {source_sha}, got {evidence.get('source_sha')}"
        )
    if evidence.get("canonical_source") != "template/main.tex":
        fail("Canonical release reference source identity is not template/main.tex.")
    if evidence.get("canonical_output") != PDF_PATH.as_posix():
        fail("Canonical release reference output identity is inconsistent.")
    if (
        evidence.get("independent_clean_builds") != 2
        or evidence.get("identical_sha256") is not True
    ):
        fail("Canonical release reference is not backed by two byte-identical clean builds.")

    digest = hashlib.sha256(PDF_PATH.read_bytes()).hexdigest()
    builds = evidence.get("builds") or []
    if len(builds) != 2 or any(build.get("sha256") != digest for build in builds):
        fail("Canonical release reference PDF SHA-256 does not match both clean-build records.")

    expected_validation = {
        "font_embedding": "PASS",
        "portable_pdf_validator": "PASS",
        "pdfa_2b": "PASS",
        "unicode_extraction": "PASS",
    }
    measured_validation = evidence.get("validation") or {}
    for key, expected in expected_validation.items():
        if measured_validation.get(key) != expected:
            fail(f"Canonical release reference validation {key} is not {expected}.")

    print(
        "CANONICAL-REFERENCE-EVIDENCE status=PASS "
        f"source_sha={source_sha} sha256={digest} builds=2 "
        "font_embedding=PASS pdf_validator=PASS pdfa_2b=PASS unicode=PASS"
    )


if __name__ == "__main__":
    main()
