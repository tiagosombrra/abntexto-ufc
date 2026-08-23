#!/usr/bin/env python3
from __future__ import annotations

import argparse
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def parse_version() -> str:
    text = (ROOT / "Makefile").read_text(encoding="utf-8")
    match = re.search(r"^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", text, re.MULTILINE)
    if not match:
        raise SystemExit("Makefile VERSION not found.")
    return match.group(1)


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate release metadata before publishing a tag.")
    parser.add_argument("--release-tag", required=True)
    args = parser.parse_args()

    version = parse_version()
    expected_tag = f"v{version}"
    if args.release_tag != expected_tag:
        raise SystemExit(f"Release tag mismatch: expected {expected_tag}, got {args.release_tag}.")

    cls = (ROOT / "abntexto-ufc.cls").read_text(encoding="utf-8")
    if f"v{version} UFC academic document class" not in cls:
        raise SystemExit(f"abntexto-ufc.cls does not declare v{version}.")

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    published = re.search(
        r"Versão\s+publicada\s+atual:\s*(?:\*\*)?([0-9]+\.[0-9]+\.[0-9]+)(?:\*\*)?\b",
        readme,
        re.IGNORECASE,
    )
    if not published or published.group(1) != version:
        current = published.group(1) if published else "missing"
        raise SystemExit(f"README published version mismatch: expected {version}, got {current}.")

    ctan = (ROOT / "docs/README-CTAN.md").read_text(encoding="utf-8")
    match = re.search(r"^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$", ctan, re.MULTILINE)
    if not match or match.group(1) != version:
        current = match.group(1) if match else "missing"
        raise SystemExit(f"CTAN README version mismatch: expected {version}, got {current}.")

    print(f"Release metadata validated for {args.release_tag}.")


if __name__ == "__main__":
    main()
