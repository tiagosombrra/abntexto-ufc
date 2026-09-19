# CI helper scripts

This directory contains repository-owned logic used by GitHub Actions workflows.

The design rule is:

- workflow YAML owns triggers, permissions, job orchestration, environments and artifact upload;
- scripts in this directory own deterministic project-specific checks or assembly logic that should be reviewable and runnable outside YAML heredocs.

## Integration helpers

- `select-integration-scope.py` — selects the Linux Integration scope from the complete PR diff, draft state, release-marker changes or manual input.
- `run-web-lite-e2e.sh` — validates the runner browser prerequisites and invokes the Web/Lite browser E2E test.

## Release helpers

- `validate-pkgcheck-download.py` — verifies that the host-fetched CTAN `pkgcheck` archive is present and structurally valid.
- `validate-release-reference.py` — verifies exact-source provenance and validation evidence for the canonical release PDF.
- `validate-release-assets.py` — verifies the exact expected distribution-asset set.
- `certify-ctan-package.sh` — locates the supported `pkgcheck` executable, validates the generated CTAN package and produces the release-review pairs.
- `render-release-summary.sh` — renders the GitHub Actions release-validation summary.

## Pages helper

- `build-pages-site.sh` — assembles and validates the static Pages tree before artifact upload.

## Maintenance rules

These scripts are part of the CI contract, not ad-hoc utilities.

When changing one:

1. keep the corresponding workflow trigger aware of the script when appropriate;
2. preserve fail-closed behavior;
3. do not weaken source-SHA, checksum, package, PDF or asset-policy assertions;
4. run the workflow's normal validation path through a pull request;
5. keep GitHub-specific orchestration in YAML unless moving it improves local testability without hiding permissions or trigger behavior.

The workflows remain the authoritative entry points. These helpers exist to make project logic easier to review, test and reuse.
