#!/usr/bin/env python3
"""Offline-only P0.12 pinned HTTPS routing contract and simulated adversarial tests.

No socket, DNS, TLS or HTTP client exists in this module. A future *real*
transport must prove the properties modeled here with independently audited
socket/TLS implementation and explicit opt-in, not self-reported mock fields.
"""
from __future__ import annotations

import argparse
import ipaddress
import re
from dataclasses import dataclass
from typing import Callable

from p012_probe_security_policy import (
    Deadline, UnsafeTarget, bind_public_addresses, choose_inventory_url,
    follow_redirect, target_from_url,
)

MAX_HEADER_BYTES = 8192
MAX_HOPS = 3
STATUS_LINE = re.compile(rb"HTTP/1\.[01] ([1-5][0-9][0-9])(?: [^\r\n]*)?\r\n")
HEADER_NAME = re.compile(rb"[!#$%&'*+\-.^_`|~0-9A-Za-z]+")
SUCCESS_STATUSES = frozenset(range(200, 300))


@dataclass(frozen=True)
class HopProof:
    """Data emitted by a fake adapter; not authentic TLS/network evidence."""

    connected_ip: str
    peer_ip: str
    sni: str
    certificate_hostname: str
    certificate_validated: bool
    host_header: str
    proxy_used: bool
    header_bytes: bytes
    body_bytes_consumed: int = 0


@dataclass(frozen=True)
class ProbeResult:
    url: str
    outcome: str
    hops: int
    status: int | None


def _canonical_ip(raw: str) -> str:
    if not isinstance(raw, str) or "%" in raw:
        raise UnsafeTarget("peer has a noncanonical or scoped IP")
    try:
        return str(ipaddress.ip_address(raw))
    except ValueError as error:
        raise UnsafeTarget("invalid peer IP") from error


def inspect_proof(proof: HopProof, target, pinned_ip: str) -> tuple[int, dict[str, str]]:
    """Check modeled direct routing, peer, TLS identity and bounded HEAD headers."""
    if not isinstance(proof, HopProof):
        raise UnsafeTarget("invalid transport evidence")
    if (_canonical_ip(proof.connected_ip) != _canonical_ip(pinned_ip)
            or _canonical_ip(proof.peer_ip) != _canonical_ip(pinned_ip)):
        raise UnsafeTarget("connected or peer IP differs from the pinned address")
    if proof.proxy_used:
        raise UnsafeTarget("unexpected proxy or delegated resolution")
    if (proof.sni != target.hostname or proof.certificate_hostname != target.hostname
            or not proof.certificate_validated):
        raise UnsafeTarget("hostname/SNI/certificate identity not verified")
    if proof.host_header != target.hostname:
        raise UnsafeTarget("HTTP Host differs from requested hostname")
    if proof.body_bytes_consumed != 0:
        raise UnsafeTarget("response body was consumed")
    raw = proof.header_bytes
    if (not isinstance(raw, bytes) or len(raw) > MAX_HEADER_BYTES
            or not raw.endswith(b"\r\n\r\n") or b"\x00" in raw):
        raise UnsafeTarget("unbounded or malformed response headers")
    lines = raw[:-2].split(b"\r\n")
    match = STATUS_LINE.fullmatch(lines[0] + b"\r\n")
    if not match:
        raise UnsafeTarget("malformed HTTP/1 response status line")
    status = int(match.group(1))
    headers: dict[str, str] = {}
    for line in lines[1:]:
        if not line:
            continue
        if b":" not in line:
            raise UnsafeTarget("malformed HTTP header")
        key, value = line.split(b":", 1)
        if (not HEADER_NAME.fullmatch(key) or
                any(char < 32 and char != 9 or char == 127 for char in value)):
            raise UnsafeTarget("header contains invalid tokens or controls")
        name = key.decode("ascii").lower()
        if name in headers:
            if name == "location":
                raise UnsafeTarget("ambiguous duplicate redirect location")
            continue
        headers[name] = value.strip(b" \t").decode("latin-1")
    return status, headers


def classify(status: int) -> str:
    """Keep access controls, missing documents and throttling distinct."""
    if status in SUCCESS_STATUSES:
        return "REACHABLE"
    if status in (401, 403):
        return "ACCESS_RESTRICTED"
    if status == 404:
        return "NOT_FOUND"
    if status == 410:
        return "GONE"
    if status == 429:
        return "RATE_LIMITED"
    if status in (405, 501):
        return "HEAD_UNSUPPORTED"
    return "HTTP_OTHER"


def _remaining_as_timeout(deadline: Deadline, now: float) -> float:
    """Classify an expired total deadline as timeout, not unsafe routing."""
    try:
        return deadline.remaining(now)
    except UnsafeTarget as error:
        raise TimeoutError("simulated total deadline exhausted") from error


def inspect_route_simulation(
    receipt: dict, url: str, allowed_hosts: frozenset[str],
    resolve: Callable[[str], tuple[str, ...]],
    simulated_connect: Callable[[str, str, float], HopProof],
    clock: Callable[[], float], deadline_expires_at: float,
) -> ProbeResult:
    """Exercise policy with injected fake interfaces; NEVER connect to a network.

    The resolver and simulated connector are untrusted fixtures. Runtime
    security cannot rely on self-reported HopProof values.
    """
    start_url = url
    seen: list[str] = []
    try:
        target = choose_inventory_url(receipt, url, allowed_hosts)
        budget = Deadline(deadline_expires_at)
        for hop in range(MAX_HOPS + 1):
            if target.url in seen:
                raise UnsafeTarget("redirect cycle")
            seen.append(target.url)
            _remaining_as_timeout(budget, clock())
            answers = resolve(target.hostname)
            pinned = bind_public_addresses(target, answers)
            # A later socket implementation MUST use this pinned numeric IP,
            # not the hostname or a client that resolves the name again.
            chosen_ip = pinned.public_ips[0]
            proof = simulated_connect(target.hostname, chosen_ip,
                                      _remaining_as_timeout(budget, clock()))
            _remaining_as_timeout(budget, clock())
            status, headers = inspect_proof(proof, target, chosen_ip)
            if 300 <= status <= 399:
                if hop >= MAX_HOPS:
                    raise UnsafeTarget("redirect hop limit exceeded")
                location = headers.get("location")
                if not location:
                    raise UnsafeTarget("redirect response without Location")
                target = follow_redirect(target, location, allowed_hosts,
                                         tuple(seen))
                continue
            return ProbeResult(start_url, classify(status), len(seen), status)
        raise UnsafeTarget("redirect limit exhausted")
    except UnsafeTarget:
        return ProbeResult(start_url, "UNSAFE_TARGET", len(seen), None)
    except TimeoutError:
        return ProbeResult(start_url, "TIMEOUT", len(seen), None)
    except OSError:
        return ProbeResult(start_url, "SIMULATED_NETWORK_ERROR", len(seen), None)


def _headers(code: int, location: str | None = None) -> bytes:
    lines = [f"HTTP/1.1 {code} Mock".encode("ascii")]
    if location is not None:
        lines.append(b"Location: " + location.encode("ascii"))
    return b"\r\n".join(lines) + b"\r\n\r\n"


def selftest() -> int:
    """Use only fake resolvers and fake TLS connections; assert security refusals."""
    url_a = "https://example.org/a"
    url_b = "https://second.org/b"
    receipt = {
        "schema": 1, "checkout_sha": "a" * 40,
        "fingerprint_sha256": "b" * 64, "unique_urls": 2,
        "links": [
            {"url": url_a, "references": [{"file": "a.md", "line": 1}]},
            {"url": url_b, "references": [{"file": "b.md", "line": 2}]},
        ],
    }
    allowed = frozenset({"example.org", "second.org"})
    counts = {"dns": 0, "connect": 0, "negative": 0}
    addresses = {"example.org": ("8.8.8.8",),
                 "second.org": ("1.1.1.1",)}
    status_by_host = {"example.org": _headers(200),
                      "second.org": _headers(200)}
    edits = {}

    def resolver(host):
        counts["dns"] += 1
        return addresses[host]

    def connector(host, ip, remaining):
        counts["connect"] += 1
        assert remaining > 0
        override = edits.get(host, {})
        return HopProof(
            connected_ip=override.get("connected_ip", ip),
            peer_ip=override.get("peer_ip", ip),
            sni=override.get("sni", host),
            certificate_hostname=override.get("certificate_hostname", host),
            certificate_validated=override.get("certificate_validated", True),
            host_header=override.get("host_header", host),
            proxy_used=override.get("proxy_used", False),
            header_bytes=override.get("header_bytes", status_by_host[host]),
            body_bytes_consumed=override.get("body_bytes_consumed", 0),
        )

    def run(start=url_a, hosts=allowed, now=lambda: 100.0, end=102.0):
        return inspect_route_simulation(
            receipt, start, hosts, resolver, connector, now, end)

    assert run().outcome == "REACHABLE"
    assert counts["dns"] == 1 and counts["connect"] == 1

    def reject(expected="UNSAFE_TARGET", start=url_a, hosts=allowed,
               now=lambda: 100.0, end=102.0):
        counts["negative"] += 1
        actual = run(start, hosts, now, end).outcome
        assert actual == expected, (actual, expected)

    # An explicit host allowlist does not authorize additional DNS names.
    old_connect = counts["connect"]
    reject(start=url_a, hosts=frozenset({"second.org"}))
    assert counts["connect"] == old_connect

    # A mixed public/private DNS reply is rejected before any connection.
    addresses["example.org"] = ("8.8.8.8", "10.0.0.1")
    reject()
    assert counts["connect"] == old_connect
    addresses["example.org"] = ("8.8.8.8",)

    for property_name, value in (
        ("connected_ip", "127.0.0.1"),
        ("peer_ip", "127.0.0.1"),
        ("sni", "evil.org"),
        ("certificate_hostname", "evil.org"),
        ("certificate_validated", False),
        ("host_header", "evil.org"),
        ("proxy_used", True),
        ("body_bytes_consumed", 100),
        ("header_bytes", b"HTTP/1.1 200 OK\r\nA: " + b"x" * 9000 + b"\r\n\r\n"),
        ("header_bytes", b"HTTP/1.1 302 Found\r\nLocation: /x\r\nLocation: /y\r\n\r\n"),
        ("header_bytes", b"HTTP/1.1 200 OK\r\nBad header\r\n\r\n"),
    ):
        edits["example.org"] = {property_name: value}
        reject()
    edits.clear()

    for code, outcome in ((403, "ACCESS_RESTRICTED"), (404, "NOT_FOUND"),
                          (410, "GONE"), (429, "RATE_LIMITED"),
                          (405, "HEAD_UNSUPPORTED"), (503, "HTTP_OTHER")):
        status_by_host["example.org"] = _headers(code)
        assert run().outcome == outcome
    status_by_host["example.org"] = _headers(200)

    # A redirect performs a new DNS approval and uses the redirected host.
    old_dns, old_connected = counts["dns"], counts["connect"]
    status_by_host["example.org"] = _headers(302, url_b)
    success = run()
    assert success.outcome == "REACHABLE" and success.hops == 2
    assert counts["dns"] == old_dns + 2 and counts["connect"] == old_connected + 2
    status_by_host["example.org"] = _headers(302, "https://evil.org/secret")
    reject()
    status_by_host["example.org"] = _headers(302, url_a)
    reject()
    status_by_host["example.org"] = _headers(302, url_b)
    addresses["second.org"] = ("1.1.1.1", "169.254.169.254")
    reject()
    addresses["second.org"] = ("1.1.1.1",)
    status_by_host["example.org"] = _headers(200)

    # DNS/connection time are part of the same logical deadline.
    reject("TIMEOUT", now=lambda: 102.1)
    reject("UNSAFE_TARGET", start="https://example.org/not-in-inventory")
    return counts["negative"]


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="Run fake DNS/TLS tests; no real socket is available")
    parser.parse_args()
    count = selftest()
    print("P012-PINNED-TLS-CONTRACT-EVIDENCE status=PASS"
          f" negative_cases={count} verified_fake_route=PASS"
          " fake_redirect_dns_revalidation=PASS"
          " tls_hostname_sni_host=FAKE_VALIDATED"
          " proxy_path=FAKE_DENIED header_cap=PASS"
          " offline=1 network=0 dns=NOT_EXECUTED"
          " tls=NOT_EXECUTED http=NOT_IMPLEMENTED"
          " independent_security_review=PENDING release_authorization=NONE")


if __name__ == "__main__":
    main()
