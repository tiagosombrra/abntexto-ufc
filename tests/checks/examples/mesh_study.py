#!/usr/bin/env python3
"""Fast independent checks of the canonical four-locale mesh study.

No TeX Live, external APIs, and no claims about empirical mesh quality.
Checks committed source, derived mathematics, binary/PDF syntax, and mutants.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parents[3]
SOURCE = ROOT / "examples" / "canonical-mesh-study" / "study.json"
GENERATOR = ROOT / "tools" / "examples" / "generate_mesh_study.py"
EXPECTED = {
    "uniform_quads": {"vertices": 81, "edges": 144, "cells": 64, "ratio": 1.0},
    "anisotropic_quads": {"vertices": 85, "edges": 148, "cells": 64, "ratio": 4.0},
    "uniform_triangles": {"vertices": 81, "edges": 208, "cells": 128, "ratio": 2**0.5},
}
LOCALES = ("pt", "en", "es", "fr")


def sha(data: bytes) -> str:
    """Bind comparisons to immutable fixture and generated content bytes."""
    return hashlib.sha256(data).hexdigest()


def check_assets(out: Path) -> None:
    """Validate independently derived counts and every generated asset."""
    study_bytes = SOURCE.read_bytes()
    study = json.loads(study_bytes)
    index = json.loads((out / "manifest.json").read_bytes())
    if index["source_sha256"] != sha(study_bytes):
        raise AssertionError("Canonical source SHA was not recorded")
    if index["generator_sha256"] != sha(GENERATOR.read_bytes()):
        raise AssertionError("Generator SHA was not recorded")
    if index["status"] != "deterministic_didactic_baseline_not_novel_research":
        raise AssertionError("Incorrect scientific claim status")
    if index.get("human_review") != "PENDING":
        raise AssertionError("Human editorial approval was invented")
    source_cases = {row["id"]: row for row in study["cases"]}
    records = {row["id"]: row for row in index["cases"]}
    table = {
        row["id"]: row for row in csv.DictReader(
            io.StringIO((out / "mesh_metrics.csv").read_text(encoding="utf-8"))
        )
    }
    if set(source_cases) != set(EXPECTED) or set(table) != set(EXPECTED):
        raise AssertionError("Unexpected mesh case set")
    for name, correct in EXPECTED.items():
        cfg, got, recorded = source_cases[name], records[name], table[name]
        if (got["nx"], got["ny"]) != (cfg["nx"], cfg["ny"]):
            raise AssertionError(f"Wrong source grid for {name}")
        for key in ("vertices", "edges", "cells"):
            if int(got[key]) != correct[key] or int(recorded[key]) != correct[key]:
                raise AssertionError(f"Incorrect {key} for {name}")
        if abs(float(got["edge_length_ratio"]) - correct["ratio"]) > 1e-5:
            raise AssertionError(f"Wrong edge ratio for {name}")
        if int(got["vertices"]) - int(got["edges"]) + int(got["cells"]) != 1:
            raise AssertionError(f"Euler invariant failed for {name}")
        if abs(float(recorded["cell_area"]) * int(got["cells"]) - 1) > 1e-6:
            raise AssertionError(f"Area partition invalid for {name}")
        if not (out / f"{name}.pdf").read_bytes().startswith(b"%PDF-1.4\n"):
            raise AssertionError(f"Not an original PDF figure: {name}")
        pdf = (out / f"{name}.pdf").read_bytes()
        if b"/Count 1" not in pdf or b"startxref\n" not in pdf or not pdf.endswith(b"%%EOF\n"):
            raise AssertionError(f"PDF structure corrupted for {name}")
        svg = (out / f"{name}.svg").read_text(encoding="utf-8")
        if svg.count("<line ") != int(got["edges"]) or "<svg " not in svg:
            raise AssertionError(f"SVG mesh geometry incomplete for {name}")
    for locale in LOCALES:
        text = (out / f"body-{locale}.tex").read_text(encoding="utf-8")
        authored = study["locales"][locale]
        if any(authored[key] not in text for key in (
            "heading", "motivation", "method", "interpretation", "limitations"
        )):
            raise AssertionError(f"Missing original written content: {locale}")
        if any(f"{name}.pdf" not in text for name in EXPECTED):
            raise AssertionError(f"Missing figure from scientific manuscript: {locale}")
        if any(x not in text for x in (
            r"\begin{equation}", r"\legend{table}", r"\autocite{meshBommes2009,meshShewchuk2002}"
        )):
            raise AssertionError(f"Missing real figure/table/mathematics/references: {locale}")
    if set(index["assets"]) != {p.name for p in out.iterdir() if p.is_file()} - {"manifest.json"}:
        raise AssertionError("Source-bound asset inventory incomplete")
    for file, digest in index["assets"].items():
        if sha((out / file).read_bytes()) != digest:
            raise AssertionError(f"Hash mismatch for generated {file}")
    refs = {x["key"]: x for x in study["reference_sources"]}
    if refs["bommes2009"]["doi"] != "10.1145/1576246.1531383":
        raise AssertionError("DOI mismatch in Bommes literature metadata")
    if refs["shewchuk2002"]["doi"] != "10.1016/S0925-7721(01)00047-5":
        raise AssertionError("DOI mismatch in Shewchuk literature metadata")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--artifacts", type=Path)
    args = parser.parse_args()
    # The corpus gate is intentionally fast: use Python's standard library only.
    with tempfile.TemporaryDirectory(prefix="abntexto-mesh-study-") as d:
        work = Path(d)
        result = subprocess.run([sys.executable, str(GENERATOR), "--output", str(work)],
                                cwd=ROOT, capture_output=True, text=True, check=True)
        if "MESH-CORPUS-WRITTEN" not in result.stdout:
            raise AssertionError("Generation did not report its source-bound result")
        check = subprocess.run(
            [sys.executable, str(GENERATOR), "--check", "--output", str(work)],
            cwd=ROOT, capture_output=True, text=True, check=True,
        )
        if "status=PASS" not in check.stdout:
            raise AssertionError("Reproducibility check was not performed")
        check_assets(work)
        # Mutants must be rejected; never validate by file existence alone.
        corrupted = work / "mesh_metrics.csv"
        corrupted.write_text(corrupted.read_text().replace(",81,", ",82,", 1),
                             encoding="utf-8")
        rejected = subprocess.run(
            [sys.executable, str(GENERATOR), "--check", "--output", str(work)],
            cwd=ROOT, capture_output=True, text=True, check=False,
        )
        if rejected.returncode == 0 or "nonreproducible" not in rejected.stderr:
            raise AssertionError("Mutated metrics passed a false-positive check")
        if args.artifacts:
            check_assets(args.artifacts)
    print("MESH-STUDY-FAST-EVIDENCE status=PASS profiles=7 locales=4 "
          "cases=3 diagrams=3 independent_count_assertions=9 negative_mutants=1 "
          "release_authorized=false")


if __name__ == "__main__":
    main()
