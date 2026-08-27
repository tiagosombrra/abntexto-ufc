#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
CONTRACT = ROOT / "validator" / "validation-contract.json"
WEB = ROOT / "validator" / "app.js"
INDEX = ROOT / "validator" / "index.html"
CLI = ROOT / "tools" / "validate-ufc-pdf.py"

sys.path.insert(0, str(ROOT / "tools"))
from normative_catalog import load_catalog, rule_map  # noqa: E402

EXPECTED_PROFILES = ["strict", "portable", "accessibility"]
EXPECTED_STATUSES = ["APROVADO", "REPROVADO", "ALERTA", "REVISÃO MANUAL", "NÃO APLICÁVEL"]
EXPECTED_VERDICTS = [
    "REPROVADO",
    "REVISÃO NECESSÁRIA",
    "APROVADO NOS CHECKS AUTOMÁTICOS, COM RESSALVAS",
    "APROVADO NOS CHECKS AUTOMÁTICOS",
]
EXPECTED_POLICY = {
    "normative_contract_changed": False,
    "locator_policy_changed": False,
    "oracle_tolerances_changed": False,
    "proof_state_changed": False,
    "shared_normative_catalog_required": True,
    "lite_deep_capability_separation_required": True,
    "unsupported_deep_checks_must_not_auto_pass": True,
    "measurement_backend_equivalence_required": False,
    "browser_network_upload_allowed": False,
}
EXPECTED_ALIASES = {
    "font.literal": ("font.family", "font.literal"),
    "font.embedded": ("font.embedding", "font.embedded"),
}
EXPECTED_WEB_ONLY = {"security.javascript"}
EXPECTED_CLI_ONLY = {"security.encrypted", "pdfa.claim", "access.pdfua"}


def fail(message: str) -> None:
    raise SystemExit(f"N14 validator contract failed: {message}")


def load_contract() -> dict[str, Any]:
    try:
        data = json.loads(CONTRACT.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load {CONTRACT}: {exc}")
    if not isinstance(data, dict):
        fail("contract must contain an object")
    return data


def require_marker(text: str, marker: str, label: str) -> None:
    if marker not in text:
        fail(f"{label} marker missing: {marker}")


def main() -> None:
    data = load_contract()
    if data.get("schema_version") != 1 or data.get("phase") != "N14":
        fail("invalid schema_version/phase")
    if data.get("status") != "ACTIVE":
        fail(f"unexpected N14 status: {data.get('status')}")
    if data.get("authority") != "technical-interface-contract":
        fail("N14 contract must remain a technical interface contract")
    if data.get("policy") != EXPECTED_POLICY:
        fail("N14 policy drift")
    if data.get("profiles") != EXPECTED_PROFILES:
        fail("profile drift")
    if data.get("statuses") != EXPECTED_STATUSES:
        fail("status vocabulary drift")
    if data.get("verdicts") != EXPECTED_VERDICTS:
        fail("verdict vocabulary drift")

    inventory = data.get("check_inventory")
    if not isinstance(inventory, list) or not inventory:
        fail("check_inventory must be a non-empty list")

    canonical_ids: list[str] = []
    web_ids: list[str] = []
    cli_ids: list[str] = []
    aliases: dict[str, tuple[str, str]] = {}
    web_only: set[str] = set()
    cli_only: set[str] = set()
    catalog_rules = rule_map(load_catalog())

    for item in inventory:
        if not isinstance(item, dict):
            fail("every inventory item must be an object")
        canonical_id = item.get("canonical_id")
        if not isinstance(canonical_id, str) or not canonical_id:
            fail("every inventory item requires canonical_id")
        canonical_ids.append(canonical_id)

        web_id = item.get("web_id")
        cli_id = item.get("cli_id")
        if web_id is not None:
            if not isinstance(web_id, str) or not web_id:
                fail(f"{canonical_id}: invalid web_id")
            web_ids.append(web_id)
        if cli_id is not None:
            if not isinstance(cli_id, str) or not cli_id:
                fail(f"{canonical_id}: invalid cli_id")
            cli_ids.append(cli_id)
        if web_id is None and cli_id is None:
            fail(f"{canonical_id}: no implementing surface")

        state = item.get("state")
        if state == "ALIAS_REQUIRED":
            if web_id is None or cli_id is None:
                fail(f"{canonical_id}: alias requires both surfaces")
            aliases[canonical_id] = (web_id, cli_id)
        elif state == "WEB_ONLY":
            if web_id is None or cli_id is not None:
                fail(f"{canonical_id}: invalid WEB_ONLY mapping")
            web_only.add(canonical_id)
        elif state == "CLI_ONLY":
            if cli_id is None or web_id is not None:
                fail(f"{canonical_id}: invalid CLI_ONLY mapping")
            cli_only.add(canonical_id)
        elif state != "ALIGNED":
            fail(f"{canonical_id}: unsupported state {state}")

        normative_rule = item.get("normative_rule")
        if normative_rule is not None and normative_rule not in catalog_rules:
            fail(f"{canonical_id}: unknown normative_rule {normative_rule}")

        web_mode = item.get("web_mode")
        cli_mode = item.get("cli_mode")
        if web_mode == "not-implemented" and web_id is not None:
            fail(f"{canonical_id}: web not-implemented but web_id is present")
        if cli_mode == "not-implemented" and cli_id is not None:
            fail(f"{canonical_id}: cli not-implemented but cli_id is present")

    if len(set(canonical_ids)) != len(canonical_ids):
        fail("duplicate canonical check id")
    if len(set(web_ids)) != len(web_ids):
        fail("duplicate Web/Lite check id")
    if len(set(cli_ids)) != len(cli_ids):
        fail("duplicate CLI/Deep check id")
    if aliases != EXPECTED_ALIASES:
        fail(f"unexpected alias inventory: {aliases}")
    if web_only != EXPECTED_WEB_ONLY:
        fail(f"unexpected Web/Lite-only inventory: {sorted(web_only)}")
    if cli_only != EXPECTED_CLI_ONLY:
        fail(f"unexpected CLI/Deep-only inventory: {sorted(cli_only)}")

    shared = sum(
        item.get("web_id") is not None and item.get("cli_id") is not None
        for item in inventory
    )
    baseline = data.get("baseline")
    expected_counts = {
        "web_check_count": len(web_ids),
        "cli_check_count": len(cli_ids),
        "canonical_check_count": len(canonical_ids),
        "shared_canonical_count": shared,
        "alias_count": len(aliases),
        "web_only_count": len(web_only),
        "cli_only_count": len(cli_only),
    }
    if not isinstance(baseline, dict):
        fail("baseline must be an object")
    for key, expected in expected_counts.items():
        if baseline.get(key) != expected:
            fail(f"baseline {key}={baseline.get(key)} expected={expected}")
    if expected_counts != {
        "web_check_count": 25,
        "cli_check_count": 27,
        "canonical_check_count": 28,
        "shared_canonical_count": 24,
        "alias_count": 2,
        "web_only_count": 1,
        "cli_only_count": 3,
    }:
        fail(f"unexpected N14 initial inventory counts: {expected_counts}")

    target = data.get("target_report_schema")
    if not isinstance(target, dict) or target.get("case") != "snake_case":
        fail("target report schema must use snake_case")
    if target.get("adoption_state") != "PENDING":
        fail("initial N14 target schema must remain pending adoption")

    web = WEB.read_text(encoding="utf-8")
    cli = CLI.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")
    require_marker(web, 'from "./normative-catalog.js"', "Web/Lite normative catalog")
    require_marker(cli, "from normative_catalog import", "CLI/Deep normative catalog")
    require_marker(web, "pdfjs-dist@6.2.108", "Web/Lite PDF.js pin")
    require_marker(web, 'mode:"web-lite-local"', "Web/Lite mode")
    require_marker(html, "não é enviado para servidor", "Web/Lite local-processing disclosure")

    forbidden = r"FormData\(|XMLHttpRequest|sendBeacon\(|WebSocket\(|\bfetch\s*\("
    if re.search(forbidden, web):
        fail("browser code contains a network upload API")

    for marker in ('"font.family"', '"font.embedding"', '"security.javascript"', '"pdfa.deep"'):
        require_marker(web, marker, "Web/Lite baseline")
    for marker in ("'font.literal'", "'font.embedded'", "'security.encrypted'", "'pdfa.claim'", "'access.pdfua'"):
        require_marker(cli, marker, "CLI/Deep baseline")

    require_marker(web, "normativeCatalog", "Web/Lite current report schema")
    require_marker(web, "normativeRule", "Web/Lite current check schema")
    require_marker(cli, "'normative_catalog'", "CLI/Deep current report schema")
    require_marker(cli, "normative_rule", "CLI/Deep current check schema")

    deep_boundaries = {
        item["canonical_id"]: (item["web_mode"], item["cli_mode"])
        for item in inventory
        if item["canonical_id"] in {"font.embedded", "pdfa.deep"}
    }
    if deep_boundaries != {
        "font.embedded": ("review-only", "automatic-deep"),
        "pdfa.deep": ("review-only", "automatic-deep"),
    }:
        fail(f"deep capability boundary drift: {deep_boundaries}")

    print(
        "N14-EVIDENCE validator-inventory "
        f"status=PASS web_checks={len(web_ids)} cli_checks={len(cli_ids)} "
        f"canonical_checks={len(canonical_ids)} shared={shared} aliases={len(aliases)} "
        f"web_only={len(web_only)} cli_only={len(cli_only)} phase_status=ACTIVE "
        "normative_contract_changed=false proof_state_changed=false"
    )
    print(
        "N14-EVIDENCE capability-boundary "
        "status=PASS web_lite_upload=false deep_review_only=font.embedded,pdfa.deep "
        "measurement_backend_equivalence_required=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()
