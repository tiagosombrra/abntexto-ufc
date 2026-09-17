# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Repository state, not conversation memory, is authoritative.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata or publication state:

1. resolve the actual branch, HEAD and `origin/main` dynamically;
2. read `docs/V3.0.3-DISTRIBUTION-CORRECTION.md` for the active corrective line;
3. read `docs/V3.0.2-BRANCH-HYGIENE-MANIFEST.md` only when branch/repository cleanup history is involved;
4. inspect issue #328 for the live v3.0.3 corrective program and issue #313 for the still-processing v3.0.2 CTAN publication receipt;
5. read `docs/history/v3/control/V3.0.1-DOCUMENT-LIFECYCLE.md` only for historical lifecycle classification and retained v3.0.1 evidence;
6. use older v3/v3.0.1/v3.0.2 roadmap, recovery, certification and release documents as historical evidence unless the current v3.0.3 status explicitly promotes one to current policy.

Priority on disagreement: **current Git facts > active v3.0.3 marker/status/issue #328 > current technical policy > retained historical evidence > older v3 documents > prior chat or memory**.

## Current development state

| Fact | Current state |
|---|---|
| Published/frozen baseline | `v3.0.2`; GitHub Release published from immutable certified bytes; CTAN submission processing independently |
| Current development line | `v3.0.3` |
| Canonical branch | `main`; resolve SHA dynamically |
| Repository lifecycle | Post-cleanup steady state; `main` is canonical and transient PR branches must be removed after merge |
| v3.0.2 publication tracking | #313 |
| v3.0.3 corrective tracking | #328 / PR #329 |
| Branch hygiene | DONE; historical branch inventory was pruned and automatic merged-branch deletion is enabled |
| Workflow lifecycle | four permanent workflows KEEP |
| Tool lifecycle | automated/release tools KEEP; three PowerShell scripts KEEP as documented manual Windows support |
| Full v3.0.2 regression | DONE for exact frozen candidate `3a0904324e23bfc65852d730f2647ce47dc65105` |
| v3.0.2 publication | GitHub Release COMPLETE; exact CTAN archive submitted 2026-09-17; do not rebuild or replace published/submitted bytes |
| v3.0.3 distribution correction | ACTIVE; Template/Overleaf carry the UFC coat of arms while CTAN remains sanitized |
| v3.0.3 candidate state | `NOT_FROZEN`; no candidate SHA; publication not authorized |

The `v3.0.1` and `v3.0.2` tags/releases/publication bytes must never be rewritten. Any post-release correction belongs to a later version.

## Progress documentation discipline

A material advance changes runtime, evidence, repository lifecycle, validation state or release readiness. Every material advance must update the applicable durable policy/evidence in the same work cycle; issue #328 carries v3.0.3 operational receipts and issue #313 carries v3.0.2 CTAN publication receipts.

A material lot must leave an exact changed-file record or unambiguous commit/PR diff, executed checks with classification, and unresolved findings carried forward explicitly. Failed checks remain part of the audit trail after successful reruns; do not rewrite history to make the sequence look green.

## Canonical TCC/reference rules

The canonical undergraduate artifact is rooted at `template/main.tex` and is a compact TCC tutorial, not the exhaustive API/normative manual. Its five sequential chapter files are:
`1-introduction.tex`, `2-theoretical-background.tex`, `3-methodology.tex`, `4-results.tex`, and `5-conclusion.tex`.

Learning responsibilities are separated fail-closed: `template/` teaches by realistic use; `docs/USER-GUIDE.md` explains the workflow and normative/institutional context; `docs/COMMAND-REFERENCE.md` exhaustively documents the public configuration/command/environment surface; `standards/` owns machine normative traceability; and `tests/` owns exhaustive regression cases. Do not re-expand the TCC merely to carry test coverage or maintainer documentation. The canonical tutorial PDF is budgeted at 15–35 pages by the integration gate.

## Canonical reference artifact rule

The source-tree canonical reference may use the UFC coat of arms. For the current v3.0.3 line, Template and Overleaf bundles must preserve that behavior and include exactly `assets/institutional/ufc-coat-of-arms.png`. CTAN is the intentionally sanitized surface and must remain free of institutional mark assets.

## User-bundle / CTAN distribution rule

Keep the small CTAN example and the compact TCC tutorial as different artifact roles.

The distribution contract is fail-closed and surface-specific:

- **CTAN:** no UFC coat-of-arms asset, no proprietary Microsoft font files, and the minimal CTAN example uses `coat-of-arms=false`;
- **Template:** include exactly `assets/institutional/ufc-coat-of-arms.png`, preserve canonical `coat-of-arms=true`, and embed a reference PDF generated from that exact source;
- **Overleaf:** include the same institutional PNG, preserve canonical `coat-of-arms=true`, include the pinned `abntexto.cls`, and embed the same reference PDF;
- no distribution surface may contain proprietary Microsoft font files.

Extend the existing `tools/build-public-bundles.py` / `tools/build-distribution-bundles.py` pipeline rather than adding a competing release generator. Distribution regression must extract each user bundle, rebuild its exact source deterministically and compare the rebuilt PDF SHA-256 with the embedded full-reference PDF. Cross-bundle byte identity may only be asserted after measured proof.

The CTAN archive stays lean by default and retains `docs/ctan-example.tex` as its minimal example; adding the full TCC or an institutional mark to CTAN requires an explicit future policy decision and concrete packaging evidence.

## Historical release evidence

Historical v3.0.1 and v3.0.2 release-control state is retained under `release/history/v3/`. The v3.0.2 frozen snapshot is `release/history/v3/v3.0.2-release-candidate.json`.

Do not reinterpret historical sanitized Template/Overleaf evidence from earlier releases as the current v3.0.3 user-bundle policy.

## Active release-marker policy

There is exactly one active release marker path: `release/v3-release-candidate.json`.

The current v3.0.3 state is:

- `development_line = 3.0.3`;
- `target_version = 3.0.3`;
- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_authorized = false`;
- tracking issue #328;
- authority `docs/V3.0.3-DISTRIBUTION-CORRECTION.md`.

Changing the active marker is a deliberate release-control event and must force complete Linux Integration. Historical machine state under `release/history/v3/` must never trigger candidate semantics.

The v3.0.2 CTAN submission may finish processing while v3.0.3 development continues. v3.0.3 may not be submitted to CTAN until v3.0.2 has been accepted/published.

## Future release invariant

A future release candidate must bind technical certification, generated artifacts, maintainer visual acceptance, tag and publication bytes to one immutable source SHA:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published release bytes
```

No candidate-source or publication-byte change, amendment or rebuild is permitted between final human acceptance and tagging/publication. Published v3.0.0, v3.0.1 and v3.0.2 tags/assets remain immutable historical facts.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for explicit maintainer visual approval.
