#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]

LEGACY_PUBLIC = {
    r"\ufcbibliografia": r"\ufcAddBibliographyResource",
    r"\imprimirreferencias": r"\ufcPrintReferences",
    r"\imprimirglossario": r"\ufcPrintGlossary",
    r"\imprimirindice": r"\ufcPrintIndex",
}

LEGACY_HELPERS = (
    r"\ufcPosttextualHeading",
    r"\ufcSetupGlossaryModule",
    r"\ufcIndexHeading",
    r"\ufcSetupIndexModule",
)

CONSUMER_PREFIXES = (
    "template/",
    "tests/",
    "release/ctan/",
)
CONSUMER_EXACT = {"docs/ctan-example.tex"}
TEXT_SUFFIXES = {".tex", ".sh", ".py", ".md"}


def read(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def write(path: str, text: str) -> None:
    (ROOT / path).write_text(text, encoding="utf-8")


def replace_required(path: str, old: str, new: str, expected: int = 1) -> None:
    text = read(path)
    count = text.count(old)
    if count != expected:
        raise SystemExit(f"{path}: expected {expected} occurrence(s) of {old!r}, found {count}")
    write(path, text.replace(old, new))


def tracked_files() -> list[str]:
    out = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    return [item.decode("utf-8") for item in out.split(b"\0") if item]


def grep_inventory(tokens: tuple[str, ...]) -> dict[str, list[str]]:
    inventory: dict[str, list[str]] = {token: [] for token in tokens}
    for path in tracked_files():
        file_path = ROOT / path
        if not file_path.is_file():
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in tokens:
            if token in text:
                inventory[token].append(path)
    return inventory


def is_live_consumer(path: str) -> bool:
    return path in CONSUMER_EXACT or path.startswith(CONSUMER_PREFIXES)


def migrate_consumers() -> None:
    for path in tracked_files():
        file_path = ROOT / path
        if not is_live_consumer(path) or file_path.suffix not in TEXT_SUFFIXES:
            continue
        try:
            text = file_path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        updated = text
        for old, new in LEGACY_PUBLIC.items():
            updated = updated.replace(old, new)
        if updated != text:
            file_path.write_text(updated, encoding="utf-8")
            print(f"migrated consumer: {path}")


def main() -> None:
    all_tokens = tuple(LEGACY_PUBLIC) + LEGACY_HELPERS
    before = grep_inventory(all_tokens)
    print("R2-B4 inventory before migration:")
    for token, paths in before.items():
        print(f"  {token}: {len(paths)}")
        for path in paths:
            print(f"    - {path}")

    replace_required(
        "abntexto-ufc/bibliography.def",
        "\\ProvidesFile{abntexto-ufc/bibliography.def}[2026/08/19 UFC citations and references]",
        "\\ProvidesFile{abntexto-ufc/bibliography.def}[2026/09/03 UFC citations and references]",
    )
    replace_required(
        "abntexto-ufc/bibliography.def",
        "\\NewDocumentCommand \\ufcbibliografia { m }\n  { \\addbibresource{#1} }",
        "\\NewDocumentCommand \\ufcAddBibliographyResource { m }\n  { \\addbibresource{#1} }",
    )
    replace_required(
        "abntexto-ufc/bibliography.def",
        "\\NewDocumentCommand \\imprimirreferencias { }\n  { \\ufc_print_references: }",
        "\\NewDocumentCommand \\ufcPrintReferences { }\n  { \\ufc_print_references: }",
    )

    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\ProvidesFile{abntexto-ufc/backmatter.def}[2026/08/19 UFC post-textual elements]",
        "\\ProvidesFile{abntexto-ufc/backmatter.def}[2026/09/03 UFC post-textual elements]",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\ufcPosttextualHeading { m }\n  { \\ufc_posttextual_heading:n {#1} }\n\n",
        "",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\ufcSetupGlossaryModule { }",
        "\\cs_new_protected:Npn \\ufc_setup_glossary_module:",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\imprimirglossario { }",
        "\\NewDocumentCommand \\ufcPrintGlossary { }",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "{Glossary~requested~without~glossario=glossaries}",
        "{Glossary~requested~without~glossary=glossaries}",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\ufcIndexHeading { m }\n  { \\ufc_posttextual_heading:n {#1} }",
        "\\cs_new_protected:Npn \\ufc_index_heading:n #1\n  { \\ufc_posttextual_heading:n {#1} }",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\ufcSetupIndexModule { }\n  { \\indexsetup{level=\\ufcIndexHeading} }",
        "\\cs_new_protected:Npn \\ufc_setup_index_module:\n  { \\indexsetup{level=\\ufc_index_heading:n} }",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "\\NewDocumentCommand \\imprimirindice { }",
        "\\NewDocumentCommand \\ufcPrintIndex { }",
    )
    replace_required(
        "abntexto-ufc/backmatter.def",
        "{Index~requested~without~indice=imakeidx}",
        "{Index~requested~without~index=imakeidx}",
    )

    replace_required(
        "abntexto-ufc/modules.def",
        "\\ufcSetupGlossaryModule",
        "\\ufc_setup_glossary_module:",
    )
    replace_required(
        "abntexto-ufc/modules.def",
        "\\ufcSetupIndexModule",
        "\\ufc_setup_index_module:",
    )

    # The normative centering fixture used an internal back-matter heading helper as
    # a synthetic surface. Exercise the same shared heading behavior through the
    # supported index API instead, preserving the three-surface normative proof.
    fixture = "tests/documents/mainmatter-section-unnumbered-centered-test.tex"
    replace_required(
        fixture,
        "  coat-of-arms = false\n}",
        "  coat-of-arms = false,\n  index = imakeidx\n}",
    )
    replace_required(
        fixture,
        "\\section{UCCENTERCONTEXT}\n\\nocite{silva2020}",
        "\\section{UCCENTERCONTEXT}\n\\index{UCINDEXENTRY}\n\\nocite{silva2020}",
    )
    replace_required(
        fixture,
        "\\ufcPosttextualHeading{UCPOSTCENTER}\nUCPOSTCENTERBODY",
        "\\ufcPrintIndex",
    )

    scenario = "standards/section-unnumbered-centered-scenario.json"
    replace_required(
        scenario,
        '      "marker": "UCPOSTCENTER",\n      "implementation": "ufc_backmatter_heading"',
        '      "marker": "ÍNDICE",\n      "implementation": "ufc_index_heading"',
    )

    integration = "tests/integration/section-unnumbered-centered-evidence.sh"
    replace_required(
        integration,
        'biber_log="/tmp/abntexto-ufc-v2-section-unnumbered-centered-biber.log"',
        'biber_log="/tmp/abntexto-ufc-v2-section-unnumbered-centered-biber.log"\nindex_log="/tmp/abntexto-ufc-v3-section-unnumbered-centered-index.log"',
    )
    replace_required(
        integration,
        '        "$job.out" "$job.pdf" "$job.run.xml" "$job.toc"',
        '        "$job.idx" "$job.ilg" "$job.ind" "$job.out" "$job.pdf" "$job.run.xml" "$job.toc"',
    )
    replace_required(
        integration,
        '\nbiber "$job" > "$biber_log" 2>&1 || {',
        '\nmakeindex "$job" > "$index_log" 2>&1 || {\n  cat "$index_log"\n  exit 1\n}\n\nbiber "$job" > "$biber_log" 2>&1 || {',
    )

    migrate_consumers()

    public_api = """\\ProvidesFile{abntexto-ufc/public-api.def}[2026/09/03 UFC transitional public API]\n\n% R2-B1 through R2-B4 forwarding has been absorbed by direct behavior owners.\n% This empty transitional file is intentionally retained until R2-B5 removes the\n% forwarding layer from the class load path and closes the residual migration.\n\n\\endinput\n"""
    write("abntexto-ufc/public-api.def", public_api)

    after = grep_inventory(all_tokens)
    print("R2-B4 inventory after migration:")
    forbidden_prefixes = ("abntexto-ufc/", "template/", "tests/", "release/ctan/")
    forbidden_exact = {"docs/ctan-example.tex"}
    residuals: list[tuple[str, str]] = []
    for token, paths in after.items():
        print(f"  {token}: {len(paths)}")
        for path in paths:
            print(f"    - {path}")
            if path in forbidden_exact or path.startswith(forbidden_prefixes):
                residuals.append((token, path))
    if residuals:
        lines = "\n".join(f"{token}: {path}" for token, path in residuals)
        raise SystemExit(f"B4 live-tree residuals remain:\n{lines}")

    public_api_text = read("abntexto-ufc/public-api.def")
    for command in LEGACY_PUBLIC.values():
        if command in public_api_text:
            raise SystemExit(f"public-api.def still forwards {command}")

    print("R2-B4 migration completed without live-tree residuals.")


if __name__ == "__main__":
    main()
