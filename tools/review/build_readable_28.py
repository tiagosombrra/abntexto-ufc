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
import runpy
import subprocess
import sys
import xml.etree.ElementTree as ET

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



def native_longtable_pagination(extracted: str, loc: str) -> tuple[dict, list[str]]:
    """Inspect original native longtable data rows on physical PDF pages."""
    native_name = {
        "pt": "Amostra", "en": "Sample",
        "es": "Muestra", "fr": "Échantillon",
    }[loc]
    row_pattern = re.compile(
        r"(?<!\w)" + re.escape(native_name) + r"\s+([1-9]\d{0,2})(?!\d)",
        re.I,
    )
    row_pages: dict[int, list[int]] = {}
    for page_no, page in enumerate(extracted.split("\f"), 1):
        for match in row_pattern.finditer(page):
            number = int(match.group(1))
            if 1 <= number <= 85:
                row_pages.setdefault(number, []).append(page_no)
    missing = sorted(set(range(1, 86)) - row_pages.keys())
    duplicated = sorted(number for number, pages in row_pages.items()
                        if len(pages) != 1)
    last_page = row_pages.get(85, [None])[0]
    count = sum(last_page in pages for pages in row_pages.values()) if last_page else 0
    metrics = {
        "last_data_page": last_page,
        "last_data_page_rows": count,
        "missing_rows": missing,
        "duplicate_rows": duplicated,
    }
    findings = []
    if missing or duplicated:
        findings.append("native_longtable_rows_missing_or_duplicated")
    if count == 1:
        findings.append("native_longtable_single_final_row_page:" + str(last_page))
    return metrics, findings


def isolated_author_year_line_faults(page: ET.Element) -> list[str]:
    """Reject single-word author-year fragments on actual PDF line boxes."""
    word_tag = "{http://www.w3.org/1999/xhtml}word"
    line_tag = "{http://www.w3.org/1999/xhtml}line"
    lines = list(page.iter(line_tag))
    # A nonempty word-only page proves that the extraction omitted line boxes.
    if not lines and next(page.iter(word_tag), None) is not None:
        return ["bbox_layout_line_boxes_missing"]
    faults: list[str] = []
    for line in lines:
        words = [(w.text or "").strip() for w in line.iter(word_tag)
                 if (w.text or "").strip()]
        if len(words) == 1 and re.fullmatch(r"\(\d{4}[a-z]?\)\.?", words[0]):
            faults.append("isolated_author_year_at_line_start")
    return faults


def find_layout_defects(pdf: Path, loc: str) -> tuple[list[str], float | None]:
    """Measure real glyph positions, not textual adjacency in extracted PDF text."""
    xml = subprocess.check_output(["pdftotext", "-bbox-layout", str(pdf), "-"],
                                  cwd=ROOT, text=True, errors="replace")
    doc = ET.fromstring(xml)
    word_name = "{http://www.w3.org/1999/xhtml}word"
    page_name = "{http://www.w3.org/1999/xhtml}page"
    anchors = {
        "pt": ("estruturada:", "Discretização"),
        "en": ("mesh:", "A"),
        "es": ("estructurada:", "Una"),
        "fr": (":", "Discrétisation"),
    }
    end_label, start_definition = anchors[loc]
    citation_first = {
        "pt": "Consulte", "en": "Consult",
        "es": "Consúltense", "fr": "Consulter",
    }[loc]
    pairs: list[float] = []
    citation_separations: list[float] = []
    faults: list[str] = []
    for page in doc.iter(page_name):
        words = list(page.iter(word_name))
        tails = [w for w in words if (w.text or "") == end_label]
        starts = [w for w in words if (w.text or "") == start_definition]
        for tail in tails:
            y = float(tail.get("yMin", "-100"))
            nearby = [
                w for w in starts
                if abs(float(w.get("yMin", "-100")) - y) <= 2.0
                and float(w.get("xMin", "0")) >= float(tail.get("xMax", "0")) - 1.0
            ]
            if nearby:
                head = min(nearby, key=lambda w: float(w.get("xMin", "0")))
                pairs.append(round(float(head.get("xMin", "0")) -
                                   float(tail.get("xMax", "0")), 3))
                # Text extraction can report adjacent paragraphs on one
                # physical baseline. Reject the regression where the
                # bibliography sentence was concatenated to the definition.
                citation_words = [
                    w for w in words if (w.text or "") == citation_first
                    and -1.0 <= float(w.get("yMin", "-100")) - y <= 90.0
                ]
                if citation_words:
                    vertical_gap = min(
                        float(w.get("yMin", "-100")) - y
                        for w in citation_words
                    )
                    citation_separations.append(round(vertical_gap, 3))
        # Inspect real line boxes; a word-only bbox extract is a hard failure.
        faults.extend(isolated_author_year_line_faults(page))
    if not pairs:
        faults.append("editorial_definition_pair_missing")
        return faults, None
    # A doctoral glossary can add a second legitimate occurrence. Each
    # detected pair must have a sane gap; a good pair may not mask a bad one.
    bad_gaps = [gap for gap in pairs if not 1.0 <= gap <= 9.0]
    if bad_gaps:
        faults.append("definition_interword_gap_points:" + ",".join(map(str, bad_gaps)))
    if not citation_separations:
        faults.append("following_bibliography_paragraph_not_found")
    elif any(not 12.0 <= distance <= 70.0
             for distance in citation_separations):
        faults.append("definition_bibliography_vertical_gap_points:"
                      + ",".join(map(str, citation_separations)))
    return faults, min(pairs)


def orphaned_native_table_pages(extracted: str, locale: str) -> list[int]:
    """Reject a one-row final native longtable continuation in a real PDF."""
    header_case, header_value, native_case = {
        "pt": ("Caso", "Valor", "Amostra"),
        "en": ("Case", "Value", "Sample"),
        "es": ("Caso", "Valor", "Muestra"),
        "fr": ("Cas", "Valeur", "Échantillon"),
    }[locale]
    pattern = (
        r"\d+ " + re.escape(header_case) + " " + re.escape(header_value)
        + " " + re.escape(native_case) + r" (\d+) \1"
    )
    return [
        physical_page
        for physical_page, page in enumerate(extracted.split("\f"), start=1)
        if re.fullmatch(pattern, " ".join(page.split()))
    ]


def selftest_native_longtable_orphan_guard() -> None:
    """Ensure that real PDF row-only tail pages cannot pass as normal layout."""
    old_en = "35\nCase Value\nSample 85 85\f36\nMain text\n"
    old_es = "35\nCaso Valor\nMuestra 85 85\f36\nTexto principal\n"
    valid = "34\nCaso Valor\nMuestra 83 83\nMuestra 84 84\n\f"
    if orphaned_native_table_pages(old_en, "en") != [1]:
        raise AssertionError("Native table EN orphan regression escaped")
    if orphaned_native_table_pages(old_es, "es") != [1]:
        raise AssertionError("Native table ES orphan regression escaped")
    if orphaned_native_table_pages(valid, "es"):
        raise AssertionError("Normal multirow continuation rejected")


def selftest_geometry_guard() -> None:
    """Ensure the geometric acceptance threshold rejects the known R8 defect."""
    normal_space = 3.2
    r8_bad_space = 51.36
    assert 1.0 <= normal_space <= 9.0
    assert not (1.0 <= r8_bad_space <= 9.0)

    # Exercise the exact XHTML line traversal used for real PDF pages.
    namespace = 'xmlns="http://www.w3.org/1999/xhtml"'
    good = ET.fromstring(
        f'<page {namespace}><line><word>Smith</word>'
        '<word>(2002).</word></line></page>'
    )
    bad = ET.fromstring(
        f'<page {namespace}><line><word>(2002).</word></line></page>'
    )
    word_only = ET.fromstring(
        f'<page {namespace}><word>(2002).</word></page>'
    )
    if isolated_author_year_line_faults(good):
        raise AssertionError("Valid multiword citation was rejected")
    if isolated_author_year_line_faults(bad) != [
            "isolated_author_year_at_line_start"]:
        raise AssertionError("Isolated author-year line escaped detection")
    if isolated_author_year_line_faults(word_only) != [
            "bbox_layout_line_boxes_missing"]:
        raise AssertionError("Word-only bbox XML falsely passed as layout XML")

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
    layout_failures, definition_gap_pt = find_layout_defects(final, loc)
    leaked = [w for w in ("R4-", "R5-", "INTEGRATED-", "INTEGRATED TEST",
                          "R4LONG", "R4NATIVE", "SYNTHETIC-ANON",
                          "INTEGRATED MULTILINGUAL DOCUMENT")
              if w in extracted]
    findings = list(layout_failures)
    native_table_metrics, native_table_findings = native_longtable_pagination(extracted, loc)
    findings.extend(native_table_findings)
    for page_no in orphaned_native_table_pages(extracted, loc):
        findings.append(f"orphan_native_longtable_final_row:physical_page={page_no}")
    if leaked:
        findings.append("fixture_labels_visible:" + ",".join(leaked))
    if loc != "en":
        for english_leak in ("Academic supervisor", "Co-supervisor",
                             "Committee member", "See Equation"):
            if english_leak in extracted:
                findings.append("untranslated_english_label:" + english_leak)
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        # A genuine human-readable sample must show distinct figure/table names.
        names = {
            "pt": ("Malha quadrilateral no domínio unitário",
                   "Configuração de uma malha estruturada"),
            "en": ("Quadrilateral mesh on the unit square",
                   "Structured mesh configuration"),
            "es": ("Malla cuadrilateral en el dominio unitario",
                   "Configuración de una malla estructurada"),
            "fr": ("Maillage quadrilatéral du domaine unité",
                   "Configuration d'un maillage structuré"),
        }[loc]
        # PDF text extraction commonly changes a French apostrophe to U+2019.
        # Normalize punctuation only, without discarding substantive letters.
        rendered = extracted.replace("’", "'").replace("‘", "'")
        if not all(name.replace("’", "'") in rendered for name in names):
            findings.append("distinct_figure_titles_missing")

    # Validate the three defects reported on the printed Portuguese TCC,
    # using extracted text from actual PDFs rather than only TeX predicates.
    compact = re.sub(r"\s+", " ", extracted)
    # PDF fonts can replace apostrophes with typographic U+2019 glyphs.
    compact = compact.replace("’", "'").replace("‘", "'")
    sample_titles = {
        "pt": ("Exemplo de tabela com resultados calculados",
               "Variáveis consideradas na construção das malhas",
               "Fonte: Elaboração própria com dados ilustrativos, 2026"),
        "en": ("Example table of calculated results",
               "Variables used to construct the meshes",
               "Source: Author-generated illustrative data, 2026"),
        "es": ("Ejemplo de tabla con resultados calculados",
               "Resumen de parámetros experimentales",
               "Fuente: Elaboración propia con datos ilustrativos, 2026"),
        "fr": ("Exemple de tableau de résultats calculés",
               "Variables utilisées pour construire les maillages",
               "Source: Élaboration originale avec données illustratives, 2026"),
    }
    table_title, cuadro_title, source_text = sample_titles[loc]
    last_table = compact.rfind(table_title)
    if last_table < 0:
        findings.append("short_table_caption_disfigured_or_missing")
    elif source_text not in compact[last_table:last_table + 340]:
        findings.append("short_table_source_disfigured_or_missing")
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        last_quadro = compact.rfind(cuadro_title)
        if last_quadro < 0:
            findings.append("text_table_caption_disfigured_or_missing")
        elif source_text not in compact[last_quadro:last_quadro + 340]:
            findings.append("text_table_source_disfigured_or_missing")
        institution = {
            "pt": "Universidade Federal do Ceará",
            "en": "Federal University of Ceara",
            "es": "Universidad Federal de Ceará",
            "fr": "Université fédérale du Ceará",
        }[loc]
        for member in ("Alex Ferreira", "Cris Almeida"):
            # The PDF approval-page signature prints the institution directly
            # after each name. A missing metadata key must fail this check.
            # The class now prints the localized advisor/coadvisor role
            # between the person's name and their institution.
            approval = re.escape(member) + r"\s+\([^)]{2,36}\)\s+" + re.escape(institution)
            if not re.search(approval, compact):
                findings.append("approval_institution_missing:" + member)
    if re.search(r"(?<!\.)\.\.(?!\.)", compact):
        findings.append("double_period_from_fixture")

    # Real-PDF checks for the editorial cases requested by the reviewers:
    # original long quotation blocks (never fabricated external sources),
    # correct footnote bodies, and approval signature role names.
    quoted = runpy.run_path(str(ROOT / "tools/review/generate_readable_28.py"))["QUOTE_EXAMPLES"][loc]
    for field in ("heading", "foot_1", "foot_2", "foot_3", "author_note",
                  "source_tail"):
        fragment = quoted[field][:38]
        # Primary headings render in capitals in the UFC profile, whereas
        # explanatory footnote texts preserve their author-provided case.
        if (fragment.casefold() not in compact.casefold()
                if field == "heading" else fragment not in compact):
            findings.append("missing_real_pdf_quotation_or_footnote:" + field)
    for field in ("first", "second"):
        fragment = quoted[field][:40]
        if fragment not in compact:
            findings.append("missing_real_pdf_long_quote:" + field)
    raw_source = src.read_text(encoding="utf-8")

    # A bibliographic synopsis written by this manuscript's author belongs
    # in its appendix. A genuine externally published record belongs in
    # the annex; its provenance is explicitly printed there.
    if loc == "fr" and profile != "scientific-article":
        if "APPENDICE A" not in compact.upper():
            findings.append("french_authored_appendix_not_distinct")
        if "ANNEXE A" not in compact.upper():
            findings.append("french_external_annex_not_distinct")
    if profile != "scientific-article":
        if raw_source.count(r"\begin{verbatim}") != 1 \
                or raw_source.count(r"\end{verbatim}") != 1:
            findings.append("external_original_annex_document_missing")
        if r"\par\autocite{meshBommes2009,meshShewchuk2002}" in raw_source:
            findings.append("orphaned_bibliographic_citation_regression")
        if r"\url{https://cgg.unibe.ch/publications/miq/}" not in raw_source:
            findings.append("external_document_provenance_missing")
        if "@article{Bommes:MIQ" not in compact \
                or "10.1145/1576246.1531383" not in compact:
            findings.append("external_bibliographic_record_missing_from_pdf")
        title = {
            "pt": "Registro bibliográfico externo sobre quadrangulação",
            "en": "External bibliographic record on quadrangulation",
            "es": "Registro bibliográfico externo sobre cuadrangulación",
            "fr": "Notice bibliographique externe sur la quadrangulation",
        }[loc]
        if title.upper() not in compact.upper():
            findings.append("external_annex_title_not_rendered")

    # The original R4 source had a glossary term attached directly to its
    # definition and an English conjunction in non-English manuscripts.
    glued_forms = {
        "pt": ("Malha estruturadaDiscretização",
               "Malha estruturada:Discretização"),
        "en": ("Structured meshA geometric",
               "Structured mesh:A geometric"),
        "es": ("Malla estructuradaUna",
               "Malla estructurada:Una"),
        "fr": ("Maillage structuréDiscrétisation",
               "Maillage structuré:Discrétisation"),
    }[loc]
    if any(form in compact for form in glued_forms):
        findings.append("glossary_term_glued_to_definition")
    if r"\noindent\textbf{" not in raw_source:
        findings.append("natural_flow_definition_not_used")
    if r"\begin{ufcdefinitionlist}[5cm]" in raw_source:
        findings.append("fixed_width_editorial_definition_regression")
    if r"\mbox{\textcite{meshShewchuk2002}}" not in raw_source:
        findings.append("author_year_pair_not_protected")
    if loc != "en" and "and Oliveira" in compact:
        findings.append("untranslated_bibliographic_conjunction")

    if raw_source.count(r"\begin{citacao}") != 2 or \
            raw_source.count(r"\end{citacao}") != 2:
        findings.append("long_citation_environment_missing")
    if raw_source.count(r"\footnote{") < 4:
        findings.append("explicit_footnote_examples_missing")
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        role_labels = {
            "pt": ("Orientador", "Coorientador"),
            "en": ("Advisor", "Coadvisor"),
            "es": ("Director", "Codirector"),
            "fr": ("Directeur", "Codirecteur"),
        }
        # Locale labels are controlled by the class; source metadata must
        # remain independent of the locale's presentation strings.
        approval_text = compact.split("BANCA EXAMINADORA")[-1]
        if loc == "pt" and not all(label in approval_text
                                   for label in role_labels["pt"]):
            findings.append("advisor_roles_not_shown_on_approval")
    if profile in {"undergraduate-capstone", "specialization-capstone",
                   "masters-thesis", "doctoral-thesis"}:
        # Audit the PHYSICAL approval page, never the concatenated PDF text.
        # A seven-member committee previously left the seventh institution
        # orphaned on the next page while the full-text CI falsely passed.
        expected_members = {
            "undergraduate-capstone": 3,
            "specialization-capstone": 3,
            "masters-thesis": 4,
            "doctoral-thesis": 4,
        }[profile]
        heading, university = {
            "pt": ("BANCA EXAMINADORA", "Universidade Federal do Ceará"),
            "en": ("EXAMINING COMMITTEE", "Federal University of Ceara"),
            "es": ("TRIBUNAL EXAMINADOR", "Universidad Federal de Ceará"),
            "fr": ("JURY D'EXAMEN", "Université fédérale du Ceará"),
        }[loc]
        front = subprocess.check_output(
            ["pdftotext", "-f", "1", "-l", "8", str(final), "-"],
            text=True, cwd=ROOT, errors="replace")
        approval_pages = [
            i for i, page in enumerate(front.split("\f"))
            if heading in page.replace("’", "'").replace("‘", "'")
        ]
        if len(approval_pages) != 1:
            findings.append("approval_page_missing_or_duplicated")
        else:
            page_index = approval_pages[0]
            committee_page_text = front.split("\f")[page_index]
            after_heading = committee_page_text.replace("’", "'").split(heading, 1)[1]
            institutional_lines = after_heading.count(university)
            if institutional_lines != expected_members:
                findings.append(
                    "approval_affiliations_not_all_on_same_page:"
                    + str(institutional_lines) + "/"
                    + str(expected_members))
            next_pages = front.split("\f")
            if page_index + 1 < len(next_pages):
                if next_pages[page_index + 1].strip().startswith(university):
                    findings.append("approval_orphan_affiliation_next_page")

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
              "definition_gap_pt": definition_gap_pt,
              "native_longtable_pagination": native_table_metrics,
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
    selftest_geometry_guard()
    selftest_native_longtable_orphan_guard()
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
        "source_commit_sha": (os.environ.get("SOURCE_COMMIT_SHA") or subprocess.check_output(
            ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()),
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
