#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

SUITES: dict[str, tuple[str, ...]] = {
    "complete": ("*",),
    "smoke": ("repository", "validator-source", "reference", "pdf-validator"),
    "reference-document": ("reference", "reference-corpus", "pdf-validator"),
    "reference-pdf": (
        "reference",
        "reference-corpus",
        "pdf-validator",
        "layout",
        "font-config",
        "pdf-validation-core",
        "pdf-geometry",
        "frontmatter",
        "duplex-frontmatter",
        "object-geometry",
        "table-ibge",
        "documentary-source",
        "bibliography",
        "reference-spacing",
        "backmatter",
        "duplex-backmatter",
    ),
    "frontmatter": ("frontmatter", "duplex-frontmatter"),
    "layout": (
        "layout",
        "font-config",
        "pdf-validation-core",
        "pdf-geometry",
        "math",
        "normative-complement",
    ),
    "objects": (
        "object-geometry",
        "code-typography",
        "table-ibge",
        "objects",
        "minted",
        "algorithm-numbering",
        "documentary-source",
    ),
    "bibliography": ("bibliography", "reference-spacing", "normative-complement"),
    "backmatter": ("backmatter", "duplex-backmatter"),
    "research-project": ("research-project",),
    "profiles": ("profiles", "build-path", "multivolume", "catalog-card"),
    # Before Scientific Article runtime exists this suite deliberately validates
    # only the retained article authority/source contract through validator-source.
    # The static suite contract requires an article-specific executable check to
    # be added here when the roadmap enters Scientific Article.
    "article": ("validator-source",),
}

SUITE_ORDER = tuple(SUITES)

DOC_ONLY_EXACT = {
    "README.md",
    "AGENTS.md",
    "LICENSE",
    ".gitignore",
    "release/v3-roadmap.json",
}
DOC_ONLY_PREFIXES = ("docs/",)

ORCHESTRATION_EXACT = {
    ".github/workflows/linux-integration.yml",
    "tests/run.py",
    "tests/static.py",
    "tests/integration_suites.py",
    "tests/checks/linux_integration_suites.py",
}

FORCE_COMPLETE_EXACT = {
    "Makefile",
    "abntexto-ufc.cls",
    "abntexto-ufc/core.def",
    "abntexto-ufc/fonts.def",
    "abntexto-ufc/modules.def",
}
FORCE_COMPLETE_PREFIXES = (
    "abntexto-ufc/integrations/",
    "standards/",
)

PATH_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("article", ("abntexto-ufc/article", "tests/integration/article", "tests/documents/article", "standards/article")),
    ("frontmatter", ("abntexto-ufc/frontmatter.def", "abntexto-ufc/academic-works.def", "template/frontmatter/", "tests/integration/frontmatter", "tests/integration/duplex-frontmatter")),
    ("layout", ("abntexto-ufc/layout.def", "tests/integration/layout", "tests/integration/pdf-geometry", "tests/integration/pdf-validation-core", "tests/integration/math", "tests/integration/normative-complement")),
    ("objects", ("abntexto-ufc/objects.def", "tests/integration/object", "tests/integration/table-ibge", "tests/integration/minted", "tests/integration/algorithm-numbering", "tests/integration/documentary-source")),
    ("bibliography", ("abntexto-ufc/bibliography.def", "abntexto-ufc/standards/nbr6023-2025.def", "template/backmatter/references.bib", "tests/integration/bibliography", "tests/integration/reference-spacing")),
    ("backmatter", ("abntexto-ufc/backmatter.def", "tests/integration/backmatter", "tests/integration/duplex-backmatter")),
    ("research-project", ("abntexto-ufc/research-projects.def", "tests/integration/research-project")),
    ("profiles", ("tests/integration/profile-matrix", "tests/integration/build-path", "tests/integration/multivolume", "tests/integration/catalog-card", "tests/smoke/base-profile.tex")),
    ("reference-document", ("template/main.tex", "template/chapters/", "tests/integration/reference-document", "tests/integration/reference-corpus", "tests/integration/pdf-validator")),
)


def is_docs_only(path: str) -> bool:
    return path in DOC_ONLY_EXACT or path.startswith(DOC_ONLY_PREFIXES)


def matching_suites(path: str) -> set[str]:
    matched: set[str] = set()
    for suite, patterns in PATH_RULES:
        if any(path == pattern or path.startswith(pattern) for pattern in patterns):
            matched.add(suite)
    return matched


def infer_suites(paths: list[str]) -> tuple[str, ...]:
    technical = [path for path in paths if path and not is_docs_only(path)]
    if not technical:
        return ()

    if any(path in ORCHESTRATION_EXACT for path in technical):
        orchestration_only = all(
            path in ORCHESTRATION_EXACT or is_docs_only(path)
            for path in paths
            if path
        )
        if orchestration_only:
            return ("smoke",)

    if any(path in FORCE_COMPLETE_EXACT or path.startswith(FORCE_COMPLETE_PREFIXES) for path in technical):
        return ("complete",)

    selected: set[str] = set()
    for path in technical:
        matched = matching_suites(path)
        if not matched:
            return ("complete",)
        selected.update(matched)

    return tuple(name for name in SUITE_ORDER if name in selected)


def git_changed_paths(base: str, head: str) -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        raise SystemExit(completed.stderr.strip() or "git diff failed")
    return [line.strip() for line in completed.stdout.splitlines() if line.strip()]


def self_test() -> None:
    cases = {
        ("docs/ROADMAP-V3.0.0.md",): (),
        ("abntexto-ufc/objects.def",): ("objects",),
        ("abntexto-ufc/bibliography.def",): ("bibliography",),
        ("abntexto-ufc/frontmatter.def",): ("frontmatter",),
        ("tests/run.py",): ("smoke",),
        ("tests/integration/article-runtime.sh",): ("article",),
        ("abntexto-ufc/objects.def", "abntexto-ufc/bibliography.def"): ("objects", "bibliography"),
        ("abntexto-ufc/core.def",): ("complete",),
        ("unknown/technical.file",): ("complete",),
    }
    for paths, expected in cases.items():
        measured = infer_suites(list(paths))
        if measured != expected:
            raise SystemExit(
                f"Linux suite inference self-test failed for {paths}: expected {expected}, got {measured}"
            )
    print(f"LINUX-SUITE-EVIDENCE status=PASS inference_cases={len(cases)} suites={len(SUITES)}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Select scoped Linux integration suites.")
    parser.add_argument("--base")
    parser.add_argument("--head")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args()

    if args.self_test:
        self_test()
        return
    if args.list:
        for name, checks in SUITES.items():
            rendered = "all PR checks" if checks == ("*",) else ",".join(checks)
            print(f"{name:20} {rendered}")
        return
    if not args.base or not args.head:
        raise SystemExit("--base and --head are required for automatic scope selection")

    suites = infer_suites(git_changed_paths(args.base, args.head))
    print(",".join(suites) if suites else "none")


if __name__ == "__main__":
    main()
