# Release state

This file is the durable human-readable release-state authority for the repository.

## Published release

| Fact | State |
|---|---|
| Latest GitHub release | `v3.0.4` |
| Publication state | `PUBLISHED` |
| Published source SHA | `7e176fd5472925b519d469a9a756330f4851f0b3` |
| Annotated tag | `v3.0.4` |
| Annotated tag object SHA | `184b00ad2eaed8a98e6b17033e7623efb3e53571` |
| GitHub Release ID | `392476983` |
| Published at | `2026-09-20T15:29:02Z` |
| Maintainer visual acceptance | PASS — 2026-09-20 |
| CTAN v3.0.4 | published/accepted 2026-09-22 from the exact 2026-09-20 submission — issue #356 |
| Active development line | `v3.0.5` — NEW seven-profile ACCEPT recorded under issue #475 on 2026-10-10; `UNRELEASED` / `FROZEN` / `UNPUBLISHED` |

The current `main` branch may contain control/documentation commits made after publication. Those commits do not alter the published v3.0.4 source, annotated tag, release assets or checksums.

## Certified v3.0.4 publication evidence

The published source `7e176fd5472925b519d469a9a756330f4851f0b3` passed:

- Static Contract #675;
- Linux Integration #582;
- Linux Release Check #233 / run `35510145977`;
- complete regression `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- CTAN `pkgcheck 4.1.0`;
- canonical-reference reproducibility;
- PDF/A-2b, embedded-font, Unicode and repository-PDF validation;
- seven supported-profile review preflights;
- explicit maintainer visual acceptance.

The annotated tag `v3.0.4` resolves exactly to that source SHA. GitHub Release ID `392476983` was published at `2026-09-20T15:29:02Z`.

Published release assets are immutable project evidence and must not be rebuilt or replaced:

- `abntexto-ufc-3.0.4.zip` — `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`;
- `abntexto-ufc-template-3.0.4.zip` — `3412c0c63a85d340ec7789da509e1f6a2994efa1974207f3d79ac402a3aa159c`;
- `abntexto-ufc-overleaf-3.0.4.zip` — `4967ce1407e8b42b0a77ab688edbe9e759a64827e566f52d7864cb1f6118cf92`;
- `SHA256SUMS` — `a1aeb3f0c75449811677aaa6b11ee954cef3a253bd492433f066ba3ffea4f4d3`.

GitHub-reported asset digests were independently verified against those frozen values and matched exactly.

## Current repository lifecycle

GitHub publication of v3.0.4 is complete. Release issue #353 is completed and closed. Phase 10A / issue #469 selected v3.0.5 as the maintenance line and merged as `9aeed2cd57665bf4ec6d13990b88d8b779de22a1`. Phase 10B / issue #471 / PR #472 now prepares the exact publication-source candidate.

v3.0.5 remains `UNRELEASED`, `NOT_FROZEN` and `UNPUBLISHED` with no frozen candidate SHA and no publication authorization in the machine marker. Phase 10C has now received explicit maintainer ACCEPT for one exact certified source; Phase 10D must still perform a separately validated control-plane freeze before tag/publication. Phase 10B finalizes release-source content before candidate selection: the canonical changelog is dated, while `CITATION.cff` continues to describe the latest actually published release v3.0.4. The exact merged #472 SHA must be recertified before it can be offered for maintainer visual acceptance.

The root machine receipt `release/v3-release-candidate.json` represents this active development state while embedding the immutable v3.0.4 publication receipt. Completed v3.0.3 and v3.0.4 release receipts remain preserved under `release/history/v3/`, and the detailed v3.0.4 publication receipt remains under `docs/history/v3/release/`.

CTAN publication is a separate external operation tracked by issue #356. The exact `abntexto-ufc-3.0.4.zip` asset from GitHub Release v3.0.4, SHA-256 `137ba95ff0d8dab5fe8af6eab05d22b3cb9fd453d16d84b6beb26d090dc48cec`, was submitted on 2026-09-20 as an update from CTAN version 3.0.2 to 3.0.4. The official CTAN-ann update on 2026-09-22 confirms version 3.0.4 publication/acceptance. Repository control therefore records CTAN state `PUBLISHED` and acceptance state `ACCEPTED`; the submitted archive remains immutable and must not be rebuilt or replaced.

Previous GitHub release v3.0.3 remains immutable. Its machine receipt is preserved at `release/history/v3/v3.0.3-release-candidate.json`.

## Active v3.0.5 maintenance line

| Fact | State |
|---|---|
| Candidate version | `v3.0.5` |
| Candidate state | `FROZEN` (subject to freeze-control PR gates) |
| Candidate exact certified SHA | `30ff9b7bc777db28584fce7e96930e748ee1a661` |
| Current release issue | issue #475; CTAN metadata issue #369 |
| Publication authorized | true following explicit new maintainer ACCEPT |
| Publication state | `UNPUBLISHED` — no v3.0.5 tag or GitHub Release |
| Review evidence | artifact `11670542808`, sha256 `8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886` |
| Distribution evidence | artifact `11670527758`, sha256 `ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c` |
| Source checks | Static `38052629167`, Linux Integration `38052629234`, Linux Release `38052629238`, Windows `38055168762`, macOS `38055168813` PASS |
| Changelog | `3.0.5 — 2026-10-06`; CITATION.cff remains v3.0.4 until publication |

A freeze-control merge is not the release source and must not become the `v3.0.5` tag target. The release process must annotate/tag exactly `30ff9b7bc777db28584fce7e96930e748ee1a661`, verify and reuse the retained certified distribution bytes, and only then publish using an authenticated authorized mechanism. CTAN submission is later and independent. Existing v3.0.4 publication must not be altered.

## Authority order

When facts disagree, use this order:

1. current Git facts and GitHub release/tag state;
2. `release/v3-release-candidate.json` machine receipt;
3. this file;
4. current durable technical documentation;
5. controlled historical evidence under `docs/history/v3/` and `release/history/v3/`.

Closed Issues and historical release documents are audit evidence, not active authority.

## Explicit v3.0.5 maintainer ACCEPT — 2026-10-09

The maintainer explicitly approved exact certified candidate source `407f279a78df3824b27585d0e86d688c19cd90ee` and seven-profile review artifact ID `11415094731` (digest `sha256:23193aaaacdb2af7b465e4ddae17428344d1ac1d65d5dcc1b7089cf7bb342fa4`) through issue #474. The review artifact was produced by Linux Release Check #306 / run `37467235323`, with full Static #945, Linux Integration #798, Windows #20 and macOS #12 certification.

**Human acceptance is complete; freeze and publication are not.** Issue #475 owns the next step. The current `release/v3-release-candidate.json` remains `NOT_FROZEN`, `candidate_sha=null`, `publication_authorized=false` and `UNPUBLISHED` until a separate freeze-control PR and its required gates pass. The future annotated `v3.0.5` tag must peel to the accepted source SHA, not to a subsequent documentation/control commit. The retained distribution set is artifact `11416117138`; it must be verified and reused byte-for-byte without rebuilding. The published v3.0.4 tag/assets remain immutable and CTAN v3.0.5 is a separate future operation.


## Phase 10D freeze preflight — 2026-10-10

A fresh remote reconciliation at `main=47f101129316a72815c5e2f0bb1f9223dba5a3eb` confirmed #474 ACCEPT for exact source `407f279a78df3824b27585d0e86d688c19cd90ee`, but identified a publication-metadata blocker before #475 freeze. The accepted source's `release/ctan/README.md` still declares `Release status: Unreleased` and describes 3.0.5 as an unreleased development line. `tools/build-distribution-bundles.py` copies this file verbatim into the CTAN archive. Issue #369 explicitly forbids this status in a frozen/publication-authorized candidate.

**Decision: BLOCKED, fail closed.** No control-plane-only freeze may silently certify these inconsistent publication-source bytes. Editing that README changes the previously accepted source and therefore requires selecting an updated exact source SHA, rerunning complete Static/Linux Integration/Linux Release (including CTAN, reproducibility and distribution) plus Windows/macOS portability certification, regenerating/reviewing the seven profile pairs and obtaining explicit renewed maintainer ACCEPT for the updated source/artifact pair. Existing 10B/10C receipts remain valid historical evidence for the original SHA but are not transferable to changed bytes. No tag/Release/CTAN submission is authorized. The v3.0.4 publication is untouched.

The repository metadata-consistency contract now fails closed if a frozen or publication-authorized 3.0.5 marker retains either stale CTAN README declaration; unfrozen development continues to be explicitly labelled Unreleased. The freeze-control transition and downstream #475 publication work remain pending, and the separate authenticated annotated-tag/Release-asset capability remains a later dependency. Track #475 and #369; do not bypass this by weakening tests or publishing the accepted archive with stale metadata.


## Phase 10D source-metadata correction — 2026-10-10

Current owner: issue #475 (release control) and issue #369 (CTAN metadata); PR #478 implements this bounded correction.

PR #477 was merged as `57b433bb2525e9776a5e86c7b26b8412b33268eb`. All mandatory exact-merge-SHA post-merge gates passed: Static run `38048287023`, complete Linux Integration `38048286958`, Linux Release `38048287005`. This is a certified prerequisite, not a freeze. At entry, no PR was open.

Issue #369 requires correction of the verbatim CTAN `release/ctan/README.md`. Its version metadata now reads **Prepared for publication**: the source is staged for distribution without falsely claiming GitHub Release or CTAN publication. The earlier 'unreleased maintenance development line' assertion is removed. Metadata and governance tests bind that corrected status to the explicit source-correction stage, preserving a fail-closed release control and immutable v3.0.4 receipt.

**This change creates a new source, not an approved publication candidate.** Historic #474 ACCEPT binds only exact source `407f279a78df3824b27585d0e86d688c19cd90ee` and review artifact `11415094731`; the acceptance cannot carry over to changed package bytes. The release marker stays `NOT_FROZEN`, `candidate_sha=null`, `UNPUBLISHED`, `publication_authorized=false`.

Next gate: Static, complete Linux Integration and Linux Release of the source-correction PR; only after all PASS, merge and recertify the exact new `main` SHA, plus fresh Windows/macOS portability and seven-profile review. Require renewed explicit maintainer ACCEPT on the **new** source and artifacts before a separately certified freeze-control transition. Annotated tag, GitHub Release and CTAN submission remain forbidden until their independent gates and publication capabilities exist. Published v3.0.4 tags and bytes remain immutable.


## Phase 10D corrected-source certification complete; new visual ACCEPT pending — 2026-10-10

**Source identity (binding):** corrected v3.0.5 publication-source SHA `30ff9b7bc777db28584fce7e96930e748ee1a661`, Git tree `4b2a64e5c318ef761d84364877000086d51f1664`; PR **#478** merged into `main` after head `4d1a2d8e7817ae2377bef42cc7b74a5d0bb7cd4d` passed Static `38050245712`, complete Linux Integration `38050245726` and Linux Release `38050245720`. A previously failed Static run `38050098273` required literal issue #475 traceability in release-state documentation, corrected by commit `3848be3634d768ec92feeb5aeb158315e6cb807a` without weakening tests. This remains visible in CI.

**Certified exact source:** post-merge `main` Static `38052629167` PASS, complete Linux Integration `38052629234` PASS, Linux Release `38052629238` PASS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`, CTAN pkgcheck **4.1.2 PASS**. Seven-profile review pairs: artifact `11670542808`, GitHub/downloaded ZIP SHA256 `8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886`; status `READY_FOR_MAINTAINER_REVIEW` / `PENDING`. Independently downloaded the ZIP, verified archive integrity and **all 14 .tex/.pdf hashes** against both its `SHA256SUMS` and `manifest.json` (seven profiles).

**Portable exact source:** PR **#479** was a disposable **DO-NOT-MERGE** harness, head `f317764917f3a82e591913692844925cfcc66ea2`, explicitly pinning build/certification checkouts to source SHA `30ff9b7bc777db28584fce7e96930e748ee1a661` with Git HEAD assertions and source-bound evidence. Windows run `38055168762`: native build and Linux PDF certification both PASS, four strict Arial/Times PDFs, Unicode extraction, font embedding, PDF/A-2b PASS; Windows evidence artifact `11670004777`, SHA256 `ac5236cb819d2a2bed3b05da7f86ce5331148e1d8492d76816b6a5bb2d6f3a30`. macOS ARM64 run `38055168813`: native pdfLaTeX/LuaLaTeX template build and Linux PDF certification both PASS, embedded fonts and PDF/A-2b PASS; macOS evidence artifact `11670744828`, SHA256 `8500a8c2dd094ac0edef60beeb1bc91c656c9cb2069999ff29f9e451d09e2d22`. Harness Static `38055168782` PASS; nonpublication Linux Integration `38055168840` was still running at receipt creation, which is not a substitute for the green complete source Linux Integration `38052629234`. PR #479 was **closed unmerged** after the platform certifications; harness commit is NEVER a publication source. The temporary validation-only branch may require external cleanup because the GitHub connector cannot delete refs.

**Independently verified distribution:** artifact `11670527758`, GitHub/downloaded ZIP SHA256 `ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c`. All three contained v3.0.5 ZIPs verify against retained `SHA256SUMS` and pass ZIP integrity. Canonical class SHA256 across CTAN/Template/Overleaf is identically `e9dba9b3e8ab7b973e3d3788c0308082dd5267de63dae8f36c3bb1ae4aac0f27`. CTAN ZIP README explicitly says `Release status: Prepared for publication` and contains no `Unreleased` token. Inner canonical asset SHA256: CTAN `b57e2f4f17d5a707e93a30f5fe701f0f14606fc39c01d6f09b6e8a3781e652e8`; Template `a6433d7e698a8e89a39761a7ea5951b267cce2169844827410fdc958da39196a`; Overleaf `082255fddec80f6e6aeee17f6781d579d3c488c8571a456018aa3524eade7e3d`.

**State/gate:** The earlier explicit ACCEPT in issue #474 binds **only** SHA `407f279a78df3824b27585d0e86d688c19cd90ee` / historical artifact `11415094731` and does NOT transfer to the corrected source. For the seven newly certified v3.0.5 PDFs, an **explicit fresh maintainer visual ACCEPT** of exactly source `30ff9b7bc777db28584fce7e96930e748ee1a661` and artifact `11670542808` is still required. Thus the machine marker must stay `NOT_FROZEN`, `candidate_sha=null`, `UNPUBLISHED`, `publication_authorized=false`; the last published release is immutable v3.0.4. These docs are a subsequent control-plane receipt, **not** a new release source and not a request to transfer acceptance to their merge SHA.

**Next exact step:** Present the seven PDFs for human review and obtain the new unambiguous maintainer ACCEPT, or correct visual defects through a new isolated release-source PR and rerun all exact-SHA certifications. Only after human ACCEPT may a separate freeze-control PR reconcile marker/governance, pass its full gates, then use an authorized authenticated mechanism for annotated `v3.0.5` tag targeting **exactly the accepted source**, verify retained distribution bytes/digests, publish GitHub Release and separately follow up on CTAN. No tag, release upload, CTAN submission or retroactive change to v3.0.4 has occurred.


## Phase 10D — explicit corrected-source ACCEPT and controlled freeze (2026-10-10)

The maintainer has now explicitly **ACCEPTED** the seven reviewed PDFs by responding "Pode seguir, aceitos" on 2026-10-10. Issue #475 records the new and only applicable publication-source identity: exact certified commit `30ff9b7bc777db28584fce7e96930e748ee1a661` (tree `4b2a64e5c318ef761d84364877000086d51f1664`), seven-profile review artifact `11670542808` (sha256 `8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886`), retained distribution artifact `11670527758` (sha256 `ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c`). The previous #474 ACCEPT binds a **different source** and is preserved as historical evidence, not reused.

Source was certified on exact SHA by Static `38052629167`, complete Linux Integration `38052629234`, Linux Release `38052629238` (38/38 and CTAN pkgcheck 4.1.2 PASS), native Windows `38055168762` and macOS ARM64 `38055168813`. All retained distribution inner ZIP checksums and seven PDF/.tex pairs were verified. The published v3.0.4 receipt is immutable.

**This PR changes only control plane:** `release/v3-release-candidate.json`, the two strict governance/metadata tests, AGENTS, RELEASE-STATE and REPOSITORY-MAINTENANCE. Candidate `FROZEN` / `candidate_sha=30ff9b7bc777db28584fce7e96930e748ee1a661` / `publication_authorized=true` / `publication_state=UNPUBLISHED`. It neither modifies publication source nor creates v3.0.5 GitHub Release/tag/CTAN entry. All Static, **complete** Linux Integration and Linux Release gates must be green on freeze-control head; verify base/head and certify post-merge main. The control-plane SHA must **never** be substituted for `30ff9b7bc777db28584fce7e96930e748ee1a661`.

**Next gate after fully green freeze:** tag `v3.0.5` as an annotated Git tag peeled **exactly** to `30ff9b7bc777db28584fce7e96930e748ee1a661` using an authenticated authorized mechanism, verify original certified assets vs recorded hashes, publish GitHub Release with only those bytes, verify server receipts, synchronize release state, then create separate CTAN follow-up. Connected GitHub connector lacks tag and Release asset mutations; do not attempt lightweight tags, substitute binaries, unverified publication or silent bypass. If those capabilities remain unavailable, stop publication and record the external CLI instructions and limitation in issue #475.
