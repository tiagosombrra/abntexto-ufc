#!/usr/bin/env python3
"""Fail-closed coverage audit of the 4-locale class-generated text catalog.

This is a *source catalog coverage* proof, not an official terminology review.
Keep public inherited package strings and user-authored metadata separately
audited through real PDF integration and institutional policy sign-off.
"""
from collections import defaultdict
from pathlib import Path
import re

source = Path("abntexto-ufc.cls").read_text(encoding="utf-8")
langs = {"pt", "en", "es", "fr"}

def between(begin: str, end: str) -> str:
    if source.count(begin) != 1:
        raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL missing_or_repeated={begin}")
    return source.split(begin, 1)[1].split(end, 1)[0]

def gather(matches, category):
    found = defaultdict(dict)
    for locale, key, value in matches:
        if key in found[locale] or not value.strip():
            raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL repeated_or_empty={category}:{locale}/{key}")
        found[locale][key] = value
    if set(found) != langs:
        raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL locale_set={category}:{sorted(found)}")
    baseline = set(found["pt"])
    for locale in sorted(langs):
        if set(found[locale]) != baseline:
            raise SystemExit(
                f"LOCALE-CATALOG-EVIDENCE status=FAIL unequal_keys={category}:{locale} "
                f"missing={sorted(baseline - set(found[locale]))} "
                f"extra={sorted(set(found[locale]) - baseline)}"
            )
    return baseline

heading_src = between(
    r"\prop_gset_from_keyval:Nn \g_ufc_heading_labels_prop", r"\cs_generate_variant:Nn"
)
heading_keys = gather(
    re.findall(r"^\s*(pt|en|es|fr)/([\w-]+)\s*=\s*\{([^{}]+)\}", heading_src, re.M),
    "pretextual",
)
if len(heading_keys) != 9:
    raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL pretextual_count={len(heading_keys)}")

text_src = between(
    r"\prop_gset_from_keyval:Nn \g_ufc_document_text_prop",
    r"\cs_new:Npn \ufc_doc_text:n"
)
inline = re.findall(
    r"^\s*(pt|en|es|fr)/([\w-]+)\s*=\s*\{([^{}]+)\}",
    text_src, re.M,
)
# Nature strings are nested TeX token trees; capture the locale and ensure
# the complete value begins with nonempty text, plus matched four-locale keys.
nature = re.findall(
    r"^\\prop_gput:Nnn \\g_ufc_document_text_prop "
    r"\{(pt|en|es|fr)/([\w-]+)\} \{(.+)\}$",
    text_src, re.M,
)
text_keys = gather(inline + nature, "document")
expected = {
    "advisor-male", "advisor-female", "coadvisor-male", "coadvisor-female",
    "approved-on", "examining-committee", "volume",
    "undergraduate-program-line", "specialization-program-line",
    "submitted-on", "article-approved-on", "references", "glossary",
    "list-charts", "list-code", "list-algorithms",
    "caption-chart", "caption-code", "caption-algorithm", "caption-text-table",
    "appendix", "annex", "index", "default-project-type",
    "caption-figure", "caption-table", "source-label", "note-label",
    "nature-undergraduate", "nature-specialization", "nature-masters",
    "nature-doctoral", "nature-project",
}
if text_keys != expected:
    raise SystemExit(
        "LOCALE-CATALOG-EVIDENCE status=FAIL unexpected_document_catalog "
        f"missing={sorted(expected - text_keys)} extra={sorted(text_keys - expected)}"
    )

used = set(re.findall(r"\\ufc_doc_text:n\s*\{([\w-]+)\}", source))
if expected - used:
    raise SystemExit(
        "LOCALE-CATALOG-EVIDENCE status=FAIL unused_or_unrouted_labels "
        f"missing={sorted(expected - used)}"
    )
if used - text_keys:
    raise SystemExit(
        f"LOCALE-CATALOG-EVIDENCE status=FAIL missing_runtime_labels={sorted(used - text_keys)}"
    )
for table_name, key in (("summary", "summary_headings"), ("keywords", "summary_keywords")):
    material = between(
        rf"\prop_gset_from_keyval:Nn \g_ufc_{key}_prop",
        r"\tl_new:N \g_ufc_cover_mode_tl",
    )
    if not re.search(r"\{\s*pt=\{[^}]+\},en=\{[^}]+\},es=\{[^}]+\},fr=\{[^}]+\}\s*\}", material):
        raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL summary_catalog={table_name}")

# Our own generated fixed Portuguese labels should only be in the PT catalog,
# the PT defaults for immutable institutional proper names, or legacy commands.
required_routes = (
    r"\ufc_doc_text:n {nature-doctoral}",
    r"\ufc_doc_text:n {default-project-type}",
    r"\ufc_doc_text:n {examining-committee}",
    r"\ufc_doc_text:n {approved-on}",
    r"\ufc_doc_text:n {references}",
    r"\ufc_doc_text:n {glossary}",
    r"\ufc_doc_text:n {caption-text-table}",
    r"\cs_gset:Npn \appendixlabel",
    r"\cs_gset:Npn \annexlabel",
    r"\cs_gset:Npn \abntextonotelabel",
    r"\cs_gset:Npn \legendlabel",
    r"\cs_gset:Npn \sublegendlabel",
    r"\cs_new_eq:NN \ufc_original_alternativesublegend \alternativesublegend",
    r"\currentlegendID\nobreakspace{}",
    r"\ufc_doc_text:n {note-label}",
)
for route in required_routes:
    if route not in source:
        raise SystemExit(f"LOCALE-CATALOG-EVIDENCE status=FAIL missing_render_route={route}")

print(
    "LOCALE-CATALOG-EVIDENCE status=PASS locales=4 "
    f"pretextual_keys={len(heading_keys)} document_keys={len(text_keys)} "
    "summary_keys=2 complete_per_locale=true usage_coverage=PASS "
    "scope=class_owned_labels official_wording_review=PENDING"
)
