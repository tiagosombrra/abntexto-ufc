#!/usr/bin/env python3
from __future__ import annotations

import re
from pathlib import Path

CHECKS = Path("tests/checks")


def replace_once(text: str, old: str, new: str, label: str) -> str:
    if old not in text:
        raise SystemExit(f"{label}: expected source block not found")
    return text.replace(old, new, 1)


# Current validation policy and vector extension names.
for path in sorted(CHECKS.glob("*.py")):
    text = path.read_text(encoding="utf-8")
    original = text
    text = text.replace(
        'ROOT / "standards" / "oracle-policy.json"',
        'ROOT / "standards" / "validation-reference-policy.json"',
    )
    text = text.replace(
        'ROOT / "standards" / "vector-rule-oracle-extension.json"',
        'ROOT / "standards" / "vector-rule-validation-extension.json"',
    )
    text = text.replace(
        'ROOT / "standards" / "n11-project-structure-final-pdf-scenario.json"',
        'ROOT / "standards" / "research-project-structure-final-pdf-scenario.json"',
    )
    if "validation-reference-policy.json" in text:
        text = text.replace("ORACLE_POLICY", "VALIDATION_POLICY")
        text = re.sub(r"\boracle\b", "validation", text)
        text = re.sub(r"\bOracle\b", "Validation", text)
        replacements = {
            "oracle policy": "validation reference policy",
            "oracle-policy": "validation-reference-policy",
            "oracle extension": "validation extension",
            "oracle-extension": "validation-extension",
            "oracle configuration": "validation configuration",
            "N5 oracle policy": "validation reference policy",
            "N5 tolerances": "validation tolerances",
            "N5 font-size tolerance": "validation font-size tolerance",
            "N5 vertical tolerance": "validation vertical tolerance",
            "N5 vector-rule-geometry capability": "vector-rule-geometry capability",
            "n5_vertical_tolerance": "validation_vertical_tolerance",
        }
        for old, new in replacements.items():
            text = text.replace(old, new)
        text = text.replace(
            'validation.get("schema_version") != 1',
            'validation.get("schema_version") != 2',
        )
        text = re.sub(
            r"\s*or\s+validation\.get\(\"phase\"\)\s*!=\s*\"N5\"",
            "",
            text,
        )
        text = re.sub(
            r"validation\.get\(\"phase\"\)\s*!=\s*\"N5\"\s*or\s*",
            "",
            text,
        )
    if text != original:
        path.write_text(text, encoding="utf-8")


# Deleted campaign plans are replaced by scenario/full-contract/locator invariants.
for name, next_statement in {
    "normative_equation_display.py": "presentation_rules",
    "normative_illustration.py": "reduced",
    "normative_table_typography.py": "reduced",
    "normative_table_ibge_vector.py": "located",
}.items():
    path = CHECKS / name
    text = path.read_text(encoding="utf-8")
    text = re.sub(r"^CAMPAIGN_PLAN = .*\n", "", text, flags=re.MULTILINE)
    text = re.sub(
        r"^\s*plan = load_json\(CAMPAIGN_PLAN\)\n",
        "",
        text,
        flags=re.MULTILINE,
    )
    pattern = rf"\n    campaigns = .*?(?=\n    {re.escape(next_statement)} = )"
    text, count = re.subn(pattern, "\n", text, count=1, flags=re.DOTALL)
    if count != 1:
        raise SystemExit(f"{name}: deleted campaign-plan block not found")
    path.write_text(text, encoding="utf-8")


# Appendix/annex: remove deleted N10 scope ledger and bind scenario directly.
path = CHECKS / "normative_appendix_annex.py"
text = path.read_text(encoding="utf-8")
text = re.sub(r"^N10_SCOPE = .*\n", "", text, flags=re.MULTILINE)
text = re.sub(
    r'^\s*scope = load_json\(N10_SCOPE, "N10 scope"\)\n',
    "",
    text,
    flags=re.MULTILINE,
)
start = text.find("    campaign = next(")
end = text.find("    rules = {rule[\"id\"]", start)
if start < 0 or end < 0:
    raise SystemExit("normative_appendix_annex.py: deleted scope block not found")
text = (
    text[:start]
    + '    scenario_rules = scenario.get("rules")\n'
      '    if not isinstance(scenario_rules, list) or len(scenario_rules) != 13:\n'
      '        fail("scenario rule scope is invalid")\n\n'
    + text[end:]
)
needle = "    for rule_id, value in supported.items():\n"
text = replace_once(
    text,
    needle,
    '    if set(scenario_rules) != set(supported):\n'
    '        fail("scenario rules drifted from the supported full-contract scope")\n\n'
    + needle,
    "normative_appendix_annex.py",
)
path.write_text(text, encoding="utf-8")


# Index/glossary: same semantic scope binding.
path = CHECKS / "normative_index_glossary.py"
text = path.read_text(encoding="utf-8")
text = re.sub(r"^N10_SCOPE = .*\n", "", text, flags=re.MULTILINE)
text = re.sub(
    r'^\s*scope = load_json\(N10_SCOPE, "N10 scope"\)\n',
    "",
    text,
    flags=re.MULTILINE,
)
start = text.find("    campaign = next(")
end = text.find("    rules = {rule[\"id\"]", start)
if start < 0 or end < 0:
    raise SystemExit("normative_index_glossary.py: deleted scope block not found")
text = (
    text[:start]
    + '    scenario_rules = scenario.get("rules")\n'
      '    if not isinstance(scenario_rules, list) or len(scenario_rules) != 5:\n'
      '        fail("scenario rule scope is invalid")\n\n'
    + text[end:]
)
needle = "    for rule_id, expected in supported.items():\n"
text = replace_once(
    text,
    needle,
    '    if set(scenario_rules) != set(supported):\n'
    '        fail("scenario rules drifted from the supported full-contract scope")\n\n'
    + needle,
    "normative_index_glossary.py",
)
path.write_text(text, encoding="utf-8")


# Research-project evidence: scope is the scenario + current full contract, not a campaign ledger.
path = CHECKS / "normative_research_project_structure.py"
text = path.read_text(encoding="utf-8")
text = re.sub(r"^SCOPE = .*\n", "", text, flags=re.MULTILINE)
text = re.sub(r"^\s*scope = load_json\(SCOPE\)\n", "", text, flags=re.MULTILINE)
text = text.replace('    support_ids = set(scope.get("support_only_rule_ids", []))\n', "")
old = '''    if rule_ids != expected_rule_ids or support_ids != expected_rule_ids:
        fail(
            "campaign/scope mismatch: "
            f"scenario={sorted(rule_ids)} support={sorted(support_ids)}"
        )
'''
new = '''    if rule_ids != expected_rule_ids:
        fail(f"scenario rule scope drifted: {sorted(rule_ids)}")
'''
text = replace_once(text, old, new, "normative_research_project_structure.py")
text, count = re.subn(
    r'\n    expected_progress = scenario\.get\("expected_progress", \{\}\).*?(?=\n    payload = \{)',
    "\n",
    text,
    count=1,
    flags=re.DOTALL,
)
if count != 1:
    raise SystemExit("normative_research_project_structure.py: progress ledger block not found")
text = text.replace('        "bounded_progress": progress,\n', "")
text = text.replace('        "bounded_progress_mismatches": progress_mismatches,\n', "")
print_start = text.find('    print(\n        "N11-EVIDENCE bounded-progress "')
if print_start >= 0:
    print_end = text.find("\n    if args.enforce", print_start)
    if print_end < 0:
        raise SystemExit("normative_research_project_structure.py: progress print boundary missing")
    text = text[:print_start] + text[print_end:]
text = re.sub(
    r'\n    if progress_mismatches:\n        fail\(.*?\n        \)\n',
    "\n",
    text,
    count=1,
    flags=re.DOTALL,
)
path.write_text(text, encoding="utf-8")


# Deleted coverage audit was process evidence, not a current normative source.
path = CHECKS / "normative_currency.py"
text = path.read_text(encoding="utf-8")
text = re.sub(
    r'^\s*ROOT / "standards" / "coverage-audit\.json",\n',
    "",
    text,
    flags=re.MULTILINE,
)
path.write_text(text, encoding="utf-8")


# Deleted N9 scope ledger becomes a semantic current-contract integrity check.
(CHECKS / "normative_objects_scope.py").write_text(
    '''#!/usr/bin/env python3
from __future__ import annotations

import ast
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))

from normative_full import load_full_contract

TARGET_CATEGORIES = {"objects", "equations", "code-algorithms"}
CROSS_CUTTING_RULE_IDS = {
    "font.size.reduced.illustration-caption",
    "font.size.reduced.illustration-source",
    "font.size.reduced.table-caption",
    "font.size.reduced.table-source",
}
EXPECTED_PROJECT_POLICY = {
    "code.listing.project-policy",
    "algorithm.project-policy",
}


def fail(message: str) -> None:
    raise SystemExit(f"Objects scope integrity failed: {message}")


def runner_ids() -> set[str]:
    source = (ROOT / "tests" / "run.py").read_text(encoding="utf-8")
    module = ast.parse(source)
    result: set[str] = set()
    for node in ast.walk(module):
        if not isinstance(node, ast.Call):
            continue
        if not isinstance(node.func, ast.Name) or node.func.id != "Check":
            continue
        if not node.args or not isinstance(node.args[0], ast.Constant):
            continue
        if isinstance(node.args[0].value, str):
            result.add(node.args[0].value)
    return result


def main() -> None:
    contract = load_full_contract()
    rules = {rule["id"]: rule for rule in contract["rules"]}
    scoped = {
        rule_id
        for rule_id, rule in rules.items()
        if rule.get("category") in TARGET_CATEGORIES
    } | CROSS_CUTTING_RULE_IDS

    if len(scoped) != 23:
        fail(f"expected 23 current scoped rules, got {len(scoped)}")
    missing_cross = sorted(CROSS_CUTTING_RULE_IDS - set(rules))
    if missing_cross:
        fail("missing cross-cutting rules: " + ", ".join(missing_cross))

    for rule_id in CROSS_CUTTING_RULE_IDS:
        if rules[rule_id].get("values") != {"pt": 10}:
            fail(f"{rule_id}: expected 10 pt current contract")

    observed_project_policy = {
        rule_id for rule_id in scoped if rules[rule_id].get("authority") == "project-policy"
    }
    if observed_project_policy != EXPECTED_PROJECT_POLICY:
        fail("project-policy boundary drifted: " + repr(sorted(observed_project_policy)))
    for rule_id in EXPECTED_PROJECT_POLICY:
        if rules[rule_id].get("values") != {"supported": True, "normative_claim": False}:
            fail(f"{rule_id}: project-policy values drifted")
    for rule_id in sorted(scoped - EXPECTED_PROJECT_POLICY):
        if rules[rule_id].get("authority") != "normative":
            fail(f"{rule_id}: unexpected non-normative authority")

    gates = runner_ids()
    uncovered = sorted(
        rule_id
        for rule_id in scoped
        if not (set(rules[rule_id]["validation"]["checks"]) & gates)
    )
    if uncovered:
        fail("current scoped rules without unified validation gate: " + ", ".join(uncovered))

    print(
        "OBJECTS-SCOPE-EVIDENCE "
        f"rules={len(scoped)} project_policy={len(EXPECTED_PROJECT_POLICY)} "
        f"cross_cutting={len(CROSS_CUTTING_RULE_IDS)} uncovered=0"
    )


if __name__ == "__main__":
    main()
''',
    encoding="utf-8",
)


# Validation policy schema is current and phase-free.
residual_policy_phase: list[str] = []
for path in sorted(CHECKS.glob("*.py")):
    text = path.read_text(encoding="utf-8")
    if "validation-reference-policy.json" in text and 'validation.get("phase")' in text:
        residual_policy_phase.append(path.as_posix())
if residual_policy_phase:
    raise SystemExit(
        "Validation policy consumers still require a deleted phase:\n"
        + "\n".join(residual_policy_phase)
    )
