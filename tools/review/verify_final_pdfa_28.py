#!/usr/bin/env python3
"""Fail-closed PDF/A-2b certification of 28 final R8.1 PDF artifacts."""
import hashlib
import json
import os
import pathlib
import re
import shutil
import subprocess
import sys
import xml.etree.ElementTree as ET

# Development evidence must never overwrite R8.1 historical approval receipts.
SCOPE = os.environ.get("R81_PDFA_SCOPE", "historical")
ROOT = pathlib.Path("artifacts/r5-development-pdfa"
                    if SCOPE == "development" else "artifacts/r5-final-pdfa")
PDFS = ROOT / "pdfs"
PROFILES = {
    "undergraduate-capstone", "specialization-capstone",
    "masters-thesis", "doctoral-thesis", "research-project",
    "anonymized-research-project", "scientific-article",
}
LOCALES = ("pt", "en", "es", "fr")


def require(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha256(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def prepare():
    require(SCOPE in ("historical", "development"), "Unknown PDF/A evidence scope")
    expected_sha = os.environ["SOURCE_COMMIT_SHA"]
    run = os.environ["GITHUB_RUN_ID"]
    require(re.fullmatch(r"[0-9a-f]{40}", expected_sha) is not None,
            "Invalid source commit SHA")
    PDFS.mkdir(parents=True, exist_ok=True)
    files = []
    for loc in LOCALES:
        directory = ROOT / "source" / loc / "human-readable-28" / loc
        report = json.loads((directory / "review-pdfs.json").read_text("utf-8"))
        sources = json.loads((directory / "review-sources.json").read_text("utf-8"))
        require(report["locale"] == loc and sources["locale"] == loc,
                f"{loc}: locale mismatch")
        require(report["source_commit_sha"] == expected_sha,
                f"{loc}: missing or wrong SHA-bound source receipt")
        expected_locale_pages = (246 if SCOPE == "historical" or loc in ("pt", "fr")
                                 else 240)
        require(report["pdf_count"] == 7
                and report["page_count"] == expected_locale_pages,
                f"{loc}: wrong document/page count")
        require(report["failures"] == 0 and report["human_approval"] == "PENDING"
                and report["release_authorized"] is False,
                f"{loc}: illegal approval status")
        require(sources["expected_pdf_count"] == 7
                and sources["human_approval"] == "PENDING",
                f"{loc}: source manifest mismatch")
        by_profile = {x["profile"]: x for x in sources["entries"]}
        documents = report["documents"]
        require(len(documents) == 7 and len(by_profile) == 7
                and {x["profile"] for x in documents} == PROFILES
                and set(by_profile) == PROFILES,
                f"{loc}: incomplete profile matrix")
        for doc in documents:
            profile = doc["profile"]
            src = by_profile[profile]
            require(doc["locale"] == loc and src["locale"] == loc
                    and doc["failures"] == []
                    and doc["human_visual_approval"] == "PENDING",
                    f"{loc}/{profile}: invalid document receipt")
            name = f"review-{profile}-{loc}.pdf"
            require(pathlib.Path(doc["pdf"]).name == name,
                    f"{loc}/{profile}: unexpected PDF name")
            pdf = directory / name
            tex = directory / f"review-{profile}-{loc}.tex"
            require(pdf.is_file() and tex.is_file(),
                    f"{loc}/{profile}: missing PDF or source")
            require(pathlib.Path(src["source"]).name == tex.name
                    and sha256(tex) == src["source_sha256"] == doc["source_sha256"],
                    f"{loc}/{profile}: source hash mismatch")
            require(sha256(pdf) == doc["pdf_sha256"],
                    f"{loc}/{profile}: PDF binary was altered")
            info = subprocess.check_output(
                ["pdfinfo", str(pdf)], text=True, errors="replace")
            match = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
            require(match is not None and int(match.group(1)) == doc["pages"],
                    f"{loc}/{profile}: actual page count mismatches receipt")
            shutil.copyfile(pdf, PDFS / name)
            files.append({
                "filename": name, "profile": profile, "locale": loc,
                "pages": doc["pages"],
                "pdf_sha256": sha256(pdf),
                "tex_sha256": sha256(tex),
                "source_commit_sha": expected_sha,
            })
    require(len(files) == 28 and len({x["filename"] for x in files}) == 28,
            "Missing or duplicate PDF")
    expected_total_pages = 984 if SCOPE == "historical" else 972
    require(sum(x["pages"] for x in files) == expected_total_pages,
            f"R8.1 input page count differs from the {expected_total_pages}-page source")
    require(len(list(PDFS.glob("*.pdf"))) == 28, "Unexpected PDF in validator input")
    manifest = {
        "source_run": run, "source_commit_sha": expected_sha,
        "source_class_git_blob": subprocess.check_output(
            ["git", "hash-object", "abntexto-ufc.cls"], text=True).strip(),
        "expected_profile": "PDF/A-2b", "documents": files,
        "pdf_count": 28, "page_count": expected_total_pages,
        "human_review": "PENDING", "publication_authorized": False,
        "status": "PDF_A_EXTERNAL_PENDING",
    }
    if SCOPE == "development":
        # This validates a new runtime, never the older approved R8.1 class.
        actual_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD"], text=True).strip()
        class_at_commit = subprocess.check_output(
            ["git", "rev-parse", "HEAD:abntexto-ufc.cls"], text=True).strip()
        require(os.environ.get("GITHUB_EVENT_NAME") == "pull_request",
                "Development PDF/A evidence requires a pull request")
        require(actual_commit == expected_sha
                and manifest["source_class_git_blob"] == class_at_commit,
                "Development PDF/A source/class provenance mismatch")
        require(class_at_commit == "299293e273dcefb80256eed2e17d2557db6aae52",
                "Development PDF/A source class changed; requalification required")
        manifest["certification_scope"] = "DEVELOPMENT_UNRELEASED_ONLY"
    else:
        require(manifest["source_class_git_blob"]
                == "a73ef656de71d38ad30d7029ac3d86f852339950",
                "R8.1 accepted class has changed; re-approval required")
        manifest["certification_scope"] = "HISTORICAL_R8_1_CLASS_ONLY"
    (ROOT / "input-manifest.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    label = "DEVELOPMENT" if SCOPE == "development" else "FINAL"
    print(f"R81-{label}-PDFA-SOURCE status=PASS pdfs=28 pages={expected_total_pages} "
          + "source_sha=" + expected_sha
          + " human_review=PENDING publication_authorized=false", flush=True)


def verify():
    require(SCOPE in ("historical", "development"), "Unknown PDF/A evidence scope")
    manifest = json.loads((ROOT / "input-manifest.json").read_text("utf-8"))
    expected_scope = ("DEVELOPMENT_UNRELEASED_ONLY" if SCOPE == "development"
                      else "HISTORICAL_R8_1_CLASS_ONLY")
    require(manifest.get("certification_scope") == expected_scope,
            "PDF/A evidence scope mismatch")
    documents = {x["filename"]: x for x in manifest["documents"]}
    require(len(documents) == 28, "Invalid input count")
    for name, doc in documents.items():
        require(sha256(PDFS / name) == doc["pdf_sha256"],
                "Validator input hash mismatch: " + name)
    xml = ET.parse(ROOT / "verapdf-raw.xml").getroot()
    for entry in xml.iter():
        if "}" in entry.tag:
            entry.tag = entry.tag.rsplit("}", 1)[-1]
    require(xml.tag == "rawResults", "Unexpected veraPDF root")
    config = xml.find("processorConfig/validatorConfig")
    require(config is not None and config.get("flavour") == "PDFA_2_B",
            "Validator did not select PDF/A-2b")
    nodes = [x for x in xml if x.tag not in ("processorConfig", "batchSummary")]
    require(len(nodes) == 56, "Expected precisely 28 paired reports")
    results = {}
    for i in range(0, 56, 2):
        item, result = nodes[i:i + 2]
        require(item.tag == "item" and result.tag == "validationResult",
                "Invalid veraPDF pair")
        label = item.findtext("name")
        require(bool(label), "Missing validator input path")
        name = pathlib.PurePosixPath(label).name
        require(name in documents and name not in results,
                "Unexpected or repeated validation: " + name)
        require(result.get("flavour") == "PDFA_2_B"
                and result.get("jobEndStatus") == "NORMAL",
                "Wrong validator profile/status for " + name)
        compliant = result.get("isCompliant")
        require(compliant in ("true", "false"), "Invalid compliance result")
        assertions = result.find("assertions")
        require(assertions is not None, "Missing rule assertions")
        failures = [
            {
                "element": node.tag, "attributes": node.attrib,
                "description": " ".join(node.itertext()).strip()[:1000],
            }
            for node in assertions
        ]
        require(compliant != "true" or not failures,
                "Contradictory validation for " + name)
        results[name] = {
            "pdfa_2b_compliant": compliant == "true",
            "failed_rules": failures,
            "assertion_count": result.get("totalAssertions"),
        }
    batch = xml.find("batchSummary")
    require(batch is not None, "Missing batch summary")
    for field in ("failedToParse", "encrypted", "outOfMemory", "veraExceptions"):
        require(batch.get(field) == "0", "Validator runtime error: " + field)
    total = batch.find("validationReports")
    compliant_count = sum(x["pdfa_2b_compliant"] for x in results.values())
    require(total is not None
            and int(total.get("compliant", "-1")) == compliant_count
            and int(total.get("nonCompliant", "-1")) == 28 - compliant_count,
            "Contradictory batch totals")
    for doc in manifest["documents"]:
        doc["verapdf"] = results[doc["filename"]]
    manifest.update({
        "validator": "veraPDF official CLI Docker",
        "validator_image_digests": json.loads(
            (ROOT / "validator-image-digests.json").read_text("utf-8")),
        "pdfa_2b_compliant": compliant_count,
        "pdfa_2b_noncompliant": 28 - compliant_count,
        "human_review": "PENDING", "publication_authorized": False,
        "status": (("PASS_DEVELOPMENT_EXTERNAL_PDF_A_2B"
                    if compliant_count == 28
                    else "BLOCKED_DEVELOPMENT_EXTERNAL_PDF_A_2B")
                   if SCOPE == "development"
                   else ("PASS_EXTERNAL_PDF_A_2B" if compliant_count == 28
                         else "BLOCKED_EXTERNAL_PDF_A_2B")),
    })
    (ROOT / "results.json").write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", "utf-8")
    print(("R81-DEVELOPMENT-PDFA-EVIDENCE" if SCOPE == "development"
           else "R81-FINAL-PDFA-EVIDENCE")
          + " status=" + manifest["status"]
          + f" compliant={compliant_count} noncompliant={28-compliant_count}"
          + " human_review=PENDING publication_authorized=false",
          flush=True)
    require(compliant_count == 28, "Noncompliant final PDF/A-2b document(s)")


if __name__ == "__main__":
    require(len(sys.argv) == 2 and sys.argv[1] in ("prepare", "verify"),
            "Usage: verify_final_pdfa_28.py prepare|verify")
    {"prepare": prepare, "verify": verify}[sys.argv[1]]()
