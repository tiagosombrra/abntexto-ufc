#!/usr/bin/env python3
"""Audit freshly generated 72-ID evidence in one current-class CI run.

No artifact ID or expiring archived ZIP is required for this permanent gate.
Human, normative and publication decisions remain explicitly pending.
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
import sys
import urllib.request

# Support direct CLI execution and package imports from repository CI preflights.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from requalify_current_runtime_72 import (
    CLASS_BLOB, GROUP_COUNTS, OPTIONAL, PROOFS,
    canonical_groups, git, positive_pair, require, scoped_row,
)

ROOT = Path(__file__).resolve().parents[2]
LOCALES = ("pt", "en", "es", "fr")
AUX = ("dual", "coat")
EVIDENCE_KEYS = (*LOCALES, *(f"opt-{locale}" for locale in LOCALES), *AUX)
EXPECTED_IDS = sum(GROUP_COUNTS.values())
# A squash merge need not retain the producer PR commit in the final ancestry.
# Pin actual Git blobs, not the ancestry or expiration of producer artifacts.
IMMUTABLE_API_BLOBS = {
    "standards/api/i18n-per-identifier-proof-status.json":
        "4cb998e9210b3cfadfa0ca6d29922fa218f32d74",
    "standards/api/i18n-v310-runtime-proof-candidate.json":
        "84f8af1fed88d93464275dc8475c9691e2b31046",
    "standards/api/i18n-v310-bounded-functional-qualified.json":
        "f47dce18aa7cfa3ba0056b08df9cc0ddf460af19",
    "standards/api/public-api.json":
        "1d32b3ea0ccfd1ff5e73e372a9b0479f94173787",
    "standards/api/i18n-functional-evidence-crosswalk.json":
        "614cd1579f92b65a6f632c3642f49f88f955c752",
}


def verify_current_class_scope() -> None:
    """Require exact reviewed runtime/API bytes even after a protected squash merge."""
    protected = {"abntexto-ufc.cls": CLASS_BLOB, **IMMUTABLE_API_BLOBS}
    for path, expected_blob in protected.items():
        require(git("rev-parse", "HEAD:" + path) == expected_blob and
                git("hash-object", path) == expected_blob,
                "Source-bound runtime/API Git blob changed: " + path)



def sha256(value: bytes) -> str:
    return hashlib.sha256(value).hexdigest()


class CurrentArtifact:
    """Original file bytes from a single run's downloaded producer artifact."""

    def __init__(self, key: str, root: Path, metadata: dict, source_sha: str) -> None:
        self.key = key
        self.name = metadata["name"]
        self.artifact_id = metadata["id"]
        self.zip_digest = metadata["digest"]
        self.root = root / self.name
        require(self.root.is_dir(), "Missing current-run evidence: " + self.name)
        self.files = {}
        self.by_hash: dict[str, list[str]] = {}
        for path in self.root.rglob("*"):
            if not path.is_file():
                continue
            resolved = path.resolve()
            require(self.root.resolve() in resolved.parents,
                    "Unsafe artifact member path")
            relative = path.relative_to(self.root).as_posix()
            require(relative not in self.files, "Duplicate artifact member")
            self.files[relative] = path
            if path.suffix in {".pdf", ".tex", ".log"}:
                self.by_hash.setdefault(sha256(path.read_bytes()), []).append(relative)
        require(self.files, "Empty current-run evidence: " + key)
        self.source_sha = source_sha

    def member(self, source_hash: str, suffix: str) -> str | None:
        return next((p for p in self.by_hash.get(source_hash, [])
                     if p.endswith(suffix)), None)

    def proof(self, path: str) -> tuple[str, str, dict]:
        found = [name for name in self.files
                 if name == path or name.endswith("/" + path)]
        require(len(found) == 1, self.key + ": expected one proof: " + path)
        value = self.files[found[0]].read_bytes()
        parsed = json.loads(value)
        require(parsed.get("source_sha") == self.source_sha,
                "Stale source in " + self.key + ": " + path)
        return found[0], sha256(value), parsed


def artifacts_from_current_run(root: Path, run_id: str, source_sha: str,
                               token: str) -> dict[str, CurrentArtifact]:
    require(token, "GH_TOKEN is required for current-run artifact metadata")
    require(re.fullmatch(r"[0-9]+", run_id) is not None, "Invalid run ID")
    from requalify_current_runtime_72 import REPO
    endpoint = (f"https://api.github.com/repos/{REPO}/actions/runs/"
                f"{run_id}/artifacts?per_page=100")
    request = urllib.request.Request(endpoint, headers={
        "Authorization": "Bearer " + token,
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
    })
    with urllib.request.urlopen(request, timeout=45) as response:
        metadata = json.load(response)["artifacts"]
    prefix = {
        **{loc: "issue624-full-integrated-" + loc for loc in LOCALES},
        **{"opt-" + loc: "issue624-live-optional-" + loc for loc in LOCALES},
        **{suite: "issue624-live-aux-" + suite for suite in AUX},
    }
    expected = {key: f"{name}-{run_id}" for key, name in prefix.items()}
    found = {}
    for entry in metadata:
        if entry["name"] not in expected.values():
            continue
        key = next(k for k, name in expected.items() if name == entry["name"])
        require(key not in found and entry["expired"] is False and
                entry["workflow_run"]["id"] == int(run_id) and
                entry["workflow_run"]["head_sha"] == source_sha and
                re.fullmatch(r"sha256:[0-9a-f]{64}", entry["digest"]) is not None,
                "Invalid current-run artifact metadata: " + key)
        found[key] = CurrentArtifact(key, root, entry, source_sha)
    require(set(found) == set(EVIDENCE_KEYS),
            "Missing/extra current-run proof producers: " +
            str(set(EVIDENCE_KEYS) - set(found)))
    return found


def scoped_receipt(suite: str, identifier: str,
                   sources: dict[str, CurrentArtifact]) -> dict:
    if identifier == "labels-language":
        keys = ("dual",)
    elif identifier == "coat-of-arms":
        keys = ("coat",)
    elif suite in OPTIONAL:
        keys = tuple("opt-" + locale for locale in LOCALES)
    else:
        keys = LOCALES
    for key in keys:
        source = sources[key]
        proof_member, proof_hash, proof = source.proof(PROOFS[suite])
        observation = scoped_row(suite, proof, identifier)
        if observation is None:
            continue
        pair = positive_pair(observation)
        kind = "BOUNDED_REAL_PDF_PASS"
        extra = {}
        if identifier == "strict-font":
            negative = next((case for case in proof["certified_evidence"]["strict-font"]
                             if case.get("verified") and
                             source.member(case.get("source_sha256", ""), ".tex") and
                             source.member(case.get("log_sha256", ""), ".log")), None)
            pair = positive_pair(proof["certified_evidence"]["font"])
            require(negative is not None and pair is not None,
                    "Expected strict-font rejection source/log missing")
            pdf_hash, _, detail = pair
            tex_hash = negative["source_sha256"]
            extra = {
                "rejection_log_member": source.member(negative["log_sha256"], ".log"),
                "rejection_log_sha256": negative["log_sha256"],
            }
            kind = "EXPECTED_REJECTION_PLUS_ADJACENT_POSITIVE_PDF"
        elif pair:
            pdf_hash, tex_hash, detail = pair
        else:
            continue
        pdf_member = source.member(pdf_hash, ".pdf")
        tex_member = source.member(tex_hash, ".tex")
        if not pdf_member or not tex_member:
            continue
        negatives = proof.get(
            "negative_controls", proof.get(
                "negatives", proof.get("proof", {}).get("negative_controls_from_producer")))
        require(type(negatives) is int and negatives > 0,
                "Missing family-specific negative controls: " + suite)
        return {
            "current_run_artifact_id": source.artifact_id,
            "current_run_artifact_name": source.name,
            "current_run_artifact_digest": source.zip_digest,
            "proof_json": proof_member, "proof_sha256": proof_hash,
            "scenario": detail.get("scenario") or detail.get("profile") or suite,
            "pdf_member": pdf_member, "pdf_sha256": pdf_hash,
            "tex_member": tex_member, "tex_sha256": tex_hash,
            "negative_controls": negatives, "kind": kind, **extra,
        }
    raise ValueError("Missing current-run PDF/TeX source pair: " + suite + "/" + identifier)


def build(sources: dict[str, CurrentArtifact], run_id: str, sha: str) -> dict:
    candidate = json.loads((ROOT / "standards/api/i18n-v310-runtime-proof-candidate.json").read_text())
    canonical = json.loads((ROOT / "standards/api/public-api.json").read_text())
    crosswalk = json.loads((ROOT / "standards/api/i18n-functional-evidence-crosswalk.json").read_text())
    groups = canonical_groups(candidate, canonical, crosswalk)
    entries = {}
    for group, identifiers in groups.items():
        for identifier in sorted(identifiers):
            suite = candidate["entries"][group][identifier]["proof_suite"]
            require(suite in PROOFS, "Unrecognized proof family")
            key = group + "/" + identifier
            entries[key] = {
                "group": group,
                "identifier": identifier,
                "family": suite,
                "scoped_evidence_state": "BOUNDED_CURRENT_RUNTIME_PDF_PASS",
                "formal_human_review": "PENDING",
                "formal_runtime_promotion": "NOT_AUTHORIZED",
                "evidence": scoped_receipt(suite, identifier, sources),
            }
    require(len(entries) == EXPECTED_IDS == 72,
            "Incomplete canonical current-runtime inventory")
    return {
        "schema_version": 1,
        "issue": 624,
        "scope": "FRESH_CURRENT_RUN_BOUNDED_PDF_EVIDENCE",
        "source_sha": sha,
        "class_git_blob": CLASS_BLOB,
        "producer_workflow_run_id": int(run_id),
        "summary": {
            "identifiers": len(entries),
            "families": len({v["family"] for v in entries.values()}),
            "artifacts": len(sources),
            "human_acceptances": 0,
            "formal_runtime_approvals": 0,
        },
        "artifacts": {
            key: {"id": source.artifact_id, "name": source.name,
                  "digest": source.zip_digest} for key, source in sources.items()
        },
        "historical_ledger_mutated": False,
        "human_normative_linguistic_review": "PENDING",
        "editorial_visual_acceptance": "PENDING",
        "global_internationalization_acceptance": "PENDING",
        "publication_authorized": False,
        "release_candidate_state": "UNRELEASED",
        "entries": entries,
    }


def verify_report(report: dict, sources: dict[str, CurrentArtifact],
                  run_id: str, source_sha: str) -> None:
    expected = build(sources, run_id, source_sha)
    require(report == expected,
            "Current-run report changed from authenticated PDF/TeX/JSON bytes")


def mutation_tests(report: dict, sources: dict[str, CurrentArtifact],
                   run_id: str, source_sha: str) -> int:
    original = next(iter(report["entries"]))
    variants = []
    for change in (
        lambda d: d["entries"].pop(original),
        lambda d: d["entries"][original]["evidence"].update(pdf_sha256="0" * 64),
        lambda d: d["entries"][original]["evidence"].update(tex_sha256="0" * 64),
        lambda d: d["entries"][original]["evidence"].update(proof_sha256="0" * 64),
        lambda d: d.update(source_sha="0" * 40),
        lambda d: d.update(class_git_blob="0" * 40),
        lambda d: d.update(publication_authorized=True),
        lambda d: d["entries"][original].update(formal_runtime_promotion="PASS"),
        lambda d: d["summary"].update(identifiers=71),
        lambda d: d["artifacts"].pop("pt"),
    ):
        candidate = copy.deepcopy(report)
        change(candidate)
        try:
            verify_report(candidate, sources, run_id, source_sha)
        except ValueError:
            variants.append(candidate)
            continue
        raise ValueError("Mutation bypassed current-run byte-integrity verifier")
    return len(variants)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--inputs", type=Path, required=True)
    parser.add_argument("--report", type=Path,
                        default=Path("artifacts/issue624/current-run-72.json"))
    args = parser.parse_args()
    source_sha = os.environ.get("SOURCE_COMMIT_SHA", "")
    run_id = os.environ.get("GITHUB_RUN_ID", "")
    require(re.fullmatch(r"[0-9a-f]{40}", source_sha) is not None,
            "Missing candidate Git commit SHA")
    require(source_sha == subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip(),
        "Artifacts are not checked against current source")
    verify_current_class_scope()
    sources = artifacts_from_current_run(
        args.inputs, run_id, source_sha, os.environ.get("GH_TOKEN", ""))
    report = build(sources, run_id, source_sha)
    verify_report(report, sources, run_id, source_sha)
    mutations = mutation_tests(report, sources, run_id, source_sha)
    report["negative_mutations_rejected"] = mutations
    args.report.parent.mkdir(parents=True, exist_ok=True)
    args.report.write_text(json.dumps(report, indent=2, ensure_ascii=False, sort_keys=True) + "\n",
                           encoding="utf-8")
    print("ISSUE624-LIVE-EVIDENCE status=PASS ids=72 families=13"
          f" artifacts=10 negative_mutations={mutations} sha={source_sha}"
          " formal_human=PENDING publication_authorized=false", flush=True)


if __name__ == "__main__":
    main()
