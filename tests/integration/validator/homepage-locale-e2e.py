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
wait_for = browser_utils["wait_for"]

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
RETURN_LABELS = {
    "pt-BR": "Voltar ao site",
    "en": "Back to website",
    "es": "Volver al sitio",
    "fr": "Retour au site",
}
FAQ_EXPECTED = {
    "pt-BR": (
        "Ajuda para começar e dúvidas frequentes",
        ("Qual ZIP devo usar?", "Por que o validador pede revisão manual?", "O que verificar se a compilação falhar?"),
        "Baixar a v3.0.5 publicada", "Guia da linha em desenvolvimento (em português)",
    ),
    "en": (
        "Getting started and frequently asked questions",
        ("Which ZIP should I use?", "Why does the validator require manual review?", "What should I check if compilation fails?"),
        "Download published v3.0.5", "Development-branch guide (Portuguese)",
    ),
    "es": (
        "Primeros pasos y preguntas frecuentes",
        ("¿Qué archivo ZIP debo utilizar?", "¿Por qué el validador solicita revisión manual?", "¿Qué revisar si falla la compilación?"),
        "Descargar v3.0.5 publicada", "Guía de la rama en desarrollo (en portugués)",
    ),
    "fr": (
        "Premiers pas et questions fréquentes",
        ("Quelle archive ZIP utiliser ?", "Pourquoi le validateur demande-t-il une vérification manuelle ?", "Que vérifier si la compilation échoue ?"),
        "Télécharger la version publiée v3.0.5", "Guide de la branche en développement (en portugais)",
    ),
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
        helpHeading: document.querySelector('[data-i18n="helpHeading"]').textContent,
        helpNavigationName: document.querySelector('.help-links').getAttribute('aria-labelledby'),
        faq: Array.from(document.querySelectorAll('.help details')).map(node=>({
          question:node.querySelector('summary').textContent,
          answer:node.querySelector('p').textContent,
          open:node.open
        })),
        stableReleaseLabel: document.querySelector('[data-i18n="stableReleaseLink"]').textContent,
        guideLabel: document.querySelector('[data-i18n="guideLink"]').textContent,
        contentReady: document.querySelectorAll("[data-i18n]").length
    }))()""")

def verify_home_responsive_keyboard(browser, port):
    """Check mobile layout and a real keyboard focus transition on the published homepage."""
    browser.navigate(f"http://127.0.0.1:{port}/index.html?lang=pt-BR")
    results={}
    for width in (320,375,768,1440):
        browser.command("POST", "/goog/cdp/execute", {
            "cmd": "Emulation.setDeviceMetricsOverride",
            "params": {"width":width,"height":900,"deviceScaleFactor":1,"mobile":False},
        })
        observed=browser.execute("""return (() => {
            const selector=document.querySelector('#home-locale');
            const action=document.querySelector('a[data-i18n="openValidator"]');
            const rect=action.getBoundingClientRect();
            return {viewport:innerWidth,bodyWidth:document.documentElement.scrollWidth,
                locale:document.documentElement.lang,
                selectorWidth:selector.getBoundingClientRect().width,
                actionWidth:rect.width,actionLeft:rect.left,actionRight:rect.right};
        })()""")
        if (observed["viewport"] != width or observed["bodyWidth"] > width+1 or observed["locale"] != "pt-BR"):
            fail(f"homepage responsive overflow at {width}px: {observed!r}")
        if observed["actionLeft"] < -1 or observed["actionRight"] > width+1 or observed["selectorWidth"] < 50:
            fail(f"homepage interactive controls outside viewport at {width}px: {observed!r}")
        results[str(width)]={"viewport":width,"document_overflow":False,"cta_visible":True}
    browser.command("POST", "/goog/cdp/execute", {
        "cmd": "Emulation.setDeviceMetricsOverride",
        "params": {"width":320,"height":900,"deviceScaleFactor":1,"mobile":False},
    })
    browser.execute("document.querySelector('#home-locale').focus();")
    browser.command("POST", "/actions", {"actions": [{
        "type":"key","id":"homepage-a11y-keyboard",
        "actions":[
            {"type":"keyDown","value":"\ue004"},
            {"type":"keyUp","value":"\ue004"},
        ],
    }]})
    focus=browser.execute("""return (() => {
        const e=document.activeElement,style=getComputedStyle(e);
        return {href:e.getAttribute('href'),visible:e.matches(':focus-visible'),
            outlineStyle:style.outlineStyle,outlineWidth:parseFloat(style.outlineWidth)};
    })()""")
    if (focus["href"] != "./validator/?lang=pt-BR" or not focus["visible"] or focus["outlineStyle"] == "none" or focus["outlineWidth"] < 2):
        fail(f"homepage keyboard focus visibility drift: {focus!r}")
    browser.command("POST", "/goog/cdp/execute", {
        "cmd": "Emulation.clearDeviceMetricsOverride","params":{},
    })
    print("HOMEPAGE-RESPONSIVE-EVIDENCE status=PASS viewports=320,375,768,1440 "
          "document_overflow=0 keyboard_tab_focus=PASS cta=VISIBLE")
    return {"status":"PASS","viewports":results,"keyboard_tab_focus":focus}

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
                "https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.5",
                "https://github.com/tiagosombrra/abntexto-ufc/blob/main/docs/USER-GUIDE.md",
            }:
                fail("canonical_urls_changed:"+locale)
            if item["originalLinks"].count("./validator/?lang="+locale) != 2:
                fail("validator_secondary_link_lost:"+locale)
            expected_help, expected_questions, expected_release, expected_guide = FAQ_EXPECTED[locale]
            if (item["helpHeading"],item["stableReleaseLabel"],item["guideLabel"]) != (
                expected_help,expected_release,expected_guide
            ):
                fail("untranslated_onboarding_or_release_guide:"+locale)
            if item["helpNavigationName"] != "help-heading":
                fail("faq_navigation_has_untranslated_name:"+locale)
            if (
                len(item["faq"]) != 3
                or tuple(entry["question"] for entry in item["faq"]) != expected_questions
                or any(entry["open"] or len(entry["answer"]) < 70 for entry in item["faq"])
            ):
                fail("faq_missing_or_untranslated:"+locale)
            if "v3.0.5" not in item["faq"][0]["answer"] or "v3.1.0" not in item["faq"][0]["answer"]:
                fail("published_development_boundary_lost:"+locale)
            # Native disclosure must actually expand in Chromium, not just exist in HTML.
            browser.click(".help details:first-of-type summary")
            if browser.execute("return !document.querySelector('.help details').open;"):
                fail("faq_disclosure_did_not_open:"+locale)
            browser.click(".help details:first-of-type summary")
            if browser.execute("return document.querySelector('.help details').open;"):
                fail("faq_disclosure_did_not_close:"+locale)
            if "abntexto-ufc-reference.pdf" not in item["fileNames"]:
                fail("canonical_filename_changed:"+locale)
            # A deep-linked validator must expose a same-origin, keyboard-reachable return.
            browser.navigate(f"http://127.0.0.1:{server.server_port}/validator/?lang={locale}")
            back=browser.execute("""return (() => {
                const a=document.querySelector('#home-return');
                const destination=new URL(a.href,window.location.href);
                return {lang:document.documentElement.lang,
                  text:a.textContent,href:a.getAttribute('href'),
                  sameOrigin:destination.origin===window.location.origin,
                  pathname:destination.pathname,language:destination.searchParams.get('lang'),
                  hidden:a.hidden};
            })()""")
            if back != {
                "lang":locale,"text":RETURN_LABELS[locale],
                "href":"../?lang="+locale,"sameOrigin":True,"pathname":"/",
                "language":locale,"hidden":False,
            }:
                fail(f"localized_validator_home_return_invalid:{locale}:{back!r}")
            browser.command("POST", "/actions", {"actions": [{
                "type":"key","id":"validator-return-tab",
                "actions":[{"type":"keyDown","value":"\ue004"},
                           {"type":"keyUp","value":"\ue004"}],
            }]})
            focus=browser.execute("""const a=document.querySelector('#home-return');
                const style=getComputedStyle(a);
                return {active:document.activeElement===a,
                  visible:a.matches(':focus-visible'),
                  outlineStyle:style.outlineStyle,
                  outlineWidth:parseFloat(style.outlineWidth)};""")
            if not focus["active"] or not focus["visible"] or focus["outlineStyle"] == "none" or focus["outlineWidth"] < 2:
                fail(f"validator_return_keyboard_focus_missing:{locale}:{focus!r}")
            browser.click("#home-return")
            wait_for(
                lambda: browser.execute(
                    "return document.querySelector('#home-locale')?.value || null;"
                ) == locale,
                "validator to homepage return "+locale,timeout=15,
            )
            if browser.execute(
                "return new URLSearchParams(location.search).get('lang');"
            ) != locale:
                fail("return_route_lost_locale:"+locale)
            browser.click('a[data-i18n="openValidator"]')
            wait_for(
                lambda: browser.execute(
                    "return document.querySelector('#ui-locale')?.value || null;"
                ) == locale,
                "homepage to validator roundtrip "+locale,timeout=15,
            )
            if browser.execute(
                "return document.querySelector('#home-return').getAttribute('href');"
            ) != "../?lang="+locale:
                fail("roundtrip_return_link_lost_locale:"+locale)
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
        responsive=verify_home_responsive_keyboard(browser,server.server_port)
        requests=performance_request_urls(browser.logs("performance"))
        external=external_http_requests(requests,server.server_port)
        if external:
            fail("external_network:"+",".join(external))
        if csp_log_violations(browser.logs("browser")):
            fail("csp_violation")
        evidence={"status":"PASS","locales":samples,"selector_change":"PASS","cross_page_locale":"PASS","stored_preference":"PASS","invalid_locale_fallback":"pt-BR","invalid_storage_fallback":"pt-BR","storage_denial":"PASS","responsive_keyboard":responsive,"return_navigation":"PASS","onboarding_faq":"PASS","stable_guide_links":"PASS","same_origin_assets":True,"external_http_requests":0,"csp":"PASS"}
        args.evidence.write_text(json.dumps(evidence,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
        print("HOMEPAGE-BROWSER-EVIDENCE status=PASS locales=4 selector_change=PASS cross_page=PASS storage=PASS invalid_fallback=PASS responsive_keyboard=PASS return_roundtrip=LOCALIZED_4 keyboard_return=PASS faq=LOCALIZED_4 disclosures=PASS stable_guide_links=PASS canonical_links=PASS external_network=DENIED csp=PASS")
    finally:
        browser.stop()
        server.shutdown();server.server_close();thread.join(timeout=5)
        proxy.shutdown();proxy.server_close();proxy_thread.join(timeout=5)
if __name__=="__main__":
    main()
