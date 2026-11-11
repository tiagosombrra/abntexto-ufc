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
}
EXPECTED_PASS_ENV = {
    "ufclettereditems": "core-lists-12",
    "ufcdashedsubitems": "core-lists-12",
    "ufcdefinitionlist": "core-lists-12",
    "ufcobject": "optional-env-12",
    "ufclisting": "optional-env-12",
    "ufcalgorithm": "optional-env-12",
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
        if evidence["scope"] != "ONE_ISOLATED_PDF_PER_ENVIRONMENT_AND_LOCALE":
            raise ValueError("PDF proof no longer bounded by locale and environment")
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
            elif (result != "PENDING" or row["evidence_id"] is not None
                  or row["scope"] != "NOT_YET_CERTIFIED_PER_IDENTIFIER"):
                raise ValueError(f"unproven identifier promoted or wrongly classified: {name}")
    if counts != {"PASS": 6, "PENDING": 66, "NA": 0}:
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
    x["entries"]["public_commands"]["\\ufcsetup"]["result"] = "PASS"
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
        "proof_boundary": "Six public environments with four-locale PDF proof; other 66 identifiers pending individual evidence",
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
