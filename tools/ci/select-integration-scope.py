#!/usr/bin/env python3
from __future__ import annotations

import argparse
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
DEFAULT_MARKER = "release/v3-release-candidate.json"


def bool_text(value: str) -> bool:
    return value.strip().lower() == "true"


def git_changed_paths(base: str, head: str) -> set[str]:
    output = subprocess.check_output(
        ["git", "diff", "--name-only", base, head],
        cwd=ROOT,
        text=True,
    )
    return {line.strip() for line in output.splitlines() if line.strip()}


def classify_suite(base: str, head: str) -> str:
    return subprocess.check_output(
        [
            "python3",
            "tests/integration_suites.py",
            "--base",
            base,
            "--head",
            head,
        ],
        cwd=ROOT,
        text=True,
    ).strip()


def append(path: Path | None, text: str) -> None:
    if path is None:
        return
    with path.open("a", encoding="utf-8") as handle:
        handle.write(text)


def main() -> None:
    parser = argparse.ArgumentParser(description="Select Linux integration scope.")
    parser.add_argument("--event-name", required=True)
    parser.add_argument("--pr-draft", default="false")
    parser.add_argument("--base-sha", default="")
    parser.add_argument("--head-sha", default="")
    parser.add_argument("--input-scope", default="auto")
    parser.add_argument("--candidate-marker", default=DEFAULT_MARKER)
    parser.add_argument("--github-output", type=Path)
    parser.add_argument("--github-summary", type=Path)
    args = parser.parse_args()

    run_integration = True
    selected_scope = "complete"
    reason = "manual-auto-fail-closed"

    if args.event_name == "pull_request":
        if bool_text(args.pr_draft):
            run_integration = False
            selected_scope = "none"
            reason = "draft-pr"
        else:
            if not args.base_sha or not args.head_sha:
                raise SystemExit("Pull-request scope selection requires base/head SHAs.")
            changed = git_changed_paths(args.base_sha, args.head_sha)
            if args.candidate_marker in changed:
                selected_scope = "complete"
                reason = "release-candidate-full-pr"
            else:
                selected_scope = classify_suite(args.base_sha, args.head_sha)
                if selected_scope == "none":
                    run_integration = False
                    reason = "documentation-only-full-pr"
                else:
                    reason = f"auto-full-pr:{selected_scope}"
    elif args.input_scope != "auto":
        selected_scope = args.input_scope
        reason = f"manual:{selected_scope}"
    elif args.event_name == "push":
        selected_scope = "complete"
        reason = "release-marker-main-push"

    output = (
        f"run_integration={'true' if run_integration else 'false'}\n"
        f"scope={selected_scope}\n"
        f"reason={reason}\n"
    )
    print(output, end="")
    append(args.github_output, output)

    summary = (
        "### Linux integration scope\n\n"
        f"- run integration: `{str(run_integration).lower()}`\n"
        f"- scope: `{selected_scope}`\n"
        f"- reason: `{reason}`\n"
    )
    append(args.github_summary, summary)


if __name__ == "__main__":
    main()
