# Core Corrections — Phase-end Regression

Updated: 2026-09-05
Status: CLOSED

## Accepted candidate

Immutable candidate `5f67560aeded1e6b4f77f4a31e14a91f3181a4da` closed Core Corrections.

- Static contract `33982156041`: SUCCESS.
- Full Linux integration `33982156042`: SUCCESS.
- Linux validation summary: `PASS=31 FAIL=0 SKIP=0`.
- Repository/phase-governance/engineering-language guards: PASS.
- Existing phase-specific reviewer evidence remained green.
- No shared runtime FAIL was opened.
- Librarian review remained `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW`.

The candidate was not amended after CI began.

## Evidence retained from Linux

The accepted Linux run re-exercised the complete 31-check PR contract, including reference document, layout, front matter, object geometry, code typography, documentary sources, bibliography, research-project profiles, back matter, build path and normative evidence contribution.

Explicit reviewer evidence remained present for the resolved review surfaces, including items 1, 2, 7, 11, 16, 19, 20, 23, 28, 30, 31, 32 and 34. The run ended with no FAIL or SKIP.

## Candidate history

Candidate `3b2476371e1df5180d8ee25ea53aed6a13fa2da2` is rejected. Static `33981960024` failed because `release/v3-roadmap.json` had replaced the contractually required `one-immutable-sha` governance sentinel with descriptive text. `tests/checks/phase_governance.py` correctly failed closed.

That was a control-plane representation defect, not a LaTeX/runtime, normative, librarian-review, or evidence-predicate failure. The governance test was not weakened.

Candidate `5f67560a...` restored:

`phase_end_regression.candidate = one-immutable-sha`

and then passed the complete phase-end gate.

## Authority boundary at closure

Review item 33 remains explicit and fail-closed pending authoritative current NBR 6023:2025 evidence. Core Corrections closure does not reinterpret that unresolved authority item as PASS and does not authorize speculative bibliography runtime changes.

## Closure decision

Core Corrections is CLOSED. Reference PDF Validation is ACTIVE under `docs/V3-REFERENCE-PDF-VALIDATION.md`.

Scientific Article remains deferred until the canonical V3 PDF passes complete page-level presentation validation and the Reference PDF Validation phase-end regression.
