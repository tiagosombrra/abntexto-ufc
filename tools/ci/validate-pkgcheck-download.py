#!/usr/bin/env python3
from __future__ import annotations

import argparse
import zipfile
from pathlib import Path


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Validate the downloaded CTAN pkgcheck archive."
    )
    parser.add_argument(
        "archive",
        nargs="?",
        type=Path,
        default=Path(".ci-downloads/pkgcheck.zip"),
    )
    args = parser.parse_args()
    archive = args.archive

    if not archive.is_file() or archive.stat().st_size == 0:
        raise SystemExit("Current CTAN pkgcheck download is missing or empty.")
    with zipfile.ZipFile(archive) as handle:
        bad = handle.testzip()
        if bad is not None:
            raise SystemExit(f"Current CTAN pkgcheck archive is corrupt at {bad}.")

    print(
        "PKGCHECK-DOWNLOAD-EVIDENCE status=PASS "
        f"archive={archive.as_posix()} bytes={archive.stat().st_size}"
    )


if __name__ == "__main__":
    main()
