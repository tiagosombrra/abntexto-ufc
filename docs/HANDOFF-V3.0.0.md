# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `fbf7cc4839ce318024a7d1ed517dd50fab5773ac` |
| Active branch / PR | `feat/v3-scientific-article` / #286 |
| Current-main reconciliation merge | `85cf22b6fe5d117bb2611a2865911e0d20a19363` |
| Active phase | **Scientific Article** |
| Steps 1–5 | **ACCEPTED** |
| Step 6 | **IMPLEMENTED — CI ACCEPTANCE PENDING** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Final Certification | QUEUED |
| Release | QUEUED |

PR #288 corrected the stale root README and canonical main control documents and merged as `fbf7cc4...`. The article branch was immediately reconciled with that new main before Step 6 implementation.

## Step 6 material advance

Step 6 now adds:

- `standards/article-evidence-map.json`, covering exactly all 18 retained article rule IDs;
- `tests/checks/scientific_article_evidence_map.py`, wired into `tests/static.py`;
- explicit evidence dispositions distinguishing required executable support, optional present/absent support, advisory non-enforcing support and source/applicability-only boundaries;
- zero validation-mode promotions: executable support is intentionally not equated with normative proof.

The source-backed 18-rule contract in `standards/coverage-rules-article.json` is unchanged. In particular, recommendations remain manual/non-enforcing and journal precedence remains `required-when-applicable`, `conditional-manual`, with `target-journal-submission` applicability.

## Immediate action

1. publish the synchronized Step 6 technical checkpoint;
2. require Static contract and the Linux scope selected by changed-path policy;
3. classify any failure before modifying predicates;
4. if green, record the Step 6 SHA/run IDs and mark Step 6 accepted;
5. start Step 7 canonical article PDF generation and page-by-page visual review;
6. after Step 7 acceptance, create one immutable Step 8 candidate for Static + **complete** Linux phase-end regression;
7. only then close Scientific Article and activate Final Certification.

## What still blocks V3 completion

- Step 6 acceptance is pending CI.
- Step 7 canonical Scientific Article PDF has not been produced/visually accepted.
- Step 8 Scientific Article complete phase-end regression has not run.
- PR #286 / issue #280 remain open until the phase is accepted.
- Final Certification has not been executed on the final candidate.
- Issue #18 still requires deterministic release-reference-PDF reproducibility with pinned epoch/SOURCE_DATE_EPOCH and hash evidence.
- Release packaging, checksums, tag/release and publication actions remain unexecuted.
- Librarian item 33 remains explicit `NORMATIVE-REVIEW` and fail-closed unless authoritative NBR 6023:2025 evidence becomes available.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete phase-end regression on one immutable SHA. Scoped intermediate checks never authorize a phase transition.
