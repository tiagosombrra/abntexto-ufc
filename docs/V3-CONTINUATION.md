# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1.3 page-23 geometry correction committed for targeted validation; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct current state from chat history.

## Start here

1. Resolve the actual branch, HEAD and `origin/main` from Git.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `release/v3.0.1-final-corrections.json`.
5. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
6. Continue from `current_next_action` in the machine state.

Current Git facts override the machine state; the machine state overrides this handoff; lot evidence overrides older phase/recovery documents. Prior conversation memory is lowest priority.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; retained as evidence, superseded as final candidate |
| Active branch | `release/v3.0.1-final-corrections` |
| Tracking issue / PR | #304 / #305 |
| PR merge | BLOCKED until R1–R5 acceptance |
| Target | `v3.0.1` |
| Publication | BLOCKED until R6 |
| Public `v3.0.0` | historical/superseded; never retarget |

## R1 state

R1.1 is DONE. Seven canonical chapter names are sequential/semantic; Static #474 failed closed on stale path consumers and Static #475 passed after reconciliation.

R1.2 is DONE. The coverage matrix and history audit prove that all seven reviewed commented-guide chapter bodies survived from `2cbd6d0...` to the R1.3 boundary as renames with zero additions/deletions; Static #476 passed.

R1.3 remains open. The bounded teaching rewrite at `f8452bc...` preserves the reviewed object corpus and adds mechanism/evidence callouts, coherent `\ufcsetup` guidance, list behavior, font embedding, footnote/citation examples, all seven profiles, build workflow, CLI/Deep, bounded Web/Lite guidance, accessibility limits and an expanded checklist.

Preserve this audit trail:

- Static #478 (`34481185238`) failed because `AGENTS.md` lost the required governance phrase `material advance`; `e2f1998...` restored `material advance` and `phase-end regression` without weakening the checker. Static #479 passed.
- Linux #399 was green but heavy integration was skipped because the PR was draft; it is not acceptance evidence. PR #305 was moved to ready-for-review only so repository-owned integration could execute; this does not authorize merge.
- Linux #400 (`34481808802`) ran `complete` and failed only `reference`; root cause was executable `\ufcsetup` in a `.toc`-replayed moving heading. The heading is now plain `Configuração central do documento`.
- Static #481 (`34484253436`) passed on the corrected-heading head `ba8aeb1...`.
- Linux #402 (`34484253425`) was superseded/cancelled after an unnecessarily broad selection caused by treating the active state JSON as an unknown technical path.
- Commit `1438a7cad27116170440535b9f62e2c084c0c8b8` corrected that selector classification without weakening fail-closed technical behavior. Static #482 (`34485632344`) passed.
- Linux #403 (`34485632570`) correctly selected `reference-document`, but failed the strict warning gate on two long monospaced invocations in chapter 5. Those invocations were split without semantic change in `e7f6fc88618329505e7f0de4449aec7c54fe45b0`.
- Static #483 (`34487258470`) passed on `e7f6fc8...`.
- Linux #404 (`34487258455`) on `e7f6fc8...` proved `reference=PASS` and `reference-corpus=PASS`; only `pdf-validator` failed. PDF.js measured one em dash on page 23 at `(82.6, 94.9)` pt, approximately 0.6 pt beyond the left-margin threshold including tolerance.
- The page-23 glyph correlates with editorial em-dash punctuation around `como \section e \subsection` in chapter 2. The current correction replaces those dashes with commas. Meaning, margin values, tolerance and validator logic are unchanged.

## Bounded CI-scope correction

`release/v3.0.1-final-corrections.json` is required machine-readable documentation/control state. Updating it alone does not launch heavy integration. Unknown technical files still select `complete`; runtime/core/standards changes retain required scopes; final/release candidate markers force `complete`; orchestration-only changes select `smoke`; canonical TCC changes select `reference-document`. The selector self-test and `tests/checks/linux_integration_suites.py` protect this rule.

Current next action: resolve the current branch HEAD dynamically. Require fresh Static PASS and a real `reference-document` Linux run with `reference`, `reference-corpus` and `pdf-validator` all PASS and no skips. If that succeeds, mark R1.3 DONE and begin R2.

## R2 prepared decision

Do not create another PDF generator. `make release-check` already invokes `tests/integration/release-reference-reproducibility.sh`, which performs two independent clean builds, byte-identical SHA-256 comparison, font embedding, CLI/Deep, PDF/A-2b and Unicode extraction and writes `artifacts/validation/release-reference-pdf.pdf` plus provenance JSON. R2 must make this output a first-class named release artifact and statically protect that wiring. The existing Linux Release Check should remain the authoritative heavy execution path; avoid a redundant full Linux integration solely because an upload step changes.

## R3 prepared decision

Keep the minimal CTAN example separate from the full canonical TCC. `tools/build-public-bundles.py` sanitizes distributed `main.tex` from `coat-of-arms = true` to `false`; the public full PDF must therefore be compiled from that same sanitized source variant, not copied from the source-tree PDF. The strongest distribution regression is to recompile the extracted sanitized Overleaf source and compare its PDF hash with the full reference PDF embedded in the public bundles. The CTAN archive remains minimal unless an explicit later decision changes that role. Never redistribute Microsoft fonts or UFC mark assets.

## R4 prepared decision

`validator/app.js` imports missing `./normative-catalog.js`. Prefer a deterministic generated-and-tracked `validator/normative-catalog.js` with a static byte-for-byte equality check against `tools/normative_catalog.py --emit-web`; this keeps a plain static checkout deployable and prevents generator drift. Then add clean relative-module closure plus a real-PDF browser E2E through the existing `analyze(file, profile)` implementation, using a canonical positive PDF and a negative PDF. Deep-only checks remain REVIEW rather than false PASS. No public Pages state is assumed without repository evidence.

## Remaining work

R2 full canonical reference PDF and visual evidence; R3 public distribution repair; R4 Web/Lite static package + real-PDF E2E; R5 exact immutable release regression; R6 maintainer visual acceptance and publication.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Documentation discipline

Every material advance updates the machine state, affected lot evidence and this handoff in the same work cycle. Failed checks remain recorded after successful reruns. The mandatory phase-end regression on one immutable candidate remains distinct from targeted development checks.
