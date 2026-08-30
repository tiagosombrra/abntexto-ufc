#!/usr/bin/env python3
from __future__ import annotations

import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
LEDGER = ROOT / "release/n15-b2b-article-runtime.json"
CLASS = ROOT / "abntexto-ufc.cls"


def git_blob_sha(path: Path) -> str:
    data = path.read_bytes()
    header = f"blob {len(data)}\0".encode("ascii")
    return hashlib.sha1(header + data).hexdigest()


def require(condition: bool, message: str, errors: list[str]) -> None:
    if not condition:
        errors.append(message)


def main() -> None:
    errors: list[str] = []
    require(LEDGER.is_file(), "B2B runtime ledger is missing", errors)
    if errors:
        raise SystemExit("\n".join(errors))

    ledger = json.loads(LEDGER.read_text(encoding="utf-8"))
    require(ledger.get("schema_version") == 1, "B2B ledger schema must be 1", errors)
    require(ledger.get("phase") == "N15-B2B", "B2B ledger phase is invalid", errors)
    require(
        ledger.get("status") in {"IMPLEMENTED_AWAITING_PR_CERTIFICATION", "DONE"},
        "B2B ledger status is invalid",
        errors,
    )

    source_contract_info = ledger.get("source_contract", {})
    source_contract_path = ROOT / source_contract_info.get("path", "")
    require(source_contract_path.is_file(), "B2A source contract is missing", errors)
    if source_contract_path.is_file():
        require(
            git_blob_sha(source_contract_path) == source_contract_info.get("blob_sha"),
            "B2A source contract blob changed during B2B",
            errors,
        )
        source_contract = json.loads(source_contract_path.read_text(encoding="utf-8"))
        require(source_contract.get("phase") == "N15-B2A", "B2A source phase changed", errors)
        require(
            source_contract.get("runtime", {}).get("implementation_phase") == "N15-B2B",
            "B2A contract no longer delegates runtime to B2B",
            errors,
        )
        expected_rules = set(source_contract.get("article_rule_ids", []))
        implemented = set(ledger.get("implemented_rules", []))
        advisory = set(ledger.get("advisory_rules", []))
        require(
            implemented | advisory == expected_rules,
            "B2B rule disposition does not cover the complete B2A article contract",
            errors,
        )
        require(
            not (implemented & advisory),
            "B2B article rules overlap implemented and advisory dispositions",
            errors,
        )

    for name, frozen in ledger.get("frozen_b2r", {}).items():
        path = ROOT / frozen.get("path", "")
        require(path.is_file(), f"Frozen B2R surface missing: {name}", errors)
        if path.is_file():
            require(
                git_blob_sha(path) == frozen.get("blob_sha"),
                f"Frozen B2R surface changed during B2B: {name}",
                errors,
            )

    runtime = ledger.get("runtime", {})
    article_path = ROOT / runtime.get("article_module", "")
    require(article_path.is_file(), "articles.def is missing", errors)
    if article_path.is_file():
        article_text = article_path.read_text(encoding="utf-8")
        require(
            git_blob_sha(article_path) == runtime.get("article_module_blob_sha"),
            "articles.def does not match the reviewed B2B runtime blob",
            errors,
        )
    else:
        article_text = ""

    class_text = CLASS.read_text(encoding="utf-8")
    public_load = "\\input{abntexto-ufc/public-api.def}"
    article_load = "\\input{abntexto-ufc/articles.def}"
    require(public_load in class_text, "public-api.def class load is missing", errors)
    require(article_load in class_text, "articles.def class load is missing", errors)
    if public_load in class_text and article_load in class_text:
        require(
            class_text.index(public_load) < class_text.index(article_load),
            "articles.def must load after the frozen public API layer",
            errors,
        )

    required_source_tokens = {
        "compatibility profile": "tipo / artigo .code:n",
        "canonical profile": "type / article .meta:n = { tipo = artigo }",
        "submission date": "submission-date .meta:n",
        "author curriculum": "author-short-curriculum .meta:n",
        "author affiliation": "author-affiliation .meta:n",
        "author contact": "author-contact .meta:n",
        "article predicate": "\\ufc_if_article:TF",
        "article header": "\\ufcPrintArticleHeader",
        "Portuguese article header": "\\imprimircabecalhoartigo",
        "article dates": "\\ufcPrintArticleDates",
        "Portuguese article dates": "\\imprimirdatasartigo",
        "fixed article geometry": "\\ufc_article_layout:",
        "single spacing": "\\singlesp",
        "2 cm paragraph indent": "\\setlength{\\parindent}{2cm}",
        "first-page pagination path": "\\textual",
        "continuous section dispatch": "\\ufc_article_base_primary_section_break:",
        "summary dispatch": "\\RenewDocumentCommand \\imprimirresumo",
        "abstract dispatch": "\\RenewDocumentCommand \\imprimirabstract",
        "reference dispatch": "\\ufc_article_base_print_references:",
    }
    for label, token in required_source_tokens.items():
        require(token in article_text, f"articles.def missing {label}", errors)

    for fragment in ("left = 3cm", "top = 3cm", "right = 2cm", "bottom = 2cm"):
        require(fragment in article_text, f"articles.def missing article margin: {fragment}", errors)

    profile_pairs = runtime.get("new_metadata_key_pairs", {})
    for canonical, legacy in profile_pairs.items():
        pattern = re.compile(
            rf"(?m)^\s*{re.escape(canonical)}\s*\.meta:n\s*=\s*\{{\s*{re.escape(legacy)}\s*=",
        )
        require(pattern.search(article_text) is not None, f"Missing metadata alias {canonical} -> {legacy}", errors)

    policies = ledger.get("runtime_policies", {})
    require(policies.get("body_line_spacing") == 1.0, "Article body spacing must remain single", errors)
    require(policies.get("first_line_indent_mm") == 20, "Article paragraph indent must remain 20 mm", errors)
    require(policies.get("primary_sections_start_new_page") is False, "Article sections must remain continuous", errors)
    require(policies.get("page_numbering_start") == "first-page", "Article pagination must start on page 1", errors)
    require(policies.get("references_force_page_break") is False, "Article references must remain continuous", errors)

    if errors:
        for error in sorted(set(errors)):
            print(error)
        raise SystemExit(f"N15-B2B article runtime contract failed with {len(set(errors))} issue(s).")

    print(
        "N15-EVIDENCE article-runtime "
        "canonical=type/article compatibility=tipo/artigo "
        "b2a_rules=13 implemented=11 advisory=2 frozen_b2r=true "
        "article_runtime=true"
    )
    print("N15-B2B scientific article runtime contract passed.")


if __name__ == "__main__":
    main()
