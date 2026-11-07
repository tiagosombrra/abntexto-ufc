#!/usr/bin/env python3
"""Exercise all 28 public TeX sources independently of the R4 stress fixtures."""
from __future__ import annotations

import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
OUT = ROOT / "artifacts/public-mesh-documents"
GENERATOR = ROOT / "tools/examples/generate_public_mesh_documents.py"
CONTENT = ROOT / "examples/public-mesh-documents/content.json"
STUDY = ROOT / "examples/canonical-mesh-study/study.json"
LOCALES = {"pt", "en", "es", "fr"}
PROFILES = {
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
}
BAD = ("INTEGRATED-", "R4-METHOD-", "R4SHORT-", "R4LONG-", "SYNTHETIC-ANON")


def sha(raw: bytes) -> str:
    """Use actual bytes rather than trusting a self-reported source manifest."""
    return hashlib.sha256(raw).hexdigest()


def check() -> None:
    manifest = json.loads((OUT / "manifest.json").read_text(encoding="utf-8"))
    entries = manifest["entries"]
    assert manifest["example_count"] == len(entries) == 28
    assert not manifest["pdf_certified"] and not manifest["publication_authorized"]
    assert manifest["test_fixture_separated"]
    assert manifest["source_study_sha256"] == sha(STUDY.read_bytes())
    assert manifest["public_content_sha256"] == sha(CONTENT.read_bytes())
    assert manifest["generator_sha256"] == sha(GENERATOR.read_bytes())
    assert {(e["profile"], e["locale"]) for e in entries} == {
        (p, l) for p in PROFILES for l in LOCALES
    }
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    paths = set()
    for entry in entries:
        source_path = ROOT / entry["source"]
        assert source_path.is_relative_to(OUT)
        raw = source_path.read_bytes()
        source = raw.decode("utf-8")
        assert sha(raw) == entry["source_sha256"]
        paths.add(str(source_path))
        assert entry["status"] == "SOURCE_ONLY_PDF_UNVERIFIED"
        assert entry["human_approval"] == "PENDING"
        locale, profile = entry["locale"], entry["profile"]
        assert f"type={profile}" in source
        assert f"document-language={locale}" in source
        assert "\\ufcsetup{\n  type=" in source
        assert "\\ufcsetup{\n\n" not in source
        assert "\n\n}\n" not in source
        assert fr"\input{{artifacts/canonical-mesh-study/body-{locale}.tex}}" in source
        assert r"\ufcAddBibliographyResource{examples/canonical-mesh-study/references.bib}" in source
        assert source.count(r"\section{") == 5
        assert r"\ufcPrintReferences" in source
        assert content["profile_context"][profile][locale] in source
        assert content["locales"][locale]["introduction"] in source
        assert not any(b.casefold() in source.casefold() for b in BAD)
        if profile in {"research-project", "anonymized-research-project"}:
            assert r"\ufcPrintApprovalPage" not in source
            assert content["locales"][locale]["proposal_conclusion"] in source
        elif profile == "scientific-article":
            assert r"\ufcPrintArticleFrontMatter" in source
            assert r"\ufcPrintTableOfContents" not in source
        else:
            assert r"\ufcPrintApprovalPage" in source
            assert r"\ufcPrintRequiredSummaries" in source
        if profile == "anonymized-research-project":
            assert "author={}" in source
            assert r"\ufcPrintCover" not in source
        for key, value in entry["support"].items():
            p = ROOT / key
            assert p.is_relative_to(OUT)
            assert sha(p.read_bytes()) == value
            paths.add(str(p))
    assert all(entry["source"].startswith("artifacts/public-mesh-documents/")
               for entry in entries)
    assert len(paths) == 60, len(paths)
    generated = {str(p) for p in OUT.rglob("*") if p.is_file()}
    assert generated == paths | {str(OUT / "manifest.json")}
    subprocess.run([sys.executable, str(GENERATOR), "--check"], cwd=ROOT, check=True)

    # Deliberately corrupt one generated TeX source and demand fail-closed behavior.
    target = OUT / "pt" / "undergraduate-capstone.tex"
    original = target.read_bytes()
    try:
        target.write_bytes(original + b"\n% Unexpected changed source\n")
        corrupted = subprocess.run(
            [sys.executable, str(GENERATOR), "--check"],
            cwd=ROOT, capture_output=True, text=True,
        )
        assert corrupted.returncode != 0, "Changed generated source was accepted"
        assert "PUBLIC-EXAMPLES-FAIL" in corrupted.stdout + corrupted.stderr
    finally:
        target.write_bytes(original)
    subprocess.run([sys.executable, str(GENERATOR), "--check"], cwd=ROOT, check=True)
    print("PUBLIC-ACADEMIC-EXAMPLES status=PASS sources=28 support=32 "
          "languages=4 profiles=7 negative_mutants=1 pdf_certification=NOT_CHECKED")


if __name__ == "__main__":
    check()
