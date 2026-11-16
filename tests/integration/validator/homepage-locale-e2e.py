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

READMES = {"pt-BR": "README completo", "en": "Full README", "es": "README completo", "fr": "README complet"}

VERSION_LABELS = {
    "pt-BR": ("Estado das versões", "Versão publicada:", "Em desenvolvimento:"),
    "en": ("Release status", "Published version:", "In development:"),
    "es": ("Estado de las versiones", "Versión publicada:", "En desarrollo:"),
    "fr": ("Statut des versions", "Version publiée :", "En développement :"),
}

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
        readmeLabel: document.querySelector('a[href="https://github.com/tiagosombrra/abntexto-ufc#readme"]').textContent,
        releaseHeading: document.querySelector('[data-i18n="releaseStateHeading"]').textContent,
        publishedLabel: document.querySelector('[data-i18n="publishedVersionLabel"]').textContent,
        publishedText: document.querySelector('[data-i18n="publishedVersionText"]').textContent,
        developmentLabel: document.querySelector('[data-i18n="developmentVersionLabel"]').textContent,
        developmentText: document.querySelector('[data-i18n="developmentVersionText"]').textContent,
        publishedVersion: document.querySelector('code[data-version="published"]').textContent,
        developmentVersion: document.querySelector('code[data-version="development"]').textContent,
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
            if item["readmeLabel"] != READMES[locale]:
                fail("untranslated_readme_link:"+locale)
            if (item["releaseHeading"],item["publishedLabel"],item["developmentLabel"]) != VERSION_LABELS[locale]:
                fail("untranslated_release_status:"+locale)
            if (item["publishedVersion"],item["developmentVersion"]) != ("v3.0.5","v3.1.0"):
                fail("untrusted_release_version:"+locale)
            if "Releases" not in item["publishedText"] or "v3.0.5" not in item["developmentText"]:
                fail("development_misrepresented_as_download:"+locale)
            if len(item["description"])<30 or not item["disclaimer"] or not item["footer"] or item["contentReady"]<30:
                fail("incomplete_visible_translation:"+locale)
            if set(item["originalLinks"]) != {
                "./validator/?lang="+locale,
                "https://github.com/tiagosombrra/abntexto-ufc/releases",
                "https://github.com/tiagosombrra/abntexto-ufc",
                "https://github.com/tiagosombrra/abntexto-ufc#readme",
                "https://github.com/tiagosombrra/abntexto-ufc/issues",
            }:
                fail("canonical_urls_changed:"+locale)
            if item["originalLinks"].count("./validator/?lang="+locale) != 2:
                fail("validator_secondary_link_lost:"+locale)
            if "abntexto-ufc-reference.pdf" not in item["fileNames"]:
                fail("canonical_filename_changed:"+locale)
            samples[locale]={"lang":item["lang"],"heading":item["heading"],"description":item["description"],"disclaimer":item["disclaimer"],"published":item["publishedVersion"],"development":item["developmentVersion"]}
        # Changing the homepage selector updates the URL and both validator links.
        changed=browser.execute("""const s=document.getElementById('home-locale');
            s.value='en';s.dispatchEvent(new Event('change',{bubbles:true}));
            return [document.documentElement.lang,s.value,
                document.querySelector('[data-i18n="startHeading"]').textContent,
                new URLSearchParams(window.location.search).get('lang')];""")
        if changed != ["en","en","Getting started","en"]:
            fail("selector_change_not_productive")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        if snapshot(browser)["lang"] != "en":
            fail("homepage_stored_locale_not_restored")

        # A real same-origin navigation must carry locale into the validator.
        validator_url=f"http://127.0.0.1:{server.server_port}/validator/?lang=en"
        browser.navigate(validator_url)
        validator=browser.execute("""return [document.documentElement.lang,
            document.querySelector('#ui-locale').value,
            new URLSearchParams(window.location.search).get('lang')];""")
        if validator != ["en","en","en"]:
            fail("homepage_to_validator_locale_lost")

        # A change inside the validator must persist across return navigation.
        validator_changed=browser.execute("""const s=document.querySelector('#ui-locale');
            s.value='fr';s.dispatchEvent(new Event('change',{bubbles:true}));
            return [document.documentElement.lang,s.value,
                new URLSearchParams(window.location.search).get('lang')];""")
        if validator_changed != ["fr","fr","fr"]:
            fail("validator_locale_change_not_persisted")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        if snapshot(browser)["lang"] != "fr":
            fail("validator_to_homepage_locale_lost")

        # An unsupported deep link must fall back to PT without poisoning storage.
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html?lang=xx")
        if snapshot(browser)["lang"] != "pt-BR":
            fail("unsupported_homepage_locale_fallback")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/validator/?lang=xx")
        bad_validator=browser.execute("""return [document.documentElement.lang,
            document.querySelector('#ui-locale').value];""")
        if bad_validator != ["pt-BR","pt-BR"]:
            fail("unsupported_validator_locale_fallback")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        if snapshot(browser)["lang"] != "fr":
            fail("invalid_deep_link_poisoned_stored_locale")

        # Invalid stored values must not become an unsupported locale.
        browser.execute("""localStorage.setItem('abntexto-ufc.ui-locale','xx');""")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        if snapshot(browser)["lang"] != "pt-BR":
            fail("unsupported_stored_homepage_locale_fallback")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/validator/")
        bad_storage_validator=browser.execute("""return [document.documentElement.lang,
            document.querySelector('#ui-locale').value];""")
        if bad_storage_validator != ["pt-BR","pt-BR"]:
            fail("unsupported_stored_validator_locale_fallback")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")

        # Storage denial must not break the visible UI or URL-based handoff.
        storage_block=browser.execute("""const original=Storage.prototype.setItem;
            Storage.prototype.setItem=function(){throw Error('storage disabled');};
            try {
              let denied=false;
              try {localStorage.setItem('abntexto-ufc.ui-locale','xx');} catch {denied=true;}
              const s=document.querySelector('#home-locale');
              s.value='es';s.dispatchEvent(new Event('change',{bubbles:true}));
              return [denied,document.documentElement.lang,s.value,
                new URLSearchParams(window.location.search).get('lang'),
                document.querySelector('a[data-i18n="openValidator"]').getAttribute('href')];
            } finally {Storage.prototype.setItem=original;}""")
        if storage_block != [True,"es","es","es","./validator/?lang=es"]:
            fail("homepage_storage_denied_not_safe")
        browser.navigate(f"http://127.0.0.1:{server.server_port}/validator/?lang=es")
        denied_validator=browser.execute("""const original=Storage.prototype.setItem;
            Storage.prototype.setItem=function(){throw Error('storage disabled');};
            try {
              let denied=false;
              try {localStorage.setItem('abntexto-ufc.ui-locale','xx');} catch {denied=true;}
              const s=document.querySelector('#ui-locale');
              s.value='en';s.dispatchEvent(new Event('change',{bubbles:true}));
              return [denied,document.documentElement.lang,s.value,
                new URLSearchParams(window.location.search).get('lang')];
            } finally {Storage.prototype.setItem=original;}""")
        if denied_validator != [True,"en","en","en"]:
            fail("validator_storage_denied_not_safe")
        requests=performance_request_urls(browser.logs("performance"))
        external=external_http_requests(requests,server.server_port)
        if external:
            fail("external_network:"+",".join(external))
        if csp_log_violations(browser.logs("browser")):
            fail("csp_violation")
        evidence={"status":"PASS","locales":samples,"selector_change":"PASS","cross_page_locale":"PASS","stored_preference":"PASS","invalid_locale_fallback":"pt-BR","invalid_storage_fallback":"pt-BR","storage_denial":"PASS","same_origin_assets":True,"external_http_requests":0,"csp":"PASS"}
        args.evidence.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("HOMEPAGE-BROWSER-EVIDENCE status=PASS locales=4 selector_change=PASS cross_page=PASS storage=PASS invalid_fallback=PASS canonical_links=PASS external_network=DENIED csp=PASS")
    finally:
        browser.stop()
        server.shutdown();server.server_close();thread.join(timeout=5)
        proxy.shutdown();proxy.server_close();proxy_thread.join(timeout=5)
if __name__=="__main__":
    main()
