#!/usr/bin/env python3
"""Compile and audit seven human-readable manuscript PDFs for one locale.

Every PDF has actual authored source, full scientific figures, original hashes,
and a first-page raster. This does not assert human visual or normative approval.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[2]
OUT = ROOT / "artifacts/human-readable-28"
PROFILES = ("undergraduate-capstone", "specialization-capstone",
            "masters-thesis", "doctoral-thesis", "research-project",
            "anonymized-research-project", "scientific-article")
LOCALES = ("pt", "en", "es", "fr")

def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()

def run(args: list[str], log: Path, *, cwd: Path = ROOT) -> None:
    with log.open("w", encoding="utf-8") as f:
        r = subprocess.run(args, cwd=cwd, stdout=f,
                           stderr=subprocess.STDOUT, check=False)
    if r.returncode:
        tail = "\n".join(log.read_text(errors="replace").splitlines()[-60:])
        raise RuntimeError(f"{' '.join(args[:2])}: exit {r.returncode}\n{tail}")

def page_text(pdf: Path, *, first_only: bool = False) -> str:
    cmd = ["pdftotext", "-layout"]
    if first_only:
        cmd += ["-f", "1", "-l", "1"]
    return subprocess.check_output([*cmd, str(pdf), "-"], text=True,
                                   cwd=ROOT, errors="replace")

def images_on_cover(pdf: Path) -> int:
    output = subprocess.check_output(["pdfimages", "-list", str(pdf)],
                                     text=True, cwd=ROOT)
    # Poppler prints a separate first-page record for an embedded crest raster.
    return sum(bool(re.match(r"^\s*1\s+\d+\s+", row))
               for row in output.splitlines()[2:])

def build_one(entry: dict, loc: str, out: Path, work: Path) -> dict:
    profile = entry["profile"]
    src = ROOT / entry["source"]
    if sha(src) != entry["source_sha256"]:
        raise ValueError("Source was modified after generation: " + str(src))
    job = src.stem
    def command():
        return ["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                "-file-line-error", f"-jobname={job}",
                f"-output-directory={work}", str(src)]
    run(command(), out / f"{job}-latex1.log")
    run(["biber", "--input-directory", str(work),
         "--output-directory", str(work), job], out / f"{job}-biber.log")
    if profile == "doctoral-thesis":
        run(["makeglossaries", "-d", str(work), job],
            out / f"{job}-glossaries.log")
        run(["makeindex", f"{job}.idx", "-o", f"{job}.ind"],
            out / f"{job}-index.log", cwd=work)
    run(command(), out / f"{job}-latex2.log")
    run(command(), out / f"{job}-latex3.log")
    pdf = work / (job + ".pdf")
    if not pdf.is_file() or pdf.stat().st_size < 1000:
        raise ValueError("Missing PDF " + job)
    final = out / pdf.name
    final.write_bytes(pdf.read_bytes())
    extracted = page_text(final)
    first = page_text(final, first_only=True)
    leaked = [w for w in ("R4-", "R5-", "INTEGRATED-", "INTEGRATED TEST",
                          "R4LONG", "R4NATIVE", "SYNTHETIC-ANON",
                          "INTEGRATED MULTILINGUAL DOCUMENT")
              if w in extracted]
    findings = []
    if leaked:
        findings.append("fixture_labels_visible:" + ",".join(leaked))
    if profile not in {"scientific-article", "anonymized-research-project"}:
        if images_on_cover(final) < 1:
            findings.append("ufc_coat_of_arms_absent_on_cover")
    if profile == "anonymized-research-project":
        if "ABNTEXTO-UFC editorial team" in extracted or \
                "Equipe editorial ABNTEXTO-UFC" in extracted:
            findings.append("anonymous_author_visible")
    info = subprocess.check_output(["pdfinfo", str(final)], text=True,
                                   cwd=ROOT, errors="replace")
    p = re.search(r"^Pages:\s+(\d+)", info, flags=re.M)
    if not p or int(p[1]) < 5:
        findings.append("physical_pages_missing")
    for marker in (r"\subsection{", r"\subsubsection{", r"\begin{longtable}",
                   r"\begin{longabnttblr}", r"\begin{ufcalgorithm}",
                   r"\begin{ufclisting}", r"\ufcPrintReferences"):
        if marker not in src.read_text(encoding="utf-8"):
            findings.append("source_feature_missing:" + marker)
    if profile != "scientific-article" and "2026" not in first:
        findings.append("cover_text_missing")
    # Keep only the rendered first-page image for manual crest/title inspection.
    preview = out / (job + "-cover")
    run(["pdftoppm", "-f", "1", "-l", "1", "-scale-to", "1050",
         "-png", "-singlefile", str(final), str(preview)],
        out / (job + "-raster.log"))
    result = {"profile": profile, "locale": loc,
              "source_sha256": entry["source_sha256"],
              "pdf_sha256": sha(final), "pdf": str(final.relative_to(ROOT)),
              "pages": int(p[1]) if p else 0,
              "coat_of_arms_embedded": (images_on_cover(final) > 0),
              "failures": findings, "human_visual_approval": "PENDING"}
    (out / f"{job}-receipt.json").write_text(
        json.dumps(result, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    print(f"READABLE-REVIEW-PDF locale={loc} profile={profile} "
          f"pages={result['pages']} crest={result['coat_of_arms_embedded']} "
          f"failures={findings}", flush=True)
    return result

def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, choices=LOCALES)
    parser.add_argument("--preflight", action="store_true")
    args = parser.parse_args()
    loc = args.locale
    (OUT / loc).mkdir(parents=True, exist_ok=True)
    src_manifest = OUT / loc / "review-sources.json"
    if not src_manifest.is_file():
        run([sys.executable, "tools/review/generate_readable_28.py",
             "--locale", loc], OUT / loc / "generation.log")
    items = json.loads(src_manifest.read_text(encoding="utf-8"))["entries"]
    if len(items) != 7 or set(x["profile"] for x in items) != set(PROFILES):
        raise ValueError("Incomplete review source matrix")
    for x in items:
        if sha(ROOT / x["source"]) != x["source_sha256"]:
            raise ValueError("Source hash mismatch")
    if args.preflight:
        print(f"READABLE-REVIEW-PREFLIGHT status=PASS locale={loc} sources=7")
        return 0
    out = OUT / loc
    work = out / "work"
    work.mkdir(parents=True, exist_ok=True)
    results = []
    for item in items:
        results.append(build_one(item, loc, out, work))
    complete = {
        "source_commit_sha": os.environ.get("SOURCE_COMMIT_SHA", ""),
        "locale": loc, "pdf_count": len(results),
        "page_count": sum(x["pages"] for x in results),
        "failures": sum(len(x["failures"]) for x in results),
        "human_approval": "PENDING",
        "release_authorized": False, "documents": results}
    (out / "review-pdfs.json").write_text(
        json.dumps(complete, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8")
    if complete["failures"]:
        print("READABLE-REVIEW-EVIDENCE status=FAIL", flush=True)
        return 1
    print(f"READABLE-REVIEW-EVIDENCE status=AUTOMATED_PARTIAL locale={loc} "
          f"pdfs=7 pages={complete['page_count']} human_approval=PENDING", flush=True)
    return 0

if __name__ == "__main__":
    try:
        sys.exit(main())
    except (ValueError, RuntimeError, OSError, subprocess.CalledProcessError) as e:
        print("READABLE-REVIEW-EVIDENCE status=FAIL reason=" + str(e),
              file=sys.stderr)
        sys.exit(1)
