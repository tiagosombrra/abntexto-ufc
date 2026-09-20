#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]

REQUIRED_PATHS = {
    "abntexto-ufc.cls",
    "template/main.tex",
    "tests/run.py",
    "docs/ARCHITECTURE.md",
    "docs/ENGINEERING-LANGUAGE.md",
    "docs/RELEASE-STATE.md",
    ".gitattributes",
    ".editorconfig",
    "docs/README.md",
    "CONTRIBUTING.md",
    "SECURITY.md",
    "CITATION.cff",
    "tests/README.md",
    "standards/README.md",
    "assets/institutional/README.md",
    ".github/pull_request_template.md",
    ".github/dependabot.yml",
    ".github/ISSUE_TEMPLATE/bug.yml",
    ".github/ISSUE_TEMPLATE/documentation.yml",
    ".github/ISSUE_TEMPLATE/config.yml",
    "docs/history/v3/audits/V3.0.2-REPOSITORY-HYGIENE-RECEIPT.md",
    "docs/WINDOWS-FONT-SUPPORT.md",
    "release/v3-release-candidate.json",
    "release/history/v3/README.md",
}

FORBIDDEN_EXACT_PATHS = {
    "ufctex.cls",
    "docs/B2R-NAMING-INVENTORY.md",
    "docs/HANDOFF-V2.2.0.md",
    "docs/NAMING.md",
    "docs/V3.0.2-BRANCH-HYGIENE-MANIFEST.md",
    "docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md",
    "docs/MIGRATING-TO-V3.md",
    "docs/V3.0.3-DISTRIBUTION-CORRECTION.md",
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

APPROVED_HISTORY_PREFIX = "docs/history/v3/"
APPROVED_RELEASE_HISTORY_PREFIX = "release/history/v3/"
HISTORICAL_SNAPSHOT_BANNER = "> **Historical snapshot.**"

RELOCATED_RELEASE_PATHS = (
    "release/v3-api-migration.json",
    "release/v3-r3-b2-proof-semantics.json",
    "release/v3-r3-inventory.json",
    "release/v3-roadmap.json",
    "release/v3.0.1-final-corrections.json",
    "release/v3.0.1-global-regression.json",
)

RELOCATED_HISTORY_PATHS = (
    "docs/HANDOFF-V3.0.0.md",
    "docs/ROADMAP-V3.0.0.md",
    "docs/R2-API-OWNERSHIP.md",
    "docs/R3-B2-EVIDENCE-CONTRIBUTION.md",
    "docs/R3-B2-NONAUTOMATIC-CLASSIFICATION.md",
    "docs/R3-HARDENING-INVENTORY.md",
    "docs/V3-CORE-CORRECTIONS-PHASE-END.md",
    "docs/V3-CORRECTION-PLAN.md",
    "docs/V3-FINAL-CERTIFICATION-PHASE-END.md",
    "docs/V3-FINAL-CERTIFICATION.md",
    "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md",
    "docs/V3-REFERENCE-PDF-VALIDATION.md",
    "docs/V3-REFERENCE-PDF-VISUAL-REVIEW.md",
    "docs/V3-REGRESSION-AUDIT.md",
    "docs/V3-RELEASE-PHASE-END.md",
    "docs/V3-RELEASE-READINESS.md",
    "docs/V3-RELEASE-RECOVERY.md",
    "docs/V3-SCIENTIFIC-ARTICLE-PDF-VALIDATION.md",
    "docs/V3-SCIENTIFIC-ARTICLE-PHASE-END.md",
    "docs/V3-SCIENTIFIC-ARTICLE.md",
    "docs/V3.0.1-R1-TCC-SOURCE-AUDIT.md",
    "docs/V3.0.1-R1.1-EVIDENCE.md",
    "docs/V3.0.1-R1.2-EVIDENCE.md",
    "docs/V3.0.1-R1.2-TCC-COVERAGE-MATRIX.md",
    "docs/V3.0.1-R1.3-EVIDENCE.md",
    "docs/V3.0.1-R2-EVIDENCE.md",
    "docs/V3.0.1-R3-EVIDENCE.md",
    "docs/V3.0.1-R4-EVIDENCE.md",
    "docs/V3-CONTINUATION.md",
    "docs/V3.0.1-FINAL-CORRECTION-PLAN.md",
    "docs/V3.0.1-DOCUMENT-LIFECYCLE.md",
    "docs/V3.0.1-R5-EVIDENCE.md",
    "docs/V3.0.1-R6-EVIDENCE.md",
)

FORBIDDEN_PREFIXES = (
    "abntexto-ufc/",
    ".release/",
    "artifacts/",
    ".ci-downloads/",
    "_site/",
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
    "docs/V3.0.3-DISTRIBUTION-CORRECTION.md",
    "docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md",
    "normativa/",
    "tests/normativa/",
    "tests/fixtures/pretextuais/",
    "standards/history/",
    "ufctex.cls",
)

CONTENT_SCAN_EXEMPT = {
    # The API migration mapping intentionally names retired paths and API
    # identifiers as migration evidence; current release authorities are scanned normally.
    "release/history/v3/v3-api-migration.json",
    # This checker defines the forbidden literals above; scanning its own
    # source would report those policy definitions as active stale references.
    "tests/checks/repository_contract.py",
}

# These active technical/documentation surfaces intentionally name the removed
# class entrypoint only to assert that it must remain absent.
NEGATIVE_FRAGMENT_EXEMPT = {
    "tests/checks/canonical_identity.py": {"ufctex.cls"},
    "tests/checks/repository_contract.py": {"ufctex.cls"},
}


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
    approved_history_files: list[str] = []
    approved_release_history_files: list[str] = []

    for required in sorted(REQUIRED_PATHS - path_set):
        errors.append(f"missing required path: {required}")

    for path in paths:
        lower = path.lower()

        if path in FORBIDDEN_EXACT_PATHS:
            errors.append(f"obsolete active path: {path}")

        if path.startswith("docs/history/"):
            if not path.startswith(APPROVED_HISTORY_PREFIX):
                errors.append(f"unapproved documentation history prefix: {path}")
            else:
                approved_history_files.append(path)
                if path != f"{APPROVED_HISTORY_PREFIX}README.md":
                    if not path.endswith(".md"):
                        errors.append(f"non-Markdown file in approved documentation history: {path}")
                    else:
                        history_text = read_text(path)
                        if history_text is None or not history_text.startswith(HISTORICAL_SNAPSHOT_BANNER):
                            errors.append(f"historical snapshot banner missing: {path}")

        if path.startswith("release/history/"):
            if not path.startswith(APPROVED_RELEASE_HISTORY_PREFIX):
                errors.append(f"unapproved release history prefix: {path}")
            else:
                approved_release_history_files.append(path)
                if path != f"{APPROVED_RELEASE_HISTORY_PREFIX}README.md" and not path.endswith(".json"):
                    errors.append(f"non-JSON file in approved release history: {path}")

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
        # Approved historical snapshots intentionally preserve obsolete paths and
        # phase-time wording as evidence. Their explicit banner prevents them from
        # being confused with current repository authority.
        if path.startswith(APPROVED_HISTORY_PREFIX) or path.startswith(APPROVED_RELEASE_HISTORY_PREFIX):
            continue

        if re.search(r"docs/history/(?!v3/)", text):
            errors.append(f"{path}: reference to unapproved documentation history root")
        if re.search(r"release/history/(?!v3/)", text):
            errors.append(f"{path}: reference to unapproved release history root")

        for relocated_path in RELOCATED_HISTORY_PATHS:
            if relocated_path in text:
                errors.append(f"{path}: stale reference to relocated historical path: {relocated_path}")
        for relocated_path in RELOCATED_RELEASE_PATHS:
            if relocated_path in text:
                errors.append(f"{path}: stale reference to relocated release-state path: {relocated_path}")

        active_user_doc = (
            path == "README.md"
            or path in {"CONTRIBUTING.md", "SECURITY.md"}
            or (path.startswith("docs/") and not path.startswith(APPROVED_HISTORY_PREFIX))
        )
        if active_user_doc:
            migration_pattern = re.compile(
                r"(?:migrat(?:e|ing|ion)|migra(?:r|ção|ndo)).{0,80}"
                r"(?:\bv2\b|\b2\.x\b|série\s+2|serie\s+2|versão\s+2|versao\s+2)"
                r"|(?:\bv2\b|\b2\.x\b|série\s+2|serie\s+2|versão\s+2|versao\s+2).{0,80}"
                r"(?:migrat(?:e|ing|ion)|migra(?:r|ção|ndo))",
                re.IGNORECASE,
            )
            if migration_pattern.search(text):
                errors.append(f"{path}: obsolete v2-to-current migration guidance remains in active documentation")

        allowed_fragments = NEGATIVE_FRAGMENT_EXEMPT.get(path, set())
        for fragment in STALE_CONTENT_FRAGMENTS:
            if fragment in allowed_fragments:
                continue
            if fragment in text:
                errors.append(f"{path}: stale active path reference: {fragment}")

    class_text = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if re.search(r"\\input\{abntexto-ufc/[^}]+\.def\}", class_text):
        errors.append("abntexto-ufc.cls: external project-owned .def module load remains")
    if re.search(r"\\ProvidesFile\{abntexto-ufc/", class_text):
        errors.append("abntexto-ufc.cls: project-module ProvidesFile wrapper remains")
    if "ufctex" in class_text.lower():
        errors.append("abntexto-ufc.cls: deprecated ufctex identity remains")

    if errors:
        print("Repository contract failed:")
        for error in sorted(set(errors)):
            print(f"- {error}")
        return 1

    print(
        "REPOSITORY-EVIDENCE status=PASS "
        f"tracked_files={len(paths)} history_directories=2 "
        f"doc_history_files={len(approved_history_files)} "
        f"release_history_files={len(approved_release_history_files)} legacy_class=0"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
