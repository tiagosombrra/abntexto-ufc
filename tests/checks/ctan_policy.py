#!/usr/bin/env python3
from __future__ import annotations

import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

BINARY_POLICY = {
    "assets/institutional/ufc-coat-of-arms.png": "0cd0bbc38fba2e01c40051d6c4ae9a5e71025f74",
    "figures/fluxo-exemplo.png": "cab7ed494b6e2f8606565baf2381f5333b282385",
    "figures/grafico-exemplo.jpg": "a9f5d2020677dcc39619d91ca5f2425cbe207140",
}


def tracked_blob_ids() -> dict[str, str]:
    output = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", "ls-files", "-s", "-z"],
        cwd=ROOT,
    )
    result: dict[str, str] = {}
    for record in output.split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        fields = metadata.split()
        result[raw_path.decode("utf-8")] = fields[1].decode("ascii")
    return result


def tracked_files() -> list[str]:
    output = subprocess.check_output(
        ["git", "-c", f"safe.directory={ROOT}", "ls-files", "-z"], cwd=ROOT
    )
    return [item.decode("utf-8") for item in output.split(b"\0") if item]


def is_binary(path: Path) -> bool:
    data = path.read_bytes()
    if b"\0" in data:
        return True
    try:
        data.decode("utf-8")
    except UnicodeDecodeError:
        return True
    return False


def main() -> None:
    errors: list[str] = []
    blob_ids = tracked_blob_ids()
    binaries = {
        name: blob_ids.get(name, "")
        for name in tracked_files()
        if is_binary(ROOT / name)
    }

    expected = set(BINARY_POLICY)
    actual = set(binaries)
    for name in sorted(actual - expected):
        errors.append(f"{name}: unclassified tracked binary")
    for name in sorted(expected - actual):
        errors.append(f"{name}: approved binary is missing or no longer binary")
    for name in sorted(actual & expected):
        if binaries[name] != BINARY_POLICY[name]:
            errors.append(
                f"{name}: binary content changed; review provenance and distribution policy"
            )

    ctan_readme = (ROOT / "docs/README-CTAN.md").read_text(encoding="utf-8")
    required_phrases = (
        "The CTAN archive contains no institutional image assets.",
        "The UFC coat of arms is not distributed in the CTAN archive",
        "brasao-arquivo",
    )
    for phrase in required_phrases:
        if phrase not in ctan_readme:
            errors.append(f"docs/README-CTAN.md: required CTAN asset policy missing: {phrase}")

    licenses = (ROOT / "figures/LICENCAS.md").read_text(encoding="utf-8")
    if "`ufctex`" in licenses:
        errors.append("figures/LICENCAS.md: stale ufctex package identity")

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(f"CTAN policy check failed with {len(errors)} issue(s).")

    print(f"CTAN policy check passed: {len(binaries)} tracked binaries classified.")


if __name__ == "__main__":
    main()
