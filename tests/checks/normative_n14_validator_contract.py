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
EXPECTED_BASELINE_COUNTS = {
    "web_check_count": 25,
    "cli_check_count": 27,
    "canonical_check_count": 28,
    "shared_canonical_count": 24,
    "alias_count": 2,
    "web_only_count": 1,
    "cli_only_count": 3,
}
EXPECTED_BASELINE_ALIASES = {
    "font.literal": {"web_id": "font.family", "cli_id": "font.literal"},
    "font.embedded": {"web_id": "font.embedding", "cli_id": "font.embedded"},
}
EXPECTED_BASELINE_SCHEMA_DRIFT = {
    "web_normative_catalog_field": "normativeCatalog",
    "cli_normative_catalog_field": "normative_catalog",
    "web_normative_rule_field": "normativeRule",
    "cli_normative_rule_field": "normative_rule",
    "web_mode_field": True,
    "cli_mode_field": False,
}
EXPECTED_WEB_ONLY = {"security.javascript"}
EXPECTED_CLI_ONLY = {"security.encrypted", "pdfa.claim", "access.pdfua"}
EXPECTED_TOP_LEVEL = ["file", "profile", "verdict", "normative_catalog", "checks", "mode"]
EXPECTED_CHECK_FIELDS = [
    "id",
    "category",
    "rule",
    "source",
    "status",
    "evidence",
    "correction",
    "mandatory",
    "level",
    "normative_rule",
    "locator",
    "normativity",
]
EXPECTED_ADOPTION = {
    "state": "ADOPTED",
    "emitted_alias_count": 0,
    "web_report_case": "snake_case",
    "cli_report_case": "snake_case",
    "web_mode": "web-lite-local",
    "cli_mode": "cli-deep-local",
    "normative_contract_changed": False,
    "proof_state_changed": False,
}


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


def forbid_marker(text: str, marker: str, label: str) -> None:
    if marker in text:
        fail(f"{label} legacy marker still present: {marker}")


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

    baseline = data.get("baseline")
    if not isinstance(baseline, dict):
        fail("baseline must be an object")
    for key, expected in EXPECTED_BASELINE_COUNTS.items():
        if baseline.get(key) != expected:
            fail(f"baseline {key}={baseline.get(key)} expected={expected}")
    if baseline.get("aliases") != EXPECTED_BASELINE_ALIASES:
        fail("historical alias baseline drift")
    if baseline.get("observed_schema_drift") != EXPECTED_BASELINE_SCHEMA_DRIFT:
        fail("historical schema-drift baseline changed")

    surfaces = data.get("surfaces")
    if not isinstance(surfaces, dict):
        fail("surfaces must be an object")
    web_surface = surfaces.get("web-lite")
    cli_surface = surfaces.get("cli-deep")
    if not isinstance(web_surface, dict) or not isinstance(cli_surface, dict):
        fail("both validator surfaces must be declared")
    if web_surface.get("report_case") != "snake_case" or cli_surface.get("report_case") != "snake_case":
        fail("both surfaces must adopt snake_case")
    if web_surface.get("mode") != "web-lite-local" or cli_surface.get("mode") != "cli-deep-local":
        fail("surface mode drift")
    if web_surface.get("local_processing") is not True or cli_surface.get("local_processing") is not True:
        fail("both surfaces must remain local-processing")

    target = data.get("target_report_schema")
    if not isinstance(target, dict) or target.get("case") != "snake_case":
        fail("target report schema must use snake_case")
    if target.get("required_top_level") != EXPECTED_TOP_LEVEL:
        fail("target top-level schema drift")
    if target.get("required_check_fields") != EXPECTED_CHECK_FIELDS:
        fail("target check schema drift")
    if target.get("adoption_state") != "ADOPTED":
        fail("target schema must be adopted in N14-B")
    if data.get("adoption") != EXPECTED_ADOPTION:
        fail("N14-B adoption receipt drift")

    inventory = data.get("check_inventory")
    if not isinstance(inventory, list) or not inventory:
        fail("check_inventory must be a non-empty list")

    canonical_ids: list[str] = []
    web_ids: list[str] = []
    cli_ids: list[str] = []
    web_only: set[str] = set()
    cli_only: set[str] = set()
    current_aliases: list[str] = []
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
        if state == "WEB_ONLY":
            if web_id != canonical_id or cli_id is not None:
                fail(f"{canonical_id}: invalid WEB_ONLY mapping")
            web_only.add(canonical_id)
        elif state == "CLI_ONLY":
            if cli_id != canonical_id or web_id is not None:
                fail(f"{canonical_id}: invalid CLI_ONLY mapping")
            cli_only.add(canonical_id)
        elif state == "ALIGNED":
            if web_id != canonical_id or cli_id != canonical_id:
                current_aliases.append(canonical_id)
        else:
            fail(f"{canonical_id}: unsupported post-adoption state {state}")

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
    if current_aliases:
        fail(f"unresolved emitted aliases: {sorted(current_aliases)}")
    if web_only != EXPECTED_WEB_ONLY:
        fail(f"unexpected Web/Lite-only inventory: {sorted(web_only)}")
    if cli_only != EXPECTED_CLI_ONLY:
        fail(f"unexpected CLI/Deep-only inventory: {sorted(cli_only)}")

    shared = sum(item.get("web_id") is not None and item.get("cli_id") is not None for item in inventory)
    if (len(web_ids), len(cli_ids), len(canonical_ids), shared) != (25, 27, 28, 24):
        fail("post-adoption inventory counts changed")

    web = WEB.read_text(encoding="utf-8")
    cli = CLI.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")
    require_marker(web, 'from "./normative-catalog.js"', "Web/Lite normative catalog")
    require_marker(cli, "from normative_catalog import", "CLI/Deep normative catalog")
    require_marker(web, "pdfjs-dist@6.2.108", "Web/Lite PDF.js pin")
    require_marker(web, 'mode:"web-lite-local"', "Web/Lite mode")
    require_marker(cli, "'mode':'cli-deep-local'", "CLI/Deep mode")
    require_marker(html, "não é enviado para servidor", "Web/Lite local-processing disclosure")

    forbidden = r"FormData\(|XMLHttpRequest|sendBeacon\(|WebSocket\(|\bfetch\s*\("
    if re.search(forbidden, web):
        fail("browser code contains a network upload API")

    require_marker(
        web,
        'CHECK_ID_ALIASES={"font.family":"font.literal","font.embedding":"font.embedded"}',
        "Web/Lite boundary alias normalization",
    )
    require_marker(web, "id:CHECK_ID_ALIASES[c.id]??c.id", "Web/Lite canonical emitted ID")
    require_marker(web, "normative_rule:c.normativeRule", "Web/Lite canonical normative metadata")
    for marker in ('"security.javascript"', '"pdfa.deep"'):
        require_marker(web, marker, "Web/Lite current inventory")
    for marker in ("'font.literal'", "'font.embedded'", "'security.encrypted'", "'pdfa.claim'", "'access.pdfua'"):
        require_marker(cli, marker, "CLI/Deep current inventory")

    require_marker(
        web,
        "normative_catalog:{schema_version:normativeCatalog.schema_version,reviewed_at:normativeCatalog.reviewed_at}",
        "Web/Lite adopted top-level schema",
    )
    require_marker(web, "checks:reportChecks", "Web/Lite normalized check boundary")
    require_marker(web, "generated_at:new Date().toISOString()", "Web/Lite generated timestamp")
    require_marker(web, "c.normative_rule", "Web/Lite CSV canonical metadata")
    forbid_marker(web, "normativeCatalog:{", "Web/Lite top-level report schema")
    forbid_marker(web, "generatedAt:", "Web/Lite top-level report schema")
    require_marker(cli, "'normative_catalog'", "CLI/Deep report schema")
    require_marker(cli, "normative_rule", "CLI/Deep check schema")

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
        "N14-EVIDENCE validator-baseline "
        "status=PASS web_checks=25 cli_checks=27 canonical_checks=28 shared=24 "
        "baseline_aliases=2 web_only=1 cli_only=3 phase_status=ACTIVE "
        "normative_contract_changed=false proof_state_changed=false"
    )
    print(
        "N14-EVIDENCE schema-adoption "
        "status=PASS web_case=snake_case cli_case=snake_case emitted_aliases=0 "
        "web_mode=web-lite-local cli_mode=cli-deep-local phase_status=ACTIVE "
        "normative_contract_changed=false proof_state_changed=false"
    )
    print(
        "N14-EVIDENCE capability-boundary "
        "status=PASS web_lite_upload=false deep_review_only=font.embedded,pdfa.deep "
        "measurement_backend_equivalence_required=false proof_state_changed=false"
    )


if __name__ == "__main__":
    main()
