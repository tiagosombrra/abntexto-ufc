#!/usr/bin/env python3
"""Offline-only durable journal and killable fixture worker for P0.12.

This module deliberately contains no DNS, TLS, socket or HTTP transport.
Its worker executes only this file's fixed local fixtures. Never interpret
simulated outcomes as live link reachability.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import signal
import stat
import subprocess
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

from p012_probe_security_policy import UnsafeTarget, receipt_urls

SCHEMA = 1
MAX_RECORD_BYTES = 16384
SIMULATIONS = frozenset({"SIMULATED_OK", "SIMULATED_TIMEOUT", "SIMULATED_UNSAFE"})
ZERO_SHA = "0" * 64


def observed_at() -> str:
    """Use a UTC timestamp, not a hypothetical network observation."""
    return datetime.now(timezone.utc).isoformat()


def _encode(entry: dict) -> bytes:
    data = json.dumps(entry, sort_keys=True, ensure_ascii=True,
                      separators=(",", ":"), allow_nan=False).encode("ascii") + b"\n"
    if len(data) > MAX_RECORD_BYTES:
        raise UnsafeTarget("journal record exceeds the bounded byte limit")
    return data


def _safe_fd(path: Path) -> int:
    """Create a new private receipt, refusing overwrite and symbolic links."""
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    fd = os.open(path, flags, 0o600)
    mode = os.fstat(fd)
    if not stat.S_ISREG(mode.st_mode) or mode.st_nlink != 1:
        os.close(fd)
        raise UnsafeTarget("journal path must be a private regular file")
    return fd


class Journal:
    """Append source-bound simulated results with a hash chain and fsync."""

    def __init__(self, path: Path, inventory: dict, selected: tuple[str, ...]):
        known_urls = receipt_urls(inventory)
        if not selected or len(selected) != len(set(selected)):
            raise UnsafeTarget("selection must be nonempty and unique")
        if not set(selected).issubset(known_urls):
            raise UnsafeTarget("selection includes a URL not in the inventory")
        self.path = path
        self.selected = tuple(sorted(selected))
        self.completed: set[str] = set()
        self.sequence = 0
        self.previous = ZERO_SHA
        self.closed = False
        self.fd = _safe_fd(path)
        try:
            self._append({
                "kind": "start", "schema": SCHEMA, "mode": "SIMULATED_ONLY",
                "checkout_sha": inventory["checkout_sha"],
                "fingerprint_sha256": inventory["fingerprint_sha256"],
                "selected_urls": self.selected,
                "started_at": observed_at(),
            })
        except BaseException:
            os.close(self.fd)
            self.closed = True
            raise

    def _append(self, record: dict) -> None:
        if self.closed:
            raise UnsafeTarget("journal is closed")
        payload = {**record, "sequence": self.sequence, "previous_sha256": self.previous}
        data = _encode(payload)
        remaining = memoryview(data)
        while remaining:
            written = os.write(self.fd, remaining)
            if written <= 0:
                raise OSError("journal write made no progress")
            remaining = remaining[written:]
        os.fsync(self.fd)
        self.previous = hashlib.sha256(data).hexdigest()
        self.sequence += 1

    def record(self, url: str, simulated_outcome: str) -> None:
        """Persist one outcome before advancing to another URL."""
        if url not in self.selected or url in self.completed:
            raise UnsafeTarget("result URL absent or already recorded")
        if simulated_outcome not in SIMULATIONS:
            raise UnsafeTarget("only explicit simulated outcomes are allowed")
        self._append({
            "kind": "result", "url": url, "outcome": simulated_outcome,
            "observed_at": observed_at(), "network": "NOT_EXECUTED",
        })
        self.completed.add(url)

    def finish(self) -> None:
        if self.completed != set(self.selected):
            raise UnsafeTarget("cannot finish while some URLs are unrecorded")
        self._append({"kind": "finish", "completed": len(self.completed),
                      "result": "SIMULATED_COMPLETE", "finished_at": observed_at()})
        self.close()

    def close(self) -> None:
        if not self.closed:
            os.close(self.fd)
            self.closed = True

    def __enter__(self) -> Journal:
        return self

    def __exit__(self, *_exc: object) -> None:
        self.close()


def inspect(path: Path) -> dict:
    """Recover intact records and explicitly flag a torn final JSONL line.

    A hash chain detects accidental mutation; it is NOT a cryptographic
    authentication of attacker-controlled evidence.
    """
    entries: list[dict] = []
    previous = ZERO_SHA
    torn = False
    with path.open("rb") as handle:
        while True:
            data = handle.readline(MAX_RECORD_BYTES + 1)
            if not data:
                break
            if len(data) > MAX_RECORD_BYTES:
                raise UnsafeTarget("oversized journal record")
            if not data.endswith(b"\n"):
                torn = True
                break
            try:
                record = json.loads(data)
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise UnsafeTarget("corrupt complete journal record") from error
            if not isinstance(record, dict):
                raise UnsafeTarget("journal record is not an object")
            if (record.get("sequence") != len(entries)
                    or record.get("previous_sha256") != previous):
                raise UnsafeTarget("journal chain mismatch")
            previous = hashlib.sha256(data).hexdigest()
            entries.append(record)
    if not entries or entries[0].get("kind") != "start":
        raise UnsafeTarget("journal has no valid start record")
    first = entries[0]
    if first.get("schema") != SCHEMA or first.get("mode") != "SIMULATED_ONLY":
        raise UnsafeTarget("unknown journal schema or evidence mode")
    selected = first.get("selected_urls")
    if (not isinstance(selected, list) or not selected
            or selected != sorted(set(selected))):
        raise UnsafeTarget("invalid journal selection")
    completed: set[str] = set()
    finished = False
    for entry in entries[1:]:
        if finished:
            raise UnsafeTarget("entries after journal finish")
        if entry.get("kind") == "result":
            url = entry.get("url")
            if (url not in selected or url in completed
                    or entry.get("outcome") not in SIMULATIONS
                    or entry.get("network") != "NOT_EXECUTED"):
                raise UnsafeTarget("unrecognized or duplicated simulated result")
            completed.add(url)
        elif entry.get("kind") == "finish":
            if (completed != set(selected) or entry.get("completed") != len(completed)
                    or entry.get("result") != "SIMULATED_COMPLETE"):
                raise UnsafeTarget("journal finish does not match recorded URLs")
            finished = True
        else:
            raise UnsafeTarget("unknown journal event type")
    if finished and torn:
        raise UnsafeTarget("journal has trailing data after finish")
    return {
        "state": "SIMULATED_COMPLETE" if finished else "PARTIAL",
        "integrity": "TRUNCATED_TAIL" if torn else "CHAIN_OK",
        "source_sha": first["checkout_sha"],
        "fingerprint_sha256": first["fingerprint_sha256"],
        "selected": len(selected),
        "recorded": len(completed),
        "missing": len(selected) - len(completed),
    }


def fixture_worker(kind: str, deadline_seconds: float) -> str:
    """Kill a fixed local fixture process when its single budget expires."""
    if kind not in {"pass", "fail", "sleep"}:
        raise UnsafeTarget("non-fixture worker forbidden")
    if not 0.05 <= deadline_seconds <= 5:
        raise UnsafeTarget("fixture timeout outside test bounds")
    args = [sys.executable, "-I", str(Path(__file__).resolve()),
            "--_fixture", kind]
    use_group = os.name == "posix"
    process = subprocess.Popen(
        args, stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL,
        stderr=subprocess.DEVNULL, close_fds=True,
        start_new_session=use_group,
    )
    try:
        process.wait(timeout=deadline_seconds)
    except subprocess.TimeoutExpired:
        if use_group:
            os.killpg(process.pid, signal.SIGKILL)
        else:
            process.kill()
        process.wait()
        return "SIMULATED_TIMEOUT"
    return "SIMULATED_OK" if process.returncode == 0 else "SIMULATED_UNSAFE"


def selftest() -> None:
    """Exercise on-disk recovery, chain detection and actual child termination."""
    sample = {
        "schema": 1, "checkout_sha": "a" * 40,
        "fingerprint_sha256": "b" * 64, "unique_urls": 2,
        "links": [
            {"url": "https://example.org/a", "references": [{"file": "a.md", "line": 1}]},
            {"url": "https://example.org/b", "references": [{"file": "b.md", "line": 2}]},
        ],
    }
    urls = ("https://example.org/a", "https://example.org/b")
    with tempfile.TemporaryDirectory(prefix="p012-journal-") as root:
        root = Path(root)
        receipt = root / "partial.jsonl"
        with Journal(receipt, sample, urls) as journal:
            journal.record(urls[0], "SIMULATED_OK")
            partial = inspect(receipt)
            assert partial["state"] == "PARTIAL" and partial["recorded"] == 1
            assert partial["integrity"] == "CHAIN_OK"
            try:
                Journal(receipt, sample, urls)
            except FileExistsError:
                pass
            else:
                raise AssertionError("journal overwrite unexpectedly succeeded")
            try:
                journal.record(urls[0], "SIMULATED_OK")
            except UnsafeTarget:
                pass
            else:
                raise AssertionError("duplicate result unexpectedly accepted")
            journal.record(urls[1], "SIMULATED_TIMEOUT")
            journal.finish()
        completed = inspect(receipt)
        assert completed["state"] == "SIMULATED_COMPLETE" and completed["recorded"] == 2
        torn_path = root / "torn.jsonl"
        torn_path.write_bytes(receipt.read_bytes().splitlines(keepends=True)[:-1][0] +
                              b'{"kind":"result",')
        recovered = inspect(torn_path)
        assert recovered["state"] == "PARTIAL" and recovered["integrity"] == "TRUNCATED_TAIL"
        tampered_path = root / "tampered.jsonl"
        tampered_path.write_bytes(receipt.read_bytes().replace(b"SIMULATED_OK",
                                                               b"SIMULATED_NO", 1))
        try:
            inspect(tampered_path)
        except UnsafeTarget:
            pass
        else:
            raise AssertionError("hash-chained tampering unexpectedly accepted")
        other = root / "not-authorized.jsonl"
        try:
            Journal(other, sample, ("https://evil.org/",))
        except UnsafeTarget:
            pass
        else:
            raise AssertionError("URL outside inventory unexpectedly accepted")
        assert not other.exists()
        assert fixture_worker("pass", 5) == "SIMULATED_OK"
        assert fixture_worker("fail", 5) == "SIMULATED_UNSAFE"
        assert fixture_worker("sleep", 0.1) == "SIMULATED_TIMEOUT"


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--self-test", action="store_true",
                        help="Run local-only journal/worker fixtures")
    parser.add_argument("--_fixture", choices=("pass", "fail", "sleep"),
                        help=argparse.SUPPRESS)
    args = parser.parse_args()
    if args._fixture == "sleep":
        time.sleep(10)
        return
    if args._fixture == "fail":
        raise SystemExit(7)
    if args._fixture == "pass":
        return
    selftest()
    print("P012-PROBE-JOURNAL-EVIDENCE status=PASS"
          " simulated_receipts=PASS recovery=PARTIAL"
          " torn_tail=DETECTED chain_mutation=REJECTED"
          " worker_pass=PASS worker_failure=CLASSIFIED worker_timeout=KILLED"
          " source=OFFLINE_INVENTORY network=0"
          " dns=NOT_EXECUTED http=NOT_IMPLEMENTED"
          " egress_review=PENDING release_authorization=NONE")


if __name__ == "__main__":
    main()
