#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import time
import urllib.request
from pathlib import Path

COMMIT = "4c03fd7b5a7af089627dedb547c53cad4eed2a2a"
BLOB_SHA1 = "f9cc40c65fbf6c2f9520b4ca4f312440e8d0ee6a"
MARKER = b"[2026-05-08 1.1 Preparation of works in ABNT standards]"
URL = f"https://raw.githubusercontent.com/ElaysonAbreu/abntexto/{COMMIT}/abntexto.cls"


def git_blob_sha1(content: bytes) -> str:
    payload = b"blob " + str(len(content)).encode("ascii") + b"\0" + content
    return hashlib.sha1(payload).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description="Fetch the pinned abntexto 1.1 class used by the Overleaf bundle.")
    parser.add_argument("--output", type=Path, default=Path("abntexto.cls"))
    args = parser.parse_args()

    content = None
    for attempt in range(1, 4):
        try:
            request = urllib.request.Request(URL, headers={"User-Agent": "abntexto-ufc-release"})
            with urllib.request.urlopen(request, timeout=30) as response:
                content = response.read()
            break
        except Exception:
            if attempt == 3:
                raise
            time.sleep(5 * attempt)

    if content is None:
        raise SystemExit("abntexto 1.1 could not be downloaded.")

    digest = git_blob_sha1(content)
    if digest != BLOB_SHA1:
        raise SystemExit(f"abntexto blob mismatch: expected {BLOB_SHA1}, got {digest}")
    if MARKER not in content:
        raise SystemExit("abntexto 1.1 identity marker missing.")

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_bytes(content)
    print(f"Pinned abntexto 1.1 written to {args.output} ({COMMIT}).")


if __name__ == "__main__":
    main()
