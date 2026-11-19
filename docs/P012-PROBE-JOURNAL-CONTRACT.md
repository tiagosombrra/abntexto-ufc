# P0.12 / #612 — durable offline evidence and killable test worker

**Lifecycle:** v3.1.0 UNRELEASED and publication_authorized=false. This is the second isolated P0.12 implementation slice; #615 supplied the URL/IP/redirect preflight. **No HTTP transport, DNS resolution, proxy, or outbound socket is present in this slice.** This change cannot establish end-to-end SSRF safety.

## Scope

The implementation is tests/checks/repository/p012_probe_journal.py with tests/static.py registration. It reuses receipt_urls() from the previously merged p012_probe_security_policy.py, so only URLs that appear in a schema-1 source-bound inventory may enter a journal. The inventory's claimed SHA and fingerprint remain **unauthenticated** by this module: a future network probe must independently recompute or authenticate the complete inventory at the expected checkout before trusting either field.

The journal uses exclusive creation (O_EXCL) of a private regular file, a bounded ASCII-escaped JSONL format, UTC timestamps, a sequence number, **a SHA-256 checksum inside every complete record including the final one**, SHA-256 chaining across records, fsync after every record and a POSIX fsync of the containing directory at journal creation. On Windows, process-level synchronization is performed but directory-entry persistence after a machine power loss is **not certified**. Outcomes are strictly simulation-only. The chain detects accidental corruption but is **not a signature or adversarial integrity proof**. No HTTP response bodies, credentials, or environment variables are recorded.

An incomplete run remains PARTIAL, with intact previously synchronized URL results. A torn final record reports TRUNCATED_TAIL, rather than concealing that evidence was interrupted. A changed complete record, **including the final result of an interrupted run**, or invalid event chain raises an error. The writer refuses overwrite, duplicate URL results, URL substitutions and premature completion.

The supervisor executes **only the same local fixture script** using a direct subprocess with no shell, stdin/stdout/stderr bound to DEVNULL and a time budget. A stalled child is terminated (POSIX process group or direct process on other systems). Tests cover local worker success, failure, timeout, kill and journal recovery. This supervisor is a *fixture*, not yet a remote-probe subprocess, and does not demonstrate termination of arbitrary process descendants on Windows. Future production code must isolate network workers with a platform-appropriate process-tree guarantee.

## Static evidence and important limits

The command python3 tests/checks/repository/p012_probe_journal.py --self-test performs only filesystem operations inside a temporary test directory and launches local non-network fixtures. It must emit P012-PROBE-JOURNAL-EVIDENCE status=PASS, network=0, dns=NOT_EXECUTED, http=NOT_IMPLEMENTED, recovery=PARTIAL and worker_timeout=KILLED. It cannot claim any external link as REACHABLE or broken.

A future, separate explicitly opt-in network PR remains required for actual TCP pinning of vetted public IPs, hostname-correct TLS SNI/certificate/Host, proxy isolation, DNS and request deadlines, redirect revalidation, bounded headers/body, trusted checkout/receipt provenance, incremental **real** status receipts and protected no-network unit/fake-socket tests. Demand independent security review and a controlled egress integration environment. Until then P0.12_HTTP_PROBE=NOT_IMPLEMENTED, SSRF_END_TO_END_CERTIFIED=NO, P0.12_GLOBAL=IN_PROGRESS.

**Release lock:** v3.0.5 is the last immutable public GitHub/CTAN release. v3.1.0 is UNRELEASED; no tag, release or CTAN upload is approved. Review of ABNT 6034:2026 and final seven-profile human PDFs is independent of this technical slice.

Related: [issue #612](https://github.com/tiagosombrra/abntexto-ufc/issues/612), [PR #615](https://github.com/tiagosombrra/abntexto-ufc/pull/615), [issue #489](https://github.com/tiagosombrra/abntexto-ufc/issues/489).
