#!/usr/bin/env python3
"""Build editable, four-language academic mesh examples distinct from R4 fixtures.

Generated sources reuse the canonical deterministic geometry but are not
evidence of novel results, institutional approval, or PDF/A conformance.
All TeX paths are relative to the repository root.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CONTENT = ROOT / "examples/public-mesh-documents/content.json"
STUDY = ROOT / "examples/canonical-mesh-study/study.json"
CANONICAL_GENERATOR = ROOT / "tools/examples/generate_mesh_study.py"
CANONICAL_ASSETS = Path("artifacts/canonical-mesh-study")
DEFAULT_OUTPUT = Path("artifacts/public-mesh-documents")
LOCALES = ("pt", "en", "es", "fr")
PROFILES = (
    "undergraduate-capstone", "specialization-capstone", "masters-thesis",
    "doctoral-thesis", "research-project", "anonymized-research-project",
    "scientific-article",
)
PROJECTS = {"research-project", "anonymized-research-project"}
ACADEMIC = set(PROFILES) - PROJECTS - {"scientific-article"}
PROPOSALS = PROJECTS
FORBIDDEN = (
    "INTEGRATED-", "R4-METHOD-", "R4SHORT-", "R4LONG-",
    "SYNTHETIC-ANON", "INTEGRATED TEST AUTHOR",
)


def digest(raw: bytes) -> str:
    """Bind every manuscript and supporting file to its source bytes."""
    return hashlib.sha256(raw).hexdigest()


def line(value: str) -> str:
    """Avoid LaTeX-command injection in externally editable prose fields."""
    if not isinstance(value, str) or not value.strip():
        raise ValueError("Empty text field")
    if any(char in value for char in ("\\", "{", "}", "%", "#", "&", "$", "_", "^", "~")):
        raise ValueError(f"Unescaped TeX control in user-facing content: {value[:35]!r}")
    if any(marker.casefold() in value.casefold() for marker in FORBIDDEN):
        raise ValueError("An R4 synthetic fixture marker leaked into public content")
    return value


def tex_config(profile: str, locale: str, data: dict) -> str:
    """Keep institution legal identity distinct from translated display text."""
    anonymized = profile == "anonymized-research-project"
    institution = ("Instituição não identificada" if anonymized
                   else "Universidade Federal do Ceará")
    presentation = institution if anonymized else data["institution_display"]
    program, degree, spec, graduate, field = (line(x) for x in data["programs"])
    author = "" if anonymized else line(data["author"])
    options = {
        "type": profile,
        "document-language": locale,
        "print-mode": "single-sided",
        "cover": "false" if profile in {"scientific-article", "anonymized-research-project"} else "true",
        "coat-of-arms": "false",
        "catalog-card": "false",
        "author": "{" + author + "}",
        "title": "{" + line(data["proposal_title"] if profile in PROJECTS else data["title"]) + "}",
        "institution": "{" + institution + "}",
        "institution-display": "{" + presentation + "}",
        "location": "{Fortaleza}",
        "year": "{2026}",
        "approval-date": "{2026}",
        "submission-date": "{2026}",
        "article-author-note": "{" + line(data["article_note"]) + "}",
        "advisor": "{" + ("" if anonymized else line(data["advisor"])) + "}",
        "undergraduate-program": "{" + program + "}",
        "undergraduate-degree": "{" + degree + "}",
        "specialization-program": "{" + spec + "}",
        "masters-graduate-program": "{" + graduate + "}",
        "masters-program": "{" + graduate + "}",
        "masters-degree-field": "{" + field + "}",
        "doctoral-graduate-program": "{" + graduate + "}",
        "doctoral-program": "{" + graduate + "}",
        "doctoral-degree-field": "{" + field + "}",
        "project-program": "{" + line(data["project_program"]) + "}",
        "submission-entity": "{" + institution + "}",
        "submission-entity-display": "{" + presentation + "}",
    }
    if profile in ACADEMIC:
        options["examiner-2"] = "{" + line(data["examiner"]) + "}"
        options["examiner-2-institution"] = "{Universidade Federal do Ceará}"
        options["examiner-3"] = "{" + line(data["examiner"]) + "}"
        options["examiner-3-institution"] = "{Universidade Federal do Ceará}"
    return "\n".join(f"  {key}={value}{',' if i < len(options)-1 else ''}"
                     for i, (key, value) in enumerate(options.items()))


def summary(locale: str, content: dict) -> str:
    """Render one original summary with its own language-specific keywords."""
    d = content["locales"][locale]
    return (line(d["abstract"]) + "\n\n"
            + rf"\ufcSummaryKeywordsInLanguage{{{locale}}}{{{line(d['keywords'])}}}" + "\n")


def manuscript(profile: str, locale: str, content: dict, output: Path) -> tuple[str, dict[str, str]]:
    """Use genuine mathematical content and a distinct profile-specific argument."""
    d = content["locales"][locale]
    companion = "en" if locale == "pt" else "pt"
    headings = [line(x) for x in d["headings"]]
    specific = line(content["profile_context"][profile][locale])
    appendix = output / locale / f"{profile}-summary.tex"
    companion_path = output / locale / f"{profile}-companion.tex"
    support = {}
    if profile in ACADEMIC:
        support[str(appendix)] = summary(locale, content)
        support[str(companion_path)] = summary(companion, content)
    lines = [
        "% Editable public academic example. NOT the R4 regression test fixture.",
        "% Compile from the repository root after generating canonical mesh assets.",
        rf"\DocumentMetadata{{lang={d['lang']},pdfstandard=A-2b,pdfversion=1.7}}",
        r"\documentclass{abntexto-ufc}",
        r"\usepackage{graphicx}",
        r"\usepackage{amsmath}",
        r"\usepackage{booktabs}",
        r"\ufcsetup{",
        tex_config(profile, locale, d),
        "}",
        r"\ufcAddBibliographyResource{examples/canonical-mesh-study/references.bib}",
        r"\begin{document}",
    ]
    if profile == "scientific-article":
        lines.append(
            r"\ufcPrintArticleFrontMatter{"
            + line(d["abstract"])
            + rf" \ufcSummaryKeywordsInLanguage{{{locale}}}{{{line(d['keywords'])}}}"
            + "}"
        )
        lines.append(
            rf"\ufcPrintArticleTranslatedSummary{{{companion}}}{{"
            + line(content["locales"][companion]["abstract"])
            + rf" \ufcSummaryKeywordsInLanguage{{{companion}}}{{{line(content['locales'][companion]['keywords'])}}}"
            + "}"
        )
    else:
        lines += [
            r"\pretextual",
        ]
        if profile != "anonymized-research-project":
            lines.append(r"\ufcPrintCover")
        lines.append(r"\ufcPrintTitlePage")
        if profile in ACADEMIC:
            lines += [
                r"\ufcPrintApprovalPage",
                rf"\ufcPrintRequiredSummaries{{{appendix.as_posix()}}}"
                + "{" + companion_path.as_posix() + "}",
            ]
        lines += [
            r"\ufcPrintListOfFigures",
            r"\ufcPrintListOfTables",
            r"\ufcPrintTableOfContents",
        ]
    lines += [
        r"\textual",
        rf"\section{{{headings[0]}}}",
        line(d["introduction"]),
        rf"\section{{{headings[1]}}}",
        line(d["objective"]),
        specific,
        rf"\section{{{headings[2]}}}",
        rf"\input{{{CANONICAL_ASSETS.as_posix()}/body-{locale}.tex}}",
        rf"\section{{{headings[3]}}}",
        line(d["discussion"]),
        specific,
        rf"\section{{{headings[4]}}}",
        line(d["proposal_conclusion"] if profile in PROPOSALS else d["conclusion"]),
        r"\ufcPrintReferences",
        r"\end{document}",
    ]
    tex = "\n\n".join(lines) + "\n"
    for marker in FORBIDDEN:
        if marker.casefold() in tex.casefold():
            raise ValueError(f"Public example contains synthetic fixture marker: {marker}")
    return tex, support


def build(content: dict, output: Path) -> dict[str, bytes]:
    """Materialize a deterministic 28-source matrix without compiling PDFs."""
    if content.get("schema_version") != 1:
        raise ValueError("Unsupported public document content schema")
    if set(content["profile_context"]) != set(PROFILES):
        raise ValueError("Seven academic profiles are mandatory")
    if set(content["locales"]) != set(LOCALES):
        raise ValueError("Four manuscript languages are mandatory")
    built = {}
    inventory = []
    for locale in LOCALES:
        for profile in PROFILES:
            value = content["profile_context"][profile]
            if set(value) != set(LOCALES) or any(len(line(v)) < 100 for v in value.values()):
                raise ValueError(f"Incomplete genre-specific content: {profile}")
            source, extras = manuscript(profile, locale, content, output)
            name = output / locale / f"{profile}.tex"
            built[str(name)] = source.encode("utf-8")
            for path, value in extras.items():
                built[path] = value.encode("utf-8")
            inventory.append({
                "profile": profile, "locale": locale,
                "source": str(name),
                "source_sha256": digest(source.encode("utf-8")),
                "support": {path: digest(value.encode("utf-8")) for path, value in extras.items()},
                "status": "SOURCE_ONLY_PDF_UNVERIFIED",
                "human_approval": "PENDING",
            })
    manifest = {
        "schema_version": 1,
        "source_study_sha256": digest(STUDY.read_bytes()),
        "public_content_sha256": digest(CONTENT.read_bytes()),
        "generator_sha256": digest(Path(__file__).read_bytes()),
        "example_count": 28,
        "test_fixture_separated": True,
        "no_fabricated_scientific_novelty": True,
        "pdf_certified": False,
        "publication_authorized": False,
        "entries": inventory,
    }
    built[str(output / "manifest.json")] = (json.dumps(
        manifest, ensure_ascii=False, indent=2) + "\n").encode("utf-8")
    return built


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    if not args.output.is_absolute():
        args.output = ROOT / args.output
    if not args.check:
        subprocess.run([
            sys.executable, str(CANONICAL_GENERATOR),
            "--output", str(ROOT / CANONICAL_ASSETS),
        ], cwd=ROOT, check=True)
    content = json.loads(CONTENT.read_text(encoding="utf-8"))
    generated = build(content, args.output)
    if args.check:
        actual = {str(p) for p in args.output.rglob("*") if p.is_file()}
        if actual != set(generated):
            raise SystemExit(f"PUBLIC-EXAMPLES-FAIL source_set: missing={sorted(set(generated)-actual)} "
                             f"extra={sorted(actual-set(generated))}")
        for path, expected in generated.items():
            if Path(path).read_bytes() != expected:
                raise SystemExit(f"PUBLIC-EXAMPLES-FAIL source_changed={path}")
        print("PUBLIC-EXAMPLES-EVIDENCE status=PASS sources=28 languages=4 profiles=7 "
              "public_source_only=true release_authorized=false")
    else:
        for path, value in generated.items():
            target = Path(path)
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(value)
        print("PUBLIC-EXAMPLES-WRITTEN sources=28 languages=4 profiles=7 "
              "pdf_certification=NOT_YET")


if __name__ == "__main__":
    main()
