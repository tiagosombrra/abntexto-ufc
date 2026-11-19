# P0.12 / #612 — opt-in HTTPS transport candidate (DRAFT, NOT SECURITY-APPROVED)

**Release status:** v3.0.5 last published; v3.1.0 UNRELEASED, publication_authorized=false. This implementation is a proposed *real* HTTPS client under independent security review. It is not production-ready, has not been exercised against Internet targets, and does not certify end-to-end SSRF resistance.

## Boundary and explicit activation

Normal invocation and the Static CI registration execute only local fixtures. No DNS, socket, SSL handshake or HTTP traffic may occur unless the operator explicitly passes **all** of --network-opt-in, one or more exact --host values, one or more --url values and an absolute --journal output path. The selected URLs must occur byte-for-byte in the Markdown external-link inventory **recomputed from immutable Git tree/blob objects at the pinned HEAD, not the working tree**. This explicitly prevents skip-worktree/assume-unchanged local modifications from being falsely attributed to the original commit. The parent passes the exact checkout SHA and inventory fingerprint to each isolated worker; the worker recomputes the trusted inventory and refuses to access the network if either value differs. The parent also rejects child output with different source identifiers. The operator does not supply a trusted inventory SHA or fingerprint; the tool recomputes them. The journal is a newly created private file; it cannot overwrite an existing report. Use an output directory **outside the repository**, to prevent untracked output from invalidating a clean-checkout verification in the child worker.

Example command for a reviewed, egress-controlled environment only (illustrative, DO NOT run during normal CI):

    python3 tests/checks/repository/p012_opt_in_https_probe.py --network-opt-in --host example.org --url https://example.org/path-from-current-inventory --journal /tmp/abntexto-p012-real.jsonl --timeout 8

The hostname and URL are illustrations, not a claim that this URL exists in this repository's inventory.

## Exact network construction

- The worker checks every DNS answer with the merged public-IP policy. A single private, reserved or scoped answer rejects the entire response. The worker chooses one numeric global IP and never passes a DNS hostname into the TCP connect operation.
- Direct TCP socket to numeric IP on port 443, then compare actual getpeername() with the pinned address. Python's verified default CA-backed SSL context handshakes using the original approved hostname as TLS SNI and certificate-validation hostname. The certificate must exist, and the post-handshake peer IP must still equal the selected address.
- HTTP/1.1 HEAD request uses the original hostname in Host and only a validated path/query. No urllib, requests, proxies, custom CA environment or redirects inherited from a higher-level client. A single pinned-IP GET with Range: bytes=0-0 is used only if HEAD returns 405/501.
- The parser stops at the **first** CRLF-CRLF of each HTTP response block, follows bounded 100/102/103 informational blocks to their final status, rejects unsupported 101 upgrades, and applies **one aggregate limit of 8 KiB to all headers** and **zero application-level body bytes**. Thus an arbitrary server body, or a server ignoring Range, cannot trigger unbounded downloading. Redirect bodies are never consumed. A redirect is allowed only to an approved HTTPS host, with a new DNS vetting and IP pinning on the next hop, no more than three redirects.
- A separate process per URL can be forcibly terminated by its parent on a *single monotonic timeout* encompassing DNS, connect, TLS, HEAD, GET fallback and redirects. The POSIX parent also installs a SIGTERM handler that unwinds worker cleanup and preserves the unfinished journal as PARTIAL; termination while launching the worker and non-POSIX descendant cleanup still require independent review. Runtime disables environment inheritance for the child, closes other descriptors, uses isolated Python mode and a fixed worker entry point; the runner invokes no shell.
- Per-URL status is persisted immediately to a private REAL_HTTP schema-2 JSONL journal with per-record checksum, SHA-chain and fsync. On POSIX the containing directory is fsynced after creation. Missing finish means PARTIAL; this is not a signature or authentication against a malicious writer. Failures of one URL should not discard earlier receipts. Windows child-process descendant termination and directory-entry crash durability are not certified.

## Known hard limits / independent-review requirements

- **This is not an audited SSRF defense.** Local network egress filtering is a separate mandatory control; future adversarial validation must use a disposable egress-restricted environment and an independent reviewer for the exact final SHA.
- DNS rebinding and mixed public/private records, IPv6/mapped addresses, certificate/SNI correctness, proxies, slow DNS, handshake/header trickle, malformed redirect, HEAD-to-GET behavior, HTTP parsing, interruption, process cleanup and partial journal recovery must undergo negative tests and controlled real integration. The fake tests and static approval alone are insufficient.
- The worker currently selects the first supported approved IP, without fallback to other public A/AAAA addresses. This may yield false-negative NETWORK_ERROR; do not report this as an absent document.
- A HEAD-supported server may misbehave and report statuses different from GET; record classifications conservatively. HTTP 401/403 is ACCESS_RESTRICTED, not broken. Timeout and network errors are not evidence of missing links. No 2xx GET body is retained.
- There is no real-network check in default CI, in module import or in the self-test. A child receives no inherited HTTP_PROXY, HTTPS_PROXY, SSL_CERT_FILE, PYTHONPATH, or HOME.
- Production readiness also requires review of live REAL_HTTP journal validation and source fingerprint binding, process-tree portability, parser interoperability, and an independent red-team-style security gate. The PR must remain DRAFT and **MUST NOT MERGE** until all applicable gates are completed and the independent reviewer explicitly signs off.

Related: issue #612; previous offline-only PRs #615, #616 and #617. A success in this PR does not imply release approval for v3.1.0, normative ABNT acceptance or maintainer visual sign-off.
