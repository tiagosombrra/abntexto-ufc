# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1.3 implemented; Static #478 failed on control-document wording and correction is being rerun; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct the current plan from chat history.

## Start here

1. Resolve branch, HEAD and `origin/main` from Git.
2. Read this file.
3. Read `release/v3.0.1-final-corrections.json`.
4. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
5. Continue from `current_next_action` in the machine state.

`AGENTS.md` defines fail-closed precedence, material-advance documentation and phase-end regression rules. Older v3 phase-end/recovery documents remain historical evidence and do not override this handoff.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve current SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565` — retained as evidence, superseded as final candidate |
| Active branch | `release/v3.0.1-final-corrections` |
| Tracking issue / PR | #304 / draft #305 |
| Target | `v3.0.1` |
| Publication | BLOCKED |
| Public `v3.0.0` | historical/superseded; never retarget |

## Execution state

R0 is DONE. R1.1 is DONE: canonical chapter names are sequential/semantic; Static #474 failed closed on old path consumers, then Static #475 passed after those consumers were reconciled. R1.2 is DONE: the pedagogical coverage matrix and historical-retention audit prove that all seven reviewed guide chapter bodies survived from `2cbd6d0...` to the R1.3 boundary as renames with zero additions/deletions; Static #476 passed.

R1.3 is implemented at `f8452bc3507a5206fc4e5a4c837feef872f23f3c`. The bounded rewrite preserves the reviewed object corpus and adds mechanism/evidence callouts, coherent `\ufcsetup` guidance, list behavior, font embedding, footnote example, citation/`apud` guidance, all seven profiles including `scientific-article`, module-policy boundaries, build workflow, CLI/Deep, bounded Web/Lite guidance, accessibility limits and an expanded final checklist. Evidence: `docs/V3.0.1-R1.3-EVIDENCE.md`.

CI on that implementation exposed a documentation-governance regression before the TCC contracts ran. Linux Integration #398 (`34481185134`) completed successfully under draft/development scope and is not release evidence. Static #478 (`34481185238`) failed because the self-contained `AGENTS.md` rewrite no longer contained the exact governance concept `material advance` required by `tests/checks/phase_governance.py`. The checker also requires `phase-end regression`. The correct fix is to restore those concepts in `AGENTS.md`; the checker is not weakened. This failure remains preserved in R1.3 evidence/machine state.

Current next action: rerun Static on the control-document correction. If Static passes, confirm the canonical reference/integration path and close R1.3. Then begin R2.

## Remaining work

R2: certify the full PDF from `template/main.tex` as the canonical release reference with deterministic build, warning/overflow preflight, A4/geometry, embedded fonts, PDF/A-2b where claimed, CLI/Deep, hash/provenance and visual review.

R3: repair distribution. The minimal CTAN example remains a separate small example. The full TCC must gain an explicit public release role without violating the existing ban on redistributing proprietary Microsoft fonts or disallowed UFC institutional marks.

R4: repair Web/Lite. Confirmed defect: `validator/app.js` imports `./normative-catalog.js`, but that module is absent from the tracked static tree. Existing synthetic cross-surface vectors do not run the actual canonical PDF through the browser analysis path. Require deterministic catalog materialization, clean module closure and real-PDF positive/negative E2E.

R5: certify one exact immutable SHA through the complete release matrix and freeze distribution hashes. R6: maintainer visually approves the full canonical TCC plus seven profile pairs from that same SHA; then tag/release/CTAN must use the exact frozen source/artifacts.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

## Deferred after v3.0.1

Whole-repository lifecycle cleanup, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain outside this release correction unless a direct blocker is demonstrated.

## Documentation discipline

Every material advance updates this handoff and `release/v3.0.1-final-corrections.json` in the same work cycle. Lot evidence stays under `docs/`. Issue #304 may record external CI receipts without a new source commit made solely to echo the result.
