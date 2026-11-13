#!/usr/bin/env python3
"""Inspect the original immutable R8.1 PDFs page by page for table-row isolation.

This is a diagnostic, not automated normative or human visual acceptance.
"""
from __future__ import annotations

import hashlib
import json
import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
INPUT = ROOT / "artifacts/r81-original-audit/downloads"
OUTPUT = ROOT / "artifacts/r81-original-audit"
SOURCE_SHA = "a4a4665ce099d0786e92e443b95dab656b25afad"
LOCALES = {
    "pt": {"abnt": "Execução", "native": "Amostra", "header": "Caso"},
    "en": {"abnt": "Run", "native": "Sample", "header": "Case"},
    "es": {"abnt": "Ejecución", "native": "Muestra", "header": "Caso"},
    "fr": {"abnt": "Exécution", "native": "Échantillon", "header": "Cas"},
}
ROW_COUNTS = {"abnt": 125, "native": 85}


def command(*args: str) -> str:
    result = subprocess.run(args, text=True, capture_output=True, check=False)
    if result.returncode:
        raise RuntimeError(f"{args}: {result.stderr[-2000:]}")
    return result.stdout


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def pdf_pages(path: Path) -> list[str]:
    text = command("pdftotext", "-layout", str(path), "-")
    pages = text.split("\f")
    if pages and not pages[-1]:
        pages.pop()
    return pages


def inspect_rows(pages: list[str], token: str, count: int) -> dict:
    # The source generator writes "<localized row prefix> <number>".
    pattern = re.compile(r"(?<!\w)" + re.escape(token)
                         + r"\s+([1-9]\d{0,2})(?!\d)", re.I)
    row_pages: dict[int, list[int]] = {}
    for pno, page in enumerate(pages, 1):
        for match in pattern.finditer(page):
            value = int(match.group(1))
            if 1 <= value <= count:
                row_pages.setdefault(value, []).append(pno)
    missing = sorted(set(range(1, count + 1)) - row_pages.keys())
    duplicate = {str(value): positions for value, positions in row_pages.items()
                 if len(positions) != 1}
    final_page = row_pages.get(count, [None])[0]
    rows_on_final = sorted(value for value, positions in row_pages.items()
                           if final_page in positions) if final_page else []
    sample = []
    if final_page is not None:
        lines = [line.strip() for line in pages[final_page - 1].splitlines()
                 if line.strip()]
        sample = (lines[:9] + ["..."] + lines[-9:]) if len(lines) > 18 else lines
    return {
        "expected_rows": count,
        "found_unique_rows": len(row_pages),
        "missing_rows": missing,
        "duplicated_rows": duplicate,
        "last_row_page": final_page,
        "rows_on_last_table_page": rows_on_final,
        "last_page_row_count": len(rows_on_final),
        "single_row_on_last_table_page": len(rows_on_final) == 1,
        "last_page_text_excerpt": sample,
    }


def main() -> None:
    report = {
        "source_sha": SOURCE_SHA,
        "original_run": 43452221682,
        "classification": "PAGE_GEOMETRY_CANDIDATE_NOT_NORMATIVE_VERDICT",
        "documents": [],
    }
    failures = []
    total_pages = 0
    for locale, names in LOCALES.items():
        folder = INPUT / locale
        manifests = list(folder.rglob("review-pdfs.json"))
        if len(manifests) != 1:
            raise RuntimeError(f"{locale}: expected one manifest, got {len(manifests)}")
        manifest = json.loads(manifests[0].read_text(encoding="utf-8"))
        entries = manifest["documents"]
        if manifest.get("source_commit_sha") != SOURCE_SHA:
            raise RuntimeError(f"{locale}: original run source SHA mismatch")
        if len(entries) != 7:
            raise RuntimeError(f"{locale}: expected 7 PDFs, got {len(entries)}")
        pdfs = list(folder.rglob("*.pdf"))
        for item in entries:
            filename = Path(item["pdf"]).name
            candidates = [p for p in pdfs if p.name == filename]
            if len(candidates) != 1:
                raise RuntimeError(f"{locale}/{filename}: found {len(candidates)} PDFs")
            pdf = candidates[0]
            actual_sha = sha256(pdf)
            if actual_sha != item["pdf_sha256"]:
                raise RuntimeError(f"{locale}/{filename}: PDF SHA-256 mismatch")
            pages = pdf_pages(pdf)
            expected_page_count = item["pages"]
            if len(pages) != expected_page_count:
                raise RuntimeError(f"{locale}/{filename}: wrong physical page count "
                                   f"{len(pages)} != {expected_page_count}")
            total_pages += len(pages)
            measurements = {}
            for family, count in ROW_COUNTS.items():
                measurements[family] = inspect_rows(pages, names[family], count)
                if measurements[family]["missing_rows"] or \
                        measurements[family]["duplicated_rows"]:
                    failures.append(f"{locale}/{item['profile']}/{family}: "
                                    "row extraction incomplete (requires inspection)")
            record = {
                "locale": locale,
                "profile": item["profile"],
                "pdf_sha256": actual_sha,
                "pages": len(pages),
                "tables": measurements,
                "human_review": "PENDING",
            }
            report["documents"].append(record)
            print("R81-ORIGINAL "
                  f"{locale}/{item['profile']} pages={len(pages)} "
                  f"abnt_last_page={measurements['abnt']['last_row_page']} "
                  f"abnt_rows={measurements['abnt']['last_page_row_count']} "
                  f"native_last_page={measurements['native']['last_row_page']} "
                  f"native_rows={measurements['native']['last_page_row_count']}",
                  flush=True)
    if len(report["documents"]) != 28 or total_pages != 984:
        raise RuntimeError(f"R8.1 corpus mismatch: {len(report['documents'])} PDFs, "
                           f"{total_pages} pages")
    summary = {}
    for family in ROW_COUNTS:
        candidates = [f"{d['locale']}/{d['profile']}"
                      for d in report["documents"]
                      if d["tables"][family]["single_row_on_last_table_page"]]
        summary[family] = {"single_last_row_candidates": len(candidates),
                           "documents": candidates}
    report["summary"] = summary
    report["page_total"] = total_pages
    report["row_extraction_findings"] = failures
    OUTPUT.mkdir(parents=True, exist_ok=True)
    (OUTPUT / "original-audit.json").write_text(
        json.dumps(report, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print("R81-ORIGINAL-SUMMARY " + json.dumps(summary, ensure_ascii=False),
          flush=True)
    if failures:
        print("R81-ORIGINAL-WARNINGS " + json.dumps(failures, ensure_ascii=False),
              flush=True)


if __name__ == "__main__":
    main()
