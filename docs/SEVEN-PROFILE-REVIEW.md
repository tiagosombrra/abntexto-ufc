# Seven-profile development PDF review — source-bound protocol

Status: **DEVELOPMENT v3.1.0 UNRELEASED**. Tracking: [#507](https://github.com/tiagosombrra/abntexto-ufc/issues/507), macro [#489](https://github.com/tiagosombrra/abntexto-ufc/issues/489).

## Verified current-main review reference (pre-correction snapshot)

The upstream [Linux Release run 39461123236](https://github.com/tiagosombrra/abntexto-ufc/actions/runs/39461123236) on exact source commit `9fa86c79eb6de7a37354aab4e116bd2b021cbe97` passed **SCOPE=complete PASS=38 FAIL=0 SKIP=0**, CTAN pkgcheck 4.1.2 PASS, generated artifact **12283299881** `abntexto-ufc-v3.1.0-review-pairs-39461123236`. That archive was independently opened and `manifest.json`, `SHA256SUMS` and all 14 PDF/TeX bytes independently matched. Manifest explicitly says `READY_FOR_MAINTAINER_REVIEW` and `maintainer_visual_approval=PENDING`, **not ACCEPTED**.

| Profile | Pages | PDF SHA-256 |
|---|---:|---|
| undergraduate-capstone | 12 | `79bb059911d728469b7c9959bcbdac8b7960084d5e545903c040726200d23b25` |
| specialization-capstone | 12 | `e3cf094a212f7d32f6c7f09ab08bef62358bf19909e0dd9eb9ac57affbcf06ed` |
| masters-thesis | 12 | `28b1b5bafb7a88d9452ad81b59165b91f859ba8ad2828417a9c483b18cb285f8` |
| doctoral-thesis | 12 | `0a14a9cab25145f8684e548006bdb6cedc08f52cbc406fbcd27b8eff3e317e82` |
| research-project | 9 | `9ea145b7614bb06f901f82f4d5164c2f72e4934cb8294871eaf5050a962f95db` |
| anonymized-research-project | 9 | `5b47d32ddc41a78846cac939ecc724ac26b02ff4cd5c650a17ded43fa723be1e` |
| scientific-article | 5 | `07e07ecbee2f055a86fc90653fb7899382e7f11271c3241c8c45f142cc03b176` |

71 PDF pages total. The independent text-extraction/media-box preflight found no fully blank extracted-text page, embedded PDF attachments, or out-of-page text blocks; the sampling is **not** a page-by-page ABNT/UFC or human visual ACCEPT. PDFs are synthetic institutional-profile test examples, not complete manuscripts.

## Important anonymization boundary

The **anonymized generated PDF** on the reviewed artifact does not expose fixture identity tokens `Autor Matriz Teste`, `Prof. Orientador Matriz Teste` or `Prof. Membro Matriz Teste` in PDF-extracted page text, PDF Info/XMP, and has no attachments. The matching **`06-anonymized-research-project.tex` source DOES contain these fixture identity fields**, by design: the class masks them from visible PDF output, not from authored source bytes.

Therefore:

- **The seven-pair .tex/.pdf archive is for internal maintainer audit only. Never ship its anonymized .tex or the full combined audit bundle as a blind-submission package.**
- The PDF token checks cover only named synthetic fixtures and checked metadata surfaces. They do **not** certify general anonymization, all possible hidden PDF identifiers, institutional blind-review acceptability or absence of indirect identifying material.
- Any blind submission or PDF-only export needs its own human policy review and must not infer safety from the generic review-pair artifact. This change does not create a blind-submission distribution package.
- The `maintainer_visual_approval=PENDING` field is an explicit gate; a green workflow is **never** a maintainer's manual signoff.

## Executable gate

`tests/integration/release/release-review-pairs.sh` writes seven source/PDF pairs and the original manifest. Immediately after generation it invokes `tools/ci/validate-review-pairs.py` and fails closed if:

1. the manifest SHA does not exactly equal the audited commit, the version is not 3.1.0, the number/order/names of profiles are wrong, or visual approval is other than `PENDING`;
2. any source or PDF digest disagrees with its manifest entry or `SHA256SUMS`, duplicate/unexpected archive files appear, or the complete 14-file pair set is missing;
3. the anonymized TeX fixture unexpectedly lacks expected synthetic identity-bearing inputs (a test invalidation), or any of those named identities appears in extracted PDF text, PDF Info or XMP metadata;
4. the anonymized PDF contains embedded files or the declaration incorrectly treats identity-bearing TeX as safe for blind review.

The static *controlled negative* inside the Python tool proves its identity-token check recognizes whitespace-reflowed fixture names, not merely contiguous literal strings. Linux Release is also now triggered on PRs changing either the review producer or verifier (previous `pull_request.paths` gap), while unchanged integration and other release invariants remain mandatory.

## Human review requirements and release boundaries

Each of the seven document profiles must receive **ACCEPT, REJECT or NEEDS_CHANGES** with exact source SHA, artifact ID and SHA-256 digest, individual PDF digest, inspected pages, reviewer and decision date. Any rejection requires a scoped PR, exact-head Static/Integration/Release gates, guarded merge, new full postmerge certification and **new** seven-pair artifact: historical acceptance is never transferred to new bytes.

Check covers, frontmatter, degree/programme/committee wording, table of contents, title blocks, section breaks, geometry, font sizes, accessible text extraction, dates, special footers, profile-specific forbidden/optional elements, and any suspected overflow on representative first/middle/last pages. A page dimension or lexical test alone is not sufficient visual approval. Institutional rules and ABNT edition/errata status remain separately tracked in [#488](https://github.com/tiagosombrra/abntexto-ufc/issues/488).

The publicly published **v3.0.5** release and its dated seven-profile ACCEPT remain immutable and source-specific; this v3.1.0 preflight does not approve a publication, retarget a tag or modify any of the 29 normative parent rules/seven document profiles.
