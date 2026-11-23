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

## Executable audit

The workflow .github/workflows/current-runtime-72-requalification.yml invokes
tools/ci/requalify_current_runtime_72.py with --download and --self-test. This
produces artifacts/issue624/current-runtime-72.json as a workflow artifact.
The exact class blob and original evidence-producing commit ancestry must match.

The validator authenticates the ten artifact IDs, producer run IDs, GitHub
digest metadata, source commit, ZIP bytes, safe member paths and CRC. It then
checks all 72 unique canonical names and evidence-family assignments, requiring
actual PDF and TeX SHA-256 records in each identifier's appropriate source
manifest, together with recorded negative controls. For strict-font, an expected
rejection log and source are required, along with an adjacent positive nonstrict
font PDF. It never fabricates a positive strict-font PDF.

Eight negative mutation tests must reject a dropped identifier, altered PDF
hash, altered artifact ID, altered proof hash, incorrect class blob, fabricated
release approval, fabricated human promotion and incorrect total.

Machine success is a bounded functional candidate finding only. All human and
normative review fields remain PENDING, formal promotion NOT_AUTHORIZED,
v3.1.0 UNRELEASED, publication_authorized=false.

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
