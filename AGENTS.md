# AGENTS.md — Repository Bootstrap and Control Rules

This repository uses fail-closed state reconciliation. Repository state, not conversation memory, is authoritative.

## Mandatory session bootstrap

Before changing code, tests, standards, workflows, documentation, release metadata or publication state:

1. resolve the actual branch and HEAD from Git and resolve `origin/main` dynamically;
2. read `docs/V3-CONTINUATION.md` first;
3. read `release/v3.0.1-final-corrections.json`;
4. read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`;
5. read the evidence document for the active lot. R1 evidence is under `docs/V3.0.1-R1*.md`, R2 uses `docs/V3.0.1-R2-EVIDENCE.md`, R3 uses `docs/V3.0.1-R3-EVIDENCE.md`, R4 uses `docs/V3.0.1-R4-EVIDENCE.md`, and the current active lot R5 uses `docs/V3.0.1-R5-EVIDENCE.md`;
6. inspect issue #304 and PR #305 when remote GitHub state is available;
7. use older v3 roadmap, recovery and certification documents only as historical/background evidence when the current handoff or machine state points to them.

Priority on disagreement: **current Git facts > active machine state > current continuation handoff > active-lot evidence > older documents > prior chat or memory**.

## Current release-correction state

| Fact | Current state |
|---|---|
| Target | `3.0.1` |
| Active phase | Release |
| Canonical branch | `main`; always resolve current SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; evidence only, superseded as final candidate |
| Active correction branch | `fix/v3.0.1-approval-page` |
| Tracking issue / PR | #304 / #305 merged historical; active correction PR #311 |
| Publication | BLOCKED until R6 |
| R0 | DONE — auditable control plane |
| R1 | DONE — canonical source identity, coverage and coherent pedagogical TCC |
| R2 | DONE — exact-SHA full canonical engineering PDF artifact and provenance |
| R3 | DONE — sanitized public reference embedded and independently inspected |
| R4 | DONE — static package and productive real-PDF Chrome E2E accepted |
| R5 | ACTIVE_POST_MERGE_CORRECTION — approval-page fix requires fresh complete PR + exact-main recertification |
| R6 | PENDING — maintainer acceptance and publication |
| Public `v3.0.0` | historical/superseded; never silently retarget |

Never treat a SHA copied from this document as current Git state; resolve the branch dynamically first.

## Progress documentation discipline

A material advance changes runtime, evidence, certification/release result, active-lot acceptance state, artifact provenance, reproducibility state, candidate transport, tag/release state or publication readiness. Every material advance must update the affected machine state, lot evidence and `docs/V3-CONTINUATION.md` in the same work cycle.

A material lot must leave an exact changed-file record or unambiguous commit/PR diff, executed checks with classification, and unresolved findings carried forward explicitly. Failed checks remain part of the audit trail after successful reruns; do not rewrite history to make the sequence look green.

## Canonical TCC/reference rules

The canonical undergraduate reference is rooted at `template/main.tex`. It is both a user-facing commented guide and a regression/reference corpus. The seven chapter files remain sequential and semantically named.

The guide distinguishes ABNT normative requirements, UFC institutional requirements, project/editorial policy, and examples/recommendations. For each major user-visible formatting or document-structure topic, it explains authority/classification, expected rendered behavior, the public `abntexto-ufc` mechanism and the validation/evidence route. The machine normative contract remains authoritative for atomic proof semantics.

R1.3 closed on source SHA `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa` with Static #484 PASS and Linux #405 `reference-document` PASS (`PASS=3 FAIL=0 SKIP=0`). Detailed failed development runs remain in `docs/V3.0.1-R1.3-EVIDENCE.md`.

## Canonical reference artifact rule

R2 reuses `tests/integration/release-reference-reproducibility.sh`; do not create a competing source-tree reference generator. R2 accepted implementation SHA `514c128f542b00d4a10a9ad05ce7fc94f770ef55`: Static #486 PASS, Linux #407 `smoke` PASS, Linux Release Check #121 `complete` PASS, and dedicated artifact/provenance verification PASS. The canonical engineering PDF SHA-256 is `bd8964c8a37940924758d44eef61bc079f5101cf25cd180b42c3df22e00d1d3a`; all 63 pages were inspected as development evidence. See `docs/V3.0.1-R2-EVIDENCE.md`.

That source-tree PDF is not automatically a distributable public PDF because the canonical source may use a locally configured UFC mark. R3 owns the public sanitized PDF route.

## R3 public distribution rule

Keep the small CTAN example and the complete pedagogical reference as different artifact roles. The full public reference PDF must be generated from the exact sanitized `main.tex` and runtime distributed in the template/Overleaf bundle; never copy the R2 source-tree PDF into public bundles.

Public source must have `coat-of-arms=false`, no UFC mark asset, and no proprietary Microsoft font files. Extend the existing `tools/build-public-bundles.py` / `tools/build-distribution-bundles.py` pipeline rather than adding a parallel release generator. Distribution regression must extract each public bundle, rebuild its exact source deterministically and compare the rebuilt PDF SHA-256 with the embedded full-reference PDF. Cross-bundle byte identity may only be asserted after measured proof.

The CTAN archive stays lean by default and retains `docs/ctan-example.tex` as its minimal example; adding the full TCC to CTAN requires concrete packaging evidence, not convenience.

## R3 accepted public distribution

R3 accepted corrective source `2556489da23e16495fc51ebf093f9f4704c6d52f`. Static #489 PASS, Linux Integration #410 `distribution` PASS, and Linux Release Check #124 complete PASS on that SHA. The exact distribution artifact `10169809155` has archive digest `sha256:6445ce5e3b870fc6c418fa23c4dc318576f58d00bfe48525ed100e86feaca761`; its three inner ZIPs validate against `SHA256SUMS`. Template and Overleaf embed byte-identical 63-page public references with SHA-256 `e92378a0ef01310c656599d1f1765db6d0040467367313e74776c8ebd75b766c`, while CTAN excludes the full reference. Independent inspection confirmed `coat-of-arms=false`, no prohibited institutional-mark asset, no proprietary Microsoft font, A4 output and visually intact pages. See `docs/V3.0.1-R3-EVIDENCE.md`.

## R4 accepted Web/Lite boundary

R4 accepted source `170fec009cc89ec0ca98d8d627cd4c8fb3e8447b`. Static #495 PASS. Linux #416 selected `web-lite`, passed `SCOPE=web-lite PASS=3 FAIL=0 SKIP=0`, then drove the productive `validator/index.html` UI in Chrome 152 with the real 63-page reference PDF and a valid non-A4 negative PDF. The positive input passed readable/A4/margins without top-level FAIL; the negative input failed A4 with verdict FAIL; `font.embedded` and `pdfa.deep` remained `MANUAL REVIEW`. Artifact `10182427862` was independently downloaded and its JSON/log inspected. Release #130 also passed `SCOPE=complete PASS=38 FAIL=0 SKIP=0` with current `pkgcheck 4.1.0`. Detailed failed harness iterations #412/#413/#414 and non-closing #415 remain in `docs/V3.0.1-R4-EVIDENCE.md`.

## Canonical approval-page release rule

The canonical reference approval page uses `12 de setembro de 2026` and exactly three committee people: advisor, examiner 2 and examiner 3. Every committee signature block renders only member name and institution. Department, center, program or other unit metadata must not render in the committee block, and advisor/coadvisor role suffixes must not be appended there. Legacy unit metadata keys remain accepted for compatibility.

PR #305's squash result `ab641d49c5f6a79ff54a16a78d1946a6e008fe6d` violated this rule and is invalidated as a final v3.0.1 candidate. Active correction branch is `fix/v3.0.1-approval-page`. Never tag/publish `ab641d49...`.

## R5 dynamic candidate transport

R5 uses exactly one release marker: `release/v3-release-candidate.json`. A marker change must force complete Linux Integration on PR #305; after those pre-merge gates pass, PR #305 is squash-merged to `main`. The squash SHA is resolved dynamically from Git and must pass Static, automatic complete Linux Integration (including the Web/Lite host E2E) and Linux Release Check/current CTAN `pkgcheck` again.

The R5 source documents are deliberately written as a dynamic state machine so they remain valid across the squash merge without a documentation commit that would change the candidate SHA. After the exact `main` candidate is certified, do not commit merely to record its SHA before R6/tag/publication; use immutable GitHub run/artifact facts and issue #304 as the live receipt, then write final repository receipts only after publication bytes are frozen.

## Mandatory phase-end regression and release invariant

Targeted R1–R4 checks are development evidence only. R5 must bind the complete applicable release matrix to one immutable exact SHA. R6 then requires explicit maintainer visual approval of artifacts from that same SHA.

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 human acceptance and before tagging/publication. Existing `v3.0.0` bytes remain untouched. CTAN receives only the canonical `abntexto-ufc-3.0.1.zip` frozen by R5.

## Deferred post-v3.0.1 work

Whole-repository lifecycle classification, broad branch pruning, broad historical-document consolidation, unrelated runtime/API refactors and deletion of utilities without direct release-defect evidence remain deferred until after v3.0.1.

## Fail-closed rule

If a required fact cannot be established from current Git state, active machine state, current evidence or reviewed source material, record the ambiguity and stop that advancement. Automated success never substitutes for R6 explicit maintainer visual approval.
