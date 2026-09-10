#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import shutil
import socket
import subprocess
import tempfile
import time
import urllib.error
import urllib.request
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Thread
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
VALIDATOR = ROOT / "validator"
CONTRACT = VALIDATOR / "validation-contract.json"
CATALOG = ROOT / "standards" / "catalog.json"
ELEMENT_KEY = "element-6066-11e4-a52e-4f735466cecf"
PASS = "PASS"
FAIL = "FAIL"
REVIEW = "MANUAL REVIEW"


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


class Browser:
    def __init__(self, chrome: str, chromedriver: str, driver_log: Path) -> None:
        self.chrome = chrome
        self.chromedriver = chromedriver
        self.driver_log = driver_log
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
                        "goog:chromeOptions": {
                            "binary": self.chrome,
                            "args": [
                                "--headless=new",
                                "--no-sandbox",
                                "--disable-dev-shm-usage",
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
            f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\n"
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


def validate_schema(report: dict[str, Any], profile: str, contract: dict[str, Any], catalog: dict[str, Any]) -> None:
    schema = contract["target_report_schema"]
    missing = [key for key in schema["required_top_level"] if key not in report]
    if missing:
        fail("browser report is missing top-level fields: " + ", ".join(missing))
    if report.get("profile") != profile:
        fail(f"browser profile mismatch: {report.get('profile')!r}")
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


def analyze_through_ui(browser: Browser, pdf: Path, profile: str) -> dict[str, Any]:
    browser.execute(
        "window.alert=(message)=>{window.__ufcTestAlert=String(message)};"
        "const p=document.querySelector('#profile');p.value=arguments[0];"
        "document.querySelector('#pdf-file').value='';return p.value;",
        [profile],
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
    if report.get("file") != pdf.name:
        fail(f"productive report file mismatch: {report.get('file')!r} != {pdf.name!r}")
    return report


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real PDFs through the productive Web/Lite browser UI.")
    parser.add_argument("--pdf", type=Path, required=True)
    parser.add_argument("--profile", choices=("strict", "portable", "accessibility"), default="portable")
    parser.add_argument("--evidence", type=Path)
    args = parser.parse_args()

    positive = args.pdf.resolve()
    if not positive.is_file() or positive.stat().st_size == 0:
        fail(f"positive PDF is missing or empty: {positive}")

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

    handler = partial(QuietHandler, directory=str(VALIDATOR))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = Thread(target=server.serve_forever, daemon=True)
    thread.start()

    evidence_path = args.evidence.resolve() if args.evidence else None
    driver_log = (
        evidence_path.with_name("web-lite-chromedriver.log")
        if evidence_path
        else Path(tempfile.gettempdir()) / "abntexto-ufc-web-lite-chromedriver.log"
    )
    browser = Browser(chrome, driver, driver_log)
    try:
        browser.start()
        browser.navigate(f"http://127.0.0.1:{server.server_port}/index.html")
        wait_for(
            lambda: bool(browser.execute("return document.querySelector('#norm-reviewed')?.textContent||'';")),
            "Web/Lite module graph and normative base",
            timeout=70,
        )

        with tempfile.TemporaryDirectory(prefix="abntexto-ufc-web-lite-") as temp:
            negative = Path(temp) / "web-lite-negative-letter.pdf"
            write_negative_pdf(negative)

            positive_sha256 = file_sha256(positive)
            negative_sha256 = file_sha256(negative)

            positive_report = analyze_through_ui(browser, positive, args.profile)
            validate_schema(positive_report, args.profile, contract, catalog)
            positive_checks = by_id(positive_report)
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
            negative_checks = by_id(negative_report)
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
                "local_processing": True,
                "normative_catalog": positive_report["normative_catalog"],
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
                "productive_ui=true local_processing=true"
            )
    finally:
        browser.stop()
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)


if __name__ == "__main__":
    main()
