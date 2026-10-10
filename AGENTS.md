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
| Published release | `v3.0.4` |
| Published v3.0.4 source | `7e176fd5472925b519d469a9a756330f4851f0b3` |
| GitHub Release ID | `392476983` |
| Canonical branch | `main`; resolve SHA dynamically |
| Repository lifecycle | v3.0.5 CTAN source correction #369/#475; #474 ACCEPT is historical for a superseded source; `NOT_FROZEN` / `UNPUBLISHED` |
| Active development line | `v3.0.5` — `NOT_FROZEN` / `UNPUBLISHED` |
| Active release-control issue | issue #475; metadata correction #369; earlier #471 / PR #472 is historical |
| Completed v3.0.4 release issue | issue #353 |
| CTAN follow-up | issue #356 — exact submitted bytes published as v3.0.4 on 2026-09-22 |
| Repository maintenance roadmap | issue #359 — active; current map in `docs/REPOSITORY-MAINTENANCE.md` |
| Workflow lifecycle | Static Contract, Linux Integration, Linux Release Check and Pages are permanent distinct workflows |
| Branch hygiene | `main` plus only active short-lived PR branches; merged heads auto-delete |

Published version tags/releases and their assets must never be rewritten, retargeted or rebuilt. Any future runtime/public-API change belongs to a newly selected unreleased development line.

## Active and historical authority

Current authority consists of:

- `docs/RELEASE-STATE.md`;
- `release/v3-release-candidate.json`;
- current durable technical documentation;
- current GitHub tag/release state when publication facts are being verified.

Historical v3 engineering evidence belongs under `docs/history/v3/`. Historical machine state belongs under `release/history/v3/`. Historical receipts may preserve obsolete paths, issue numbers, phase names and release states as evidence, but they do not override current facts.

## Progress documentation discipline

A material advance changes runtime, evidence, repository lifecycle, validation state, repository taxonomy or release readiness. Every material advance must leave an exact commit/PR receipt, executed checks with classification, and unresolved findings carried forward explicitly.

Repository-wide maintenance is currently mapped by `docs/REPOSITORY-MAINTENANCE.md` and issue #359. Update that map when a phase begins, completes, is superseded or discovers a material dependency. Do not advance to a structural move merely because the previous implementation commit exists; reconcile the durable map and current `main` first.

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

The repository currently has published v3.0.4 evidence plus a v3.0.5 maintenance line in release-candidate preparation:

- `lifecycle = active-development-marker`;
- `release_line = 3.0.5`;
- `target_version = 3.0.5`;
- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_state = UNPUBLISHED`;
- `publication_authorized = false`;
- `active_development_line = 3.0.5`;
- active tracking issue #471 / PR #472;
- latest published GitHub Release remains v3.0.4 / ID `392476983`;
- authority `docs/RELEASE-STATE.md`.

The embedded published-release receipt for v3.0.4 remains immutable and continues to bind source `7e176fd5472925b519d469a9a756330f4851f0b3`, Static #675, Linux #582, Linux Release run `35510145977`, CTAN `pkgcheck 4.1.0`, explicit maintainer visual acceptance, annotated tag identity and published asset digests.

Phase 10B finalizes release-source content before candidate selection. It still does not freeze a source: the exact merged #472 source must receive fresh full certification and explicit maintainer visual acceptance before a later control-plane freeze/tag/publication step.

Completed release machine receipts belong under `release/history/v3/`; completed publication narrative belongs under `docs/history/v3/release/`. The exact published CTAN archive for v3.0.4 was submitted on 2026-09-20 under issue #356; the official CTAN-ann update confirmed v3.0.4 publication on 2026-09-22. The submitted bytes remain immutable and must not be rebuilt or replaced.

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

Structural taxonomy changes must preserve semantic identity independently of directory depth. Movable static/integration entrypoints use `tests/path_resolver.py`; machine normative authorities use `tools/repository_paths.py`. Do not create duplicate compatibility copies merely to preserve an old path: ambiguity must fail closed and callers must be migrated to the canonical resolver or updated atomically with the owning move.

## Runtime-source architecture changes

The current project-owned runtime is one canonical `abntexto-ufc.cls`. Runtime-source changes must:

1. remain inside the active unreleased development line;
2. preserve the public API and rendered behavior unless a reviewed versioned change explicitly says otherwise;
3. prove source/package equivalence through the required Static, Linux Integration and Linux Release checks;
4. keep one project runtime source of truth;
5. never modify already-published tags or release assets.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for explicit maintainer visual approval when a release gate requires it.

## v3.0.5 explicit maintainer ACCEPT receipt

The maintainer explicitly recorded `ACCEPT` on 2026-10-09 for certified source `407f279a78df3824b27585d0e86d688c19cd90ee` and retained seven-profile review-pair artifact `11415094731` (digest `sha256:23193aaaacdb2af7b465e4ddae17428344d1ac1d65d5dcc1b7089cf7bb342fa4`). Issue #474 is closed; #475 owns freeze/tag/publication.

This receipt does **not** modify the current machine marker: the candidate remains `NOT_FROZEN`, `candidate_sha=null`, `UNPUBLISHED` and publication unauthorized until an independent freeze-control PR passes the full required gates. The approved publication source remains the exact earlier SHA even after future documentation/control commits. No v3.0.5 tag or GitHub Release exists yet.


## Phase 10D freeze preflight — 2026-10-10

A fresh remote reconciliation at `main=47f101129316a72815c5e2f0bb1f9223dba5a3eb` confirmed #474 ACCEPT for exact source `407f279a78df3824b27585d0e86d688c19cd90ee`, but identified a publication-metadata blocker before #475 freeze. The accepted source's `release/ctan/README.md` still declares `Release status: Unreleased` and describes 3.0.5 as an unreleased development line. `tools/build-distribution-bundles.py` copies this file verbatim into the CTAN archive. Issue #369 explicitly forbids this status in a frozen/publication-authorized candidate.

**Decision: BLOCKED, fail closed.** No control-plane-only freeze may silently certify these inconsistent publication-source bytes. Editing that README changes the previously accepted source and therefore requires selecting an updated exact source SHA, rerunning complete Static/Linux Integration/Linux Release (including CTAN, reproducibility and distribution) plus Windows/macOS portability certification, regenerating/reviewing the seven profile pairs and obtaining explicit renewed maintainer ACCEPT for the updated source/artifact pair. Existing 10B/10C receipts remain valid historical evidence for the original SHA but are not transferable to changed bytes. No tag/Release/CTAN submission is authorized. The v3.0.4 publication is untouched.

The repository metadata-consistency contract now fails closed if a frozen or publication-authorized 3.0.5 marker retains either stale CTAN README declaration; unfrozen development continues to be explicitly labelled Unreleased. The freeze-control transition and downstream #475 publication work remain pending, and the separate authenticated annotated-tag/Release-asset capability remains a later dependency. Track #475 and #369; do not bypass this by weakening tests or publishing the accepted archive with stale metadata.


## Phase 10D source-metadata correction — 2026-10-10

PR #477 was merged as `57b433bb2525e9776a5e86c7b26b8412b33268eb`. All mandatory exact-merge-SHA post-merge gates passed: Static run `38048287023`, complete Linux Integration `38048286958`, Linux Release `38048287005`. This is a certified prerequisite, not a freeze. At entry, no PR was open.

Issue #369 requires correction of the verbatim CTAN `release/ctan/README.md`. Its version metadata now reads **Prepared for publication**: the source is staged for distribution without falsely claiming GitHub Release or CTAN publication. The earlier 'unreleased maintenance development line' assertion is removed. Metadata and governance tests bind that corrected status to the explicit source-correction stage, preserving a fail-closed release control and immutable v3.0.4 receipt.

**This change creates a new source, not an approved publication candidate.** Historic #474 ACCEPT binds only exact source `407f279a78df3824b27585d0e86d688c19cd90ee` and review artifact `11415094731`; the acceptance cannot carry over to changed package bytes. The release marker stays `NOT_FROZEN`, `candidate_sha=null`, `UNPUBLISHED`, `publication_authorized=false`.

Next gate: Static, complete Linux Integration and Linux Release of the source-correction PR; only after all PASS, merge and recertify the exact new `main` SHA, plus fresh Windows/macOS portability and seven-profile review. Require renewed explicit maintainer ACCEPT on the **new** source and artifacts before a separately certified freeze-control transition. Annotated tag, GitHub Release and CTAN submission remain forbidden until their independent gates and publication capabilities exist. Published v3.0.4 tags and bytes remain immutable.


### Phase 10D source PR #478 — validation iteration

PR #478 head initially `17d13433f450b120016c397897eafbd30a0238b1` failed Static Contract run `38050098273` because `docs/RELEASE-STATE.md` lacked the explicit token `issue #475` required by `phase_governance.py`. The error is retained, not bypassed. Commit `3848be3634d768ec92feeb5aeb158315e6cb807a` repaired the active ownership wording. This follow-up binds the now-assigned PR #478 into machine release metadata and the regression contract, so future CI runs use one consolidated corrected PR head. The required gates are **not yet certified** and this PR must not merge until current head Static, complete Linux Integration and Linux Release are all PASS.

No version tag, GitHub release, CTAN update, runtime/API/template change or acceptance transfer is authorized.
