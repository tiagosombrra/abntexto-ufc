# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Repository state, not conversation memory, is authoritative.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata or publication state:

1. resolve the actual branch, HEAD and `origin/main` dynamically;
2. read `docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md`;
3. read `docs/V3.0.2-BRANCH-HYGIENE-MANIFEST.md` when branch/repository cleanup is involved;
4. inspect issue #313 for the live post-v3.0.1 regression/hygiene program;
5. read `docs/history/v3/control/V3.0.1-DOCUMENT-LIFECYCLE.md` only for historical lifecycle classification and retained v3.0.1 evidence;
6. use older v3/v3.0.1 roadmap, recovery, certification and release documents as historical evidence unless the v3.0.2 status explicitly promotes one to current policy.

Priority on disagreement: **current Git facts > current v3.0.2 status/issue #313 > current technical policy > retained v3.0.1 evidence > older v3 documents > prior chat or memory**.

## Current development state

| Fact | Current state |
|---|---|
| Published/frozen baseline | `v3.0.1`; immutable historical release bytes |
| Current development line | `v3.0.2` |
| Canonical branch | `main`; resolve SHA dynamically |
| Repository lifecycle | Post-cleanup steady state; `main` is canonical and transient PR branches must be removed after merge |
| Tracking issue | #313 |
| TOC References/Glossary correction | DONE; merged through PR #314 |
| Branch hygiene | DONE; 185 non-`main` refs physically pruned on 2026-09-13; manifest retains the forensic pre-pruning snapshot |
| Workflow lifecycle | four permanent workflows KEEP |
| Tool lifecycle | automated/release tools KEEP; three PowerShell scripts KEEP as documented manual Windows support |
| Documentation cleanup | DONE; active docs/release state consolidated and post-cleanup status reconciled |
| Full post-cleanup regression | DONE technically on `main@5c8919498e01ccbfee1d3891a254d03527dcceea`; maintainer visual acceptance remains a separate release gate |
| v3.0.2 publication | NOT AUTHORIZED; release marker remains `NOT_FROZEN` until explicit maintainer visual acceptance and P8 preparation |

The `v3.0.1` tag/release/CTAN-submission bytes must never be rewritten. Any post-release correction belongs to a later version.

## Progress documentation discipline

A material advance changes runtime, evidence, repository lifecycle, validation state or release readiness. Every material advance must update `docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md` and the applicable durable policy/evidence in the same work cycle; issue #313 carries live operational receipts when a source commit would be inappropriate.

A material lot must leave an exact changed-file record or unambiguous commit/PR diff, executed checks with classification, and unresolved findings carried forward explicitly. Failed checks remain part of the audit trail after successful reruns; do not rewrite history to make the sequence look green.

## Canonical TCC/reference rules

The canonical undergraduate reference is rooted at `template/main.tex`. It is both a user-facing commented guide and a regression/reference corpus. The seven chapter files remain sequential and semantically named.

The guide distinguishes ABNT normative requirements, UFC institutional requirements, project/editorial policy, and examples/recommendations. For each major user-visible formatting or document-structure topic, it explains authority/classification, expected rendered behavior, the public `abntexto-ufc` mechanism and the validation/evidence route. The machine normative contract remains authoritative for atomic proof semantics.

R1.3 closed on source SHA `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa` with Static #484 PASS and Linux #405 `reference-document` PASS (`PASS=3 FAIL=0 SKIP=0`). Detailed failed development runs remain in `docs/history/v3/evidence/v3.0.1/V3.0.1-R1.3-EVIDENCE.md`.

## Canonical reference artifact rule

R2 reuses `tests/integration/release-reference-reproducibility.sh`; do not create a competing source-tree reference generator. R2 accepted implementation SHA `514c128f542b00d4a10a9ad05ce7fc94f770ef55`: Static #486 PASS, Linux #407 `smoke` PASS, Linux Release Check #121 `complete` PASS, and dedicated artifact/provenance verification PASS. The canonical engineering PDF SHA-256 is `bd8964c8a37940924758d44eef61bc079f5101cf25cd180b42c3df22e00d1d3a`; all 63 pages were inspected as development evidence. See `docs/history/v3/evidence/v3.0.1/V3.0.1-R2-EVIDENCE.md`.

That source-tree PDF is not automatically a distributable public PDF because the canonical source may use a locally configured UFC mark. R3 owns the public sanitized PDF route.

## R3 public distribution rule

Keep the small CTAN example and the complete pedagogical reference as different artifact roles. The full public reference PDF must be generated from the exact sanitized `main.tex` and runtime distributed in the template/Overleaf bundle; never copy the R2 source-tree PDF into public bundles.

Public source must have `coat-of-arms=false`, no UFC mark asset, and no proprietary Microsoft font files. Extend the existing `tools/build-public-bundles.py` / `tools/build-distribution-bundles.py` pipeline rather than adding a parallel release generator. Distribution regression must extract each public bundle, rebuild its exact source deterministically and compare the rebuilt PDF SHA-256 with the embedded full-reference PDF. Cross-bundle byte identity may only be asserted after measured proof.

The CTAN archive stays lean by default and retains `docs/ctan-example.tex` as its minimal example; adding the full TCC to CTAN requires concrete packaging evidence, not convenience.

## R3 accepted public distribution

R3 accepted corrective source `2556489da23e16495fc51ebf093f9f4704c6d52f`. Static #489 PASS, Linux Integration #410 `distribution` PASS, and Linux Release Check #124 complete PASS on that SHA. The exact distribution artifact `10169809155` has archive digest `sha256:6445ce5e3b870fc6c418fa23c4dc318576f58d00bfe48525ed100e86feaca761`; its three inner ZIPs validate against `SHA256SUMS`. Template and Overleaf embed byte-identical 63-page public references with SHA-256 `e92378a0ef01310c656599d1f1765db6d0040467367313e74776c8ebd75b766c`, while CTAN excludes the full reference. Independent inspection confirmed `coat-of-arms=false`, no prohibited institutional-mark asset, no proprietary Microsoft font, A4 output and visually intact pages. See `docs/history/v3/evidence/v3.0.1/V3.0.1-R3-EVIDENCE.md`.

## R4 accepted Web/Lite boundary

R4 accepted source `170fec009cc89ec0ca98d8d627cd4c8fb3e8447b`. Static #495 PASS. Linux #416 selected `web-lite`, passed `SCOPE=web-lite PASS=3 FAIL=0 SKIP=0`, then drove the productive `validator/index.html` UI in Chrome 152 with the real 63-page reference PDF and a valid non-A4 negative PDF. The positive input passed readable/A4/margins without top-level FAIL; the negative input failed A4 with verdict FAIL; `font.embedded` and `pdfa.deep` remained `MANUAL REVIEW`. Artifact `10182427862` was independently downloaded and its JSON/log inspected. Release #130 also passed `SCOPE=complete PASS=38 FAIL=0 SKIP=0` with current `pkgcheck 4.1.0`. Detailed failed harness iterations #412/#413/#414 and non-closing #415 remain in `docs/history/v3/evidence/v3.0.1/V3.0.1-R4-EVIDENCE.md`.

## Historical v3.0.1 release evidence

The v3.0.1 publication cycle is closed historical evidence. Its machine state is retained under `release/history/v3/`, its publication guide under `docs/history/v3/release/CTAN-RELEASE-v3.0.1.md`, and its document lifecycle under `docs/history/v3/control/V3.0.1-DOCUMENT-LIFECYCLE.md`.

Do not reactivate v3.0.1 branches, roadmaps, recovery plans or candidate semantics as current authority.

## Active release-marker policy

There is exactly one active release marker path: `release/v3-release-candidate.json`.

During ordinary v3.0.2 development it must remain:

- `candidate_state = NOT_FROZEN`;
- `candidate_sha = null`;
- `publication_authorized = false`;
- bound to issue #313 and the current v3.0.2 status document.

Changing the active marker is a deliberate release-control event and must force complete Linux Integration. Historical machine state under `release/history/v3/` must never trigger candidate semantics.

## Future release invariant

A future release candidate must bind technical certification, generated artifacts, maintainer visual acceptance, tag and publication bytes to one immutable source SHA:

```text
certified source SHA == visually approved source SHA == tagged source SHA == source SHA of published release bytes
```

No tracked commit or asset rebuild is permitted between final human acceptance and tagging/publication. Published v3.0.0 and v3.0.1 tags/assets remain immutable historical facts.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for R6 explicit maintainer visual approval.
