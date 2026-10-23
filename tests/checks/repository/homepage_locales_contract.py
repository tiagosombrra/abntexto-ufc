#!/usr/bin/env python3
"""Fail-closed multilingual homepage contract; no browser/TeX required."""
from html.parser import HTMLParser
from pathlib import Path
import json
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
HTML = (ROOT / "site/index.html").read_text(encoding="utf-8")
JS = (ROOT / "site/homepage-locales.js").read_text(encoding="utf-8")

class HomepageParser(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.tokens = {}
        self.current = None
        self.options = set()
        self.hrefs = []
        self.scripts = []
        self.select_found = False
        self.label_found = False
        self.language_default = False
        self.meta_description = None
        self.default_text = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "html":
            self.language_default = attrs.get("lang") == "pt-BR"
        if tag == "meta" and attrs.get("name") == "description":
            self.meta_description = attrs.get("content")
        if tag == "script":
            self.scripts.append(attrs.get("src"))
        if tag == "label" and attrs.get("for") == "home-locale":
            self.label_found = True
        if tag == "select" and attrs.get("id") == "home-locale":
            self.select_found = True
        if tag == "option" and attrs.get("value"):
            self.options.add(attrs["value"])
        if tag == "a":
            self.hrefs.append(attrs.get("href"))
        if attrs.get("data-i18n"):
            key = attrs["data-i18n"]
            if key in self.tokens or self.current is not None:
                raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL duplicate_or_nested_key={key}")
            self.tokens[key] = ""
            self.current = (tag, key)
    def handle_data(self, value):
        if self.current:
            self.tokens[self.current[1]] += value
    def handle_endtag(self, tag):
        if self.current and tag == self.current[0]:
            self.current = None

parser = HomepageParser()
parser.feed(HTML)
if parser.current is not None:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL incomplete_translation_element")
if not parser.language_default or not parser.select_found or not parser.label_found:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL accessible_locale_selector")
if parser.options != {"pt-BR", "en", "es", "fr"}:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL selector_options")
if parser.scripts != ["./homepage-locales.js"]:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL script_origin")
if "http-equiv=\"Content-Security-Policy\"" not in HTML:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL missing_csp")
expected_hrefs = (
    "./validator/", "https://github.com/tiagosombrra/abntexto-ufc/releases",
    "https://github.com/tiagosombrra/abntexto-ufc",
    "https://github.com/tiagosombrra/abntexto-ufc#readme",
    "https://github.com/tiagosombrra/abntexto-ufc/issues",
)
if set(parser.hrefs) != set(expected_hrefs) or len(parser.hrefs) != 6:
    raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL canonical_hrefs={parser.hrefs}")
if any(mark in JS for mark in ("fetch(", "XMLHttpRequest", "sendBeacon", "localStorage", "sessionStorage", "innerHTML")):
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL unexpected_network_storage_or_markup")
data = json.loads(subprocess.check_output(
    ["node", "-e", "const s=require('./site/homepage-locales.js');process.stdout.write(JSON.stringify({copies:s.HOME_COPY,locales:s.HOME_LOCALES}))"],
    cwd=ROOT, text=True
))
if data["locales"] != ["pt-BR", "en", "es", "fr"] or set(data["copies"]) != set(data["locales"]):
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL locales")
baseline = data["copies"]["pt-BR"]
if set(baseline) != set(parser.tokens) | {"metaDescription"}:
    raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL unused_or_missing_keys expected={sorted(set(parser.tokens)|{'metaDescription'})} actual={sorted(baseline)}")
if parser.meta_description != baseline["metaDescription"]:
    raise SystemExit("HOMEPAGE-I18N-EVIDENCE status=FAIL default_description")
def normalized(value):
    return re.sub(r"\s+", " ", value).strip()
for key,value in parser.tokens.items():
    if normalized(value) != normalized(baseline[key]):
        raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL default_pt_drift={key}")
for locale,words in data["copies"].items():
    if set(words) != set(baseline):
        raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL missing_keys={locale}")
    if any(not isinstance(v,str) or not v.strip() or "<" in v for v in words.values()):
        raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL invalid_text={locale}")
    if words["metaDescription"] == baseline["metaDescription"] and locale != "pt-BR":
        raise SystemExit(f"HOMEPAGE-I18N-EVIDENCE status=FAIL untranslated_description={locale}")
print(f"HOMEPAGE-I18N-EVIDENCE status=PASS locales=4 keys={len(baseline)} default_pt=IDENTICAL accessible_selector=true canonical_links=true script_same_origin=true")
