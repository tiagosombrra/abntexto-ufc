#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = {
    "abntexto-ufc.cls",
    "abntexto-ufc/integrations/abntexto.def",
    "abntexto-ufc/standards/nbr6023-2025.def",
    "template/main.tex",
    "tests/run.py",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "release/v3-roadmap.json",
}

FORBIDDEN_EXACT_PATHS = {
    "ufctex.cls",
    "docs/B2R-NAMING-INVENTORY.md",
    "docs/HANDOFF-V2.2.0.md",
    "docs/NAMING.md",
    "release/final-audit.json",
    "release/n15-b1-source-authority.json",
    "release/n15-b2a-article-contract.json",
    "release/n15-b2r-a-naming-inventory.json",
    "release/n15-b2r-b-public-api.json",
    "release/n15-b2r-b2-setup-aliases.json",
    "release/n15-b2r-b3-command-environment-aliases.json",
    "release/n15-b2r-b4-en-pt-equivalence.json",
    "tests/checks/public_api_contract.py",
    "tests/checks/normative_article_contract.py",
    "tests/checks/normative_final_audit.py",
    "tests/checks/normative_source_authority.py",
}

FORBIDDEN_PREFIXES = (
    "docs/history/",
    "release/history/",
    "standards/history/",
    "normativa/",
    "tests/normativa/",
    "tests/fixtures/pretextuais/",
)

FORBIDDEN_PATH_SEGMENT = re.compile(
    r"(?:^|/)(?:v2(?:[-_.]|$)|n(?:9|10|11|12|13|14|15)(?:[-_.]|$)|b2r(?:[-_.]|$))",
    re.IGNORECASE,
)

PORTUGUESE_TECHNICAL_PATH_TOKENS = {
    "normas",
    "vigencia-normativa",
    "pretextuais",
    "pos-textuais",
    "pós-textuais",
    "textual-oracle",
}

GENERATED_SUFFIXES = {
    ".aux",
    ".bbl",
    ".bcf",
    ".blg",
    ".fdb_latexmk",
    ".fls",
    ".glg",
    ".glo",
    ".gls",
    ".idx",
    ".ilg",
    ".ind",
    ".lof",
    ".log",
    ".lot",
    ".out",
    ".pdf",
    ".pyc",
    ".run.xml",
    ".synctex.gz",
    ".toc",
    ".zip",
}

TEXT_SUFFIXES = {
    ".bib",
    ".cls",
    ".def",
    ".json",
    ".md",
    ".ps1",
    ".py",
    ".sh",
    ".tex",
    ".toml",
    ".txt",
    ".yaml",
    ".yml",
}

STALE_CONTENT_FRAGMENTS = (
    "normativa/",
    "tests/normativa/",
    "tests/fixtures/pretextuais/",
    "docs/history/",
    "release/history/",
    "standards/history/",
    "ufctex.cls",
)

CONTENT_SCAN_EXEMPT = {
    "docs/ROADMAP-V3.0.0.md",
    "docs/HANDOFF-V3.0.0.md",
    "release/v3-path-migration.json",
    "release/v3-api-migration.json",
    "release/v3-test-migration.json",
    # This checker defines the forbidden literals above; scanning its own
    # source would report those policy definitions as active stale references.
    "tests/checks/repository_contract.py",
}

# These active technical/documentation surfaces intentionally name the removed
# class entrypoint only to assert that it must remain absent.
NEGATIVE_FRAGMENT_EXEMPT = {
    "docs/ARCHITECTURE.md": {"ufctex.cls"},
    "tests/checks/canonical_identity.py": {"ufctex.cls"},
    "tests/checks/repository_contract.py": {"ufctex.cls"},
}

MODULE_PATTERN = re.compile(r"\\input\{((?:abntexto-ufc)/[^}]+\.def)\}")


def tracked_paths() -> list[str]:
    output = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", "ls-files", "-z"],
        cwd=ROOT,
    )
    return [item.decode("utf-8") for item in output.split(b"\0") if item]


def read_text(path: str) -> str | None:
    candidate = ROOT / path
    if candidate.name in {"Makefile", "LICENSE"} or candidate.suffix.lower() in TEXT_SUFFIXES:
        try:
            return candidate.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            return None
    return None


def main() -> int:
    errors: list[str] = []
    paths = tracked_paths()
    path_set = set(paths)

    for required in sorted(REQUIRED_PATHS - path_set):
        errors.append(f"missing required path: {required}")

    for path in paths:
        lower = path.lower()

        if path in FORBIDDEN_EXACT_PATHS:
            errors.append(f"obsolete active path: {path}")
        if any(path.startswith(prefix) for prefix in FORBIDDEN_PREFIXES):
            errors.append(f"forbidden archive/legacy prefix: {path}")
        if FORBIDDEN_PATH_SEGMENT.search(path):
            errors.append(f"phase/version engineering identity remains in active path: {path}")

        components = {component.lower() for component in Path(path).parts}
        stem = Path(path).stem.lower()
        if components & PORTUGUESE_TECHNICAL_PATH_TOKENS or stem in PORTUGUESE_TECHNICAL_PATH_TOKENS:
            errors.append(f"Portuguese technical path remains active: {path}")

        if any(lower.endswith(suffix) for suffix in GENERATED_SUFFIXES):
            errors.append(f"generated artifact is tracked: {path}")

        if path in CONTENT_SCAN_EXEMPT:
            continue
        text = read_text(path)
        if text is None:
            continue
        allowed_fragments = NEGATIVE_FRAGMENT_EXEMPT.get(path, set())
        for fragment in STALE_CONTENT_FRAGMENTS:
            if fragment in allowed_fragments:
                continue
            if fragment in text:
                errors.append(f"{path}: stale active path reference: {fragment}")

    class_text = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    modules = MODULE_PATTERN.findall(class_text)
    if not modules:
        errors.append("abntexto-ufc.cls: no canonical modules are loaded")
    for module in modules:
        if module not in path_set:
            errors.append(f"abntexto-ufc.cls: missing loaded module: {module}")
    if "ufctex" in class_text.lower():
        errors.append("abntexto-ufc.cls: deprecated ufctex identity remains")

    if errors:
        print("Repository contract failed:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(
        "REPOSITORY-EVIDENCE status=PASS "
        f"tracked_files={len(paths)} history_directories=0 legacy_class=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
