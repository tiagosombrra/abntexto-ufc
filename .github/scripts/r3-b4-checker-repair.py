#!/usr/bin/env python3
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
TARGET = ROOT / "tests/checks/engineering_language.py"

text = TARGET.read_text(encoding="utf-8")

old = '''MACHINE_FILES = (
    "standards/catalog.json",
    "standards/coverage-rules-frontmatter.json",
    "standards/coverage-rules-project.json",
    "standards/frontmatter-approval-scenario.json",
    "standards/frontmatter-cover-scenario.json",
    "tests/checks/normative_frontmatter_title_page.py",
    "tests/integration/frontmatter-approval-evidence.sh",
)
'''
new = '''MACHINE_JSON_FILES = (
    "standards/catalog.json",
    "standards/coverage-rules-frontmatter.json",
    "standards/coverage-rules-project.json",
    "standards/frontmatter-approval-scenario.json",
    "standards/frontmatter-cover-scenario.json",
)
MACHINE_SOURCE_FILES = (
    "tests/checks/normative_frontmatter_title_page.py",
    "tests/integration/frontmatter-approval-evidence.sh",
)
RETIRED_PROFILE_VALUES = {"tccgraduacao", "tccespecializacao", "dissertacao", "tese", "projeto", "projetoanonimizado"}
'''
if old not in text:
    raise SystemExit("machine-file block not found")
text = text.replace(old, new)

old = '''        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if is_comment_or_diagnostic(line) and PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic(line)):
                errors.append(f"{rel}:{number}: Portuguese project-owned engineering text: {line.strip()}")
    for rel in MACHINE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if RETIRED_PROFILE_IDS.search(line):
                errors.append(f"{rel}:{number}: retired Portuguese technical profile identifier: {line.strip()}")
'''
new = '''        if rel == "tests/checks/engineering_language.py":
            continue
        text = path.read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if is_comment_or_diagnostic(line) and PORTUGUESE_TECHNICAL_TERMS.search(normalized_diagnostic(line)):
                errors.append(f"{rel}:{number}: Portuguese project-owned engineering text: {line.strip()}")

    def visit_machine_values(value, location: str) -> None:
        if isinstance(value, dict):
            for key, item in value.items():
                visit_machine_values(item, f"{location}.{key}")
        elif isinstance(value, list):
            for index, item in enumerate(value):
                visit_machine_values(item, f"{location}[{index}]")
        elif isinstance(value, str) and value in RETIRED_PROFILE_VALUES:
            errors.append(f"{location}: retired Portuguese technical profile identifier: {value}")

    for rel in MACHINE_JSON_FILES:
        payload = json.loads((ROOT / rel).read_text(encoding="utf-8"))
        visit_machine_values(payload, rel)
    for rel in MACHINE_SOURCE_FILES:
        text = (ROOT / rel).read_text(encoding="utf-8")
        for number, line in enumerate(text.splitlines(), 1):
            if RETIRED_PROFILE_IDS.search(line):
                errors.append(f"{rel}:{number}: retired Portuguese technical profile identifier: {line.strip()}")
'''
if old not in text:
    raise SystemExit("audit block not found")
text = text.replace(old, new)

TARGET.write_text(text, encoding="utf-8")
print("R3-B4 checker false-positive boundaries repaired.")
