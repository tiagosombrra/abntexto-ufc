#!/usr/bin/env python3
from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
STANDARDS_DIR = ROOT / "standards"
MAP_PATH = STANDARDS_DIR / "reference-guide-map.json"
CATALOG_PATH = STANDARDS_DIR / "catalog.json"
ATOMIC_PATH = STANDARDS_DIR / "atomic-rules.json"
API_CONTRACT_PATH = STANDARDS_DIR / "public-api.json"
COMMAND_REFERENCE_PATH = ROOT / "docs" / "COMMAND-REFERENCE.md"
CLASS_PATH = ROOT / "abntexto-ufc.cls"
REFERENCE_ROOT = ROOT / "template"
BIBLIOGRAPHY_PATH = REFERENCE_ROOT / "backmatter" / "references.bib"

ALLOWED_CLASSIFICATIONS = {"normative", "institutional", "model-policy", "example"}
EXPECTED_CHAPTERS = [
    "1-introduction.tex",
    "2-theoretical-background.tex",
    "3-methodology.tex",
    "4-results.tex",
    "5-conclusion.tex",
]
RETIRED_REFERENCE_TOKENS = (
    "tccgraduacao",
    "tccespecializacao",
    "projetoanonimizado",
    "ficha-catalografica",
    "fonte-estrita",
    "backmatter/referencias.bib",
    "frontmatter/dedicatoria.tex",
)
REVIEWED_LEGACY_HEADINGS = (
    "Usando Fórmulas Matemáticas",
    "Usando Código-fonte",
    "Usando Teoremas, Proposições, etc",
    "Usando Questões",
    "Resultados do Experimento A",
    "Resultados do Experimento B",
)


def load_json(path: Path) -> Any:
    return json.loads(path.read_text(encoding="utf-8"))


def collect_declared_rule_ids(value: Any) -> set[str]:
    rule_ids: set[str] = set()
    if isinstance(value, dict):
        for key, item in value.items():
            if key in {"rule_id", "expected_rule_id"} and isinstance(item, str):
                rule_ids.add(item)
            elif key == "rule_ids" and isinstance(item, list):
                rule_ids.update(entry for entry in item if isinstance(entry, str))
            else:
                rule_ids.update(collect_declared_rule_ids(item))
    elif isinstance(value, list):
        for item in value:
            rule_ids.update(collect_declared_rule_ids(item))
    return rule_ids


def collect_rule_ids(catalog: dict[str, Any], atomic: dict[str, Any]) -> set[str]:
    rule_ids = {rule["id"] for rule in catalog.get("rules", []) if "id" in rule}
    rule_ids.update(atomic.get("keep_atomic", []))
    for group in atomic.get("groups", {}).values():
        for rule in group:
            if "id" in rule:
                rule_ids.add(rule["id"])

    for path in sorted(STANDARDS_DIR.glob("*.json")):
        if path == MAP_PATH:
            continue
        rule_ids.update(collect_declared_rule_ids(load_json(path)))
    return rule_ids


def audit_reference_hygiene() -> list[str]:
    failures: list[str] = []
    chapter_dir = REFERENCE_ROOT / "chapters"
    actual_chapters = sorted(path.name for path in chapter_dir.glob("*.tex"))
    if actual_chapters != EXPECTED_CHAPTERS:
        failures.append(
            "template/chapters: canonical tutorial chapter set drift: "
            f"expected={EXPECTED_CHAPTERS} actual={actual_chapters}"
        )

    for path in sorted(REFERENCE_ROOT.rglob("*.tex")):
        text = path.read_text(encoding="utf-8")
        rel = path.relative_to(ROOT).as_posix()
        if re.search(r"\bV2\b", text):
            failures.append(f"{rel}: stale V2 wording remains in the canonical V3 reference")
        for token in RETIRED_REFERENCE_TOKENS:
            if token in text:
                failures.append(f"{rel}: retired V3 reference token remains: {token}")
        if re.search(r"\\texttt\{tipo\}", text):
            failures.append(f"{rel}: retired public profile key is still documented: tipo")
        if re.search(r"\\guia(?:normativa|institucional|politica|exemplo|mecanismo|validacao)", text):
            failures.append(
                f"{rel}: documentation callout remains embedded in the tutorial corpus"
            )

    main = (REFERENCE_ROOT / "main.tex").read_text(encoding="utf-8")
    intro = (chapter_dir / "1-introduction.tex").read_text(encoding="utf-8")
    annex = (REFERENCE_ROOT / "backmatter" / "annexes" / "annex-a.tex").read_text(
        encoding="utf-8"
    )

    main_markers = (
        "department = {}",
        "author = {Nome Completo do Autor}",
        "coat-of-arms = true",
        "\\input{chapters/1-introduction}",
        "\\input{chapters/5-conclusion}",
    )
    for marker in main_markers:
        if marker not in main:
            failures.append(f"template/main.tex: tutorial marker missing: {marker}")

    if "Universidade Federal do Ceará (UFC)" not in intro:
        failures.append(
            "template/chapters/1-introduction.tex: full UFC name with acronym is missing"
        )
    if "\\textbf{Fonte:}" not in annex:
        failures.append(
            "template/backmatter/annexes/annex-a.tex: external source marker is missing"
        )

    return failures


def audit_tutorial_content() -> tuple[list[str], dict[int, dict[str, Any]]]:
    failures: list[str] = []
    chapter_paths = sorted((REFERENCE_ROOT / "chapters").glob("*.tex"))
    chapters = {
        path.relative_to(ROOT).as_posix(): path.read_text(encoding="utf-8")
        for path in chapter_paths
    }
    corpus = "\n".join(chapters.values())
    intro = chapters.get("template/chapters/1-introduction.tex", "")

    expected_objects = (
        "Fluxo simplificado da validação automatizada",
        "Critérios observados no procedimento demonstrativo",
        "Função auxiliar para cálculo da média",
        "Resultados sintéticos da validação",
    )
    missing_objects = [title for title in expected_objects if title not in corpus]
    if missing_objects:
        failures.append(
            "tutorial object examples missing: " + ", ".join(missing_objects)
        )

    ufc_phrase = "Universidade Federal do Ceará (UFC)"
    phrase_at = intro.find(ufc_phrase)
    first_ufc = re.search(r"\bUFC\b", intro)
    expected_ufc_at = phrase_at + ufc_phrase.index("UFC") if phrase_at >= 0 else -1
    first_use_ok = (
        phrase_at >= 0
        and first_ufc is not None
        and first_ufc.start() == expected_ufc_at
    )
    if not first_use_ok:
        failures.append(
            "the first body-text UFC occurrence is not Universidade Federal do Ceará (UFC)"
        )

    headings: list[str] = []
    for text in chapters.values():
        headings.extend(
            re.findall(r"\\(?:section|subsection|subsubsection)\{([^{}]+)\}", text)
        )
    expected_headings = (
        "Introdução",
        "Fundamentação teórica",
        "Metodologia",
        "Resultados e discussão",
        "Conclusão",
        "Citações e referências",
    )
    missing_headings = [heading for heading in expected_headings if heading not in headings]
    legacy_headings = [heading for heading in REVIEWED_LEGACY_HEADINGS if heading in corpus]
    if missing_headings:
        failures.append("tutorial headings missing: " + ", ".join(missing_headings))
    if legacy_headings:
        failures.append("legacy tutorial headings remain: " + ", ".join(legacy_headings))

    evidence = {
        11: {
            "status": "PASS" if not missing_objects else "FAIL",
            "tutorial_objects": len(expected_objects),
        },
        16: {
            "status": "PASS" if first_use_ok else "FAIL",
            "first_use": ufc_phrase if first_use_ok else None,
        },
        28: {
            "status": "PASS" if not missing_headings and not legacy_headings else "FAIL",
            "tutorial_headings": len(expected_headings),
            "legacy_headings_present": len(legacy_headings),
        },
    }
    return failures, evidence


def audit_citation_closure() -> tuple[list[str], dict[str, int]]:
    failures: list[str] = []
    bibliography = BIBLIOGRAPHY_PATH.read_text(encoding="utf-8")
    declared = {
        match.group(1).strip()
        for match in re.finditer(
            r"(?m)^\s*@[A-Za-z]+\s*\{\s*([^,\s]+)\s*,",
            bibliography,
        )
    }

    citation_re = re.compile(
        r"\\(?:textcite|parencite|cite|nocite|apud|textapud)\*?"
        r"(?:\[[^\]]*\])*\{([^{}]+)\}"
    )
    used: set[str] = set()

    for path in sorted(REFERENCE_ROOT.rglob("*.tex")):
        source = path.read_text(encoding="utf-8")
        # Strip TeX comments before reading citation commands.
        source = "\n".join(line.split("%", 1)[0] for line in source.splitlines())
        for match in citation_re.finditer(source):
            for key in match.group(1).split(","):
                normalized = key.strip()
                if normalized and normalized != "*":
                    used.add(normalized)

    missing = sorted(used - declared)
    if missing:
        failures.append(
            "template/backmatter/references.bib: citation keys missing: "
            + ", ".join(missing)
        )

    return failures, {"declared": len(declared), "used": len(used), "missing": len(missing)}


def audit_command_reference() -> list[str]:
    failures: list[str] = []
    api = load_json(API_CONTRACT_PATH)
    text = COMMAND_REFERENCE_PATH.read_text(encoding="utf-8")

    if api.get("contract") != "current-public-api" or api.get("status") != "active":
        failures.append("standards/public-api.json: current API contract identity/status is invalid")
    if api.get("runtime_source") != "abntexto-ufc.cls":
        failures.append("standards/public-api.json: runtime source must be abntexto-ufc.cls")

    setup_keys: set[str] = set()
    for values in api.get("setup_keys", {}).values():
        setup_keys.update(values)

    class_text = CLASS_PATH.read_text(encoding="utf-8")
    runtime_keys = set(
        re.findall(
            r"(?m)^\s*([a-z][a-z0-9-]*)\s+\.(?:choice:|code:n|tl_gset:N)",
            class_text,
        )
    )
    missing_runtime_keys = sorted(setup_keys - runtime_keys)
    undeclared_runtime_keys = sorted(runtime_keys - setup_keys)
    if missing_runtime_keys:
        failures.append(
            "standards/public-api.json: setup keys missing from runtime: "
            + ", ".join(missing_runtime_keys)
        )
    if undeclared_runtime_keys:
        failures.append(
            "standards/public-api.json: runtime setup keys missing from current contract: "
            + ", ".join(undeclared_runtime_keys)
        )

    runtime_types = set(
        re.findall(
            r"(?m)^\s*type\s*/\s*([a-z][a-z0-9-]*)\s+\.code:n",
            class_text,
        )
    )
    contract_types = set(api.get("setup_values", {}).get("type", []))
    if runtime_types != contract_types:
        failures.append(
            "standards/public-api.json: type values differ from runtime: "
            f"contract={sorted(contract_types)} runtime={sorted(runtime_types)}"
        )

    missing_keys = sorted(key for key in setup_keys if f"`{key}`" not in text)
    if missing_keys:
        failures.append(
            "docs/COMMAND-REFERENCE.md: setup keys missing: " + ", ".join(missing_keys)
        )

    retained_commands = api.get("public_commands", {}).get("canonical", [])
    missing_runtime_commands = sorted(
        command for command in retained_commands if command not in class_text
    )
    if missing_runtime_commands:
        failures.append(
            "standards/public-api.json: public commands missing from runtime: "
            + ", ".join(missing_runtime_commands)
        )
    missing_commands = sorted(command for command in retained_commands if command not in text)
    if missing_commands:
        failures.append(
            "docs/COMMAND-REFERENCE.md: public commands missing: "
            + ", ".join(missing_commands)
        )

    environments = api.get("public_environments", {}).get("canonical", [])
    missing_runtime_environments = sorted(
        environment for environment in environments if environment not in class_text
    )
    if missing_runtime_environments:
        failures.append(
            "standards/public-api.json: public environments missing from runtime: "
            + ", ".join(missing_runtime_environments)
        )
    missing_environments = sorted(
        environment for environment in environments if environment not in text
    )
    if missing_environments:
        failures.append(
            "docs/COMMAND-REFERENCE.md: public environments missing: "
            + ", ".join(missing_environments)
        )

    if "scientific-article" not in text:
        failures.append(
            "docs/COMMAND-REFERENCE.md: current scientific-article profile is missing"
        )

    return failures


def main() -> None:
    guide = load_json(MAP_PATH)
    catalog = load_json(CATALOG_PATH)
    atomic = load_json(ATOMIC_PATH)

    source_ids = {source["id"] for source in catalog.get("sources", []) if "id" in source}
    rule_ids = collect_rule_ids(catalog, atomic)

    failures: list[str] = audit_reference_hygiene()
    tutorial_failures, tutorial_evidence = audit_tutorial_content()
    failures.extend(tutorial_failures)
    api_failures = audit_command_reference()
    failures.extend(api_failures)
    citation_failures, citation_evidence = audit_citation_closure()
    failures.extend(citation_failures)

    seen_topics: set[str] = set()
    passes = 0
    for topic in guide.get("topics", []):
        topic_id = topic.get("id", "<missing-id>")
        classification = topic.get("classification")
        topic_sources = topic.get("source_ids", [])
        topic_rules = topic.get("rule_ids", [])
        source_file = topic.get("source_file", "")
        marker = topic.get("marker", "")
        reasons: list[str] = []

        if topic_id in seen_topics:
            reasons.append("duplicate-topic-id")
        seen_topics.add(topic_id)

        if classification not in ALLOWED_CLASSIFICATIONS:
            reasons.append(f"invalid-classification:{classification}")
        if classification in {"normative", "institutional"}:
            if not topic_sources:
                reasons.append("sources-required")
            if not topic_rules:
                reasons.append("rules-required")

        missing_sources = sorted(set(topic_sources) - source_ids)
        if missing_sources:
            reasons.append("unknown-sources:" + ",".join(missing_sources))

        missing_rules = sorted(set(topic_rules) - rule_ids)
        if missing_rules:
            reasons.append("unknown-rules:" + ",".join(missing_rules))

        source_path = ROOT / source_file
        if not source_file or not source_path.is_file():
            reasons.append(f"missing-source-file:{source_file}")
        elif not marker:
            reasons.append("empty-marker")
        elif marker not in source_path.read_text(encoding="utf-8"):
            reasons.append(f"marker-not-found:{marker}")

        status = "FAIL" if reasons else "PASS"
        if reasons:
            failures.append(f"{topic_id}: {';'.join(reasons)}")
        else:
            passes += 1

        print(
            "GUIDE-EVIDENCE "
            f"topic={topic_id} status={status} classification={classification} "
            f"sources={len(topic_sources)} rules={len(topic_rules)}"
        )

    for item in (11, 16, 28):
        evidence = tutorial_evidence[item]
        details = " ".join(
            f"{key}={json.dumps(value, ensure_ascii=False)}"
            for key, value in evidence.items()
            if key != "status"
        )
        print(
            f"LIBRARIAN-REVIEW-EVIDENCE item={item} "
            f"status={evidence['status']} context=tutorial-reference {details}"
        )

    print(
        "GUIDE-EVIDENCE api_reference_status="
        + ("FAIL" if api_failures else "PASS")
    )
    print(
        "CANONICAL-CITATION-CLOSURE-EVIDENCE status="
        + ("FAIL" if citation_failures else "PASS")
        + f" declared={citation_evidence['declared']}"
        + f" used={citation_evidence['used']}"
        + f" missing={citation_evidence['missing']}"
    )
    print(f"GUIDE-EVIDENCE summary PASS={passes} FAIL={len(failures)} total={len(guide.get('topics', []))}")
    print("GUIDE-EVIDENCE normative_contract_changed=false")

    if failures:
        raise SystemExit("Reference guide contract failed:\n- " + "\n- ".join(failures))


if __name__ == "__main__":
    main()
