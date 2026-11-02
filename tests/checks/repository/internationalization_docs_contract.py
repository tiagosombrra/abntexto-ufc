#!/usr/bin/env python3
"""Check public internationalization documentation against the class catalog."""
import ast
from pathlib import Path

root = Path(__file__).resolve().parents[3]
# Read the executable catalog key set instead of freezing a stale document count.
catalog = ast.parse(
    (root / "tests/integration/frontmatter/document-locale-catalog.py").read_text(encoding="utf-8")
)
catalog_sets = [
    node.value for node in catalog.body
    if isinstance(node, ast.Assign)
    and any(isinstance(target, ast.Name) and target.id == "expected"
            for target in node.targets)
]
if len(catalog_sets) != 1:
    raise SystemExit("I18N-DOCS-EVIDENCE status=FAIL catalog_expected_set_missing")
document_keys = len(ast.literal_eval(catalog_sets[0]))
if document_keys < 1:
    raise SystemExit("I18N-DOCS-EVIDENCE status=FAIL catalog_empty")
expected = {
    "docs/USER-GUIDE.md": ("document-language=pt|en|es|fr", f"{document_keys} chaves", "I18N-AUDIT-2026-10-23.md"),
    "docs/COMMAND-REFERENCE.md": ("document-language", f"{document_keys} chaves", r"\appendixlabel", r"\abntextonotelabel"),
    "docs/PROFILE-LOCALE-COVERAGE.md": ("display-only", f"{document_keys} class-owned text keys", "PENDING"),
    "docs/INTERNATIONALIZATION-COVERAGE.md": (f"{document_keys} document keys", "document-language", "PDF"),
    "docs/I18N-COMPLETION-MATRIX.md": ("P0", "7 × 4", "PENDING", "legacy", "PDF"),
    "docs/I18N-AUDIT-2026-10-23.md": ("PT/EN/ES/FR", "34", "28 PDFs", "PENDING"),
}
for filename, markers in expected.items():
    source = (root / filename).read_text(encoding="utf-8")
    for marker in markers:
        if marker.casefold() not in source.casefold():
            raise SystemExit(f"I18N-DOCS-EVIDENCE status=FAIL file={filename} missing={marker}")

# Avoid literal escaped newlines and double-escaped TeX commands in the audit.
audit = (root / "docs/I18N-AUDIT-2026-10-23.md").read_text(encoding="utf-8")
if r"\\n\\n" in audit:
    raise SystemExit("I18N-DOCS-EVIDENCE status=FAIL escaped_audit_paragraphs")
for command in (r"\\legendlabel", r"\\nobreakspace"):
    if command in audit:
        raise SystemExit(f"I18N-DOCS-EVIDENCE status=FAIL doubled_tex_command={command}")

# Markdown code spans preserve slashes verbatim; catching a copied doubled
# TeX command across the four public documents needs no LaTeX run.
for filename in (
    "docs/COMMAND-REFERENCE.md",
    "docs/USER-GUIDE.md",
    "docs/SUMMARY-LANGUAGE-POLICY.md",
    "docs/INTERNATIONALIZATION-COVERAGE.md",
):
    source = (root / filename).read_text(encoding="utf-8")
    if r"\\selectlanguage{english}" in source:
        raise SystemExit(f"I18N-DOCS-EVIDENCE status=FAIL doubled_babel_command={filename}")

# Fail early when the old labels-only summary is accidentally restored.
guide = (root / "docs/USER-GUIDE.md").read_text(encoding="utf-8").casefold()
for stale in ("essa primeira entrega é **experimental e limitada aos rótulos**",
              "não há tradução institucional automática"):
    if stale in guide:
        raise SystemExit(f"I18N-DOCS-EVIDENCE status=FAIL outdated_claim={stale}")

print(f"I18N-DOCS-EVIDENCE status=PASS keys={document_keys} locales=4 "
      "legacy_preserved=true human_review=PENDING tex_pdf=0")
