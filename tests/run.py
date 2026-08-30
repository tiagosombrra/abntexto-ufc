#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys
import time
from dataclasses import asdict, dataclass
from pathlib import Path


@dataclass(frozen=True)
class Check:
    name: str
    label: str
    command: tuple[str, ...]
    modes: tuple[str, ...] = ("pr", "release")
    depends: tuple[str, ...] = ()


@dataclass
class Result:
    name: str
    label: str
    status: str
    command: list[str]
    duration_seconds: float
    exit_code: int | None
    log: str
    reason: str = ""


CHECKS = (
    Check("public-api", "Public API contract", ("python3", "tests/checks/public_api_contract.py")),
    Check(
        "repository",
        "Repository contract",
        ("python3", "tests/checks/repository_contract.py"),
        depends=("public-api",),
    ),
    Check("validator-source", "PDF validator sources", ("python3", "tests/checks/validator_source.py")),
    Check("reference", "Reference document", ("sh", "tests/integration/reference-document.sh")),
    Check(
        "reference-corpus",
        "Reference corpus",
        ("sh", "tests/integration/reference-corpus.sh"),
        depends=("reference",),
    ),
    Check(
        "pdf-validator",
        "UFC PDF validator",
        ("sh", "tests/integration/pdf-validator.sh", "main.pdf"),
        depends=("reference",),
    ),
    Check(
        "pdfa",
        "Reference PDF/A-2b",
        ("sh", "tests/integration/pdfa.sh", "main.pdf"),
        modes=("release",),
        depends=("reference",),
    ),
    Check("distribution-source", "Distribution source", ("sh", "tests/integration/distribution.sh")),
    Check("layout", "Layout", ("sh", "tests/integration/layout.sh")),
    Check("font-config", "Font configuration", ("sh", "tests/integration/font-config.sh")),
    Check("pdf-oracle-core", "PDF normative oracle core", ("sh", "tests/integration/pdf-oracle-core.sh")),
    Check(
        "pdf-geometry",
        "PDF geometry",
        ("sh", "tests/integration/pdf-geometry.sh"),
        depends=("pdf-oracle-core",),
    ),
    Check("math", "Mathematics", ("sh", "tests/integration/math.sh")),
    Check("normative-complement", "Normative complement", ("sh", "tests/integration/normative-complement.sh")),
    Check("negative-paths", "Negative paths", ("sh", "tests/integration/negative-paths.sh")),
    Check("frontmatter", "Front matter", ("sh", "tests/integration/frontmatter.sh")),
    Check("duplex-frontmatter", "Duplex front matter", ("sh", "tests/integration/duplex-frontmatter.sh")),
    Check("object-geometry", "Object geometry", ("sh", "tests/integration/object-geometry.sh")),
    Check("code-typography", "Code typography", ("sh", "tests/integration/code-typography.sh")),
    Check("table-ibge", "IBGE tables", ("sh", "tests/integration/table-ibge.sh")),
    Check("objects", "Academic objects", ("sh", "tests/integration/object.sh")),
    Check("minted", "Minted objects", ("sh", "tests/integration/minted.sh")),
    Check("algorithm-numbering", "Algorithm numbering", ("sh", "tests/integration/algorithm-numbering.sh")),
    Check("documentary-source", "Documentary sources", ("sh", "tests/integration/documentary-source.sh")),
    Check("bibliography", "Bibliography", ("sh", "tests/integration/bibliography.sh")),
    Check(
        "reference-spacing",
        "Reference spacing",
        ("sh", "tests/integration/reference-spacing.sh"),
        depends=("bibliography",),
    ),
    Check("research-project", "Research project", ("sh", "tests/integration/research-project.sh")),
    Check("profiles", "Document profiles", ("sh", "tests/integration/profile-matrix.sh")),
    Check(
        "profile-pdfa",
        "Profile PDF/A-2b",
        ("sh", "tests/integration/profile-pdfa.sh"),
        modes=("release",),
        depends=("profiles",),
    ),
    Check("backmatter", "Back matter", ("sh", "tests/integration/backmatter.sh")),
    Check("duplex-backmatter", "Duplex back matter", ("sh", "tests/integration/duplex-backmatter.sh")),
    Check("build-path", "Build path", ("sh", "tests/integration/build-path.sh")),
    Check("multivolume", "Multi-volume documents", ("sh", "tests/integration/multivolume.sh")),
    Check("catalog-card", "Catalog card", ("sh", "tests/integration/catalog-card.sh")),
)

EVIDENCE_PATTERN = re.compile(r"^[A-Z0-9_-]+-EVIDENCE ")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Run abntexto-ufc validation as one coordinated gate.")
    parser.add_argument("--mode", choices=("pr", "release"), default="pr")
    parser.add_argument("--only", help="Comma-separated check names.")
    parser.add_argument("--report-dir", default="artifacts/validation")
    parser.add_argument("--list", action="store_true", help="List checks and exit.")
    return parser.parse_args()


def selected_checks(mode: str, only: str | None) -> list[Check]:
    available = [check for check in CHECKS if mode in check.modes]
    if not only:
        return available

    requested = {item.strip() for item in only.split(",") if item.strip()}
    known = {check.name for check in available}
    unknown = sorted(requested - known)
    if unknown:
        raise SystemExit("Unknown checks: " + ", ".join(unknown))

    by_name = {check.name: check for check in available}

    def add_with_dependencies(name: str, target: set[str]) -> None:
        if name in target:
            return
        for dependency in by_name[name].depends:
            if dependency in by_name:
                add_with_dependencies(dependency, target)
        target.add(name)

    expanded: set[str] = set()
    for name in requested:
        add_with_dependencies(name, expanded)
    return [check for check in available if check.name in expanded]


def run_check(check: Check, report_dir: Path, results: dict[str, Result]) -> Result:
    blocked = [dependency for dependency in check.depends if dependency in results and results[dependency].status != "PASS"]
    log_path = report_dir / "checks" / f"{check.name}.log"
    if blocked:
        result = Result(
            name=check.name,
            label=check.label,
            status="SKIP",
            command=list(check.command),
            duration_seconds=0.0,
            exit_code=None,
            log=str(log_path),
            reason="blocked by: " + ", ".join(blocked),
        )
        log_path.write_text(result.reason + "\n", encoding="utf-8")
        return result

    start = time.monotonic()
    env = os.environ.copy()
    env["PYTHONUNBUFFERED"] = "1"
    try:
        completed = subprocess.run(
            check.command,
            cwd=Path.cwd(),
            env=env,
            stdout=subprocess.PIPE,
            stderr=subprocess.STDOUT,
            text=True,
            errors="replace",
            check=False,
        )
        output = completed.stdout
        exit_code = completed.returncode
    except FileNotFoundError as error:
        output = f"{error}\n"
        exit_code = 127

    duration = time.monotonic() - start
    log_path.write_text(output, encoding="utf-8")
    return Result(
        name=check.name,
        label=check.label,
        status="PASS" if exit_code == 0 else "FAIL",
        command=list(check.command),
        duration_seconds=round(duration, 3),
        exit_code=exit_code,
        log=str(log_path),
    )


def write_reports(report_dir: Path, mode: str, results: list[Result], complete: bool) -> None:
    report_dir.mkdir(parents=True, exist_ok=True)
    failed = any(item.status == "FAIL" for item in results)
    skipped = any(item.status == "SKIP" for item in results)
    state = "FAIL" if complete and (failed or skipped) else "PASS" if complete else "RUNNING"
    payload = {
        "mode": mode,
        "complete": complete,
        "result": state,
        "checks": [asdict(item) for item in results],
    }
    (report_dir / "validation-report.json").write_text(
        json.dumps(payload, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    lines = [
        "# abntexto-ufc validation",
        "",
        f"- Mode: `{mode}`",
        f"- Complete: `{str(complete).lower()}`",
        f"- Result: **{state}**",
        "",
        "| Status | Check | Duration |",
        "|---|---|---:|",
    ]
    for item in results:
        duration = f"{item.duration_seconds:.1f}s" if item.duration_seconds else "-"
        lines.append(f"| {item.status} | {item.label} | {duration} |")
    failures = [item for item in results if item.status == "FAIL"]
    skipped_results = [item for item in results if item.status == "SKIP"]
    if failures:
        lines.extend(["", "## Failures", ""])
        for item in failures:
            lines.append(f"- `{item.name}`: exit {item.exit_code}; log `{item.log}`")
    if skipped_results:
        lines.extend(["", "## Skipped", ""])
        for item in skipped_results:
            lines.append(f"- `{item.name}`: {item.reason}")
    (report_dir / "validation-report.md").write_text("\n".join(lines) + "\n", encoding="utf-8")


def print_failure_tail(result: Result, lines: int = 35) -> None:
    path = Path(result.log)
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    print(f"\n--- {result.name}: last {min(lines, len(content))} log lines ---")
    for line in content[-lines:]:
        print(line)


def print_structured_evidence(result: Result) -> None:
    path = Path(result.log)
    if not path.is_file():
        return
    content = path.read_text(encoding="utf-8", errors="replace").splitlines()
    evidence = [line for line in content if EVIDENCE_PATTERN.match(line)]
    if not evidence:
        return
    print(f"\n--- {result.name}: structured evidence ---")
    for line in evidence:
        print(line)


def main() -> int:
    args = parse_args()
    checks = selected_checks(args.mode, args.only)

    if args.list:
        for check in checks:
            print(f"{check.name:24} {check.label}")
        return 0

    report_dir = Path(args.report_dir)
    (report_dir / "checks").mkdir(parents=True, exist_ok=True)

    results_by_name: dict[str, Result] = {}
    ordered_results: list[Result] = []
    write_reports(report_dir, args.mode, ordered_results, complete=False)

    print(f"abntexto-ufc validation: mode={args.mode}, checks={len(checks)}")
    for index, check in enumerate(checks, 1):
        print(f"[{index:02}/{len(checks):02}] {check.label} ...", flush=True)
        result = run_check(check, report_dir, results_by_name)
        results_by_name[result.name] = result
        ordered_results.append(result)
        write_reports(report_dir, args.mode, ordered_results, complete=False)
        suffix = f" ({result.duration_seconds:.1f}s)" if result.duration_seconds else ""
        print(f"         {result.status}{suffix}")
        if result.status == "PASS":
            print_structured_evidence(result)
        if result.status == "FAIL":
            print_failure_tail(result)

    write_reports(report_dir, args.mode, ordered_results, complete=True)

    passed = sum(item.status == "PASS" for item in ordered_results)
    failed = sum(item.status == "FAIL" for item in ordered_results)
    skipped = sum(item.status == "SKIP" for item in ordered_results)
    print("\nValidation summary")
    print(f"PASS={passed} FAIL={failed} SKIP={skipped}")
    print(f"Report: {report_dir / 'validation-report.md'}")
    return 1 if failed or skipped else 0


if __name__ == "__main__":
    sys.exit(main())
