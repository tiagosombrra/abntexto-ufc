# P0.12 / #612 — pinned HTTPS routing contract (fake-only)

**Status:** development-only isolated implementation slice. Source main after PR #616 was `26e4839fa3b1ad5abd2bfa474b820317decefcda`. Published version v3.0.5 unchanged; v3.1.0 UNRELEASED and publication_authorized=false.

## Delivered and deliberately excluded

`tests/checks/repository/p012_pinned_tls_contract.py` defines a **pure offline contract** for URL authorization, all-address DNS vetting, pinned numeric destination identity, TLS SNI/peer certificate hostname, HTTP Host identity, no proxy path, bounded HTTP/1 headers **with the first CRLF-CRLF terminator required at the very end of the simulated header block (no body bytes parsed as headers) and a printable-ASCII status reason phrase (no control, DEL, TAB or non-ASCII bytes)**, conservative HEAD status mapping, same logical deadline and redirected-host DNS revalidation. Its resolver and connector are **simulated functions supplied by local tests**, not real operating-system services.

The contract may refuse inconsistent simulated evidence, but **the evidence fields are not authenticated by an actual TLS handshake**. A hostile real adapter could forge them. Treat `HopProof` as a test assertion mechanism, never production security evidence. This code contains no socket, DNS resolver, SSL context, HTTP client, worker launcher or command-line option to use a network.

The unit fixture verifies a normal HEAD 200, redirects to a second host (separate fake DNS approval and connection), rejects mixed public/private answers, direct peer IP mismatches, forged Host/SNI/certificate identity, proxy-use signals, a body consumed on HEAD, oversized/duplicate Location headers, malformed HTTP response headers, redirect cycles, unapproved hosts and expired deadlines. It distinguishes 401/403, 404, 410, 429 and HEAD unsupported. All tests run in Static with `network=0`.

## Required future **separate** implementation and security acceptance

- Explicit user network opt-in and an allowlist of **exact hosts** selected from an inventory authenticated to a trusted checkout, not merely SHA/fingerprint strings in a caller-provided JSON.
- Dedicated **killable worker process per URL** with parent-enforced monotonic deadline encompassing DNS, TCP, TLS, HEAD, redirect hops and limited GET fallback. No unrestricted subprocess, shell or environment-proxy inheritance.
- Real IP-resolving step: inspect **every** DNS answer, rejecting private, reserved, link-local, site-local, scoped, multicast and metadata addresses; actual TCP socket must connect by the selected numeric IP and verify actual peer IP. Re-check each retry and redirect from scratch.
- HTTPS context with certificate verification, hostname validation, exact SNI and HTTP Host bound to the original approved DNS hostname; explicitly HTTP/1.1 or a separately audited HTTP/2 client. No proxy delegation of DNS or TLS and network egress guardrails outside the process.
- Bound header sizes, stream bytes, number of redirects and total runtime. Never consume arbitrarily large redirect bodies; distinguish HTTP 401/403 from broken links. Implement and test a bounded GET fallback where HEAD truly unsupported.
- Real per-URL incremental, authenticated-source (not signed) receipts, using distinct `REAL_HTTP` vocabulary and schema, not the `SIMULATED_*` journal from PR #616. Preserve partial observations through timeouts and cancellation.
- Independent security review on the **exact** final SHA, adversarial fake-socket tests and controlled ephemeral egress integration. No network requests from default Static/CI or module import. No production use or merge of a live implementation until these gates pass.

**Gate boundaries:** `P0.12_ROUTE_CONTRACT=FAKE_ONLY`; `P0.12_LIVE_HTTP=NOT_IMPLEMENTED`; `SSRF_END_TO_END_CERTIFIED=NO`; `P0.12_GLOBAL=IN_PROGRESS`; `v3.1.0=UNRELEASED`.

Related: [#612](https://github.com/tiagosombrra/abntexto-ufc/issues/612), [#615](https://github.com/tiagosombrra/abntexto-ufc/pull/615), [#616](https://github.com/tiagosombrra/abntexto-ufc/pull/616).
