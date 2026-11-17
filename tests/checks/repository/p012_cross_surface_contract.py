#!/usr/bin/env python3
"""Source-bound P0.12 homepage/validator four-locale and release cross-surface contract."""
from __future__ import annotations

import copy
import json
import re
import subprocess
from pathlib import Path
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parents[3]
LOCALES = ("pt-BR", "en", "es", "fr")
SOURCE = "standards/api/i18n-coverage-inventory.json"
RELEASE = "release/v3-release-candidate.json"
DOC = "docs/I18N-COMPLETION-MATRIX.md"

# Execute the two real JavaScript dictionaries in Node, without a browser,
# HTTP access or a duplicated and potentially stale handwritten key list.
NODE_PROBE = r"""
const fs = require("node:fs");
const vm = require("node:vm");
const home = require("./site/homepage-locales.js");
const source = fs.readFileSync("./validator/ui-locales.js", "utf8");
const script = source.replace(/\bexport\s+(?=(?:const|function)\b)/g, "");
const validator = JSON.parse(vm.runInNewContext(
  script + "\nJSON.stringify({copies:COPIES,locales:SUPPORTED_LOCALES,required:REQUIRED_KEYS,options:OPTION_TARGETS,statuses:CANONICAL_STATUS,verdicts:CANONICAL_VERDICT})",
  Object.create(null), { timeout: 2000 }
));
process.stdout.write(JSON.stringify({
  home: { copies: home.HOME_COPY, locales: home.HOME_LOCALES },
  validator
}));
"""


def fail(reason: str) -> None:
    raise SystemExit("P012-CROSS-SURFACE-EVIDENCE status=FAIL " + reason)


def require(condition: bool, reason: str) -> None:
    if not condition:
        raise ValueError(reason)


def tokens(text: str) -> tuple[str, ...]:
    return tuple(sorted(re.findall(r"\{(\d+)\}", text)))


def audit_copy(copies: dict, label: str) -> int:
    require(set(copies) == set(LOCALES), f"{label}_locale_set")
    reference = copies["pt-BR"]
    require(isinstance(reference, dict) and bool(reference), f"{label}_empty")
    keys = set(reference)
    for locale in LOCALES:
        items = copies[locale]
        require(isinstance(items, dict) and set(items) == keys,
                f"{label}_keys_drift_{locale}")
        for key in keys:
            value = items[key]
            require(isinstance(value, str) and value.strip()
                    and "\ufffd" not in value and not re.search(r"</?[a-z]", value, re.I),
                    f"{label}_invalid_text_{locale}_{key}")
            require(tokens(value) == tokens(reference[key]),
                    f"{label}_format_tokens_{locale}_{key}")
    return len(keys)


def audit_release(marker: dict, site: str) -> None:
    published = marker.get("published_release", {})
    candidate = marker.get("next_development_candidate", {})
    require(published.get("version") == "3.0.5" and published.get("tag") == "v3.0.5"
            and published.get("immutable_by_project_policy") is True,
            "published_release_changed")
    require(candidate.get("version") == "3.1.0"
            and candidate.get("candidate_state") == "UNRELEASED"
            and candidate.get("publication_authorized") is False
            and candidate.get("maintainer_visual_acceptance") is False,
            "release_lock_changed")
    require('data-version="published">v3.0.5</code>' in site
            and 'data-version="development">v3.1.0</code>' in site,
            "homepage_release_labels_drift")
    require('href="https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.5"' in site,
            "stable_release_link_drift")
    require('href="https://github.com/tiagosombrra/abntexto-ufc/blob/main/docs/USER-GUIDE.md"' in site,
            "development_guide_link_drift")
    # These are exact critical URL identities, NOT external URL reachability checks.
    for url in (
        "https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.5",
        "https://github.com/tiagosombrra/abntexto-ufc/blob/main/docs/USER-GUIDE.md",
    ):
        parsed = urlparse(url)
        require(parsed.scheme == "https" and parsed.netloc == "github.com",
                "critical_link_protocol")


def negative_controls(payload: dict, marker: dict, site: str) -> int:
    cases = []
    def removed_locale_key():
        copy_payload = copy.deepcopy(payload)
        del copy_payload["validator"]["copies"]["fr"]["statusReady"]
        audit_copy(copy_payload["validator"]["copies"], "validator")
    cases.append(removed_locale_key)

    def changed_placeholder():
        copy_payload = copy.deepcopy(payload)
        copy_payload["validator"]["copies"]["en"]["rulesStats"] += " {88}"
        audit_copy(copy_payload["validator"]["copies"], "validator")
    cases.append(changed_placeholder)

    def untranslated_empty():
        copy_payload = copy.deepcopy(payload)
        copy_payload["home"]["copies"]["es"]["localeLabel"] = " "
        audit_copy(copy_payload["home"]["copies"], "homepage")
    cases.append(untranslated_empty)

    def missing_home_locale():
        copy_payload = copy.deepcopy(payload)
        del copy_payload["home"]["copies"]["fr"]
        audit_copy(copy_payload["home"]["copies"], "homepage")
    cases.append(missing_home_locale)

    def unauthorized_release():
        copy_marker = copy.deepcopy(marker)
        copy_marker["next_development_candidate"]["publication_authorized"] = True
        audit_release(copy_marker, site)
    cases.append(unauthorized_release)

    def released_wrong_html():
        audit_release(marker, site.replace('data-version="published">v3.0.5</code>',
                                           'data-version="published">v3.1.0</code>'))
    cases.append(released_wrong_html)

    for case in cases:
        try:
            case()
        except ValueError:
            continue
        fail("negative_control_escaped=" + case.__name__)
    return len(cases)


def main() -> None:
    run = subprocess.run(
        ["node", "-e", NODE_PROBE], cwd=ROOT, text=True, encoding="utf-8",
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False, timeout=12,
    )
    if run.returncode:
        fail("js_dictionary_probe=" + run.stderr.strip()[:300])
    payload = json.loads(run.stdout)
    try:
        require(tuple(payload["home"]["locales"]) == LOCALES
                and tuple(payload["validator"]["locales"]) == LOCALES,
                "surface_locale_set")
        home_count = audit_copy(payload["home"]["copies"], "homepage")
        validator_count = audit_copy(payload["validator"]["copies"], "validator")
        validator = payload["validator"]
        require(set(validator["required"]) <= set(validator["copies"]["pt-BR"]),
                "validator_required_keys_missing")
        require(set(validator["statuses"]) == {
            "PASS", "FAIL", "WARNING", "MANUAL REVIEW", "NOT APPLICABLE"
        }, "canonical_status_mutated")
        require(set(validator["verdicts"]) == {
            "FAIL", "REVIEW REQUIRED", "AUTOMATED CHECKS PASSED WITH WARNINGS",
            "AUTOMATED CHECKS PASSED",
        }, "canonical_verdict_mutated")
        marker = json.loads((ROOT / RELEASE).read_text(encoding="utf-8"))
        site = (ROOT / "site/index.html").read_text(encoding="utf-8")
        audit_release(marker, site)
        doc = (ROOT / DOC).read_text(encoding="utf-8")
        require("P012-CROSS-SURFACE-EVIDENCE" in doc,
                "audit_matrix_missing_live_contract")
        require("65 textos de validador e 32 do site" not in doc,
                "historical_ui_key_counts_unreconciled")
        tests = negative_controls(payload, marker, site)
    except (ValueError, KeyError, TypeError) as error:
        fail(str(error))
    print(
        f"P012-CROSS-SURFACE-EVIDENCE status=PASS locales=4 "
        f"homepage_keys={home_count} validator_keys={validator_count} "
        f"placeholder_parity=PASS canonical_status=UNCHANGED "
        f"release_boundary=LOCKED critical_link_identity=PASS "
        f"external_reachability=NOT_CHECKED negative_controls={tests} "
        f"network=0 tex_pdf=0 institutional_review=PENDING"
    )


if __name__ == "__main__":
    main()
