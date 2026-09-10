# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-10
Status: RELEASE — R1.3 correction committed at `64192a35bde415bfca5abdb86fbfea85766e601c`; fresh Static/Linux evidence pending; publication blocked

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

## Execution state

R0 is DONE. R1.1 is DONE: seven canonical chapter names are sequential and semantic; Static #474 failed closed on stale path consumers and Static #475 passed after reconciliation. R1.2 is DONE: the coverage matrix and history audit prove that all seven reviewed commented-guide chapter bodies survived from `2cbd6d0...` to the R1.3 boundary as renames with zero additions/deletions; Static #476 passed.

R1.3 is still open. The bounded teaching rewrite is anchored at `f8452bc3507a5206fc4e5a4c837feef872f23f3c`. It preserves the reviewed object corpus and adds mechanism/evidence callouts, coherent `\ufcsetup` guidance, list behavior, font embedding, a footnote example, citation/`apud` guidance, all seven profiles, build workflow, CLI/Deep, bounded Web/Lite guidance, accessibility limits and an expanded checklist.

The audit trail that must be preserved:

- Static #478 (`34481185238`) failed because `AGENTS.md` lost the exact required governance concept `material advance` during bootstrap rewriting.
- Commit `e2f1998ac9e565767d85aedbcd65f2fa48e38d0d` restored explicit `material advance` and `phase-end regression` wording without weakening the checker.
- Static #479 (`34481697858`) passed.
- Linux #399 (`34481697908`) was green but heavy integration was skipped because the PR was draft; it is not acceptance evidence.
- PR #305 was moved to ready-for-review solely to let the repository-owned integration run. Ready-for-review does not mean ready to merge.
- Linux #400 (`34481808802`) ran scope `complete` and failed with `PASS=32 FAIL=1 SKIP=3`. The sole failing check was `reference`.
- Root cause of #400: the R1.3 subsection heading contained the `\ufcsetup` configuration command in a moving argument. When `main.toc` was re-read, LaTeX executed the command and reported unknown key `ufc/\check@icr`.
- Commit `64192a35bde415bfca5abdb86fbfea85766e601c` changes that heading to `Configuração central do documento`, retaining the API command only in body text, and synchronizes R1.3 evidence/state/handoff.

Current next action is to validate `64192a35bde415bfca5abdb86fbfea85766e601c` with a fresh Static run and a real Linux integration run. R1.3 becomes DONE only when the canonical reference check passes. R2 must not begin before that.

## R2–R4 prepared decisions

R2 must promote the full PDF built from `template/main.tex` to a first-class canonical reference. Existing `tests/integration/release-reference-reproducibility.sh` already performs two independent clean builds, SHA-256 equality, font-embedding validation, CLI/Deep validation, PDF/A-2b validation and Unicode extraction. R2 should reuse that implementation rather than duplicate it, expose its PDF/evidence through the existing Linux integration/release infrastructure, and obtain page-by-page visual review evidence.

R3 must keep two roles separate: the minimal CTAN example remains small; the full canonical TCC becomes a public user-facing reference. A critical packaging constraint already exists: `tools/build-public-bundles.py` replaces `coat-of-arms = true` with `coat-of-arms = false` in distributed `main.tex`. Therefore a public full reference PDF must be compiled from the same sanitized public source variant. Do not copy the source-tree PDF with the institutional mark into public bundles. Do not redistribute Microsoft fonts or UFC mark assets.

R4 must repair the Web/Lite deployment and E2E path. `validator/app.js` imports `./normative-catalog.js`, while the tracked static validator tree lacks that module. `tools/normative_catalog.py --emit-web` can generate it deterministically, but current tests generate it only in a temporary directory. The real `analyze(file, profile)` function already exists in `validator/app.js`; R4 should test that same implementation in a clean browser deployment instead of creating a parallel validator. Deep-only checks such as font embedding and full PDF/A certification must remain REVIEW in Web/Lite.

## Remaining work

R2: full canonical reference PDF contract and artifact.  
R3: public distribution repair with source/PDF correspondence and hash assertions.  
R4: deterministic Web/Lite site materialization plus real-PDF positive/negative E2E.  
R5: one exact immutable candidate passes Static, complete Linux Integration, Linux Release Check, current CTAN pkgcheck, canonical reference, seven profile pairs, CLI/Deep, Web/Lite E2E and frozen distribution hashes.  
R6: maintainer visually approves the full canonical TCC and seven profile pairs from that exact R5 SHA; then tag, GitHub Release and CTAN use exactly those bytes.

Invariant:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Documentation discipline

Every material advance updates `release/v3.0.1-final-corrections.json`, the affected lot evidence and this handoff in the same work cycle. Failed checks remain recorded after successful reruns. The mandatory phase-end regression on one immutable candidate remains distinct from targeted development checks.
