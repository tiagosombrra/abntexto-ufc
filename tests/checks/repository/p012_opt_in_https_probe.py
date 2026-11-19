#!/usr/bin/env python3
"""Explicitly opted-in HTTPS link probe with direct pinned IP and a killable worker.

Normal execution (including Static) is offline. A live URL can be probed ONLY
with --network-opt-in, --host, --url and --journal. Network use is a DRAFT
candidate, not independently certified for SSRF or production execution.
"""
from __future__ import annotations

import argparse
import hashlib
import ipaddress
import json
import math
import os
import signal
import socket
import ssl
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from urllib.parse import urlsplit

# Python -I excludes the script directory; resolve only the trusted local module dir.
sys.path.insert(0, str(Path(__file__).resolve().parent))

from p012_pinned_tls_contract import HopProof, classify, inspect_proof
from p012_probe_journal import MAX_RECORD_BYTES, ZERO_SHA, _encode, _safe_fd, _sync_directory
from p012_probe_security_policy import (
    Deadline, UnsafeTarget, _host, bind_public_addresses, choose_inventory_url,
    follow_redirect, target_from_url,
)
from external_links_contract import inventory
from documentation_links_contract import EXCLUDED_PARENTS, ROOT

MAX_SELECTED = 5
MAX_HOPS = 3
MAX_RESPONSE_HEADER = 8192
MAX_INFORMATIONAL = 4
MAX_CHILD_OUTPUT = 8192
MAX_URL_LENGTH = 2048
SCHEMA = 2
STATUS_CODES = frozenset({
    "REACHABLE", "ACCESS_RESTRICTED", "NOT_FOUND", "GONE", "RATE_LIMITED",
    "HEAD_UNSUPPORTED", "HTTP_OTHER", "TIMEOUT", "UNSAFE_TARGET",
    "DNS_ERROR", "TLS_ERROR", "NETWORK_ERROR", "WORKER_ERROR",
})


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat()


def checked_budget(deadline: float) -> float:
    """Use a single monotonic budget across all socket/TLS operations."""
    try:
        left = Deadline(deadline).remaining(time.monotonic())
    except UnsafeTarget as error:
        raise TimeoutError("per-URL monotonic deadline exhausted") from error
    return min(left, 10.0)


def validated_ip(value: str) -> str:
    if not isinstance(value, str) or "%" in value:
        raise UnsafeTarget("invalid scoped or non-text socket peer")
    try:
        return str(ipaddress.ip_address(value))
    except ValueError as error:
        raise UnsafeTarget("invalid socket peer IP") from error


def trusted_source_inventory(root: Path = ROOT) -> dict:
    """Derive every Markdown link from immutable Git HEAD tree blobs, not files.

    A clean git status is insufficient: skip-worktree and assume-unchanged
    allow an edited Markdown file to evade status while HEAD stays constant.
    """
    head = subprocess.check_output(
        ["git", "rev-parse", "HEAD"], cwd=root, text=True,
    ).strip()
    raw_tree = subprocess.check_output(
        ["git", "ls-tree", "-r", "--name-only", "-z", head], cwd=root,
    )
    documents = []
    for raw_path in raw_tree.split(b"\0"):
        if not raw_path:
            continue
        try:
            path = Path(raw_path.decode("utf-8"))
        except UnicodeDecodeError as error:
            raise UnsafeTarget("non-UTF8 tracked path in Git HEAD") from error
        if (path.is_absolute() or ".." in path.parts or
                (path.parts and path.parts[0] == ".git")):
            raise UnsafeTarget("unsafe path in Git HEAD tree")
        if path.suffix.lower() != ".md":
            continue
        if tuple(path.parts[:2]) in EXCLUDED_PARENTS:
            continue
        documents.append(path)
    if not documents:
        raise UnsafeTarget("Git HEAD has no active Markdown documents")
    with tempfile.TemporaryDirectory(prefix="p012-head-objects-") as folder:
        snapshot_root = Path(folder)
        for path in documents:
            # git show reads the pinned commit object, never skip-worktree bytes.
            content = subprocess.check_output(
                ["git", "show", head + ":" + path.as_posix()], cwd=root,
            )
            destination = snapshot_root / path
            destination.parent.mkdir(parents=True, exist_ok=True)
            destination.write_bytes(content)
        links = inventory(snapshot_root, documents)
    links["checkout_sha"] = head
    return links


def require_source_identity(receipt: dict, sha: str, fingerprint: str) -> None:
    """Ensure a worker cannot silently switch the selected source snapshot."""
    if (receipt.get("checkout_sha") != sha
            or receipt.get("fingerprint_sha256") != fingerprint):
        raise UnsafeTarget("source SHA or inventory fingerprint changed")


def resolve_all(hostname: str) -> tuple[str, ...]:
    """Obtain all addresses; the parent worker timeout bounds slow DNS."""
    try:
        answers = socket.getaddrinfo(hostname, 443, type=socket.SOCK_STREAM,
                                     proto=socket.IPPROTO_TCP)
    except socket.gaierror as error:
        raise LookupError("DNS lookup failed") from error
    return tuple(answer[4][0] for answer in answers)


def header_from_socket(tls_socket: ssl.SSLSocket, deadline: float,
                       remaining_bytes: int = MAX_RESPONSE_HEADER) -> bytes:
    """Stop exactly at the FIRST terminator without consuming response body."""
    data = bytearray()
    while len(data) < remaining_bytes:
        tls_socket.settimeout(checked_budget(deadline))
        byte = tls_socket.recv(1)
        if not byte:
            raise UnsafeTarget("HTTP response ended before headers")
        data.extend(byte)
        if data.endswith(b"\r\n\r\n"):
            return bytes(data)
    raise UnsafeTarget("HTTP response header exceeded byte cap")


def exchange(target, numeric_ip: str, method: str, deadline: float) -> tuple[int, dict]:
    """Connect to numeric IP, verify actual peer and CA-backed TLS hostname."""
    if method not in ("HEAD", "GET"):
        raise UnsafeTarget("unsupported HTTP method")
    ip = ipaddress.ip_address(numeric_ip)
    # Disallow IPv4-mapped IPv6 sockets even if preflight policy admits them.
    if getattr(ip, "ipv4_mapped", None):
        raise UnsafeTarget("IPv4-mapped IPv6 transport unsupported")
    family = socket.AF_INET6 if ip.version == 6 else socket.AF_INET
    address = (str(ip), 443, 0, 0) if ip.version == 6 else (str(ip), 443)
    with socket.socket(family, socket.SOCK_STREAM, socket.IPPROTO_TCP) as transport:
        transport.settimeout(checked_budget(deadline))
        transport.connect(address)
        if validated_ip(transport.getpeername()[0]) != str(ip):
            raise UnsafeTarget("TCP peer differs from pinned numeric IP")

        context = ssl.create_default_context(ssl.Purpose.SERVER_AUTH)
        context.check_hostname = True
        context.verify_mode = ssl.CERT_REQUIRED
        with context.wrap_socket(transport, server_hostname=target.hostname,
                                 do_handshake_on_connect=False) as tls:
            tls.settimeout(checked_budget(deadline))
            tls.do_handshake()
            if not tls.getpeercert():
                raise ssl.SSLError("TLS peer certificate is missing")
            peer = validated_ip(tls.getpeername()[0])
            if peer != str(ip):
                raise UnsafeTarget("TLS peer differs from pinned numeric IP")

            parts = urlsplit(target.url)
            resource = parts.path or "/"
            if parts.query:
                resource += "?" + parts.query
            extra = "Range: bytes=0-0\r\n" if method == "GET" else ""
            # Raw sockets do not consult environment HTTP(S)_PROXY variables.
            request = (f"{method} {resource} HTTP/1.1\r\n"
                       f"Host: {target.hostname}\r\n"
                       "User-Agent: ABNTEXTO-P012-OptIn/0\r\n"
                       "Accept-Encoding: identity\r\n"
                       f"{extra}Connection: close\r\n\r\n").encode("ascii")
            tls.settimeout(checked_budget(deadline))
            tls.sendall(request)
            remaining_headers = MAX_RESPONSE_HEADER
            for interim in range(MAX_INFORMATIONAL + 1):
                # A single aggregate header cap applies across 100/102/103
                # responses and the final status block, not per block.
                raw_headers = header_from_socket(tls, deadline,
                                                 remaining_headers)
                remaining_headers -= len(raw_headers)
                # Data comes from the actual verified TLS session. HopProof
                # checks consistency and HTTP syntax, not TLS cryptography.
                observation = HopProof(
                    connected_ip=str(ip), peer_ip=peer, sni=target.hostname,
                    certificate_hostname=target.hostname,
                    certificate_validated=True, host_header=target.hostname,
                    proxy_used=False, header_bytes=raw_headers,
                    body_bytes_consumed=0,
                )
                status, headers = inspect_proof(observation, target, str(ip))
                if status == 101:
                    raise UnsafeTarget("HTTP protocol upgrade unsupported")
                if 100 <= status < 200:
                    if interim >= MAX_INFORMATIONAL or remaining_headers <= 0:
                        raise UnsafeTarget("too many informational HTTP headers")
                    continue
                return status, headers
            raise UnsafeTarget("final HTTP status not received")


def actual_probe(receipt: dict, url: str, allowed: frozenset[str],
                 total_deadline: float) -> dict:
    """Probe one inventory URL with no automatic redirects or proxy fallback."""
    target = choose_inventory_url(receipt, url, allowed)
    seen: list[str] = []
    for hop in range(MAX_HOPS + 1):
        checked_budget(total_deadline)
        if len(target.url) > MAX_URL_LENGTH:
            raise UnsafeTarget("redirect exceeds the maximum URL length")
        if target.url in seen:
            raise UnsafeTarget("redirect cycle")
        seen.append(target.url)
        dns_answers = resolve_all(target.hostname)
        # Reject the ENTIRE DNS set if even one address is not public.
        decision = bind_public_addresses(target, dns_answers)
        # Deterministic first approved IP; no hostname-based second resolution.
        numeric_ip = next((ip for ip in decision.public_ips
                           if not getattr(ipaddress.ip_address(ip),
                                          "ipv4_mapped", None)), None)
        if numeric_ip is None:
            raise UnsafeTarget("no supported un-mapped public address")
        checked_budget(total_deadline)
        status, headers = exchange(target, numeric_ip, "HEAD", total_deadline)
        if status in (405, 501):
            # HEAD unsupported: issue a bounded GET; close after its headers.
            # Even a server ignoring Range cannot cause an unbounded download.
            checked_budget(total_deadline)
            status, headers = exchange(target, numeric_ip, "GET", total_deadline)
        if 300 <= status <= 399:
            if hop >= MAX_HOPS:
                raise UnsafeTarget("redirect limit exceeded")
            location = headers.get("location")
            if not location:
                raise UnsafeTarget("redirect missing a single Location header")
            target = follow_redirect(target, location, allowed, tuple(seen))
            continue
        return {"outcome": classify(status), "status": status,
                "hops": len(seen), "final_url": target.url}
    raise UnsafeTarget("redirect limit exceeded")


def worker_result(receipt: dict, url: str, allowed: frozenset[str],
                  timeout: float) -> dict:
    """Classify each URL independently; never turn unknown errors into success."""
    started = time.monotonic()
    try:
        result = actual_probe(receipt, url, allowed, started + timeout)
    except TimeoutError:
        result = {"outcome": "TIMEOUT", "status": None}
    except LookupError:
        result = {"outcome": "DNS_ERROR", "status": None}
    except ssl.SSLError:
        result = {"outcome": "TLS_ERROR", "status": None}
    except UnsafeTarget:
        result = {"outcome": "UNSAFE_TARGET", "status": None}
    except OSError:
        result = {"outcome": "NETWORK_ERROR", "status": None}
    result["url"] = url
    result["observed_at"] = utc_now()
    return result


def isolated_worker(url: str, hosts: tuple[str, ...], seconds: float,
                    expected_sha: str, expected_fingerprint: str) -> dict:
    """Hard-stop a worker even when DNS or TLS blocks without a socket timeout."""
    args = [sys.executable, "-I", str(Path(__file__).resolve()),
            "--_worker", "--network-opt-in", "--timeout", str(seconds),
            "--_expected-sha", expected_sha,
            "--_expected-fingerprint", expected_fingerprint,
            "--url", url]
    for host in hosts:
        args += ["--host", host]
    # No proxy, SSL_CERT_FILE, PYTHONPATH or user-supplied environment is inherited.
    environment = {"PYTHONDONTWRITEBYTECODE": "1"}
    use_session = os.name == "posix"
    deadline = time.monotonic() + seconds
    try:
        process = subprocess.Popen(
            args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
            stderr=subprocess.DEVNULL, env=environment, close_fds=True,
            start_new_session=use_session,
        )
    except OSError:
        return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                "observed_at": utc_now()}
    try:
        try:
            out, _ = process.communicate(
                timeout=max(.001, deadline - time.monotonic()))
        except subprocess.TimeoutExpired:
            return {"outcome": "TIMEOUT", "status": None, "url": url,
                    "observed_at": utc_now()}
        if process.returncode != 0 or len(out) > MAX_CHILD_OUTPUT:
            return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                    "observed_at": utc_now()}
        try:
            result = json.loads(out)
        except (ValueError, UnicodeDecodeError):
            return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                    "observed_at": utc_now()}
        if (not isinstance(result, dict) or result.get("url") != url
                or result.get("checkout_sha") != expected_sha
                or result.get("fingerprint_sha256") != expected_fingerprint
                or result.get("outcome") not in STATUS_CODES
                or not isinstance(result.get("observed_at"), str)):
            return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                    "observed_at": utc_now()}
        return result
    finally:
        if process.poll() is None:
            try:
                if use_session:
                    os.killpg(process.pid, signal.SIGKILL)
                else:
                    process.kill()
            except ProcessLookupError:
                # The child can exit between poll and the termination signal.
                pass
        process.wait()


class RealJournal:
    """Exclusive-create, fsynced REAL_HTTP records, not simulated receipts."""

    def __init__(self, path: Path, receipt: dict, urls: tuple[str, ...]):
        if (not urls or len(urls) != len(set(urls))
                or any(not isinstance(url, str) for url in urls)):
            raise UnsafeTarget("journal selection must contain unique URLs")
        self.fd = _safe_fd(path)
        self.previous = ZERO_SHA
        self.count = 0
        self.closed = False
        self.finished = False
        self.receipt = receipt
        self.urls = urls
        self.completed: set[str] = set()
        try:
            self.append({"kind": "start", "schema": SCHEMA, "mode": "REAL_HTTP",
                         "checkout_sha": receipt["checkout_sha"],
                         "fingerprint_sha256": receipt["fingerprint_sha256"],
                         "urls": urls, "started_at": utc_now()})
            _sync_directory(path)
        except BaseException:
            self.close()
            raise

    def append(self, record: dict) -> None:
        if self.closed or self.finished:
            raise UnsafeTarget("journal closed or already finished")
        content = {**record, "sequence": self.count,
                   "previous_sha256": self.previous}
        checksum = hashlib.sha256(_encode(content)).hexdigest()
        data = _encode({**content, "record_sha256": checksum})
        pending = memoryview(data)
        while pending:
            written = os.write(self.fd, pending)
            if written <= 0:
                raise OSError("journal write did not progress")
            pending = pending[written:]
        os.fsync(self.fd)
        self.previous = hashlib.sha256(data).hexdigest()
        self.count += 1

    def result(self, outcome: dict) -> None:
        if not isinstance(outcome, dict) or outcome.get("outcome") not in STATUS_CODES:
            raise UnsafeTarget("not an approved REAL_HTTP result")
        url = outcome.get("url")
        if not isinstance(url, str) or url not in self.urls or url in self.completed:
            raise UnsafeTarget("result not selected, or URL already completed")
        if (not isinstance(outcome.get("observed_at"), str)
                or outcome.get("status") is not None
                and (type(outcome["status"]) is not int or not 100 <= outcome["status"] <= 599)):
            raise UnsafeTarget("invalid result timestamp or status")
        self.append({"kind": "result", **outcome})
        self.completed.add(url)

    def finish(self) -> None:
        if self.completed != set(self.urls):
            raise UnsafeTarget("incomplete URL journal cannot be finalized")
        self.append({"kind": "finish", "completed": len(self.completed),
                     "finished_at": utc_now()})
        self.finished = True

    def close(self) -> None:
        if not self.closed:
            os.close(self.fd)
            self.closed = True

    def __enter__(self):
        return self

    def __exit__(self, *_exc):
        self.close()


def inspect_real_journal(path: Path) -> dict:
    """Verify every complete JSONL record; preserve partial but report torn tails."""
    entries = []
    previous = ZERO_SHA
    torn_tail = False
    with path.open("rb") as handle:
        while True:
            raw = handle.readline(MAX_RECORD_BYTES + 1)
            if not raw:
                break
            if len(raw) > MAX_RECORD_BYTES:
                raise UnsafeTarget("overlong REAL_HTTP journal line")
            if not raw.endswith(b"\n"):
                torn_tail = True
                break
            try:
                entry = json.loads(raw)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise UnsafeTarget("corrupt complete REAL_HTTP journal entry") from error
            if not isinstance(entry, dict):
                raise UnsafeTarget("invalid REAL_HTTP journal entry type")
            checksum = entry.get("record_sha256")
            unsigned = {key: val for key, val in entry.items()
                        if key != "record_sha256"}
            if (not isinstance(checksum, str)
                    or hashlib.sha256(_encode(unsigned)).hexdigest() != checksum
                    or entry.get("sequence") != len(entries)
                    or entry.get("previous_sha256") != previous):
                raise UnsafeTarget("REAL_HTTP journal checksum or chain mismatch")
            previous = hashlib.sha256(raw).hexdigest()
            entries.append(entry)
    if not entries or entries[0].get("kind") != "start":
        raise UnsafeTarget("REAL_HTTP journal has no start receipt")
    start = entries[0]
    if (start.get("schema") != SCHEMA or start.get("mode") != "REAL_HTTP"
            or not isinstance(start.get("checkout_sha"), str)
            or len(start["checkout_sha"]) != 40
            or not isinstance(start.get("fingerprint_sha256"), str)
            or len(start["fingerprint_sha256"]) != 64):
        raise UnsafeTarget("unsupported or source-unbound REAL_HTTP journal")
    urls = start.get("urls")
    if (not isinstance(urls, list) or not urls
            or any(not isinstance(url, str) for url in urls)
            or len(set(urls)) != len(urls)):
        raise UnsafeTarget("invalid REAL_HTTP URL selection")
    completed = set()
    finished = False
    for entry in entries[1:]:
        if finished:
            raise UnsafeTarget("unexpected event after REAL_HTTP finish")
        if entry.get("kind") == "result":
            url = entry.get("url")
            outcome = entry.get("outcome")
            if (not isinstance(url, str) or url not in urls or url in completed
                    or not isinstance(outcome, str) or outcome not in STATUS_CODES):
                raise UnsafeTarget("invalid or duplicated REAL_HTTP URL result")
            completed.add(url)
        elif entry.get("kind") == "finish":
            if completed != set(urls) or entry.get("completed") != len(completed):
                raise UnsafeTarget("premature REAL_HTTP finish")
            finished = True
        else:
            raise UnsafeTarget("invalid REAL_HTTP journal event")
    if torn_tail and finished:
        raise UnsafeTarget("unexpected torn data following completed journal")
    return {"state": "COMPLETE" if finished else "PARTIAL",
            "integrity": "TRUNCATED_TAIL" if torn_tail else "CHAIN_OK",
            "recorded": len(completed), "selected": len(urls),
            "checkout_sha": start["checkout_sha"],
            "fingerprint_sha256": start["fingerprint_sha256"]}



def selftest() -> int:
    """Run fixture-only checks; no DNS resolver or socket is invoked."""
    from unittest.mock import patch

    negative = 0

    class FakeTLS:
        def __init__(self, payload):
            self.data = bytearray(payload)
            self.sent = b""
            self.timeout = 0

        def settimeout(self, timeout):
            self.timeout = timeout

        def recv(self, count):
            if not self.data:
                return b""
            result = bytes(self.data[:count])
            del self.data[:count]
            return result

    # Reading stops at exactly the first CRLF-CRLF (never consumes body bytes).
    stream = FakeTLS(b"HTTP/1.1 302 Found\r\nLocation: /b\r\n\r\nBODY")
    with patch(__name__ + ".checked_budget", return_value=2):
        headers = header_from_socket(stream, time.monotonic() + 2)
    assert headers == b"HTTP/1.1 302 Found\r\nLocation: /b\r\n\r\n"
    assert stream.data == b"BODY"
    for payload in (b"HTTP/1.1 200 OK\r\nno-ending",
                    b"HTTP/1.1 200 OK\r\nA: " + b"x" * 9000):
        stream = FakeTLS(payload)
        try:
            with patch(__name__ + ".checked_budget", return_value=2):
                header_from_socket(stream, 100)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("malformed/oversized HTTP header accepted")

    # Assert that the live transport construction itself chooses a numeric
    # sockaddr, checks the peer, passes the hostname to TLS, and sends Host.
    class FakeRaw:
        def __init__(self, peer="8.8.8.8"):
            self.peer = peer
            self.destination = None

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def settimeout(self, _timeout):
            return None

        def connect(self, address):
            self.destination = address

        def getpeername(self):
            return (self.peer, 443)

    class FakeVerifiedTLS(FakeTLS):
        def __init__(self, payload, peer="8.8.8.8", certificate=True):
            super().__init__(payload)
            self.peer = peer
            self.certificate = certificate
            self.handshaken = False

        def __enter__(self):
            return self

        def __exit__(self, *_args):
            return None

        def do_handshake(self):
            self.handshaken = True

        def getpeercert(self):
            return {"subject": (("CN", "example.org"),)} if self.certificate else {}

        def getpeername(self):
            return (self.peer, 443)

        def sendall(self, payload):
            self.sent = payload

    class FakeContext:
        def __init__(self, wrapped):
            self.wrapped = wrapped
            self.sni = None
            self.check_hostname = False
            self.verify_mode = ssl.CERT_NONE

        def wrap_socket(self, _raw, *, server_hostname, do_handshake_on_connect):
            assert do_handshake_on_connect is False
            self.sni = server_hostname
            return self.wrapped

    target = target_from_url("https://example.org/a?b=1",
                             frozenset({"example.org"}))
    raw = FakeRaw()
    verified = FakeVerifiedTLS(b"HTTP/1.1 200 OK\r\n\r\nEXTRA")
    context = FakeContext(verified)
    with patch.object(socket, "socket", return_value=raw), \
            patch.object(ssl, "create_default_context", return_value=context), \
            patch(__name__ + ".checked_budget", return_value=2), \
            patch.dict(os.environ, {"HTTPS_PROXY": "http://127.0.0.1:9999"}):
        status, headers = exchange(target, "8.8.8.8", "HEAD", 100)
    assert status == 200 and headers == {}
    assert raw.destination == ("8.8.8.8", 443)
    assert context.sni == "example.org" and verified.handshaken
    assert context.check_hostname and context.verify_mode == ssl.CERT_REQUIRED
    assert b"HEAD /a?b=1 HTTP/1.1\r\n" in verified.sent
    assert b"Host: example.org\r\n" in verified.sent
    assert verified.data == b"EXTRA"

    for peer, certificate in (("127.0.0.1", True), ("8.8.8.8", False)):
        bad_raw = FakeRaw(peer)
        bad_tls = FakeVerifiedTLS(b"HTTP/1.1 200 OK\r\n\r\n",
                                  certificate=certificate)
        with patch.object(socket, "socket", return_value=bad_raw), \
                patch.object(ssl, "create_default_context",
                             return_value=FakeContext(bad_tls)), \
                patch(__name__ + ".checked_budget", return_value=2):
            try:
                exchange(target, "8.8.8.8", "HEAD", 100)
            except (UnsafeTarget, ssl.SSLError):
                negative += 1
            else:
                raise AssertionError("unsafe socket peer or missing certificate accepted")

    sample = {"schema": 1, "checkout_sha": "a" * 40,
              "fingerprint_sha256": "b" * 64, "unique_urls": 1,
              "links": [{"url": "https://example.org/a",
                         "references": [{"file": "a.md", "line": 1}]}]}
    url = "https://example.org/a"
    require_source_identity(sample, "a" * 40, "b" * 64)
    for mismatch_sha, mismatch_fingerprint in (
        ("f" * 40, "b" * 64), ("a" * 40, "f" * 64),
    ):
        try:
            require_source_identity(sample, mismatch_sha, mismatch_fingerprint)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("changed inventory identity passed worker admission")

    # Exercise the real orchestration logic with fully injected fake DNS and
    # exchange functions: no operating-system resolver or network is called.
    secure_hosts = frozenset({"example.org", "second.org"})
    dns_log = []
    exchange_log = []
    dns_map = {"example.org": ("8.8.8.8",), "second.org": ("1.1.1.1",)}
    response_map = {"example.org": (200, {}), "second.org": (200, {})}

    def fake_dns(host):
        dns_log.append(host)
        return dns_map[host]

    def fake_exchange(destination, ip, method, _deadline):
        exchange_log.append((destination.hostname, ip, method))
        return response_map[destination.hostname]

    with patch(__name__ + ".resolve_all", side_effect=fake_dns), \
            patch(__name__ + ".exchange", side_effect=fake_exchange):
        valid = actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        assert valid["outcome"] == "REACHABLE" and valid["hops"] == 1
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD")]
        dns_log.clear()
        exchange_log.clear()

        # An unsafe DNS answer poisons the entire set before any TCP attempt.
        dns_map["example.org"] = ("8.8.8.8", "10.0.0.1")
        try:
            actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("mixed public/private DNS was accepted")
        assert not exchange_log
        dns_map["example.org"] = ("8.8.8.8",)
        dns_log.clear()

        # A redirect to a second allowlisted hostname must re-resolve and
        # pin a distinct numeric address before its next exchange.
        response_map["example.org"] = (302, {"location": "https://second.org/z"})
        rerouted = actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        assert rerouted["hops"] == 2 and rerouted["outcome"] == "REACHABLE"
        assert dns_log == ["example.org", "second.org"]
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD"),
                                ("second.org", "1.1.1.1", "HEAD")]
        dns_log.clear()
        exchange_log.clear()

        dns_map["second.org"] = ("1.1.1.1", "169.254.169.254")
        try:
            actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("redirect poisoned with link-local IP was accepted")
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD")]
        dns_map["second.org"] = ("1.1.1.1",)
        exchange_log.clear()

        response_map["example.org"] = (302, {"location": "https://evil.org/secret"})
        try:
            actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("redirect to unauthorized host was accepted")
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD")]
        exchange_log.clear()

        response_map["example.org"] = (
            302, {"location": "https://second.org/" + "x" * (MAX_URL_LENGTH + 1)})
        try:
            actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("oversized redirect was accepted")
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD")]
        exchange_log.clear()

        # A 405 HEAD response triggers exactly one bounded GET request at
        # the approved numeric IP, without another hostname-based connect.
        response_map["example.org"] = (405, {})
        def fake_head_get(destination, ip, method, _deadline):
            exchange_log.append((destination.hostname, ip, method))
            return (405, {}) if method == "HEAD" else (206, {})
        with patch(__name__ + ".exchange", side_effect=fake_head_get):
            fallback = actual_probe(sample, url, secure_hosts, time.monotonic() + 5)
        assert fallback["outcome"] == "REACHABLE"
        assert exchange_log == [("example.org", "8.8.8.8", "HEAD"),
                                ("example.org", "8.8.8.8", "GET")]

    with tempfile.TemporaryDirectory(prefix="p012-real-fixture-") as directory:
        file = Path(directory) / "results.jsonl"
        with RealJournal(file, sample, (url,)) as journal:
            journal.result({"url": url, "outcome": "TIMEOUT",
                            "status": None, "observed_at": utc_now()})
            saved = file.read_bytes()
            assert b'"mode":"REAL_HTTP"' in saved
            assert b'"outcome":"TIMEOUT"' in saved
            assert b'"record_sha256"' in saved
            assert inspect_real_journal(file)["state"] == "PARTIAL"
            try:
                journal.result({"url": url, "outcome": "TIMEOUT",
                                "status": None, "observed_at": utc_now()})
            except UnsafeTarget:
                negative += 1
            else:
                raise AssertionError("duplicate REAL_HTTP receipt accepted")
            journal.finish()
        assert inspect_real_journal(file)["state"] == "COMPLETE"
        last = file.read_bytes()
        tampered = Path(directory) / "tampered.jsonl"
        tampered.write_bytes(last.replace(b'"outcome":"TIMEOUT"',
                                          b'"outcome":"GONE"', 1))
        try:
            inspect_real_journal(tampered)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("mutated REAL_HTTP receipt accepted")
        partial = Path(directory) / "interrupted.jsonl"
        partial.write_bytes(b"".join(last.splitlines(keepends=True)[:2]))
        assert inspect_real_journal(partial)["state"] == "PARTIAL"
        partial.write_bytes(partial.read_bytes() + b'{"kind":"result",')
        assert inspect_real_journal(partial)["integrity"] == "TRUNCATED_TAIL"
        try:
            RealJournal(file, sample, (url,))
        except FileExistsError:
            negative += 1
        else:
            raise AssertionError("journal overwrite accepted")
    for raw in ("127.0.0.1%eth0", "untrusted"):
        try:
            validated_ip(raw)
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("untrusted socket peer accepted")
    # Explicit non-network default is tested by invoking main without opt-in.
    return negative


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true")
    parser.add_argument("--network-opt-in", action="store_true",
                        help="EXPLICIT consent to run HTTPS requests outside Static/CI")
    parser.add_argument("--host", action="append", default=[],
                        help="Exact allowed hostname (repeat for each authorized host)")
    parser.add_argument("--url", action="append", default=[],
                        help="Exact URL selected from the current checked-out inventory")
    parser.add_argument("--journal", type=Path)
    parser.add_argument("--timeout", type=float, default=8.0)
    parser.add_argument("--_worker", action="store_true", help=argparse.SUPPRESS)
    parser.add_argument("--_expected-sha", help=argparse.SUPPRESS)
    parser.add_argument("--_expected-fingerprint", help=argparse.SUPPRESS)
    args = parser.parse_args()
    if not args.network_opt_in:
        number = selftest()
        print("P012-LIVE-HTTPS-TRANSPORT-EVIDENCE status=PASS"
              f" negative_cases={number} offline_default=PASS"
              " simulated_reader=PASS journal=LOCAL_ONLY"
          " journal_partial=PASS record_integrity=PASS network=0"
              " dns=NOT_EXECUTED tls=NOT_EXECUTED http=NOT_EXECUTED"
              " live_security_review=PENDING release_authorization=NONE")
        return

    if (not math.isfinite(args.timeout) or not 1 <= args.timeout <= 30
            or not args.host or not args.url or len(args.url) > MAX_SELECTED
            or len(args.url) != len(set(args.url))
            or any(len(url) > MAX_URL_LENGTH for url in args.url)):
        parser.error("explicit hosts, unique inventoried URLs and 1-30s budget required")
    try:
        allowed = frozenset(_host(host) for host in args.host)
        if len(allowed) != len(args.host):
            raise UnsafeTarget("duplicate or noncanonical allowlisted host")
        source = trusted_source_inventory()
        for url in args.url:
            choose_inventory_url(source, url, allowed)
    except (UnsafeTarget, OSError, subprocess.CalledProcessError) as error:
        parser.error(f"inventory or host validation failed: {error}")

    if args._worker:
        if len(args.url) != 1:
            parser.error("worker requires exactly one selected URL")
        try:
            require_source_identity(source, args._expected_sha,
                                    args._expected_fingerprint)
        except UnsafeTarget as error:
            parser.error(str(error))
        result = worker_result(source, args.url[0], allowed, args.timeout)
        result["checkout_sha"] = source["checkout_sha"]
        result["fingerprint_sha256"] = source["fingerprint_sha256"]
        print(json.dumps(result, ensure_ascii=True, separators=(",", ":")))
        return

    if args.journal is None or not args.journal.is_absolute():
        parser.error("--journal must be a new absolute path")
    if args.journal.resolve().is_relative_to(Path(ROOT).resolve()):
        parser.error("--journal must be outside the Git working tree")
    with RealJournal(args.journal, source, tuple(args.url)) as journal:
        for url in args.url:
            journal.result(isolated_worker(url, tuple(sorted(allowed)), args.timeout,
                                           source["checkout_sha"],
                                           source["fingerprint_sha256"]))
        journal.finish()
    print("P012-LIVE-HTTPS-PROBE status=COMPLETE"
          f" urls={len(args.url)} journal={args.journal}"
          " source_bound=RECOMPUTED_FROM_CLEAN_GIT_CHECKOUT"
          " release_authorization=NONE")


if __name__ == "__main__":
    main()
