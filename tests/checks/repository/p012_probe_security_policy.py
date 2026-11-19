#!/usr/bin/env python3
"""Offline-only security preflight for a future opt-in external-link probe.

No DNS, sockets, proxies or HTTP transport are implemented here. An approved
transport must connect to a pinned, policy-approved IP and verify the URL host
as the TLS peer name; adding a normal URL-opening client is forbidden.
"""
from __future__ import annotations

import argparse
import ipaddress
import math
import re
from dataclasses import dataclass
from urllib.parse import urljoin, urlsplit, urlunsplit

HEX40 = re.compile(r"[0-9a-f]{40}\Z")
HEX64 = re.compile(r"[0-9a-f]{64}\Z")
DNS_LABEL = re.compile(r"[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\Z")
# inet_aton-style numbers can resolve to loopback, even when ipaddress rejects them.
LEGACY_IPV4 = re.compile(r"(?:0x[0-9a-f]+|0[0-7]+|[0-9]+)(?:\.(?:0x[0-9a-f]+|0[0-7]+|[0-9]+)){0,3}\Z")
DENIED_SUFFIXES = (
    ".localhost", ".local", ".lan", ".internal", ".home.arpa",
    ".test", ".invalid", ".onion", ".example", ".localdomain",
)
MAX_REDIRECTS = 3


class UnsafeTarget(ValueError):
    """Classify an unsafe target without contacting it."""


@dataclass(frozen=True)
class Target:
    url: str
    hostname: str
    tls_port: int = 443


@dataclass(frozen=True)
class PinnedEndpoint:
    """An immutable socket routing decision; not a socket implementation."""

    target: Target
    public_ips: tuple[str, ...]


@dataclass(frozen=True)
class Deadline:
    """One total budget shared by DNS, TLS, redirects and HTTP."""

    expires_at: float

    def remaining(self, now: float) -> float:
        left = self.expires_at - now
        if not math.isfinite(left) or left <= 0:
            raise UnsafeTarget("total URL deadline exhausted")
        return left


def _host(host: str) -> str:
    """Reject ambiguous, internal and non-canonical DNS spellings."""
    if not host or not host.isascii() or len(host) > 253 or host.endswith("."):
        raise UnsafeTarget("non-canonical hostname")
    host = host.lower()
    if host in {"localhost", "localdomain", "home.arpa"} or host.endswith(DENIED_SUFFIXES):
        raise UnsafeTarget("internal or reserved hostname")
    try:
        ipaddress.ip_address(host)
    except ValueError:
        pass
    else:
        raise UnsafeTarget("direct IP literals are not supported")
    labels = host.split(".")
    if len(labels) < 2 or labels[-1].isdecimal() or LEGACY_IPV4.fullmatch(host):
        raise UnsafeTarget("single-label or legacy numeric IPv4 hostname")
    if any(not DNS_LABEL.fullmatch(label) for label in labels):
        raise UnsafeTarget("invalid DNS label")
    return host


def target_from_url(raw: str, allowed_hosts: frozenset[str]) -> Target:
    """Allow only explicitly approved HTTPS hosts and the default TLS port."""
    if (not isinstance(raw, str) or not raw or not raw.isascii()
            or any(ord(c) < 33 or ord(c) > 126 or c == "\\" for c in raw)):
        raise UnsafeTarget("URL contains whitespace, control or ambiguous characters")
    try:
        uri = urlsplit(raw)
        name = uri.hostname
        port = uri.port
        user = uri.username
        password = uri.password
    except ValueError as error:
        raise UnsafeTarget("malformed URL authority or port") from error
    if uri.scheme.lower() != "https" or not name or not uri.netloc:
        raise UnsafeTarget("only absolute HTTPS URLs are supported")
    if user is not None or password is not None or "@" in uri.netloc:
        raise UnsafeTarget("credentials or userinfo forbidden")
    if uri.netloc.endswith(":") or port not in (None, 443):
        raise UnsafeTarget("nonstandard or empty port forbidden")
    host = _host(name)
    if host not in allowed_hosts:
        raise UnsafeTarget("host not explicitly allowlisted")
    path = uri.path or "/"
    authority = host if port is None else host + ":443"
    return Target(urlunsplit(("https", authority, path, uri.query, "")), host)


def bind_public_addresses(target: Target, dns_answers: tuple[str, ...]) -> PinnedEndpoint:
    """Require every DNS answer to be a global unicast IP before pinning."""
    if not dns_answers:
        raise UnsafeTarget("DNS response contains no addresses")
    approved: set[str] = set()
    for raw in dns_answers:
        # Reject scope identifiers and non-string values before IP parsing.
        # Scoped IPv6 literals can change the selected local network interface.
        if not isinstance(raw, str) or "%" in raw:
            raise UnsafeTarget("DNS answer is not an unscoped IP literal")
        try:
            ip = ipaddress.ip_address(raw)
        except ValueError as error:
            raise UnsafeTarget("DNS response is not an IP address") from error
        if isinstance(ip, ipaddress.IPv6Address) and ip.ipv4_mapped:
            # IPv4-mapped IPv6 is allowed only when its embedded IPv4 is public.
            # Classify the embedded address explicitly across Python versions.
            mapped = ip.ipv4_mapped
            if (not mapped.is_global or mapped.is_reserved
                    or mapped.is_multicast or mapped.is_unspecified):
                raise UnsafeTarget("non-global IPv4-mapped IPv6 address")
        elif (not ip.is_global or ip.is_multicast or ip.is_unspecified
              or ip.is_reserved
              or (isinstance(ip, ipaddress.IPv6Address) and ip.is_site_local)):
            raise UnsafeTarget("DNS response contains a non-global, reserved or site-local address")
        approved.add(str(ip))
    return PinnedEndpoint(target, tuple(sorted(approved)))


def follow_redirect(current: Target, location: str,
                    allowed_hosts: frozenset[str], visited: tuple[str, ...]) -> Target:
    """Normalize and re-approve every redirect, detecting loops and hop limits."""
    if len(visited) >= MAX_REDIRECTS + 1:
        raise UnsafeTarget("redirect limit exceeded")
    if (not isinstance(location, str) or not location or not location.isascii()
            or any(ord(c) < 33 or ord(c) > 126 or c == "\\" for c in location)):
        raise UnsafeTarget("empty or unsafe redirect target")
    try:
        resolved = urljoin(current.url, location)
    except ValueError as error:
        raise UnsafeTarget("malformed redirect URL") from error
    candidate = target_from_url(resolved, allowed_hosts)
    if candidate.url in visited:
        raise UnsafeTarget("redirect cycle")
    # The caller must resolve, validate and pin fresh DNS addresses on EVERY hop.
    return candidate


def receipt_urls(receipt: dict) -> frozenset[str]:
    """Validate the source-bound offline inventory's minimum provenance shape."""
    if not isinstance(receipt, dict) or receipt.get("schema") != 1:
        raise UnsafeTarget("unsupported inventory schema")
    if not HEX40.fullmatch(str(receipt.get("checkout_sha", ""))):
        raise UnsafeTarget("missing exact checkout SHA")
    if not HEX64.fullmatch(str(receipt.get("fingerprint_sha256", ""))):
        raise UnsafeTarget("missing inventory fingerprint")
    links = receipt.get("links")
    if not isinstance(links, list) or not links:
        raise UnsafeTarget("empty or invalid inventory")
    urls: list[str] = []
    for entry in links:
        if (not isinstance(entry, dict) or not isinstance(entry.get("url"), str)
                or not isinstance(entry.get("references"), list)
                or not entry["references"]):
            raise UnsafeTarget("inventory link lacks URL or source references")
        urls.append(entry["url"])
    if len(urls) != len(set(urls)) or receipt.get("unique_urls") != len(urls):
        raise UnsafeTarget("inventory has duplicate or inconsistent URLs")
    return frozenset(urls)


def choose_inventory_url(receipt: dict, url: str,
                         allowed_hosts: frozenset[str]) -> Target:
    """Prevent a probe from substituting arbitrary URLs for inventoried links."""
    if url not in receipt_urls(receipt):
        raise UnsafeTarget("requested URL is absent from the offline inventory")
    return target_from_url(url, allowed_hosts)


def selftest() -> int:
    """Run positive and adversarial controls without DNS or network calls."""
    failures_detected = 0

    def must_reject(function, *args):
        nonlocal failures_detected
        try:
            function(*args)
        except UnsafeTarget:
            failures_detected += 1
        else:
            raise AssertionError("negative security test unexpectedly accepted")

    hosts = frozenset({"example.org"})
    safe = target_from_url("https://example.org/a?x=1", hosts)
    assert safe.hostname == "example.org" and safe.tls_port == 443
    pinned = bind_public_addresses(safe, ("8.8.8.8", "2001:4860:4860::8888"))
    assert len(pinned.public_ips) == 2 and pinned.target == safe
    # A public IPv4-mapped IPv6 address is deliberately allowed when embedded IPv4 is public.
    assert bind_public_addresses(safe, ("::ffff:8.8.8.8",)).public_ips
    redirected = follow_redirect(safe, "/b", hosts, (safe.url,))
    assert redirected.url == "https://example.org/b"
    assert Deadline(102.0).remaining(100.0) == 2.0
    receipt = {"schema": 1, "checkout_sha": "a" * 40,
               "fingerprint_sha256": "b" * 64, "unique_urls": 2,
               "links": [{"url": safe.url, "references": [{"file": "README.md", "line": 1}]},
                         {"url": "http://example.org/inventory-only",
                          "references": [{"file": "docs/a.md", "line": 2}]}]}
    assert choose_inventory_url(receipt, safe.url, hosts) == safe

    for raw in (
        "http://example.org", "https://localhost/a", "https://service.local/a",
        "https://127.0.0.1/a", "https://2130706433/a", "https://127.1/a",
        "https://example.org:8080/a", "https://example.org:/a",
        "https://user:pass@example.org/a", "https://example.org@evil.org/a",
        "https://example.org\\@evil.org/a", "https://example.org/a\nb",
        "https://[::1]/a", "https://sub.example.org/a",
        "https://example.org:bad/a", "https://example.org./a",
        "https://example.org/a b", "javascript:alert(1)",
    ):
        must_reject(target_from_url, raw, hosts)
    # Test numeric aliases even when the caller explicitly allows the exact spelling.
    for numeric in ("0x7f.1", "0x7f.0x0.1", "0177.0.0.1",
                    "0x7f000001", "127.0x0.0.1", "0X7F.1"):
        must_reject(target_from_url, "https://" + numeric + "/",
                    frozenset({numeric.lower()}))
    must_reject(target_from_url, "https://home.arpa/", frozenset({"home.arpa"}))
    for answers in (
        (), ("8.8.8.8", "127.0.0.1"), ("169.254.169.254",),
        ("10.1.2.3",), ("::1",), ("fe80::1",),
        ("fc00::1",), ("fec0::1",), ("8.8.8.8", "fec0::1"),
        ("::2",), ("4000::1",), ("8.8.8.8", "::2"),
        ("8.8.8.8", "4000::1"), ("::ffff:127.0.0.1",),
        ("2001:4860:4860::8888%eth0",), ("::ffff:8.8.8.8%lo",),
        ("8.8.8.8", "2001:4860:4860::8888%eth0"),
        ("not-an-IP",),
    ):
        must_reject(bind_public_addresses, safe, answers)
    must_reject(follow_redirect, safe, "https://evil.org/", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "http://example.org/a", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "https://example.org/a\nb", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "https://[", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "https://[not-ip]/", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "https://example.org:bad/", hosts, (safe.url,))
    must_reject(follow_redirect, safe, "/b", hosts, (safe.url, redirected.url))
    must_reject(follow_redirect, safe, "/c", hosts,
                (safe.url, "https://example.org/x", "https://example.org/y",
                 "https://example.org/z"))
    must_reject(Deadline(102.0).remaining, 102.01)
    must_reject(Deadline(float("nan")).remaining, 100.0)
    must_reject(choose_inventory_url, receipt, "https://example.org/other", hosts)
    must_reject(choose_inventory_url, receipt, "http://example.org/inventory-only", hosts)
    must_reject(receipt_urls, {**receipt, "fingerprint_sha256": ""})
    must_reject(receipt_urls, {**receipt, "unique_urls": 3})
    return failures_detected


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="Run offline negative controls; no HTTP transport exists")
    parser.parse_args()
    count = selftest()
    print("P012-PROBE-PREFLIGHT-EVIDENCE status=PASS"
          f" negative_cases={count}"
          " network=0 dns=NOT_EXECUTED http=NOT_IMPLEMENTED"
          " source=OFFLINE_INVENTORY opt_in_transport=UNAVAILABLE"
          " security_review=PENDING release_authorization=NONE")


if __name__ == "__main__":
    main()
