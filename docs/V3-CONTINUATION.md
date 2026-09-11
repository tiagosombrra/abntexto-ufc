# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R0/R1/R2/R3 DONE; R4 IN_PROGRESS; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct current state from chat history.

## Start here

1. Resolve the actual branch, HEAD and `origin/main` from Git.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `release/v3.0.1-final-corrections.json`.
5. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
6. For the active lot R4, read `docs/V3.0.1-R4-EVIDENCE.md`.
7. Continue from `current_next_action` in the machine state.

Current Git facts override the machine state; the machine state overrides this handoff; lot evidence overrides older phase/recovery documents. Prior conversation memory is lowest priority.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; retained as evidence, superseded as final candidate |
| Active branch | `release/v3.0.1-final-corrections` |
| Tracking issue / PR | #304 / #305 |
| PR state | CI vehicle only; merge remains blocked |
| Target | `v3.0.1` |
| Publication | BLOCKED until R6 |
| Public `v3.0.0` | historical/superseded; never retarget |

## R0/R1 — DONE

R0 established the auditable correction control plane. R1 normalized the seven canonical chapter paths, established pedagogical/normative coverage and completed the coherent teaching rewrite.

R1.3 acceptance source: `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa`.

- Static #484 (`34488189988`): PASS.
- Linux #405 (`34488190044`): PASS.
- Linux scope: `reference-document`.
- Summary: `PASS=3 FAIL=0 SKIP=0`.

Detailed earlier failures and corrections remain in `docs/V3.0.1-R1.3-EVIDENCE.md`.

## R2 — DONE

R2 makes the complete PDF rooted at `template/main.tex` a first-class exact-SHA engineering release reference. Acceptance source: `514c128f542b00d4a10a9ad05ce7fc94f770ef55`.

- Static #486 (`34491624099`): PASS.
- Linux #407 (`34491624073`): PASS, `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`.
- Linux Release Check #121 (`34491624158`): PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.
- CTAN `pkgcheck 4.1.0`: PASS in the same release run.
- Canonical PDF SHA-256: `bd8964c8a37940924758d44eef61bc079f5101cf25cd180b42c3df22e00d1d3a`.
- Two independent clean builds are byte-identical; font embedding, portable CLI/Deep validation, PDF/A-2b and Unicode extraction are PASS.
- Dedicated artifact: `abntexto-ufc-v3.0.1-canonical-reference-34491624158`, id `10158771936`, archive digest `sha256:0677b776c3eb3a358f91a06119973a00b8f3aa8ade841d54565f85fe5db53bc7`.
- The exact 63-page A4 PDF was rendered and inspected page by page; no clipping, overlap, broken glyphs, black boxes or missing structural blocks were observed.

The R2 visual inspection is development evidence only; it does not replace R6 explicit maintainer acceptance on the final immutable R5 candidate. Full evidence: `docs/V3.0.1-R2-EVIDENCE.md`.

## R3 — DONE

R3 repairs public distribution so users receive the complete editable source and a compiled full pedagogical reference while CTAN remains lean.

The implementation commit containing this handoff must be resolved dynamically from the active branch. It introduces:

- generated public filename `abntexto-ufc-reference.pdf`;
- deterministic compilation by `tools/build-public-bundles.py` from the exact public `main.tex` sanitized to `coat-of-arms = false`;
- the same generated reference PDF embedded in template and Overleaf bundles;
- no full reference PDF in the CTAN archive, whose minimal example remains separate;
- an extracted-bundle gate that independently rebuilds template and Overleaf projects and requires rebuilt SHA-256 == embedded PDF SHA-256;
- fail-closed checks for no institutional mark assets, no proprietary Microsoft fonts and correct public mark disablement;
- first-class PR integration suite `distribution`, with release-mode distribution execution still owned by `make release-check` to avoid duplicate execution.

`tools/build-distribution-bundles.py` is intentionally unchanged because it already delegates usage-bundle generation to `tools/build-public-bundles.py`.

Accepted corrective source: `2556489da23e16495fc51ebf093f9f4704c6d52f`.

- Static #489: PASS.
- Linux #410: PASS, `SCOPE=distribution PASS=1 FAIL=0 SKIP=0`.
- Linux Release Check #124: PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.
- CTAN `pkgcheck 4.1.0`: PASS.
- Exact distribution artifact id `10169809155`, digest `sha256:6445ce5e3b870fc6c418fa23c4dc318576f58d00bfe48525ed100e86feaca761`.
- Release public-reference SHA-256 `e92378a0ef01310c656599d1f1765db6d0040467367313e74776c8ebd75b766c`, identical in Template/Overleaf, 63 A4 pages.
- Independent archive/hash/content and page-by-page visual inspection: PASS.
- CTAN excludes the full reference; distributed source uses `coat-of-arms=false`; no prohibited mark/font files were found.

The first implementation failures #409/#123 and their causes remain retained in `docs/V3.0.1-R3-EVIDENCE.md`.

## R4 — CORRECTIVE COMMIT IN CI

The R4 source closes both entry defects: `validator/normative-catalog.js` is generated/tracked and byte-compared against the authoritative generator; the source gate proves relative-module closure; and Linux `web-lite` snapshots the real canonical/reference PDF and drives the productive UI in Chrome with positive and non-A4 negative PDFs. Static #491/#492/#493 passed across successive corrections. Linux #412 timed out creating the local ChromeDriver session; Linux #413 still failed before readiness and exposed a non-fail-safe log path; source `6560a0369e20b953c8ae8321a9e5a21317451735` then captured process output but Linux #414 failed before ChromeDriver launch with `PermissionError` because the host tried to write into container-owned `artifacts/validation`. Release Check #128 passed on that source. The current correction writes only browser JSON/log under host-owned `${RUNNER_TEMP}/abntexto-ufc-web-lite`; the positive PDF remains the existing read-only workspace snapshot. No PDF assertion, normative predicate or Deep-only `MANUAL REVIEW` boundary changes. Evidence contract: `docs/V3.0.1-R4-EVIDENCE.md`.

## R5/R6 — PENDING

R5 is the mandatory complete exact-SHA phase-end release regression on the final canonical `main` candidate after R3/R4 closure and correction-PR merge. R6 is explicit maintainer visual acceptance and publication. The invariant remains:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication. Post-publication documentation may advance only after the tag/release bytes are frozen and verified.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Current next action

Resolve the #414 corrective successor and inspect Static/Linux on that exact SHA. Require `web-lite` container PASS, host-side browser evidence under `${RUNNER_TEMP}/abntexto-ufc-web-lite`, and real Chrome E2E PASS. Inspect uploaded JSON and ChromeDriver log. The positive reference must pass readable/A4/margins without top-level FAIL; the valid non-A4 fixture must fail A4 with verdict FAIL; `font.embedded` and `pdfa.deep` remain `MANUAL REVIEW`; record exact input hashes. Preserve #412/#413/#414. Close R4 only after exact-HEAD browser evidence is independently inspected; then open R5.

## Documentation discipline

Every material advance updates the machine state, affected lot evidence and this handoff in the same work cycle. Current Git facts always take precedence.
