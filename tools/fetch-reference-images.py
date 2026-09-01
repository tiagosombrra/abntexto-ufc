#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import time
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

ASSETS = (
    (
        "template/figures/ufc-campus-pici.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/2/23/Campus_do_Pici.jpg",
        "5f431612cdbfbb088c37c685a0e3c93852e96ccd",
    ),
    (
        "template/figures/ufc-reitoria.jpg",
        "https://upload.wikimedia.org/wikipedia/commons/3/39/Reitoria_da_UFC.jpg",
        "b6746bb53d82dae52330805ca0a08f029b773b2e",
    ),
)


def sha1(data: bytes) -> str:
    return hashlib.sha1(data).hexdigest()


def download(url: str) -> bytes:
    request = urllib.request.Request(url, headers={"User-Agent": "abntexto-ufc/3.0.0 reference-assets"})
    last_error: Exception | None = None
    for attempt in range(4):
        try:
            with urllib.request.urlopen(request, timeout=60) as response:
                return response.read()
        except Exception as exc:
            last_error = exc
            if attempt < 3:
                time.sleep(2**attempt)
    raise SystemExit(f"Unable to download {url}: {last_error}")


def main() -> None:
    for relative, url, expected in ASSETS:
        path = ROOT / relative
        if path.is_file():
            data = path.read_bytes()
            if sha1(data) == expected:
                print(f"Reference image verified: {relative}")
                continue

        data = download(url)
        actual = sha1(data)
        if actual != expected:
            raise SystemExit(f"SHA-1 mismatch for {relative}: {actual} != {expected}")
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        print(f"Reference image downloaded: {relative}")


if __name__ == "__main__":
    main()
