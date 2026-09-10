# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1.3 typography correction committed for targeted validation; publication blocked

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

- Static #478 (`34481185238`) failed because `AGENTS.md` lost the required governance phrase `material advance`; `e2f1998...` restored `material advance` and `phase-end regression` without weakening the checker.
- Static #479 passed.
- Linux #399 was green but heavy integration was skipped because the PR was draft; it is not acceptance evidence.
- PR #305 was moved to ready-for-review only so repository-owned integration could execute. This does not authorize merge.
- Linux #400 (`34481808802`) ran `complete` and failed `PASS=32 FAIL=1 SKIP=3`; the sole failure was `reference`.
- Root cause of #400: an R1.3 subsection heading contained the executable `\ufcsetup` command. `main.toc` replay executed it and produced unknown key `ufc/\check@icr`.
- The heading is plain `Configuração central do documento`; `\ufcsetup` remains only in body text. A source comment records that executable commands must stay out of this moving heading.
- Static #481 (`34484253436`) passed on the corrected-heading head `ba8aeb1...`.
- Linux #402 (`34484253425`) was superseded and cancelled by workflow concurrency after it selected an unnecessarily broad scope because the active state JSON had been treated as an unknown technical path.
- Commit `1438a7cad27116170440535b9f62e2c084c0c8b8` corrected that selector classification without weakening fail-closed technical behavior.
- Static #482 (`34485632344`) passed on `1438a7c...`.
- Linux #403 (`34485632570`) correctly selected `reference-document`, but failed `PASS=0 FAIL=1 SKIP=2`. `make compile` completed and generated a 63-page `template/main.pdf`; the strict warning gate then found one `Underfull \hbox` at source line 39 and one `Overfull \hbox` of 29.22328 pt at source line 57.
- Both warning lines were traced to `template/chapters/5-citations-notes-references.tex`: oversized monospaced command invocations for `\apud` and `\ufcAddBibliographyResource`. The current correction retains the semantics but splits command names, arguments and paths into smaller breakable units. The warning gate is unchanged.

## Bounded CI-scope correction

`release/v3.0.1-final-corrections.json` is required machine-readable documentation/control state. Updating that file alone must not launch heavy integration. The selector treats it as docs-only, matching `release/v3-roadmap.json` and `docs/**`.

Fail-closed behavior remains: unknown technical files still select `complete`; runtime/core/standards changes retain required scopes; final/release candidate markers force `complete`; orchestration-only changes select `smoke`; canonical TCC changes select `reference-document`. The selector self-test and `tests/checks/linux_integration_suites.py` protect this rule.

Current next action: resolve the current branch HEAD dynamically. Require fresh Static PASS and a real `reference-document` Linux run with `reference`, `reference-corpus` and `pdf-validator` all PASS and no skips. If that succeeds, mark R1.3 DONE and begin R2.

## R2–R4 prepared decisions

R2: promote the full PDF from `template/main.tex` to a first-class canonical reference. Reuse `tests/integration/release-reference-reproducibility.sh`, which already performs two independent clean builds, byte-identical SHA-256 comparison, font embedding, CLI/Deep, PDF/A-2b and Unicode extraction. Expose the generated PDF/evidence through the existing Linux workflow rather than creating a fourth workflow, then perform page-by-page visual review.

R3: keep the minimal CTAN example separate from the full canonical TCC. `tools/build-public-bundles.py` sanitizes distributed `main.tex` from `coat-of-arms = true` to `false`; therefore the public full PDF must be compiled from that same sanitized source variant. Never copy the source-tree marked PDF into public bundles. Do not redistribute Microsoft fonts or UFC mark assets.

R4: repair Web/Lite. `validator/app.js` imports missing `./normative-catalog.js`; `tools/normative_catalog.py --emit-web` already generates it deterministically but only to temporary locations in current tests. Build a clean static site with that generated module and test the existing real `analyze(file, profile)` path in a browser using a canonical PDF and a negative PDF. Deep-only checks must remain REVIEW rather than false PASS. No indexed public Pages deployment was established during the current audit, and the connector does not expose repository Pages configuration; do not assume deployment state without Git/repository evidence.

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
