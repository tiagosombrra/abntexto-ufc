#!/usr/bin/env python3
"""Source-bound offline URL inventory and opt-in, bounded HTTP availability probe."""
from __future__ import annotations

import argparse
import hashlib
import html
import ipaddress
import json
import socket
import ssl
import subprocess
import tempfile
from concurrent.futures import ThreadPoolExecutor
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import urlsplit, urlunsplit
from urllib.request import HTTPRedirectHandler, Request, build_opener

from documentation_links_contract import (LINK, REFERENCE, ROOT, SCHEME,
                                          tracked_markdown, visible_text)


def normalize_url(raw: str) -> str:
    """Retain HTTP resource identity, discarding only fragment and HTML escaping."""
    raw = html.unescape(raw.strip())
    if raw.startswith("//"):
        raw = "https:" + raw
    parsed = urlsplit(raw)
    if parsed.scheme.lower() not in ("http", "https") or not parsed.hostname:
        raise ValueError(f"non-HTTP or malformed external link: {raw}")
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


def public_hostname(hostname: str) -> None:
    """Reject localhost, special domains, literal nonpublic IPs and DNS private answers."""
    host = hostname.rstrip(".").lower()
    if not host or "." not in host or host.endswith((".local", ".internal", ".localhost", ".test")):
        raise ValueError("nonpublic hostname")
    try:
        literal = ipaddress.ip_address(host)
    except ValueError:
        literal = None
    if literal is not None:
        if not literal.is_global:
            raise ValueError("nonpublic IP literal")
        return
    for answer in socket.getaddrinfo(host, None, type=socket.SOCK_STREAM):
        if not ipaddress.ip_address(answer[4][0]).is_global:
            raise ValueError("nonpublic DNS answer")


class PublicRedirects(HTTPRedirectHandler):
    """Prevent the probe from following redirects to nonpublic targets."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        url = urlsplit(newurl)
        if url.scheme not in ("http", "https") or not url.hostname:
            raise ValueError("redirect target is not public HTTP(S)")
        public_hostname(url.hostname)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


def classify_status(code: int) -> str:
    if 200 <= code < 400:
        return "REACHABLE"
    if code in (401, 403):
        return "ACCESS_RESTRICTED"
    if code == 404:
        return "NOT_FOUND"
    if code == 410:
        return "GONE"
    if code == 429:
        return "RATE_LIMITED"
    if 500 <= code:
        return "SERVER_ERROR"
    return "HTTP_OTHER"


def probe_one(url: str, timeout: float) -> dict:
    """Perform HEAD, with a range-limited GET fallback only for HEAD rejection."""
    parsed = urlsplit(url)
    try:
        if parsed.scheme not in ("http", "https") or not parsed.hostname:
            raise ValueError("invalid URL")
        public_hostname(parsed.hostname)
        opener = build_opener(PublicRedirects())
        for method in ("HEAD", "GET"):
            headers = {"User-Agent": "abntexto-ufc-link-audit/1.0",
                       "Accept": "*/*"}
            if method == "GET":
                headers["Range"] = "bytes=0-0"
            request = Request(url, headers=headers, method=method)
            try:
                with opener.open(request, timeout=timeout) as response:
                    return {"status": classify_status(response.status),
                            "http_code": response.status, "method": method,
                            "final_url": response.geturl()}
            except HTTPError as error:
                if method == "HEAD" and error.code in (405, 501):
                    error.close()
                    continue
                result = {"status": classify_status(error.code),
                          "http_code": error.code, "method": method,
                          "final_url": error.geturl()}
                error.close()
                return result
    except ValueError as error:
        return {"status": "UNSAFE_TARGET", "detail": str(error)[:150]}
    except (socket.timeout, TimeoutError):
        return {"status": "TIMEOUT"}
    except ssl.SSLError as error:
        return {"status": "TLS_ERROR", "detail": type(error).__name__}
    except (URLError, OSError) as error:
        reason = getattr(error, "reason", error)
        return {"status": "NETWORK_ERROR", "detail": type(reason).__name__}
    return {"status": "HTTP_OTHER", "detail": "unsupported HEAD/GET sequence"}


def selftest() -> None:
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
        for bad in ("javascript:alert", "file:///etc/passwd", "https://name:pw@example.org"):
            try:
                normalize_url(bad)
            except ValueError:
                pass
            else:
                raise AssertionError("unsafe scheme/userinfo accepted")
        for bad in ("localhost", "127.0.0.1", "10.1.2.3", "[::1]"):
            try:
                public_hostname(bad.strip("[]"))
            except ValueError:
                pass
            else:
                raise AssertionError("nonpublic hostname accepted")
        assert classify_status(403) == "ACCESS_RESTRICTED"
        assert classify_status(404) == "NOT_FOUND"
        assert classify_status(429) == "RATE_LIMITED"
        assert classify_status(200) == "REACHABLE"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--probe", action="store_true",
                        help="Perform opt-in HTTP requests (never run in Static)")
    parser.add_argument("--report", type=Path,
                        help="Write source-bound JSON receipt (required for --probe)")
    parser.add_argument("--limit", type=int, default=0,
                        help="Max unique URLs for a partial probe; zero means all")
    parser.add_argument("--timeout", type=float, default=5.0)
    parser.add_argument("--workers", type=int, default=4)
    args = parser.parse_args()
    if args.probe and args.report is None:
        parser.error("--probe requires --report to preserve a bounded receipt")
    if args.limit < 0 or not (0.5 <= args.timeout <= 15) or not (1 <= args.workers <= 8):
        parser.error("limit >= 0, timeout in [0.5,15], workers in [1,8] required")
    selftest()
    result = inventory(ROOT, tracked_markdown())
    result["commit_sha"] = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=ROOT, text=True).strip()
    if not result["links"]:
        raise SystemExit("P012-EXTERNAL-LINK-EVIDENCE status=FAIL no_external_links")
    if args.probe:
        selected = result["links"][:args.limit or None]
        result["observed_at_utc"] = datetime.now(timezone.utc).isoformat()
        with ThreadPoolExecutor(max_workers=args.workers) as pool:
            responses = list(pool.map(lambda item: probe_one(item["url"], args.timeout),
                                      selected))
        result["probe"] = [{"url": item["url"], **response}
                           for item, response in zip(selected, responses)]
        result["probe_scope"] = ("COMPLETE" if len(selected) == result["unique_urls"]
                                 else "PARTIAL")
        result["probe_counts"] = dict(sorted(Counter(
            item["status"] for item in result["probe"]).items()))
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(json.dumps(result, ensure_ascii=False, indent=2) + "\n",
                               encoding="utf-8")
    print("P012-EXTERNAL-LINK-EVIDENCE status=PASS"
          f" commit={result['commit_sha'][:12]} files={result['files']}"
          f" occurrences={result['occurrences']} unique={result['unique_urls']}"
          f" sha256={result['fingerprint_sha256']}"
          f" http={'PROBED' if args.probe else 'NOT_CHECKED'}"
          f" scope={result.get('probe_scope', 'OFFLINE')}"
          f" results={result.get('probe_counts', {})}"
          " selftest=PASS network_opt_in=true release_authorization=NONE")


if __name__ == "__main__":
    main()
