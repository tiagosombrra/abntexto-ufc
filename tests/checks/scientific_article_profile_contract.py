#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
CORE = ROOT / "abntexto-ufc" / "core.def"
ROADMAP = ROOT / "release" / "v3-roadmap.json"
ARTICLE_RULES = ROOT / "standards" / "coverage-rules-article.json"

CANONICAL = "scientific-article"
ALIASES = (
    "article",
    "scientific_article",
    "artigo",
    "artigo-cientifico",
    "artigo-científico",
)
REQUIRED_METADATA = ("submission-date", "article-author-note")


def fail(message: str) -> None:
    raise SystemExit(f"Scientific article profile contract failed: {message}")


def main() -> None:
    core = CORE.read_text(encoding="utf-8")
    roadmap = json.loads(ROADMAP.read_text(encoding="utf-8"))
    article = json.loads(ARTICLE_RULES.read_text(encoding="utf-8"))

    canonical_pattern = re.compile(
        r"type\s*/\s*" + re.escape(CANONICAL) + r"\s*\.code:n\s*="
    )
    canonical_count = len(canonical_pattern.findall(core))
    if canonical_count != 1:
        fail(f"expected exactly one canonical {CANONICAL!r} type choice; found {canonical_count}")

    alias_hits: list[str] = []
    for alias in ALIASES:
        pattern = re.compile(r"type\s*/\s*" + re.escape(alias) + r"\s*\.code:n\s*=")
        if pattern.search(core):
            alias_hits.append(alias)
    if alias_hits:
        fail("runtime aliases are not allowed: " + ", ".join(alias_hits))

    for key in REQUIRED_METADATA:
        default_count = len(re.findall(r"^[ \t]*" + re.escape(key) + r"\s*=", core, re.MULTILINE))
        setter_count = len(re.findall(re.escape(key) + r"\s*\.code:n\s*=", core))
        if default_count != 1 or setter_count != 1:
            fail(
                f"metadata key {key!r} must have one default and one setter; "
                f"defaults={default_count} setters={setter_count}"
            )

    if roadmap.get("phase") not in {"scientific-article", "final-certification", "release"}:
        fail("scientific-article profile exists outside the article-or-later roadmap phases")

    rules = article.get("rules")
    if not isinstance(rules, list) or len(rules) != 18:
        fail("scientific article authority contract must retain exactly 18 rules")

    print(
        "ARTICLE-PROFILE-CONTRACT-EVIDENCE status=PASS "
        f"canonical_choice={canonical_count} aliases={len(alias_hits)} "
        f"metadata_keys={len(REQUIRED_METADATA)} article_rules={len(rules)}"
    )


if __name__ == "__main__":
    main()
