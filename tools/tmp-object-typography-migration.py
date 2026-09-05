#!/usr/bin/env python3
from __future__ import annotations

import json
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
RETIRED = {
    "font.size.reduced.illustration-caption": "illustration.identification.font-size",
    "font.size.reduced.table-caption": "table.identification.font-size",
}


def load_json(relative: str) -> dict:
    return json.loads((ROOT / relative).read_text(encoding="utf-8"))


def write_json(relative: str, data: dict) -> None:
    (ROOT / relative).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


def replace_once(relative: str, old: str, new: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    count = text.count(old)
    if count != 1:
        raise SystemExit(f"{relative}: expected one replacement match, found {count}: {old!r}")
    path.write_text(text.replace(old, new), encoding="utf-8")


def append_before(relative: str, marker: str, block: str) -> None:
    path = ROOT / relative
    text = path.read_text(encoding="utf-8")
    if block.strip() in text:
        return
    if marker not in text:
        raise SystemExit(f"{relative}: insertion marker not found: {marker!r}")
    path.write_text(text.replace(marker, block.rstrip() + "\n\n" + marker, 1), encoding="utf-8")


# 1. Compatibility parent: reduced-font exceptions no longer include upper titles.
catalog = load_json("standards/catalog.json")
parent = next(rule for rule in catalog["rules"] if rule["id"] == "font.size.reduced")
parent["applies_to"] = [
    item
    for item in parent["applies_to"]
    if item not in {"illustration-caption", "table-caption"}
]
write_json("standards/catalog.json", catalog)

# 2. N3 atomic split: retire the two semantically incorrect reduced-title children.
atomic = load_json("standards/atomic-rules.json")
atomic["reviewed_at"] = "2026-09-05"
group = atomic["groups"]["font.size.reduced"]
atomic["groups"]["font.size.reduced"] = [
    spec for spec in group if spec.get("id") not in RETIRED
]
write_json("standards/atomic-rules.json", atomic)

plan = load_json("standards/atomicity-plan.json")
plan["reviewed_at"] = "2026-09-05"
targets = plan["rules"]["font.size.reduced"]["targets"]
plan["rules"]["font.size.reduced"]["targets"] = [
    rule_id for rule_id in targets if rule_id not in RETIRED
]
write_json("standards/atomicity-plan.json", plan)

# 3. Promote semantically correct institutional title-size rules.
coverage = load_json("standards/coverage-rules-documentary.json")
coverage["reviewed_at"] = "2026-09-05"
coverage["rules"] = [
    rule
    for rule in coverage["rules"]
    if rule.get("id") not in set(RETIRED.values())
]
coverage["rules"].extend(
    [
        {
            "id": "illustration.identification.font-size",
            "category": "objects",
            "requirement": "A identificação/título superior da ilustração usa o tamanho-base de 12 pt; a exceção de tamanho reduzido aplica-se aos textos auxiliares inferiores previstos pelo guia.",
            "locator": "Guia UFC 2022, 4.1(c) e 4.9(c-e)",
            "normativity": "required",
            "kind": "font-size",
            "values": {"pt": 12},
            "validation": {
                "mode": "automatic-partial",
                "checks": ["object-geometry"],
            },
            "scope": "institutional",
            "sources": ["ufc-guia-trabalhos-2022"],
        },
        {
            "id": "table.identification.font-size",
            "category": "objects",
            "requirement": "A identificação/título superior da tabela usa o tamanho-base de 12 pt; a exceção de tamanho reduzido aplica-se aos textos auxiliares inferiores previstos pelo guia.",
            "locator": "Guia UFC 2022, 4.1(c) e 4.10(b-c)",
            "normativity": "required",
            "kind": "font-size",
            "values": {"pt": 12},
            "validation": {
                "mode": "automatic-partial",
                "checks": ["object-geometry"],
            },
            "scope": "institutional",
            "sources": ["ufc-guia-trabalhos-2022"],
        },
    ]
)
write_json("standards/coverage-rules-documentary.json", coverage)

# 4. Correct locator ownership: upper identification/title is separate from reduced lower text.
locator = load_json("standards/locator-audit-typography-paragraphs.json")
locator["reviewed_at"] = "2026-09-05"
reduced = next(item for item in locator["rulesets"] if item["id"] == "typography.reduced-font")
reduced["rule_ids"] = [rule_id for rule_id in reduced["rule_ids"] if rule_id not in RETIRED]
new_ruleset = {
    "id": "typography.object-identification-title",
    "rule_ids": [
        "illustration.identification.font-size",
        "table.identification.font-size",
    ],
    "current_locator": "UFC 4.1(c), 4.9(c-e), 4.10(b-c)",
    "status": "VERIFIED",
    "source_checks": [
        {
            "source_id": "ufc-guia-trabalhos-2022",
            "locator": "4.1(c); 4.9(c-e); 4.10(b-c)",
            "status": "VERIFIED",
            "checked_at": "2026-09-05",
            "basis_url": "https://biblioteca.ufc.br/wp-content/uploads/2022/05/guianormalizacaotrabalhosacademicos-17.05.2022.pdf",
        }
    ],
}
locator["rulesets"] = [
    item for item in locator["rulesets"] if item.get("id") != new_ruleset["id"]
]
insert_at = next(i for i, item in enumerate(locator["rulesets"]) if item["id"] == "typography.reduced-font") + 1
locator["rulesets"].insert(insert_at, new_ruleset)
write_json("standards/locator-audit-typography-paragraphs.json", locator)

# 5. Scenario contracts follow the corrected semantics.
illustration_scenario = load_json("standards/illustration-final-pdf-scenario.json")
illustration_scenario["reviewed_at"] = "2026-09-05"
illustration_scenario["purpose"] = "Bounded final-PDF evidence for upper illustration identification/title size, reduced source size, bounds and relative-position predicates."
illustration_scenario["rules"] = [
    RETIRED.get(rule_id, rule_id) for rule_id in illustration_scenario["rules"]
]
loc_map = illustration_scenario["locator_rulesets"]
loc_map["illustration.identification.font-size"] = "typography.object-identification-title"
loc_map.pop("font.size.reduced.illustration-caption", None)
illustration_scenario["measurement"]["typography"] = "upper identification/title is measured at 12 pt and lower source at 10 pt using pdftohtml XML and the shared font-size tolerance"
write_json("standards/illustration-final-pdf-scenario.json", illustration_scenario)

table_scenario = load_json("standards/table-typography-final-pdf-scenario.json")
table_scenario["reviewed_at"] = "2026-09-05"
table_scenario["purpose"] = "Measure upper table identification/title at 12 pt and lower source at reduced 10 pt directly from an isolated final PDF."
table_scenario["rules"] = [RETIRED.get(rule_id, rule_id) for rule_id in table_scenario["rules"]]
table_scenario.pop("locator_ruleset", None)
table_scenario["locator_rulesets"] = {
    "table.identification.font-size": "typography.object-identification-title",
    "font.size.reduced.table-source": "typography.reduced-font",
}
write_json("standards/table-typography-final-pdf-scenario.json", table_scenario)

# 6. Runtime: upper identification/title returns to body size, lower source/note paths remain unchanged.
replace_once(
    "abntexto-ufc/objects.def",
    "% Keep object titles within the real object width and use the reduced normative size.",
    "% Keep upper object identification/title within the real object width at body size.",
)
replace_once(
    "abntexto-ufc/objects.def",
    "  \\abntsmall\\singlesp\n  \\ufcObjectLegendHook",
    "  \\normalsize\\singlesp\n  \\ufcObjectLegendHook",
)

# 7. Final-PDF checkers use separate title/source contracts.
replace_once(
    "tests/checks/normative_illustration.py",
    '    "font.size.reduced.illustration-caption",',
    '    "illustration.identification.font-size",',
)
replace_once(
    "tests/checks/normative_illustration.py",
    '    "font.size.reduced.illustration-caption": {"pt": 10},',
    '    "illustration.identification.font-size": {"pt": 12},',
)
replace_once(
    "tests/checks/normative_illustration.py",
    '    reduced = ruleset(loc_typ, "typography.reduced-font").get("rule_ids", [])\n    if not {RULES[0], RULES[1]} <= set(reduced):\n        fail("illustration reduced-font locator scope drift")',
    '    reduced = ruleset(loc_typ, "typography.reduced-font").get("rule_ids", [])\n    title_size = ruleset(loc_typ, "typography.object-identification-title").get("rule_ids", [])\n    if RULES[1] not in set(reduced):\n        fail("illustration source reduced-font locator scope drift")\n    if RULES[0] not in set(title_size):\n        fail("illustration identification/title locator scope drift")',
)
replace_once(
    "tests/checks/normative_illustration.py",
    "    cap_font_delta = abs(cap_run.font_size - 10.0)\n    src_font_delta = abs(src_run.font_size - 10.0)",
    "    cap_font_delta = abs(cap_run.font_size - 12.0)\n    src_font_delta = abs(src_run.font_size - 10.0)",
)

replace_once(
    "tests/checks/normative_table_typography.py",
    '    "font.size.reduced.table-caption",',
    '    "table.identification.font-size",',
)
replace_once(
    "tests/checks/normative_table_typography.py",
    'EXPECTED = {rule_id: {"pt": 10} for rule_id in RULES}',
    'EXPECTED = {\n    "table.identification.font-size": {"pt": 12},\n    "font.size.reduced.table-source": {"pt": 10},\n}',
)
replace_once(
    "tests/checks/normative_table_typography.py",
    '    reduced = ruleset(locator, "typography.reduced-font").get("rule_ids", [])\n    if not set(RULES) <= set(reduced):\n        fail("table reduced-font locator scope drifted")',
    '    reduced = ruleset(locator, "typography.reduced-font").get("rule_ids", [])\n    title_size = ruleset(locator, "typography.object-identification-title").get("rule_ids", [])\n    if RULES[1] not in set(reduced):\n        fail("table source reduced-font locator scope drifted")\n    if RULES[0] not in set(title_size):\n        fail("table identification/title locator scope drifted")',
)
replace_once(
    "tests/checks/normative_table_typography.py",
    "        delta = abs(run.font_size - 10.0)",
    "        expected_pt = float(EXPECTED[rule_id][\"pt\"])\n        delta = abs(run.font_size - expected_pt)",
)

# 8. Scope/count contracts reflect two N3 retirements and two N4 promotions.
replace_once(
    "tests/checks/normative_objects_scope.py",
    'CROSS_CUTTING_RULE_IDS = {\n    "font.size.reduced.illustration-caption",\n    "font.size.reduced.illustration-source",\n    "font.size.reduced.table-caption",\n    "font.size.reduced.table-source",\n}',
    'CROSS_CUTTING_RULE_IDS = {\n    "font.size.reduced.illustration-source",\n    "font.size.reduced.table-source",\n}',
)
replace_once(
    "tests/checks/normative_atomicity.py",
    '    if keep_count + target_count != 100:\n        fail("N3 contract must resolve to exactly 100 atomic rules")',
    '    if keep_count + target_count != 98:\n        fail("N3 contract must resolve to exactly 98 atomic rules after object-title migration")',
)
replace_once(
    "tests/checks/normative_atomic_contract.py",
    '    if len(atomic) != 100:\n        fail(f"expected 100 N3 atomic rules, got {len(atomic)}")',
    '    if len(atomic) != 98:\n        fail(f"expected 98 N3 atomic rules after object-title migration, got {len(atomic)}")',
)
replace_once(
    "tests/checks/normative_full_contract.py",
    "BASE_RULE_COUNT = 100",
    "BASE_RULE_COUNT = 98",
)

# Object geometry directly checks title=12 and lower source/note=10.
replace_once(
    "tests/integration/object-geometry.sh",
    "expected_small = 10.0 * pt_per_bp\n\nclose('largura física do objeto', dim('UFC-OBJECT-CONTENT-WIDTH'), expected_width)\nfor name in ('UFC-OBJECT-TITLE-WIDTH', 'UFC-OBJECT-SOURCE-WIDTH', 'UFC-OBJECT-NOTE-WIDTH'):\n    close(name, dim(name), expected_width)\nfor name in ('UFC-OBJECT-TITLE-FONTSIZE', 'UFC-OBJECT-SOURCE-FONTSIZE', 'UFC-OBJECT-NOTE-FONTSIZE'):\n    close(name, scalar(name), expected_small)",
    "expected_body = 12.0 * pt_per_bp\nexpected_small = 10.0 * pt_per_bp\n\nclose('object physical width', dim('UFC-OBJECT-CONTENT-WIDTH'), expected_width)\nfor name in ('UFC-OBJECT-TITLE-WIDTH', 'UFC-OBJECT-SOURCE-WIDTH', 'UFC-OBJECT-NOTE-WIDTH'):\n    close(name, dim(name), expected_width)\nclose('UFC-OBJECT-TITLE-FONTSIZE', scalar('UFC-OBJECT-TITLE-FONTSIZE'), expected_body)\nfor name in ('UFC-OBJECT-SOURCE-FONTSIZE', 'UFC-OBJECT-NOTE-FONTSIZE'):\n    close(name, scalar(name), expected_small)",
)
replace_once(
    "tests/integration/object-geometry.sh",
    '    echo "$job: warning ou overflow não reconhecido."',
    '    echo "$job: unrecognized warning or overflow."',
)

# 9. Explicit provenance for retired rule IDs.
migrations = {
    "schema_version": 1,
    "reviewed_at": "2026-09-05",
    "purpose": "Preserve provenance when a previously active rule ID is retired because its semantic classification was incorrect.",
    "migrations": [
        {
            "retired_id": retired,
            "replacement_id": replacement,
            "status": "semantic-correction",
            "retired_value": {"pt": 10},
            "replacement_value": {"pt": 12},
            "reason": "The retired reduced-font child conflated the upper identification/title with the lower legend/source reduced-font exception in UFC guidance.",
            "decision": "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md",
        }
        for retired, replacement in RETIRED.items()
    ],
}
write_json("standards/rule-migrations.json", migrations)

migration_checker = '''#!/usr/bin/env python3
from __future__ import annotations

import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
from normative_full import load_full_contract

MIGRATIONS = ROOT / "standards" / "rule-migrations.json"
EXPECTED = {
    "font.size.reduced.illustration-caption": "illustration.identification.font-size",
    "font.size.reduced.table-caption": "table.identification.font-size",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative rule migration failed: {message}")


def main() -> None:
    data = json.loads(MIGRATIONS.read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        fail("unsupported migration schema")
    rows = data.get("migrations")
    if not isinstance(rows, list) or len(rows) != 2:
        fail("object-title migration must contain exactly two rows")
    observed = {row.get("retired_id"): row.get("replacement_id") for row in rows}
    if observed != EXPECTED:
        fail(f"unexpected migration mapping: {observed}")

    rules = {rule["id"]: rule for rule in load_full_contract()["rules"]}
    for row in rows:
        retired = row["retired_id"]
        replacement = row["replacement_id"]
        if retired in rules:
            fail(f"retired rule remains active: {retired}")
        if replacement not in rules:
            fail(f"replacement rule is missing: {replacement}")
        if row.get("retired_value") != {"pt": 10}:
            fail(f"retired value provenance drifted: {retired}")
        if row.get("replacement_value") != {"pt": 12}:
            fail(f"replacement value provenance drifted: {replacement}")
        if rules[replacement].get("values") != {"pt": 12}:
            fail(f"active replacement value drifted: {replacement}")
        if row.get("status") != "semantic-correction":
            fail(f"migration status drifted: {retired}")
        if row.get("decision") != "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md":
            fail(f"migration decision provenance drifted: {retired}")

    print("RULE-MIGRATION-EVIDENCE status=PASS retired=2 replacements=2 semantic_corrections=2")


if __name__ == "__main__":
    main()
'''
(ROOT / "tests/checks/normative_rule_migrations.py").write_text(migration_checker, encoding="utf-8")

replace_once(
    "tests/static.py",
    '    "tests/checks/normative_objects_scope.py",',
    '    "tests/checks/normative_rule_migrations.py",\n    "tests/checks/normative_objects_scope.py",',
)

# 10. Synchronize documentation with the material implementation advance, but keep item 21 open until CI proves it.
replace_once(
    "docs/UFC-LIBRARIAN-REVIEW.md",
    "| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | FAIL — authority reconciled; current runtime/test contract still renders upper identification/title at 10 pt. | `objects.def`, normative contract, object final-PDF checks |",
    "| 21 | Figure/table/object upper identification/title must use body-size typography (12 pt); lower legend/source/note remain reduced where applicable. | FAIL — implementation candidate migrated runtime/contract/evidence to 12 pt upper title; Static/full Linux confirmation is still required before closure. | `objects.def`, normative contract, object final-PDF checks |",
)
replace_once(
    "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md",
    "Status: ACCEPTED FOR CORE CORRECTIONS IMPLEMENTATION",
    "Status: IMPLEMENTED — CI CONFIRMATION PENDING",
)
append_before(
    "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md",
    "## Current-edition technical boundary",
    "## Implementation checkpoint state\n\nThe runtime, active normative contract, locator ownership and final-PDF expectations have now been migrated according to this decision. The historical 10 pt title IDs are preserved only through `standards/rule-migrations.json`; they are no longer active rules. Item 21 remains `FAIL` until Static contract and full Linux integration prove the generated candidate, including measured 12 pt upper identification/title and 10 pt lower source evidence.",
)
append_before(
    "docs/HANDOFF-V3.0.0.md",
    "## Phase-end regression rule",
    "## Object typography implementation candidate\n\nThe active object batch has migrated the runtime, normative contract, locator ownership and final-PDF expectations to 12 pt upper identification/title and 10 pt lower source/note behavior. The two historically incorrect reduced-title rule IDs are retired with explicit provenance in `standards/rule-migrations.json`. Item 21 remains `FAIL` until the candidate passes Static contract and full Linux integration; the latest fully validated checkpoint remains `f6ca012164273e67480dca127fe17b392e8a8a21` until then.",
)
replace_once(
    "docs/V3-CORRECTION-PLAN.md",
    "Current defect: `abntexto-ufc/objects.def` applies `\\abntsmall` to the complete upper `\\printlegendbox`, and the final-PDF rule set currently certifies 10 pt upper titles.",
    "Implementation candidate: `abntexto-ufc/objects.def`, the active normative contract, locator ownership and final-PDF rules have been migrated to the accepted 12 pt upper-title semantics. Item 21 intentionally remains FAIL until Static/full Linux evidence is green.",
)
replace_once(
    "docs/ROADMAP-V3.0.0.md",
    "The implementation batch must update runtime, normative contract, locator audits and final-PDF evidence atomically. Item 21 remains FAIL until the corrected final-PDF measurements pass.",
    "The implementation batch has now updated runtime, normative contract, locator audits and final-PDF evidence atomically. Item 21 remains FAIL while Static/full Linux confirmation is pending; only green corrected final-PDF measurements can close it.",
)
roadmap = load_json("release/v3-roadmap.json")
roadmap["active_work"]["object_typography_implementation_state"] = "implemented-ci-pending"
roadmap["active_work"]["object_typography_rule_migration_manifest"] = "standards/rule-migrations.json"
roadmap["authority_decisions"]["object_typography"]["current_state"] = "IMPLEMENTED-CI-PENDING"
write_json("release/v3-roadmap.json", roadmap)

# 11. Fail if retired IDs remain in active technical surfaces outside the explicit migration/decision provenance.
allowed_retired_paths = {
    "standards/rule-migrations.json",
    "docs/V3-OBJECT-TYPOGRAPHY-DECISION.md",
}
for retired in RETIRED:
    completed = subprocess.run(
        ["git", "grep", "-n", "--", retired],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )
    if completed.returncode not in {0, 1}:
        raise SystemExit(completed.stderr)
    unexpected = []
    for line in completed.stdout.splitlines():
        path = line.split(":", 1)[0]
        if path not in allowed_retired_paths:
            unexpected.append(line)
    if unexpected:
        raise SystemExit("retired rule ID leaked outside provenance surfaces:\n" + "\n".join(unexpected))

# 12. Temporary executor lifecycle closes before the generated checkpoint.
for relative in (
    "tools/tmp-object-typography-migration.py",
    ".github/workflows/tmp-object-typography-migration.yml",
):
    path = ROOT / relative
    if path.exists():
        path.unlink()

print("OBJECT-TYPOGRAPHY-MIGRATION status=PREPARED retired=2 promoted=2 upper_title_pt=12 lower_source_pt=10")
