# abntexto-ufc v3.0.0 — Engineering Roadmap

Updated: 2026-09-05

## Current status

**Core Corrections is ACTIVE and in phase-end regression preparation.**

Accepted checkpoints:

- object/Core: `3f47081cbbd00a44b9ee86a6b406580e79b593c0`, Static `33965794475`, Linux `33965794519`;
- canonical reference content: `c4c59f83b67cb152ed9a88345541457b8f18021c`, Static `33969505681`, Linux `33969505614`;
- engineering-language hardening: `edeb14b7a96d1cab3ad9551701087ddf4dff059a`, Static `33972111694`, Linux `33972111696`;
- bounded reference evidence: `bcd851b3176b516091a254bc57b5ae4e8add9358`, Static `33974062993`, Linux `33974063103`;
- front matter and annex closeout: `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8`, Static `33980847191`, Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`.

Current review state is **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**. Item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

Machine authority: `release/v3-roadmap.json`.
Canonical handoff: `docs/HANDOFF-V3.0.0.md`.
Correction queue: `docs/V3-CORRECTION-PLAN.md`.
Librarian review: `docs/UFC-LIBRARIAN-REVIEW.md`.

## Operating discipline

Every **material advance** must update the relevant execution documentation and canonical handoff in the same work cycle. Changes to phase state, acceptance state, evidence state, current correction batch, or branch/checkpoint facts must also update this roadmap and `release/v3-roadmap.json`.

Every phase ends with a mandatory **phase-end regression** on one immutable candidate SHA. Targeted checks accumulated during a phase do not replace this gate.

## Phase plan

| Phase | Status | Goal | Exit gate |
|---|---|---|---|
| **Regression Audit** | CLOSED | Revalidate the shared V3 foundation and classify recovered review requirements and newly discovered defects. | 34-item contract plus green Static/full Linux phase-end regression. |
| **Core Corrections** | ACTIVE — CLOSEOUT | Correct shared runtime, template, normative mapping, documentation and tests identified by the audit. | No unresolved shared FAIL; blocking evidence complete; authority gaps explicit/fail-closed; phase-end regression green on one immutable SHA. |
| **Reference PDF Validation** | QUEUED | Inspect the corrected canonical V3 PDF page by page against accepted UFC requirements, recovered reviews and preservation baseline. | Visual checklist and reproducible presentation evidence pass; phase-end regression green. |
| **Scientific Article** | QUEUED | Implement the article profile on the corrected shared foundation. | Article runtime/evidence/rendering and phase-end regression pass. |
| **Final Certification** | QUEUED | Complete profile/engine/literal-font/Unicode/embedding/PDF-A/distribution certification. | Heavy certification matrix and phase-end regression green on one SHA. |
| **Release** | QUEUED | Finalize documentation, bundles, release assets, checksums and publication actions. | Release checklist complete and final regression recorded. |

## Active phase — Core Corrections

### Validated work

- readable control plane and machine-protected 34-item review contract;
- documentation-on-material-advance and phase-end regression governance;
- front-matter advisor/co-advisor, department, complete-author and committee evidence;
- citation/locator/body/list corrections and evidence;
- object typography authority/runtime/evidence;
- canonical source/PDF evidence for items 11, 16 and 28;
- engineering-language hardening accepted and retained as a permanent guard;
- bounded bibliography evidence for items 30-32 accepted;
- annex source/heading/TOC closeout accepted.

### Review-contract closeout

Linux `33980847189` emitted PASS evidence for items 1, 2, 7 and 34. Together with prior accepted batches, the matrix is now **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW**.

Item 33 is not a runtime FAIL. It is an explicit authority gap and remains fail-closed. No speculative runtime change is allowed.

### Current work — Phase-end regression preparation

The next commit after this acceptance-state synchronization must be a separate immutable **Core Corrections phase-end candidate**. That candidate must preserve the accepted runtime/evidence state and pass Static contract plus full Linux integration on the same SHA.

No phase transition occurs until the candidate result is recorded.

## Gate before Reference PDF Validation

No shared runtime FAIL; all blocking P0/P1 corrections have accepted evidence; item 33 is explicit and fail-closed; documentation/machine state match the candidate; one immutable candidate passes the complete Core Corrections phase-end regression.

## Gate before Scientific Article

Scientific Article starts only after Core Corrections closes and the corrected canonical V3 reference PDF passes Reference PDF Validation and its own phase-end regression.

## Naming policy

Use descriptive work names. Do not create new opaque nested letter/number identifiers. GitHub issue/PR numbers and immutable SHAs provide traceability.
