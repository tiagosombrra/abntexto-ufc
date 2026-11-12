#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import PurePosixPath

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
    "profiles": ("profiles", "tagged-pdf-baseline", "tagged-pdf-graphics", "tagged-pdf-table", "tagged-pdf-mathml", "build-path", "multivolume", "catalog-card"),
    "distribution": ("distribution-bundles",),
    "web-lite": ("validator-source", "web-lite-positive", "profiles", "pdf-geometry"),
    "article": (
        "validator-source", "scientific-article-profile", "scientific-article-front-block",
        "scientific-article-foreign-elements", "scientific-article-body",
        "scientific-article-recommendations",
    ),
}

SUITE_ORDER = tuple(SUITES)

DOC_ONLY_EXACT = {
    "README.md",
    "AGENTS.md",
    "LICENSE",
    ".gitignore",
}
DOC_ONLY_PREFIXES = ("docs/", "release/history/v3/")

ORCHESTRATION_EXACT = {
    ".github/workflows/linux-release-check.yml",
    ".github/workflows/i18n-pretextual-api-matrix.yml",
    ".github/workflows/i18n-listing-font-matrix.yml",
    ".github/workflows/i18n-optional-modules-matrix.yml",
    ".github/workflows/integrated-manuscript-locale-matrix.yml",

    "tests/run.py",
    "tests/static.py",
    "tests/integration_suites.py",
    "tests/checks/repository/linux_integration_suites.py",
    "tests/checks/repository/linux_integration_suites.py",
    "tools/ci/select-integration-scope.py",
    "tools/ci/validate-pkgcheck-download.py",
    "tools/ci/validate-release-assets.py",
    "tools/ci/validate-release-reference.py",
    "tools/ci/certify-ctan-package.sh",
    "tools/ci/render-release-summary.sh",
}

FORCE_COMPLETE_EXACT = {
    # Public API evidence must not bypass full Linux regression on PRs.
    "tests/integration/frontmatter/i18n-api-inventory.py",
    "tests/integration/frontmatter/i18n-six-api-output-evidence.py",
    "tests/integration/frontmatter/institution-display-fallback-evidence.py",
    "tests/integration/frontmatter/i18n-list-environment-evidence.py",
    "tests/integration/frontmatter/i18n-optional-environment-evidence.py",
    "tests/integration/frontmatter/i18n-pretextual-command-evidence.py",
    "tests/integration/frontmatter/i18n-b2-remaining-summary-evidence.py",
    "tests/integration/frontmatter/i18n-b2-family-evidence.py",
    "tests/integration/frontmatter/i18n-b1-family-evidence.py",
    "tests/integration/frontmatter/i18n-b1-auxiliary-pdf-evidence.py",
    "tests/integration/objects/i18n-b1-optional-config-evidence.py",
    "tests/integration/frontmatter/i18n-per-identifier-proof-status.py",
    ".github/workflows/linux-integration.yml",
    "Makefile",
    "abntexto-ufc.cls",
    "release/v3-release-candidate.json",
}
FORCE_COMPLETE_PREFIXES = (
    "standards/",
)

PATH_RULES: tuple[tuple[str, tuple[str, ...]], ...] = (
    # Content-only assets are validated by a separate deterministic Python
    # gate; do not recompile 42 LaTeX integrations for each prose or SVG edit.
    # Any concurrent class/runtime or release change still forces full CI.
    ("smoke", ("examples/canonical-mesh-study/", "tools/examples/",
               "tests/checks/mesh_study.py",
               ".github/workflows/mesh-canonical-fast.yml")),
    ("article", ("tests/integration/scientific-article", "tests/documents/scientific-article", "tests/checks/scientific_article")),
    ("frontmatter", ("template/frontmatter/", "tests/integration/frontmatter", "tests/integration/duplex-frontmatter", "tests/integration/i18n-pretextual-api-evidence.py")),
    ("layout", ("tests/integration/layout", "tests/integration/pdf-geometry", "tests/integration/pdf-validation-core", "tests/integration/math", "tests/integration/normative-complement")),
    ("objects", ("tests/integration/object", "tests/integration/table-ibge", "tests/integration/minted", "tests/integration/algorithm-numbering", "tests/integration/documentary-source", "tests/integration/i18n-listing-font-evidence.py")),
    ("bibliography", ("template/backmatter/references.bib", "tests/integration/bibliography", "tests/integration/reference-spacing")),
    ("backmatter", ("tests/integration/backmatter", "tests/integration/duplex-backmatter")),
    ("research-project", ("tests/integration/research-project",)),
    ("profiles", ("tests/integration/profile-matrix", "tests/integration/tagged-pdf-baseline", "tests/documents/tagged-pdf-baseline", "tests/integration/tagged-pdf-graphics", "tests/documents/tagged-pdf-graphics", "tests/integration/tagged-pdf-table", "tests/documents/tagged-pdf-table", "tests/integration/tagged-pdf-mathml", "tests/documents/tagged-pdf-mathml", "tests/integration/build-path", "tests/integration/multivolume", "tests/integration/catalog-card", "tests/smoke/base-profile.tex")),
    ("reference-document", ("template/main.tex", "template/chapters/", "tests/integration/reference-document", "tests/integration/reference-corpus", "tests/integration/pdf-validator")),
    ("distribution", ("tools/build-public-bundles.py", "tools/build-distribution-bundles.py", "tests/integration/distribution-bundles.sh")),
    ("web-lite", ("validator/", "tests/checks/validator/validator_source.py", "tests/integration/web-lite-e2e.py", "tools/ci/run-web-lite-e2e.sh", "tools/ci/build-pages-site.sh")),
)


def is_docs_only(path: str) -> bool:
    return path in DOC_ONLY_EXACT or path.startswith(DOC_ONLY_PREFIXES)


def normalized_movable_test_path(path: str) -> str:
    # CI orchestration uses its canonical nested path, not a legacy flat alias.
    if path in ORCHESTRATION_EXACT:
        return path
    for prefix in ("tests/checks/", "tests/integration/", "tests/documents/"):
        if path.startswith(prefix):
            return prefix + PurePosixPath(path).name
    return path


def matching_suites(path: str) -> set[str]:
    # Match both the actual tracked path and the historical normalized alias.
    # This avoids fake/flat paths in the registry while retaining legacy tests.
    normalized = normalized_movable_test_path(path)
    matched: set[str] = set()
    for suite, patterns in PATH_RULES:
        if any(path == pattern or path.startswith(pattern)
               or normalized == pattern or normalized.startswith(pattern)
               for pattern in patterns):
            matched.add(suite)
    return matched


def infer_suites(paths: list[str]) -> tuple[str, ...]:
    technical = [path for path in paths if path and not is_docs_only(path)]
    if not technical:
        return ()

    # Preserve repository-native paths for static reachability validation.
    # Only the matcher below may derive a legacy flattened comparison key.
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
        ("docs/ARCHITECTURE.md",): (),
        ("examples/canonical-mesh-study/study.json",): ("smoke",),
        ("tools/examples/generate_mesh_study.py",): ("smoke",),
        ("tests/checks/examples/mesh_study.py",): ("smoke",),
        (".github/workflows/mesh-canonical-fast.yml",): ("smoke",),
        ("examples/canonical-mesh-study/study.json", "abntexto-ufc.cls"): ("complete",),
        ("examples/canonical-mesh-study/study.json", "tests/integration/frontmatter/frontmatter.sh"):
            ("smoke", "frontmatter"),
        ("release/history/v3/v3.0.1-final-corrections.json",): (),
        ("abntexto-ufc.cls",): ("complete",),
        ("tests/integration/frontmatter/i18n-api-inventory.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-six-api-output-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/institution-display-fallback-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-list-environment-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-optional-environment-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-pretextual-command-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-b2-remaining-summary-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-b2-family-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-b1-family-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-b1-auxiliary-pdf-evidence.py",): ("complete",),
        ("tests/integration/frontmatter/i18n-per-identifier-proof-status.py",): ("complete",),
        ("tests/integration/frontmatter/institution-display-fallback-evidence.py",
         ".github/workflows/integrated-manuscript-locale-matrix.yml"): ("complete",),
        ("tests/integration/frontmatter/i18n-six-api-output-evidence.py",
         ".github/workflows/linux-release-check.yml"): ("complete",),
        ("tests/run.py",): ("smoke",),
        (".github/workflows/linux-integration.yml",): ("complete",),
        (".github/workflows/linux-release-check.yml",): ("smoke",),
        ("tools/ci/select-integration-scope.py",): ("smoke",),
        ("tools/ci/validate-release-reference.py",): ("smoke",),
        ("tools/build-public-bundles.py",): ("distribution",),
        ("tools/build-distribution-bundles.py",): ("distribution",),
        ("tests/integration/distribution-bundles.sh",): ("distribution",),
        ("tests/run.py", "tools/build-public-bundles.py"): ("distribution",),
        ("validator/app.js",): ("web-lite",),
        ("validator/normative-catalog.js",): ("web-lite",),
        ("tests/checks/validator/validator_source.py",): ("web-lite",),
        ("tests/integration/web-lite-e2e.py",): ("web-lite",),
        ("tools/ci/run-web-lite-e2e.sh",): ("web-lite",),
        ("tools/ci/build-pages-site.sh",): ("web-lite",),
        ("tests/run.py", "validator/app.js"): ("web-lite",),
        ("tests/integration/scientific-article-profile.sh",): ("article",),
        ("tests/integration/profiles/article/scientific-article-profile.sh",): ("article",),
        ("tests/checks/validator/validator_source.py",): ("web-lite",),
        ("tests/documents/profiles/article/scientific-article-body.tex",): ("article",),
        ("tests/integration/scientific-article-recommendations.sh",): ("article",),
        ("tests/run.py", "tests/integration/scientific-article-recommendations.sh"): ("article",),
        ("tests/integration/profiles/tagged-pdf-baseline.sh",): ("profiles",),
        ("tests/documents/tagged-pdf-baseline.tex",): ("profiles",),
        ("tests/integration/profiles/tagged-pdf-graphics.sh",): ("profiles",),
        ("tests/documents/tagged-pdf-graphics.tex",): ("profiles",),
        ("tests/integration/profiles/tagged-pdf-table.sh",): ("profiles",),
        ("tests/documents/tagged-pdf-table.tex",): ("profiles",),
        ("tests/integration/profiles/tagged-pdf-mathml.sh",): ("profiles",),
        ("tests/documents/tagged-pdf-mathml.tex",): ("profiles",),
        ("tests/run.py", "unknown/technical.file"): ("complete",),
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
    print("LINUX-SUITE-EVIDENCE status=PASS " f"inference_cases={len(cases)} suites={len(SUITES)}")


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
