#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
CLASS = ROOT / "abntexto-ufc.cls"
MODULE_RE = re.compile(r"\\input\{(abntexto-ufc/[^}]+\.def)\}")
LEGACY_CLASS_MESSAGE_RE = re.compile(
    r"\\Class(?:Info|Error|Warning|WarningNoLine)\{ufctex\}"
)


def main() -> None:
    errors: list[str] = []
    class_text = CLASS.read_text(encoding="utf-8")

    if "\\input{ufctex/" in class_text:
        errors.append("abntexto-ufc.cls: canonical class loads the legacy module namespace")

    modules = MODULE_RE.findall(class_text)
    if not modules:
        errors.append("abntexto-ufc.cls: no canonical modules found")

    if len(modules) != len(set(modules)):
        errors.append("abntexto-ufc.cls: duplicate canonical module input")

    for module in modules:
        path = ROOT / module
        if not path.is_file():
            errors.append(f"{module}: loaded canonical module does not exist")
            continue

        text = path.read_text(encoding="utf-8")
        expected = f"\\ProvidesFile{{{module}}}"
        if expected not in text:
            errors.append(f"{module}: expected {expected}")
        if "\\ProvidesFile{ufctex/" in text:
            errors.append(f"{module}: legacy ProvidesFile identity")
        if LEGACY_CLASS_MESSAGE_RE.search(text):
            errors.append(f"{module}: legacy ufctex class-message identity")

    normas = (ROOT / "docs/NORMAS.md").read_text(encoding="utf-8")
    if "`ufctex/" in normas:
        errors.append("docs/NORMAS.md: legacy module path remains in CTAN documentation")

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(f"Canonical identity check failed with {len(errors)} issue(s).")

    print(f"Canonical identity check passed: {len(modules)} modules aligned.")


if __name__ == "__main__":
    main()
