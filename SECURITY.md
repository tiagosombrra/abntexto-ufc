# Security policy

## Supported scope

Security reports are appropriate for issues that can affect the confidentiality, integrity or supply-chain safety of the current project, including:

- unexpected network transmission or upload behavior in the Web/Lite validator;
- unsafe handling of user-provided PDF data by project-owned validator code;
- dependency or GitHub Actions supply-chain concerns;
- release/distribution tampering or checksum inconsistencies;
- path traversal, unsafe archive construction or unexpected file inclusion in generated bundles;
- accidental redistribution of restricted/proprietary assets;
- repository automation that can modify protected publication state outside the documented controls.

Formatting defects, academic-rule disagreements and ordinary LaTeX compilation bugs are not security vulnerabilities. Report those as normal project issues.

## Current processing boundary

The Web/Lite validator is designed for local browser processing and must not upload the user's PDF to a server.

The CLI/deep validator runs locally in the user's environment.

A report that demonstrates behavior outside these boundaries should include enough evidence to reproduce the observation.

## Reporting

Use a private security-reporting mechanism provided by the repository/platform when available. Do not publish exploit details in a public issue before the maintainer has had a reasonable opportunity to evaluate the report.

Include, when applicable:

- affected version or commit SHA;
- environment/browser/runtime versions;
- reproducible steps;
- minimal sample input that does not contain sensitive personal data;
- observed network request, unsafe file path or integrity mismatch;
- expected security boundary;
- impact assessment.

## Release integrity

Published tags, release assets and checksums are treated as immutable project evidence.

A suspected mismatch between a release asset and its published checksum, or between a certified source and a distributed project runtime, should be treated as an integrity incident and investigated before any replacement or new publication.

Do not rebuild an existing published release in place as a remediation. Corrections belong to a later version.

## Dependency and CI hygiene

GitHub Actions must remain pinned according to repository policy. Dependency-update automation must not bypass required checks or branch/tag protection.

Generated archives must continue to enforce the distribution contract documented in `docs/ARCHITECTURE.md` and `docs/CTAN-RELEASE.md`.
