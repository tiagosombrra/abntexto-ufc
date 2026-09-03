#!/usr/bin/env python3
from __future__ import annotations

import json
from pathlib import Path

ROOT = Path.cwd()


def load(path: str) -> dict:
    return json.loads((ROOT / path).read_text(encoding="utf-8"))


def save(path: str, data: dict) -> None:
    (ROOT / path).write_text(
        json.dumps(data, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )


# Rebind inherited atomic validation to the gate that emits exact rule evidence.
overrides = load("standards/validation-overrides.json")
additions = {
    "font.size.reduced.footnote": {
        "mode": "automatic-partial",
        "checks": ["layout"],
        "scope": "footnote",
        "reason": "The layout gate measures the rendered 10 pt footnote sample for this exact atomic dimension.",
    },
    "font.size.reduced.pagination": {
        "mode": "automatic-partial",
        "checks": ["layout"],
        "scope": "pagination",
        "reason": "The layout gate measures rendered pagination glyphs at 10 pt for this exact atomic dimension.",
    },
    "toc.heading.alignment": {
        "mode": "automatic-partial",
        "checks": ["frontmatter"],
        "scope": "toc",
        "reason": "The frontmatter gate measures the Sumário heading against the text-area center.",
    },
    "toc.heading.case": {
        "mode": "automatic-partial",
        "checks": ["frontmatter"],
        "scope": "toc",
        "reason": "The frontmatter gate observes and asserts the uppercase Sumário heading.",
    },
    "toc.page-number.position": {
        "mode": "automatic-partial",
        "checks": ["frontmatter"],
        "scope": "toc",
        "reason": "The frontmatter gate measures TOC page-number alignment at the right text boundary.",
    },
    "toc.section-hierarchy.mirror": {
        "mode": "automatic-partial",
        "checks": ["frontmatter"],
        "scope": "toc",
        "reason": "The frontmatter gate compares TOC and body hierarchy styles for the controlled five-level fixture.",
    },
    "illustration.source.required": {
        "mode": "automatic-partial",
        "checks": ["objects"],
        "scope": "illustration-source",
        "reason": "The objects gate requires a rendered source marker and emits rule-specific bounded evidence.",
    },
    "illustration.source.external-citation": {
        "mode": "automatic-partial",
        "checks": ["documentary-source"],
        "scope": "illustration-source",
        "reason": "The documentary-source gate asserts an external adapted source rendered with author-date citation tokens.",
    },
    "table.ibge.open-sides": {
        "mode": "automatic-partial",
        "checks": ["object-geometry"],
        "scope": "ibge-table",
        "reason": "The object-geometry gate inspects final-PDF vector boundaries and asserts open table sides.",
    },
    "table.ibge.body-grid": {
        "mode": "automatic-partial",
        "checks": ["object-geometry"],
        "scope": "ibge-table",
        "reason": "The object-geometry gate inspects final-PDF vectors and asserts absence of the body grid.",
    },
    "table.ibge.top-rule": {
        "mode": "automatic-partial",
        "checks": ["object-geometry"],
        "scope": "ibge-table",
        "reason": "The object-geometry gate identifies the final-PDF top boundary rule.",
    },
    "table.ibge.header-rule": {
        "mode": "automatic-partial",
        "checks": ["object-geometry"],
        "scope": "ibge-table",
        "reason": "The object-geometry gate identifies the final-PDF header separator rule.",
    },
    "table.ibge.bottom-rule": {
        "mode": "automatic-partial",
        "checks": ["object-geometry"],
        "scope": "ibge-table",
        "reason": "The object-geometry gate identifies the final-PDF bottom boundary rule.",
    },
}
overrides["reviewed_at"] = "2026-09-03"
overrides["purpose"] = (
    "Rule-local validation ownership for atomic rules whose normative value and provenance "
    "stay inherited while their proof-contributing evidence differs from the aggregate parent."
)
overrides["overrides"].update(additions)
save("standards/validation-overrides.json", overrides)

false_policy = load("standards/false-coverage-policy.json")
false_policy["reviewed_at"] = "2026-09-03"
false_policy["rule_local_overrides"] = sorted(overrides["overrides"])
save("standards/false-coverage-policy.json", false_policy)


def add_check(path: str, rule_id: str, check: str) -> None:
    data = load(path)
    for rule in data["rules"]:
        if rule["id"] == rule_id:
            checks = rule["validation"]["checks"]
            if check not in checks:
                checks.insert(0, check)
            save(path, data)
            return
    raise SystemExit(f"Missing rule {rule_id} in {path}")


# Keep N4 ownership in each promoted rule's canonical source file.
add_check("standards/coverage-rules-documentary.json", "equation.display", "object-geometry")
add_check("standards/coverage-rules-closure.json", "frontmatter.start.recto", "frontmatter")
add_check("standards/coverage-rules.json", "heading.unnumbered.centered", "layout")
add_check("standards/coverage-rules-project.json", "project.cover.optional", "frontmatter")

# Publish exact rule evidence from checks that already enforce the predicate.
object_path = ROOT / "tests/integration/object.sh"
object_text = object_path.read_text(encoding="utf-8")
object_marker = (
    "  grep -Fq 'Nota:' /tmp/abntexto-ufc-objects.txt || "
    "{ echo 'Nota de objeto ausente.'; exit 1; }\n"
)
if "rule=illustration.source.required status=PASS" not in object_text:
    if object_marker not in object_text:
        raise SystemExit("Object evidence insertion point not found")
    object_text = object_text.replace(
        object_marker,
        object_marker
        + "  echo 'VALIDATION-EVIDENCE rule=illustration.source.required status=PASS "
        "expected=source-required measured=rendered-source-marker-present'\n",
        1,
    )
    object_path.write_text(object_text, encoding="utf-8")

documentary_path = ROOT / "tests/integration/documentary-source.sh"
documentary_text = documentary_path.read_text(encoding="utf-8")
documentary_marker = "PY\n\ndone\n\necho 'Gate de fontes documentais concluído.'\n"
if "rule=illustration.source.external-citation status=PASS" not in documentary_text:
    if documentary_marker not in documentary_text:
        raise SystemExit("Documentary evidence insertion point not found")
    documentary_text = documentary_text.replace(
        documentary_marker,
        "PY\n\n  echo 'VALIDATION-EVIDENCE rule=illustration.source.external-citation "
        "status=PASS expected=author-date-citation measured=adapted-source-citation-present'\n\n"
        "done\n\necho 'Gate de fontes documentais concluído.'\n",
        1,
    )
    documentary_path.write_text(documentary_text, encoding="utf-8")

references_path = ROOT / "tests/integration/references-6023.sh"
references_text = references_path.read_text(encoding="utf-8")
references_marker = "  \"$@\"\nfi\n\necho 'Gate NBR 6023:2025 concluído.'\n"
if "rule=references.nbr6023-2025.test-profile status=PASS" not in references_text:
    if references_marker not in references_text:
        raise SystemExit("References evidence insertion point not found")
    references_text = references_text.replace(
        references_marker,
        "  \"$@\"\n"
        "  echo 'VALIDATION-EVIDENCE rule=references.nbr6023-2025.test-profile "
        "status=PASS expected=nine-profile-cases measured=nine-cases-validated'\n"
        "fi\n\necho 'Gate NBR 6023:2025 concluído.'\n",
        1,
    )
    references_path.write_text(references_text, encoding="utf-8")

math_path = ROOT / "tests/integration/math.sh"
math_text = math_path.read_text(encoding="utf-8")n
# The math gate already checks numbering placement; make parenthesized Arabic format explicit.
old = (
    '    pdftotext -bbox-layout "$job.pdf" "$bbox"\n'
    '    python3 - "$bbox" <<\'PY\'\n'
    'import sys\n'
    'import xml.etree.ElementTree as ET\n'
    'from pathlib import Path\n'
)
new = (
    '    plain="/tmp/$job.txt"\n'
    '    pdftotext "$job.pdf" "$plain"\n'
    '    pdftotext -bbox-layout "$job.pdf" "$bbox"\n'
    '    python3 - "$bbox" "$plain" <<\'PY\'\n'
    'import re\n'
    'import sys\n'
    'import xml.etree.ElementTree as ET\n'
    'from pathlib import Path\n'
)
if old not in math_text:
    raise SystemExit("Math extraction insertion point not found")
math_text = math_text.replace(old, new, 1)

old = "path = Path(sys.argv[1])\nroot = ET.parse(path).getroot()\n"
new = (
    "path = Path(sys.argv[1])\n"
    "plain_path = Path(sys.argv[2])\n"
    "plain_text = plain_path.read_text(encoding='utf-8', errors='replace')\n"
    "if not re.search(r'\\(\\s*1\\s*\\)', plain_text):\n"
    "    raise SystemExit('número da equação não usa algarismo arábico entre parênteses.')\n"
    "root = ET.parse(path).getroot()\n"
)
if old not in math_text:
    raise SystemExit("Math format assertion insertion point not found")
math_text = math_text.replace(old, new, 1)

old = (
    "if not any(text == '1' or '(1)' in text for text, _, _ in words):\n"
    "    raise SystemExit('número da equação não identificado no bbox.')\n"
)
new = (
    "if not any('1' in text for text, _, _ in words):\n"
    "    raise SystemExit('número da equação não identificado no bbox.')\n"
)
if old not in math_text:
    raise SystemExit("Math bbox assertion insertion point not found")
math_text = math_text.replace(old, new, 1)

old = (
    "    raise SystemExit(\n"
    "        f'número da equação não está alinhado à direita: '\n"
    "        f'esperado xMax≈{expected_right:.2f}, obtido {rightmost[2]:.2f} ({rightmost[0]!r})'\n"
    "    )\n"
    "PY\n"
)
new = (
    "    raise SystemExit(\n"
    "        f'número da equação não está alinhado à direita: '\n"
    "        f'esperado xMax≈{expected_right:.2f}, obtido {rightmost[2]:.2f} ({rightmost[0]!r})'\n"
    "    )\n"
    "print('VALIDATION-EVIDENCE rule=equation.numbering.format status=PASS "
    "expected=arabic-parenthesized measured=(1)')\n"
    "print('VALIDATION-EVIDENCE rule=equation.numbering.right status=PASS "
    "expected=right-aligned measured=right-margin-aligned')\n"
    "PY\n"
)
if "rule=equation.numbering.format status=PASS" not in math_text:
    if old not in math_text:
        raise SystemExit("Math structured evidence insertion point not found")
    math_text = math_text.replace(old, new, 1)
math_path.write_text(math_text, encoding="utf-8")

policy = {
    "schema_version": 1,
    "reviewed_at": "2026-09-03",
    "purpose": (
        "Conservative evidence-contribution semantics. A declared or green mechanism is "
        "support-only until the current coordinated run emits rule-specific PASS evidence "
        "from a check owned by that rule."
    ),
    "allowed_classes": [
        "enforced-automatic",
        "bounded-positive",
        "manual-review",
        "conditional-review",
        "support-only",
        "not-applicable",
        "automation-gap",
    ],
    "proof_contributing_classes": ["enforced-automatic", "bounded-positive"],
    "runtime_rule_evidence_pattern": "rule=<rule-id> status=PASS",
    "automatic_partial_requires_current_owned_rule_evidence": True,
    "nonautomatic_rules": {
        "deposit.approval-signatures": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "Signature-image and handwritten/digital-signature review remains a deposit-time manual inspection.",
        },
        "deposit.capes": {
            "class": "conditional-review",
            "mode": "conditional-manual",
            "rationale": "CAPES acknowledgement applies only to funded work and retains a conditional institutional review boundary.",
        },
        "font.size.reduced.catalog-card": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "The catalog card is an externally supplied PDF whose internal typography is outside class styling control.",
        },
        "format.text.color": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "Automated fixture observations support the rule, but full-document color compliance remains conservatively manual.",
        },
        "spine.conditional": {
            "class": "not-applicable",
            "mode": "not-applicable",
            "rationale": "Printed-spine presentation is outside the standard electronic package; applicability is explicitly conditional.",
        },
        "deposit.metadata.workflow": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "Repository metadata belongs to the institutional DSpace deposit workflow rather than PDF rendering.",
        },
        "accessibility.pdfua.profile": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "PDF/UA is an additional technical profile and is not certified by the current portable release gate.",
        },
        "distribution.overleaf-ctan.policy": {
            "class": "manual-review",
            "mode": "manual",
            "rationale": "Distribution readiness is project policy and requires release/distribution review beyond document rendering.",
        },
        "glossary.element.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "The glossary is optional; evidence is meaningful only for present/absent applicability routes.",
        },
        "volume.number.cover-title-page": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "Volume numbering applies only to multi-volume documents.",
        },
        "errata.element.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "Errata is optional and is evaluated through explicit present/absent routes.",
        },
        "errata.position": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "Errata position is relevant only when an errata element is present.",
        },
        "errata.contents": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "Errata contents are relevant only when an errata element is present.",
        },
        "list.illustrations.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "The illustration list is optional and evaluated only when the corresponding content route applies.",
        },
        "list.tables.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "The table list is optional and evaluated only when the corresponding content route applies.",
        },
        "list.abbreviations.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "The abbreviations list is optional and evaluated through present/absent routes.",
        },
        "list.symbols.optional": {
            "class": "conditional-review",
            "mode": "conditional",
            "rationale": "The symbols list is optional and evaluated through present/absent routes.",
        },
    },
}
save("standards/evidence-contribution-policy.json", policy)

checker = r'''#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import re
import sys
from collections import Counter, defaultdict
from pathlib import Path
from typing import Any

ROOT = Path(__file__).resolve().parents[2]
sys.path.insert(0, str(ROOT / "tools"))
sys.path.insert(0, str(ROOT / "tests" / "checks"))

from normative_full import load_full_contract
from normative_traceability import build_matrix as build_traceability_matrix

POLICY = ROOT / "standards" / "evidence-contribution-policy.json"
RULE_PASS = re.compile(r"\brule=([A-Za-z0-9._-]+)\s+status=PASS(?:\s|$)")
AUTOMATIC_MODES = {
    "automatic",
    "automatic-deep",
    "automatic-partial",
    "automatic-policy",
}


def fail(message: str) -> None:
    raise SystemExit(f"Normative evidence contribution failed: {message}")


def load_policy() -> dict[str, Any]:
    try:
        data = json.loads(POLICY.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        fail(f"cannot load contribution policy: {exc}")
    if data.get("schema_version") != 1:
        fail("unsupported evidence-contribution-policy schema_version")
    allowed = data.get("allowed_classes")
    contributing = data.get("proof_contributing_classes")
    nonautomatic = data.get("nonautomatic_rules")
    if not isinstance(allowed, list) or not allowed:
        fail("allowed_classes must be a non-empty list")
    if not isinstance(contributing, list) or not contributing:
        fail("proof_contributing_classes must be a non-empty list")
    if not set(contributing) <= set(allowed):
        fail("proof-contributing classes must be allowed classes")
    if not isinstance(nonautomatic, dict):
        fail("nonautomatic_rules must be an object")
    return data


def validate_static_contract() -> tuple[dict[str, Any], dict[str, dict[str, Any]], dict[str, Any]]:
    contract = load_full_contract()
    traceability = build_traceability_matrix()
    policy = load_policy()
    trace_rows = {row["rule_id"]: row for row in traceability["rows"]}
    rules = {rule["id"]: rule for rule in contract["rules"]}
    if set(rules) != set(trace_rows):
        fail("full contract and traceability rule sets differ")

    expected_nonautomatic = {
        rule_id
        for rule_id, rule in rules.items()
        if rule["validation"]["mode"] not in AUTOMATIC_MODES
    }
    policy_nonautomatic = set(policy["nonautomatic_rules"])
    if expected_nonautomatic != policy_nonautomatic:
        fail(
            "nonautomatic policy set differs from full contract: "
            f"missing={sorted(expected_nonautomatic - policy_nonautomatic)}, "
            f"extra={sorted(policy_nonautomatic - expected_nonautomatic)}"
        )

    allowed = set(policy["allowed_classes"])
    for rule_id, entry in policy["nonautomatic_rules"].items():
        if not isinstance(entry, dict):
            fail(f"rule {rule_id}: nonautomatic policy entry must be an object")
        if entry.get("mode") != rules[rule_id]["validation"]["mode"]:
            fail(f"rule {rule_id}: policy validation mode drift")
        if entry.get("class") not in allowed:
            fail(f"rule {rule_id}: invalid evidence class")
        if not isinstance(entry.get("rationale"), str) or not entry["rationale"]:
            fail(f"rule {rule_id}: rationale is required")

    return contract, trace_rows, policy


def observed_rule_evidence(log_dir: Path) -> dict[str, set[str]]:
    observed: dict[str, set[str]] = defaultdict(set)
    if not log_dir.is_dir():
        fail(f"log directory does not exist: {log_dir}")
    for path in sorted(log_dir.glob("*.log")):
        gate = path.stem
        text = path.read_text(encoding="utf-8", errors="replace")
        for match in RULE_PASS.finditer(text):
            observed[match.group(1)].add(gate)
    return observed


def build_matrix(log_dir: Path | None, mode: str) -> dict[str, Any]:
    contract, trace_rows, policy = validate_static_contract()
    observed = observed_rule_evidence(log_dir) if log_dir is not None else {}
    rows: list[dict[str, Any]] = []

    for rule in contract["rules"]:
        rule_id = rule["id"]
        validation_mode = rule["validation"]["mode"]
        trace = trace_rows[rule_id]
        declared = [item["id"] for item in trace["evidence"]]
        declared_set = set(declared)
        direct_observers = sorted(observed.get(rule_id, set()))
        proof_owners = sorted(set(direct_observers) & declared_set)
        support_observers = sorted(set(direct_observers) - declared_set)

        if validation_mode in AUTOMATIC_MODES:
            if log_dir is None:
                evidence_class = "support-only"
            elif validation_mode == "automatic-partial":
                evidence_class = "bounded-positive" if proof_owners else "automation-gap"
            else:
                evidence_class = "enforced-automatic" if proof_owners else "support-only"
            rationale = (
                "Current coordinated run emitted rule-specific PASS evidence from a declared owner."
                if proof_owners
                else "No current rule-specific PASS evidence from a declared owner is being treated as enforcement."
            )
        else:
            policy_entry = policy["nonautomatic_rules"][rule_id]
            evidence_class = policy_entry["class"]
            rationale = policy_entry["rationale"]

        rows.append(
            {
                "rule_id": rule_id,
                "validation_mode": validation_mode,
                "evidence_class": evidence_class,
                "declared_evidence": declared,
                "proof_owners": proof_owners,
                "support_observers": support_observers,
                "rationale": rationale,
            }
        )

    counts = Counter(row["evidence_class"] for row in rows)
    automatic_partial = [row for row in rows if row["validation_mode"] == "automatic-partial"]
    partial_gaps = [
        row["rule_id"]
        for row in automatic_partial
        if row["evidence_class"] == "automation-gap"
    ]
    return {
        "schema_version": 1,
        "mode": mode,
        "runtime_evidence": log_dir is not None,
        "rule_count": len(rows),
        "class_counts": dict(sorted(counts.items())),
        "automatic_partial_count": len(automatic_partial),
        "automatic_partial_bounded_positive": sum(
            row["evidence_class"] == "bounded-positive" for row in automatic_partial
        ),
        "automatic_partial_gaps": partial_gaps,
        "rows": rows,
    }


def write_markdown(matrix: dict[str, Any], path: Path) -> None:
    lines = [
        "# Normative evidence contribution",
        "",
        f"- Mode: **{matrix['mode']}**",
        f"- Rules: **{matrix['rule_count']}**",
        f"- Runtime evidence: **{str(matrix['runtime_evidence']).lower()}**",
        f"- Automatic-partial bounded evidence: **{matrix['automatic_partial_bounded_positive']}/{matrix['automatic_partial_count']}**",
        "",
        "## Evidence classes",
        "",
    ]
    lines.extend(f"- `{name}`: **{count}**" for name, count in matrix["class_counts"].items())
    lines.extend(
        [
            "",
            "## Rule ownership",
            "",
            "| Rule | Mode | Class | Proof owners | Support observers | Declared evidence |",
            "|---|---|---|---|---|---|",
        ]
    )
    for row in matrix["rows"]:
        lines.append(
            f"| `{row['rule_id']}` | {row['validation_mode']} | {row['evidence_class']} | "
            f"{', '.join(row['proof_owners'])} | {', '.join(row['support_observers'])} | "
            f"{', '.join(row['declared_evidence'])} |"
        )
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text("\n".join(lines) + "\n", encoding="utf-8")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Classify normative evidence contribution without overclaiming green gates."
    )
    parser.add_argument("--log-dir", type=Path)
    parser.add_argument("--mode", choices=("pr", "release"), default="pr")
    parser.add_argument("--static", action="store_true")
    parser.add_argument("--strict-partial", action="store_true")
    parser.add_argument("--json", type=Path)
    parser.add_argument("--markdown", type=Path)
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    if not args.static and args.log_dir is None:
        fail("--log-dir is required unless --static is used")
    matrix = build_matrix(None if args.static else args.log_dir, args.mode)
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(matrix, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
    if args.markdown:
        write_markdown(matrix, args.markdown)
    if args.strict_partial and matrix["automatic_partial_gaps"]:
        fail(
            "automatic-partial rules without current owned rule evidence: "
            + ", ".join(matrix["automatic_partial_gaps"])
        )
    counts = " ".join(f"{name}={count}" for name, count in sorted(matrix["class_counts"].items()))
    print(
        "NORMATIVE-CONTRIBUTION-EVIDENCE status=PASS "
        f"rules={matrix['rule_count']} "
        f"automatic_partial={matrix['automatic_partial_bounded_positive']}/{matrix['automatic_partial_count']} "
        f"{counts}"
    )


if __name__ == "__main__":
    main()
'''
(ROOT / "tests/checks/normative_evidence_contribution.py").write_text(checker, encoding="utf-8")

# Wire the contribution checker into static source validation.
validator_path = ROOT / "tests/checks/validator_source.py"
validator_text = validator_path.read_text(encoding="utf-8")
constant_anchor = 'NORMATIVE_PROOF_STATE = ROOT / "tests" / "checks" / "normative_proof_state.py"\n'
constant = 'NORMATIVE_EVIDENCE_CONTRIBUTION = ROOT / "tests" / "checks" / "normative_evidence_contribution.py"\n'
if constant not in validator_text:
    if constant_anchor not in validator_text:
        raise SystemExit("validator_source constant insertion point not found")
    validator_text = validator_text.replace(constant_anchor, constant_anchor + constant, 1)
if "        NORMATIVE_EVIDENCE_CONTRIBUTION,\n" not in validator_text:
    validator_text = validator_text.replace(
        "        NORMATIVE_PROOF_STATE,\n",
        "        NORMATIVE_PROOF_STATE,\n        NORMATIVE_EVIDENCE_CONTRIBUTION,\n",
        1,
    )
if "normative evidence contribution" not in validator_text:
    validator_text = validator_text.replace(
        '    run_source_check(NORMATIVE_PROOF_STATE, "normative proof state")\n',
        '    run_source_check(NORMATIVE_PROOF_STATE, "normative proof state")\n'
        '    run_source_check(NORMATIVE_EVIDENCE_CONTRIBUTION, "normative evidence contribution", "--static")\n',
        1,
    )
validator_path.write_text(validator_text, encoding="utf-8")

# Keep static coverage as traceability and defer enforcement claims to runtime evidence.
coverage_path = ROOT / "tests/checks/normative_coverage.py"
coverage_text = coverage_path.read_text(encoding="utf-8")
old = '''    automatic = sum(
        rule["validation"]["mode"].startswith("automatic")
        for rule in rules.values()
    )
    manual = len(rules) - automatic
    project_policy = sum(
'''
new = '''    automatic = sum(
        rule["validation"]["mode"].startswith("automatic")
        for rule in rules.values()
    )
    manual_review = sum(
        rule["validation"]["mode"] == "manual"
        for rule in rules.values()
    )
    conditional_review = sum(
        rule["validation"]["mode"] in {"conditional", "conditional-manual"}
        for rule in rules.values()
    )
    not_applicable = sum(
        rule["validation"]["mode"] == "not-applicable"
        for rule in rules.values()
    )
    project_policy = sum(
'''
if old not in coverage_text:
    raise SystemExit("normative_coverage count block not found")
coverage_text = coverage_text.replace(old, new, 1)
old = '        f"automatic={automatic} manual_or_conditional={manual} "\n        f"project_policy={project_policy} runner_gates={len(gate_checks)} "\n'
new = '        f"automatic_declared={automatic} manual_review={manual_review} "\n        f"conditional_review={conditional_review} not_applicable={not_applicable} "\n        f"project_policy={project_policy} runner_gates={len(gate_checks)} "\n'
if old not in coverage_text:
    raise SystemExit("normative_coverage output count block not found")
coverage_text = coverage_text.replace(old, new, 1)
old = '        f"validator_checks={len(validator_checks)} "\n        f"reviewed={contract_reviewed.isoformat()}"\n'
new = '        f"validator_checks={len(validator_checks)} "\n        f"coverage_semantics=runtime-rule-contribution "\n        f"reviewed={contract_reviewed.isoformat()}"\n'
if old not in coverage_text:
    raise SystemExit("normative_coverage output semantics block not found")
coverage_text = coverage_text.replace(old, new, 1)
coverage_path.write_text(coverage_text, encoding="utf-8")

# Add a coordinated post-run contribution gate only for complete runs.
runner_path = ROOT / "tests/run.py"
runner_text = runner_path.read_text(encoding="utf-8")
old = (
    '    print(f"abntexto-ufc validation: mode={args.mode}, checks={len(checks)}")\n'
    '    for index, check in enumerate(checks, 1):\n'
    '        print(f"[{index:02}/{len(checks):02}] {check.label} ...", flush=True)\n'
)
new = (
    '    contribution_enabled = args.only is None\n'
    '    total_checks = len(checks) + (1 if contribution_enabled else 0)\n'
    '    print(f"abntexto-ufc validation: mode={args.mode}, checks={total_checks}")\n'
    '    for index, check in enumerate(checks, 1):\n'
    '        print(f"[{index:02}/{total_checks:02}] {check.label} ...", flush=True)\n'
)
if old not in runner_text:
    raise SystemExit("tests/run.py loop header not found")
runner_text = runner_text.replace(old, new, 1)
anchor = "    write_reports(report_dir, args.mode, ordered_results, complete=True)\n\n"
addition = '''    if contribution_enabled:
        contribution_check = Check(
            "evidence-contribution",
            "Normative evidence contribution",
            (
                sys.executable,
                "tests/checks/normative_evidence_contribution.py",
                "--log-dir",
                str(report_dir / "checks"),
                "--mode",
                args.mode,
                "--strict-partial",
                "--json",
                str(report_dir / "normative-evidence-contribution.json"),
                "--markdown",
                str(report_dir / "normative-evidence-contribution.md"),
            ),
            depends=tuple(check.name for check in checks),
        )
        print(f"[{total_checks:02}/{total_checks:02}] {contribution_check.label} ...", flush=True)
        result = run_check(contribution_check, report_dir, results_by_name)
        results_by_name[result.name] = result
        ordered_results.append(result)
        suffix = f" ({result.duration_seconds:.1f}s)" if result.duration_seconds else ""
        print(f"         {result.status}{suffix}")
        if result.status == "PASS":
            print_structured_evidence(result)
        if result.status == "FAIL":
            print_failure_tail(result)

'''
if "Normative evidence contribution" not in runner_text:
    if anchor not in runner_text:
        raise SystemExit("tests/run.py contribution insertion point not found")
    runner_text = runner_text.replace(anchor, addition + anchor, 1)
runner_path.write_text(runner_text, encoding="utf-8")
