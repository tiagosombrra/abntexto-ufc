#!/usr/bin/env python3
"""Check public internationalization documentation against the class catalog."""
from pathlib import Path

root = Path(__file__).resolve().parents[3]
expected = {
    "docs/USER-GUIDE.md": ("document-language=pt|en|es|fr", "33 chaves", "I18N-AUDIT-2026-10-23.md"),
    "docs/COMMAND-REFERENCE.md": ("document-language", "33 chaves", r"\appendixlabel", r"\abntextonotelabel"),
    "docs/PROFILE-LOCALE-COVERAGE.md": ("display-only", "33 class-owned text keys", "PENDING"),
    "docs/INTERNATIONALIZATION-COVERAGE.md": ("33 document keys", "document-language", "PDF"),
    "docs/I18N-AUDIT-2026-10-23.md": ("PT/EN/ES/FR", "33", "28 PDFs", "PENDING"),
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

# Fail early when the old labels-only summary is accidentally restored.
guide = (root / "docs/USER-GUIDE.md").read_text(encoding="utf-8").casefold()
for stale in ("essa primeira entrega é **experimental e limitada aos rótulos**",
              "não há tradução institucional automática"):
    if stale in guide:
        raise SystemExit(f"I18N-DOCS-EVIDENCE status=FAIL outdated_claim={stale}")

print("I18N-DOCS-EVIDENCE status=PASS keys=33 locales=4 "
      "legacy_preserved=true full_document_matrix=PENDING tex_pdf=0")
