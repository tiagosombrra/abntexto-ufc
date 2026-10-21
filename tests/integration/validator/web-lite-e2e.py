#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import io
import re
import hashlib
import json
import shutil
import socket
import sys
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from functools import partial
from http.server import BaseHTTPRequestHandler, SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
from pathlib import Path
from threading import Thread
from typing import Any

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT  # noqa: E402

TOOLS = ROOT / "tools"
if str(TOOLS) not in sys.path:
    sys.path.insert(0, str(TOOLS))

from repository_paths import standard_file

VALIDATOR = ROOT / "validator"
CONTRACT = VALIDATOR / "validation-contract.json"
CATALOG = standard_file("catalog.json")
ELEMENT_KEY = "element-6066-11e4-a52e-4f735466cecf"
PASS = "PASS"
FAIL = "FAIL"
REVIEW = "MANUAL REVIEW"
CSP_POLICY = "default-src 'self'; script-src 'self'; style-src 'self' 'unsafe-inline'; worker-src 'self'; connect-src 'self'; img-src 'self' data:; object-src 'none'; frame-src 'none'; base-uri 'none'; form-action 'none'"


def fail(message: str) -> None:
    raise SystemExit(f"Web/Lite E2E failed: {message}")


def free_port() -> int:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
        sock.bind(("127.0.0.1", 0))
        return int(sock.getsockname()[1])


def http_json(method: str, url: str, payload: Any | None = None, timeout: float = 30) -> Any:
    data = None if payload is None else json.dumps(payload).encode("utf-8")
    request = urllib.request.Request(
        url,
        data=data,
        method=method,
        headers={"Content-Type": "application/json;charset=UTF-8"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw = response.read()
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")
        fail(f"WebDriver HTTP {exc.code} for {method} {url}: {detail}")
    except OSError as exc:
        raise RuntimeError(f"WebDriver request failed for {method} {url}: {exc}") from exc
    parsed = json.loads(raw.decode("utf-8")) if raw else {}
    value = parsed.get("value", parsed) if isinstance(parsed, dict) else parsed
    if isinstance(value, dict) and value.get("error"):
        fail(f"WebDriver error {value.get('error')}: {value.get('message')}")
    return value


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, fmt: str, *args: object) -> None:
        pass


class DenyProxyHandler(BaseHTTPRequestHandler):
    protocol_version = "HTTP/1.1"

    def log_message(self, fmt: str, *args: object) -> None:
        pass

    def deny(self) -> None:
        denied = getattr(self.server, "denied_requests", None)
        if isinstance(denied, list):
            denied.append(self.requestline)
        self.send_response(502)
        self.send_header("Content-Length", "0")
        self.send_header("Connection", "close")
        self.end_headers()

    def do_CONNECT(self) -> None:
        self.deny()

    def do_GET(self) -> None:
        self.deny()

    def do_HEAD(self) -> None:
        self.deny()

    def do_POST(self) -> None:
        self.deny()


class Browser:
    def __init__(self, chrome: str, chromedriver: str, driver_log: Path, proxy_port: int) -> None:
        self.chrome = chrome
        self.chromedriver = chromedriver
        self.driver_log = driver_log
        self.proxy_port = proxy_port
        self.port = free_port()
        self.base = f"http://127.0.0.1:{self.port}"
        self.process: subprocess.Popen[bytes] | None = None
        self.session = ""

    def start(self) -> None:
        self.driver_log.parent.mkdir(parents=True, exist_ok=True)
        driver_stream = self.driver_log.open("wb")
        try:
            self.process = subprocess.Popen(
                [
                    self.chromedriver,
                    f"--port={self.port}",
                    "--verbose",
                ],
                stdout=driver_stream,
                stderr=subprocess.STDOUT,
            )
        finally:
            driver_stream.close()

        deadline = time.monotonic() + 30
        while time.monotonic() < deadline:
            if self.process.poll() is not None:
                detail = ""
                if self.driver_log.is_file():
                    detail = self.driver_log.read_text(
                        encoding="utf-8", errors="replace"
                    )[-4000:].strip()
                suffix = f" Log tail: {detail}" if detail else ""
                fail(
                    f"ChromeDriver exited before readiness with code "
                    f"{self.process.returncode}.{suffix}"
                )
            try:
                http_json("GET", self.base + "/status", timeout=1)
                break
            except RuntimeError:
                time.sleep(0.2)
        else:
            detail = ""
            if self.driver_log.is_file():
                detail = self.driver_log.read_text(
                    encoding="utf-8", errors="replace"
                )[-4000:].strip()
            suffix = f" Log tail: {detail}" if detail else ""
            fail(f"ChromeDriver did not become ready within 30 seconds.{suffix}")

        created = http_json(
            "POST",
            self.base + "/session",
            {
                "capabilities": {
                    "alwaysMatch": {
                        "browserName": "chrome",
                        "goog:loggingPrefs": {
                            "performance": "ALL",
                            "browser": "ALL",
                        },
                        "goog:chromeOptions": {
                            "binary": self.chrome,
                            "args": [
                                "--headless=new",
                                "--no-sandbox",
                                "--disable-dev-shm-usage",
                                "--disable-background-networking",
                                "--disable-component-update",
                                "--no-default-browser-check",
                                f"--proxy-server=http://127.0.0.1:{self.proxy_port}",
                                "--proxy-bypass-list=127.0.0.1;localhost",
                                "--host-resolver-rules=MAP * ~NOTFOUND, EXCLUDE 127.0.0.1, EXCLUDE localhost",
                                "--window-size=1440,1000",
                            ],
                        },
                    }
                }
            },
            timeout=90,
        )
        if not isinstance(created, dict) or not created.get("sessionId"):
            fail(f"ChromeDriver session response is invalid: {created!r}")
        self.session = str(created["sessionId"])
        self.command(
            "POST",
            "/timeouts",
            {"implicit": 0, "pageLoad": 60000, "script": 30000},
        )

    def command(self, method: str, path: str, payload: Any | None = None, timeout: float = 30) -> Any:
        base = f"{self.base}/session/{self.session}" if self.session else self.base
        return http_json(method, base + path, payload, timeout)

    def navigate(self, url: str) -> None:
        self.command("POST", "/url", {"url": url}, timeout=70)

    def execute(self, script: str, args: list[Any] | None = None) -> Any:
        return self.command("POST", "/execute/sync", {"script": script, "args": args or []})

    def execute_async(self, script: str, args: list[Any] | None = None) -> Any:
        return self.command("POST", "/execute/async", {"script": script, "args": args or []}, timeout=40)

    def logs(self, log_type: str) -> list[dict[str, Any]]:
        result = self.command("POST", "/log", {"type": log_type})
        if not isinstance(result, list):
            fail(f"WebDriver returned invalid {log_type} logs: {result!r}")
        return [entry for entry in result if isinstance(entry, dict)]

    def element(self, selector: str) -> str:
        result = self.command(
            "POST",
            "/element",
            {"using": "css selector", "value": selector},
        )
        if not isinstance(result, dict):
            fail(f"WebDriver returned an invalid element for {selector}: {result!r}")
        element = result.get(ELEMENT_KEY) or result.get("ELEMENT")
        if not element:
            fail(f"WebDriver did not return an element id for {selector}")
        return str(element)

    def send_file(self, selector: str, path: Path) -> None:
        element = self.element(selector)
        value = str(path.resolve())
        self.command(
            "POST",
            f"/element/{element}/value",
            {"text": value, "value": list(value)},
        )

    def click(self, selector: str) -> None:
        element = self.element(selector)
        self.command("POST", f"/element/{element}/click", {})

    def stop(self) -> None:
        if self.session:
            try:
                self.command("DELETE", "")
            except BaseException:
                pass
            self.session = ""
        if self.process is not None:
            self.process.terminate()
            try:
                self.process.wait(timeout=5)
            except subprocess.TimeoutExpired:
                self.process.kill()
            self.process = None


def wait_for(predicate, label: str, timeout: float = 180) -> None:
    deadline = time.monotonic() + timeout
    last: BaseException | None = None
    while time.monotonic() < deadline:
        try:
            if predicate():
                return
        except BaseException as exc:
            last = exc
        time.sleep(0.25)
    suffix = f"; last error: {last}" if last else ""
    fail(f"timeout waiting for {label}{suffix}")


def write_negative_pdf(path: Path) -> None:
    content = b"BT /F1 12 Tf 72 720 Td (Web Lite negative Letter fixture) Tj ET"
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 612 792] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        b"<< /Length " + str(len(content)).encode("ascii") + b" >>\nstream\n" + content + b"\nendstream",
        b"<< /Title (=1+2) >>",  # Real PDF Info dictionary: negative spreadsheet-formula control.
    ]
    data = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, body in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode("ascii"))
        data.extend(body)
        data.extend(b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(objects) + 1}\n".encode("ascii"))
    data.extend(b"0000000000 65535 f \n")
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    data.extend(
        (
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R /Info 6 0 R >>\n"
            f"startxref\n{xref}\n%%EOF\n"
        ).encode("ascii")
    )
    path.write_bytes(data)


def file_sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    checks = report.get("checks")
    if not isinstance(checks, list) or not checks:
        fail("browser report has no checks")
    result: dict[str, dict[str, Any]] = {}
    for check in checks:
        if not isinstance(check, dict) or not isinstance(check.get("id"), str):
            fail("browser report contains an invalid check")
        if check["id"] in result:
            fail(f"browser report contains duplicate check id {check['id']}")
        result[check["id"]] = check
    return result


def validate_schema(report: dict[str, Any], profile: str, contract: dict[str, Any], catalog: dict[str, Any], document_type: str = 'undergraduate-capstone', print_mode: str = 'single-sided') -> None:
    schema = contract["target_report_schema"]
    missing = [key for key in schema["required_top_level"] if key not in report]
    if missing:
        fail("browser report is missing top-level fields: " + ", ".join(missing))
    if report.get("profile") != profile:
        fail(f"browser profile mismatch: {report.get('profile')!r}")
    if report.get("document_type") != document_type:
        fail(f"browser document type mismatch: {report.get('document_type')!r} != {document_type!r}")
    if report.get("print_mode") != print_mode:
        fail(f"browser print mode mismatch: {report.get('print_mode')!r} != {print_mode!r}")
    if report.get("mode") != "web-lite-local":
        fail(f"browser mode mismatch: {report.get('mode')!r}")
    base = report.get("normative_catalog")
    expected_base = {"schema_version": catalog["schema_version"], "reviewed_at": catalog["reviewed_at"]}
    if base != expected_base:
        fail(f"browser normative catalog identity mismatch: {base!r} != {expected_base!r}")
    required_check = set(schema["required_check_fields"])
    for check in report["checks"]:
        absent = sorted(required_check - set(check))
        if absent:
            fail(f"browser check {check.get('id')} is missing fields: {', '.join(absent)}")


def performance_request_urls(entries: list[dict[str, Any]]) -> list[str]:
    urls: list[str] = []
    for entry in entries:
        raw = entry.get("message")
        if not isinstance(raw, str):
            continue
        try:
            envelope = json.loads(raw)
        except json.JSONDecodeError:
            continue
        message = envelope.get("message")
        if not isinstance(message, dict) or message.get("method") != "Network.requestWillBeSent":
            continue
        params = message.get("params")
        request = params.get("request") if isinstance(params, dict) else None
        url = request.get("url") if isinstance(request, dict) else None
        if isinstance(url, str):
            urls.append(url)
    return urls


def external_http_requests(urls: list[str], port: int) -> list[str]:
    external: list[str] = []
    for url in urls:
        parsed = urlsplit(url)
        if parsed.scheme not in {"http", "https"}:
            continue
        if parsed.hostname in {"127.0.0.1", "localhost"} and parsed.port == port:
            continue
        external.append(url)
    return sorted(set(external))


def csp_log_violations(entries: list[dict[str, Any]]) -> list[str]:
    violations: list[str] = []
    for entry in entries:
        message = str(entry.get("message", ""))
        folded = message.casefold()
        if "content security policy" in folded or "violates the following content security policy" in folded:
            violations.append(message)
    return violations


def analyze_through_ui(browser: Browser, pdf: Path, profile: str, document_type: str = 'undergraduate-capstone', print_mode: str = 'single-sided') -> dict[str, Any]:
    browser.execute(
        "window.alert=(message)=>{window.__ufcTestAlert=String(message)};"
        "const p=document.querySelector('#profile');p.value=arguments[0];"
        "const d=document.querySelector('#document-type');d.value=arguments[1];"
        "const m=document.querySelector('#print-mode');m.value=arguments[2];"
        "document.querySelector('#summary').classList.add('hidden');"
        "document.querySelector('#pdf-file').value='';return p.value;",
        [profile, document_type, print_mode],
    )
    browser.send_file("#pdf-file", pdf)
    browser.click("#analyze")

    def complete() -> bool:
        return bool(
            browser.execute(
                "const s=document.querySelector('#summary'),b=document.querySelector('#analyze'),"
                "f=document.querySelector('#file-name');"
                "return Boolean(s&&!s.classList.contains('hidden')&&b&&!b.disabled&&"
                "f&&f.textContent===arguments[0]);",
                [pdf.name],
            )
        )

    wait_for(complete, f"productive UI report for {pdf.name}")
    report = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(m=>done(m.getLastReport()))"
        ".catch(e=>done({__import_error__:String(e)}));"
    )
    if not isinstance(report, dict):
        fail(f"productive report is not an object for {pdf.name}: {report!r}")
    if report.get("__import_error__"):
        fail(f"cannot read productive app module report: {report['__import_error__']}")
    actual_verdict = browser.execute("return document.querySelector('#verdict')?.textContent||'';")
    if actual_verdict != PT_VERDICT.get(report["verdict"], report["verdict"]):
        fail(f"visible pt-BR verdict mismatches canonical report: {actual_verdict!r}")
    if report.get("file") != pdf.name:
        fail(f"productive report file mismatch: {report.get('file')!r} != {pdf.name!r}")
    return report


PT_STATUS = {
    "PASS": "Aprovado",
    "FAIL": "Falha",
    "WARNING": "Aviso",
    "MANUAL REVIEW": "Revisão manual",
    "NOT APPLICABLE": "Não aplicável",
}
PT_VERDICT = {
    "FAIL": "Falha",
    "REVIEW REQUIRED": "Revisão obrigatória",
    "AUTOMATED CHECKS PASSED WITH WARNINGS": "Verificações automáticas aprovadas com ressalvas",
    "AUTOMATED CHECKS PASSED": "Verificações automáticas aprovadas",
}


def verify_portuguese_ui(browser: Browser) -> None:
    """Assert real browser copy, semantics and unchanged public select values."""
    observed = browser.execute(
        "const pick=id=>document.querySelector('#'+id);"
        "const options=id=>[...pick(id).options].map(o=>({value:o.value,label:o.textContent}));"
        "const label=id=>pick(id).closest('label')?.textContent||'';"
        "return {lang:document.documentElement.lang,"
        "heading:document.querySelector('header h1')?.textContent||'',"
        "lead:document.querySelector('header .lead')?.textContent||'',"
        "button:pick('analyze').textContent,"
        "profile:options('profile'),types:options('document-type'),"
        "print:options('print-mode'),filter:options('report-filter'),"
        "fileLabel:label('pdf-file'),profileLabel:label('profile'),"
        "docLabel:label('document-type'),printLabel:label('print-mode'),"
        "filterLabel:document.querySelector('label[for=report-filter]')?.textContent||'',"
        "exportJSON:pick('export-json').textContent,printReport:pick('print-report').textContent};"
    )
    if observed.get("lang") != "pt-BR":
        fail(f"Web/Lite html language must be pt-BR: {observed!r}")
    for field, marker in {
        "heading": "Validador de PDF UFC/ABNT",
        "lead": "o arquivo não é enviado a um servidor",
        "button": "Validar PDF",
        "fileLabel": "PDF",
        "profileLabel": "Modo de validação",
        "docLabel": "Tipo de documento",
        "printLabel": "Modo de impressão",
        "filterLabel": "Exibir verificações",
        "exportJSON": "Exportar JSON",
        "printReport": "Imprimir relatório",
    }.items():
        if marker not in observed.get(field, ""):
            fail(f"Web/Lite pt-BR missing {field}={marker!r}: {observed!r}")
    types = observed.get("types", [])
    expected_types = [
        "undergraduate-capstone",
        "specialization-capstone",
        "masters-thesis",
        "doctoral-thesis",
        "research-project",
        "anonymized-research-project",
        "scientific-article",
    ]
    if [x["value"] for x in types] != expected_types or any(not x["label"] for x in types):
        fail(f"Web/Lite changed public document types: {types!r}")
    if [x["value"] for x in observed["profile"]] != ["strict", "portable", "accessibility"]:
        fail("Web/Lite changed public validation-mode values")
    if [x["value"] for x in observed["print"]] != ["single-sided", "double-sided"]:
        fail("Web/Lite changed public print-mode values")
    filters = observed.get("filter", [])
    if [x["value"] for x in filters] != ["all", "attention", "failures", "manual"]:
        fail(f"Web/Lite changed canonical result filter values: {filters!r}")
    if any(not x["label"] for x in filters) or "revisão" not in filters[-1]["label"].lower():
        fail("Web/Lite report filter has inaccessible or untranslated labels")


def verify_report_filters(browser: Browser, report: dict[str, Any]) -> dict[str, int]:
    """Exercise all filters on the productive UI; canonical report stays whole."""
    original = report["checks"]
    modes = {
        "all": lambda c: True,
        "attention": lambda c: c["status"] in {"FAIL", "WARNING", "MANUAL REVIEW"},
        "failures": lambda c: c["status"] == "FAIL",
        "manual": lambda c: c["status"] == "MANUAL REVIEW",
    }
    evidence: dict[str, int] = {}
    for mode, predicate in modes.items():
        observed = browser.execute(
            "const select=document.querySelector('#report-filter');"
            "if(!select||select.disabled)return {error:'filter unavailable'};"
            "select.value=arguments[0];"
            "select.dispatchEvent(new Event('change',{bubbles:true}));"
            "const rows=[...document.querySelectorAll('#report-body tr')];"
            "return {mode:select.value,total:rows.length,"
            "visible:rows.filter(row=>!row.hidden).length,"
            "statuses:rows.filter(row=>!row.hidden)"
            ".map(row=>row.querySelector('td')?.textContent||''),"
            "label:document.querySelector('#filter-count')?.textContent||''};",
            [mode],
        )
        if not isinstance(observed, dict) or observed.get("error"):
            fail(f"report filter not available: {observed!r}")
        expected_statuses = [PT_STATUS[c["status"]] for c in original if predicate(c)]
        expected_count = len(expected_statuses)
        if (
            observed.get("mode") != mode
            or observed.get("total") != len(original)
            or observed.get("visible") != expected_count
            or observed.get("statuses") != expected_statuses
            or observed.get("label") != f"Exibindo {expected_count} de {len(original)} verificações"
        ):
            fail(f"productive UI {mode} filter diverged from canonical report: {observed!r}")
        evidence[mode] = expected_count

    canonical = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(mod=>done(mod.getLastReport()))"
        ".catch(e=>done({__import_error__:String(e)}));"
    )
    if not isinstance(canonical, dict) or canonical.get("checks") != original:
        fail("filtering modified the canonical full report or exported evidence")
    return evidence




def verify_csv_export(browser: Browser, report: dict[str, Any]) -> dict[str, Any]:
    """Exercise the production download button with a real PDF metadata formula."""
    vectors = [
        ["=1+2", "\"'=1+2\""],
        ["+SUM(1,2)", "\"'+SUM(1,2)\""],
        ["-1+2", "\"'-1+2\""],
        ["@SUM(1,2)", "\"'@SUM(1,2)\""],
        [" \t=1+2", "\"' \t=1+2\""],
        ["\r\n=1+2", "\"'\r\n=1+2\""],
        ["simple,comma", "\"simple,comma\""],
        ['with "quotes"', '"with ""quotes"""'],
        ["normal evidence", "\"normal evidence\""],
        [None, "\"\""],
    ]
    check = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./csv-export.js').then(m=>done("
        "arguments[0].map(pair=>({actual:m.csvCell(pair[0]),expected:pair[1]}))"
        ")).catch(e=>done({error:String(e)}));",
        [vectors],
    )
    if not isinstance(check, list) or any(row["actual"] != row["expected"] for row in check):
        fail(f"spreadsheet formula/escaping vectors diverged: {check!r}")
    actual_csv = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "const previous=URL.createObjectURL;let captured=null;"
        "try{URL.createObjectURL=blob=>{captured=blob;return previous(blob)};"
        "document.querySelector('#export-csv').click();"
        "}catch(e){URL.createObjectURL=previous;done({error:String(e)});return;}"
        "URL.createObjectURL=previous;"
        "if(!captured){done({error:'productive CSV download missing'});return;}"
        "Promise.all([captured.text(),captured.arrayBuffer()])"
        ".then(([text,bytes])=>done({text,type:captured.type,"
        "bom:[...new Uint8Array(bytes).slice(0,3)]}))"
        ".catch(e=>done({error:String(e)}));"
    )
    if not isinstance(actual_csv, dict) or actual_csv.get("error"):
        fail(f"CSV download was not created: {actual_csv!r}")
    payload = actual_csv.get("text")
    if not isinstance(payload, str) or actual_csv.get("bom") != [239, 187, 191] or "text/csv" not in actual_csv.get("type", ""):
        fail("CSV download missing expected UTF-8 BOM or MIME type")
    rows = list(csv.reader(io.StringIO(payload.lstrip("\ufeff"))))
    names = ["Status", "Category", "Rule", "Source", "Evidence", "Correction",
             "Level", "Mandatory", "Normative rule", "Locator", "Normativity"]
    if not rows or rows[0] != names or len(rows) != len(report["checks"]) + 1:
        fail("CSV export does not include the canonical header and all checks")
    fields = ["status", "category", "rule", "source", "evidence", "correction",
              "level", "mandatory", "normative_rule", "locator", "normativity"]
    formula = re.compile(r"^[\s\x00-\x1f\x7f]*[=+@-]")
    formula_cells = 0
    for row, check_entry in zip(rows[1:], report["checks"], strict=True):
        canonical = [check_entry[field] for field in fields]
        canonical[7] = "yes" if canonical[7] else "no"
        expected = []
        for raw in canonical:
            text = str(raw if raw is not None else "")
            if formula.match(text):
                formula_cells += 1
                text = "'" + text
            expected.append(text)
        if row != expected:
            fail(f"CSV export changes report row or misses a formula guard: {row!r} != {expected!r}")
    metadata = by_id(report).get("meta.title")
    if metadata is None or metadata.get("evidence") != "=1+2" or formula_cells < 1:
        fail(f"real negative PDF formula metadata not exercised: {metadata!r}")
    canonical_after = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(m=>done(m.getLastReport())).catch(e=>done({error:String(e)}));"
    )
    if not isinstance(canonical_after, dict) or canonical_after.get("checks") != report["checks"]:
        fail("CSV export mutated the canonical machine report")
    print(
        "CSV-EXPORT-EVIDENCE surface=web-lite status=PASS "
        f"real_pdf_formula=NEUTRALIZED attack_vectors={len(vectors)} "
        f"exported_checks={len(report['checks'])} formula_cells={formula_cells} "
        "canonical_report=UNCHANGED no_network_dependency=true"
    )
    return {"status": "PASS", "attack_vectors": len(vectors),
            "exported_checks": len(report["checks"]), "formula_cells": formula_cells,
            "canonical_report_unchanged": True}


def verify_ui_locales(browser: Browser, positive: Path, negative: Path, profile: str, canonical_positive: dict[str, Any], canonical_negative: dict[str, Any]) -> dict[str, Any]:
    """Verify four locales with real PDFs and strict canonical-result invariance."""
    outcomes: dict[str, Any] = {}
    expected = {
        "pt-BR": ("Validador de PDF UFC/ABNT", "Validar PDF", "Exibindo", "o arquivo não é enviado a um servidor", "PDF é processado apenas neste dispositivo", "Idioma da interface", "Falha"),
        "en": ("UFC/ABNT PDF Validator", "Validate PDF", "Showing", "not uploaded to a server", "PDF is processed only on this device", "Interface language", "Failed"),
        "es": ("Validador de PDF UFC/ABNT", "Validar PDF", "Mostrando", "no se envía a ningún servidor", "PDF se procesa únicamente en este dispositivo", "Idioma de la interfaz", "Fallo"),
        "fr": ("Validateur de PDF UFC/ABNT", "Valider le PDF", "Affichage", "n’est pas envoyé à un serveur", "PDF est traité uniquement sur cet appareil", "Langue de l’interface", "Échec"),
    }
    canonical_keys = lambda report: {key: value for key, value in report.items() if key != "generated_at"}
    for locale, (heading, button, counter, lead_privacy, device_privacy, accessible_name, fail_label) in expected.items():
        observed = browser.execute(
            "const control=document.querySelector('#ui-locale');"
            "control.value=arguments[0];control.dispatchEvent(new Event('change',{bubbles:true}));"
            "return {locale:document.documentElement.lang,selected:control.value,"
            "heading:document.querySelector('header h1').textContent,"
            "button:document.querySelector('#analyze').textContent,"
            "privacy:document.querySelector('section.controls p.note').textContent,"
            "lead:document.querySelector('header .lead').textContent,"
            "label:control.labels?.[0]?.querySelector('span')?.textContent||'',"
            "associatedLabels:control.labels?.length??0,hasAriaOverride:control.hasAttribute('aria-label'),"
            "types:[...document.querySelector('#document-type').options].map(o=>o.value),"
            "filters:[...document.querySelector('#report-filter').options].map(o=>o.value)};",
            [locale],
        )
        if observed["locale"] != locale or observed["selected"] != locale:
            fail(f"locale DOM selection mismatch: {observed!r}")
        if observed["heading"] != heading or observed["button"] != button:
            fail(f"locale {locale} headline or button copy incomplete: {observed!r}")
        if lead_privacy not in observed["lead"] or device_privacy not in observed["privacy"]:
            fail(f"locale {locale} local-only privacy disclosures are incomplete: {observed!r}")
        if observed["label"] != accessible_name or observed["associatedLabels"] != 1 or observed["hasAriaOverride"]:
            fail(f"locale {locale} accessible selector name did not follow the selected language: {observed!r}")
        if len(observed["types"]) != 7 or observed["filters"] != ["all", "attention", "failures", "manual"]:
            fail(f"locale {locale} changed canonical form options")
        positive_report = analyze_through_ui_locale(browser, positive, profile)
        if canonical_keys(positive_report) != canonical_keys(canonical_positive):
            fail(f"locale {locale} changed canonical positive PDF report")
        count = browser.execute("return document.querySelector('#filter-count').textContent;")
        if not count.startswith(counter):
            fail(f"locale {locale} did not translate dynamic counter: {count!r}")
        negative_report = analyze_through_ui_locale(browser, negative, profile)
        if canonical_keys(negative_report) != canonical_keys(canonical_negative):
            fail(f"locale {locale} changed canonical negative PDF report")
        if negative_report["verdict"] != FAIL:
            fail(f"locale {locale} lost negative PDF failure")
        visual_failure = browser.execute(
            "const first=[...document.querySelectorAll('#report-body tr')]"
            ".find(row=>row.querySelector('td')?.classList.contains('status-fail'));"
            "return {verdict:document.querySelector('#verdict')?.textContent||'',"
            "row:first?.querySelector('td')?.textContent||''};"
        )
        if visual_failure != {"verdict": fail_label, "row": fail_label}:
            fail(f"locale {locale} failure presentation differs from machine status: {visual_failure!r}")
        outcomes[locale] = {"positive": positive_report["verdict"], "negative": negative_report["verdict"], "canonical_equal": True}
    invalid = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(m=>{try{m.setLocale('xx-INVALID');done('ACCEPTED')}catch(e){done(e.name)}}).catch(e=>done(String(e)));"
    )
    if invalid != "RangeError":
        fail(f"unsupported Web/Lite locale was not rejected: {invalid!r}")
    coverage = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(m=>done(m.assertLocaleCoverage())).catch(e=>done(String(e)));"
    )
    if coverage is not True:
        fail(f"Web/Lite locale dictionary incomplete: {coverage!r}")
    browser.execute("const x=document.querySelector('#ui-locale');x.value='pt-BR';x.dispatchEvent(new Event('change',{bubbles:true}));")
    return outcomes


def analyze_through_ui_locale(browser: Browser, pdf: Path, profile: str) -> dict[str, Any]:
    """Read the productive analysis path without imposing the Portuguese display assertion."""
    browser.execute(
        "const p=document.querySelector('#profile');p.value=arguments[0];"
        "document.querySelector('#document-type').value='undergraduate-capstone';"
        "document.querySelector('#print-mode').value='single-sided';"
        "document.querySelector('#summary').classList.add('hidden');"
        "document.querySelector('#pdf-file').value='';",
        [profile],
    )
    browser.send_file("#pdf-file", pdf)
    browser.click("#analyze")
    wait_for(
        lambda: bool(browser.execute(
            "const s=document.querySelector('#summary'),b=document.querySelector('#analyze'),f=document.querySelector('#file-name');"
            "return Boolean(s&&!s.classList.contains('hidden')&&b&&!b.disabled&&f&&f.textContent===arguments[0]);",
            [pdf.name],
        )),
        f"localized UI report for {pdf.name}",
    )
    report = browser.execute_async(
        "const done=arguments[arguments.length-1];"
        "import('./app.js').then(m=>done(m.getLastReport())).catch(e=>done({error:String(e)}));"
    )
    if not isinstance(report, dict) or report.get("error"):
        fail(f"localized report unavailable: {report!r}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real PDFs through the productive Web/Lite browser UI.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--profile", choices=("strict", "portable", "accessibility"), default="portable")
    parser.add_argument("--site-root", type=Path, default=VALIDATOR)
    parser.add_argument("--document-pdf-dir", type=Path, help="Five real class-rendered profile PDFs and matching CLI evidence")
    parser.add_argument("--duplex-pdf-dir", type=Path, help="Two real recto/verso PDFs and matching CLI evidence")
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()

    positive = args.pdf.resolve()
    if not positive.is_file() or positive.stat().st_size == 0:
        fail(f"positive PDF is missing or empty: {positive}")

    site_root = args.site_root.resolve()
    if not (site_root / "index.html").is_file() or not (site_root / "app.js").is_file():
        fail(f"Web/Lite site root is incomplete: {site_root}")
    try:
        site_root_label = str(site_root.relative_to(ROOT))
    except ValueError:
        site_root_label = str(site_root)

    chrome = (
        shutil.which("google-chrome")
        or shutil.which("chromium")
        or shutil.which("chromium-browser")
    )
    driver = shutil.which("chromedriver")
    if not chrome:
        fail("Chrome/Chromium executable not found")
    if not driver:
        fail("chromedriver executable not found")

    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    catalog = json.loads(CATALOG.read_text(encoding="utf-8"))

    handler = partial(QuietHandler, directory=str(site_root))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    deny_proxy = ThreadingHTTPServer(("127.0.0.1", 0), DenyProxyHandler)
    deny_proxy.denied_requests = []
    proxy_thread = Thread(target=deny_proxy.serve_forever, daemon=True)
    proxy_thread.start()

    evidence_path = args.evidence.resolve() if args.evidence else None
    driver_log = (
        evidence_path.with_name("web-lite-chromedriver.log")
        if evidence_path
        else Path(tempfile.gettempdir()) / "abntexto-ufc-web-lite-chromedriver.log"
    )
    browser = Browser(chrome, driver, driver_log, deny_proxy.server_port)
    try:
        browser.start()
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        wait_for(
            lambda: bool(browser.execute("return document.querySelector('#norm-reviewed')?.textContent||'';")),
            "Web/Lite module graph and normative base",
            timeout=70,
        )
        csp_policy = browser.execute(
            "return document.querySelector('meta[http-equiv=\"Content-Security-Policy\"]')?.content||'';"
        )
        if csp_policy != CSP_POLICY:
            fail(f"productive Web/Lite CSP mismatch: {csp_policy!r}")

        verify_portuguese_ui(browser)

        with tempfile.TemporaryDirectory(prefix="abntexto-ufc-web-lite-") as temp:
            negative = Path(temp) / "web-lite-negative-letter.pdf"
            write_negative_pdf(negative)

            positive_sha256 = file_sha256(positive)
            negative_sha256 = file_sha256(negative)

            positive_report = analyze_through_ui(browser, positive, args.profile)
            validate_schema(positive_report, args.profile, contract, catalog)
            positive_checks = by_id(positive_report)
            positive_filter_counts = verify_report_filters(browser, positive_report)
            for check_id in ("pdf.open", "layout.a4", "layout.margins"):
                if positive_checks.get(check_id, {}).get("status") != PASS:
                    fail(f"positive PDF {check_id} is not PASS: {positive_checks.get(check_id)}")
            if positive_report.get("verdict") == FAIL:
                fail("positive canonical/reference PDF received FAIL in Web/Lite")
            for check_id in ("font.embedded", "pdfa.deep"):
                check = positive_checks.get(check_id)
                if not check or check.get("status") != REVIEW or check.get("mandatory") is not False:
                    fail(f"positive Web/Lite deep boundary drift for {check_id}: {check}")

            negative_report = analyze_through_ui(browser, negative, args.profile)
            validate_schema(negative_report, args.profile, contract, catalog)
            if browser.execute("return document.querySelector('#report-filter').value;") != "all":
                fail("new PDF analysis did not reset filter to all (may hide real failures)")
            negative_filter_counts = verify_report_filters(browser, negative_report)
            negative_checks = by_id(negative_report)
            csv_evidence = verify_csv_export(browser, negative_report)
            if negative_checks.get("pdf.open", {}).get("status") != PASS:
                fail("negative fixture is not a readable PDF")
            if negative_checks.get("layout.a4", {}).get("status") != FAIL:
                fail(f"negative non-A4 fixture did not fail layout.a4: {negative_checks.get('layout.a4')}")
            if negative_report.get("verdict") != FAIL:
                fail(f"negative non-A4 fixture verdict is not FAIL: {negative_report.get('verdict')}")
            for check_id in ("font.embedded", "pdfa.deep"):
                check = negative_checks.get(check_id)
                if not check or check.get("status") != REVIEW or check.get("mandatory") is not False:
                    fail(f"negative Web/Lite deep boundary drift for {check_id}: {check}")

            profile_reports: dict[str, Any] = {}
            if args.document_pdf_dir:
                directory = args.document_pdf_dir.resolve()
                cli_evidence_file = directory / "cli-evidence.json"
                if not cli_evidence_file.is_file():
                    fail("real-PDF CLI evidence missing: " + str(cli_evidence_file))
                cli_evidence = json.loads(cli_evidence_file.read_text(encoding="utf-8"))
                if cli_evidence.get("status") != PASS or len(cli_evidence.get("pdfs", {})) != 5:
                    fail("real-PDF CLI evidence is incomplete")
                for scenario, expected in cli_evidence["pdfs"].items():
                    pdf = directory / (scenario + ".pdf")
                    if not pdf.is_file() or file_sha256(pdf) != expected["pdf_sha256"]:
                        fail("real-PDF identity mismatch: " + scenario)
                    result = analyze_through_ui(
                        browser, pdf, args.profile, expected["document_type"]
                    )
                    validate_schema(
                        result, args.profile, contract, catalog, expected["document_type"]
                    )
                    if result.get("file") != pdf.name:
                        fail("wrong real-PDF browser report: " + scenario)
                    checks = by_id(result)
                    if checks.get("pdf.open", {}).get("status") != PASS:
                        fail("browser did not open real PDF: " + scenario)
                    for check_id, expected_status in expected["expected_checks"].items():
                        status = checks.get(check_id, {}).get("status")
                        if status != expected_status:
                            fail(
                                "real-PDF cross-surface drift: "
                                f"{scenario}/{check_id}: browser {status!r}, "
                                f"CLI {expected_status!r}"
                            )
                    if expected["negative_control"]:
                        if result.get("verdict") != FAIL:
                            fail("real negative PDF did not fail: " + scenario)
                    elif result.get("verdict") == FAIL:
                        fail("real positive PDF failed: " + scenario)
                    profile_reports[scenario] = {
                        "document_type": expected["document_type"],
                        "sha256": expected["pdf_sha256"],
                        "verdict": result["verdict"],
                        "checks": {
                            key: checks[key]["status"]
                            for key in expected["expected_checks"]
                        },
                        "negative_control": expected["negative_control"],
                    }
                print(
                    "DOCUMENT-TYPE-PDF-EVIDENCE surface=web-lite status=PASS "
                    "real_pdfs=5 positive=3 negative=2 "
                    "cross_surface_checks=ALIGNED proof_state=automatic-partial"
                )

            duplex_reports: dict[str, Any] = {}
            if args.duplex_pdf_dir:
                directory = args.duplex_pdf_dir.resolve()
                evidence_file = directory / "cli-evidence.json"
                if not evidence_file.is_file():
                    fail("duplex CLI evidence is missing")
                control = json.loads(evidence_file.read_text(encoding="utf-8"))
                if control.get("status") != PASS or len(control.get("scenarios", {})) != 4:
                    fail("duplex CLI evidence scenarios are incomplete")
                for scenario, spec in control["scenarios"].items():
                    pdf = directory / spec["pdf_file"]
                    if not pdf.is_file() or file_sha256(pdf) != spec["pdf_sha256"]:
                        fail("duplex real PDF identity mismatch: " + scenario)
                    report = analyze_through_ui(
                        browser, pdf, args.profile, "doctoral-thesis", spec["print_mode"]
                    )
                    validate_schema(
                        report, args.profile, contract, catalog, "doctoral-thesis", spec["print_mode"]
                    )
                    checks = by_id(report)
                    if checks.get("pdf.open", {}).get("status") != PASS:
                        fail("duplex PDF is not readable: " + scenario)
                    actual = checks.get("layout.margins", {}).get("status")
                    if actual != spec["margins"]:
                        fail(
                            "duplex cross-surface mismatch: "
                            f"{scenario}: Web/Lite={actual!r}, CLI/Deep={spec['margins']!r}"
                        )
                    if checks.get("layout.a4", {}).get("status") != PASS:
                        fail("duplex PDF is not A4: " + scenario)
                    duplex_reports[scenario] = {
                        "print_mode": spec["print_mode"],
                        "pdf_sha256": spec["pdf_sha256"],
                        "layout_margins": actual,
                        "negative_control": spec["negative_control"],
                    }
                print(
                    "DUPLEX-MARGIN-PDF-EVIDENCE surface=web-lite status=PASS "
                    "actual_pdfs=2 scenarios=4 positive=2 negative=2 "
                    "cross_surface_margins=ALIGNED"
                )

            locale_evidence = verify_ui_locales(browser, positive, negative, args.profile, positive_report, negative_report)

            performance_entries = browser.logs("performance")
            requested_urls = performance_request_urls(performance_entries)
            external_urls = external_http_requests(requested_urls, server.server_port)
            if external_urls:
                fail("productive Web/Lite attempted external HTTP(S): " + ", ".join(external_urls))

            browser_entries = browser.logs("browser")
            csp_violations = csp_log_violations(browser_entries)
            if csp_violations:
                fail("productive Web/Lite emitted CSP violations: " + " | ".join(csp_violations[:5]))

            observed_http_requests = [
                url for url in requested_urls if urlsplit(url).scheme in {"http", "https"}
            ]
            denied_proxy_requests = list(getattr(deny_proxy, "denied_requests", []))

            chrome_version = subprocess.run(
                [chrome, "--version"], text=True, capture_output=True, check=False
            ).stdout.strip()
            driver_version = subprocess.run(
                [driver, "--version"], text=True, capture_output=True, check=False
            ).stdout.strip()
            evidence = {
                "status": "PASS",
                "surface": "web-lite",
                "ui": "validator/index.html",
                "analysis_path": "productive UI -> exported analyze/getLastReport",
                "profile": args.profile,
                "site_root": site_root_label,
                "local_processing": True,
                "ui_locale": "pt-BR",
                "ui_locales": locale_evidence,
                "canonical_machine_values_preserved": True,
                "normative_catalog": positive_report["normative_catalog"],
                "network": {
                    "external_network_denied": True,
                    "proxy_mode": "deny",
                    "dns_external_denied": True,
                    "observed_http_requests": len(observed_http_requests),
                    "observed_external_http_requests": 0,
                    "deny_proxy_requests": len(denied_proxy_requests),
                    "csp": csp_policy,
                    "csp_violations": 0,
                },
                "browser": chrome_version,
                "driver": driver_version,
                "driver_log": str(driver_log),
                "positive": {
                    "file": positive_report["file"],
                    "sha256": positive_sha256,
                    "bytes": positive.stat().st_size,
                    "pages": positive_report["pages"],
                    "verdict": positive_report["verdict"],
                    "pdf_open": positive_checks["pdf.open"]["status"],
                    "layout_a4": positive_checks["layout.a4"]["status"],
                    "layout_margins": positive_checks["layout.margins"]["status"],
                    "font_embedded": positive_checks["font.embedded"]["status"],
                    "pdfa_deep": positive_checks["pdfa.deep"]["status"],
                },
                "report_filter": {"positive": positive_filter_counts, "negative": negative_filter_counts, "source_report_preserved": True},
                "csv_export": csv_evidence,
                "document_type_pdfs": profile_reports,
                "duplex_margin_pdfs": duplex_reports,
                "negative": {
                    "file": negative_report["file"],
                    "sha256": negative_sha256,
                    "bytes": negative.stat().st_size,
                    "pages": negative_report["pages"],
                    "verdict": negative_report["verdict"],
                    "pdf_open": negative_checks["pdf.open"]["status"],
                    "layout_a4": negative_checks["layout.a4"]["status"],
                    "font_embedded": negative_checks["font.embedded"]["status"],
                    "pdfa_deep": negative_checks["pdfa.deep"]["status"],
                },
            }
            if args.evidence:
                args.evidence.parent.mkdir(parents=True, exist_ok=True)
                args.evidence.write_text(json.dumps(evidence, indent=2) + "\n", encoding="utf-8")

            print(
                "WEB-LITE-E2E-EVIDENCE status=PASS "
                f"profile={args.profile} positive_pages={positive_report['pages']} "
                f"positive_sha256={positive_sha256} negative_sha256={negative_sha256} "
                f"positive_verdict={positive_report['verdict'].replace(' ', '_')} "
                "positive_pdf_open=PASS positive_a4=PASS positive_margins=PASS "
                "negative_pdf_open=PASS negative_a4=FAIL negative_verdict=FAIL "
                "font_embedded=MANUAL_REVIEW pdfa_deep=MANUAL_REVIEW "
                "productive_ui=true local_processing=true pages_package=true "
                "external_network=DENIED external_http_requests=0 csp=PASS "
                "report_filter=PASS csv_export=PASS full_report_unchanged=true ui_locale=pt-BR locales=4"
            )
    finally:
        browser.stop()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)
        deny_proxy.shutdown()
        deny_proxy.server_close()
        proxy_thread.join(timeout=5)


if __name__ == "__main__":
    main()
