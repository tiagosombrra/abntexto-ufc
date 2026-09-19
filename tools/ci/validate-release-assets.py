#!/usr/bin/env python3
from __future__ import annotations

import os
from pathlib import Path

PACKAGE_ID = "abntexto-ufc"


def main() -> None:
    root = Path("dist")
    version = os.environ["RELEASE_VERSION"]
    expected = {
        f"{PACKAGE_ID}-{version}.zip",
        f"{PACKAGE_ID}-template-{version}.zip",
        f"{PACKAGE_ID}-overleaf-{version}.zip",
        "SHA256SUMS",
    }
    actual = {path.name for path in root.iterdir() if path.is_file()}
    if actual != expected:
        raise SystemExit(
            "Release asset build failed: unexpected dist file set: "
            + ", ".join(sorted(actual ^ expected))
        )
    print(
        "RELEASE-ASSET-SET-EVIDENCE status=PASS "
        f"version={version} assets={len(expected)}"
    )


if __name__ == "__main__":
    main()
