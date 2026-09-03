#!/usr/bin/env python3
from __future__ import annotations

from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]


def replace_exact(path: Path, old: str, new: str) -> None:
    # Fail closed if the expected source shape has changed.
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"expected exactly one repair target in {path}, found {count}")
    path.write_text(text.replace(old, new), encoding="utf-8")


approval = ROOT / "tests/integration/frontmatter-approval-evidence.sh"
replace_exact(
    approval,
    '''  sed "s/tipo = tese,/tipo = $profile,/" "$fixture" > "$generated"\n\n''',
    '''  case "$profile" in\n    tccgraduacao) document_type="undergraduate-capstone" ;;\n    tccespecializacao) document_type="specialization-capstone" ;;\n    dissertacao) document_type="masters-thesis" ;;\n    tese) document_type="doctoral-thesis" ;;\n    projeto) document_type="research-project" ;;\n    projetoanonimizado) document_type="anonymized-research-project" ;;\n    *)\n      echo "Unknown approval profile label: $profile"\n      exit 1\n      ;;\n  esac\n\n  sed "s/type = doctoral-thesis,/type = $document_type,/" "$fixture" > "$generated"\n\n  type_lines=$(grep -Ec '^[[:space:]]*type[[:space:]]*=' "$generated" || true)\n  if [ "$type_lines" -ne 1 ] || ! grep -Fq "type = $document_type," "$generated"; then\n    echo "Approval profile generation failed for $profile -> $document_type."\n    cat "$generated"\n    exit 1\n  fi\n\n''',
)

summary = ROOT / "tests/checks/normative_frontmatter_summary.py"
replace_exact(
    summary,
    '''    before_macro = re.split(r"\\\\(?:palavraschave|keywords)\\s*\\{", text, maxsplit=1)[0].strip()\n''',
    '''    before_macro = re.split(\n        r"\\\\(?:ufcSummaryKeywords|keywords)\\s*\\{", text, maxsplit=1\n    )[0].strip()\n''',
)

print("R3-B1 observer repair applied: approval profile generation + summary keyword boundary.")
