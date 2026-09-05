# Core Corrections — Phase-end Regression

Updated: 2026-09-05
Status: CANDIDATE-PENDING

## Candidate history

Candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2` is rejected. Static `33981960024` failed only because `release/v3-roadmap.json` changed the governance sentinel from the contractually required `one-immutable-sha` to a descriptive phrase. `tests/checks/phase_governance.py` correctly failed closed with `phase-end regression must bind to one immutable SHA`.

This is a control-plane representation defect, not a LaTeX/runtime, normative, librarian-review, or evidence-predicate failure. The governance test is not weakened.

## Corrected candidate contract

The machine invariant is restored to:

`phase_end_regression.candidate = one-immutable-sha`

The commit that first contains this corrected synchronized state is the new immutable **Core Corrections phase-end regression candidate**. Its exact SHA is obtained from Git after creation and is recorded with workflow results in the later phase-transition commit. The candidate itself is not amended after CI starts.

## Preconditions satisfied

- Front Matter and Annex Closeout checkpoint `6d7a8fb8c7005030f5e1d64a42152d0364fa68c8` passed Static `33980847191` and Linux `33980847189`, `PASS=31 FAIL=0 SKIP=0`.
- Librarian review state is `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.
- Item 33 remains explicit and fail-closed pending authoritative current NBR 6023:2025 evidence.
- No shared runtime FAIL is open.
- Scientific Article runtime remains deferred.

## Required regression gate

The new candidate must pass, on the same immutable SHA:

1. Static contract;
2. full Linux integration;
3. existing phase-specific reviewer evidence;
4. repository, phase-governance and engineering-language guards;
5. canonical reference-document build checks already exercised by Linux integration.

A failure is classified before any correction. Tests must not be weakened to obtain green status.

## Exit rule

Only after Static and Linux are green and their run IDs/conclusions are recorded may Core Corrections be marked `CLOSED` and Reference PDF Validation become `ACTIVE`.
