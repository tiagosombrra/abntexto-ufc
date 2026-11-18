#!/usr/bin/env python3
"""Fail-closed, offline asset graph for the deployed homepage and Web/Lite."""
from __future__ import annotations

import hashlib
import json
import posixpath
import re
import subprocess
from html.parser import HTMLParser
from pathlib import Path
from urllib.parse import unquote, urlsplit

ROOT = Path(__file__).resolve().parents[3]
DOCUMENTS = ("index.html", "validator/index.html")
JS_MODULE = "validator/app.js"
MODULE_IMPORT = re.compile(
    r"""(?m)^\s*import\s+.+?\s+from\s+["']([^"']+)["']\s*;?\s*$"""
)
WORKER = re.compile(
    r"""GlobalWorkerOptions\.workerSrc\s*=\s*["']([^"']+)["']"""
)
ATTRIBUTES = {
    "a": "href", "script": "src", "link": "href",
    "img": "src", "source": "src", "iframe": "src",
}


class References(HTMLParser):
    """Collect actual browser resource and navigation attributes."""

    def __init__(self) -> None:
        super().__init__(convert_charrefs=True)
        self.refs: list[tuple[str, str]] = []

    def handle_starttag(self, tag: str, attrs: list[tuple[str, str | None]]) -> None:
        attribute = ATTRIBUTES.get(tag)
        if attribute is None:
            return
        values = dict(attrs)
        if attribute in values:
            if not values[attribute]:
                raise ValueError(f"empty {tag}.{attribute} target")
            self.refs.append((tag, values[attribute]))


def deployed_files(root: Path) -> set[str]:
    """Map the tracked site and validator trees into the Pages deployment root."""
    result: set[str] = set()
    for directory, prefix in (("site", ""), ("validator", "validator/")):
        source = root / directory
        for item in source.rglob("*"):
            if not item.is_file():
                continue
            if not item.resolve().is_relative_to(root.resolve()):
                raise ValueError(f"asset escapes repository: {item}")
            result.add(prefix + item.relative_to(source).as_posix())
    return result


def resolve_reference(owner: str, raw: str, kind: str,
                      available: set[str]) -> tuple[str, str]:
    """Resolve against the deployment root, never against a local machine path."""
    if not raw or any(ord(char) < 32 or ord(char) == 127 for char in raw):
        raise ValueError(f"{owner}: missing/control-character {kind} URL")
    parsed = urlsplit(raw)
    if parsed.scheme or parsed.netloc:
        if (kind == "a" and parsed.scheme == "https" and parsed.netloc
                and not parsed.username and not parsed.password):
            try:
                parsed.port
            except ValueError as error:
                raise ValueError(f"{owner}: invalid external anchor port") from error
            return ("external-anchor", raw)
        raise ValueError(f"{owner}: external/non-HTTPS resource forbidden: {kind} {raw}")
    decoded = unquote(parsed.path)
    if decoded.startswith("/") or "\\" in decoded:
        raise ValueError(f"{owner}: absolute/non-portable URL: {raw}")
    if any(part in (".", "..") for part in decoded.split("/")):
        # Permit ordinary ./ and ../ paths only after containment validation.
        pass
    if not decoded:
        target = owner
    else:
        target = posixpath.normpath(posixpath.join(posixpath.dirname(owner), decoded))
        if decoded.endswith("/"):
            target = posixpath.join(target, "index.html")
    if target == ".." or target.startswith("../") or target.startswith("/"):
        raise ValueError(f"{owner}: URL escapes deployed site: {raw}")
    if target not in available:
        raise ValueError(f"{owner}: missing deployed resource: {raw} -> {target}")
    return ("local", target)


def scan(root: Path) -> dict:
    """Check all HTML link/asset attributes plus application imports and worker."""
    files = deployed_files(root)
    required = set(DOCUMENTS) | {JS_MODULE}
    if not required.issubset(files):
        raise ValueError(f"missing mandatory Pages source: {sorted(required - files)}")
    graph = []
    for owner in DOCUMENTS:
        original = root / ("site" if owner == "index.html" else "validator")
        original /= "index.html"
        parser = References()
        parser.feed(original.read_text(encoding="utf-8"))
        for kind, value in parser.refs:
            scope, target = resolve_reference(owner, value, kind, files)
            graph.append({"from": owner, "kind": kind,
                          "scope": scope, "target": target})
    app = (root / JS_MODULE).read_text(encoding="utf-8")
    imports = MODULE_IMPORT.findall(app)
    workers = WORKER.findall(app)
    if not imports or len(workers) != 1:
        raise ValueError("missing app imports or unique PDF.js worker")
    for kind, values in (("module", imports), ("worker", workers)):
        for value in values:
            scope, target = resolve_reference(JS_MODULE, value, kind, files)
            if scope != "local":
                raise ValueError(f"remote {kind} is prohibited")
            graph.append({"from": JS_MODULE, "kind": kind,
                          "scope": scope, "target": target})
    destinations = {(edge["from"], edge["target"]) for edge in graph
                    if edge["scope"] == "local"}
    for origin, expected in (
        ("index.html", "validator/index.html"),
        ("validator/index.html", "index.html"),
        ("index.html", "homepage-locales.js"),
        ("validator/index.html", JS_MODULE),
        (JS_MODULE, "validator/vendor/pdfjs/pdf.mjs"),
        (JS_MODULE, "validator/vendor/pdfjs/pdf.worker.mjs"),
    ):
        if (origin, expected) not in destinations:
            raise ValueError(f"missing critical local edge: {origin} -> {expected}")
    canonical = json.dumps(graph, sort_keys=True, separators=(",", ":"))
    return {
        "schema": 1,
        "deployed_documents": len(DOCUMENTS),
        "local_references": sum(item["scope"] == "local" for item in graph),
        "external_anchors_unchecked": sum(
            item["scope"] == "external-anchor" for item in graph),
        "modules": len(imports),
        "workers": len(workers),
        "fingerprint_sha256": hashlib.sha256(canonical.encode()).hexdigest(),
        "edges": graph,
        "http": "NOT_CHECKED",
        "network": 0,
        "release_authorization": "NONE",
    }


def selftest() -> int:
    """Exercise valid relative traversal and six negative resource/scheme cases."""
    paths = {"index.html", "validator/index.html", "validator/app.js",
             "homepage-locales.js"}
    assert resolve_reference("index.html", "./validator/", "a", paths) == (
        "local", "validator/index.html")
    assert resolve_reference("validator/index.html", "../?lang=pt-BR", "a", paths) == (
        "local", "index.html")
    assert resolve_reference("validator/index.html", "app.js", "script", paths) == (
        "local", "validator/app.js")
    assert resolve_reference("index.html", "https://example.org/a", "a", paths)[0] == (
        "external-anchor")
    invalid = (
        ("validator/index.html", "./missing.js", "script"),
        ("index.html", "../private.txt", "a"),
        ("index.html", "%2e%2e/private.txt", "a"),
        ("validator/index.html", "/etc/passwd", "script"),
        ("validator/index.html", "https://example.org/app.js", "script"),
        ("index.html", "javascript:alert(1)", "a"),
        ("index.html", "https://example.org:bad/path", "a"),
        ("index.html", "https://name:password@example.org/a", "a"),
    )
    for owner, uri, kind in invalid:
        try:
            resolve_reference(owner, uri, kind, paths)
        except ValueError:
            continue
        raise AssertionError(f"unsafe/missing target accepted: {uri}")
    parser = References()
    parser.feed('<script src="./app.js"></script><a href="./"></a>')
    assert parser.refs == [("script", "./app.js"), ("a", "./")]
    return len(invalid)


def main() -> None:
    negatives = selftest()
    try:
        result = scan(ROOT)
    except (ValueError, OSError) as error:
        raise SystemExit(f"P012-PAGES-ASSET-EVIDENCE status=FAIL reason={error}") from error
    sha = subprocess.check_output(["git", "rev-parse", "HEAD"],
                                  cwd=ROOT, text=True).strip()
    print("P012-PAGES-ASSET-EVIDENCE status=PASS"
          f" checkout={sha[:12]}"
          f" pages={result['deployed_documents']}"
          f" local={result['local_references']}"
          f" external_anchors_unchecked={result['external_anchors_unchecked']}"
          f" modules={result['modules']} workers={result['workers']}"
          f" negative_cases={negatives}"
          f" sha256={result['fingerprint_sha256']}"
          " network=0 http=NOT_CHECKED release_authorization=NONE")


if __name__ == "__main__":
    main()
