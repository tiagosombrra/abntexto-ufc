#!/usr/bin/env python3
"""Requalify 72 named APIs against unchanged, source-bound candidate PDF artifacts.

This ledger is bounded technical evidence, not human, normative or release approval.
The original 58/72 and corrected-runtime 72/72 ledgers remain immutable.
"""
from __future__ import annotations

import argparse
import copy
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
SOURCE_SHA = "b5393f94af996ee978144eb7ba95f21140924400"
CLASS_BLOB = "4f3b266e8fce9204577565961d35c3066fd59cee"
REPO = "tiagosombrra/abntexto-ufc"
GROUP_COUNTS = {
    "setup_option_identifiers": 17, "public_commands": 43,
    "public_environments": 6, "retained_upstream_identifiers": 6,
}
# Artifacts belong to two real workflows at the same exact candidate class SHA.
ARTIFACTS = {
    "pt": (14831103054, 45200284116, "69d61005f4d406d673e9798552b43f685fa1fab7beb0d8135d004e1c328e546f"),
    "en": (14829969507, 45200284116, "06cf542a8fe6f62eb5500772b63679a680ebe68d81652b8eb3d32731a067aa17"),
    "es": (14830887131, 45200284116, "8b405fec866b19f33c1a160d25a8b9462df253b116d5bd0331c1019d98ce60dc"),
    "fr": (14830469132, 45200284116, "e9997f246c58eee49c74ba277cc233ac9bc5f2cfcd9aaf5fb6584496bcd097fb"),
    "dual": (14830414084, 45200284116, "2418ca4f5157b295d3989e2ec5f5ba790118345840d6799b7e3877a44b1428e4"),
    "coat": (14830339251, 45200284116, "47439faabc23f134db4cea728bb07592e2ada8949cd3a5a35d18d1959ecd84d0"),
    "opt-pt": (14832158097, 45200285066, "f497d6076385c123fc172847a15c84d0a5d02c615c12de5ee4f28f0c56341b9d"),
    "opt-en": (14831527215, 45200285066, "f38b1a1f0f6faec8d565fb8c0d121a84b137c2624e0a43ceeb3350a7674d0850"),
    "opt-es": (14830887113, 45200285066, "3b8d60ecb130412afbeee8f0382ac793269365b6f1b49fad5552f01a4863954b"),
    "opt-fr": (14832760001, 45200285066, "b9b5df541877993342a90306a609f09ecbcfed2e55857eeb30a61170e7ac5755"),
}
PROOFS = {
    "b1-integrated-15": "b1-family-proof.json",
    "b1-auxiliary-2": "b1-auxiliary-proof.json",
    "b1-final-five": "b1-final-five/manifest.json",
    "b1-optional-config-3": "b1-optional-config-proof.json",
    "b2-family-12": "b2-family-proof.json",
    "b2-summary-remaining": "b2-summary-remaining/manifest.json",
    "b3-integrated-9": "b3-integrated-list-proof.json",
    "b3-optional-2": "b3-optional-list-proof.json",
    "b4-integrated-11": "b4-integrated-backmatter-proof.json",
    "b4-isolated-2": "b4-isolated/manifest.json",
    "b4-inputminted-1": "b4-inputminted-proof.json",
    "core-lists-12": "core-list-environments/manifest.json",
    "optional-env-12": "optional-environments/manifest.json",
}
OPTIONAL = {"b1-optional-config-3", "b3-optional-2", "b4-inputminted-1"}


def require(ok: bool, message: str) -> None:
    if not ok:
        raise ValueError(message)


def digest(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def original_sources_unchanged() -> None:
    require(git("hash-object", "abntexto-ufc.cls") == CLASS_BLOB,
            "Current runtime does not match issue 598 evidenced class")
    require(git("rev-parse", "HEAD:abntexto-ufc.cls") == CLASS_BLOB,
            "Working tree/class commit mismatch")
    require(subprocess.run(["git", "merge-base", "--is-ancestor", SOURCE_SHA, "HEAD"],
                           cwd=ROOT, capture_output=True).returncode == 0,
            "Evidence-producing commit is not an ancestor of this candidate")
    historical = (
        "standards/api/i18n-per-identifier-proof-status.json",
        "standards/api/i18n-v310-runtime-proof-candidate.json",
        "standards/api/i18n-v310-bounded-functional-qualified.json",
        "standards/api/public-api.json",
        "standards/api/i18n-functional-evidence-crosswalk.json",
    )
    for path in historical:
        require(git("rev-parse", "HEAD:" + path) ==
                git("rev-parse", SOURCE_SHA + ":" + path),
                "Historical registry/API was changed: " + path)


def github_get(url: str, token: str) -> bytes:
    require(url.startswith("https://api.github.com/repos/" + REPO + "/actions/artifacts/"),
            "Only pinned GitHub artifact endpoints are permitted")
    request = urllib.request.Request(url, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=120) as response:
        require(int(response.headers.get("Content-Length", "0")) < 35000000,
                "Oversized remote artifact")
        data = response.read(35000001)
    require(len(data) <= 35000000, "Remote artifact exceeds byte limit")
    return data


def download_archives(directory: Path) -> None:
    token = os.environ.get("GH_TOKEN", "")
    require(bool(token), "GH_TOKEN is required to download authenticated artifacts")
    directory.mkdir(parents=True, exist_ok=True)
    for key, (artifact_id, run_id, expected_hash) in ARTIFACTS.items():
        root = f"https://api.github.com/repos/{REPO}/actions/artifacts/{artifact_id}"
        metadata = json.loads(github_get(root, token))
        require(metadata["id"] == artifact_id and
                metadata["workflow_run"]["id"] == run_id and
                metadata["workflow_run"]["head_sha"] == SOURCE_SHA and
                metadata["digest"] == "sha256:" + expected_hash and
                metadata["expired"] is False,
                "Remote artifact identity/provenance mismatch: " + key)
        data = github_get(root + "/zip", token)
        require(digest(data) == expected_hash, "ZIP bytes differ: " + key)
        (directory / (key + ".zip")).write_bytes(data)


class Artifact:
    def __init__(self, key: str, directory: Path) -> None:
        self.key = key
        self.id, self.run_id, self.expected_hash = ARTIFACTS[key]
        data = (directory / (key + ".zip")).read_bytes()
        require(digest(data) == self.expected_hash, "Bad artifact ZIP digest: " + key)
        self.archive = zipfile.ZipFile(directory / (key + ".zip"))
        require(self.archive.testzip() is None, "Bad ZIP CRC: " + key)
        names = self.archive.namelist()
        require(len(names) <= 1800, "Unexpected number of ZIP members")
        require(sum(x.file_size for x in self.archive.infolist()) < 135000000,
                "ZIP uncompressed size exceeds bound")
        for name in names:
            parts = PurePosixPath(name).parts
            require(not name.startswith("/") and ".." not in parts and
                    "\\" not in name, "Unsafe ZIP path: " + name)
        self.names = names
        self.by_hash: dict[str, list[str]] = {}
        for name in names:
            if name.endswith((".tex", ".pdf", ".log")):
                value = digest(self.archive.read(name))
                self.by_hash.setdefault(value, []).append(name)

    def member(self, value: str, suffix: str) -> str | None:
        return next((s for s in self.by_hash.get(value, []) if s.endswith(suffix)), None)

    def proof(self, path: str) -> tuple[str, str, dict]:
        found = [s for s in self.names if s == path or s.endswith("/" + path)]
        require(len(found) == 1, f"{self.key}: expected exactly one proof: {path}")
        value = self.archive.read(found[0])
        data = json.loads(value)
        require(data["source_sha"] == SOURCE_SHA,
                f"{self.key}: proof source differs from candidate")
        return found[0], digest(value), data


def positive_pair(value: object) -> tuple[str, str, dict] | None:
    if isinstance(value, list):
        for row in value:
            matched = positive_pair(row)
            if matched:
                return matched
    elif isinstance(value, dict):
        if value.get("verified", True) is not False:
            pdf = value.get("pdf_sha256") or value.get("enabled_pdf_sha256")
            tex = (value.get("source_sha256") or value.get("tex_sha256") or
                   value.get("enabled_source_sha256"))
            if isinstance(pdf, str) and isinstance(tex, str) and re.fullmatch(
                    "[0-9a-f]{64}", pdf) and re.fullmatch("[0-9a-f]{64}", tex):
                return pdf, tex, value
        for name, nested in value.items():
            if name not in {"disabled", "negative", "negative_control", "not_exercised"}:
                if isinstance(nested, (dict, list)):
                    matched = positive_pair(nested)
                    if matched:
                        return matched
    return None


def scoped_row(suite: str, data: dict, name: str) -> object | None:
    if suite == "b1-integrated-15":
        return data["records"][0] if name in data["candidate_identifiers"] else None
    if suite == "b1-auxiliary-2":
        return data["proof"]["record_checks"] if name == data["proof"]["identifier"] else None
    if suite == "b1-final-five":
        return data["certified_evidence"].get(name)
    if suite == "b1-optional-config-3":
        return next((r for r in data["observations"] if
                     r["identifier"] == name and r["verified"]), None)
    if suite == "b2-family-12":
        return next((r for r in data["observations"] if
                     r["identifier"] == name and r.get("verified")), None)
    if suite == "b2-summary-remaining":
        return next((r for r in data["records"] if name in r["commands"] and
                     r.get("verified")), None)
    if suite in {"b3-integrated-9", "b3-optional-2"}:
        return next((r for r in data["records"] if any(
            o["identifier"] == name and
            (o.get("applicability") == "BOUNDED_REAL_PDF_PASS" or
             o.get("status") == "BOUNDED_REAL_PDF_PASS")
            for o in r["observations"])), None)
    if suite == "b4-integrated-11":
        return next((r for r in data["receipts"] if any(
            o["identifier"] == name and o.get("status") == "BOUNDED_REAL_PDF_PASS"
            for o in r["observations"])), None)
    if suite == "b4-isolated-2":
        return next((r for r in data["records"] if r["identifier"] == name and
                     r["status"] == "BOUNDED_ISOLATED_REAL_PDF_PASS"), None)
    if suite == "b4-inputminted-1":
        return next((r for r in data["records"] if
                     r["observation"]["identifier"] == name and
                     r["observation"]["status"] == "BOUNDED_REAL_PDF_PASS"), None)
    if suite in {"core-lists-12", "optional-env-12"}:
        return next((r for r in data["records"] if r["environment"] == name and
                     r["verified"]), None)
    raise ValueError("Unrecognized proof family: " + suite)


def scoped_receipt(suite: str, name: str, archives: dict[str, Artifact]) -> dict:
    if name == "labels-language":
        keys = ("dual",)
    elif name == "coat-of-arms":
        keys = ("coat",)
    elif suite in OPTIONAL:
        keys = tuple("opt-" + x for x in ("pt", "en", "es", "fr"))
    else:
        keys = ("pt", "en", "es", "fr")
    for key in keys:
        artifact = archives[key]
        member, proof_hash, data = artifact.proof(PROOFS[suite])
        row = scoped_row(suite, data, name)
        if row is None:
            continue
        pair = positive_pair(row)
        kind = "BOUNDED_REAL_PDF_PASS"
        log_member = None
        log_hash = None
        if name == "strict-font":
            trials = data["certified_evidence"]["strict-font"]
            negative = next((x for x in trials if x.get("verified") and
                             artifact.member(x.get("source_sha256", ""), ".tex") and
                             artifact.member(x.get("log_sha256", ""), ".log")), None)
            pair = positive_pair(data["certified_evidence"]["font"])
            require(negative is not None and pair is not None,
                    "Strict-font expected rejection evidence missing")
            kind = "EXPECTED_REJECTION_PLUS_ADJACENT_POSITIVE_PDF"
            pdf, _, observation = pair
            source_hash = negative["source_sha256"]
            log_hash = negative["log_sha256"]
            log_member = artifact.member(log_hash, ".log")
        elif pair is not None:
            pdf, source_hash, observation = pair
        else:
            continue
        pdf_member = artifact.member(pdf, ".pdf")
        source_member = artifact.member(source_hash, ".tex")
        if not pdf_member or not source_member:
            continue
        negative_controls = data.get(
            "negative_controls", data.get(
                "negatives", data.get("proof", {}).get("negative_controls_from_producer")))
        require(isinstance(negative_controls, int) and negative_controls > 0,
                "Missing negative controls for " + suite)
        receipt = {
            "artifact_id": artifact.id, "workflow_run_id": artifact.run_id,
            "artifact_zip_sha256": artifact.expected_hash,
            "archive_locale": key, "proof_json_member": member,
            "proof_json_sha256": proof_hash, "scenario": (
                observation.get("scenario") or observation.get("profile") or
                observation.get("job") or observation.get("filename") or suite),
            "tex_member": source_member, "tex_sha256": source_hash,
            "pdf_member": pdf_member, "pdf_sha256": pdf,
            "negative_controls": negative_controls, "evidence_kind": kind,
        }
        if log_member is not None:
            receipt["log_member"] = log_member
            receipt["log_sha256"] = log_hash
        return receipt
    raise ValueError("No positive scoped source/PDF evidence: " + suite + " / " + name)


def canonical_groups(candidate: dict, public: dict, crosswalk: dict) -> dict:
    # The 17 configuration identifiers are a subset of canonical setup keys.
    core = {value for group in public["setup_keys"].values() for value in group}
    expected = {
        "setup_option_identifiers": set(candidate["entries"]["setup_option_identifiers"]),
        "public_commands": set(public["public_commands"]["canonical"]),
        "public_environments": set(public["public_environments"]["canonical"]),
        "retained_upstream_identifiers": set(
            public["upstream_boundary"]["retained_identifiers"]),
    }
    require(expected["setup_option_identifiers"] <= core,
            "Named setup options do not belong to public API")
    for group, names in expected.items():
        require(len(names) == GROUP_COUNTS[group] and
                names == set(candidate["entries"][group]) and
                names == set(crosswalk["entries"][group]),
                "Canonical group drift: " + group)
    return expected


def build(archives: dict[str, Artifact]) -> dict:
    candidate = json.loads((ROOT / "standards/api/i18n-v310-runtime-proof-candidate.json").read_text())
    public = json.loads((ROOT / "standards/api/public-api.json").read_text())
    crosswalk = json.loads((ROOT / "standards/api/i18n-functional-evidence-crosswalk.json").read_text())
    groups = canonical_groups(candidate, public, crosswalk)
    entries = {}
    for group, names in groups.items():
        for name in sorted(names):
            original = candidate["entries"][group][name]
            suite = original["proof_suite"]
            require(suite in PROOFS and
                    original["candidate_functional_result"] == "BOUNDED_PDF_CANDIDATE_PASS",
                    "Unknown/unsupported original proof family")
            entries[f"{group}/{name}"] = {
                "identifier": name, "group": group, "family": suite,
                "scoped_evidence_state": "BOUNDED_CURRENT_RUNTIME_PDF_PASS",
                "formal_human_review": "PENDING",
                "formal_runtime_promotion": "NOT_AUTHORIZED",
                "evidence": scoped_receipt(suite, name, archives),
            }
    return {
        "schema_version": 1, "issue": 624, "pr": 623,
        "scope": "CURRENT_RUNTIME_BOUNDED_PDF_EVIDENCE_ONLY",
        "evidence_source_sha": SOURCE_SHA, "class_git_blob": CLASS_BLOB,
        "archives": {str(value.id): {
            "workflow_run_id": value.run_id, "zip_sha256": value.expected_hash,
        } for value in archives.values()},
        "summary": {"bounded_named_identifier_pass": len(entries),
                    "families": len(set(x["family"] for x in entries.values())),
                    "human_acceptances": 0, "formal_release_authorizations": 0},
        "historical_ledger_mutated": False,
        "global_internationalization_acceptance": "PENDING",
        "human_normative_linguistic_review": "PENDING",
        "editorial_visual_acceptance": "PENDING",
        "publication_authorized": False,
        "release_candidate_state": "UNRELEASED",
        "entries": entries,
    }


def verify_report(report: dict, archives: dict[str, Artifact]) -> None:
    require(report["evidence_source_sha"] == SOURCE_SHA and
            report["class_git_blob"] == CLASS_BLOB, "Invalid candidate identity")
    require(report["summary"] == {
        "bounded_named_identifier_pass": 72, "families": 13,
        "human_acceptances": 0, "formal_release_authorizations": 0,
    }, "Unjustified completion/status/count")
    require(report["historical_ledger_mutated"] is False and
            report["publication_authorized"] is False and
            report["human_normative_linguistic_review"] == "PENDING" and
            report["editorial_visual_acceptance"] == "PENDING" and
            report["global_internationalization_acceptance"] == "PENDING" and
            report["release_candidate_state"] == "UNRELEASED",
            "Forbidden release/human approval promotion")
    expected_ids = set(build(archives)["entries"])
    require(set(report["entries"]) == expected_ids and len(expected_ids) == 72,
            "Missing, duplicated or invented API identifier")
    for key, row in report["entries"].items():
        archive = archives[row["evidence"]["archive_locale"]]
        receipt = row["evidence"]
        require(row["family"] == build_family_for_id(key) and
                row["scoped_evidence_state"] == "BOUNDED_CURRENT_RUNTIME_PDF_PASS" and
                row["formal_human_review"] == "PENDING" and
                row["formal_runtime_promotion"] == "NOT_AUTHORIZED",
                "Invalid per-ID status or proof family: " + key)
        require(receipt["artifact_id"] == archive.id and
                receipt["workflow_run_id"] == archive.run_id and
                receipt["artifact_zip_sha256"] == archive.expected_hash,
                "Altered artifact identity: " + key)
        for path, hash_key in (
            ("proof_json_member", "proof_json_sha256"),
            ("pdf_member", "pdf_sha256"),
            ("tex_member", "tex_sha256"),
        ):
            value = receipt[path]
            require(value in archive.names and
                    digest(archive.archive.read(value)) == receipt[hash_key],
                    "Missing or altered artifact member: " + key + " / " + path)
        if receipt["evidence_kind"] == "EXPECTED_REJECTION_PLUS_ADJACENT_POSITIVE_PDF":
            require(row["identifier"] == "strict-font" and
                    receipt["log_member"] in archive.names and
                    digest(archive.archive.read(receipt["log_member"])) ==
                    receipt["log_sha256"], "Expected rejection log absent")
        else:
            require(receipt["evidence_kind"] == "BOUNDED_REAL_PDF_PASS",
                    "Unsupported proof classification")
        require(receipt["negative_controls"] > 0, "Negative controls absent")
        suite = row["family"]
        proof = archive.proof(PROOFS[suite])[2]
        require(scoped_row(suite, proof, row["identifier"]) is not None,
                "Identifier absent from its proof manifest")
    require(len(report["archives"]) == 10 and
            set(report["archives"]) == {str(a.id) for a in archives.values()},
            "Wrong archive manifest")


def build_family_for_id(key: str) -> str:
    # The original candidate registry provides the authoritative per-ID family.
    group, identifier = key.split("/", 1)
    data = json.loads((ROOT / "standards/api/i18n-v310-runtime-proof-candidate.json").read_text())
    return data["entries"][group][identifier]["proof_suite"]


def mutation_tests(report: dict, archives: dict[str, Artifact]) -> int:
    first = next(iter(report["entries"]))
    mutants = []
    def mutate(action):
        altered = copy.deepcopy(report)
        action(altered)
        mutants.append(altered)
    mutate(lambda x: x["entries"].pop(first))
    mutate(lambda x: x["entries"][first]["evidence"].update(pdf_sha256="0" * 64))
    mutate(lambda x: x["entries"][first]["evidence"].update(artifact_id=1))
    mutate(lambda x: x["entries"][first]["evidence"].update(proof_json_sha256="0" * 64))
    mutate(lambda x: x.update(class_git_blob="0" * 40))
    mutate(lambda x: x.update(publication_authorized=True))
    mutate(lambda x: x["entries"][first].update(formal_runtime_promotion="PASS"))
    mutate(lambda x: x["summary"].update(bounded_named_identifier_pass=71))
    for mutant in mutants:
        try:
            verify_report(mutant, archives)
        except (KeyError, ValueError, TypeError):
            continue
        raise ValueError("Mutation bypassed current-runtime fail-closed audit")
    return len(mutants)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--archives", type=Path, required=True)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--report", type=Path,
                        default=Path("artifacts/issue624/current-runtime-72.json"))
    args = parser.parse_args()
    original_sources_unchanged()
    if args.download:
        download_archives(args.archives)
    archives = {name: Artifact(name, args.archives) for name in ARTIFACTS}
    report = build(archives)
    verify_report(report, archives)
    mutants = mutation_tests(report, archives) if args.self_test else 0
    report["self_test_negative_mutations"] = mutants
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, sort_keys=True, ensure_ascii=False, indent=2)
                           + "\n", encoding="utf-8")
    print("ISSUE624-BOUND-CANDIDATE-EVIDENCE status=PASS"
          f" source_sha={SOURCE_SHA} class_blob={CLASS_BLOB}"
          f" ids=72 families=13 artifacts=10 mutants={mutants}"
          " formal_human=PENDING publication_authorized=false", flush=True)


if __name__ == "__main__":
    main()
