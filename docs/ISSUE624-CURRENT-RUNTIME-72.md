# Issue #624 — current-runtime 72-ID bounded PDF requalification

This is an independent candidate-only evidence ledger, not a promotion of the
historical 58/72 ledger or the 72/72 corrected-runtime ledger from an earlier
class. It does not certify institutional, normative, linguistic, editorial
or publication approval.

## Exact provenance

- Evidence producer: PR #623, commit b5393f94af996ee978144eb7ba95f21140924400.
- Current candidate class Git blob: 4f3b266e8fce9204577565961d35c3066fd59cee.
- Prior corrected-runtime class blob: 299293e273dcefb80256eed2e17d2557db6aae52.
- Ten GitHub Actions ZIP artifacts from integrated diagnostics run 45200284116
  and optional modules run 45200285066, all bound to that same commit.
- Inventory: 17 setup identifiers, 43 commands, six environments and six
  upstream identifiers, mapped to 13 scoped proof families.

## Two distinct executable audits

The **permanent CI gate** is
.github/workflows/current-runtime-integrated-28.yml. Each run generates the
seven complete manuscripts in four languages, optional module PDFs in each
language and both B1 auxiliary suites, on the exact candidate commit. The
final fresh-source-ledger job downloads **only artifacts from that same run**
through a SHA-pinned download action with digest mismatch treated as an error.
It executes tools/ci/requalify_live_runtime_72.py, compares the 72 API records
to genuine newly generated PDF/TeX/JSON hashes, checks the original immutable
API maps, and produces artifacts/issue624/current-run-72.json with ten negative
mutations. No old GitHub Actions artifact ID is a dependency of this CI gate. The
source contract compares the actual class and five original API/ledger Git
blobs, rather than requiring ancestry of an old PR commit; it therefore
survives a protected squash merge while still failing closed on changed bytes.
All ten negative mutations are checked by invoking the same verification
function used on the real current-run report.

The **archival audit**, in
.github/workflows/current-runtime-72-requalification.yml, is manual-only
(workflow_dispatch), not a permanent status check. Its original archived
artifact IDs will expire under GitHub's configured retention policy. During
retention, tools/ci/requalify_current_runtime_72.py can authenticate those
frozen ZIP bytes and output a bounded historical candidate receipt. Once the
ZIPs expire this optional recheck is unavailable unless their exact bytes
have been preserved separately; no new run is allowed to impersonate their
artifact IDs or original SHA. The archival check is not necessary to run
future current-class PDF generation and validation.

The archival validator checks frozen ZIP IDs, producer run IDs, GitHub digests,
source commit, byte hashes, safe paths and CRC, while the permanent validator
checks same-run artifacts, the source SHA, every actual file's SHA-256 and
the 72 identifiers in all 13 proof families. Both require negative controls
and protect the unchanged original API inventory. For strict-font, an expected
rejection log and source are required, along with an adjacent positive nonstrict
font PDF. It never fabricates a positive strict-font PDF.

The archival test rejects eight negative mutations; the fresh-run gate rejects
at least ten. These include a dropped identifier, altered PDF
hash, altered artifact ID, altered proof hash, incorrect class blob, fabricated
release approval, fabricated human promotion and incorrect total.

Machine success is a bounded functional candidate finding only. All human and
normative review fields remain PENDING, formal promotion NOT_AUTHORIZED,
v3.1.0 UNRELEASED, publication_authorized=false.

## Current matrix and post-merge contract

The live gate also executes the original locale preflights, the six executable
driver relationships (12 rejected source mutants), and 12 institutional
fallback PDFs per locale (48 total, 18 negative controls). These are additional
bounded checks, not extra identifiers in the 72-ID ledger. The source
preflight preserves the executable-driver report, and locale artifacts
preserve the fallback PDF, TeX, log and manifest bytes.

The expanded matrix passed all eight jobs in run 45374463506 on
12c95b462224ae7b0bc4f8b47e7296d6bdb52855. Ledger artifact 14911340728
has SHA-256 435fe8a3475976fb3315ed8ca89ae883d0c2ada3b3f1c203c4fb6a943bf8285c.
This is a receipt for that commit only, not the post-merge source.

The current workflow is configured to run on every push to main, as well as
its existing PR and manual triggers. A protected squash must produce new
evidence using github.sha, not inherit the pre-merge artifact or receipt.
The same class/API blob checks remain mandatory. Unknown class/API bytes
must fail closed. The new push route cannot be certified until it actually
runs on main after a separately authorized merge.

## Historical gate reconciliation (candidate implementation; review pending)

| Existing check | Current-source route | Historical route |
| --- | --- | --- |
| Integrated manuscript four-language matrix | All locale/preflight/auxiliary producers plus fresh 72-ID ledger; verify complete parity before retiring duplicate execution | Preserve old blob-bound ledgers and original receipt |
| v3.1.0 corrected-runtime 72-ID original archive byte audit | Fresh current-run ledger only after explicit reviewed disposition | Original ten ZIPs and exact historical source, no current certification; expiration must be reported, not waived |
| R8.1 archived reviewed-PDF independent PDF/A-2b validation | Fresh R5 editorial 28 PDFs/972 pages and veraPDF on the same final SHA; human acceptance is separate | Original reviewer ZIPs, source and PDF/A receipt, ARCHIVE_ONLY |

The three old workflows are now proposed as manual-only ARCHIVE ONLY routes
on the immutable pre-change main commit f0e3617783e6d7bf072d846a0e28b62d7f79b232.
This commit contains the old class and unchanged archive validators; the
original proof ancestry is still fetched and checked. Original ZIP expiry
remains a hard failure, not a reason to reconstruct or substitute bytes.
The old integrated diagnostic jobs are superseded by the complete current-run
matrix; their definitions and failed run receipts remain in Git history.
The live 72-ID gate also triggers on changes to the three archive workflows.
R5 now runs for relevant stacked PRs and every main push; its development
PDF/A gate verifies the current 972-page corpus without human acceptance.
The historical 984-page manual branch route is unchanged. None of these
changes are yet merged or independently approved. Manual archive dispatches
and main-push routes must be checked separately after the workflow definitions
are present on main; current-source PR runs are not evidence of those events.
Current Linux full integration/release and all other final SHA gates remain
required by project policy, even if not required by the GitHub ruleset.

## Remaining gates

- Requalify the integrated manuscript preflight for the current class separately
  from the immutable historical source guards, without transferring old receipts.
- Authenticate original archived R8.1 PDFs under their original source and label
  those results ARCHIVE_ONLY, not current-class approval.
- Prepare current-class human review packet with 972 initially PENDING page
  decisions and obtain explicit maintainer acceptance.
- Reconcile reviews and complete all source-bound Linux 42/42, Release 38/38,
  R4 32 PDFs, R5 28 PDF/A-2b, Windows and macOS checks at the final SHA.
- Do not merge PR #623 or publish version 3.1.0 until required conditions hold.

Last public version: 3.0.5. No tag, GitHub Release or CTAN publication authorized.
