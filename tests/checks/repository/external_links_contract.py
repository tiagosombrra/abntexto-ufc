#!/usr/bin/env python3
"""Source-bound, offline-only inventory of active Markdown HTTP(S) links."""
from __future__ import annotations

import argparse
import hashlib
import html
import json
import os
import subprocess
import tempfile
from collections import Counter, defaultdict
from pathlib import Path
from urllib.parse import urlsplit, urlunsplit

from documentation_links_contract import (LINK, REFERENCE, ROOT, SCHEME,
                                          tracked_markdown, visible_text)


def normalize_url(raw: str) -> str:
    """Retain HTTP resource identity, discarding only fragment and HTML escaping."""
    raw = html.unescape(raw.strip())
    if any(ord(ch) < 32 or ord(ch) == 127 for ch in raw):
        raise ValueError("URL contains control characters")
    if raw.startswith("//"):
        raw = "https:" + raw
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
        raise ValueError(f"non-HTTP or malformed external link: {raw}")
    if any(ch.isspace() for ch in parsed.netloc):
        raise ValueError(f"whitespace in URL authority: {raw}")
    if parsed.username is not None or parsed.password is not None:
        raise ValueError(f"credential-bearing external link: {raw}")
    try:
        port = parsed.port
    except ValueError as error:
        raise ValueError(f"invalid URL port: {raw}") from error
    host = parsed.hostname.lower()
    netloc = f"[{host}]" if ":" in host else host
    if port is not None:
        netloc += f":{port}"
    return urlunsplit((parsed.scheme.lower(), netloc, parsed.path or "/", parsed.query, ""))


def inventory(root: Path, documents: list[Path]) -> dict:
    """Use exactly the live Markdown link patterns, excluding fenced examples."""
    occurrences = []
    for path in sorted(documents):
        source = visible_text((root / path).read_text(encoding="utf-8"))
        matches = sorted(
            ((match.start(), match.group(1) or match.group(2))
             for regex in (LINK, REFERENCE) for match in regex.finditer(source)),
            key=lambda item: item[0],
        )
        for position, raw in matches:
            if not (raw.startswith("//") or SCHEME.match(raw)):
                continue
            url = normalize_url(raw)
            occurrences.append({"url": url, "file": path.as_posix(),
                                "line": source.count("\n", 0, position) + 1})
    grouped = defaultdict(list)
    for item in occurrences:
        grouped[item["url"]].append({"file": item["file"], "line": item["line"]})
    entries = [{"url": url, "references": grouped[url]}
               for url in sorted(grouped)]
    fingerprint = hashlib.sha256(json.dumps(occurrences, sort_keys=True,
                        ensure_ascii=False, separators=(",", ":")).encode("utf-8")).hexdigest()
    hosts = Counter(urlsplit(item["url"]).hostname for item in occurrences)
    return {"schema": 1, "fingerprint_sha256": fingerprint,
            "files": len(documents), "occurrences": len(occurrences),
            "unique_urls": len(entries), "hosts": dict(sorted(hosts.items())),
            "links": entries}


def selftest() -> None:
    """Check deduplication, source positions, references and unsafe URI rejection."""
    with tempfile.TemporaryDirectory(prefix="p012-urls-") as directory:
        root = Path(directory)
        (root / "a.md").write_text(
            "[A](https://example.org/x#part)\n"
            "[B](https://example.org/x#other)\n"
            "[C][ref]\n[ref]: https://example.net/a?x=1&amp;y=2\n"
            + (chr(96) * 3) + "md\n[ignored](https://wrong.example/)\n"
            + (chr(96) * 3) + "\n", encoding="utf-8")
        result = inventory(root, [Path("a.md")])
        assert result["occurrences"] == 3, result
        assert result["unique_urls"] == 2, result
        by_url = {item["url"]: item["references"] for item in result["links"]}
        assert by_url["https://example.org/x"] == [
            {"file": "a.md", "line": 1}, {"file": "a.md", "line": 2}]
        assert "https://example.net/a?x=1&y=2" in by_url
        for bad in ("javascript:alert", "file:///etc/passwd",
                    "https://name:pw@example.org", "https://example.org:bad/path",
                    "https://example.org:\n443/path", "https://example.org/a\nb"):
            try:
                normalize_url(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("unsafe scheme, authority or control accepted")
        assert normalize_url("//example.org/a#f") == "https://example.org/a"

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--report", type=Path,
                        help="Write source-bound JSON inventory without making network requests")
    args = parser.parse_args()
    selftest()
    result = inventory(ROOT, tracked_markdown())
    # Pull-request workflows may check out a synthetic merge commit, not the PR head.
    result["checkout_sha"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    event_path = os.environ.get("GITHUB_EVENT_PATH")
    if event_path:
        event = json.loads(Path(event_path).read_text(encoding="utf-8"))
        pr_head = (event.get("pull_request") or {}).get("head", {}).get("sha")
        if pr_head:
            result["pull_request_head_sha"] = pr_head
    if not result["links"]:
        raise SystemExit("P012-EXTERNAL-LINK-EVIDENCE status=FAIL no_external_links")
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    print("P012-EXTERNAL-LINK-EVIDENCE status=PASS"
          f" checkout={result['checkout_sha'][:12]}"
          f" pr_head={result.get('pull_request_head_sha', 'N/A')[:12]}"
          f" files={result['files']}"
          f" occurrences={result['occurrences']} unique={result['unique_urls']}"
          f" sha256={result['fingerprint_sha256']}"
          " http=NOT_CHECKED scope=OFFLINE"
          " selftest=PASS network_opt_in=false release_authorization=NONE")


if __name__ == "__main__":
    main()
