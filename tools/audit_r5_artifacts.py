#!/usr/bin/env python3
"""Source-bound R5 PDF audit: inspection never authorizes a release."""

from __future__ import annotations

import argparse
import csv
import hashlib
import json
import re
import zipfile
from pathlib import Path

try:
    import fitz
except ImportError as exc:
    raise SystemExit("Install PyMuPDF: python3 -m pip install pymupdf") from exc

LOCALES = {"pt", "en", "es", "fr"}
MARKERS = (
    "INTEGRATED MULTILINGUAL DOCUMENT",
    "INTEGRATED TEST AUTHOR",
    "INTEGRATED-MANUSCRIPT-",
    "R4-METHOD-",
    "R4SHORT-",
)
VALID_REVIEW = {"ACCEPT", "NEEDS_CHANGES", "REJECT"}


def require(condition: bool, message: str) -> None:
    if not condition:
        raise ValueError(message)


def digest(blob: bytes) -> str:
    return hashlib.sha256(blob).hexdigest()


def sources_by_filename(index: dict) -> dict:
    found = {}
    for main in index["entries"]:
        found[main["name"] + ".pdf"] = main
        for item in main.get("supplementary_variants", []):
            found[item["name"] + ".pdf"] = {
                **item, "features": main.get("features", {})
            }
    require(len(found) == 8, "Expected exactly seven baseline and one supplemental source")
    return found


def receipts_by_filename(receipts: dict, locale: str) -> dict:
    found = {}
    for entry in receipts["entries"]:
        profile = ("doctoral-code-lists"
                   if entry["specimen_kind"] == "supplementary-doctoral-code-lists"
                   else entry["profile"])
        filename = f"comprehensive-{profile}-{locale}.pdf"
        require(filename not in found, f"Duplicate receipt: {filename}")
        found[filename] = entry
    require(len(found) == 8, "Expected eight real-PDF receipts per locale")
    return found


def physical_page(page, page_number: int, duplex: bool) -> dict:
    text = page.get_text("text").strip()
    no_objects = not page.get_images(full=True) and not page.get_drawings()
    white = None
    if not text and no_objects:
        pix = page.get_pixmap(matrix=fitz.Matrix(0.33, 0.33),
                              colorspace=fitz.csGRAY, alpha=False)
        white = min(pix.samples) >= 250
    blank = not text and no_objects and white is True
    number_only = bool(re.fullmatch(r"\d{1,5}", text))
    if blank and duplex and page_number > 1 and page_number % 2 == 1:
        classification = "DUPLEX_VERSO_CANDIDATE"
    elif blank:
        classification = "UNEXPLAINED_BLANK"
    elif number_only:
        classification = "NUMBER_ONLY"
    elif not text:
        classification = "NO_EXTRACTABLE_TEXT"
    else:
        classification = "CONTENT"
    return {
        "physical_page": page_number,
        "classification": classification,
        "a4": (abs(page.rect.width - 595.276) < 1
               and abs(page.rect.height - 841.89) < 1),
        "text_characters": len(text),
        "white_raster": white,
        "preview": re.sub(r"\s+", " ", text)[:110],
        "review_status": "PENDING",
        "normative_justification": "",
    }


def audit_zip(path: Path) -> dict:
    with zipfile.ZipFile(path) as archive:
        names = set(archive.namelist())
        require({"source-index.json", "pdf-receipts.json"} <= names,
                f"{path}: missing source-index or PDF receipts")
        index = json.loads(archive.read("source-index.json"))
        record = json.loads(archive.read("pdf-receipts.json"))
        locale = index["locale"]
        require(locale in LOCALES and locale == record["locale"],
                f"{path}: mismatched locale")
        require(record.get("source_commit_sha"), "Missing source commit SHA")
        require(record.get("release_authorized") is False,
                "CI may not authorize a publication")
        sources = sources_by_filename(index)
        receipts = receipts_by_filename(record, locale)
        pdf_set = {n.removeprefix("build/") for n in names
                   if n.startswith("build/") and n.endswith(".pdf")}
        require(set(sources) == set(receipts) == pdf_set,
                f"{path}: missing or unexpected PDF/receipt/source")
        results = []
        for filename in sorted(sources):
            source = sources[filename]
            receipt = receipts[filename]
            pdf_bytes = archive.read("build/" + filename)
            sha = digest(pdf_bytes)
            require(sha == receipt["pdf_sha256"], f"{filename}: PDF SHA mismatch")
            require(source["source_sha256"] == receipt["source_sha256"],
                    f"{filename}: TeX source SHA mismatch")
            doc = fitz.open(stream=pdf_bytes, filetype="pdf")
            require(len(doc) == receipt["pages"], f"{filename}: page count mismatch")
            duplex = bool(source.get("features", {}).get("duplex", False))
            pages = [physical_page(page, number, duplex)
                     for number, page in enumerate(doc, 1)]
            require(all(page["a4"] for page in pages), f"{filename}: non-A4 leaf")
            textless = [page["physical_page"] for page in pages
                        if not page["text_characters"]]
            require(textless == receipt["blank_physical_pages"],
                    f"{filename}: independently observed textless leaves differ from CI")
            require(receipt["human_page_by_page_review"] == "PENDING",
                    f"{filename}: CI falsely claims a human review")
            if source["profile"] == "anonymized-research-project":
                require(not doc.metadata.get("author", "").strip(),
                        f"{filename}: anonymous author leaked in PDF Info")
            markers = sorted({marker for marker in MARKERS
                              if any(marker.casefold() in page.get_text().casefold()
                                     for page in doc)})
            results.append({
                "pdf": filename, "profile": source["profile"], "locale": locale,
                "sha256": sha, "source_sha256": source["source_sha256"],
                "source_commit_sha": record["source_commit_sha"],
                "duplex": duplex, "synthetic_markers": markers,
                "pages": pages,
            })
    return {"locale": locale, "commit": record["source_commit_sha"], "documents": results}


def compile_inventory(paths: list[Path]) -> dict:
    require(len(paths) == 4, "Exactly four original artifact ZIPs required")
    sources = [audit_zip(path) for path in paths]
    require({entry["locale"] for entry in sources} == LOCALES,
            "Exactly PT/EN/ES/FR required")
    require(len({entry["commit"] for entry in sources}) == 1,
            "Cannot combine artifacts from different commits")
    documents = sorted((document for entry in sources
                        for document in entry["documents"]),
                       key=lambda item: (item["locale"], item["pdf"]))
    pages = [page for document in documents for page in document["pages"]]
    counts = {kind: sum(page["classification"] == kind for page in pages)
              for kind in ("DUPLEX_VERSO_CANDIDATE", "UNEXPLAINED_BLANK",
                           "NUMBER_ONLY", "NO_EXTRACTABLE_TEXT")}
    return {
        "source_commit_sha": sources[0]["commit"],
        "pdfs": len(documents), "pages": len(pages),
        "classification_counts": counts,
        "human_review": "PENDING", "publication_authorized": False,
        "documents": documents,
    }


def review_problems(inventory: dict, reviews: dict) -> list[str]:
    """A review must bind each page to the exact binary and approve it explicitly."""
    errors = []
    if reviews.get("source_commit_sha") != inventory["source_commit_sha"]:
        errors.append("review_commit_mismatch")
    if not reviews.get("reviewer", "").strip():
        errors.append("human_reviewer_missing")
    entries = reviews.get("documents", {})
    for document in inventory["documents"]:
        answer = entries.get(document["pdf"], {})
        if answer.get("sha256") != document["sha256"]:
            errors.append(document["pdf"] + ":review_pdf_sha_mismatch")
        page_answers = answer.get("pages", {})
        for page in document["pages"]:
            num = str(page["physical_page"])
            review = page_answers.get(num, {})
            state = review.get("status")
            if state not in VALID_REVIEW:
                errors.append(f"{document['pdf']}:{num}:not_reviewed")
            elif state != "ACCEPT":
                errors.append(f"{document['pdf']}:{num}:not_accepted")
            if page["classification"] in {"DUPLEX_VERSO_CANDIDATE", "UNEXPLAINED_BLANK"}:
                if not review.get("normative_justification", "").strip():
                    errors.append(f"{document['pdf']}:{num}:blank_without_normative_basis")
    return errors


def self_test() -> None:
    """Verify that unexplained pages, false approval and rejected pages fail closed."""
    doc = fitz.open()
    doc.new_page(width=595.276, height=841.89)
    empty = physical_page(doc[0], 3, True)
    require(empty["classification"] == "DUPLEX_VERSO_CANDIDATE",
            "Blank duplex verso not detected")
    require(physical_page(doc[0], 2, True)["classification"] == "UNEXPLAINED_BLANK",
            "Unexpected blank was not detected")
    doc[0].insert_text((72, 72), "123")
    require(physical_page(doc[0], 3, True)["classification"] == "NUMBER_ONLY",
            "Number-only page was not detected")
    sample = {"source_commit_sha": "abc", "documents": [
        {"pdf": "x.pdf", "sha256": "def", "pages": [
            {"physical_page": 1, "classification": "CONTENT"},
            {"physical_page": 2, "classification": "UNEXPLAINED_BLANK"},
        ]}
    ]}
    reviews = {"source_commit_sha": "abc", "reviewer": "Reviewer", "documents": {
        "x.pdf": {"sha256": "def", "pages": {
            "1": {"status": "REJECT"}, "2": {"status": "ACCEPT"}
        }}
    }}
    errors = review_problems(sample, reviews)
    require(any("not_accepted" in error for error in errors),
            "A rejected page could pass the gate")
    require(any("blank_without_normative_basis" in error for error in errors),
            "A blank page without justification could pass")
    reviews["documents"]["x.pdf"]["sha256"] = "tampered"
    require(any("review_pdf_sha_mismatch" in error
                for error in review_problems(sample, reviews)),
            "Stale PDF hash was not detected")
    print("R5-AUDIT-SELFTEST status=PASS cases=6 release_authorized=false")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--artifact", type=Path, action="append",
                        help="Original, unmodified CI artifact ZIP; use four")
    parser.add_argument("--output", type=Path)
    parser.add_argument("--reviews", type=Path,
                        help="Independent page-by-page human review JSON")
    parser.add_argument("--require-r5-approval", action="store_true",
                        help="Fail without accepted pages, justifications and non-synthetic publication content")
    args = parser.parse_args()
    if args.self_test:
        self_test()
        return
    require(args.artifact is not None and args.output is not None,
            "--artifact x4 and --output are required")
    inventory = compile_inventory(args.artifact)
    args.output.mkdir(parents=True, exist_ok=True)
    (args.output / "inventory.json").write_text(
        json.dumps(inventory, ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    with (args.output / "pages.csv").open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle)
        writer.writerow(["locale", "pdf", "pdf_sha256", "page", "classification",
                         "a4", "characters", "review_status", "normative_justification"])
        for document in inventory["documents"]:
            for page in document["pages"]:
                writer.writerow([document["locale"], document["pdf"],
                                 document["sha256"], page["physical_page"],
                                 page["classification"], page["a4"],
                                 page["text_characters"], page["review_status"],
                                 page["normative_justification"]])
    errors = []
    if args.reviews:
        reviews = json.loads(args.reviews.read_text(encoding="utf-8"))
        errors += review_problems(inventory, reviews)
    if args.require_r5_approval:
        if not args.reviews:
            errors.append("independent_human_reviews_required")
        errors += [document["pdf"] + ":synthetic_test_fixture"
                   for document in inventory["documents"]
                   if document["synthetic_markers"]]
        if any(inventory["classification_counts"][key] for key in
               ("UNEXPLAINED_BLANK", "NUMBER_ONLY", "NO_EXTRACTABLE_TEXT")):
            errors.append("unexpected_or_unexplained_page")
    (args.output / "gate.json").write_text(json.dumps({
        "status": "BLOCKED" if errors or not args.require_r5_approval else "R5_REVIEW_RECORDED",
        "problems": errors, "publication_authorized": False
    }, indent=2) + "\n", encoding="utf-8")
    print("R5-AUDIT-EVIDENCE "
          f"pdfs={inventory['pdfs']} pages={inventory['pages']} "
          f"classifications={inventory['classification_counts']} "
          "human_review=PENDING publication_authorized=false")
    if errors:
        raise SystemExit("R5-AUDIT-BLOCKED: " + "; ".join(errors[:12]))


if __name__ == "__main__":
    main()
