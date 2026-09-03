#!/usr/bin/env python3
from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[2]
EXPECTED_MAIN = "fbee5bd329f98a389c2880932af40547c8d1674e"

PATCHES = {
    "docs/ROADMAP-V3.0.0.md": [
        ("Its permanent residual contract covers 303 sources (134 LaTeX + 169 engineering)", "Its permanent residual contract covers 302 sources (134 LaTeX + 168 engineering)"),
        ("now covers 134 LaTeX plus 169 behavior-affecting engineering sources", "now covers 134 LaTeX plus 168 behavior-affecting engineering sources"),
    ],
    "docs/HANDOFF-V3.0.0.md": [
        ("the residual gate scans 303 sources", "the residual gate scans 302 sources"),
    ],
}


def run(*args):
    return subprocess.check_output(args, cwd=ROOT, text=True).strip()


def main():
    run("git", "fetch", "origin", "main")
    if run("git", "rev-parse", "origin/main") != EXPECTED_MAIN:
        raise SystemExit("origin/main moved; stop fail-closed")

    for rel, patches in PATCHES.items():
        path = ROOT / rel
        text = path.read_text(encoding="utf-8")
        for old, new in patches:
            if text.count(old) != 1:
                raise SystemExit(f"{rel}: expected exactly one match for {old!r}")
            text = text.replace(old, new, 1)
        path.write_text(text, encoding="utf-8")

    subprocess.check_call(["git", "rm", ".github/scripts/r3-b3-closeout-text-fix.py", ".github/workflows/r3-b3-closeout-text-fix.yml"], cwd=ROOT)
    subprocess.check_call(["make", "static-check"], cwd=ROOT)
    subprocess.check_call(["git", "diff", "--check"], cwd=ROOT)
    subprocess.check_call(["git", "add", *PATCHES.keys()], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.name", "github-actions[bot]"], cwd=ROOT)
    subprocess.check_call(["git", "config", "user.email", "41898282+github-actions[bot]@users.noreply.github.com"], cwd=ROOT)
    subprocess.check_call(["git", "commit", "-m", "docs: finalize permanent B3 residual baseline"], cwd=ROOT)
    subprocess.check_call(["git", "push", "origin", "HEAD"], cwd=ROOT)

if __name__ == "__main__":
    main()
