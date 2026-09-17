# V3 release-state history

This directory preserves closed v3 release machine-state snapshots.

Files here are historical evidence only. They must not be used as current development or release authority.

Current release-state authority:

- `release/v3-release-candidate.json` — active CI marker path;
- `docs/V3.0.3-DISTRIBUTION-CORRECTION.md` — current v3.0.3 corrective development state;
- issue #328 — live v3.0.3 operational receipts.

Historical publication control remains available here, including the frozen v3.0.1 and v3.0.2 release-candidate snapshots. Issue #313 retains the v3.0.2 CTAN publication closeout while that submission finishes processing.

The active marker is intentionally kept at its stable root path because GitHub Actions uses that path to force complete integration/release validation when candidate state changes.
