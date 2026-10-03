#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import struct
import subprocess
from pathlib import Path

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
ROOT = TESTS_DIR.parent

ASSET_PATH = "assets/institutional/ufc-coat-of-arms.png"
PROVENANCE_PATH = "assets/institutional/PROVENANCE.json"
EXPECTED_SHA256 = "163614098ff875cc39db3b5398d5a974001d19178bbd433ee235bef4efed4825"
EXPECTED_GIT_BLOB = "0cd0bbc38fba2e01c40051d6c4ae9a5e71025f74"
EXPECTED_BYTES = 225873
EXPECTED_DIMENSIONS = (488, 730)
EXPECTED_DISTRIBUTION = {
    "template": "include",
    "overleaf": "include",
    "ctan": "exclude",
}


def fail(message: str) -> None:
    raise SystemExit(message)


def git_blob(path: str) -> str:
    completed = subprocess.run(
        ["git", "hash-object", path],
        cwd=ROOT,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
        encoding="utf-8",
        errors="replace",
        check=False,
    )
    if completed.returncode != 0:
        fail(completed.stderr.strip() or f"git hash-object failed: {path}")
    return completed.stdout.strip()


def png_dimensions(data: bytes) -> tuple[int, int]:
    if not data.startswith(b"\x89PNG\r\n\x1a\n"):
        fail("institutional asset is not a PNG")
    if len(data) < 24 or data[12:16] != b"IHDR":
        fail("institutional PNG is missing a valid IHDR")
    return struct.unpack(">II", data[16:24])


def main() -> None:
    metadata = json.loads((ROOT / PROVENANCE_PATH).read_text(encoding="utf-8"))
    if metadata.get("schema_version") != 1:
        fail("institutional provenance schema_version must be 1")

    asset = metadata.get("asset")
    expected_asset = {
        "bytes": EXPECTED_BYTES,
        "git_blob_sha1": EXPECTED_GIT_BLOB,
        "height_px": EXPECTED_DIMENSIONS[1],
        "media_type": "image/png",
        "path": ASSET_PATH,
        "sha256": EXPECTED_SHA256,
        "width_px": EXPECTED_DIMENSIONS[0],
    }
    if asset != expected_asset:
        fail(f"institutional asset metadata drift: expected={expected_asset} actual={asset}")

    data = (ROOT / ASSET_PATH).read_bytes()
    if len(data) != EXPECTED_BYTES:
        fail(f"institutional asset byte-size drift: {len(data)}")
    actual_sha256 = hashlib.sha256(data).hexdigest()
    if actual_sha256 != EXPECTED_SHA256:
        fail(f"institutional asset SHA-256 drift: {actual_sha256}")
    actual_blob = git_blob(ASSET_PATH)
    if actual_blob != EXPECTED_GIT_BLOB:
        fail(f"institutional asset Git blob drift: {actual_blob}")
    actual_dimensions = png_dimensions(data)
    if actual_dimensions != EXPECTED_DIMENSIONS:
        fail(f"institutional asset dimensions drift: {actual_dimensions}")

    if metadata.get("classification") != {
        "institution": "Universidade Federal do Ceará (UFC)",
        "kind": "institutional-mark",
        "project_license_coverage": False,
        "project_source": False,
    }:
        fail("institutional asset classification drift")

    if metadata.get("distribution_policy") != EXPECTED_DISTRIBUTION:
        fail("institutional asset distribution policy drift")

    if metadata.get("external_source_provenance") != {
        "status": "not-documented-in-repository",
        "url": None,
    }:
        fail("external institutional asset provenance must remain explicitly undocumented unless evidenced")

    if metadata.get("rights") != {
        "project_grant": "none",
        "statement": "Repository inclusion does not grant independent trademark, brand or institutional-mark rights.",
    }:
        fail("institutional asset rights statement drift")

    if metadata.get("repository_history") != {
        "canonical_path": ASSET_PATH,
        "canonicalized_commit": "c31013b4c7cebe3ddaf3dc0011f489b8de3cd20e",
        "canonicalized_date": "2026-08-28",
        "content_changed_on_canonicalization": False,
        "introduced_commit": "c25cd4dd1c923d9afc910b1011251dcd78ac5ee3",
        "introduced_date": "2026-08-19",
        "introduced_path": "assets/institucional/brasao-ufc.PNG",
    }:
        fail("institutional asset repository-history metadata drift")

    readme = (ROOT / "assets/institutional/README.md").read_text(encoding="utf-8")
    required_readme = (
        "PROVENANCE.json",
        "not covered by the project's LPPL license",
        "External source provenance is not documented in repository evidence.",
        "Template bundle: include",
        "Overleaf bundle: include",
        "CTAN package: do **not** redistribute",
    )
    for token in required_readme:
        if token not in readme:
            fail(f"institutional asset README contract missing: {token}")

    print(
        "INSTITUTIONAL-ASSET-EVIDENCE status=PASS "
        f"bytes={EXPECTED_BYTES} dimensions={EXPECTED_DIMENSIONS[0]}x{EXPECTED_DIMENSIONS[1]} "
        f"sha256={EXPECTED_SHA256} git_blob={EXPECTED_GIT_BLOB} "
        "classification=institutional-mark project_license_coverage=false "
        "external_source_provenance=not-documented-in-repository "
        "template=include overleaf=include ctan=exclude"
    )


if __name__ == "__main__":
    main()
