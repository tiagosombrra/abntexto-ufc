#!/usr/bin/env python3
"""Fail-closed PUBLIC API evidence-source crosswalk; source links are NOT PDFs.

This registry is deliberately conservative. Finding a token in an existing
test/fixture does not certify a translated output, any public branch, or a
human visual/linguistic acceptance. Reconcile these separately in later P0.8D
functional evidence; do not silently promote the registry to "all PASS".
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[3]
API_FILE = ROOT / "standards/api/public-api.json"
I18N_FILE = ROOT / "standards/api/i18n-coverage-inventory.json"
MAP_FILE = ROOT / "standards/api/i18n-functional-evidence-crosswalk.json"
OUTPUT = ROOT / "artifacts/validation/i18n-public-evidence-crosswalk.json"
SOURCE_STATES = {"SOURCE_REFERENCE_ONLY", "UNMAPPED"}
SOURCES = {"integrated-28", "optional-12", "coat-32", "inherited-pdf",
           "legacy-summary-pdf", "profile-28", "display-labels-pdf",
           "summary-language-pdf", "multivolume-pdf", "layout-font-integration", "fixture"}


def expected_groups(api: dict, inventory: dict) -> dict[str, set[str]]:
    options = {key for key, value in inventory["setup_keys"].items()
               if value["origin"] == "option_identifier"}
    if len(options) != 17:
        raise ValueError("public option identifier count changed; re-audit")
    original_setup = {key for group in api["setup_keys"].values() for key in group}
    if set(inventory["setup_keys"]) != original_setup:
        raise ValueError("public setup inventory differs from canonical API")
    if inventory["completion"] != "PENDING_INTEGRATED_PDF_AND_HUMAN_REVIEW":
        raise ValueError("premature promotion of global i18n acceptance")
    return {
        "setup_option_identifiers": options,
        "public_commands": set(api["public_commands"]["canonical"]),
        "public_environments": set(api["public_environments"]["canonical"]),
        "retained_upstream_identifiers":
            set(api["upstream_boundary"]["retained_identifiers"]),
    }


def validate(data: dict, api: dict, inventory: dict) -> list[dict]:
    expected = expected_groups(api, inventory)
    if data.get("schema_version") != 1:
        raise ValueError("unsupported evidence crosswalk schema")
    if data.get("locales") != ["pt", "en", "es", "fr"]:
        raise ValueError("target locale contract changed")
    if data.get("acceptance") != "PENDING_ITEM_PDF_ASSERTIONS_AND_HUMAN_REVIEW":
        raise ValueError("unproved complete internationalization claim")
    if set(data.get("entries", {})) != set(expected):
        raise ValueError("missing or unexpected API evidence group")
    catalog = data.get("sources")
    if not isinstance(catalog, list) or not catalog:
        raise ValueError("missing source manifest")
    registered: dict[str, dict] = {}
    for item in catalog:
        if set(item) != {"path", "suite", "scope"}:
            raise ValueError("unrecognized source manifest fields")
        source = item["path"]
        if (not isinstance(source, str)
                or not source.startswith("tests/")
                or ".." in Path(source).parts
                or Path(source).is_absolute()
                or source in registered):
            raise ValueError(f"invalid/duplicate evidence source {source}")
        if item["suite"] not in SOURCES or not item["scope"]:
            raise ValueError(f"unqualified source suite {source}")
        filepath = (ROOT / source).resolve()
        if not filepath.is_relative_to((ROOT / "tests").resolve()) or not filepath.is_file():
            raise ValueError(f"source outside existing test tree: {source}")
        registered[source] = {
            "suite": item["suite"],
            "sha256": hashlib.sha256(filepath.read_bytes()).hexdigest(),
            "text": filepath.read_text(encoding="utf-8"),
        }

    records = []
    for kind, identifiers in expected.items():
        actual = data["entries"][kind]
        if not isinstance(actual, dict) or set(actual) != identifiers:
            raise ValueError(f"canonical API drift in group {kind}")
        for identifier in sorted(identifiers):
            item = actual[identifier]
            if set(item) != {"candidate_test_file", "candidate_suite", "proof_state"}:
                raise ValueError(f"invalid evidence fields: {kind}/{identifier}")
            state = item["proof_state"]
            if state not in SOURCE_STATES:
                raise ValueError(f"invalid proof state/overclaimed success: {kind}/{identifier}")
            source = item["candidate_test_file"]
            if state == "UNMAPPED":
                if source is not None or item["candidate_suite"] != "none":
                    raise ValueError(f"unmapped name has invented source: {identifier}")
                digest = None
            else:
                if not isinstance(source, str) or source not in registered:
                    raise ValueError(f"unregistered source for {identifier}")
                data_source = registered[source]
                if item["candidate_suite"] != data_source["suite"]:
                    raise ValueError(f"wrong suite for {identifier}")
                # Match the complete public-name token; never accept a prefix
                # such as ufcPrintSummary inside ufcPrintSummaryInLanguage.
                token = identifier.removeprefix("\\")
                name = re.compile(r"(?<![A-Za-z])" + re.escape(token)
                                  + r"(?![A-Za-z])")
                if name.search(data_source["text"]) is None:
                    raise ValueError(f"public identifier absent from source: {identifier}")
                digest = data_source["sha256"]
            records.append({
                "group": kind, "identifier": identifier, "proof_state": state,
                "candidate_source": source, "source_suite": item["candidate_suite"],
                "candidate_source_sha256": digest,
                "independent_pdf_assertion": "NOT_CERTIFIED_PER_IDENTIFIER",
                "human_linguistic_review": "PENDING",
            })
    if len(records) != 72:
        raise ValueError(f"expected 72 public API rows; got {len(records)}")
    return records


def mutation_controls(data: dict, api: dict, inventory: dict) -> int:
    mutations = []
    def mutant():
        return copy.deepcopy(data)

    a = mutant()
    a["entries"]["public_commands"].pop(next(iter(a["entries"]["public_commands"])))
    mutations.append(a)
    a = mutant()
    a["entries"]["public_commands"]["\\ufcImaginary"] = {
        "candidate_test_file": None, "candidate_suite": "none", "proof_state": "UNMAPPED"}
    mutations.append(a)
    a = mutant()
    a["entries"]["setup_option_identifiers"]["type"]["proof_state"] = "CERTIFIED"
    mutations.append(a)
    a = mutant()
    a["entries"]["setup_option_identifiers"]["type"]["candidate_test_file"] = "tests/does-not-exist.tex"
    mutations.append(a)
    a = mutant()
    a["entries"]["public_environments"]["ufcobject"]["candidate_suite"] = "fixture"
    mutations.append(a)
    a = mutant()
    a["schema_version"] = 2
    mutations.append(a)
    a = mutant()
    a["sources"][0]["path"] = "../../etc/passwd"
    mutations.append(a)
    a = mutant()
    a["sources"].append(copy.deepcopy(a["sources"][0]))
    mutations.append(a)
    a = mutant()
    a["locales"] = ["pt", "en", "es"]
    mutations.append(a)

    for index, candidate in enumerate(mutations, start=1):
        try:
            validate(candidate, api, inventory)
        except ValueError:
            continue
        raise ValueError(f"negative crosswalk mutation accepted: {index}")
    return len(mutations)


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--report", action="store_true")
    args = parser.parse_args()
    api = json.loads(API_FILE.read_text(encoding="utf-8"))
    inventory = json.loads(I18N_FILE.read_text(encoding="utf-8"))
    data = json.loads(MAP_FILE.read_text(encoding="utf-8"))
    records = validate(data, api, inventory)
    negatives = mutation_controls(data, api, inventory)
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=ROOT,
                                  text=True).strip()
    expected = os.getenv("SOURCE_COMMIT_SHA")
    if expected and expected != sha:
        raise ValueError("CI checkout is not at requested exact source SHA")
    links = sum(row["proof_state"] == "SOURCE_REFERENCE_ONLY" for row in records)
    gaps = [row["identifier"] for row in records if row["proof_state"] == "UNMAPPED"]
    if args.report:
        OUTPUT.parent.mkdir(parents=True, exist_ok=True)
        OUTPUT.write_text(json.dumps({
            "source_sha": sha, "status": "SOURCE_LINKS_ONLY",
            "global_acceptance": data["acceptance"],
            "linked_identifiers": links, "unmapped_identifiers": gaps,
            "negative_controls": negatives, "records": records,
        }, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    print(f"I18N-EVIDENCE-CROSSWALK status=PASS source_sha={sha}"
          f" identifiers=72 linked={links} gaps={len(gaps)}"
          f" negative_controls={negatives} "
          f"per_identifier_pdf_certification=PENDING human_review=PENDING")


if __name__ == "__main__":
    try:
        main()
    except (OSError, KeyError, TypeError, ValueError,
            subprocess.CalledProcessError) as error:
        raise SystemExit(f"I18N-EVIDENCE-CROSSWALK status=FAIL reason={error}") from error
