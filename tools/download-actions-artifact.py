#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import io
import json
import os
import urllib.error
import urllib.request
import zipfile
from pathlib import Path


class NoRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self, req, fp, code, msg, headers, newurl):
        return None


def main() -> None:
    parser = argparse.ArgumentParser(description="Download and verify one GitHub Actions artifact.")
    parser.add_argument("--repository", required=True)
    parser.add_argument("--artifact-id", required=True, type=int)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()

    token = os.environ.get("GH_TOKEN") or os.environ.get("GITHUB_TOKEN")
    if not token:
        raise SystemExit("GH_TOKEN or GITHUB_TOKEN is required.")

    headers = {
        "Authorization": f"Bearer {token}",
        "Accept": "application/vnd.github+json",
        "X-GitHub-Api-Version": "2022-11-28",
        "User-Agent": "abntexto-ufc-artifact-download",
    }
    metadata_url = f"https://api.github.com/repos/{args.repository}/actions/artifacts/{args.artifact_id}"
    with urllib.request.urlopen(
        urllib.request.Request(metadata_url, headers=headers), timeout=30
    ) as response:
        artifact = json.load(response)

    if artifact.get("expired"):
        raise SystemExit(f"Artifact {args.artifact_id} is expired.")

    download_url = f"{metadata_url}/zip"
    request = urllib.request.Request(download_url, headers=headers)
    opener = urllib.request.build_opener(NoRedirect())
    try:
        with opener.open(request, timeout=30) as response:
            content = response.read()
    except urllib.error.HTTPError as error:
        if error.code not in (301, 302, 307, 308):
            raise
        location = error.headers.get("Location")
        if not location:
            raise SystemExit("Artifact redirect did not include Location.")
        with urllib.request.urlopen(
            urllib.request.Request(location, headers={"User-Agent": "abntexto-ufc-artifact-download"}),
            timeout=60,
        ) as response:
            content = response.read()

    expected = artifact.get("digest")
    if expected and expected.startswith("sha256:"):
        actual = hashlib.sha256(content).hexdigest()
        if actual != expected.split(":", 1)[1]:
            raise SystemExit(
                f"Artifact SHA-256 mismatch: expected {expected}, got sha256:{actual}."
            )

    destination = args.output.resolve()
    destination.mkdir(parents=True, exist_ok=True)
    root = destination.resolve()
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        for member in archive.infolist():
            target = (destination / member.filename).resolve()
            if target != root and root not in target.parents:
                raise SystemExit(f"Unsafe artifact path: {member.filename}")
        archive.extractall(destination)

    print(f"Downloaded and verified artifact {artifact.get('name')} ({args.artifact_id}).")


if __name__ == "__main__":
    main()
