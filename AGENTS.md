# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Current repository state is authoritative; conversation memory and historical documents are not.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata or publication state:

1. resolve the actual branch, HEAD and `origin/main` dynamically;
2. read `release/v3-release-candidate.json` and `docs/V3.0.3-DISTRIBUTION-CORRECTION.md`;
3. inspect issue #328 for live v3.0.3 release-control receipts;
4. consult `docs/history/v3/` and `release/history/v3/` only when historical evidence is relevant;
5. use issue #313 only for the external v3.0.2 CTAN publication receipt while that submission remains open.

Priority on disagreement: **current Git facts > active release marker > current v3.0.3 authority/issue #328 > current technical policy > controlled historical evidence > prior chat or memory**.

## Current development state

| Fact | Current state |
|---|---|
| Published/frozen baseline | `v3.0.2`; immutable GitHub Release; CTAN submission tracked externally in #313 |
| Current development line | `v3.0.3` |
| Canonical branch | `main`; resolve SHA dynamically |
| Repository lifecycle | Final v3.0.3 audit/cleanup and candidate preparation |
| v3.0.2 external publication tracking | #313 — CTAN receipt only |
| v3.0.3 release tracking | #328 |
| Implementation transport | PR #329 — merged historical receipt |
| Release-state documentation reconciliation | PR #330 — merged historical receipt |
| Branch hygiene | steady state: `main` plus only active short-lived PR branches; merged heads auto-delete |
| Workflow lifecycle | Static Contract, Linux Integration, Linux Release Check and Pages are permanent distinct workflows |
| Active candidate state | `NOT_FROZEN`; no candidate SHA; publication not authorized until explicit freeze |

The `v3.0.0`, `v3.0.1` and `v3.0.2` tags/releases/publication bytes must never be rewritten. Any correction belongs to a later version.

## Active and historical authority

Active v3.0.3 release authority consists of:

- `release/v3-release-candidate.json`;
- `docs/V3.0.3-DISTRIBUTION-CORRECTION.md`;
- issue #328.

Historical v3 engineering evidence belongs under `docs/history/v3/`. Historical machine state belongs under `release/history/v3/`. The frozen v3.0.2 release snapshot is `release/history/v3/v3.0.2-release-candidate.json`.

The compact v3.0.2 repository-hygiene receipt is retained at `docs/history/v3/audits/V3.0.2-REPOSITORY-HYGIENE-RECEIPT.md`. Detailed superseded snapshots remain recoverable from Git history and are not active control-plane documents.

## Progress documentation discipline

A material advance changes runtime, evidence, repository lifecycle, validation state or release readiness. Every material advance must leave an exact commit/PR receipt, executed checks with classification, and unresolved findings carried forward explicitly.

Failed checks remain part of the audit trail after successful reruns. Do not rewrite history to make the sequence appear uniformly green.

## Canonical TCC/reference rules

The canonical undergraduate artifact is rooted at `template/main.tex` and is a compact TCC tutorial, not the exhaustive API/normative manual. Its five sequential chapter files are:

`1-introduction.tex`, `2-theoretical-background.tex`, `3-methodology.tex`, `4-results.tex`, and `5-conclusion.tex`.

Responsibilities remain separated:

- `template/` teaches by realistic use;
- `docs/USER-GUIDE.md` explains workflow and normative/institutional context;
- `docs/COMMAND-REFERENCE.md` documents the public configuration/command/environment surface;
- `standards/` owns machine normative traceability;
- `tests/` owns exhaustive regression and edge-case coverage.

The canonical tutorial PDF is budgeted at 15–35 pages by integration gates. Do not re-expand it merely to carry maintainer documentation or test coverage.

## Distribution contract

The distribution contract is surface-specific and fail-closed:

- **CTAN:** no UFC coat-of-arms asset, no proprietary Microsoft font files, minimal example uses `coat-of-arms=false`;
- **Template:** include exactly `assets/institutional/ufc-coat-of-arms.png`, preserve canonical `coat-of-arms=true`, and embed a reference PDF generated from that exact source;
- **Overleaf:** include the same institutional PNG, preserve canonical `coat-of-arms=true`, include the pinned `abntexto.cls`, and embed the same reference PDF;
- no distribution surface may contain proprietary Microsoft font files.

Use the existing `tools/build-public-bundles.py` / `tools/build-distribution-bundles.py` pipeline. Do not create a competing release generator.

Distribution regression must extract Template and Overleaf, rebuild their exact source deterministically, and compare the rebuilt PDF with the embedded `abntexto-ufc-reference.pdf`. The CTAN archive remains the intentionally sanitized surface.

## Active release-marker policy

There is exactly one active release marker path: `release/v3-release-candidate.json`.

Before freeze, v3.0.3 must remain:

- `development_line = 3.0.3`;
- `target_version = 3.0.3`;
- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_authorized = false`;
- tracking issue #328;
- authority `docs/V3.0.3-DISTRIBUTION-CORRECTION.md`.

Changing the active marker is a deliberate release-control event and forces complete Linux integration/release validation. Historical machine state under `release/history/v3/` must never trigger candidate semantics.

## Release invariant

A release candidate must bind technical certification, generated artifacts, maintainer visual acceptance, tag and publication bytes to one immutable source SHA:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published release bytes
```

A candidate may be frozen only after the exact source SHA has passed the complete technical release path and its canonical/reference profile PDFs have received explicit maintainer visual acceptance.

The subsequent control commit that records `FROZEN` state does not become the publication source. The version tag must resolve to the already-certified candidate SHA.

GitHub publication of v3.0.3 may be completed independently of the later CTAN update. The v3.0.3 CTAN archive is retained for future submission, but CTAN timing is an external follow-up and does not justify modifying certified GitHub release bytes.

## Repository hygiene rule

Active paths must describe current supported state. Closed phase/version control documents must either:

- move into the controlled `docs/history/v3/` or `release/history/v3/` namespaces with explicit historical classification; or
- be removed from the active tree while remaining recoverable through Git history.

Generated PDFs/ZIPs, build products, editor state and temporary downloaded assets must never be tracked. Short-lived PR branches must disappear after merge. TODO/FIXME markers and stale paths are release blockers unless explicitly documented as intentional test fixtures.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for explicit maintainer visual approval.
