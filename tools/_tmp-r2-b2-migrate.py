from __future__ import annotations

from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[1]

B2_COMMANDS = {
    r"\imprimircapa": r"\ufcPrintCover",
    r"\imprimirfolhaderosto": r"\ufcPrintTitlePage",
    r"\imprimirfolhadeaprovacao": r"\ufcPrintApprovalPage",
    r"\imprimirfichacatalografica": r"\ufcPrintCatalogCard",
    r"\imprimirdedicatoria": r"\ufcPrintDedication",
    r"\imprimiragradecimentos": r"\ufcPrintAcknowledgments",
    r"\imprimirepigrafe": r"\ufcPrintEpigraph",
    r"\imprimirerrata": r"\ufcPrintErrata",
    r"\palavraschave": r"\ufcSummaryKeywords",
    r"\imprimirresumo": r"\ufcPrintSummary",
    r"\imprimirabstract": r"\ufcPrintAbstract",
    r"\imprimirlistadeilustracoes": r"\ufcPrintListOfIllustrations",
    r"\imprimirlistadefiguras": r"\ufcPrintListOfFigures",
    r"\imprimirlistadetabelas": r"\ufcPrintListOfTables",
    r"\imprimirlistadequadros": r"\ufcPrintListOfTextTables",
    r"\imprimirlistadeabreviaturasesiglas": r"\ufcPrintListOfAbbreviationsAndAcronyms",
    r"\imprimirlistadesimbolos": r"\ufcPrintListOfSymbols",
    r"\ufclistaentrada": r"\ufcListEntry",
    r"\imprimirsumario": r"\ufcPrintTableOfContents",
}

B2_CANONICAL = {
    r"\ufcPrintCover",
    r"\ufcPrintTitlePage",
    r"\ufcPrintApprovalPage",
    r"\ufcPrintCatalogCard",
    r"\ufcPrintDedication",
    r"\ufcPrintAcknowledgments",
    r"\ufcPrintEpigraph",
    r"\ufcPrintErrata",
    r"\ufcSummaryKeywords",
    r"\ufcPrintSummary",
    r"\ufcPrintAbstract",
    r"\ufcPrintListOfIllustrations",
    r"\ufcPrintListOfFigures",
    r"\ufcPrintListOfTables",
    r"\ufcPrintListOfTextTables",
    r"\ufcPrintListOfAbbreviationsAndAcronyms",
    r"\ufcPrintListOfSymbols",
    r"\ufcListEntry",
    r"\ufcPrintTableOfContents",
}

TEXT_SUFFIXES = {".tex", ".def", ".cls", ".py", ".sh", ".md", ".json", ".yml", ".yaml", ".js", ".html"}
ACTIVE_ROOTS = [
    ROOT / "template",
    ROOT / "tests",
    ROOT / "tools",
    ROOT / "validator",
    ROOT / "standards",
    ROOT / "release" / "ctan",
]
ACTIVE_FILES = [ROOT / "README.md", ROOT / "docs" / "ctan-example.tex"]
OWNER_FILES = [
    ROOT / "abntexto-ufc" / "academic-works.def",
    ROOT / "abntexto-ufc" / "research-projects.def",
    ROOT / "abntexto-ufc" / "frontmatter.def",
    ROOT / "abntexto-ufc" / "layout.def",
]
PUBLIC_API = ROOT / "abntexto-ufc" / "public-api.def"
TEMP_FILES = [ROOT / "tools" / "_tmp-r2-b2-migrate.py", ROOT / ".github" / "workflows" / "_tmp-r2-b2-migrate.yml"]


def replace_commands(text: str) -> str:
    for old, new in B2_COMMANDS.items():
        text = text.replace(old, new)
    text = text.replace(r"\ufcPrintEpigraph[curta]", r"\ufcPrintEpigraph[short]")
    text = text.replace(r"\ufcPrintEpigraph[longa]", r"\ufcPrintEpigraph[long]")
    return text


def write_if_changed(path: Path, text: str) -> bool:
    old = path.read_text(encoding="utf-8")
    if old == text:
        return False
    path.write_text(text, encoding="utf-8")
    print(f"updated {path.relative_to(ROOT)}")
    return True


def migrate_owner(path: Path) -> None:
    text = path.read_text(encoding="utf-8")
    text = replace_commands(text)
    if path.name == "frontmatter.def":
        text = text.replace(r"\NewDocumentCommand \ufcPrintEpigraph { O{curta} m }", r"\NewDocumentCommand \ufcPrintEpigraph { O{short} m }")
        text = text.replace("{curta} { \\ufc_epigraph_short:n", "{short} { \\ufc_epigraph_short:n")
        text = text.replace("{longa} { \\ufc_epigraph_long:n", "{long} { \\ufc_epigraph_long:n")
        text = text.replace(r"\string\ufcPrintEpigraph[curta]", r"\string\ufcPrintEpigraph[short]")
        text = text.replace(r"\string\ufcPrintEpigraph[longa]", r"\string\ufcPrintEpigraph[long]")
    write_if_changed(path, text)


def prune_public_api() -> None:
    text = PUBLIC_API.read_text(encoding="utf-8")
    paragraphs = text.split("\n\n")
    kept: list[str] = []
    removed: list[str] = []
    for paragraph in paragraphs:
        matches = sorted(cmd for cmd in B2_CANONICAL if cmd in paragraph)
        if matches:
            removed.extend(matches)
            continue
        kept.append(paragraph)
    missing = sorted(B2_CANONICAL - set(removed))
    if missing:
        raise SystemExit(f"public-api.def did not contain expected B2 forwards: {missing}")
    text = "\n\n".join(kept)
    text = text.replace(
        "% Canonical commands still forward to Portuguese project-owned behavior.\n% These forwarding entries are removed by the bounded R2-B2 through R2-B4 lots.",
        "% Remaining transitional forwards belong only to the bounded R2-B3 and R2-B4 lots.",
    )
    write_if_changed(PUBLIC_API, text)


def iter_active_files():
    seen: set[Path] = set()
    for root in ACTIVE_ROOTS:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix.lower() in TEXT_SUFFIXES:
                if path in TEMP_FILES:
                    continue
                if path not in seen:
                    seen.add(path)
                    yield path
    for path in ACTIVE_FILES:
        if path.exists() and path not in seen:
            yield path


def migrate_consumers() -> None:
    owner_set = set(OWNER_FILES)
    for path in iter_active_files():
        if path in owner_set or path == PUBLIC_API:
            continue
        text = path.read_text(encoding="utf-8")
        new = replace_commands(text)
        write_if_changed(path, new)


def assert_direct_ownership() -> None:
    ownership = {
        ROOT / "abntexto-ufc" / "academic-works.def": [r"\ufcPrintCover", r"\ufcPrintTitlePage", r"\ufcPrintCatalogCard"],
        ROOT / "abntexto-ufc" / "frontmatter.def": [
            r"\ufcPrintApprovalPage", r"\ufcPrintDedication", r"\ufcPrintAcknowledgments",
            r"\ufcPrintEpigraph", r"\ufcPrintErrata", r"\ufcSummaryKeywords", r"\ufcPrintSummary",
            r"\ufcPrintAbstract", r"\ufcPrintListOfIllustrations", r"\ufcPrintListOfFigures",
            r"\ufcPrintListOfTables", r"\ufcPrintListOfTextTables", r"\ufcPrintListOfAbbreviationsAndAcronyms",
            r"\ufcPrintListOfSymbols", r"\ufcListEntry", r"\ufcPrintTableOfContents",
        ],
        ROOT / "abntexto-ufc" / "research-projects.def": [r"\ufcPrintCover", r"\ufcPrintTitlePage"],
    }
    for path, commands in ownership.items():
        text = path.read_text(encoding="utf-8")
        for command in commands:
            if command not in text:
                raise SystemExit(f"missing direct owner {command} in {path.relative_to(ROOT)}")

    pub = PUBLIC_API.read_text(encoding="utf-8")
    leaked = sorted(cmd for cmd in B2_CANONICAL if cmd in pub)
    if leaked:
        raise SystemExit(f"B2 forwards still present in public-api.def: {leaked}")


def residual_scan() -> None:
    scan_paths = OWNER_FILES + [PUBLIC_API] + list(iter_active_files())
    failures: list[str] = []
    for path in scan_paths:
        text = path.read_text(encoding="utf-8")
        for old in B2_COMMANDS:
            if old in text:
                failures.append(f"{path.relative_to(ROOT)}: {old}")
        if r"\ufcPrintEpigraph[curta]" in text or r"\ufcPrintEpigraph[longa]" in text:
            failures.append(f"{path.relative_to(ROOT)}: legacy epigraph value")
        if path == ROOT / "abntexto-ufc" / "frontmatter.def" and ("O{curta}" in text or "{curta} { \\ufc_epigraph_short:n" in text or "{longa} { \\ufc_epigraph_long:n" in text):
            failures.append(f"{path.relative_to(ROOT)}: legacy epigraph owner value")
    if failures:
        raise SystemExit("R2-B2 residual scan failed:\n" + "\n".join(failures))
    print("R2-B2 residual scan: PASS")


def run(*args: str) -> None:
    print("+", " ".join(args))
    subprocess.run(args, cwd=ROOT, check=True)


def main() -> None:
    prune_public_api()
    for path in OWNER_FILES:
        migrate_owner(path)
    migrate_consumers()
    assert_direct_ownership()
    residual_scan()

    # Remove the temporary executor before repository contract/static checks.
    for path in TEMP_FILES:
        if path.exists():
            path.unlink()
            print(f"removed {path.relative_to(ROOT)}")

    run("make", "static-check")
    run("git", "diff", "--check")
    print("R2-B2 bounded migration: PASS")


if __name__ == "__main__":
    try:
        main()
    except subprocess.CalledProcessError as exc:
        sys.exit(exc.returncode)
