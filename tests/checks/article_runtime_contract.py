#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "release/n15-b2b-article-runtime.json"
ARTICLE_SOURCE = ROOT / "abntexto-ufc/articles.def"
CLASS_SOURCE = ROOT / "abntexto-ufc.cls"

VALUE_PATTERN = re.compile(
    r"(?m)^\s*([a-z][a-z0-9-]*)\s*/\s*([A-Za-z0-9-]+)\s*\."
    r"(?:code|meta)(?::[A-Za-z]+)?\s*="
)
KEY_PATTERN = re.compile(
    r"(?m)^\s*([a-z][a-z0-9-]*)\s*\."
    r"(?:choice|code|meta|tl_gset)(?::[A-Za-z]+)?\s*(?::|=)"
)
MODULE_PATTERN = re.compile(r"\\input\{(abntexto-ufc/[^}]+\.def)\}")


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8")


def blob_sha(path: Path) -> str:
    data = path.read_bytes()
    return hashlib.sha1(f"blob {len(data)}\0".encode("ascii") + data).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    ledger = json.loads(read(LEDGER))

    require(ledger.get("schema_version") == 1, "B2B ledger schema must be 1", errors)
    require(ledger.get("phase") == "N15-B2B", "B2B ledger phase is invalid", errors)
    require(
        ledger.get("status") in {"IMPLEMENTED_PENDING_CERTIFICATION", "DONE"},
        "B2B ledger status is invalid",
        errors,
    )

    for name, contract in ledger.get("base_contracts", {}).items():
        path = ROOT / contract.get("path", "")
        require(path.is_file(), f"B2B base contract missing: {name}", errors)
        if path.is_file():
            require(
                blob_sha(path) == contract.get("blob_sha"),
                f"B2B base contract blob changed: {name}",
                errors,
            )

    normative = json.loads(read(ROOT / "normativa/coverage-rules-article.json"))
    require(normative.get("phase") == "N15-B2A", "article normative contract phase changed", errors)
    rules = normative.get("rules", [])
    require(len(rules) == 13, f"expected 13 article predicates, got {len(rules)}", errors)
    rule_ids = {item.get("id") for item in rules}
    required_ids = {
        "article.structure.required",
        "article.title.presentation",
        "article.authorship.presentation",
        "article.abstract.presentation",
        "article.abstract.length.recommended",
        "article.dates.required",
        "article.textual.required-sections",
        "article.textual.typography",
        "article.references.required-placement",
        "article.page.margins",
        "article.font.family.recommended",
        "article.pagination",
        "article.sections.continuous",
    }
    require(rule_ids == required_ids, "article normative predicate set changed", errors)

    article = read(ARTICLE_SOURCE)
    class_text = read(CLASS_SOURCE)

    values = set(VALUE_PATTERN.findall(article))
    require(
        values == {("tipo", "artigo"), ("type", "article")},
        f"unexpected B2B setup values: {sorted(values)}",
        errors,
    )
    keys = set(KEY_PATTERN.findall(article))
    require(not keys, f"B2B introduced new setup keys: {sorted(keys)}", errors)

    require("\\NewDocumentCommand" not in article, "B2B introduced a new public command", errors)
    require("\\ProvideDocumentCommand" not in article, "B2B introduced a provided public command", errors)
    require("\\NewDocumentEnvironment" not in article, "B2B introduced a new environment", errors)
    require("\\ProvideDocumentEnvironment" not in article, "B2B introduced a provided environment", errors)
    require(
        "\\cs_set_protected:Npn \\ufc_primary_section_break:" not in article,
        "B2B must not take ownership of the layout internal section-break function",
        errors,
    )

    modules = MODULE_PATTERN.findall(class_text)
    require(modules.count("abntexto-ufc/articles.def") == 1, "articles.def must be loaded exactly once", errors)
    if "abntexto-ufc/articles.def" in modules:
        article_index = modules.index("abntexto-ufc/articles.def")
        require(
            article_index == len(modules) - 1,
            "articles.def must be the final UFC runtime layer",
            errors,
        )
        for predecessor in (
            "abntexto-ufc/frontmatter.def",
            "abntexto-ufc/academic-works.def",
            "abntexto-ufc/research-projects.def",
            "abntexto-ufc/bibliography.def",
            "abntexto-ufc/compat-nbr6023-2025.def",
            "abntexto-ufc/backmatter.def",
            "abntexto-ufc/public-api.def",
        ):
            require(
                predecessor in modules and modules.index(predecessor) < article_index,
                f"articles.def must load after {predecessor}",
                errors,
            )

    required_markers = (
        "type / article .meta:n = { tipo = artigo }",
        "\\RenewDocumentCommand \\date",
        "\\g_ufc_article_submission_date_set_bool",
        "Required~article~submission~date~was~not~set",
        "\\ufc_article_base_textual:",
        "\\ufc_layout_one_sided:",
        "\\setcounter{page}{1}",
        "\\singlesp",
        "\\setlength{\\parindent}{2cm}",
        "\\RenewDocumentCommand \\ufcPrimarySectionBreak",
        "\\RenewDocumentCommand \\ufcPretextualBreak",
        "Data~de~submissão:",
        "\\cs_use:c {@date}",
        "Data~de~aprovação:",
        "\\ufc_pretextual_heading:n {Resumo}",
        "\\ufc_pretextual_heading:n {Abstract}",
        "\\bfseries REFERÊNCIAS",
        "\\RenewDocumentCommand \\imprimirfolhaderosto",
        "\\RenewDocumentCommand \\imprimirresumo",
        "\\RenewDocumentCommand \\imprimirabstract",
        "\\RenewDocumentCommand \\imprimirsumario",
        "\\RenewDocumentCommand \\imprimirreferencias",
    )
    for marker in required_markers:
        require(marker in article, f"B2B runtime marker missing: {marker}", errors)

    policy = ledger.get("policy", {})
    require(policy.get("b2r_public_runtime_blob_must_remain_frozen") is True, "B2B must freeze B2R public runtime", errors)
    require(policy.get("n12_workflow_must_remain_frozen") is True, "B2B must freeze N12 workflow", errors)
    require(policy.get("existing_profile_behavior_change_allowed") is False, "B2B may not change existing profile behavior", errors)
    require(
        policy.get("article_public_surface_expansion_beyond_reserved_values_allowed") is False,
        "B2B public expansion policy is invalid",
        errors,
    )

    if errors:
        for error in errors:
            print(error)
        raise SystemExit(f"N15-B2B article runtime contract failed with {len(errors)} issue(s).")

    print(
        "N15-EVIDENCE article-runtime-contract "
        "predicates=13 setup_values=2 new_keys=0 new_commands=0 new_environments=0 "
        "explicit_submission_date=true final_runtime_layer=true layout_internal_owner_preserved=true "
        "b2r_runtime_frozen=true n12_frozen=true status=PASS"
    )


if __name__ == "__main__":
    main()
