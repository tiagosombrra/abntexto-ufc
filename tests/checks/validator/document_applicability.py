#!/usr/bin/env python3
"""Fail-closed cross-surface document-type applicability regression."""
from __future__ import annotations

import json
import runpy
from pathlib import Path

ROOT = Path(__file__).resolve().parents[3]
CONTRACT = ROOT / "validator" / "document-applicability.json"
WEB = ROOT / "validator" / "document-applicability.js"
APP = ROOT / "validator" / "app.js"
INDEX = ROOT / "validator" / "index.html"
CLI = ROOT / "tools" / "validate-ufc-pdf.py"

TYPES = (
    "undergraduate-capstone",
    "specialization-capstone",
    "masters-thesis",
    "doctoral-thesis",
    "research-project",
    "anonymized-research-project",
    "scientific-article",
)
KEYS = ("cover", "approval", "resumo", "abstract", "toc", "refs", "keywords", "keywords-en")
TOKENS = (
    "UNIVERSIDADE FEDERAL DO CEARA BANCA EXAMINADORA RESUMO ABSTRACT "
    "SUMARIO REFERENCIAS PALAVRAS-CHAVE KEYWORDS"
)


def require(ok: bool, message: str) -> None:
    if not ok:
        raise SystemExit("Profile structure applicability: " + message)


def main() -> None:
    contract = json.loads(CONTRACT.read_text(encoding="utf-8"))
    require(contract["schema_version"] == 1, "schema version drift")
    require(tuple(contract["check_ids"]) == KEYS, "canonical structure keys drift")
    require(tuple(contract["document_types"]) == TYPES, "seven-profile identity drift")
    require(set(contract["modalities"]) == {"required", "optional", "not-applicable"}, "unexpected modality")

    # The served JS is an exact derivative of the JSON authority, not a second rule source.
    expected = (
        "// Generated from document-applicability.json; do not edit manually.\n"
        "export const documentApplicability = Object.freeze("
        + json.dumps(contract, ensure_ascii=False, indent=2)
        + ");\n"
    )
    require(WEB.read_text(encoding="utf-8") == expected, "static JavaScript module has drifted")

    app = APP.read_text(encoding="utf-8")
    html = INDEX.read_text(encoding="utf-8")
    cli = CLI.read_text(encoding="utf-8")
    require('from "./document-applicability.js"' in app, "browser does not load shared contract")
    require('"#document-type"' in app, "browser does not pass selected document type")
    require("'--document-type'" in cli, "CLI does not expose explicit type selection")
    require("document_type" in cli and "document_type:documentType" in app, "report type metadata missing")

    module = runpy.run_path(str(CLI), run_name="document_applicability_test")
    check_structure = module["check_structure"]
    PASS, FAIL = module["PASS"], module["FAIL"]
    NA, REVIEW = module["NA"], module["REVIEW"]

    for document_type, definition in contract["document_types"].items():
        modes = definition["checks"]
        require(set(modes) == set(KEYS), document_type + " check set drift")
        require(bool(definition.get("authority")), document_type + " lacks normative provenance")
        require(set(modes.values()) <= set(contract["modalities"]), document_type + " unknown mode")
        for sample, present in ((TOKENS, True), ("", False)):
            checks = check_structure(sample, document_type)
            require(len(checks) == len(KEYS), document_type + " unexpected number of checks")
            actual = {check.id.removeprefix("structure."): check for check in checks}
            require(set(actual) == set(KEYS), document_type + " check IDs drift")
            for key, mode in modes.items():
                c = actual[key]
                expected_status = (
                    (PASS if present else FAIL) if mode == "required"
                    else (REVIEW if present else NA) if mode == "optional"
                    else NA
                )
                require(c.status == expected_status, f"{document_type}/{key}: {c.status} != {expected_status}")
                require(c.mandatory == (mode == "required"), f"{document_type}/{key}: mandatory drift")

    project = contract["document_types"]["research-project"]["checks"]
    anonymous = contract["document_types"]["anonymized-research-project"]["checks"]
    article = contract["document_types"]["scientific-article"]["checks"]
    require(project == anonymous, "both project profiles must preserve structural applicability")
    require(project["cover"] == "optional" and project["approval"] == "not-applicable", "project cover/approval contract")
    require(article["cover"] == article["approval"] == article["toc"] == "not-applicable", "article false FAIL risk")
    require(article["refs"] == article["resumo"] == "required", "required article content must not be weakened")
    require(all(f'value="{document_type}"' in html for document_type in TYPES), "Web/Lite selector incomplete")

    print("DOCUMENT-APPLICABILITY-EVIDENCE status=PASS types=7 checks=8 scenarios=14 "
          "generated_js=IDENTICAL required_negative=FAIL optional_negative=NOT_APPLICABLE")


if __name__ == "__main__":
    main()
