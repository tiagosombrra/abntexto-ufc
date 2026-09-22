#!/usr/bin/env python3
from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from typing import Any

TESTS_DIR = next(
    parent
    for parent in Path(__file__).resolve().parents
    if (parent / "path_resolver.py").is_file()
)
if str(TESTS_DIR) not in sys.path:
    sys.path.insert(0, str(TESTS_DIR))

from path_resolver import ROOT  # noqa: E402
MARKER = ROOT / "release" / "v3-release-candidate.json"
CITATION = ROOT / "CITATION.cff"
CLASS = ROOT / "abntexto-ufc.cls"
MAKEFILE = ROOT / "Makefile"
ARCHITECTURE = ROOT / "docs" / "ARCHITECTURE.md"
RELEASE_STATE = ROOT / "docs" / "RELEASE-STATE.md"


def fail(message: str) -> int:
    print(f"Metadata consistency contract failed: {message}")
    return 1


def load_json(path: Path) -> dict[str, Any]:
    value = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(value, dict):
        raise SystemExit(f"Metadata consistency contract failed: {path} must contain an object")
    return value


def top_level_cff_field(text: str, field: str) -> str | None:
    match = re.search(
        rf"^{re.escape(field)}:\s*[\"']?([^\"'\n]+)[\"']?\s*$",
        text,
        flags=re.MULTILINE,
    )
    return match.group(1).strip() if match else None


def main() -> int:
    marker = load_json(MARKER)
    published = marker.get("published_release")
    if not isinstance(published, dict):
        return fail("release marker must contain published_release")

    published_version = published.get("version")
    published_at = published.get("published_at")
    if not isinstance(published_version, str) or not published_version:
        return fail("published release version is missing")
    if not isinstance(published_at, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}T.*Z", published_at):
        return fail("published release timestamp is missing or malformed")
    published_date = published_at[:10]

    cff = CITATION.read_text(encoding="utf-8")
    if top_level_cff_field(cff, "version") != published_version:
        return fail("CITATION.cff version must match the latest published release")
    if top_level_cff_field(cff, "date-released") != published_date:
        return fail("CITATION.cff date-released must match the GitHub publication date")

    class_text = CLASS.read_text(encoding="utf-8")
    class_match = re.search(
        r"\\ProvidesClass\{abntexto-ufc\}\[(\d{4}/\d{2}/\d{2})\s+v([^\s]+)\s+",
        class_text,
    )
    if not class_match:
        return fail("cannot read abntexto-ufc.cls version identity")
    class_version = class_match.group(2)

    makefile = MAKEFILE.read_text(encoding="utf-8")
    make_match = re.search(r"^VERSION\s*:=\s*([^\s]+)\s*$", makefile, flags=re.MULTILINE)
    if not make_match:
        return fail("cannot read Makefile VERSION")
    make_version = make_match.group(1)

    active_line = marker.get("active_development_line")
    if active_line is None:
        if class_version != published_version:
            return fail("steady-state class version must match the latest published release")
        if make_version != published_version:
            return fail("steady-state Makefile VERSION must match the latest published release")
    else:
        allowed_versions = {published_version, str(active_line)}
        if class_version not in allowed_versions or make_version not in allowed_versions:
            return fail("active-line version metadata must identify either the published or active line")
        if class_version != make_version:
            return fail("abntexto-ufc.cls and Makefile VERSION must agree during active development")

    architecture = ARCHITECTURE.read_text(encoding="utf-8")
    forbidden_architecture_fragments = (
        "The latest published release is v",
        "The active unreleased development line is v",
        "During the active v3.",
    )
    for fragment in forbidden_architecture_fragments:
        if fragment in architecture:
            return fail(f"ARCHITECTURE.md contains volatile release-state text: {fragment}")
    if "Current publication and development-line facts are owned by" not in architecture:
        return fail("ARCHITECTURE.md must delegate volatile release state to current authorities")

    release_state = RELEASE_STATE.read_text(encoding="utf-8")
    if "Release issue #353 is in closeout" in release_state:
        return fail("RELEASE-STATE.md still reports completed issue #353 as in closeout")
    if "Release issue #353 is completed and closed" not in release_state:
        return fail("RELEASE-STATE.md must record issue #353 as completed and closed")

    print(
        "METADATA-CONSISTENCY-EVIDENCE status=PASS "
        f"published_version={published_version} citation_date={published_date} "
        f"class_version={class_version} make_version={make_version} "
        f"active_development_line={active_line if active_line is not None else 'none'}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
