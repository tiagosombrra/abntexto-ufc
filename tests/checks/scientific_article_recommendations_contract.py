#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RULES = ROOT / "standards" / "coverage-rules-article.json"
ARTICLE_MODULE = ROOT / "abntexto-ufc" / "articles.def"
RECOMMENDED_FIXTURE = ROOT / "tests" / "documents" / "scientific-article-recommendations-recommended.tex"
OUTSIDE_FIXTURE = ROOT / "tests" / "documents" / "scientific-article-recommendations-outside.tex"

RECOMMENDED_RULES = {
    "article.authorship.alignment.recommended",
    "article.summary.word-count.recommended",
    "article.summary.keywords.minimum.recommended",
    "article.summary.single-paragraph.recommended",
}
JOURNAL_RULE = "article.journal-guidelines.precedence"


def fail(message: str) -> None:
    raise SystemExit(f"Scientific article recommendation contract failed: {message}")


def rule_map() -> dict[str, dict]:
    payload = json.loads(RULES.read_text(encoding="utf-8"))
    rules = payload.get("rules")
    if not isinstance(rules, list):
        fail("article rule registry is not a list")
    return {str(rule.get("id")): rule for rule in rules if isinstance(rule, dict)}


def summary_source(path: Path) -> tuple[str, str]:
    source = path.read_text(encoding="utf-8")
    start_token = "\\ufcPrintArticleFrontMatter{%"
    keyword_token = "\\ufcSummaryKeywords{"
    start = source.find(start_token)
    if start < 0:
        fail(f"{path.name}: article front-matter call is missing")
    start += len(start_token)
    keyword_start = source.find(keyword_token, start)
    if keyword_start < 0:
        fail(f"{path.name}: controlled keyword marker is missing")
    summary = source[start:keyword_start].strip()
    keyword_value_start = keyword_start + len(keyword_token)
    keyword_value_end = source.find("}", keyword_value_start)
    if keyword_value_end < 0:
        fail(f"{path.name}: keyword list is not closed")
    keywords = source[keyword_value_start:keyword_value_end].strip()
    return summary, keywords


def word_count(text: str) -> int:
    cleaned = re.sub(r"\\[A-Za-z@]+(?:\[[^]]*\])?", " ", text)
    cleaned = re.sub(r"[{}%]", " ", cleaned)
    return len(re.findall(r"\b[\wÀ-ÿ-]+\b", cleaned, flags=re.UNICODE))


def paragraph_count(text: str) -> int:
    return len([part for part in re.split(r"\n\s*\n|\\par\b", text) if part.strip()])


def keyword_count(text: str) -> int:
    values = [item.strip().rstrip(".") for item in text.split(";")]
    return len([item for item in values if item])


def main() -> None:
    rules = rule_map()

    required_ids = RECOMMENDED_RULES | {JOURNAL_RULE}
    missing = sorted(required_ids - set(rules))
    if missing:
        fail("required Step 5 rules are missing: " + ", ".join(missing))

    for rule_id in sorted(RECOMMENDED_RULES):
        rule = rules[rule_id]
        if rule.get("normativity") != "recommended":
            fail(f"{rule_id}: normativity must remain recommended")
        validation = rule.get("validation") or {}
        if validation.get("mode") != "manual":
            fail(f"{rule_id}: recommendation proof state must remain manual")
        if validation.get("checks") != ["article.source-review"]:
            fail(f"{rule_id}: recommendation checks changed unexpectedly")

    journal = rules[JOURNAL_RULE]
    if journal.get("normativity") != "required-when-applicable":
        fail("journal precedence must remain required-when-applicable")
    journal_validation = journal.get("validation") or {}
    if journal_validation.get("mode") != "conditional-manual":
        fail("journal precedence must remain conditional-manual")
    if journal_validation.get("checks") != ["article.source-review"]:
        fail("journal precedence checks changed unexpectedly")
    applicability = journal.get("applicability") or {}
    if applicability.get("context") != "target-journal-submission":
        fail("journal precedence applicability must remain target-journal-submission")

    module = ARTICLE_MODULE.read_text(encoding="utf-8")
    author_match = re.search(
        r"\\cs_new_protected:Npn \\ufc_article_author:(.*?)\\cs_new_protected:Npn",
        module,
        flags=re.DOTALL,
    )
    if not author_match or "\\raggedleft" not in author_match.group(1):
        fail("generic article authorship default no longer uses right alignment")

    recommended_summary, recommended_keywords = summary_source(RECOMMENDED_FIXTURE)
    outside_summary, outside_keywords = summary_source(OUTSIDE_FIXTURE)

    recommended_words = word_count(recommended_summary)
    outside_words = word_count(outside_summary)
    recommended_paragraphs = paragraph_count(recommended_summary)
    outside_paragraphs = paragraph_count(outside_summary)
    recommended_keyword_count = keyword_count(recommended_keywords)
    outside_keyword_count = keyword_count(outside_keywords)

    if not 150 <= recommended_words <= 250:
        fail(f"recommended fixture must remain within 150-250 words; measured={recommended_words}")
    if recommended_paragraphs != 1:
        fail(f"recommended fixture must use one paragraph; measured={recommended_paragraphs}")
    if recommended_keyword_count < 3:
        fail(f"recommended fixture must contain at least three keywords; measured={recommended_keyword_count}")

    if outside_words >= 150:
        fail(f"outside fixture must remain below the recommended word interval; measured={outside_words}")
    if outside_paragraphs < 2:
        fail(f"outside fixture must violate the one-paragraph recommendation; measured={outside_paragraphs}")
    if outside_keyword_count >= 3:
        fail(f"outside fixture must remain below the recommended keyword count; measured={outside_keyword_count}")

    print(
        "ARTICLE-RECOMMENDATION-CONTRACT-EVIDENCE status=PASS "
        f"recommended_rules={len(RECOMMENDED_RULES)} journal_rules=1 "
        f"recommended_words={recommended_words} outside_words={outside_words} "
        f"recommended_paragraphs={recommended_paragraphs} outside_paragraphs={outside_paragraphs} "
        f"recommended_keywords={recommended_keyword_count} outside_keywords={outside_keyword_count} "
        "recommendation_mode=manual journal_mode=conditional-manual proof_state_promoted=0"
    )


if __name__ == "__main__":
    main()
