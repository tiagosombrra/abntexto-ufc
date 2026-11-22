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
import selectors
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
    # Git can transparently call "fetch" for promised missing blobs in a
    # partial clone. Deny that before any source inventory read.
    git_env = os.environ.copy()
    git_env["GIT_NO_LAZY_FETCH"] = "1"
    git_env["GIT_TERMINAL_PROMPT"] = "0"
    head = subprocess.check_output(
        ["git", "--no-replace-objects", "rev-parse", "HEAD"],
        cwd=root, text=True, env=git_env,
    ).strip()
    raw_tree = subprocess.check_output(
        ["git", "--no-replace-objects", "ls-tree", "-r", "--name-only", "-z", head],
        cwd=root, env=git_env,
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
                ["git", "--no-replace-objects", "show", head + ":" + path.as_posix()],
                cwd=root, env=git_env,
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


_cancellation_signal: int | None = None


def _record_cancellation(signum: int) -> None:
    """Record a requested cancellation without raising inside a signal handler."""
    global _cancellation_signal
    if _cancellation_signal is None:
        _cancellation_signal = signum


def abort_on_sigterm(signum: int, _frame: object) -> None:
    """Defer SIGTERM until the worker supervisor can safely unwind."""
    _record_cancellation(signum)


def abort_on_sigint(signum: int, _frame: object) -> None:
    """Defer SIGINT until the worker supervisor can safely unwind."""
    _record_cancellation(signum)


def _raise_if_cancelled() -> None:
    """Propagate cancellation synchronously, never from a Python signal handler."""
    if _cancellation_signal == signal.SIGTERM:
        raise SystemExit(128 + signal.SIGTERM)
    if _cancellation_signal == signal.SIGINT:
        raise KeyboardInterrupt


def _read_unreaped_posix(process: subprocess.Popen, deadline: float) -> bytes | None:
    """Read child stdout without reaping its session leader before killpg().

    Popen.communicate() calls wait() after EOF, allowing the leader's PID/PGID
    to be reused before our final killpg(). Keep its zombie PID as an identity
    anchor using waitid(WNOWAIT), and reap only AFTER signaling the group.
    """
    if not (hasattr(os, "waitid") and hasattr(os, "WNOWAIT")):
        raise UnsafeTarget("non-reaping POSIX worker inspection is unavailable")
    if process.stdout is None:
        raise UnsafeTarget("POSIX worker stdout pipe is missing")
    output = bytearray()
    with selectors.DefaultSelector() as selector:
        selector.register(process.stdout, selectors.EVENT_READ)
        while True:
            _raise_if_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return None
            events = selector.select(timeout=min(0.1, remaining))
            for _key, _mask in events:
                chunk = os.read(process.stdout.fileno(), 4096)
                if not chunk:
                    selector.unregister(process.stdout)
                else:
                    output.extend(chunk)
                    if len(output) > MAX_CHILD_OUTPUT:
                        return bytes(output)
            if not selector.get_map():
                # Do not call process.poll(), communicate(), or wait() here:
                # every one of them may reap the leader and release its PGID.
                while True:
                    _raise_if_cancelled()
                    remaining = deadline - time.monotonic()
                    if remaining <= 0:
                        return None
                    status = os.waitid(
                        os.P_PID, process.pid,
                        os.WEXITED | os.WNOHANG | os.WNOWAIT)
                    if status is not None:
                        return bytes(output)
                    time.sleep(min(0.01, remaining))



def _parent_capability(url: str, hosts: tuple[str, ...], expected_sha: str,
                       expected_fingerprint: str, journal_start: str) -> bytes:
    """Bind an isolated worker's private pipe to a parent-owned journal."""
    if (len(journal_start) != 64 or journal_start == ZERO_SHA
            or any(c not in "0123456789abcdef" for c in journal_start)):
        raise UnsafeTarget("missing parent journal start checksum")
    payload = {
        "version": 1, "url": url, "hosts": list(hosts),
        "checkout_sha": expected_sha,
        "fingerprint_sha256": expected_fingerprint,
        "journal_start_sha256": journal_start,
        "parent_pid": os.getpid(),
    }
    raw = (json.dumps(payload, sort_keys=True, separators=(",", ":"))
           + "\n").encode("ascii")
    if len(raw) > MAX_CHILD_OUTPUT:
        raise UnsafeTarget("parent worker capability exceeds byte budget")
    return raw


def verify_parent_capability(fd: int, url: str, hosts: tuple[str, ...],
                             expected_sha: str, expected_fingerprint: str,
                             parent_pid: int | None = None) -> None:
    """Reject a naked internal CLI before ANY DNS, TLS or HTTP operations.

    An inherited anonymous pipe is a process-lifecycle capability, not a
    cryptographic defense against an arbitrary program running as the same
    local user. The parent only creates it after opening its O_EXCL journal.
    """
    import stat

    if os.name != "posix" or type(fd) is not int or fd < 3:
        raise UnsafeTarget("worker requires inherited POSIX parent pipe")
    try:
        with os.fdopen(fd, "rb") as handle:
            if not stat.S_ISFIFO(os.fstat(handle.fileno()).st_mode):
                raise UnsafeTarget("worker capability is not an inherited pipe")
            raw = handle.readline(MAX_CHILD_OUTPUT + 1)
            if (not raw.endswith(b"\n")
                    or len(raw) > MAX_CHILD_OUTPUT):
                raise UnsafeTarget("invalid or oversized parent capability")
            payload = json.loads(raw)
    except (OSError, ValueError, UnicodeDecodeError) as error:
        raise UnsafeTarget("missing or corrupt parent worker capability") from error
    if (not isinstance(payload, dict)
            or set(payload) != {
                "version", "url", "hosts", "checkout_sha",
                "fingerprint_sha256", "journal_start_sha256", "parent_pid",
            }
            or payload["version"] != 1
            or payload["url"] != url or payload["hosts"] != list(hosts)
            or payload["checkout_sha"] != expected_sha
            or payload["fingerprint_sha256"] != expected_fingerprint
            or type(payload["parent_pid"]) is not int
            or payload["parent_pid"] != (
                os.getppid() if parent_pid is None else parent_pid)):
        raise UnsafeTarget("parent capability does not match selected request")
    journal_start = payload["journal_start_sha256"]
    if (not isinstance(journal_start, str) or len(journal_start) != 64
            or journal_start == ZERO_SHA
            or any(c not in "0123456789abcdef" for c in journal_start)):
        raise UnsafeTarget("parent-owned journal receipt not authenticated")


def isolated_worker(url: str, hosts: tuple[str, ...], seconds: float,
                    expected_sha: str, expected_fingerprint: str,
                    journal_start: str) -> dict:
    """Run one URL in a child whose entire lifecycle is guarded by the parent."""
    _raise_if_cancelled()
    args = [sys.executable, "-I", str(Path(__file__).resolve()),
            "--_worker", "--network-opt-in", "--timeout", str(seconds),
            "--_expected-sha", expected_sha,
            "--_expected-fingerprint", expected_fingerprint,
            "--url", url]
    for host in hosts:
        args += ["--host", host]
    environment = {"PYTHONDONTWRITEBYTECODE": "1"}
    use_session = os.name == "posix"
    deadline = time.monotonic() + seconds
    process = None
    previous_mask = None
    output = None
    read_fd = None
    write_fd = None
    try:
        if not use_session:
            raise UnsafeTarget("live worker parent channel requires POSIX")
        if use_session:
            if not (hasattr(signal, "pthread_sigmask") and
                    hasattr(os, "waitid") and hasattr(os, "WNOWAIT")):
                raise UnsafeTarget("safe POSIX process supervision is unavailable")
            # Ignored SIGCHLD auto-reaps the session leader and releases its
            # PID/PGID before our anchored killpg() cleanup can run.
            if signal.getsignal(signal.SIGCHLD) == signal.SIG_IGN:
                raise UnsafeTarget("SIGCHLD ignored: safe worker supervision unavailable")
            # Block both cancellation signals before handing responsibility
            # for the new session's lifetime to this guarding try/finally.
            previous_mask = signal.pthread_sigmask(
                signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGINT})
        # The parent is invoked only inside RealJournal, after its start
        # receipt was fsynced. Give the worker a private anonymous pipe
        # instead of treating hidden CLI flags as authorization.
        capability = _parent_capability(
            url, hosts, expected_sha, expected_fingerprint, journal_start)
        read_fd, write_fd = os.pipe()
        args.extend(["--_parent-fd", str(read_fd)])
        try:
            process = subprocess.Popen(
                args, cwd=ROOT, stdin=subprocess.DEVNULL, stdout=subprocess.PIPE,
                stderr=subprocess.DEVNULL, env=environment, close_fds=True,
                start_new_session=True, pass_fds=(read_fd,),
            )
        except OSError:
            return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                    "observed_at": utc_now()}
        # Keep our read end temporarily open: a fast-exiting worker cannot
        # turn a parent write into SIGPIPE. Use nonblocking writes plus the
        # single worker deadline so a non-reading child cannot hang the parent.
        os.set_blocking(write_fd, False)
        pending = memoryview(capability)
        while pending:
            _raise_if_cancelled()
            remaining = deadline - time.monotonic()
            if remaining <= 0:
                return {"outcome": "TIMEOUT", "status": None, "url": url,
                        "observed_at": utc_now()}
            try:
                written = os.write(write_fd, pending)
            except BlockingIOError:
                time.sleep(min(0.01, remaining))
                continue
            if written <= 0:
                raise OSError("parent worker capability write failed")
            pending = pending[written:]
        os.close(write_fd)
        write_fd = None
        os.close(read_fd)
        read_fd = None
        if previous_mask is not None:
            signal.pthread_sigmask(signal.SIG_SETMASK, previous_mask)
            previous_mask = None
        _raise_if_cancelled()
        if use_session:
            output = _read_unreaped_posix(process, deadline)
        else:
            while True:
                _raise_if_cancelled()
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    break
                try:
                    stdout, _ = process.communicate(timeout=min(0.1, remaining))
                except subprocess.TimeoutExpired:
                    continue
                output = stdout
                break
    finally:
        # Closing the capability pipe cannot be postponed until after wait:
        # the child might otherwise remain blocked on its parent handshake.
        for descriptor in (read_fd, write_fd):
            if descriptor is not None:
                os.close(descriptor)
        cleanup_mask = None
        if use_session and hasattr(signal, "pthread_sigmask"):
            cleanup_mask = signal.pthread_sigmask(
                signal.SIG_BLOCK, {signal.SIGTERM, signal.SIGINT})
        try:
            if process is not None:
                try:
                    if use_session:
                        # The leader has NOT been reaped: its PID/PGID cannot
                        # be reused to target an unrelated process group.
                        os.killpg(process.pid, signal.SIGKILL)
                    elif process.poll() is None:
                        process.kill()
                except ProcessLookupError:
                    pass
                finally:
                    if process.stdout is not None:
                        process.stdout.close()
                    # Reap direct leader only AFTER group termination.
                    process.wait()
        finally:
            if cleanup_mask is not None:
                signal.pthread_sigmask(
                    signal.SIG_SETMASK,
                    previous_mask if previous_mask is not None else cleanup_mask)
    _raise_if_cancelled()
    if output is None:
        return {"outcome": "TIMEOUT", "status": None, "url": url,
                "observed_at": utc_now()}
    if process.returncode != 0 or len(output) > MAX_CHILD_OUTPUT:
        return {"outcome": "WORKER_ERROR", "status": None, "url": url,
                "observed_at": utc_now()}
    try:
        result = json.loads(output)
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

    # Informational responses are not final responses; the last block must
    # determine the actual HTTP status without fetching any body.
    hints = FakeVerifiedTLS(
        b"HTTP/1.1 103 Early Hints\r\nLink: </a>\r\n\r\n"
        b"HTTP/1.1 404 Not Found\r\n\r\nEXTRA")
    with patch.object(socket, "socket", return_value=FakeRaw()), \
            patch.object(ssl, "create_default_context",
                         return_value=FakeContext(hints)), \
            patch(__name__ + ".checked_budget", return_value=2):
        final_status, _ = exchange(target, "8.8.8.8", "HEAD", 100)
    assert final_status == 404 and hints.data == b"EXTRA"
    for response in (
        b"HTTP/1.1 101 Switching Protocols\r\n\r\n",
        b"HTTP/1.1 103 Early Hints\r\n\r\n" * (MAX_INFORMATIONAL + 1)
        + b"HTTP/1.1 200 OK\r\n\r\n",
    ):
        with patch.object(socket, "socket", return_value=FakeRaw()), \
                patch.object(ssl, "create_default_context",
                             return_value=FakeContext(FakeVerifiedTLS(response))), \
                patch(__name__ + ".checked_budget", return_value=2):
            try:
                exchange(target, "8.8.8.8", "HEAD", 100)
            except UnsafeTarget:
                negative += 1
            else:
                raise AssertionError("invalid HTTP informational chain accepted")

    # The hidden --_worker flag is not sufficient to authorize networking.
    # It must fail before Git/DNS/socket access without an inherited parent FD.
    naked_worker = subprocess.run(
        [sys.executable, "-I", str(Path(__file__).resolve()),
         "--network-opt-in", "--_worker", "--url", "https://example.org/a",
         "--host", "example.org", "--timeout", "1",
         "--_expected-sha", "a" * 40,
         "--_expected-fingerprint", "b" * 64],
        cwd=ROOT, env={"PYTHONDONTWRITEBYTECODE": "1"}, check=False,
        capture_output=True, timeout=5,
    )
    assert naked_worker.returncode != 0
    assert b"internal worker requires parent-owned pipe" in naked_worker.stderr
    negative += 1

    # Positive inherited-pipe admission is supported only on POSIX. The
    # offline Static suite must remain operational on Windows as well.
    if os.name == "posix":
        # A private pipe binds URL/host/commit to the parent journal receipt.
        # No live worker or network is started by these fixture cases.
        for approved in (True, False):
            read_fd, write_fd = os.pipe()
            try:
                raw = _parent_capability(
                    "https://example.org/a", ("example.org",),
                    "a" * 40, "b" * 64, "c" * 64)
                os.write(write_fd, raw)
            finally:
                os.close(write_fd)
            if approved:
                verify_parent_capability(
                    read_fd, "https://example.org/a", ("example.org",),
                    "a" * 40, "b" * 64, parent_pid=os.getpid())
            else:
                try:
                    verify_parent_capability(
                        read_fd, "https://example.org/unauthorized",
                        ("example.org",), "a" * 40, "b" * 64,
                        parent_pid=os.getpid())
                except UnsafeTarget:
                    negative += 1
                else:
                    raise AssertionError("mismatched parent capability accepted")
        negative += 1
    else:
        # Non-POSIX live supervision is deliberately fail-closed; offline
        # self-tests should verify denial rather than attempt POSIX admission.
        for descriptor in (-1, 3):
            try:
                verify_parent_capability(
                    descriptor, "https://example.org/a", ("example.org",),
                    "a" * 40, "b" * 64, parent_pid=os.getpid())
            except UnsafeTarget:
                negative += 1
            else:
                raise AssertionError("non-POSIX parent admission was accepted")

    # Test signals during spawn, communicate, and the FIRST cleanup line.
    # Handlers must never throw asynchronously: cancellation is checked
    # synchronously after the supervised child has been killed and reaped.
    class FakeWaitingWorker:
        pid = 789123
        returncode = None
        stdout = None

        def __init__(self, interrupt_during_communicate=()):
            self.interrupt_during_communicate = tuple(
                interrupt_during_communicate)
            self.killed = False
            self.waited = False

        def communicate(self, timeout):
            assert timeout > 0
            signals = self.interrupt_during_communicate
            self.interrupt_during_communicate = ()
            for signum in signals:
                os.kill(os.getpid(), signum)
            raise subprocess.TimeoutExpired("offline-fixture", timeout)

        def poll(self):
            return None

        def kill(self):
            self.killed = True

        def wait(self):
            self.waited = True

    if os.name == "posix":
        original_mask = signal.pthread_sigmask
        initial_mask = original_mask(signal.SIG_BLOCK, set())

        def verify_signal_cleanup(spawn_signals=(), wait_signals=(),
                                  cleanup_signals=()):
            """Reproduce signal delivery at three distinct lifecycle stages."""
            global _cancellation_signal
            _cancellation_signal = None
            child = FakeWaitingWorker(wait_signals)
            blocked = [0]
            previous_term = signal.signal(signal.SIGTERM, abort_on_sigterm)
            previous_int = signal.signal(signal.SIGINT, abort_on_sigint)

            def inject_in_spawn(*_args, **_kwargs):
                mask = original_mask(signal.SIG_BLOCK, set())
                assert signal.SIGTERM in mask and signal.SIGINT in mask
                for signum in spawn_signals:
                    os.kill(os.getpid(), signum)
                return child

            def inject_before_cleanup_mask(how, signals):
                if (how == signal.SIG_BLOCK and
                        {signal.SIGTERM, signal.SIGINT}.issubset(signals)):
                    blocked[0] += 1
                    if blocked[0] == 2:
                        # The initial cancellation may occur here AFTER a
                        # plain timeout, before cleanup has masked signals.
                        for signum in cleanup_signals:
                            os.kill(os.getpid(), signum)
                return original_mask(how, signals)

            def fake_killpg(pid, signum):
                assert pid == child.pid and signum == signal.SIGKILL
                child.killed = True

            def fake_nonreaping_reader(worker, _deadline):
                try:
                    worker.communicate(timeout=0.001)
                except subprocess.TimeoutExpired:
                    return None
                raise AssertionError("offline signal fixture must stay pending")

            try:
                with patch.object(subprocess, "Popen",
                                  side_effect=inject_in_spawn), \
                        patch(__name__ + "._read_unreaped_posix",
                              side_effect=fake_nonreaping_reader), \
                        patch.object(os, "killpg", side_effect=fake_killpg), \
                        patch.object(signal, "pthread_sigmask",
                                     side_effect=inject_before_cleanup_mask):
                    try:
                        # A short local fixture deadline; never a socket.
                        isolated_worker("https://example.org/a",
                                        ("example.org",), 0.02,
                                        "a" * 40, "b" * 64, "c" * 64)
                    except (SystemExit, KeyboardInterrupt):
                        if not (spawn_signals or wait_signals or cleanup_signals):
                            raise AssertionError("unexpected cancellation")
                    else:
                        if spawn_signals or wait_signals or cleanup_signals:
                            raise AssertionError("worker cancellation was ignored")
                assert blocked[0] == 2
                assert child.killed and child.waited
                assert original_mask(signal.SIG_BLOCK, set()) == initial_mask
            finally:
                signal.signal(signal.SIGTERM, previous_term)
                signal.signal(signal.SIGINT, previous_int)
                _cancellation_signal = None

        for spawn, waiting, cleaning in (
            ((), (signal.SIGTERM,), ()),
            ((), (signal.SIGINT,), ()),
            ((signal.SIGTERM,), (), ()),
            ((signal.SIGINT,), (), ()),
            ((), (), (signal.SIGTERM,)),
            ((), (), (signal.SIGINT,)),
            ((), (signal.SIGTERM,), (signal.SIGINT,)),
            ((), (signal.SIGINT,), (signal.SIGTERM,)),
            ((), (signal.SIGTERM,), (signal.SIGTERM,)),
            ((), (signal.SIGINT,), (signal.SIGINT,)),
        ):
            verify_signal_cleanup(spawn, waiting, cleaning)
            negative += 1

    # SIGCHLD=SIG_IGN automatically reaps a departed leader on POSIX.
    # Refuse the configuration BEFORE launching a worker: the PID/PGID
    # otherwise becomes reusable before the group SIGKILL.
    if os.name == "posix":
        previous_sigchld = signal.getsignal(signal.SIGCHLD)
        try:
            signal.signal(signal.SIGCHLD, signal.SIG_IGN)
            with patch.object(subprocess, "Popen",
                              side_effect=AssertionError(
                                  "worker spawned with SIGCHLD ignored")):
                try:
                    isolated_worker("https://example.org/a",
                                    ("example.org",), 1.0,
                                    "a" * 40, "b" * 64, "c" * 64)
                except UnsafeTarget:
                    negative += 1
                else:
                    raise AssertionError("ignored SIGCHLD was accepted")
        finally:
            signal.signal(signal.SIGCHLD, previous_sigchld)

    # A fast worker with no descendants closes stdout before cleanup. Even
    # then the supervisor must keep its zombie PID reserved until killpg().
    if os.name == "posix" and hasattr(os, "WNOWAIT"):
        response = {
            "url": "https://example.org/a", "outcome": "REACHABLE",
            "checkout_sha": "a" * 40, "fingerprint_sha256": "b" * 64,
            "observed_at": utc_now(),
        }
        child_program = ("import sys; sys.stdout.write("
                         + repr(json.dumps(response)) + " + '\\n')")
        real_popen = subprocess.Popen
        real_killpg = os.killpg
        saw_unreaped = []

        def spawn_fast_child(_arguments, **kwargs):
            assert kwargs["start_new_session"] is True
            return real_popen([sys.executable, "-I", "-c", child_program],
                              **kwargs)

        def ensure_group_identity(group_id, sig):
            # WNOWAIT verifies the exited leader has NOT been reaped yet.
            status = os.waitid(
                os.P_PID, group_id,
                os.WEXITED | os.WNOHANG | os.WNOWAIT)
            assert status is not None
            saw_unreaped.append(group_id)
            return real_killpg(group_id, sig)

        with patch.object(subprocess, "Popen",
                          side_effect=spawn_fast_child), \
                patch.object(os, "killpg",
                             side_effect=ensure_group_identity):
            outcome = isolated_worker(
                "https://example.org/a", ("example.org",), 2.0,
                "a" * 40, "b" * 64, "c" * 64)
        assert outcome["outcome"] == "REACHABLE" and saw_unreaped
        negative += 1

    # Regress the real POSIX process-group orphan: the worker leader exits
    # successfully, but its background descendant retains the stdout pipe.
    # communicate() times out with poll() == 0; cleanup must STILL killpg().
    if (os.name == "posix" and Path("/bin/sh").is_file()
            and Path("/bin/sleep").is_file()):
        with tempfile.TemporaryDirectory(prefix="p012-descendant-") as folder:
            child_pid = Path(folder) / "descendant.pid"
            heartbeat = Path(folder) / "heartbeat"
            shell_fixture = (
                '(while :; do printf x >> "$2"; /bin/sleep 0.05; done) & '
                'printf "%s\n" "$!" > "$1"; exit 0'
            )
            actual_popen = subprocess.Popen
            launched = [None]

            def spawn_exiting_leader(_args, **kwargs):
                assert kwargs["start_new_session"] is True
                leader = actual_popen(
                    ["/bin/sh", "-c", shell_fixture, "offline-fixture",
                     str(child_pid), str(heartbeat)], **kwargs)
                launched[0] = leader
                return leader

            try:
                with patch.object(subprocess, "Popen",
                                  side_effect=spawn_exiting_leader):
                    outcome = isolated_worker(
                        "https://example.org/a", ("example.org",), 1.0,
                        "a" * 40, "b" * 64, "c" * 64)
                assert outcome["outcome"] == "TIMEOUT"
                assert launched[0] is not None
                assert launched[0].returncode == 0
                assert child_pid.is_file() and heartbeat.is_file()
                descendant_pid = int(child_pid.read_text().strip())
                assert descendant_pid != launched[0].pid
                ticks = heartbeat.read_bytes()
                assert len(ticks) > 0
                # A still-running descendant keeps writing the heartbeat.
                time.sleep(0.2)
                assert heartbeat.read_bytes() == ticks, (
                    "a descendant survived after its leader exited")
                negative += 1
            finally:
                # The normal supervisor already kills the group and reaps the
                # leader; its PID may now belong to an unrelated group.
                # Signal only if the DIRECT child is still unreaped, which
                # pins the PID/PGID until the emergency killpg() completes.
                leader = launched[0]
                if leader is not None and leader.returncode is None:
                    try:
                        os.waitid(os.P_PID, leader.pid,
                                  os.WEXITED | os.WNOHANG | os.WNOWAIT)
                    except ChildProcessError:
                        # Already reaped: never signal this reusable PGID.
                        pass
                    else:
                        try:
                            os.killpg(leader.pid, signal.SIGKILL)
                        except ProcessLookupError:
                            pass
                        leader.wait()

    sample = {"schema": 1, "checkout_sha": "a" * 40,
              "fingerprint_sha256": "b" * 64, "unique_urls": 1,
              "links": [{"url": "https://example.org/a",
                         "references": [{"file": "a.md", "line": 1}]}]}
    url = "https://example.org/a"
    # Git skip-worktree can hide edited Markdown from status; inventory must
    # be derived from immutable HEAD objects, not this modified worktree.
    with tempfile.TemporaryDirectory(prefix="p012-git-source-") as folder:
        gitroot = Path(folder)
        subprocess.run(["git", "init", "-q"], cwd=gitroot, check=True)
        document = gitroot / "a.md"
        document.write_text("[old](https://example.org/original)\n",
                            encoding="utf-8")
        subprocess.run(["git", "add", "a.md"], cwd=gitroot, check=True)
        subprocess.run(["git", "-c", "user.name=Fixture",
                        "-c", "user.email=fixture@example.invalid",
                        "-c", "commit.gpgsign=false", "commit", "-q",
                        "-m", "source fixture"], cwd=gitroot, check=True)
        subprocess.run(["git", "update-index", "--skip-worktree", "a.md"],
                       cwd=gitroot, check=True)
        document.write_text("[changed](https://example.org/forged)\n",
                            encoding="utf-8")
        assert not subprocess.check_output(
            ["git", "status", "--porcelain=v1", "-z"], cwd=gitroot)
        original = trusted_source_inventory(gitroot)
        choose_inventory_url(original, "https://example.org/original",
                             frozenset({"example.org"}))
        try:
            choose_inventory_url(original, "https://example.org/forged",
                                 frozenset({"example.org"}))
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("skip-worktree mutated link spoofed Git HEAD")
        # Git replace refs can also rewrite a blob without changing HEAD SHA.
        old_blob = subprocess.check_output(
            ["git", "--no-replace-objects", "rev-parse", "HEAD:a.md"],
            cwd=gitroot, text=True).strip()
        replacement_blob = subprocess.check_output(
            ["git", "hash-object", "-w", "--stdin"], cwd=gitroot,
            input=b"[replaced](https://example.org/replaced)\n",
        ).decode("ascii").strip()
        subprocess.run(["git", "replace", old_blob, replacement_blob],
                       cwd=gitroot, check=True)
        unprotected = subprocess.check_output(
            ["git", "show", "HEAD:a.md"], cwd=gitroot)
        assert b"https://example.org/replaced" in unprotected

        # Verify every identity-establishing Git read explicitly forbids
        # promisor lazy-fetch, without contacting a remote in this fixture.
        original_check_output = subprocess.check_output
        checked_git_reads = [0]
        def guarded_git_read(args, **kwargs):
            if (isinstance(args, list) and len(args) > 1
                    and args[:2] == ["git", "--no-replace-objects"]):
                assert kwargs["env"]["GIT_NO_LAZY_FETCH"] == "1"
                assert kwargs["env"]["GIT_TERMINAL_PROMPT"] == "0"
                checked_git_reads[0] += 1
            return original_check_output(args, **kwargs)
        with patch.object(subprocess, "check_output",
                          side_effect=guarded_git_read):
            protected = trusted_source_inventory(gitroot)
        assert checked_git_reads[0] >= 3
        choose_inventory_url(protected, "https://example.org/original",
                             frozenset({"example.org"}))
        try:
            choose_inventory_url(protected, "https://example.org/replaced",
                                 frozenset({"example.org"}))
        except UnsafeTarget:
            negative += 1
        else:
            raise AssertionError("Git replace ref spoofed the original HEAD")
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
    parser.add_argument("--_parent-fd", type=int, help=argparse.SUPPRESS)
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

    # Authenticate the internal child branch BEFORE any Git inventory,
    # DNS, TLS or HTTP operation. Hiding an argparse flag is not a guard.
    if args._worker:
        if args._parent_fd is None:
            parser.error("internal worker requires parent-owned pipe capability")
        try:
            verify_parent_capability(
                args._parent_fd, args.url[0] if len(args.url) == 1 else "",
                tuple(sorted(args.host)), args._expected_sha,
                args._expected_fingerprint)
        except UnsafeTarget as error:
            parser.error(str(error))
    elif args._parent_fd is not None:
        parser.error("parent descriptor allowed only for internal worker")

    if (not math.isfinite(args.timeout) or not 1 <= args.timeout <= 30
            or not args.host or not args.url or len(args.url) > MAX_SELECTED
            or len(args.host) > 16
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
        if os.name == "posix" and hasattr(signal, "pthread_sigmask"):
            # The parent intentionally masks SIGTERM/SIGINT during creation.
            signal.pthread_sigmask(signal.SIG_UNBLOCK,
                                   {signal.SIGTERM, signal.SIGINT})
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
    global _cancellation_signal
    _cancellation_signal = None
    previous_term = signal.getsignal(signal.SIGTERM)
    previous_int = signal.getsignal(signal.SIGINT)
    signal.signal(signal.SIGTERM, abort_on_sigterm)
    signal.signal(signal.SIGINT, abort_on_sigint)
    try:
        with RealJournal(args.journal, source, tuple(args.url)) as journal:
            for url in args.url:
                _raise_if_cancelled()
                result = isolated_worker(
                    url, tuple(sorted(allowed)), args.timeout,
                    source["checkout_sha"], source["fingerprint_sha256"],
                    journal.previous)
                _raise_if_cancelled()
                journal.result(result)
            _raise_if_cancelled()
            journal.finish()
    finally:
        signal.signal(signal.SIGTERM, previous_term)
        signal.signal(signal.SIGINT, previous_int)
    print("P012-LIVE-HTTPS-PROBE status=COMPLETE"
          f" urls={len(args.url)} journal={args.journal}"
          " source_bound=RECOMPUTED_FROM_CLEAN_GIT_CHECKOUT"
          " release_authorization=NONE")


if __name__ == "__main__":
    main()
