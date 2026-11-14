#!/usr/bin/env python3
"""Fail-closed local Markdown link and fragment checks for nonhistorical docs."""
from __future__ import annotations

import re
import subprocess
import tempfile
from collections import Counter
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
LINK = re.compile(r"!?\[[^\]\n]*\]\(\s*(?:<([^>\n]+)>|([^\s)]+))")
REFERENCE = re.compile(r"(?m)^[ \t]{0,3}\[[^\]\n]+\]:[ \t]*(?:<([^>\n]+)>|([^\s]+))")
HEADING = re.compile(r"^[ \t]{0,3}#{1,6}[ \t]+(.+?)[ \t]*#*[ \t]*$")
FENCE = re.compile(r"^[ \t]{0,3}([\x60]{3,}|~{3,})")
SCHEME = re.compile(r"^[A-Za-z][A-Za-z0-9+.-]*:")
EXCLUDED_PARENTS = {("docs", "history"), ("release", "history")}


def visible_text(source: str) -> str:
    # Ignore sample links within fenced code: they are code, not navigation.
    result = []
    fence = None
    for line in source.splitlines():
        match = FENCE.match(line)
        if match:
            marker = match.group(1)
            if fence is None:
                fence = marker[0]
            elif marker[0] == fence:
                fence = None
            result.append("")
        else:
            result.append("" if fence else line)
    return "\n".join(result)


def anchors(source: str) -> set[str]:
    names = set()
    duplicates = Counter()
    for line in visible_text(source).splitlines():
        match = HEADING.match(line)
        if match is None:
            continue
        name = re.sub(r"<[^>]+>", "", match.group(1)).replace(chr(96), "")
        name = re.sub(r"\[([^\]]+)\]\([^)]+\)", r"\1", name)
        name = re.sub(r"[^\w\s-]", "", name.lower(), flags=re.UNICODE)
        name = re.sub(r"\s+", "-", name.strip())
        if not name:
            continue
        index = duplicates[name]
        duplicates[name] += 1
        names.add(name if index == 0 else f"{name}-{index}")
    return names


def scan(root: Path, documents: list[Path]) -> tuple[list[str], int, int, int]:
    errors: list[str] = []
    local = fragments = external = 0
    base = root.resolve()
    seen_anchors: dict[Path, set[str]] = {}
    for document in documents:
        source_file = root / document
        try:
            source = visible_text(source_file.read_text(encoding="utf-8"))
        except (OSError, UnicodeError) as exc:
            errors.append(f"{document}: unreadable Markdown: {exc}")
            continue
        matches = [
            (match.start(), match.group(1) or match.group(2))
            for regex in (LINK, REFERENCE)
            for match in regex.finditer(source)
        ]
        for position, value in matches:
            uri = value.strip()
            if uri.startswith("//") or SCHEME.match(uri):
                external += 1
                continue
            if uri.startswith("/"):
                errors.append(f"{document}: absolute root link is not a portable relative path: {uri}")
                continue
            parsed = urlsplit(uri)
            target = unquote(parsed.path)
            fragment = unquote(parsed.fragment)
            resolved = (source_file.parent / target).resolve()
            line = source.count("\n", 0, position) + 1
            if not resolved.is_relative_to(base):
                errors.append(f"{document}:{line}: link escapes repository: {uri}")
                continue
            if target and not resolved.is_file():
                errors.append(f"{document}:{line}: missing relative target: {uri}")
                continue
            local += 1
            if fragment and resolved.suffix.lower() == ".md":
                fragments += 1
                if resolved not in seen_anchors:
                    seen_anchors[resolved] = anchors(resolved.read_text(encoding="utf-8"))
                if fragment.lower() not in seen_anchors[resolved]:
                    errors.append(f"{document}:{line}: missing Markdown fragment: {uri}")
    return errors, local, fragments, external


def selftest() -> None:
    # Verify real positives and missing path/anchor and traversal negatives.
    with tempfile.TemporaryDirectory(prefix="documentation-links-") as directory:
        root = Path(directory)
        (root / "docs").mkdir()
        (root / "guide.md").write_text("# Overview\n", encoding="utf-8")
        path = root / "docs" / "index.md"
        path.write_text("[Guide](../guide.md#overview)\n", encoding="utf-8")
        ok, local, fragments, _ = scan(root, [Path("docs/index.md")])
        if ok or local != 1 or fragments != 1:
            raise AssertionError("Valid linked Markdown is rejected")
        for invalid in (
            "[Gone](../missing.md)\n",
            "[Section](../guide.md#missing)\n",
            "[Outside](../../../outside.md)\n",
        ):
            path.write_text(invalid, encoding="utf-8")
            errors, _, _, _ = scan(root, [Path("docs/index.md")])
            if not errors:
                raise AssertionError(f"Broken relative Markdown link was accepted: {invalid}")
        path.write_text(
            chr(96) * 3 + "md\n[Example](missing.md)\n" + chr(96) * 3 + "\n",
            encoding="utf-8",
        )
        errors, _, _, _ = scan(root, [Path("docs/index.md")])
        if errors:
            raise AssertionError("Link within a fenced code sample was rejected")


def tracked_markdown() -> list[Path]:
    raw = subprocess.check_output(["git", "ls-files", "-z"], cwd=ROOT)
    paths = [
        Path(item.decode("utf-8"))
        for item in raw.split(b"\0")
        if item and item.decode("utf-8").lower().endswith(".md")
    ]
    return sorted(
        path for path in paths
        if tuple(path.parts[:2]) not in EXCLUDED_PARENTS
    )


def main() -> None:
    selftest()
    documents = tracked_markdown()
    if not documents:
        raise SystemExit("DOCS-LINK-EVIDENCE status=FAIL no_tracked_markdown")
    errors, local, fragments, external = scan(ROOT, documents)
    if errors:
        for error in errors:
            print("DOCS-LINK-FINDING " + error)
        raise SystemExit(
            f"DOCS-LINK-EVIDENCE status=FAIL files={len(documents)} "
            f"violations={len(errors)}"
        )
    print(
        f"DOCS-LINK-EVIDENCE status=PASS files={len(documents)} "
        f"relative={local} fragments={fragments} external_unchecked={external} "
        "negative_cases=3 historical_excluded=true tex_pdf=0 network=0"
    )


if __name__ == "__main__":
    main()
