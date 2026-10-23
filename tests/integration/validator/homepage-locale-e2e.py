#!/usr/bin/env python3
"""Productive, offline four-locale homepage browser smoke."""
from functools import partial
from http.server import ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from urllib.parse import urlsplit
import argparse
import json
import runpy
import shutil
import tempfile

browser_utils = runpy.run_path(str(Path(__file__).with_name("web-lite-e2e.py")), run_name="homepage_browser_utils")
Browser = browser_utils["Browser"]
DenyProxyHandler = browser_utils["DenyProxyHandler"]
QuietHandler = browser_utils["QuietHandler"]
performance_request_urls = browser_utils["performance_request_urls"]
external_http_requests = browser_utils["external_http_requests"]
csp_log_violations = browser_utils["csp_log_violations"]

EXPECTED = {
    "pt-BR": ("Por onde começar", "Abrir validador Web/Lite", "Idioma do site"),
    "en": ("Getting started", "Open Web/Lite validator", "Website language"),
    "es": ("Primeros pasos", "Abrir validador Web/Lite", "Idioma del sitio"),
    "fr": ("Pour commencer", "Ouvrir le validateur Web/Lite", "Langue du site"),
}
def fail(reason):
    raise SystemExit("HOMEPAGE-BROWSER-EVIDENCE status=FAIL " + reason)
def snapshot(browser):
    return browser.execute("""return (() => ({
        lang: document.documentElement.lang,
        selected: document.getElementById("home-locale").value,
        heading: document.querySelector('[data-i18n="startHeading"]').textContent,
        cta: document.querySelector('[data-i18n="openValidator"]').textContent,
        selectorLabel: document.querySelector('[data-i18n="localeLabel"]').textContent,
        description: document.querySelector('meta[name="description"]').content,
        disclaimer: document.querySelector('[data-i18n="communityText"]').textContent,
        footer: document.querySelector('[data-i18n="footerText"]').textContent,
        originalLinks: Array.from(document.querySelectorAll("a")).map(x=>x.getAttribute("href")),
        fileNames: Array.from(document.querySelectorAll("code")).map(x=>x.textContent),
        contentReady: document.querySelectorAll("[data-i18n]").length
    }))()""")
def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--site-root", type=Path, required=True)
    parser.add_argument("--evidence", type=Path, required=True)
    args = parser.parse_args()
    root = args.site_root.resolve()
    if not (root/"index.html").is_file() or not (root/"homepage-locales.js").is_file():
        fail("missing_assembled_homepage")
    chrome = shutil.which("google-chrome") or shutil.which("chromium") or shutil.which("chromium-browser")
    driver = shutil.which("chromedriver")
    if not chrome or not driver:
        fail("missing_browser")
    args.evidence.parent.mkdir(parents=True,exist_ok=True)
    server=ThreadingHTTPServer(("127.0.0.1",0),partial(QuietHandler,directory=str(root)))
    thread=Thread(target=server.serve_forever,daemon=True)
    thread.start()
    proxy=ThreadingHTTPServer(("127.0.0.1",0),DenyProxyHandler)
    proxy.denied_requests=[]
    proxy_thread=Thread(target=proxy.serve_forever,daemon=True)
    proxy_thread.start()
    browser=Browser(chrome,driver,args.evidence.with_name("homepage-chromedriver.log"),proxy.server_port)
    samples={}
    try:
        browser.start()
        for locale,(heading,cta,label) in EXPECTED.items():
            browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html?lang={locale}")
            item=snapshot(browser)
            if (item["lang"],item["selected"],item["heading"],item["cta"],item["selectorLabel"]) != (locale,locale,heading,cta,label):
                fail(f"locale={locale} observed={item!r}")
            if len(item["description"])<30 or not item["disclaimer"] or not item["footer"] or item["contentReady"]<29:
                fail("incomplete_visible_translation:"+locale)
            if set(item["originalLinks"]) != {
                "./validator/",
                "https://github.com/tiagosombrra/abntexto-ufc/releases",
                "https://github.com/tiagosombrra/abntexto-ufc",
                "https://github.com/tiagosombrra/abntexto-ufc#readme",
                "https://github.com/tiagosombrra/abntexto-ufc/issues",
            }:
                fail("canonical_urls_changed:"+locale)
            if "abntexto-ufc-reference.pdf" not in item["fileNames"]:
                fail("canonical_filename_changed:"+locale)
            samples[locale]={"lang":item["lang"],"heading":item["heading"],"description":item["description"],"disclaimer":item["disclaimer"]}
        # Exercise an actual user-visible selector change without reloading.
        changed=browser.execute("""const s=document.getElementById('home-locale');
            s.value='en';s.dispatchEvent(new Event('change',{bubbles:true}));
            return [document.documentElement.lang,s.value,document.querySelector('[data-i18n="startHeading"]').textContent];""")
        if changed != ["en","en","Getting started"]:
            fail("selector_change_not_productive")
        # Unsupported deep-link locale must fail safely to the Portuguese baseline.
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html?lang=xx")
        if snapshot(browser)["lang"] != "pt-BR":
            fail("unsupported_locale_fallback")
        requests=performance_request_urls(browser.logs("performance"))
        external=external_http_requests(requests,server.server_port)
        if external:
            fail("external_network:"+",".join(external))
        if csp_log_violations(browser.logs("browser")):
            fail("csp_violation")
        evidence={"status":"PASS","locales":samples,"selector_change":"PASS","invalid_locale_fallback":"pt-BR","same_origin_assets":True,"external_http_requests":0,"csp":"PASS"}
        args.evidence.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("HOMEPAGE-BROWSER-EVIDENCE status=PASS locales=4 selector_change=PASS fallback=PASS canonical_links=PASS external_network=DENIED csp=PASS")
    finally:
        browser.stop()
        server.shutdown();server.server_close();thread.join(timeout=5)
        proxy.shutdown();proxy.server_close();proxy_thread.join(timeout=5)
if __name__=="__main__":
    main()
