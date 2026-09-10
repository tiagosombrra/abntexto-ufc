# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R0/R1/R2 DONE; R3 IN_PROGRESS; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct current state from chat history.

## Start here

1. Resolve the actual branch, HEAD and `origin/main` from Git.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `release/v3.0.1-final-corrections.json`.
5. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
6. For the active lot R3, read `docs/V3.0.1-R3-EVIDENCE.md`.
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

## R3 — IN PROGRESS

Goal: repair public distribution so template/Overleaf users receive both the complete editable source and a compiled full reference PDF.

Critical boundary: the R2 source-tree PDF contains the configured UFC mark because `template/main.tex` uses `coat-of-arms=true`. It must not be copied into public bundles. `tools/build-public-bundles.py` already sanitizes distributed `main.tex` to `coat-of-arms=false`; R3 must compile the public reference PDF from that exact sanitized public source/runtime and prove source-to-PDF identity by SHA-256.

Fixed R3 decisions:

- keep `docs/ctan-example.tex` as the small CTAN example;
- put the complete public reference PDF in template/Overleaf GitHub bundles, generated rather than stored manually;
- keep the CTAN archive lean unless a concrete packaging requirement proves otherwise;
- never redistribute UFC mark assets or proprietary Microsoft font files;
- extend the existing bundle/distribution pipeline rather than creating a parallel generator;
- extract public bundles in regression, rebuild their exact source and require the rebuilt PDF hash to match the embedded reference PDF.

Active contract and evidence ledger: `docs/V3.0.1-R3-EVIDENCE.md`.

## R4 — PENDING

Known blocker: `validator/app.js` imports `./normative-catalog.js`, but that file is absent from the tracked static validator tree. R4 must generate/track it deterministically, prove clean relative-module closure and run a real positive canonical PDF plus a negative PDF through the actual Web/Lite `analyze(file, profile)` path. Deep-only checks remain REVIEW rather than false PASS. Do not claim public deployment without repository evidence.

## R5/R6 — PENDING

R5 is the mandatory complete exact-SHA phase-end release regression. R6 is explicit maintainer visual acceptance and publication. The invariant remains:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Documentation discipline

Every material advance updates the machine state, affected lot evidence and this handoff in the same work cycle. Failed checks remain recorded in the corresponding evidence documents after successful reruns. Current Git facts always take precedence.
