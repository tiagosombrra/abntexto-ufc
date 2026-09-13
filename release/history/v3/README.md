# V3 release-state history

This directory preserves closed v3/v3.0.1 machine-state snapshots.

Files here are historical evidence only. They must not be used as current development or release authority.

Current release-state authority:

- `release/v3-release-candidate.json` — active CI marker path;
- `docs/V3.0.2-REPOSITORY-HYGIENE-STATUS.md` — current development/hygiene state;
- issue #313 — live operational receipts.

The active marker is intentionally kept at its stable root path because GitHub Actions uses that path to force complete integration/release validation when candidate state changes.
