# V3 Continuation Handoff — v3.0.1 final corrections

Updated: 2026-09-11
Status: RELEASE — R0/R1/R2/R3/R4 DONE; R5 REOPENED_CANONICAL_REVIEW; publication blocked

This is the shortest safe entry point for a new ChatGPT/Codex conversation or a maintainer returning to the repository. Do not reconstruct current state from chat history.

## Start here

1. Resolve the actual branch, HEAD and `origin/main` from Git.
2. Read `AGENTS.md`.
3. Read this file.
4. Read `release/v3.0.1-final-corrections.json`.
5. Read `docs/V3.0.1-FINAL-CORRECTION-PLAN.md`.
6. For the active lot R5, read `docs/V3.0.1-R5-EVIDENCE.md`.
7. Continue from `current_next_action` in the machine state.

Current Git facts override the machine state; the machine state overrides this handoff; lot evidence overrides older phase/recovery documents. Prior conversation memory is lowest priority.

## Canonical state

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; resolve SHA dynamically |
| Historical certified baseline | `111680cd934a4ea55b02f6ffe730ff5260077565`; retained as evidence, superseded as final candidate |
| Active branch | `release/v3.0.1-canonical-review-corrections` |
| Tracking issue / PR | #304 / resolve current open PR from active branch (`#305` is historical merged transport) |
| PR state | current canonical-review correction PR must remain unmerged until fresh Stage A passes |
| Target | `v3.0.1` |
| Publication | BLOCKED until R6 |
| Public `v3.0.0` | historical/superseded; never retarget |

## R0/R1 — DONE

R0 established the auditable correction control plane. R1 normalized the seven canonical chapter paths, established pedagogical/normative coverage and completed the coherent teaching rewrite.

R1.3 acceptance source: `704cedaa9960b87ae6035ac08fa4cc4c286ea9aa`.

- Static #484 (`34488189988`): PASS.
- Linux #405 (`34488190044`): PASS.
- Linux scope: `reference-document`.
- Summary: `PASS=3 FAIL=0 SKIP=0`.

Detailed earlier failures and corrections remain in `docs/V3.0.1-R1.3-EVIDENCE.md`.

## R2 — DONE

R2 makes the complete PDF rooted at `template/main.tex` a first-class exact-SHA engineering release reference. Acceptance source: `514c128f542b00d4a10a9ad05ce7fc94f770ef55`.

- Static #486 (`34491624099`): PASS.
- Linux #407 (`34491624073`): PASS, `SCOPE=smoke PASS=4 FAIL=0 SKIP=0`.
- Linux Release Check #121 (`34491624158`): PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.
- CTAN `pkgcheck 4.1.0`: PASS in the same release run.
- Canonical PDF SHA-256: `bd8964c8a37940924758d44eef61bc079f5101cf25cd180b42c3df22e00d1d3a`.
- Two independent clean builds are byte-identical; font embedding, portable CLI/Deep validation, PDF/A-2b and Unicode extraction are PASS.
- Dedicated artifact: `abntexto-ufc-v3.0.1-canonical-reference-34491624158`, id `10158771936`, archive digest `sha256:0677b776c3eb3a358f91a06119973a00b8f3aa8ade841d54565f85fe5db53bc7`.
- The exact 63-page A4 PDF was rendered and inspected page by page; no clipping, overlap, broken glyphs, black boxes or missing structural blocks were observed.

The R2 visual inspection is development evidence only; it does not replace R6 explicit maintainer acceptance on the final immutable R5 candidate. Full evidence: `docs/V3.0.1-R2-EVIDENCE.md`.

## R3 — DONE

R3 repairs public distribution so users receive the complete editable source and a compiled full pedagogical reference while CTAN remains lean.

The implementation commit containing this handoff must be resolved dynamically from the active branch. It introduces:

- generated public filename `abntexto-ufc-reference.pdf`;
- deterministic compilation by `tools/build-public-bundles.py` from the exact public `main.tex` sanitized to `coat-of-arms = false`;
- the same generated reference PDF embedded in template and Overleaf bundles;
- no full reference PDF in the CTAN archive, whose minimal example remains separate;
- an extracted-bundle gate that independently rebuilds template and Overleaf projects and requires rebuilt SHA-256 == embedded PDF SHA-256;
- fail-closed checks for no institutional mark assets, no proprietary Microsoft fonts and correct public mark disablement;
- first-class PR integration suite `distribution`, with release-mode distribution execution still owned by `make release-check` to avoid duplicate execution.

`tools/build-distribution-bundles.py` is intentionally unchanged because it already delegates usage-bundle generation to `tools/build-public-bundles.py`.

Accepted corrective source: `2556489da23e16495fc51ebf093f9f4704c6d52f`.

- Static #489: PASS.
- Linux #410: PASS, `SCOPE=distribution PASS=1 FAIL=0 SKIP=0`.
- Linux Release Check #124: PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`.
- CTAN `pkgcheck 4.1.0`: PASS.
- Exact distribution artifact id `10169809155`, digest `sha256:6445ce5e3b870fc6c418fa23c4dc318576f58d00bfe48525ed100e86feaca761`.
- Release public-reference SHA-256 `e92378a0ef01310c656599d1f1765db6d0040467367313e74776c8ebd75b766c`, identical in Template/Overleaf, 63 A4 pages.
- Independent archive/hash/content and page-by-page visual inspection: PASS.
- CTAN excludes the full reference; distributed source uses `coat-of-arms=false`; no prohibited mark/font files were found.

The first implementation failures #409/#123 and their causes remain retained in `docs/V3.0.1-R3-EVIDENCE.md`.

## R4 — DONE

Accepted source: `170fec009cc89ec0ca98d8d627cd4c8fb3e8447b`.

- Static #495: PASS.
- Linux #416: PASS, `SCOPE=web-lite PASS=3 FAIL=0 SKIP=0`.
- Real Chrome productive-UI E2E: PASS on 63-page positive reference and valid Letter negative.
- Positive SHA-256: `416bd08e184d5510d2dc1c7ab6ebd872c4175dfc20373f040c6c950d09d5a4fb`; readable/A4/margins PASS; no top-level FAIL.
- Negative SHA-256: `83943b2406b0b9f6d0ec00f997606b6c7d73903bbad3b7b8d8e0ce891e9dafdf`; readable PASS, A4 FAIL, verdict FAIL.
- Deep-only `font.embedded` and `pdfa.deep`: `MANUAL REVIEW` on both inputs.
- Browser artifact id `10182427862`, digest `sha256:62d558b681d7181b1726604cdebb25f8f1d7db627e473a16ac986951037c02c9`; independently downloaded/inspected.
- Release #130: PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, current CTAN `pkgcheck 4.1.0` PASS.

Failures #412/#413/#414 and non-closing green #415 remain in `docs/V3.0.1-R4-EVIDENCE.md`.

## R5 — REOPENED BY MAINTAINER CANONICAL REVIEW

R5 uses only `release/v3-release-candidate.json` as its phase-end marker. The previous marker head `c21ffe45f8c8ce5025ff636e0d10a0e67c72964f` had Static #496, Linux #417 and Release Check #131 green, but maintainer inspection on 2026-09-11 found four user-facing canonical defects. That head is therefore superseded as the final candidate.

The corrective batch changes `template/main.tex` and canonical chapters, removes the empty `\toclabelbox{}` from unnumbered References/Glossary/Index TOC entries in project runtime, updates reference regressions, and requires a fresh complete R5 Stage A. The canonical index remains documented and supported by the class but is not printed or populated in the canonical TCC. Once the new exact PR head passes Stage A, squash-merge the current canonical-review correction PR, resolve the resulting `main` SHA dynamically and require the automatic exact-main cycle.

Do not commit merely to record the post-merge SHA or green results before tag/publication; that would invalidate the candidate. The tracked dynamic procedure in `docs/V3.0.1-R5-EVIDENCE.md` remains the bootstrap authority, while immutable GitHub runs/artifacts and issue #304 carry live receipts until publication.

## R6 — PENDING

R5 is the mandatory complete exact-SHA phase-end release regression on the final canonical `main` candidate after R3/R4 closure and correction-PR merge. R6 is explicit maintainer visual acceptance and publication. The invariant remains:

```text
certified source SHA == visually approved source SHA == tagged v3.0.1 SHA == source SHA of published release bytes
```

No tracked commit or artifact rebuild is allowed after R6 visual acceptance and before publication. Post-publication documentation may advance only after the tag/release bytes are frozen and verified.

## Deferred after v3.0.1

Whole-repository lifecycle classification, >100 branch pruning, broad historical-document consolidation and unrelated utility/runtime cleanup remain deferred unless a direct release blocker is proven.

## Current next action

Resolve the current open PR whose head is `release/v3.0.1-canonical-review-corrections`. Require Static PASS, Linux Integration `complete` PASS (including Web/Lite E2E), Linux Release Check/current `pkgcheck` PASS, canonical reference generation and distribution/review-pair gates on that same SHA. Download the new canonical-reference and distribution artifacts generated from `template/main.tex`; visually inspect the corrected approval page and TOC, verify no rendered remissive index, and provide the resulting CTAN ZIP for maintainer inspection. Only after those checks may Stage A be considered green and the squash transport resume.

## Documentation discipline

Every material advance updates the machine state, affected lot evidence and this handoff in the same work cycle. Current Git facts always take precedence.
