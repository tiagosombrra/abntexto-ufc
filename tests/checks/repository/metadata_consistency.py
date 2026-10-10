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
CHANGELOG = ROOT / "CHANGELOG.md"
CTAN_README = ROOT / "release" / "ctan" / "README.md"
CTAN_MANUAL = ROOT / "release" / "ctan" / "abntexto-ufc.tex"


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
        if str(active_line) != "3.0.5":
            return fail("current active development line must be v3.0.5")
        if class_version != str(active_line):
            return fail("active development class/Makefile version must match v3.0.5")

        active = marker.get("active_development_candidate")
        if not isinstance(active, dict):
            return fail("active v3.0.5 marker must contain development metadata")
        current_change = active.get("current_change")

        changelog = CHANGELOG.read_text(encoding="utf-8")
        if current_change == "development-line-open":
            expected_changelog = "3.0.5 — Unreleased"
        elif current_change in ("release-candidate-preparation", "release-source-metadata-correction"):
            expected_changelog = "3.0.5 — 2026-10-06"
        else:
            return fail(f"unsupported v3.0.5 development change: {current_change}")
        if expected_changelog not in changelog:
            return fail(f"CHANGELOG.md must contain candidate heading: {expected_changelog}")

        ctan_readme = CTAN_README.read_text(encoding="utf-8")
        if not re.search(rf"(?m)^Version:\s*{re.escape(str(active_line))}\s*$", ctan_readme):
            return fail("CTAN README must identify exact v3.0.5 version")
        # Source readiness describes package bytes, not external publication.
        statuses = re.findall(r"(?m)^Release status:\s*(.+?)\s*$", ctan_readme)
        source_corrected = current_change == "release-source-metadata-correction"
        frozen_or_authorized = (
            marker.get("candidate_state") == "FROZEN"
            or marker.get("publication_authorized") is True
        )
        if frozen_or_authorized and not source_corrected:
            return fail("freeze/publication requires explicitly corrected source metadata")
        expected_status = "Prepared for publication" if source_corrected else "Unreleased"
        if statuses != [expected_status]:
            return fail(f"CTAN README status must be exactly {expected_status!r}")
        if source_corrected or frozen_or_authorized:
            if re.search(r"(?i)\bunreleased\b|\bdevelopment line\b", ctan_readme):
                return fail("publication-ready CTAN README contains stale development wording")
            if "Actual publication and acceptance are recorded separately" not in ctan_readme:
                return fail("CTAN README must distinguish source readiness from publication")

        ctan_manual = CTAN_MANUAL.read_text(encoding="utf-8")
        if r"\newcommand{\version}{3.0.5}" not in ctan_manual:
            return fail("CTAN manual must identify v3.0.5 during active development")
        if r"\texttt{abntexto-ufc-3.0.5.zip}" not in ctan_manual:
            return fail("CTAN manual distribution name must track v3.0.5")

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
    if active_line is not None:
        for token in ("`v3.0.5`", "`UNRELEASED`", "`NOT_FROZEN`", "issue #471"):
            if token not in release_state:
                return fail(f"RELEASE-STATE.md is missing active-line token: {token}")

    print(
        "METADATA-CONSISTENCY-EVIDENCE status=PASS "
        f"published_version={published_version} citation_date={published_date} "
        f"class_version={class_version} make_version={make_version} "
        f"active_development_line={active_line if active_line is not None else 'none'} "
        f"candidate_change={marker.get('active_development_candidate', {}).get('current_change', 'none')}"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
