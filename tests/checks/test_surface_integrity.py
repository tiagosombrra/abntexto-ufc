#!/usr/bin/env python3
from __future__ import annotations

import ast
import json
import runpy
from collections import deque
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
RUNNER = ROOT / "tests/run.py"
STATIC_RUNNER = ROOT / "tests/static.py"
MAKEFILE = ROOT / "Makefile"
EVIDENCE_REGISTRY = ROOT / "standards/evidence-registry.json"
NEGATIVE_PATHS = ROOT / "standards/negative-paths.json"
CANDIDATE_ROOTS = (ROOT / "tests/checks", ROOT / "tests/integration")
CANDIDATE_SUFFIXES = {".py", ".sh"}
CONTROL_ROOTS = (
    ROOT / "tests/checks",
    ROOT / "tests/integration",
    ROOT / "tools",
    ROOT / "validator",
    ROOT / ".github/workflows",
)
CONTROL_SUFFIXES = {".py", ".sh", ".ps1", ".js", ".json", ".yml", ".yaml"}
PERMANENT_WORKFLOWS = (
    ROOT / ".github/workflows/static-contract.yml",
    ROOT / ".github/workflows/linux-integration.yml",
    ROOT / ".github/workflows/linux-release-check.yml",
)


def fail(message: str) -> None:
    raise SystemExit(f"Test surface integrity failed: {message}")


def repository_path(value: str) -> Path | None:
    candidate = value.strip("'\"(),[]{}")
    if not candidate.startswith(("tests/", "tools/", "validator/", "standards/")):
        return None
    path = ROOT / candidate
    return path if path.exists() else None


def collect_files(roots: tuple[Path, ...], suffixes: set[str]) -> set[Path]:
    files: set[Path] = set()
    for root in roots:
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if path.is_file() and path.suffix in suffixes:
                files.add(path)
    return files


def candidate_files() -> set[Path]:
    return collect_files(CANDIDATE_ROOTS, CANDIDATE_SUFFIXES)


def control_files(candidates: set[Path]) -> set[Path]:
    files = collect_files(CONTROL_ROOTS, CONTROL_SUFFIXES)
    files.update(candidates)
    files.update({RUNNER, STATIC_RUNNER, MAKEFILE})
    return {path for path in files if path.is_file()}


def python_import_targets(nodes: set[Path]) -> dict[str, Path]:
    by_stem: dict[str, Path] = {}
    duplicates: set[str] = set()
    for path in nodes:
        if path.suffix != ".py":
            continue
        stem = path.stem
        if stem in by_stem:
            duplicates.add(stem)
        else:
            by_stem[stem] = path
    for stem in duplicates:
        by_stem.pop(stem, None)
    return by_stem


def direct_references(source: Path, nodes: set[Path], by_stem: dict[str, Path]) -> set[Path]:
    text = source.read_text(encoding="utf-8")
    references = {
        target
        for target in nodes
        if target != source and target.relative_to(ROOT).as_posix() in text
    }
    if source.suffix != ".py":
        return references

    try:
        tree = ast.parse(text, filename=str(source))
    except SyntaxError as exc:
        fail(f"cannot parse {source.relative_to(ROOT)} while building reference graph: {exc}")

    for node in ast.walk(tree):
        modules: list[str] = []
        if isinstance(node, ast.Import):
            modules.extend(alias.name for alias in node.names)
        elif isinstance(node, ast.ImportFrom) and node.module:
            modules.append(node.module)
        for module in modules:
            stem = module.rsplit(".", 1)[-1]
            target = by_stem.get(stem)
            if target is not None and target != source:
                references.add(target)
    return references


def collect_registry_scripts(registry: dict[str, object]) -> set[Path]:
    scripts: set[Path] = set()
    evidence = registry.get("evidence")
    if not isinstance(evidence, list):
        fail("evidence registry has no evidence list")
    for item in evidence:
        if not isinstance(item, dict):
            fail("evidence registry contains a non-object entry")
        target = item.get("target", {})
        if not isinstance(target, dict):
            fail(f"evidence {item.get('id')} has a non-object target")
        values: list[str] = []
        script = target.get("script")
        if isinstance(script, str):
            values.append(script)
        more = target.get("scripts")
        if isinstance(more, list):
            values.extend(value for value in more if isinstance(value, str))
        for value in values:
            path = ROOT / value
            if not path.is_file():
                fail(f"evidence {item.get('id')} points to missing script {value}")
            scripts.add(path)
    return scripts


def main() -> None:
    runner_ns = runpy.run_path(str(RUNNER))
    static_ns = runpy.run_path(str(STATIC_RUNNER))
    checks = tuple(runner_ns.get("CHECKS", ()))
    static_checks = tuple(static_ns.get("SOURCE_CHECKS", ()))
    if not checks:
        fail("tests/run.py exposes no CHECKS")
    if not static_checks:
        fail("tests/static.py exposes no SOURCE_CHECKS")

    names = [check.name for check in checks]
    labels = [check.label for check in checks]
    commands = [tuple(check.command) for check in checks]
    if len(names) != len(set(names)):
        fail("tests/run.py contains duplicate gate names")
    if len(labels) != len(set(labels)):
        fail("tests/run.py contains duplicate gate labels")
    if len(commands) != len(set(commands)):
        fail("tests/run.py contains duplicate top-level commands")

    name_to_index = {name: index for index, name in enumerate(names)}
    roots: set[Path] = {RUNNER, STATIC_RUNNER, MAKEFILE, *PERMANENT_WORKFLOWS}
    for root in roots:
        if not root.is_file():
            fail(f"control root is missing: {root.relative_to(ROOT)}")

    for index, check in enumerate(checks):
        for dependency in check.depends:
            if dependency not in name_to_index:
                fail(f"runner gate {check.name} depends on unknown gate {dependency}")
            if name_to_index[dependency] >= index:
                fail(f"runner gate {check.name} depends on non-prior gate {dependency}")
        for token in check.command:
            path = repository_path(token)
            if path is not None:
                roots.add(path)
            elif token.startswith(("tests/", "tools/", "validator/", "standards/")):
                fail(f"runner gate {check.name} references missing path {token}")

    for item in static_checks:
        path = Path(item)
        if not path.is_absolute():
            path = ROOT / path
        if not path.is_file():
            fail(f"static contract references missing source check {path.relative_to(ROOT)}")
        roots.add(path)

    registry = json.loads(EVIDENCE_REGISTRY.read_text(encoding="utf-8"))
    allowed_types = set(registry.get("allowed_types", []))
    evidence = registry.get("evidence", [])
    evidence_ids: list[str] = []
    for item in evidence:
        evidence_id = item.get("id")
        evidence_type = item.get("type")
        if not isinstance(evidence_id, str) or not evidence_id:
            fail("evidence registry contains an invalid id")
        evidence_ids.append(evidence_id)
        if evidence_type not in allowed_types:
            fail(f"evidence {evidence_id} has unsupported type {evidence_type}")
        target = item.get("target", {})
        gates: list[str] = []
        gate = target.get("runner_gate")
        if isinstance(gate, str):
            gates.append(gate)
        more_gates = target.get("runner_gates")
        if isinstance(more_gates, list):
            gates.extend(value for value in more_gates if isinstance(value, str))
        for gate_name in gates:
            if gate_name not in name_to_index:
                fail(f"evidence {evidence_id} points to unknown runner gate {gate_name}")
        if evidence_type == "runner-alias":
            script = target.get("script")
            if not isinstance(script, str) or len(gates) != 1:
                fail(f"runner alias {evidence_id} must name one script and one runner gate")
            gate_command = commands[name_to_index[gates[0]]]
            if script not in gate_command:
                fail(
                    f"runner alias {evidence_id} script {script} does not match gate {gates[0]} command"
                )
    if len(evidence_ids) != len(set(evidence_ids)):
        fail("evidence registry contains duplicate ids")
    roots.update(collect_registry_scripts(registry))

    negative = json.loads(NEGATIVE_PATHS.read_text(encoding="utf-8"))
    cases = negative.get("cases", [])
    case_ids: list[str] = []
    for case in cases:
        case_id = case.get("id")
        family = case.get("family")
        expected_rule = case.get("expected_rule_id")
        if not all(isinstance(value, str) and value for value in (case_id, family, expected_rule)):
            fail("negative-path case has incomplete id/family/expected_rule_id")
        case_ids.append(case_id)
        path_value = case.get("fixture")
        if not isinstance(path_value, str) or not (ROOT / path_value).is_file():
            fail(f"negative-path case {case_id} references missing fixture: {path_value}")
        for key in ("positive_gate", "validator"):
            command = case.get(key)
            if not isinstance(command, list) or not command:
                fail(f"negative-path case {case_id} has invalid {key}")
            for token in command:
                if not isinstance(token, str):
                    continue
                path = repository_path(token)
                if path is not None:
                    roots.add(path)
                elif token.startswith(("tests/", "tools/", "validator/", "standards/")):
                    fail(f"negative-path case {case_id} references missing path {token}")
    if len(case_ids) != len(set(case_ids)):
        fail("negative-path manifest contains duplicate case ids")

    candidates = candidate_files()
    nodes = control_files(candidates)
    by_stem = python_import_targets(nodes)
    graph = {
        node: direct_references(node, nodes, by_stem)
        for node in nodes
    }

    reachable_nodes: set[Path] = set()
    queue = deque(path for path in roots if path in nodes)
    while queue:
        current = queue.popleft()
        if current in reachable_nodes:
            continue
        reachable_nodes.add(current)
        queue.extend(graph.get(current, set()) - reachable_nodes)

    reachable_candidates = candidates & reachable_nodes
    orphaned = sorted(candidates - reachable_candidates)
    if orphaned:
        rendered = ", ".join(path.relative_to(ROOT).as_posix() for path in orphaned)
        fail(f"unreachable retained test/check scripts: {rendered}")

    print(
        "TEST-SURFACE-INTEGRITY-EVIDENCE status=PASS "
        f"runner_gates={len(checks)} static_checks={len(static_checks)} "
        f"evidence_ids={len(evidence_ids)} negative_cases={len(case_ids)} "
        f"control_nodes={len(nodes)} test_scripts={len(candidates)} "
        f"reachable={len(reachable_candidates)} orphaned=0"
    )


if __name__ == "__main__":
    main()
