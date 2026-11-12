#!/usr/bin/env python3
"""Fail-closed 72-identifier bounded functional acceptance inventory.

The evidence is intentionally historical and commit-bound. Neither this
validator nor lexical source links can certify any untested runtime branch,
official institutional translation, visual norm or release publication.
"""
from __future__ import annotations

import argparse
import copy
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
API_PATH = ROOT / "standards/api/public-api.json"
CROSSWALK_PATH = ROOT / "standards/api/i18n-functional-evidence-crosswalk.json"
LEDGER_PATH = ROOT / "standards/api/i18n-per-identifier-proof-status.json"
REPORT_PATH = ROOT / "artifacts/validation/i18n-per-identifier-proof-status.json"
RUNTIME_SHA = "a73ef656de71d38ad30d7029ac3d86f852339950"
BASE_SHA = "b2001b0f979f76d1e30f11afbf03f6a10becd325"
EXPECTED_EVIDENCE = {
    "core-lists-12": {
        "source_sha": "33895971db46cad90ded218d6e777394913fe18f",
        "workflow_run_id": 43047799765,
        "artifact_ids": {
            "pt": 13866994671, "en": 13869270700,
            "es": 13867558030, "fr": 13867452973,
        },
        "runner": "tests/integration/frontmatter/i18n-list-environment-evidence.py",
        "negative_controls": 15,
    },
    "optional-env-12": {
        "source_sha": "8aa467f1adb729483b0aaa49539fdf5a9a422c2b",
        "workflow_run_id": 43064254638,
        "artifact_ids": {
            "pt": 13874314489, "en": 13874738207,
            "es": 13876275360, "fr": 13874274553,
        },
        "runner": "tests/integration/frontmatter/i18n-optional-environment-evidence.py",
        "negative_controls": 22,
    },

    "b2-family-12": {
        "source_sha": "96b395ed47591c948af2d6a9bc60c9f1fb63f63b",
        "workflow_run_id": 43195021431,
        "artifact_ids": {"pt": 13932771946, "en": 13932782130, "es": 13931829747, "fr": 13933076465},
        "runner": "tests/integration/frontmatter/i18n-b2-family-evidence.py",
        "negative_controls": 26,
    },
    "b2-summary-remaining": {
        "source_sha": "96b395ed47591c948af2d6a9bc60c9f1fb63f63b",
        "workflow_run_id": 43195021431,
        "artifact_ids": {"pt": 13932771946, "en": 13932782130, "es": 13931829747, "fr": 13933076465},
        "runner": "tests/integration/frontmatter/i18n-b2-remaining-summary-evidence.py",
        "negative_controls": 30,
    },

    "b1-integrated-15": {
        "source_sha": "e3f0ebcab9321aaa4c3341c9c79c1e11511d07ce",
        "workflow_run_id": 43253526935,
        "artifact_ids": {
            "pt": 13960622165, "en": 13959738580,
            "es": 13959643566, "fr": 13960872122,
        },
        "runner": "tests/integration/frontmatter/i18n-b1-family-evidence.py",
        "negative_controls": 14,
    },
    "b1-auxiliary-2": {
        "source_sha": "e3f0ebcab9321aaa4c3341c9c79c1e11511d07ce",
        "workflow_run_id": 43253526935,
        "artifact_ids": {"mixed": 13961625458, "coat": 13959908069},
        "runner": "tests/integration/frontmatter/i18n-b1-auxiliary-pdf-evidence.py",
        "negative_controls": 4,
    },
    "b1-optional-config-3": {
        "source_sha": "e3f0ebcab9321aaa4c3341c9c79c1e11511d07ce",
        "workflow_run_id": 43253527259,
        "artifact_ids": {
            "pt": 13960227057, "en": 13959204409,
            "es": 13961605439, "fr": 13959299308,
        },
        "runner": "tests/integration/objects/i18n-b1-optional-config-evidence.py",
        "negative_controls": 10,
    },
    "b1-final-five": {
        "source_sha": "e3f0ebcab9321aaa4c3341c9c79c1e11511d07ce",
        "workflow_run_id": 43253526935,
        "artifact_ids": {
            "pt": 13960622165, "en": 13959738580,
            "es": 13959643566, "fr": 13960872122,
        },
        "runner": "tests/integration/frontmatter/i18n-b1-final-five-evidence.py",
        "negative_controls": 4,
    },
    "b3-integrated-9": {
        "source_sha": "851d16bb131a1b88ad93a5ff4830b2286297dea3",
        "workflow_run_id": 43271021807,
        "artifact_ids": {
            "pt": 13967553724, "en": 13967129601,
            "es": 13969081744, "fr": 13967509371,
        },
        "runner": "tests/integration/frontmatter/i18n-b3-integrated-list-evidence.py",
        "negative_controls": 24,
    },
    "b3-optional-2": {
        "source_sha": "851d16bb131a1b88ad93a5ff4830b2286297dea3",
        "workflow_run_id": 43271021778,
        "artifact_ids": {
            "pt": 13969011260, "en": 13968662366,
            "es": 13968561852, "fr": 13968691920,
        },
        "runner": "tests/integration/objects/i18n-b3-optional-list-evidence.py",
        "negative_controls": 14,
    },
    "b4-integrated-11": {
        "source_sha": "f5ca6036c7c4a1c976465a2f152a2aec9ab318e0",
        "workflow_run_id": 43317424521,
        "artifact_ids": {
            "pt": 13987629952, "en": 13989382024,
            "es": 13987729501, "fr": 13987894257,
        },
        "runner": "tests/integration/frontmatter/i18n-b4-integrated-backmatter-evidence.py",
        "negative_controls": 15,
    },
    "b4-inputminted-1": {
        "source_sha": "f5ca6036c7c4a1c976465a2f152a2aec9ab318e0",
        "workflow_run_id": 43317424194,
        "artifact_ids": {
            "pt": 13989391429, "en": 13988368111,
            "es": 13987814035, "fr": 13989850288,
        },
        "runner": "tests/integration/objects/i18n-b4-inputminted-evidence.py",
        "negative_controls": 9,
    },
    "b4-isolated-2": {
        "source_sha": "f5ca6036c7c4a1c976465a2f152a2aec9ab318e0",
        "workflow_run_id": 43317424521,
        "artifact_ids": {
            "pt": 13987629952, "en": 13989382024,
            "es": 13987729501, "fr": 13987894257,
        },
        "runner": "tests/integration/frontmatter/i18n-b4-isolated-public-api-evidence.py",
        "negative_controls": 18,
    },
}
EXPECTED_PASS_ENV = {
    "ufclettereditems": "core-lists-12",
    "ufcdashedsubitems": "core-lists-12",
    "ufcdefinitionlist": "core-lists-12",
    "ufcobject": "optional-env-12",
    "ufclisting": "optional-env-12",
    "ufcalgorithm": "optional-env-12",
}

EXPECTED_PASS_B2 = {
    r"\ufcPrintCover": "b2-family-12",
    r"\ufcPrintTitlePage": "b2-family-12",
    r"\ufcPrintApprovalPage": "b2-family-12",
    r"\ufcPrintCatalogCard": "b2-family-12",
    r"\ufcPrintDedication": "b2-family-12",
    r"\ufcPrintAcknowledgments": "b2-family-12",
    r"\ufcPrintEpigraph": "b2-family-12",
    r"\ufcPrintErrata": "b2-family-12",
    r"\ufcPrintRequiredSummaries": "b2-family-12",
    r"\ufcSummaryKeywords": "b2-family-12",
    r"\ufcSummaryKeywordsInLanguage": "b2-family-12",
    r"\ufcPrintArticleTranslatedSummary": "b2-family-12",
    r"\ufcPrintSummaryInLanguage": "b2-summary-remaining",
    r"\ufcPrintOptionalEnglishSummary": "b2-summary-remaining",
    r"\ufcPrintSummary": "b2-summary-remaining",
    r"\ufcPrintAbstract": "b2-summary-remaining",
}

EXPECTED_PASS_B1 = {
    ("setup_option_identifiers", "type"): "b1-integrated-15",
    ("setup_option_identifiers", "document-language"): "b1-integrated-15",
    ("setup_option_identifiers", "print-mode"): "b1-integrated-15",
    ("setup_option_identifiers", "cover"): "b1-integrated-15",
    ("setup_option_identifiers", "advisor-feminine-label"): "b1-integrated-15",
    ("setup_option_identifiers", "coadvisor-feminine-label"): "b1-integrated-15",
    ("setup_option_identifiers", "glossary"): "b1-integrated-15",
    ("setup_option_identifiers", "index"): "b1-integrated-15",
    ("public_commands", r"\ufcsetup"): "b1-integrated-15",
    ("public_commands", r"\ufcDocumentType"): "b1-integrated-15",
    ("public_commands", r"\ufcPrintMode"): "b1-integrated-15",
    ("public_commands", r"\ufcMeta"): "b1-integrated-15",
    ("public_commands", r"\ufcIfProjectTF"): "b1-integrated-15",
    ("public_commands", r"\ufcIfAnonymizedProjectTF"): "b1-integrated-15",
    ("public_commands", r"\ufcDocumentLanguage"): "b1-integrated-15",
    ("setup_option_identifiers", "labels-language"): "b1-auxiliary-2",
    ("setup_option_identifiers", "coat-of-arms"): "b1-auxiliary-2",
    ("setup_option_identifiers", "tables"): "b1-optional-config-3",
    ("setup_option_identifiers", "code"): "b1-optional-config-3",
    ("setup_option_identifiers", "algorithms"): "b1-optional-config-3",
    ("setup_option_identifiers", "catalog-card"): "b1-final-five",
    ("setup_option_identifiers", "font"): "b1-final-five",
    ("setup_option_identifiers", "strict-font"): "b1-final-five",
    ("setup_option_identifiers", "initial-page"): "b1-final-five",
    ("public_commands", r"\ufcMathFontPolicy"): "b1-final-five",
}
EXPECTED_PASS_B3 = {
    r"\ufcPrintListOfFigures": "b3-integrated-9",
    r"\ufcPrintListOfTables": "b3-integrated-9",
    r"\ufcPrintListOfIllustrations": "b3-integrated-9",
    r"\ufcPrintListOfTextTables": "b3-integrated-9",
    r"\ufcPrintListOfCharts": "b3-integrated-9",
    r"\ufcPrintListOfAbbreviationsAndAcronyms": "b3-integrated-9",
    r"\ufcPrintListOfSymbols": "b3-integrated-9",
    r"\ufcPrintTableOfContents": "b3-integrated-9",
    r"\ufcListEntry": "b3-integrated-9",
    r"\ufcPrintListOfCodeListings": "b3-optional-2",
    r"\ufcPrintListOfAlgorithms": "b3-optional-2",
}

EXPECTED_PASS_B4 = {
    ("public_commands", r"\ufcSource"): "b4-integrated-11",
    ("public_commands", r"\ufcNote"): "b4-integrated-11",
    ("public_commands", r"\ufcAddBibliographyResource"): "b4-integrated-11",
    ("public_commands", r"\ufcPrintReferences"): "b4-integrated-11",
    ("public_commands", r"\ufcPrintGlossary"): "b4-integrated-11",
    ("public_commands", r"\ufcPrintIndex"): "b4-integrated-11",
    ("retained_upstream_identifiers", r"\legend"): "b4-integrated-11",
    ("retained_upstream_identifiers", r"\appendix"): "b4-integrated-11",
    ("retained_upstream_identifiers", r"\annex"): "b4-integrated-11",
    ("retained_upstream_identifiers", r"\pretextual"): "b4-integrated-11",
    ("retained_upstream_identifiers", r"\textual"): "b4-integrated-11",
    ("public_commands", r"\ufcInputMinted"): "b4-inputminted-1",
    ("public_commands", r"\ufcInputListing"): "b4-isolated-2",
    ("retained_upstream_identifiers", r"\keywords"): "b4-isolated-2",
}

EXPECTED_PROOF_SCOPES = {
    "core-lists-12": "ONE_ISOLATED_PDF_PER_ENVIRONMENT_AND_LOCALE",
    "optional-env-12": "ONE_ISOLATED_PDF_PER_ENVIRONMENT_AND_LOCALE",
    "b2-family-12": "TWELVE_PRETEXTUAL_COMMANDS_FOUR_LOCALE_REAL_PDFS",
    "b2-summary-remaining": "FOUR_SUMMARY_COMMANDS_APPLICABLE_LOCALE_REAL_PDFS",
    "b1-integrated-15": "FIFTEEN_B1_PUBLIC_SETUP_CORE_FOUR_LOCALE_SEVEN_PROFILE_PDFS",
    "b1-auxiliary-2": "TWO_B1_CONFIG_OPTIONS_SIXTY_FOUR_REAL_PDFS",
    "b1-optional-config-3": "THREE_B1_OPTIONAL_CONFIG_FOUR_LOCALE_TWELVE_REAL_PDFS",
    "b1-final-five": "FIVE_B1_CORE_OPTIONS_FOUR_LOCALE_PDFTEX_LUATEX_RECEIPTS",
    "b3-integrated-9": "NINE_B3_PRETEXTUAL_LISTS_FOUR_LOCALE_SEVEN_PROFILE_REAL_PDFS",
    "b3-optional-2": "TWO_B3_OPTIONAL_LISTS_FOUR_LOCALE_THREE_PROFILE_REAL_PDFS",
    "b4-integrated-11": "ELEVEN_B4_BACKMATTER_SOURCE_AND_LEGACY_APIS_FOUR_LOCALE_SEVEN_PROFILE_REAL_PDFS",
    "b4-inputminted-1": "ONE_B4_MINTED_IMPORTED_PYTHON_FOUR_LOCALE_THREE_OPTIONAL_REAL_PDFS",
    "b4-isolated-2": "TWO_B4_ISOLATED_DIRECT_INPUTLISTING_AND_LEGACY_KEYWORDS_FOUR_LOCALE_REAL_PDFS",
}
GROUPS = ("setup_option_identifiers", "public_commands",
          "public_environments", "retained_upstream_identifiers")
ENTRY_KEYS = {"result", "scope", "evidence_id", "candidate_source",
              "reason", "human_normative_linguistic_review"}
PROOF_KEYS = {"source_sha", "workflow_run_id", "artifact_ids",
              "runner", "negative_controls", "scope", "qualification"}


def read_json(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def expected_names(api: dict, cross: dict) -> dict[str, set[str]]:
    if set(cross["entries"]) != set(GROUPS):
        raise ValueError("candidate crosswalk groups changed")
    options = set(cross["entries"]["setup_option_identifiers"])
    canonical = {
        "setup_option_identifiers": options,
        "public_commands": set(api["public_commands"]["canonical"]),
        "public_environments": set(api["public_environments"]["canonical"]),
        "retained_upstream_identifiers":
            set(api["upstream_boundary"]["retained_identifiers"]),
    }
    if tuple(map(len, canonical.values())) != (17, 43, 6, 6):
        raise ValueError("public API identifier counts drifted")
    if any(set(cross["entries"][kind]) != expected
           for kind, expected in canonical.items()):
        raise ValueError("crosswalk differs from public API names")
    return canonical


def validate(data: dict, api: dict, cross: dict) -> dict[str, int]:
    canonical = expected_names(api, cross)
    if data.get("schema_version") != 1:
        raise ValueError("unknown proof-status schema")
    if data.get("created_from_main_sha") != BASE_SHA:
        raise ValueError("unexpected proof-status origin")
    if data.get("same_runtime_blob") != RUNTIME_SHA:
        raise ValueError("a new runtime requires evidence recertification")
    if data.get("global_acceptance") != "PENDING":
        raise ValueError("unproved global certification")
    if data.get("publication_authorized") is not False:
        raise ValueError("publication must remain unauthorized")
    if data.get("human_normative_linguistic_review") != "PENDING":
        raise ValueError("human signoff was not supplied")
    if data.get("source_crosswalk") != "standards/api/i18n-functional-evidence-crosswalk.json":
        raise ValueError("source crosswalk binding drift")
    if data.get("api_source") != "standards/api/public-api.json":
        raise ValueError("canonical API binding drift")
    if set(data.get("evidence", {})) != set(EXPECTED_EVIDENCE):
        raise ValueError("missing, added or unreviewed proof suite")
    for suite, expected in EXPECTED_EVIDENCE.items():
        evidence = data["evidence"][suite]
        if set(evidence) != PROOF_KEYS:
            raise ValueError(f"unqualified proof metadata: {suite}")
        for key, value in expected.items():
            if evidence.get(key) != value:
                raise ValueError(f"proof provenance drift: {suite}/{key}")
        if evidence["scope"] != EXPECTED_PROOF_SCOPES[suite]:
            raise ValueError(f"PDF proof scope drift: {suite}")
        if not evidence["qualification"] or "pending" not in evidence["qualification"].lower():
            raise ValueError("scope's human review limitations omitted")
        if not (ROOT / evidence["runner"]).is_file():
            raise ValueError(f"missing original public PDF probe {suite}")
    if set(data.get("entries", {})) != set(GROUPS):
        raise ValueError("proof-state groups differ from canonical API")
    counts = {"PASS": 0, "PENDING": 0, "NA": 0}
    for group, names in canonical.items():
        entries = data["entries"][group]
        if not isinstance(entries, dict) or set(entries) != names:
            raise ValueError(f"missing or invented public identifier: {group}")
        for name, row in entries.items():
            if set(row) != ENTRY_KEYS:
                raise ValueError(f"inconsistent proof-status columns: {group}/{name}")
            if row["candidate_source"] != cross["entries"][group][name]["candidate_test_file"]:
                raise ValueError(f"source mismatch to crosswalk: {name}")
            if row["human_normative_linguistic_review"] != "PENDING":
                raise ValueError(f"human acceptance not established: {name}")
            if not isinstance(row["reason"], str) or len(row["reason"].strip()) < 35:
                raise ValueError(f"missing scope or acceptance rationale: {name}")
            result = row["result"]
            if result not in counts:
                raise ValueError(f"unknown evidence state: {name}/{result}")
            counts[result] += 1
            suite = EXPECTED_PASS_ENV.get(name) if group == "public_environments" else None
            if suite is not None:
                if (result != "PASS" or row["evidence_id"] != suite
                        or row["scope"] != "BOUNDED_REAL_PDF_4_LOCALES"):
                    raise ValueError(f"PDF-proven environment incorrectly classified: {name}")
                if cross["entries"][group][name]["candidate_suite"] != suite:
                    raise ValueError(f"candidate suite mismatch: {name}")
            elif group == "public_commands" and name in EXPECTED_PASS_B2:
                b2_suite = EXPECTED_PASS_B2[name]
                b2_scope = ("BOUNDED_REAL_PDF_ES_FR_ONLY"
                            if name == r"\ufcPrintOptionalEnglishSummary"
                            else "BOUNDED_REAL_PDF_4_LOCALES")
                if (result != "PASS" or row["evidence_id"] != b2_suite
                        or row["scope"] != b2_scope):
                    raise ValueError(f"B2 real-PDF proof incorrectly classified: {name}")
                if not any(source.get("suite") == b2_suite
                           and source.get("path") == EXPECTED_EVIDENCE[b2_suite]["runner"]
                           for source in cross["sources"]):
                    raise ValueError(f"B2 original source-to-suite relation absent: {name}")
            elif (group, name) in EXPECTED_PASS_B1:
                b1_suite = EXPECTED_PASS_B1[(group, name)]
                if (result != "PASS" or row["evidence_id"] != b1_suite
                        or row["scope"] != "BOUNDED_REAL_PDF_4_LOCALES"):
                    raise ValueError(f"B1 real-PDF proof incorrectly classified: {group}/{name}")
                if EXPECTED_EVIDENCE[b1_suite]["source_sha"] not in row["reason"]:
                    raise ValueError(f"B1 row not linked to exact source SHA: {name}")
                if not any(source.get("suite") == b1_suite
                           and source.get("path") == EXPECTED_EVIDENCE[b1_suite]["runner"]
                           for source in cross["sources"]):
                    raise ValueError(f"B1 original source-to-suite link missing: {name}")
            elif group == "public_commands" and name in EXPECTED_PASS_B3:
                b3_suite = EXPECTED_PASS_B3[name]
                if (result != "PASS" or row["evidence_id"] != b3_suite
                        or row["scope"] != "BOUNDED_REAL_PDF_4_LOCALES"):
                    raise ValueError(f"B3 real-PDF proof incorrectly classified: {name}")
                if EXPECTED_EVIDENCE[b3_suite]["source_sha"] not in row["reason"]:
                    raise ValueError(f"B3 proof not linked to exact source SHA: {name}")
                if not any(source.get("suite") == b3_suite
                           and source.get("path") == EXPECTED_EVIDENCE[b3_suite]["runner"]
                           for source in cross["sources"]):
                    raise ValueError(f"B3 source-to-suite relation missing: {name}")
            elif (group, name) in EXPECTED_PASS_B4:
                b4_suite = EXPECTED_PASS_B4[(group, name)]
                if (result != "PASS" or row["evidence_id"] != b4_suite
                        or row["scope"] != "BOUNDED_REAL_PDF_4_LOCALES"):
                    raise ValueError(f"B4 bounded real-PDF proof misclassified: {group}/{name}")
                if EXPECTED_EVIDENCE[b4_suite]["source_sha"] not in row["reason"]:
                    raise ValueError(f"B4 original source SHA not linked per API: {name}")
                if not any(source.get("suite") == b4_suite
                           and source.get("path") == EXPECTED_EVIDENCE[b4_suite]["runner"]
                           for source in cross["sources"]):
                    raise ValueError(f"B4 original runner/source relationship absent: {name}")
                if name == r"\ufcInputListing" and (
                        "#590" not in row["reason"] or "EXCLUDED" not in row["reason"]):
                    raise ValueError("nested InputListing 2026 failure was improperly claimed")
            elif (result != "PENDING" or row["evidence_id"] is not None
                  or row["scope"] != "NOT_YET_CERTIFIED_PER_IDENTIFIER"):
                raise ValueError(f"unproven identifier promoted or wrongly classified: {name}")
    if counts != {"PASS": 72, "PENDING": 0, "NA": 0}:
        raise ValueError("72-ID evidence classification totals drift")
    if data.get("summary") != counts:
        raise ValueError("evidence summary differs from individual records")
    return counts


def negative_controls(data: dict, api: dict, cross: dict) -> int:
    tests = []
    def edited() -> dict:
        return copy.deepcopy(data)

    x = edited()
    x["global_acceptance"] = "PASS"
    tests.append(x)
    x = edited()
    x["publication_authorized"] = True
    tests.append(x)
    x = edited()
    x["human_normative_linguistic_review"] = "ACCEPT"
    tests.append(x)
    x = edited()
    x["same_runtime_blob"] = "0" * 40
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"]["\\ufcsetup"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["public_environments"]["ufcobject"]["evidence_id"] = "core-lists-12"
    tests.append(x)
    x = edited()
    x["entries"]["public_environments"]["ufcobject"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["public_environments"]["ufclettereditems"]["scope"] = "GLOBAL_ALL_PROFILES"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"].pop("type")
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"]["\\ufcImaginary"] = copy.deepcopy(
        x["entries"]["public_commands"]["\\ufcsetup"])
    tests.append(x)
    x = edited()
    x["evidence"]["optional-env-12"]["artifact_ids"]["fr"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["core-lists-12"]["source_sha"] = "f" * 40
    tests.append(x)
    x = edited()
    x["evidence"]["optional-env-12"]["runner"] = "tests/not-a-real-file.py"
    tests.append(x)
    x = edited()
    x["entries"]["retained_upstream_identifiers"]["\\legend"]["candidate_source"] = "not/source"
    tests.append(x)
    x = edited()
    x["summary"]["PASS"] += 1
    tests.append(x)
    x = edited()
    x["entries"]["public_environments"]["ufcobject"]["human_normative_linguistic_review"] = "ACCEPT"
    tests.append(x)

    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintCover"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintEpigraph"]["evidence_id"] = "b2-summary-remaining"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintOptionalEnglishSummary"]["scope"] = "GLOBAL_FOUR_LOCALES"
    tests.append(x)
    x = edited()
    x["evidence"]["b2-family-12"]["source_sha"] = "e" * 40
    tests.append(x)
    x = edited()
    x["evidence"]["b2-summary-remaining"]["artifact_ids"]["es"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b2-summary-remaining"]["runner"] = "tests/not-a-real-file.py"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"]["type"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"]["labels-language"]["evidence_id"] = "b1-integrated-15"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"]["coat-of-arms"]["scope"] = "ALL_PROFILES"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"]["font"]["evidence_id"] = "b1-optional-config-3"
    tests.append(x)
    x = edited()
    x["entries"]["setup_option_identifiers"]["initial-page"]["result"] = "NA"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcMathFontPolicy"]["human_normative_linguistic_review"] = "ACCEPT"
    tests.append(x)
    x = edited()
    x["evidence"]["b1-integrated-15"]["source_sha"] = "a" * 40
    tests.append(x)
    x = edited()
    x["evidence"]["b1-auxiliary-2"]["artifact_ids"]["coat"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b1-optional-config-3"]["workflow_run_id"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b1-final-five"]["runner"] = "tests/not-a-real-file.py"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfFigures"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfTables"]["evidence_id"] = "b3-optional-2"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfCharts"]["scope"] = "ALL_PROFILES"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfAbbreviationsAndAcronyms"]["human_normative_linguistic_review"] = "ACCEPT"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfCodeListings"]["evidence_id"] = "b3-integrated-9"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintListOfAlgorithms"]["result"] = "NA"
    tests.append(x)
    x = edited()
    x["evidence"]["b3-integrated-9"]["artifact_ids"]["fr"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b3-optional-2"]["runner"] = "tests/does-not-exist.py"
    tests.append(x)
    x = edited()
    x["evidence"]["b3-optional-2"]["source_sha"] = "f" * 40
    tests.append(x)
    x = edited()
    x["evidence"]["b3-integrated-9"]["workflow_run_id"] += 1
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcSource"]["result"] = "PENDING"
    tests.append(x)
    x = edited()
    x["entries"]["retained_upstream_identifiers"][r"\legend"]["evidence_id"] = "b4-isolated-2"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcPrintGlossary"]["scope"] = "ALL_PROFILES"
    tests.append(x)
    x = edited()
    x["entries"]["retained_upstream_identifiers"][r"\textual"]["human_normative_linguistic_review"] = "ACCEPT"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcInputMinted"]["evidence_id"] = "b4-integrated-11"
    tests.append(x)
    x = edited()
    x["entries"]["retained_upstream_identifiers"][r"\keywords"]["result"] = "NA"
    tests.append(x)
    x = edited()
    x["entries"]["public_commands"][r"\ufcInputListing"]["reason"] = "Original source f5ca6036c7c4a1c976465a2f152a2aec9ab318e0; standalone only, issue not considered."
    tests.append(x)
    x = edited()
    x["evidence"]["b4-integrated-11"]["artifact_ids"]["en"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b4-inputminted-1"]["source_sha"] = "1" * 40
    tests.append(x)
    x = edited()
    x["evidence"]["b4-isolated-2"]["runner"] = "tests/not-the-actual-proof.py"
    tests.append(x)
    x = edited()
    x["evidence"]["b4-inputminted-1"]["workflow_run_id"] += 1
    tests.append(x)
    x = edited()
    x["evidence"]["b4-integrated-11"]["negative_controls"] = 0
    tests.append(x)
    for i, mutation in enumerate(tests, start=1):
        try:
            validate(mutation, api, cross)
        except ValueError:
            continue
        raise ValueError(f"mutation control {i} unexpectedly accepted")
    return len(tests)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    api, cross, data = (read_json(path) for path in
                        (API_PATH, CROSSWALK_PATH, LEDGER_PATH))
    blob = git("hash-object", "abntexto-ufc.cls")
    if blob != RUNTIME_SHA:
        raise ValueError("LaTeX class changed since bounded PDF proof; recertify")
    sha = git("rev-parse", "HEAD")
    expected_sha = os.getenv("SOURCE_COMMIT_SHA")
    if expected_sha and expected_sha != sha:
        raise ValueError("CI checkout differs from requested source SHA")
    counts = validate(data, api, cross)
    negative_count = negative_controls(data, api, cross)
    report = {
        "evaluation_sha": sha,
        "runtime_git_blob": blob,
        "status": "BOUNDED_PER_IDENTIFIER_CLASSIFICATION_PASS",
        "global_i18n_acceptance": "PENDING",
        "human_review": "PENDING",
        "published_3_1_0": False,
        "counts": counts,
        "negative_controls": negative_count,
        "historical_source_bound_proofs": data["evidence"],
        "proof_boundary": "All 72 named public identifiers have individually scoped positive real-PDF functional receipts across B1/B2/B3/B4, not universal combinations, standard-conformance review or language signoff. The InputListing inside ufcobject TeX Live 2026 defect #590 is expressly excluded from its standalone PASS. Global UFC/ABNT normative, visual and linguistic human acceptance and v3.1.0 publication remain PENDING",
    }
    if args.report:
        REPORT_PATH.parent.mkdir(parents=True, exist_ok=True)
        REPORT_PATH.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")
    print("I18N-ITEM-STATUS status=PASS"
          f" evaluation_sha={sha} PASS={counts['PASS']}"
          f" PENDING={counts['PENDING']} NA={counts['NA']}"
          f" negatives={negative_count} runtime_blob=PASS"
          " global_i18n=PENDING human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError,
            subprocess.CalledProcessError) as exc:
        raise SystemExit(f"I18N-ITEM-STATUS status=FAIL reason={exc}") from exc
