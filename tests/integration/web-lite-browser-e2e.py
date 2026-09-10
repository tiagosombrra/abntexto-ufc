#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html
import json
import re
import shutil
import subprocess
import sys
import tempfile
import threading
from functools import partial
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
SITE_BUILDER = ROOT / "tools" / "build-validator-site.py"
CONTRACT = ROOT / "validator" / "validation-contract.json"
CATALOG = ROOT / "standards" / "catalog.json"
RESULT_ID = "web-lite-e2e-result"


def fail(message: str) -> None:
    raise SystemExit(f"Web/Lite browser E2E failed: {message}")


def load_json(path: Path) -> dict[str, Any]:
    try:
        value = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {path.relative_to(ROOT)}: {exc}")
    if not isinstance(value, dict):
        fail(f"{path.relative_to(ROOT)} must contain an object")
    return value


def minimal_negative_pdf() -> bytes:
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 420 595] /Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        b"<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
    ]
    stream = b"BT /F1 18 Tf 60 500 Td (NEGATIVE WEB LITE FIXTURE) Tj ET\n"
    objects.append(
        b"<< /Length " + str(len(stream)).encode("ascii") + b" >>\nstream\n" + stream + b"endstream"
    )

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
    return bytes(data)


def chrome_binary(explicit: str | None) -> str:
    candidates = [explicit] if explicit else []
    candidates.extend(
        [
            "google-chrome",
            "google-chrome-stable",
            "chromium",
            "chromium-browser",
        ]
    )
    for candidate in candidates:
        if candidate and shutil.which(candidate):
            return shutil.which(candidate) or candidate
    fail("Chrome/Chromium is required for the real browser E2E")
    raise AssertionError("unreachable")


def build_site(output: Path) -> None:
    completed = subprocess.run(
        [sys.executable, str(SITE_BUILDER), "--output", str(output)],
        cwd=ROOT,
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    )
    if completed.stdout:
        print(completed.stdout.rstrip())
    if completed.returncode != 0:
        fail("deterministic static-site build failed")


def write_harness(site: Path, positive_names: list[str]) -> None:
    cases = [{"name": name, "url": f"/{name}", "profile": "portable"} for name in positive_names]
    cases.append({"name": "negative-a5.pdf", "url": "/negative-a5.pdf", "profile": "portable"})
    source = f"""<!doctype html>
<meta charset=\"utf-8\">
<title>Web Lite E2E harness</title>
<iframe id=\"app\" src=\"/index.html\"></iframe>
<pre id=\"{RESULT_ID}\"></pre>
<script>
const cases={json.dumps(cases)};
const result=document.getElementById({json.dumps(RESULT_ID)});
const frame=document.getElementById("app");
const sleep=ms=>new Promise(resolve=>setTimeout(resolve,ms));
async function api(){{
  for(let i=0;i<600;i++){{
    const value=frame.contentWindow?.__ABNTEXTO_UFC_WEB_LITE__;
    if(value?.analyze)return value;
    await sleep(100);
  }}
  throw new Error("production analyze API was not exposed after index.html load");
}}
async function pdfFile(item){{
  const response=await fetch(item.url,{{cache:"no-store"}});
  if(!response.ok)throw new Error(`failed to fetch ${{item.url}}: ${{response.status}}`);
  const blob=await response.blob();
  return new File([blob],item.name,{{type:"application/pdf"}});
}}
(async()=>{{
  try{{
    const production=await api();
    const reports=[];
    for(const item of cases){{
      reports.push(await production.analyze(await pdfFile(item),item.profile));
    }}
    result.textContent=JSON.stringify({{ok:true,reports}});
    document.body.dataset.e2e="done";
  }}catch(error){{
    result.textContent=JSON.stringify({{ok:false,error:String(error?.stack||error)}});
    document.body.dataset.e2e="error";
  }}
}})();
</script>
"""
    (site / "e2e.html").write_text(source, encoding="utf-8")


class QuietHandler(SimpleHTTPRequestHandler):
    def log_message(self, format: str, *args: object) -> None:
        return


def browser_reports(site: Path, chrome: str) -> list[dict[str, Any]]:
    handler = partial(QuietHandler, directory=str(site))
    server = ThreadingHTTPServer(("127.0.0.1", 0), handler)
    thread = threading.Thread(target=server.serve_forever, daemon=True)
    thread.start()
    try:
        url = f"http://127.0.0.1:{server.server_port}/e2e.html"
        completed = subprocess.run(
            [
                chrome,
                "--headless=new",
                "--no-sandbox",
                "--disable-gpu",
                "--disable-dev-shm-usage",
                "--disable-background-networking",
                "--disable-default-apps",
                "--disable-extensions",
                "--no-first-run",
                "--virtual-time-budget=120000",
                "--dump-dom",
                url,
            ],
            cwd=ROOT,
            text=True,
            encoding="utf-8",
            errors="replace",
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
            timeout=180,
        )
    finally:
        server.shutdown()
        server.server_close()
        thread.join(timeout=5)

    if completed.returncode != 0:
        fail(f"headless browser exited {completed.returncode}: {completed.stderr[-3000:]}")
    match = re.search(
        rf'<pre id="{re.escape(RESULT_ID)}">(.*?)</pre>',
        completed.stdout,
        re.DOTALL,
    )
    if not match:
        fail(f"browser DOM did not contain {RESULT_ID}; stderr={completed.stderr[-2000:]}")
    raw = html.unescape(match.group(1)).strip()
    if not raw:
        fail("browser harness produced an empty result")
    try:
        payload = json.loads(raw)
    except json.JSONDecodeError as exc:
        fail(f"browser harness result is not JSON: {exc}: {raw[:1000]}")
    if not payload.get("ok"):
        fail(f"browser harness reported an error: {payload.get('error')}")
    reports = payload.get("reports")
    if not isinstance(reports, list) or not reports:
        fail("browser harness did not return reports")
    return reports


def assert_schema(report: dict[str, Any], contract: dict[str, Any]) -> None:
    target = contract.get("target_report_schema")
    if not isinstance(target, dict):
        fail("validation contract target_report_schema is missing")
    required_top = target.get("required_top_level")
    required_fields = target.get("required_check_fields")
    if not isinstance(required_top, list) or not isinstance(required_fields, list):
        fail("validation contract schema fields are invalid")
    missing_top = [field for field in required_top if field not in report]
    if missing_top:
        fail(f"Web/Lite report is missing top-level fields: {missing_top}")
    checks = report.get("checks")
    if not isinstance(checks, list) or not checks:
        fail("Web/Lite report checks are missing")
    for check in checks:
        if not isinstance(check, dict) or list(check) != required_fields:
            fail(f"Web/Lite check schema drift: {list(check) if isinstance(check, dict) else type(check)}")


def assert_check_inventory(report: dict[str, Any], contract: dict[str, Any]) -> None:
    inventory = contract.get("check_inventory")
    if not isinstance(inventory, list):
        fail("validation contract check inventory is missing")
    expected_ids = {
        str(item["canonical_id"])
        for item in inventory
        if isinstance(item, dict) and item.get("web_id") is not None
    }
    checks = report["checks"]
    observed_ids = {str(check.get("id")) for check in checks}
    if observed_ids != expected_ids:
        fail(
            "Web/Lite emitted check IDs differ from contract: "
            f"missing={sorted(expected_ids - observed_ids)} extra={sorted(observed_ids - expected_ids)}"
        )


def assert_normative_metadata(report: dict[str, Any], catalog: dict[str, Any]) -> None:
    rules = {
        str(item["id"]): item
        for item in catalog.get("rules", [])
        if isinstance(item, dict) and isinstance(item.get("id"), str)
    }
    for check in report["checks"]:
        rule_id = check.get("normative_rule")
        if not rule_id:
            continue
        rule = rules.get(str(rule_id))
        if rule is None:
            fail(f"Web/Lite emitted unknown normative rule: {rule_id}")
        if check.get("locator") != rule.get("locator"):
            fail(f"{check.get('id')}: normative locator drift")
        if check.get("normativity") != rule.get("normativity"):
            fail(f"{check.get('id')}: normativity drift")


def by_id(report: dict[str, Any]) -> dict[str, dict[str, Any]]:
    return {str(check["id"]): check for check in report["checks"]}


def assert_positive(report: dict[str, Any]) -> None:
    if report.get("mode") != "web-lite-local" or report.get("profile") != "portable":
        fail("positive report did not use Web/Lite portable mode")
    if not isinstance(report.get("pages"), int) or report["pages"] < 20:
        fail(f"canonical/public reference looks unexpectedly small: pages={report.get('pages')}")
    checks = by_id(report)
    for check_id in (
        "pdf.open",
        "layout.a4",
        "structure.cover",
        "structure.approval",
        "structure.resumo",
        "structure.abstract",
        "structure.toc",
        "structure.refs",
        "structure.keywords",
        "structure.keywords-en",
    ):
        if checks.get(check_id, {}).get("status") != "PASS":
            fail(f"positive reference did not PASS {check_id}: {checks.get(check_id)}")
    mandatory_failures = [
        check["id"]
        for check in report["checks"]
        if check.get("mandatory") and check.get("status") == "FAIL"
    ]
    if mandatory_failures:
        fail(f"positive reference has mandatory Web/Lite failures: {mandatory_failures}")
    for deep_id in ("font.embedded", "pdfa.deep"):
        if checks.get(deep_id, {}).get("status") != "MANUAL REVIEW":
            fail(f"deep-only Web/Lite boundary auto-approved {deep_id}")


def assert_negative(report: dict[str, Any]) -> None:
    checks = by_id(report)
    if report.get("verdict") != "FAIL":
        fail(f"negative PDF verdict must be FAIL, got {report.get('verdict')}")
    if checks.get("layout.a4", {}).get("status") != "FAIL":
        fail("negative A5 fixture did not fail layout.a4")
    if checks.get("structure.resumo", {}).get("status") != "FAIL":
        fail("negative fixture did not fail structure.resumo")


def main() -> None:
    parser = argparse.ArgumentParser(description="Run real PDFs through production Web/Lite analyze() in Chrome.")
    parser.add_argument("--positive", action="append", type=Path, required=True)
    parser.add_argument("--chrome")
    args = parser.parse_args()

    positives = [path.resolve() for path in args.positive]
    for path in positives:
        if not path.is_file() or path.stat().st_size == 0:
            fail(f"positive PDF is missing/empty: {path}")
        if path.read_bytes()[:5] != b"%PDF-":
            fail(f"positive input is not a PDF: {path}")

    contract = load_json(CONTRACT)
    catalog = load_json(CATALOG)
    chrome = chrome_binary(args.chrome)

    with tempfile.TemporaryDirectory(prefix="abntexto-ufc-web-lite-e2e-") as temp:
        site = Path(temp) / "site"
        build_site(site)
        positive_names: list[str] = []
        for index, source in enumerate(positives, 1):
            name = f"positive-{index}.pdf"
            shutil.copyfile(source, site / name)
            positive_names.append(name)
        (site / "negative-a5.pdf").write_bytes(minimal_negative_pdf())
        write_harness(site, positive_names)
        reports = browser_reports(site, chrome)

    if len(reports) != len(positives) + 1:
        fail(f"unexpected browser report count: {len(reports)}")
    for report in reports:
        if not isinstance(report, dict):
            fail("browser report is not an object")
        assert_schema(report, contract)
        assert_check_inventory(report, contract)
        assert_normative_metadata(report, catalog)

    for report in reports[:-1]:
        assert_positive(report)
    assert_negative(reports[-1])

    chrome_version = subprocess.run(
        [chrome, "--version"],
        text=True,
        encoding="utf-8",
        errors="replace",
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        check=False,
    ).stdout.strip().replace(" ", "_")
    pages = ",".join(str(report.get("pages")) for report in reports[:-1])
    print(
        "WEB-LITE-E2E-EVIDENCE status=PASS "
        f"positive_pdfs={len(positives)} positive_pages={pages} negative_pdfs=1 "
        f"negative_layout_a4=FAIL deep_boundaries=REVIEW browser={chrome_version} "
        "production_analyze=true local_http=true upload_api=false"
    )


if __name__ == "__main__":
    main()
