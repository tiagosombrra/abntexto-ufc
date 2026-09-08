#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RELEASE_CANDIDATE_MARKER = ROOT / "release" / "v3-release-candidate.json"
ACTIVE_RELEASE_CANDIDATE_STATES = {"transport-probe", "candidate-active", "candidate-frozen"}

SUITES: dict[str, tuple[str, ...]] = {
    "complete": ("*",),
    "smoke": ("repository", "validator-source", "reference", "pdf-validator"),
    "reference-document": ("reference", "reference-corpus", "pdf-validator"),
    "reference-pdf": (
        "reference", "reference-corpus", "pdf-validator", "layout", "font-config",
        "pdf-validation-core", "pdf-geometry", "frontmatter", "duplex-frontmatter",
        "object-geometry", "table-ibge", "documentary-source", "bibliography",
        "reference-spacing", "backmatter", "duplex-backmatter",
    ),
    "frontmatter": ("frontmatter", "duplex-frontmatter"),
    "layout": (
        "layout", "font-config", "pdf-validation-core", "pdf-geometry", "math",
        "normative-complement",
    ),
    "objects": (
        "object-geometry", "code-typography", "table-ibge", "objects", "minted",
        "algorithm-numbering", "documentary-source",
    ),
    "bibliography": ("bibliography", "reference-spacing", "normative-complement"),
    "backmatter": ("backmatter", "duplex-backmatter"),
    "research-project": ("research-project",),
    "profiles": ("profiles", "build-path", "multivolume", "catalog-card"),
    "article": (
        "validator-source", "scientific-article-profile", "scientific-article-front-block",
        "scientific-article-foreign-elements", "scientific-article-body",
        "scientific-article-recommendations",
    ),
}

SUITE_ORDER = tuple(SUITES)

DOC_ONLY_EXACT = {
    "README.md", "AGENTS.md", "LICENSE", ".gitignore", "release/v3-roadmap.json",
}
DOC_ONLY_PREFIXES = ("docs/",)

ORCHESTRATION_EXACT = {
    ".github/workflows/linux-integration.yml",
    ".github/workflows/linux-release-check.yml",
    "tests/run.py",
    "tests/static.py",
    "tests/integration_suites.py",
    "tests/checks/linux_integration_suites.py",
    "tests/checks/release_candidate_contract.py",
}

FORCE_COMPLETE_EXACT = {
    "Makefile",
    "abntexto-ufc.cls",
    "abntexto-ufc/core.def",
    "abntexto-ufc/fonts.def",
    "abntexto-ufc/modules.def",
    "release/final-certification-candidate.json",
    "release/v3-release-candidate.json",
}
FORCE_COMPLETE_PREFIXES = (
    "abntexto-ufc/integrations/",
    "standards/",
)

PATH_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    ("article", ("abntexto-ufc/article", "tests/integration/scientific-article", "tests/documents/scientific-article", "tests/checks/scientific_article")),
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

    orchestration = [path for path in technical if path in ORCHESTRATION_EXACT]
    domain_technical = [path for path in technical if path not in ORCHESTRATION_EXACT]
    if orchestration and not domain_technical:
        return ("smoke",)
    if orchestration:
        technical = domain_technical

    if any(path in FORCE_COMPLETE_EXACT or path.startswith(FORCE_COMPLETE_PREFIXES) for path in technical):
        return ("complete",)

    selected: set[str] = set()
    for path in technical:
        matched = matching_suites(path)
        if not matched:
            return ("complete",)
        selected.update(matched)

    return tuple(name for name in SUITE_ORDER if name in selected)


def release_candidate_requires_complete(marker_path: Path = RELEASE_CANDIDATE_MARKER) -> bool:
    if not marker_path.is_file():
        return False
    try:
        marker = json.loads(marker_path.read_text(encoding="utf-8"))
    except (OSError, UnicodeError, json.JSONDecodeError) as exc:
        raise SystemExit(f"invalid Release candidate marker: {exc}") from exc

    state = marker.get("state")
    if state not in ACTIVE_RELEASE_CANDIDATE_STATES:
        return False
    if marker.get("phase") != "Release":
        raise SystemExit("active Release candidate marker must declare phase=Release")
    if marker.get("temporary") is not False:
        raise SystemExit("active Release candidate marker must be non-temporary")
    if marker.get("candidate_sha_is_self_referential") is not False:
        raise SystemExit("Release candidate marker must not embed a self-referential candidate SHA")
    return True


def select_suites(paths: list[str], *, release_candidate_active: bool = False) -> tuple[str, ...]:
    if release_candidate_active:
        return ("complete",)
    return infer_suites(paths)


def git_changed_paths(base: str, head: str) -> list[str]:
    completed = subprocess.run(
        ["git", "diff", "--name-only", base, head],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
        encoding="utf-8", errors="replace", check=False,
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
        ("tests/integration/scientific-article-profile.sh",): ("article",),
        ("tests/integration/scientific-article-recommendations.sh",): ("article",),
        ("tests/run.py", "tests/integration/scientific-article-recommendations.sh"): ("article",),
        ("tests/integration_suites.py", "abntexto-ufc/objects.def"): ("objects",),
        ("tests/run.py", "unknown/technical.file"): ("complete",),
        ("abntexto-ufc/objects.def", "abntexto-ufc/bibliography.def"): ("objects", "bibliography"),
        ("abntexto-ufc/core.def",): ("complete",),
        ("release/final-certification-candidate.json",): ("complete",),
        ("tests/integration_suites.py", "release/final-certification-candidate.json"): ("complete",),
        ("release/v3-release-candidate.json",): ("complete",),
        ("tests/integration_suites.py", "release/v3-release-candidate.json"): ("complete",),
        ("unknown/technical.file",): ("complete",),
    }
    for paths, expected in cases.items():
        measured = infer_suites(list(paths))
        if measured != expected:
            raise SystemExit(
                f"Linux suite inference self-test failed for {paths}: expected {expected}, got {measured}"
            )

    if select_suites(["tests/integration_suites.py"], release_candidate_active=True) != ("complete",):
        raise SystemExit("active Release candidate must override an orchestration-only diff to complete")
    if select_suites(["docs/ROADMAP-V3.0.0.md"], release_candidate_active=True) != ("complete",):
        raise SystemExit("active Release candidate must override a documentation-only diff to complete")

    print(
        "LINUX-SUITE-EVIDENCE status=PASS "
        f"inference_cases={len(cases)} suites={len(SUITES)} "
        "release_candidate_persistent_override=true"
    )


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

    changed_paths = git_changed_paths(args.base, args.head)
    suites = select_suites(
        changed_paths,
        release_candidate_active=release_candidate_requires_complete(),
    )
    print(",".join(suites) if suites else "none")


if __name__ == "__main__":
    main()
