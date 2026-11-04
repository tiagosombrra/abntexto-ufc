#!/usr/bin/env python3
"""Strict actual-PDF content regression gate for 7 profiles x 4 locales.

The self-test uses failure mutants, not merely happy-path compilation.
An empty or short smoke document cannot satisfy this gate. Passing this gate
still does not establish expert linguistic, institutional, PDF/A or PDF/UA approval.
"""

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tempfile
from collections import Counter
from pathlib import Path
from zipfile import ZipFile

LOCALES = ("pt", "en", "es", "fr")
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
TABLE_HEADINGS = {
    "pt": "LISTA DE TABELAS", "en": "LIST OF TABLES",
    "es": "LISTA DE TABLAS", "fr": "LISTE DES TABLEAUX",
}
TABLE_LABELS = {"pt": "Tabela", "en": "Table", "es": "Tabla", "fr": "Tableau"}


def table_list_failures(text, locale):
    """Require two consistently prefixed, sequential entries in the printed list."""
    if locale not in LOCALES:
        raise ValueError("unsupported locale")
    label = re.compile(r"^" + re.escape(TABLE_LABELS[locale]) + r"\s+(\d+)\b", re.I)
    any_label = re.compile(r"^(?:Table|Tabela|Tabla|Tableau)\s+\d+\b", re.I)
    bare = re.compile(r"^\d+\s+\S")
    rows = [x.strip() for x in text.replace("\xa0", " ").splitlines() if x.strip()]
    valid = [label.match(line) for line in rows if label.match(line)]
    bad = [line for line in rows if bare.match(line)
           or (any_label.match(line) and not label.match(line))]
    failures = []
    if len(valid) < 2:
        failures.append("table_list.fewer_than_two_entries")
    if bad:
        failures.append("table_list.mixed_or_bare_prefix")
    if valid and [int(x.group(1)) for x in valid[:2]] != [1, 2]:
        failures.append("table_list.nonsequential")
    return failures


def pdf_failures(info, pages, tex, locale, profile):
    """Inspect rendered PDF text and declared source features without guessing."""
    findings = []
    if not info.get("Title"):
        findings.append("metadata.title_empty")
    if profile != "anonymized-research-project" and not info.get("Author"):
        findings.append("metadata.author_empty")
    if profile == "anonymized-research-project" and info.get("Author"):
        findings.append("privacy.anonymous_author_leak")
    if any(re.fullmatch(r"\s*\d+\s*", page) for page in pages):
        findings.append("pagination.orphan_number_only")
    for code, test in (
        ("section.subsection_missing", r"\subsection{"),
        ("section.subsubsection_missing", r"\subsubsection{"),
        ("table.multipage_missing", r"\begin{longtable}"),
        ("algorithm.missing", r"\begin{ufcalgorithm}"),
        ("code.missing", r"\begin{ufclisting}"),
    ):
        if test not in tex:
            if code == "table.multipage_missing" and r"\begin{longabnttblr}" in tex:
                continue
            if code == "code.missing" and r"\ufcInputListing" in tex:
                continue
            findings.append(code)
    if profile != "scientific-article":
        section = next((page for page in pages
                        if TABLE_HEADINGS[locale] in page.upper()), "")
        if not section:
            findings.append("table_list.missing")
        else:
            findings += table_list_failures(section, locale)
    return sorted(set(findings))


def mutant_selftest():
    """Every historical failure must make the corresponding checker fail."""
    good = "LIST OF TABLES\nTable 1 — Initial result........10\nTable 2 — Long result........20"
    missing = "LIST OF TABLES\nTable 1 — Initial result........10"
    bare = "LIST OF TABLES\nTable 1 — Initial result........10\n2 Long result........20"
    assert not table_list_failures(good, "en")
    assert "table_list.fewer_than_two_entries" in table_list_failures(missing, "en")
    assert "table_list.mixed_or_bare_prefix" in table_list_failures(bare, "en")
    assert "pagination.orphan_number_only" in pdf_failures(
        {"Title": "Example", "Author": "Someone"},
        ["LIST OF TABLES\n" + good, "60\n"],
        r"\subsection{A}\subsubsection{B}\begin{longtable}\begin{ufcalgorithm}\begin{ufclisting}",
        "en", "doctoral-thesis",
    )
    assert "metadata.title_empty" in pdf_failures(
        {"Author": "Someone"}, [good], "", "en", "scientific-article",
    )
    assert "privacy.anonymous_author_leak" in pdf_failures(
        {"Title": "A", "Author": "Should be hidden"}, [good], "",
        "en", "anonymized-research-project",
    )


def extract_pdf_bytes(pdf):
    """Use the real Poppler tools already installed in the CI TeX image."""
    with tempfile.TemporaryDirectory() as tmp:
        path = Path(tmp) / "candidate.pdf"
        path.write_bytes(pdf)
        info = subprocess.run(["pdfinfo", str(path)], capture_output=True,
                              check=True, text=True).stdout
        text = subprocess.run(["pdftotext", "-layout", str(path), "-"],
                              capture_output=True, check=True, text=True).stdout
    metadata = dict(line.split(":", 1) for line in info.splitlines() if ":" in line)
    return {k.strip(): v.strip() for k, v in metadata.items()}, text.split("\f")


def audit(archive_dir, template):
    results = []
    for locale in LOCALES:
        path = archive_dir / template.format(locale=locale)
        with ZipFile(path) as source:
            m = json.loads(source.read("manifest.json"))
            if m.get("locale") != locale or len(m.get("entries", [])) != 7:
                raise ValueError("bad source-bound seven-profile manifest " + str(path))
            for profile in PROFILES:
                prefix = "integrated-" + profile + "-" + locale
                pdf = source.read(prefix + ".pdf")
                tex = source.read(prefix + ".tex").decode("utf-8")
                item = next(x for x in m["entries"] if x["profile"] == profile)
                digest = hashlib.sha256(pdf).hexdigest()
                if item["pdf_sha256"] != digest:
                    raise ValueError("PDF sha256 mismatch " + prefix)
                info, pages = extract_pdf_bytes(pdf)
                failures = pdf_failures(info, pages, tex, locale, profile)
                results.append({
                    "locale": locale, "profile": profile, "source_sha": m["source_sha"],
                    "pdf_sha256": digest, "pages": int(info.get("Pages", "0")),
                    "failures": failures, "human_accepted": False,
                })
    if len(results) != 28:
        raise ValueError("expected exactly 28 independent PDFs")
    return {
        "scope": "Necessary actual-PDF/source content predicates, NOT editorial acceptance",
        "total": len(results), "failed": sum(bool(r["failures"]) for r in results),
        "counts": dict(Counter(f for r in results for f in r["failures"])),
        "items": results,
    }


def main():
    p = argparse.ArgumentParser()
    p.add_argument("--selftest", action="store_true")
    p.add_argument("--archive-dir", type=Path)
    p.add_argument("--zip-template", default="integrated-{locale}.zip")
    p.add_argument("--report", type=Path)
    p.add_argument("--strict", action="store_true")
    a = p.parse_args()
    mutant_selftest()
    if a.selftest and a.archive_dir is None:
        print("COMPREHENSIVE-PDF-MUTANT-EVIDENCE status=PASS")
        return 0
    if a.archive_dir is None:
        p.error("--archive-dir is required for actual-PDF certification")
    r = audit(a.archive_dir, a.zip_template)
    if a.report:
        a.report.write_text(json.dumps(r, indent=2, ensure_ascii=False) + "\n")
    print("COMPREHENSIVE-PDF-EVIDENCE checked=%d failed=%d" % (r["total"], r["failed"]))
    print(json.dumps(r["counts"], indent=2))
    return 1 if a.strict and r["failed"] else 0


if __name__ == "__main__":
    sys.exit(main())
