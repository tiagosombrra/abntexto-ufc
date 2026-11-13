#!/usr/bin/env python3
"""Audit v3.1.0 candidate proof receipts without modifying historical certification.

Only the bounded functional evidence is audited. Human normative/visual and
linguistic acceptance and publication authorization stay explicitly pending.
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
import urllib.request
import zipfile

ROOT = Path(__file__).resolve().parents[2]
CANDIDATE = ROOT / "standards/api/i18n-v310-runtime-proof-candidate.json"
OLD = ROOT / "standards/api/i18n-per-identifier-proof-status.json"
PUBLIC = ROOT / "standards/api/public-api.json"
CROSS = ROOT / "standards/api/i18n-functional-evidence-crosswalk.json"
SOURCE_SHA = "9ab436da5027c4e20c305398bf89356b70bb17ad"
CLASS_BLOB = "299293e273dcefb80256eed2e17d2557db6aae52"
GROUPS = ("setup_option_identifiers", "public_commands",
          "public_environments", "retained_upstream_identifiers")
B4_INTEGRATED = {
    r"\ufcSource", r"\ufcNote", r"\ufcAddBibliographyResource",
    r"\ufcPrintReferences", r"\ufcPrintGlossary", r"\ufcPrintIndex",
    r"\legend", r"\appendix", r"\annex", r"\pretextual", r"\textual",
}
B4_ISOLATED = {r"\ufcInputListing", r"\keywords"}
B4_MINTED = {r"\ufcInputMinted"}
HASH = re.compile(r"^[0-9a-f]{64}$")


def require(value: bool, message: str) -> None:
    if not value:
        raise ValueError(message)


def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


def git(*args: str) -> str:
    return subprocess.check_output(["git", *args], cwd=ROOT, text=True).strip()


def load(path: Path) -> dict:
    return json.loads(path.read_text(encoding="utf-8"))


def identifier_sets(public: dict, cross: dict) -> dict[str, set[str]]:
    actual = {
        GROUPS[0]: set(cross["entries"][GROUPS[0]]),
        GROUPS[1]: set(public["public_commands"]["canonical"]),
        GROUPS[2]: set(public["public_environments"]["canonical"]),
        GROUPS[3]: set(public["upstream_boundary"]["retained_identifiers"]),
    }
    require(tuple(map(lambda g: len(actual[g]), GROUPS)) == (17, 43, 6, 6),
            "canonical inventory must contain 72 identifiers")
    return actual


def verify_registry(data: dict, old: dict, public: dict, cross: dict) -> dict:
    require(data["schema_version"] == 1
            and data["source_commit_sha"] == SOURCE_SHA
            and data["runtime_class_git_blob"] == CLASS_BLOB,
            "incorrect candidate evidence source or class")
    require(data["global_acceptance"] == "PENDING"
            and data["human_normative_linguistic_review"] == "PENDING"
            and data["publication_authorized"] is False
            and data["formal_new_runtime_ledger_promotion"] == "NOT_AUTHORIZED",
            "candidate evidence cannot grant acceptance or publication")
    require(old["same_runtime_blob"] != CLASS_BLOB
            and old["summary"] == {"PASS": 58, "PENDING": 14, "NA": 0},
            "original 58/72 ledger was overwritten or reclassified")
    require(set(data["entries"]) == set(GROUPS), "unexpected candidate groups")
    require(len(data["suites"]) == 13 and len(data["artifact_receipts"]) == 10,
            "missing suite or ZIP receipts")
    expected = identifier_sets(public, cross)
    old_pass = old_pending = 0
    suites_used = set()
    for group in GROUPS:
        rows = data["entries"][group]
        require(set(rows) == expected[group]
                and set(rows) == set(old["entries"][group])
                and set(rows) == set(cross["entries"][group]),
                f"missing or invented public identifier in {group}")
        for name, row in rows.items():
            original = old["entries"][group][name]
            require(row["candidate_functional_result"] == "BOUNDED_PDF_CANDIDATE_PASS"
                    and row["formal_new_runtime_result"] == "PENDING_FINAL_RECERTIFICATION"
                    and row["source_sha"] == SOURCE_SHA
                    and row["source_class_git_blob"] == CLASS_BLOB
                    and row["human_normative_linguistic_review"] == "PENDING",
                    f"unjustified promotion or wrong source: {group}/{name}")
            require(row["candidate_source"]
                    == cross["entries"][group][name]["candidate_test_file"]
                    and row["scope"] != "GLOBAL_ALL_PROFILES",
                    f"unsupported source or scope for {name}")
            suite = row["proof_suite"]
            if original["result"] == "PASS":
                old_pass += 1
                require(original["evidence_id"] == suite,
                        f"historical suite mapping changed: {name}")
            else:
                old_pending += 1
                require(original["result"] == "PENDING", "historical NA drift")
                expected_suite = (
                    "b4-integrated-11" if name in B4_INTEGRATED
                    else "b4-isolated-2" if name in B4_ISOLATED
                    else "b4-inputminted-1" if name in B4_MINTED else None
                )
                require(suite == expected_suite, f"B4 suite mapping invalid: {name}")
            require(suite in data["suites"], f"missing proof suite: {suite}")
            suites_used.add(suite)
    require((old_pass, old_pending) == (58, 14)
            and suites_used == set(data["suites"])
            and data["summary"]["bounded_functional_candidate_pass"] == 72
            and data["summary"]["formal_new_runtime_certified"] == 0
            and data["summary"]["formally_pending"] == 72,
            "candidate totals or 13-suite inventory drift")
    kinds = {"integrated": 0, "optional": 0, "auxiliary": 0}
    for name, record in data["artifact_receipts"].items():
        require(name.endswith(".zip") and Path(name).name == name,
                "invalid archive name")
        require(re.fullmatch(r"[0-9a-f]{64}", record["zip_sha256"]) is not None
                and record["run_id"] in (43427522352, 43427522327)
                and record["original_pdfs"] > 0
                and record["artifact_id"] > 100000,
                f"invalid original artifact reference: {name}")
        kinds[record["kind"]] += 1
    require(kinds == {"integrated": 4, "optional": 4, "auxiliary": 2},
            "incomplete original GitHub Actions archive sources")
    for name, suite in data["suites"].items():
        require(suite["source_sha"] == SOURCE_SHA
                and suite["source_class_git_blob"] == CLASS_BLOB
                and (ROOT / suite["runner"]).is_file()
                and suite["qualification"] == "CANDIDATE_ORIGINAL_BYTE_AUDIT_ONLY",
                f"unqualified source-bound suite: {name}")
        paths = suite["artifact_files"]
        require(len(paths) == (2 if name == "b1-auxiliary-2" else 4)
                and len(set(paths)) == len(paths)
                and all(n in data["artifact_receipts"] for n in paths),
                f"unbound archive evidence for {name}")
    return {"identifiers": 72, "historical_pass": old_pass,
            "historical_pending": old_pending, "suites": len(suites_used)}


def references(obj: object):
    if isinstance(obj, dict):
        for key, value in obj.items():
            if "sha256" in key.lower() and isinstance(value, str) and HASH.fullmatch(value):
                yield value
            else:
                yield from references(value)
    elif isinstance(obj, list):
        for item in obj:
            yield from references(item)


def check_proofs(name: str, manifests: dict) -> None:
    if name.startswith("requal-") and not name.startswith("requal-b1-"):
        for key in ("b1-family-proof.json", "b2-family-proof.json",
                    "b3-integrated-list-proof.json",
                    "b4-integrated-backmatter-proof.json",
                    "b4-isolated/manifest.json",
                    "b1-final-five/manifest.json",
                    "core-list-environments/manifest.json",
                    "optional-environments/manifest.json"):
            require(key in manifests, f"missing original proof {name}/{key}")
        a = manifests["b4-integrated-backmatter-proof.json"]
        b = manifests["b4-isolated/manifest.json"]
        require(len(a["identifiers"]) == 11 and a["positive_observations"] == 62
                and a["runtime_negative_mutations"] == 85
                and a["negative_controls"] == 15,
                "integrated B4 coverage drift")
        require(len(b["identifiers"]) == 2 and b["negative_controls"] == 18,
                "isolated B4 coverage drift")
        require(manifests["b2-family-proof.json"]["individual_candidate_commands"] == 16
                and manifests["b1-family-proof.json"]["candidate_count"] == 15,
                "B1/B2 scope drift")
    elif name.startswith("optional-"):
        locale = name.split("-")[1]
        prefix = "optional-i18n/" + locale + "/"
        for short in ("b1-optional-config-proof.json",
                      "b3-optional-list-proof.json", "b4-inputminted-proof.json"):
            require(prefix + short in manifests, f"missing original optional {short}")
        b = manifests[prefix + "b4-inputminted-proof.json"]
        require(b["identifier"] == r"\ufcInputMinted" and b["positive"] == 1
                and b["negative_controls"] == 9
                and len(b["records"]) == 3,
                "B4 Minted candidate controls drift")
        fixture = manifests[f"inputlisting-container-repro/runtime-{locale}/runtime-manifest.json"]
        require(fixture["cases"] == 16 and fixture["runtime_class_modified"] is True
                and all(x["valid_pdf_and_text"] for x in fixture["observations"]),
                "nested external listings regression")
    elif name.startswith("requal-b1-"):
        require(manifests["b1-auxiliary-proof.json"]["negative_controls"] == 4,
                "B1 auxiliary negative controls drift")


def audit_zip(path: Path, metadata: dict) -> dict:
    require(path.is_file(), f"original ZIP not downloaded: {path.name}")
    raw = path.read_bytes()
    require(sha256(raw) == metadata["zip_sha256"],
            f"original GitHub artifact ZIP SHA256 mismatch: {path.name}")
    with zipfile.ZipFile(path) as archive:
        filenames = [n for n in archive.namelist() if not n.endswith("/")]
        require(len(filenames) == len(set(filenames))
                and all(not n.startswith("/") and ".." not in Path(n).parts
                        for n in filenames), "duplicate or unsafe original ZIP path")
        require(archive.testzip() is None, f"corrupt original ZIP {path.name}")
        hashes = {}
        manifests = {}
        pdf_names = []
        for fname in filenames:
            raw = archive.read(fname)
            hashes.setdefault(sha256(raw), []).append(fname)
            if fname.endswith(".pdf"):
                require(raw.startswith(b"%PDF-") and b"%%EOF" in raw[-1024:],
                        f"invalid original PDF header/trailer: {fname}")
                pdf_names.append(fname)
            if fname.endswith(".json"):
                item = json.loads(raw)
                manifests[fname] = item
                if isinstance(item, dict):
                    for key in ("source_sha", "source_commit_sha"):
                        if key in item:
                            require(item[key] == SOURCE_SHA,
                                    f"wrong PDF evidence source {fname}/{key}")
                    if "publication_authorized" in item:
                        require(item["publication_authorized"] is False,
                                f"unauthorized release status in {fname}")
        require(len(pdf_names) == metadata["original_pdfs"],
                f"missing or extra PDFs in {path.name}")
        refs = [h for item in manifests.values() for h in references(item)]
        require(len(refs) >= 20
                and all(h in hashes for h in refs),
                f"SHA256 receipt does not match original archive bytes: {path.name}")
        require(all(sha256(archive.read(n)) in refs for n in pdf_names),
                f"unreferenced PDF bytes in original ZIP: {path.name}")
        check_proofs(path.name, manifests)
        return {"artifact_id": metadata["artifact_id"],
                "original_zip_sha256": metadata["zip_sha256"],
                "pdfs": len(pdf_names), "sha256_references_verified": len(refs),
                "status": "ORIGINAL_ZIP_BYTES_VERIFIED"}


def download_archive(name: str, metadata: dict, dest: Path, token: str) -> None:
    require(bool(token), "GitHub Actions token required to fetch original evidence")
    repo = os.getenv("GITHUB_REPOSITORY", "")
    require(repo == "tiagosombrra/abntexto-ufc", "unexpected evidence repository")
    url = f"https://api.github.com/repos/{repo}/actions/artifacts/{metadata['artifact_id']}"
    headers = {"Authorization": f"Bearer {token}",
               "Accept": "application/vnd.github+json",
               "X-GitHub-Api-Version": "2022-11-28"}
    with urllib.request.urlopen(urllib.request.Request(url, headers=headers)) as response:
        record = json.load(response)
    require(record["id"] == metadata["artifact_id"]
            and record["workflow_run"]["id"] == metadata["run_id"]
            and record["workflow_run"]["head_sha"] == SOURCE_SHA
            and record["digest"] == "sha256:" + metadata["zip_sha256"]
            and not record["expired"], f"incorrect or expired GitHub artifact {name}")
    # GitHub redirects the ZIP endpoint to an expiring, signed content URL.
    with urllib.request.urlopen(urllib.request.Request(url + "/zip", headers=headers)) as stream:
        dest.write_bytes(stream.read())


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--archives", type=Path)
    parser.add_argument("--download", action="store_true")
    parser.add_argument("--skip-git", action="store_true")
    parser.add_argument("--report", type=Path)
    parser.add_argument("--self-test", action="store_true")
    args = parser.parse_args()
    data, old, public, cross = map(load, (CANDIDATE, OLD, PUBLIC, CROSS))
    summary = verify_registry(data, old, public, cross)
    if not args.skip_git:
        require(git("hash-object", "abntexto-ufc.cls") == CLASS_BLOB,
                "candidate HEAD changed the evidenced runtime")
        require(git("rev-parse", SOURCE_SHA + ":abntexto-ufc.cls") == CLASS_BLOB,
                "evidence source class blob cannot be verified")
    if args.self_test:
        mutants = []
        for key, value in (("publication_authorized", True),
                           ("runtime_class_git_blob", "0" * 40)):
            candidate = copy.deepcopy(data)
            candidate[key] = value
            mutants.append(candidate)
        candidate = copy.deepcopy(data)
        candidate["entries"]["public_commands"][r"\ufcInputListing"]["proof_suite"] = "b2-family-12"
        mutants.append(candidate)
        candidate = copy.deepcopy(data)
        candidate["entries"]["public_commands"][r"\ufcInputMinted"]["formal_new_runtime_result"] = "PASS"
        mutants.append(candidate)
        for mutant in mutants:
            try:
                verify_registry(mutant, old, public, cross)
            except ValueError:
                continue
            raise ValueError("ledger mutation bypassed a fail-closed contract")
        print("V310-LEDGER-PREFLIGHT status=PASS identifiers=72 mutants=4 publication_authorized=false")
    output = {}
    if args.archives:
        args.archives.mkdir(parents=True, exist_ok=True)
        for name, metadata in data["artifact_receipts"].items():
            path = args.archives / name
            if args.download:
                download_archive(name, metadata, path, os.environ.get("GH_TOKEN", ""))
            output[name] = audit_zip(path, metadata)
            print(f"V310-ARCHIVE status=PASS artifact={metadata['artifact_id']} pdfs={output[name]['pdfs']}",
                  flush=True)
        require(len(output) == 10 and sum(x["pdfs"] for x in output.values()) == 310
                and sum(x["sha256_references_verified"] for x in output.values()) == 4952,
                "original evidence byte-audit totals drift")
        print("V310-ARCHIVE-LEDGER status=PASS archives=10 pdfs=310 hashes=4952"
              " candidate_identifiers=72 formal_certification=PENDING publication=false", flush=True)
    report = {"source_commit_sha": SOURCE_SHA, "runtime_class_git_blob": CLASS_BLOB,
              "candidate_identifiers": summary["identifiers"],
              "historical_only_pass": summary["historical_pass"],
              "historical_only_pending": summary["historical_pending"],
              "source_bound_suites": summary["suites"], "archives": output,
              "global_acceptance": "PENDING", "human_review": "PENDING",
              "publication_authorized": False,
              "formal_runtime_certification": "PENDING_REVIEW"}
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                               encoding="utf-8")


if __name__ == "__main__":
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.CalledProcessError,
            zipfile.BadZipFile, json.JSONDecodeError) as error:
        raise SystemExit(f"V310-ARCHIVE-LEDGER status=FAIL reason={error}") from error
