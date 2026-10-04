# Archival and preservation path

This document records the current citation, archival and persistent-identifier policy for `abntexto-ufc`.

It describes the repository's **current evidenced state** and the prerequisites for future archival integration. It does not claim that a Zenodo deposit, DOI or future release line already exists.

## Current state

- Published GitHub release: `v3.0.4`.
- Published source SHA: `7e176fd5472925b519d469a9a756330f4851f0b3`.
- Current repository maintenance may be ahead of that published source.
- Active development line: none selected.
- Repository citation metadata: root `CITATION.cff`.
- Current `CITATION.cff` records version `3.0.4` and release date `2026-09-20`.
- No DOI is recorded in repository citation/release metadata.
- No `.zenodo.json` or `codemeta.json` is currently authoritative.
- No repository evidence proves that the project is currently enabled in a Zenodo account or that a Zenodo record already exists.

Published v3.0.4 source, tag, GitHub Release assets and the exact CTAN-submitted archive are immutable project evidence and must not be rewritten merely to add later archival metadata.

## Citation metadata authority

Keep `CITATION.cff` as the repository citation metadata source unless a concrete integration requires a different format.

Zenodo supports `CITATION.cff` for GitHub software-release metadata. A `.zenodo.json` file is not required for ordinary GitHub release archiving. If both files exist, Zenodo uses `.zenodo.json` and ignores `CITATION.cff` for GitHub release archiving.

Therefore:

- do not add `.zenodo.json` merely for symmetry;
- add it only when real Zenodo-specific metadata such as grants, communities or related identifiers is required;
- if it is introduced later, document explicitly that it overrides `CITATION.cff` for Zenodo GitHub-release ingestion;
- do not add `codemeta.json` without a concrete consumer or metadata requirement.

References:
- https://help.zenodo.org/docs/github/describe-software/
- https://help.zenodo.org/docs/github/describe-software/citation-file/
- https://help.zenodo.org/docs/github/describe-software/zenodo-json/

## Future Zenodo/DOI procedure

A future maintainer who decides to archive a new release through Zenodo should use this order:

1. Link/authenticate the maintainer's GitHub account with Zenodo.
2. Enable `tiagosombrra/abntexto-ufc` in the Zenodo GitHub integration.
3. Select/open the future development/release line under the repository's normal release discipline.
4. Update and validate `CITATION.cff` for that actual future release before publication.
5. Complete the repository's release certification and maintainer acceptance gates.
6. Publish the GitHub release from the certified immutable source.
7. Allow the enabled Zenodo integration to archive the GitHub release.
8. Capture the external Zenodo record, DOI and archival status as evidence.
9. Only after that external receipt exists, update repository citation/release metadata with the real DOI/record identifiers in a bounded follow-up.
10. Preserve the prior published release/tag/assets and archival receipts unchanged.

Zenodo's GitHub integration and DOI documentation:
- https://help.zenodo.org/docs/github/enable-repository/
- https://help.zenodo.org/docs/github/archive-software/github-upload/
- https://help.zenodo.org/docs/deposit/describe-records/reserve-doi/

Do not invent, predict or pre-populate a DOI merely to make repository metadata look complete.

## Artifact attestations

Phase 8 evaluated GitHub artifact attestations and deliberately deferred adoption.

Current release checks rebuild versioned v3.0.4 regression candidates from post-publication `main`, while the actual published v3.0.4 assets are immutable bytes from the published source SHA above. Attesting later maintenance rebuilds as ordinary v3.0.4 release artifacts would blur that provenance boundary.

Re-evaluate artifact attestations only after a future development/release line is explicitly selected. The future release-producing workflow should attest exact release-candidate subject digests and bind them to the certified source/release receipt.

GitHub's current attestation workflow requires additional OIDC/attestation write permissions; adopting those permissions without a bounded publication subject is intentionally avoided.

Reference:
- https://docs.github.com/en/actions/how-tos/secure-your-work/use-artifact-attestations/use-artifact-attestations

## OpenSSF Scorecard

Phase 8 also evaluated a repository-owned OpenSSF Scorecard workflow and intentionally did not add one.

Current facts at the Phase 8 decision point:
- the repository is public;
- the Scorecard project provides public-repository scanning;
- all 28 external GitHub Action uses in the repository's six workflows are pinned to full commit SHAs;
- repository-owned published Scorecard results would add OIDC/security workflow permissions and maintenance constraints;
- no concrete current defect requires that additional workflow.

Re-evaluate if a Scorecard regression becomes actionable and is not already covered by repository contracts, or if repository-owned Code Scanning/Scorecard result provenance becomes an explicit project goal.

Reference:
- https://github.com/ossf/scorecard-action

## Authority and invariants

When archival/citation facts disagree, use current Git/GitHub state and the release authorities in `docs/RELEASE-STATE.md` and `release/v3-release-candidate.json`.

Never:
- fabricate a DOI or archival record;
- claim Zenodo is enabled without external evidence;
- retarget a published tag;
- replace published GitHub Release assets;
- rebuild or replace the already-submitted/published CTAN v3.0.4 archive;
- use later maintenance runs to imply provenance for earlier published bytes.
