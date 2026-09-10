# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1 closed; R2 ready to make canonical PDF first-class; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct current state from chat history.

## Start here

1. Resolve the actual branch, HEAD and `origin/main` from Git.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `release/v3.0.1-final-corrections.json`.
5. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
6. Read the evidence document for the active lot.
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
| PR state | ready-for-review only so CI can execute; merge remains blocked |
| Target | `v3.0.1` |
| Publication | BLOCKED until R6 |
| Public `v3.0.0` | historical/superseded; never retarget |

## R1 — DONE

R1.1 normalized the seven canonical chapter paths and reconciled consumers. R1.2 established pedagogical coverage and historical retention. R1.3 completed the bounded teaching rewrite without changing class runtime or normative values.

R1.3 acceptance source is exactly `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa`:

- Static #484 (`34488189988`): PASS;
- Linux #405 (`34488190044`): PASS;
- Linux scope: `reference-document`;
- summary: `PASS=3 FAIL=0 SKIP=0`;
- individual checks: `reference=PASS`, `reference-corpus=PASS`, `pdf-validator=PASS`.

The earlier #478, #400, #403 and #404 failures remain recorded in `docs/V3.0.1-R1.3-EVIDENCE.md`; they document governance drift, a moving-heading command execution bug, monospaced overflow and an editorial punctuation margin protrusion that were corrected without weakening gates.

## R2 — READY

Goal: make the full PDF generated from `template/main.tex` a first-class canonical release reference.

Do not create another PDF generator. `make release-check` already invokes `tests/integration/release-reference-reproducibility.sh`, which performs two independent clean builds, byte-identical SHA-256 comparison, font embedding, CLI/Deep, PDF/A-2b and Unicode extraction and writes:

- `artifacts/validation/release-reference-pdf.pdf`;
- `artifacts/validation/release-reference-reproducibility.json`.

R2 implementation should expose these two files as a dedicated named artifact in the existing Linux Release Check and add a static contract that prevents that wiring from disappearing. The generic validation artifact may remain; the dedicated artifact establishes explicit identity and review ergonomics.

To avoid duplicate heavy CI, classify `.github/workflows/linux-release-check.yml` as orchestration for PR integration selection and protect that classification with the existing suite-contract checker. A change to the release workflow itself already triggers Linux Release Check, which is the authoritative heavy execution path for R2. Release-candidate markers must still force `complete`.

R2 closure requires successful release-reference generation on the R2 implementation SHA, verified PDF/provenance artifact availability and page-by-page development visual inspection. That inspection is R2 evidence only; it does not replace R6 maintainer visual acceptance.

## R3 prepared decision

Keep the minimal CTAN example separate from the full canonical TCC. `tools/build-public-bundles.py` sanitizes distributed `main.tex` from `coat-of-arms = true` to `false`; the public full PDF must be compiled from that same sanitized source variant, not copied from the source-tree PDF. The strongest distribution regression is to recompile extracted sanitized public source and compare its PDF hash with the reference PDF embedded in template/Overleaf bundles. Do not redistribute Microsoft fonts or UFC mark assets.

## R4 prepared decision

`validator/app.js` imports missing `./normative-catalog.js`. Prefer a deterministic generated-and-tracked `validator/normative-catalog.js` with static byte-for-byte equality against `tools/normative_catalog.py --emit-web`, so a plain static checkout is complete. Then add relative-module closure and a real-PDF browser E2E through the existing `analyze(file, profile)` path with positive and negative PDFs. Deep-only checks remain REVIEW rather than false PASS. Do not assume a GitHub Pages deployment without repository evidence.

## Remaining work

R2 full canonical reference PDF artifact + visual evidence; R3 public distribution repair; R4 Web/Lite static package + real-PDF E2E; R5 exact immutable phase-end release regression; R6 maintainer visual acceptance and publication.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Documentation discipline

Every material advance updates the machine state, affected lot evidence and this handoff in the same work cycle. Failed checks remain recorded after successful reruns. The mandatory R5 phase-end regression on one immutable candidate remains distinct from targeted development checks.
