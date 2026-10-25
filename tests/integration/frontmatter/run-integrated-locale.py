#!/usr/bin/env python3
"""Compile and verify seven joined TeX/Biber manuscripts in one selected locale.

CI runs four isolated locales concurrently. Unlike the earlier 7x4 frontmatter
smokes, these fixtures exercise the same PDF's frontmatter, notes, objects,
citations, bibliography and applicable backmatter.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import shutil
import subprocess
import sys
import tempfile
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
ARTIFACTS = ROOT / "artifacts" / "integrated-i18n"
LANGUAGES = {
    "pt": ("pt-BR", "brazilian", "Referências", "julgado em"),
    "en": ("en-US", "english", "References", "judged on"),
    "es": ("es-ES", "spanish", "Referencias", "juzgado el"),
    "fr": ("fr-FR", "french", "Références", "jugé le"),
}


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def fold(text: str) -> str:
    text = unicodedata.normalize("NFKD", text.casefold())
    return re.sub(r"\s+", " ", "".join(c for c in text if not unicodedata.combining(c)))


def command(args: list[str], logfile: Path) -> None:
    with logfile.open("w", encoding="utf-8") as out:
        process = subprocess.run(args, cwd=ROOT, stdout=out, stderr=subprocess.STDOUT,
                                 text=True, check=False)
    if process.returncode:
        lines = logfile.read_text(encoding="utf-8", errors="replace").splitlines()
        print("\n".join(lines[-55:]), file=sys.stderr, flush=True)
        raise RuntimeError(f"command failed rc={process.returncode}: {args[:3]}")


def real_pdf_lang(pdf: Path) -> str:
    payload = json.loads(subprocess.check_output([
        "qpdf", "--json=2", "--json-key=qpdf", str(pdf)
    ], cwd=ROOT, text=True))
    data = payload["qpdf"]
    if len(data) != 2 or data[0].get("jsonversion") != 2:
        raise ValueError("qpdf JSON format drift")
    obj = data[1]
    root = obj["trailer"]["value"]["/Root"]
    if not re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root):
        raise ValueError("malformed PDF Root object reference")
    catalog = obj["obj:" + root]["value"]
    if catalog.get("/Type") != "/Catalog":
        raise ValueError("invalid PDF Root catalog")
    found = catalog.get("/Lang")
    if not isinstance(found, str) or not found.startswith("u:"):
        raise ValueError("missing or non-Unicode PDF /Root/Lang")
    return found[2:]


def check_text(txt: str, profile: str, locale: str) -> dict:
    visible = fold(txt)
    _, _, references, legal_date = LANGUAGES[locale]
    expected = [
        f"integrated-manuscript-{locale}-{profile.replace('-', '')}",
        f"integrated-section-{locale}",
        f"integrated-object-{locale}",
        f"integrated-table-{locale}",
        references, "silva", "oliveira", legal_date,
    ]
    if profile == "scientific-article":
        expected += [f"integrated-article-primary-{locale}",
                     "integrated-article-companion-"]
    else:
        expected += [f"integrated-appendix-body-{locale}",
                     f"integrated-annex-body-{locale}"]
        if profile not in {"research-project", "anonymized-research-project"}:
            companion = "en" if locale == "pt" else "pt"
            expected += [f"integrated-summary-{locale}-main",
                         f"integrated-summary-{companion}-companion"]
    if profile == "doctoral-thesis":
        expected += ["integrated term"]
    missing = [token for token in expected if fold(token) not in visible]
    if missing:
        raise ValueError(f"missing PDF text for {profile}/{locale}: {missing}, sample={visible[:750]}")
    # Target *class-owned* label leaks; never ban all Portuguese because
    # names, source titles and the required PT companion are legitimate.
    # Keep these probes narrow: Spanish Referencias folds identically to
    # Portuguese Referências and therefore cannot be an ES forbidden token.
    forbidden = {
        "pt": ("judged on", "juzgado el", "juge le"),
        "en": ("julgado em", "juzgado el", "juge le",
               "referências", "glossário", "índice remissivo",
               "banca examinadora", "tese apresentada ao"),
        "es": ("julgado em", "judged on", "juge le",
               "glossário", "índice remissivo", "banca examinadora"),
        "fr": ("julgado em", "judged on", "juzgado el",
               "referências", "glossário", "índice remissivo",
               "banca examinadora", "tese apresentada ao"),
    }
    leaking = [
        token for token in forbidden[locale]
        if re.search(r"(?<!\\w)" + re.escape(fold(token)) + r"(?!\\w)", visible)
    ]
    if leaking:
        raise ValueError(f"wrong-locale class-owned labels in {profile}/{locale}: {leaking}")
    return {"positive_tokens": len(expected), "missing": [],
            "negative_locale_labels": len(forbidden[locale]),
            "negative_policy": "targeted class-owned labels only; PT companion and authored data allowed"}


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--locale", required=True, choices=tuple(LANGUAGES))
    args = parser.parse_args()
    locale = args.locale
    path = ARTIFACTS / locale
    path.mkdir(parents=True, exist_ok=True)
    command([sys.executable, str(ROOT / "tests/integration/frontmatter/generate-integrated-locale.py"),
             "--locale", locale], path / "generation.log")
    index = json.loads((path / "source-index.json").read_text(encoding="utf-8"))
    expected = {"undergraduate-capstone", "specialization-capstone",
                "masters-thesis", "doctoral-thesis", "research-project",
                "anonymized-research-project", "scientific-article"}
    if len(index) != 7 or {v["profile"] for v in index} != expected:
        raise ValueError("integrated matrix must contain exactly the seven profiles")
    source_sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                         text=True).strip()
    expected_source = os.getenv("SOURCE_COMMIT_SHA")
    if expected_source and expected_source != source_sha:
        raise ValueError("CI checkout SHA differs from expected PR/push source SHA")
    entries = []
    with tempfile.TemporaryDirectory(prefix="abntexto-integrated-i18n-") as tmp:
        work = Path(tmp)
        for fixture in index:
            profile = fixture["profile"]
            job = fixture["name"]
            src = ROOT / fixture["source"]
            paths = [src, *(ROOT / x for x in fixture["support_sources"])]
            if not all(p.is_file() for p in paths):
                raise ValueError(f"missing source or summary input for {job}")
            logfile = path / f"{job}-pdflatex.log"
            print(f"INTEGRATED-I18N running locale={locale} profile={profile}", flush=True)
            for part in (1,):
                command(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                         "-file-line-error", f"-jobname={job}",
                         f"-output-directory={work}", str(src)], logfile)
            command(["biber", "--input-directory", str(work),
                     "--output-directory", str(work), job],
                    path / f"{job}-biber.log")
            if profile == "doctoral-thesis":
                command(["makeglossaries", "-d", str(work), job],
                        path / f"{job}-glossaries.log")
                command(["makeindex", str(work / f"{job}.idx"),
                         "-o", str(work / f"{job}.ind")],
                        path / f"{job}-index.log")
            for part in (2, 3):
                command(["pdflatex", "-interaction=nonstopmode", "-halt-on-error",
                         "-file-line-error", f"-jobname={job}",
                         f"-output-directory={work}", str(src)], logfile)
            compiled = work / (job + ".pdf")
            if not compiled.is_file() or compiled.stat().st_size == 0:
                raise ValueError(f"PDF not produced: {job}")
            pdf = path / (job + ".pdf")
            shutil.copy2(compiled, pdf)
            txt = path / (job + ".txt")
            with txt.open("w", encoding="utf-8") as out:
                process = subprocess.run(["pdftotext", "-layout", str(pdf), "-"],
                                         cwd=ROOT, stdout=out, stderr=subprocess.PIPE,
                                         text=True, check=False)
                if process.returncode:
                    raise ValueError(f"pdftotext failed for {job}: {process.stderr}")
            checks = check_text(txt.read_text(encoding="utf-8"), profile, locale)
            log = (work / (job + ".log")).read_text(encoding="utf-8", errors="replace")
            expected_babel = LANGUAGES[locale][1]
            if f"INTEGRATED-I18N-BABEL={expected_babel}" not in log:
                raise ValueError(f"Babel did not activate {expected_babel} in {job}")
            lang = real_pdf_lang(pdf)
            if lang != LANGUAGES[locale][0]:
                raise ValueError(f"/Root/Lang {lang} != {LANGUAGES[locale][0]} for {job}")
            info = subprocess.check_output(["pdfinfo", str(pdf)], cwd=ROOT, text=True)
            match = re.search(r"^Pages:\s+(\d+)", info, re.MULTILINE)
            if not match or int(match.group(1)) < 1:
                raise ValueError(f"invalid PDF page count for {job}")
            entry = {"profile": profile, "locale": locale, "job": job,
                     "source": fixture["source"], "source_sha256": sha(src),
                     "support_files": [
                         {"path": p.relative_to(ROOT).as_posix(), "sha256": sha(p)}
                         for p in paths[1:]
                     ], "pdf": pdf.relative_to(ROOT).as_posix(),
                     "pdf_sha256": sha(pdf), "pdf_pages": int(match.group(1)),
                     "babel": expected_babel, "pdf_catalog_lang": lang,
                     "biber": "PASS", "checks": checks}
            entries.append(entry)
            print(f"INTEGRATED-I18N status=PASS profile={profile} locale={locale} "
                  f"real_pdf=true biber=PASS catalog={lang} pages={entry['pdf_pages']}", flush=True)
    output = {"status": "AUTOMATED_PARTIAL", "source_sha": source_sha,
              "locale": locale, "profiles": len(entries), "bibliography": "Biber",
              "pdf_catalog_independently_verified": True,
              "full_command_optional_coverage": "PENDING",
              "official_translations_verified": False,
              "human_visual_approval": "PENDING",
              "anonymized_tex_scope": "INTERNAL_AUDIT_ONLY",
              "entries": entries}
    (path / "manifest.json").write_text(
        json.dumps(output, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"INTEGRATED-I18N status=PASS locale={locale} profiles=7 "
          "real_pdfs=7 biber=PASS sha256=PASS babel=PASS pdf_lang=PASS")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, RuntimeError, subprocess.CalledProcessError) as exc:
        raise SystemExit(f"INTEGRATED-I18N status=FAIL reason={exc}") from exc
