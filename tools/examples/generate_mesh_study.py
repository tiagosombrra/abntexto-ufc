#!/usr/bin/env python3
"""Generate source-bound scientific teaching assets, without external dependencies.

The unit-square grids are exact structured geometry, NOT a novel meshing method
or an empirical benchmarking result. Do not publish performance claims from them.
"""
from __future__ import annotations

import argparse
import csv
import hashlib
import io
import json
import math
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
STUDY_DIR = ROOT / "examples" / "canonical-mesh-study"
SOURCE = STUDY_DIR / "study.json"
DEFAULT_OUTPUT = STUDY_DIR / "generated"
CASES = ("uniform_quads", "anisotropic_quads", "uniform_triangles")
LOCALES = ("pt", "en", "es", "fr")


def sha(data: bytes) -> str:
    """Produce stable checksums for the original bytes in each derived asset."""
    return hashlib.sha256(data).hexdigest()


def mesh(case: dict) -> tuple[dict, list[tuple[float, float, float, float]]]:
    """Construct all edges, check Euler's identity and return exact counts."""
    nx, ny, kind = case["nx"], case["ny"], case["family"]
    if not (isinstance(nx, int) and isinstance(ny, int) and 1 <= nx <= 64 and 1 <= ny <= 64):
        raise ValueError("Invalid bounded grid dimensions")
    if kind not in ("triangle", "quadrilateral"):
        raise ValueError("Only triangular or quadrilateral grid cells are supported")
    vertices = {(i, j) for i in range(nx + 1) for j in range(ny + 1)}
    edges: set[tuple[tuple[int, int], tuple[int, int]]] = set()

    def add_edge(a: tuple[int, int], b: tuple[int, int]) -> None:
        edges.add(tuple(sorted((a, b))))

    for i in range(nx):
        for j in range(ny + 1):
            add_edge((i, j), (i + 1, j))
    for i in range(nx + 1):
        for j in range(ny):
            add_edge((i, j), (i, j + 1))
    if kind == "triangle":
        for i in range(nx):
            for j in range(ny):
                add_edge((i, j), (i + 1, j + 1))

    cells = nx * ny * (2 if kind == "triangle" else 1)
    if len(vertices) - len(edges) + cells != 1:
        raise AssertionError(f"Euler connectivity violation for {case['id']}")
    hx, hy = 1 / nx, 1 / ny
    edge_ratio = (math.hypot(hx, hy) / min(hx, hy) if kind == "triangle"
                  else max(hx, hy) / min(hx, hy))
    metrics = {
        "id": case["id"],
        "family": kind,
        "nx": nx, "ny": ny,
        "vertices": len(vertices), "edges": len(edges), "cells": cells,
        "cell_area": 1.0 / cells, "edge_length_ratio": round(edge_ratio, 6),
    }
    lines = [
        (a[0] / nx, a[1] / ny, b[0] / nx, b[1] / ny)
        for a, b in sorted(edges)
    ]
    return metrics, lines


def svg(lines: list[tuple[float, float, float, float]]) -> bytes:
    """Draw original vector geometry, not a downloaded illustrative image."""
    raw = [
        '<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 440 440"',
        ' role="img" aria-label="Structured unit-square mesh">',
        '<rect x="20" y="20" width="400" height="400" fill="#f9fbfd" />',
    ]
    for x1, y1, x2, y2 in lines:
        raw.append(
            f'<line x1="{20 + 400*x1:.3f}" y1="{420 - 400*y1:.3f}"'
            f' x2="{20 + 400*x2:.3f}" y2="{420 - 400*y2:.3f}"'
            ' stroke="#254760" stroke-width="1.15" />'
        )
    raw.append('</svg>')
    return ("\n".join(raw) + "\n").encode("utf-8")


def pdf(lines: list[tuple[float, float, float, float]]) -> bytes:
    """Write an uncomplicated, deterministic, single-page vector PDF 1.4."""
    commands = ["q", "0.97 0.98 0.995 rg", "20 20 400 400 re f",
                "0.14 0.28 0.38 RG", "0.75 w"]
    for x1, y1, x2, y2 in lines:
        commands.append(
            f"{20+400*x1:.3f} {20+400*y1:.3f} m "
            f"{20+400*x2:.3f} {20+400*y2:.3f} l S"
        )
    commands.append("Q")
    stream = ("\n".join(commands) + "\n").encode("ascii")
    objects = [
        b"<< /Type /Catalog /Pages 2 0 R >>",
        b"<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        b"<< /Type /Page /Parent 2 0 R /MediaBox [0 0 440 440] "
        b"/Resources << >> /Contents 4 0 R >>",
        b"<< /Length " + str(len(stream)).encode("ascii")
        + b" >>\nstream\n" + stream + b"endstream",
    ]
    data = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
    offsets = [0]
    for number, obj in enumerate(objects, 1):
        offsets.append(len(data))
        data.extend(f"{number} 0 obj\n".encode("ascii"))
        data.extend(obj)
        data.extend(b"\nendobj\n")
    xref = len(data)
    data.extend(f"xref\n0 {len(objects)+1}\n0000000000 65535 f \n".encode("ascii"))
    for offset in offsets[1:]:
        data.extend(f"{offset:010d} 00000 n \n".encode("ascii"))
    data.extend(
        f"trailer\n<< /Size {len(objects)+1} /Root 1 0 R >>\n"
        f"startxref\n{xref}\n%%EOF\n".encode("ascii")
    )
    return bytes(data)


def csv_table(metrics: list[dict]) -> bytes:
    """Serialize exact topology counts in a locale-neutral, machine CSV."""
    output = io.StringIO(newline="")
    fields = ("id", "family", "nx", "ny", "vertices", "edges",
              "cells", "cell_area", "edge_length_ratio")
    writer = csv.DictWriter(output, fieldnames=fields, lineterminator="\n")
    writer.writeheader()
    for item in metrics:
        row = dict(item)
        row["cell_area"] = f"{item['cell_area']:.8f}"
        row["edge_length_ratio"] = f"{item['edge_length_ratio']:.6f}"
        writer.writerow(row)
    return output.getvalue().encode("utf-8")


def latex_body(locale: str, text: dict, metrics: list[dict]) -> bytes:
    """Produce translated scientific prose from the same verified measurements."""
    head = text["table_headings"]
    if len(head) != 5 or len(text["case_names"]) != len(metrics):
        raise ValueError(f"Missing translated table labels in {locale}")
    nl = "\\\\"
    lines = [
        f"% Canonical mesh demonstration v1, locale={locale}; generated, do not edit.",
        rf"\subsection{{{text['heading']}}}",
        rf"\label{{sec:canonical-mesh-{locale}}}",
        text["motivation"], r"\par", text["method"], r"\par",
        r"\begin{equation}",
        r"V=(n_x+1)(n_y+1),\quad"
        r"E_{\mathrm{quad}}=n_x(n_y+1)+n_y(n_x+1),",
        r"\end{equation}",
        r"\begin{equation}",
        r"F_{\mathrm{quad}}=n_xn_y,\quad"
        r"F_{\mathrm{tri}}=2n_xn_y,\quad V-E+F=1.",
        r"\end{equation}",
        rf"\legend{{figure}}{{{text['figure_title']}}}",
        rf"\ufcSource{{{text['figure_source']}}}",
        r"\begin{ufcobject}[here]",
        r"\centering",
        r"\includegraphics[width=.28\linewidth]{examples/canonical-mesh-study/generated/uniform_quads.pdf}",
        r"\hfill",
        r"\includegraphics[width=.28\linewidth]{examples/canonical-mesh-study/generated/anisotropic_quads.pdf}",
        r"\hfill",
        r"\includegraphics[width=.28\linewidth]{examples/canonical-mesh-study/generated/uniform_triangles.pdf}",
        r"\end{ufcobject}",
        rf"\legend{{table}}{{{text['table_title']}}}",
        rf"\ufcSource{{{text['table_source']}}}",
        r"\begin{ufcobject}[here]",
        r"\centering",
        r"\begin{tabular}{lrrrr}",
        r"\toprule",
        " & ".join(head) + " " + nl,
        r"\midrule",
    ]
    for name, metric in zip(text["case_names"], metrics):
        row = [name, str(metric["vertices"]), str(metric["edges"]),
               str(metric["cells"]), f'{metric["edge_length_ratio"]:.3f}']
        lines.append(" & ".join(row) + " " + nl)
    lines += [
        r"\bottomrule",
        r"\end{tabular}",
        r"\end{ufcobject}",
        text["interpretation"], r"\par",
        text["limitations"], r"\par",
        "% These sources are real background literature, not algorithms executed here.",
        r"\autocite{meshBommes2009,meshShewchuk2002}",
    ]
    return ("\n".join(lines) + "\n").encode("utf-8")


def generate(study: dict, source: bytes, generator: bytes) -> dict[str, bytes]:
    """Build every output deterministically without reading the current clock."""
    if study.get("schema_version") != 1 or study.get("id") != "unit-square-structured-mesh-v1":
        raise ValueError("Unknown canonical-study schema/id")
    cases = study["cases"]
    if [x["id"] for x in cases] != list(CASES):
        raise ValueError("Unexpected or reordered benchmark cases")
    if set(study["locales"]) != set(LOCALES):
        raise ValueError("Must supply four complete authored languages")
    metrics = []
    outputs: dict[str, bytes] = {}
    for case in cases:
        row, lines = mesh(case)
        metrics.append(row)
        outputs[f"{case['id']}.svg"] = svg(lines)
        outputs[f"{case['id']}.pdf"] = pdf(lines)
    outputs["mesh_metrics.csv"] = csv_table(metrics)
    for locale in LOCALES:
        outputs[f"body-{locale}.tex"] = latex_body(
            locale, study["locales"][locale], metrics
        )
    index = {
        "schema_version": 1,
        "study_id": study["id"],
        "status": study["status"],
        "source_sha256": sha(source),
        "generator_sha256": sha(generator),
        "profile_policy": "same_data_distinct_document_structure",
        "cases": metrics,
        "assets": {name: sha(content) for name, content in sorted(outputs.items())},
        "claim_status": "computed_didactic_geometry_not_peer_reviewed_performance",
        "pdf_a_certification": "NOT_TESTED",
        "human_review": "PENDING",
    }
    outputs["manifest.json"] = (
        json.dumps(index, indent=2, ensure_ascii=False) + "\n"
    ).encode("utf-8")
    return outputs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--check", action="store_true",
                        help="Compare every generated byte with the committed assets")
    parser.add_argument("--output", type=Path, default=DEFAULT_OUTPUT)
    args = parser.parse_args()
    source = SOURCE.read_bytes()
    expected = generate(json.loads(source), source, Path(__file__).read_bytes())
    if args.check:
        present = {p.name for p in args.output.iterdir() if p.is_file()} if args.output.is_dir() else set()
        if present != set(expected):
            raise SystemExit(f"MESH-CORPUS-FAIL missing={sorted(set(expected)-present)} "
                             f"unexpected={sorted(present-set(expected))}")
        for name, content in expected.items():
            if (args.output / name).read_bytes() != content:
                raise SystemExit(f"MESH-CORPUS-FAIL nonreproducible={name}")
        print(f"MESH-CORPUS-EVIDENCE status=PASS source_sha256={sha(source)} "
              f"assets={len(expected)} locales=4 cases=3")
    else:
        args.output.mkdir(parents=True, exist_ok=True)
        for name, content in expected.items():
            (args.output / name).write_bytes(content)
        print(f"MESH-CORPUS-WRITTEN assets={len(expected)} "
              "release_authorized=false")


if __name__ == "__main__":
    main()
