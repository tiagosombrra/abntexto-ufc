#!/usr/bin/env python3
"""B4 candidate proof: 11 content, bibliography and upstream legacy APIs.

Uses original 7-profile/four-locale real PDFs. Only a source-bound positive
output and a fail-closed negative predicate can support a bounded API PASS.
This file never changes the canonical ledger or grants release authorization.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import unicodedata

ROOT = Path(__file__).resolve().parents[3]
OUTPUT = ROOT / "artifacts/integrated-i18n"
LOCALES = {"pt": "pt-BR", "en": "en-US", "es": "es-ES", "fr": "fr-FR"}
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
ACADEMIC = set(PROFILES[:4])
NONARTICLE = set(PROFILES[:-1])
DOCTOR = {"doctoral-thesis"}
ALL = set(PROFILES)
COMMANDS = {
    r"\ufcSource": ALL,
    r"\ufcNote": ALL,
    r"\ufcAddBibliographyResource": ALL,
    r"\ufcPrintReferences": ALL,
    r"\ufcPrintGlossary": DOCTOR,
    r"\ufcPrintIndex": DOCTOR,
    r"\legend": ALL,
    r"\appendix": NONARTICLE,
    r"\annex": NONARTICLE,
    r"\pretextual": NONARTICLE,
    r"\textual": ALL,
}
HEADINGS = {
    "pt": {"refs": "Referências", "gloss": "Glossário",
           "index": "Índice Remissivo", "appendix": "Apêndice", "annex": "Anexo"},
    "en": {"refs": "References", "gloss": "Glossary",
           "index": "Index", "appendix": "Appendix", "annex": "Annex"},
    "es": {"refs": "Referencias", "gloss": "Glosario",
           "index": "Índice Alfabético", "appendix": "Apéndice", "annex": "Anexo"},
    "fr": {"refs": "Références", "gloss": "Glossaire",
           "index": "Index", "appendix": "Appendice", "annex": "Annexe"},
}
PDF_KEYWORDS = ("anais do simpósio de teste", "estudos de informação em ambientes")
SOURCES = (r"\ufcAddBibliographyResource{tests/fixtures/references.bib}",
           r"\ufcAddBibliographyResource{tests/fixtures/i18n-jurisdiction.bib}")


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def fold(value: str) -> str:
    value = unicodedata.normalize(
        "NFKD", value.casefold().replace("’", "'").replace("ʼ", "'"))
    value = re.sub(r"\s+", " ", "".join(
        c for c in value if not unicodedata.combining(c)))
    # Restore class-independent synthetic markers split across PDF lines.
    return re.sub(r"-(?=\s+\w)\s+", "-", value)


def pages_from_pdf(extracted: str, count: int | None = None) -> list[str]:
    pages = extracted.split("\f")
    if pages and not pages[-1].strip():
        pages.pop()
    require(bool(pages) and (count is None or len(pages) == count),
            "B4 physical PDF page count differs from Poppler")
    return pages


def command_count(src: str, command: str) -> int:
    return len(re.findall(re.escape(command) + r"(?![A-Za-z])", src))


def unique_heading_page(pages: list[str], heading: str) -> int:
    matches = [
        i for i, page in enumerate(pages)
        if any(fold(line).strip() == fold(heading) for line in page.splitlines())
    ]
    require(len(matches) == 1,
            f"B4 heading absent or duplicated: {heading}/{matches}")
    return matches[0]


def proof(src: str, pages: list[str], profile: str, locale: str,
          biber: str = "PASS") -> list[dict]:
    require(profile in PROFILES and locale in LOCALES and biber == "PASS",
            "B4 invalid profile/locale or Biber did not certify")
    text = fold("\f".join(pages))
    ordered = {}
    for command, profiles in COMMANDS.items():
        applicable = profile in profiles
        expected = int(applicable)
        if command == r"\ufcAddBibliographyResource":
            expected = 2
        elif command in (r"\ufcSource", r"\legend"):
            expected = 3 if profile in ACADEMIC else 1
        require(command_count(src, command) == expected,
                f"B4 source public command occurrence drift: {profile}/{locale}/{command}")
        ordered[command] = applicable

    require(all(src.count(resource) == 1 for resource in SOURCES),
            "B4 both original distinct bibliography resources are required")
    require(r"\parencite{silva2020}" in src and r"\textcite{oliveira2011}" in src,
            "B4 actual author-supplied citation source was removed")

    manuscript = fold("INTEGRATED-MANUSCRIPT-" + locale + "-"
                      + profile.replace("-", "").upper())
    body = [i for i, p in enumerate(pages) if manuscript in fold(p)]
    require(len(body) == 1, "B4 textual manuscript body missing/duplicated")
    body_index = body[0]
    require(body_index < len(pages) - 1,
            "B4 body marker is not before bibliography/backmatter")
    require(fold("INTEGRATED-SECTION-" + locale.upper()) in fold(pages[body_index]),
            "B4 section marker is outside the textual body")

    note = "synthetic object note"
    n_sources = 3 if profile in ACADEMIC else 1
    require(text.count("synthetic original") == n_sources and text.count(note) == 1,
            "B4 real-PDF public Source/Note attribution is missing or duplicated")
    note_pages = [i for i, p in enumerate(pages) if note in fold(p)]
    require(len(note_pages) == 1 and note_pages[0] >= body_index,
            "B4 object note is not on a textual body page")
    expected_legends = ["INTEGRATED-OBJECT-" + locale.upper()]
    if profile in ACADEMIC:
        expected_legends += [
            "INTEGRATED-CHART-" + locale.upper(),
            "INTEGRATED-TEXTTABLE-" + locale.upper(),
        ]
    for marker in expected_legends:
        body_hits = [
            i for i, p in enumerate(pages)
            if i >= body_index and fold(marker) in fold(p)
        ]
        require(len(body_hits) == 1,
                f"B4 real legend caption is missing or duplicated in textual body: {marker}")

    reference_page = unique_heading_page(pages, HEADINGS[locale]["refs"])
    require(reference_page > body_index
            and all(fold(token) in fold(pages[reference_page])
                    for token in PDF_KEYWORDS),
            "B4 bibliography missing one of two real resources on references page")
    result = []
    for command, applicable in ordered.items():
        if not applicable:
            result.append({
                "identifier": command, "status": "NOT_EXERCISED_IN_PROFILE",
                "reason": "This API is not invoked for this document profile",
            })
        else:
            page = reference_page + 1
            if command in (r"\ufcSource", r"\ufcNote", r"\legend", r"\textual"):
                page = body_index + 1
            result.append({
                "identifier": command, "status": "BOUNDED_REAL_PDF_PASS",
                "proof_physical_page": page,
            })

    if profile not in NONARTICLE:
        require(command_count(src, r"\pretextual") == 0
                and command_count(src, r"\appendix") == 0
                and command_count(src, r"\annex") == 0,
                "B4 scientific article may not have legacy prelim/appendix phases")
    else:
        require(src.index(r"\pretextual") < src.index(r"\textual")
                < src.index(r"\ufcPrintReferences")
                < src.index(r"\appendix") < src.index(r"\annex"),
                "B4 legacy phase commands not in required source order")
        require(body_index >= 2,
                "B4 legacy pretextual phase omitted cover/title PDF pages")
        ap = fold("INTEGRATED-APPENDIX-BODY-" + locale.upper())
        an = fold("INTEGRATED-ANNEX-BODY-" + locale.upper())
        appendices = [i for i, p in enumerate(pages)
                      if ap in fold(p) and fold(HEADINGS[locale]["appendix"]) in fold(p)]
        annexes = [i for i, p in enumerate(pages)
                   if an in fold(p) and fold(HEADINGS[locale]["annex"]) in fold(p)]
        require(len(appendices) == len(annexes) == 1
                and reference_page < appendices[0] < annexes[0],
                "B4 appendix/annex headings or bodies misplaced/duplicated")
        for row in result:
            if row["identifier"] == r"\appendix":
                row["proof_physical_page"] = appendices[0] + 1
            if row["identifier"] == r"\annex":
                row["proof_physical_page"] = annexes[0] + 1
            if row["identifier"] == r"\pretextual":
                row["proof_physical_page"] = 1

    if profile in DOCTOR:
        require(r"\gls{integratedterm}" in src
                and r"\index{integrated term}" in src,
                "B4 real populated glossary/index source missing")
        glossary_page = unique_heading_page(pages, HEADINGS[locale]["gloss"])
        index_page = unique_heading_page(pages, HEADINGS[locale]["index"])
        require(reference_page < glossary_page < index_page
                and fold("integrated term: synthetic term for locale testing")
                in fold(pages[glossary_page])
                and fold("integrated term,") in fold(pages[index_page]),
                "B4 doctoral glossary/index does not have populated separate pages")
        for row in result:
            if row["identifier"] == r"\ufcPrintGlossary":
                row["proof_physical_page"] = glossary_page + 1
            if row["identifier"] == r"\ufcPrintIndex":
                row["proof_physical_page"] = index_page + 1
    else:
        for heading in ("gloss", "index"):
            require(not any(
                fold(line).strip() == fold(HEADINGS[locale][heading])
                for page in pages for line in page.splitlines()
            ), "B4 non-doctoral profile unexpectedly printed glossary/index")

    require(len(result) == 11, "B4 eleven-ID inventory drift")
    return result


def negatives() -> int:
    # A real producer PDF is required for certification. These mutations
    # guard source/count, physical heading, and semantic relation helpers.
    count = 0
    for cmd in COMMANDS:
        if command_count(cmd, cmd) != 1 or command_count("", cmd) != 0:
            raise ValueError("B4 public macro token boundary guard failed")
        if command_count(cmd + "Extra", cmd) != 0:
            raise ValueError("B4 public token prefix mutant escaped")
        count += 1
    if pages_from_pdf("FRONT\f\fBODY\f") != ["FRONT", "", "BODY"]:
        raise ValueError("B4 blank duplex physical page was removed")
    count += 1
    for bad in (["References", "References"], ["WRONG TITLE"], [""]):
        try:
            unique_heading_page(bad, "References")
        except ValueError:
            count += 1
        else:
            raise ValueError("B4 absent/duplicate bibliography heading accepted")
    require(count == 15, "B4 integrated mutation inventory drift")
    return count


def runtime_negative_mutations(source: str, physical: list[str],
                               profile: str, locale: str, biber: str) -> int:
    # Run the full source/PDF predicates on mutated copies of original bytes;
    # no mutated output may qualify for a positive source-bound receipt.
    proof(source, physical, profile, locale, biber)
    count = 0
    for command, applicable in COMMANDS.items():
        if profile not in applicable:
            continue
        mutated = source.replace(command, r"\B4MUTATED", 1)
        require(mutated != source, "B4 source mutation was not applied")
        try:
            proof(mutated, physical, profile, locale, biber)
        except ValueError:
            count += 1
        else:
            raise ValueError(f"B4 real source deletion accepted: {command}")

    for pattern in (r"Synthetic\s+original", r"Synthetic\s+object\s+note",
                    r"Anais\s+do\s+simpósio\s+de\s+teste"):
        changed = [re.sub(pattern, "B4-DELETED-EVIDENCE", page, flags=re.I)
                   for page in physical]
        require(changed != physical,
                f"B4 negative PDF text mutation could not find target: {pattern}")
        try:
            proof(source, changed, profile, locale, biber)
        except ValueError:
            count += 1
        else:
            raise ValueError(f"B4 missing PDF evidence accepted: {pattern}")

    if profile == "doctoral-thesis":
        for heading in ("gloss", "index"):
            index = unique_heading_page(
                physical, HEADINGS[locale][heading])
            changed = list(physical)
            changed[index] = "B4-REMOVED-DOCTORAL-BACKMATTER"
            try:
                proof(source, changed, profile, locale, biber)
            except ValueError:
                count += 1
            else:
                raise ValueError(f"B4 absent doctoral {heading} accepted")

    return count


def checked(path: Path, digest: str, folder: Path) -> bytes:
    require(path.resolve().is_relative_to(folder.resolve()) and path.is_file(),
            "B4 original source/PDF file missing or outside locale artifact")
    require(re.fullmatch(r"[0-9a-f]{64}", digest) is not None,
            "B4 source/PDF receipt is not a SHA256")
    raw = path.read_bytes()
    require(hashlib.sha256(raw).hexdigest() == digest,
            "B4 original source/PDF hash changed")
    return raw


def pdf_catalog_lang(pdf: Path, locale: str) -> str:
    raw = json.loads(subprocess.check_output([
        "qpdf", "--json=2", "--json-key=qpdf", str(pdf)
    ], cwd=ROOT, text=True))
    objects = raw["qpdf"]
    require(len(objects) == 2 and objects[0].get("jsonversion") == 2,
            "B4 malformed actual PDF catalog JSON")
    root = objects[1]["trailer"]["value"]["/Root"]
    require(re.fullmatch(r"[1-9][0-9]* [0-9]+ R", root) is not None,
            "B4 invalid PDF root catalog reference")
    catalog = objects[1]["obj:" + root]["value"]
    expected = LOCALES[locale]
    require(catalog.get("/Type") == "/Catalog"
            and catalog.get("/Lang") == "u:" + expected,
            "B4 actual PDF /Root/Lang does not match source locale")
    return expected


def run(locale: str) -> None:
    commit = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                     cwd=ROOT, text=True).strip()
    require(os.getenv("SOURCE_COMMIT_SHA") in (None, commit),
            "B4 original CI checkout SHA mismatch")
    folder = OUTPUT / locale
    manifest = json.loads((folder / "manifest.json").read_text(encoding="utf-8"))
    require(manifest.get("source_sha") == commit and manifest.get("locale") == locale
            and len(manifest.get("entries", [])) == 7,
            "B4 original integrated PDF provenance or corpus mismatch")
    seen, receipts, runtime_negatives = set(), [], 0
    for row in manifest["entries"]:
        profile = row["profile"]
        require(profile in PROFILES and profile not in seen
                and row["locale"] == locale and row["biber"] == "PASS",
                "B4 duplicate/uncertified original profile")
        seen.add(profile)
        source = checked(ROOT / row["source"], row["source_sha256"],
                         folder).decode("utf-8")
        pdf = ROOT / row["pdf"]
        checked(pdf, row["pdf_sha256"], folder)
        info = subprocess.check_output(["pdfinfo", str(pdf)], cwd=ROOT, text=True)
        quantity = re.search(r"(?m)^Pages:\s*(\d+)\s*$", info)
        require(quantity is not None, "B4 original PDF physical page count missing")
        count = int(quantity.group(1))
        extracted = subprocess.check_output(
            ["pdftotext", "-layout", str(pdf), "-"], cwd=ROOT, text=True)
        originals = pages_from_pdf(extracted, count)
        lang = pdf_catalog_lang(pdf, locale)
        require(row["pdf_catalog_lang"] == lang and row["pdf_pages"] == count,
                "B4 original PDF page/catalog manifest mismatch")
        observed = proof(source, originals, profile, locale, row["biber"])
        runtime_negatives += runtime_negative_mutations(
            source, originals, profile, locale, row["biber"])
        receipts.append({
            "locale": locale, "profile": profile, "physical_pages": count,
            "pdf_catalog_lang": lang, "source_sha256": row["source_sha256"],
            "pdf_sha256": row["pdf_sha256"], "observations": observed,
        })
    require(seen == set(PROFILES)
            and sum(e["status"] == "BOUNDED_REAL_PDF_PASS"
                    for r in receipts for e in r["observations"]) == 62,
            "B4 integrated actual positive applicability count drift")
    report = {
        "status": "BOUNDED_B4_ELEVEN_INTEGRATED_CANDIDATE_PDF_PASS",
        "source_sha": commit, "locale": locale, "real_pdfs": len(receipts),
        "identifiers": list(COMMANDS), "positive_observations": 62,
        "inapplicable_observations": 15, "negative_controls": 15,
        "runtime_negative_mutations": runtime_negatives,
        "receipts": receipts, "human_normative_linguistic_review": "PENDING",
        "ledger_promotion": "NOT_AUTOMATIC", "publication_authorized": False,
    }
    (folder / "b4-integrated-backmatter-proof.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"I18N-B4-INTEGRATED status=PASS locale={locale} IDs=11"
          " profiles=7 positives=62 negatives=15 physical_pages=PASS"
          f" source_PDF_SHA256=PASS runtime_negative={runtime_negatives}"
          " human_review=PENDING")


def main() -> None:
    p = argparse.ArgumentParser()
    p.add_argument("--locale", choices=tuple(LOCALES))
    p.add_argument("--preflight", action="store_true")
    a = p.parse_args()
    count = negatives()
    if a.preflight:
        print(f"I18N-B4-INTEGRATED-PREFLIGHT status=PASS IDs=11"
              f" negatives={count} original_PDF=PENDING")
    elif a.locale:
        run(a.locale)
    else:
        raise ValueError("choose --preflight or --locale")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError, UnicodeError) as exc:
        raise SystemExit(f"I18N-B4-INTEGRATED status=FAIL reason={exc}") from exc
