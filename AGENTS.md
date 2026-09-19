# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Current Git facts and current machine-readable state are authoritative; historical documents and prior conversation context are not.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata or publication state:

1. resolve the actual branch, HEAD and `origin/main` dynamically;
2. read `docs/RELEASE-STATE.md` and `release/v3-release-candidate.json`;
3. inspect current GitHub tags/releases only when publication facts are relevant;
4. consult `docs/history/v3/` and `release/history/v3/` only for historical evidence;
5. never treat a closed Issue or historical release document as current authority.

Priority on disagreement: **current Git/GitHub facts > machine release receipt > `docs/RELEASE-STATE.md` > current technical policy > controlled historical evidence > prior chat or memory**.

## Current repository state

| Fact | Current state |
|---|---|
| Published release | `v3.0.3` |
| Frozen publication source | `b98270f23b1b384773c409869dfb05d71acd8638` |
| Canonical branch | `main`; resolve SHA dynamically |
| Repository lifecycle | v3.0.4 unreleased development |
| Active runtime development candidate | `v3.0.4` / issue #335 / NOT_FROZEN |
| Active release issue | #335 (development tracking; not publication authorization) |
| Workflow lifecycle | Static Contract, Linux Integration, Linux Release Check and Pages are permanent distinct workflows |
| Branch hygiene | steady state: `main` plus only active short-lived PR branches; merged heads auto-delete |

Published version tags/releases and their assets must never be rewritten, retargeted or rebuilt. Any future runtime/public-API change belongs to a new unreleased development line.

## Active and historical authority

Current steady-state authority consists of:

- `docs/RELEASE-STATE.md`;
- `release/v3-release-candidate.json`;
- current durable technical documentation;
- current GitHub tag/release state when publication facts are being verified.

Historical v3 engineering evidence belongs under `docs/history/v3/`. Historical machine state belongs under `release/history/v3/`. Historical receipts may preserve obsolete paths, issue numbers, phase names and release states as evidence, but they do not override current facts.

## Progress documentation discipline

A material advance changes runtime, evidence, repository lifecycle, validation state or release readiness. Every material advance must leave an exact commit/PR receipt, executed checks with classification, and unresolved findings carried forward explicitly.

Failed checks remain part of the audit trail after successful reruns. Do not rewrite history to make a sequence appear uniformly green.

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

Use the existing `tools/build-public-bundles.py` / `tools/build-distribution-bundles.py` pipeline until a separately reviewed runtime/package architecture change explicitly replaces it.

Distribution regression must extract Template and Overleaf, rebuild their exact source deterministically, and compare the rebuilt PDF with the embedded `abntexto-ufc-reference.pdf`. The CTAN archive remains the intentionally sanitized surface.

## Release-state policy

There is exactly one root machine receipt path: `release/v3-release-candidate.json`.

During the active v3.0.4 development line it records:

- `lifecycle = active-development-marker`;
- `development_line = 3.0.4`;
- `target_version = 3.0.4`;
- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_state = UNPUBLISHED`;
- `publication_authorized = false`;
- `tracking_issue = 335`;
- published v3.0.3 receipt preserved separately in the marker;
- authority `docs/RELEASE-STATE.md`.

Changing the root marker is a deliberate release-control event and forces complete validation. Historical machine state under `release/history/v3/` must never trigger candidate semantics.

## Release invariant

A release candidate must bind technical certification, generated artifacts, maintainer visual acceptance, tag and publication bytes to one immutable source SHA:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published release bytes
```

A subsequent control or documentation commit does not become the publication source unless it independently undergoes the full release process.

GitHub publication and CTAN submission are separate operations. A delayed CTAN submission must use the already-certified canonical archive from the corresponding published release and must not justify rebuilding release bytes.

## Repository hygiene rule

Active paths must describe current supported state. Closed phase/version control documents must either:

- move into controlled `docs/history/v3/` or `release/history/v3/` namespaces with explicit historical classification; or
- be removed from the active tree while remaining recoverable through Git history.

Generated PDFs/ZIPs, build products, editor state, CI downloads, publication kits and temporary assets must never be tracked. Local release/audit material belongs under ignored `.release/`.

Short-lived PR branches must disappear after merge. TODO/FIXME markers and stale active-path references are blockers unless explicitly documented as intentional test fixtures.

## Runtime-source architecture changes

The current project-owned runtime is one canonical `abntexto-ufc.cls`. Runtime-source changes must:

1. remain inside the active unreleased development line;
2. preserve the public API and rendered behavior unless a reviewed versioned change explicitly says otherwise;
3. prove source/package equivalence through the required Static, Linux Integration and Linux Release checks;
4. keep one project runtime source of truth;
5. never modify already-published tags or release assets.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for explicit maintainer visual approval when a release gate requires it.
