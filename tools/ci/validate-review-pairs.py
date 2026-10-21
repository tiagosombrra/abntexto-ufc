#!/usr/bin/env python3
"""Fail-closed source-bound verification of seven release-review PDF/TeX pairs.

This is an automated integrity and *fixture-token* privacy preflight, NOT a
general anonymity certificate or human visual approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import unicodedata
from pathlib import Path

PROFILES = (
    "undergraduate-capstone",
    "specialization-capstone",
    "masters-thesis",
    "doctoral-thesis",
    "research-project",
    "anonymized-research-project",
    "scientific-article",
)
IDENTITY_TOKENS = (
    "Autor Matriz Teste",
    "Prof. Orientador Matriz Teste",
    "Prof. Membro Matriz Teste",
)


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def normalize(value: str) -> str:
    return "".join(
        char for char in unicodedata.normalize("NFKD", value).casefold()
        if char.isalnum()
    )


def command_text(*args: str) -> str:
    result = subprocess.run(
        list(args), text=True, capture_output=True, check=True
    )
    return result.stdout


def assert_no_tokens(text: str, surface: str) -> None:
    normalized = normalize(text)
    for token in IDENTITY_TOKENS:
        require(normalize(token) not in normalized,
                f"Anonymized review PDF leaks a fixture identity on {surface}: {token}")


def assert_manifest(root: Path, source_sha: str, expected_version: str) -> dict:
    require(re.fullmatch(r"[0-9a-f]{40}", source_sha) is not None,
            "Source SHA must be one exact Git commit")
    manifest = json.loads((root / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("source_sha") == source_sha,
            "Review manifest does not bind to the exact candidate source SHA")
    require(re.fullmatch(r"[0-9]+\.[0-9]+\.[0-9]+", expected_version) is not None,
            "Expected release version must use a semantic three-component form")
    require(manifest.get("version") == expected_version,
            "Review manifest version does not match the actual package version")
    require(manifest.get("status") == "READY_FOR_MAINTAINER_REVIEW",
            "Review manifest has an unsupported state")
    require(manifest.get("maintainer_visual_approval") == "PENDING",
            "No CI process may approve a maintainer visual review")
    pairs = manifest.get("pairs")
    require(isinstance(pairs, list) and len(pairs) == len(PROFILES)
            and manifest.get("pair_count") == len(PROFILES),
            "Review manifest must contain exactly seven pairs")
    expected = {}
    for i, (item, profile) in enumerate(zip(pairs, PROFILES), 1):
        prefix = f"{i:02d}-{profile}"
        require(item.get("profile") == profile, f"Wrong profile at index {i}")
        for field, suffix in (("source", ".tex"), ("pdf", ".pdf")):
            name = prefix + suffix
            require(item.get(field) == name, f"Unexpected {field} filename for {profile}")
            path = root / name
            require(path.is_file() and path.stat().st_size > 0,
                    f"Missing review pair: {name}")
            value = digest(path)
            require(item.get(field + "_sha256") == value,
                    f"Manifest SHA-256 mismatch: {name}")
            expected[name] = value

    checksum_lines = (root / "SHA256SUMS").read_text(encoding="utf-8").splitlines()
    recorded = {}
    for line in checksum_lines:
        match = re.fullmatch(r"([0-9a-f]{64})  \./(.+)", line)
        require(match is not None, "Unexpected SHA256SUMS entry syntax")
        sha, name = match.groups()
        require(name not in recorded, "Duplicate SHA256SUMS entry")
        recorded[name] = sha
    require(recorded == expected, "SHA256SUMS entries differ from all 14 review files")

    allowed = set(expected) | {"manifest.json", "SHA256SUMS"}
    require({x.name for x in root.iterdir()} == allowed,
            "Review-pair directory has unexpected files")

    anon = pairs[5]
    source = (root / anon["source"]).read_text(encoding="utf-8")
    normalized_source = normalize(source)
    for token in IDENTITY_TOKENS:
        require(normalize(token) in normalized_source,
                "Fixture changed: expected identity-bearing LaTeX source")

    pdf = str(root / anon["pdf"])
    assert_no_tokens(command_text("pdftotext", "-enc", "UTF-8", pdf, "-"),
                     "extracted page text")
    assert_no_tokens(command_text("pdfinfo", pdf), "PDF Info")
    assert_no_tokens(command_text("pdfinfo", "-meta", pdf), "PDF XMP metadata")
    attachments = command_text("pdfdetach", "-list", pdf).strip()
    require(attachments == "0 embedded files",
            "Anonymized PDF must not carry embedded source/attachments")

    evidence = manifest.get("blind_review_boundary")
    require(isinstance(evidence, dict), "Missing blind-review boundary declaration")
    require(evidence.get("profile") == "anonymized-research-project",
            "Anonymized blind-review evidence profile mismatch")
    require(evidence.get("latex_source_distribution") == "INTERNAL_AUDIT_ONLY",
            "The identity-bearing TeX source must NOT be declared blind-safe")
    require(evidence.get("pdf_identity_token_check") == "PASS",
            "Expected fixture-PDF identity token proof is absent")
    require(evidence.get("human_approval") == "PENDING",
            "Automated anonymity checks cannot imply human approval")
    return manifest


def self_test() -> None:
    leaked = "Title \n Prof. Orientador \n Matriz Teste end"
    try:
        assert_no_tokens(leaked, "controlled-negative")
    except ValueError:
        pass
    else:
        raise ValueError("Controlled identity-leak negative was not detected")
    assert_no_tokens("PERFIL-ANONIMO-001 / Documento de validação", "positive")
    require(normalize("PROF. \nORIENTADOR MATRIZ TESTE") ==
            normalize("Prof. Orientador Matriz Teste"),
            "Whitespace-insensitive identity detection regressed")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--directory", required=True, type=Path)
    parser.add_argument("--source-sha", required=True)
    parser.add_argument("--expected-version", required=True)
    args = parser.parse_args()
    self_test()
    manifest = assert_manifest(args.directory, args.source_sha, args.expected_version)
    print(
        "RELEASE-REVIEW-BOUNDARY-EVIDENCE status=PASS "
        f"source_sha={manifest['source_sha']} pairs=7 "
        "all_pdf_tex_sha256=PASS archive_checksum_manifest=PASS "
        "anonymized_pdf_fixture_identity=ABSENT metadata=PASS "
        "embedded_files=0 blind_tex_source=INTERNAL_AUDIT_ONLY "
        "maintainer_visual_approval=PENDING"
    )


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError, subprocess.CalledProcessError) as exc:
        print(f"Release review provenance/privacy gate failed: {exc}", file=sys.stderr)
        raise SystemExit(1) from exc
