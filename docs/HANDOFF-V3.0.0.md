# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main`; current SHA must be resolved dynamically from Git |
| Release PR #293 | **MERGED** as squash commit `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout PR #294 | **MERGED** as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Continuation synchronization PR #295 | **MERGED**; Static `34335044265` on canonical `main` SUCCESS |
| Active work branch | `release/v3-release`, aligned to canonical `main` after PR #295 |
| Superseded PR #292 | **CLOSED**; historical evidence only |
| Active phase | **Release** |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS with required complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Retained distribution artifact | ID `10086299397`, `abntexto-ufc-v3.0.0-distribution-34303586773` |
| Artifact upload digest | `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Independent artifact verification | exact five-file set; `SHA256SUMS` PASS; all four ZIP integrity checks PASS |
| Current batch | **Release publication — tag/GitHub Release verification pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

`docs/V3-CONTINUATION.md` is the shortest safe entry point for resuming from a new conversation or local clone. Current `main` HEAD is intentionally not hardcoded as a continuing invariant; fetch Git at session start.

## Accepted Release phase-end regression

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` is immutable and accepted.

| Gate | Accepted evidence |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reference PDF reproducibility | PASS; 2 builds; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Distribution bundle contract | PASS; four ZIPs + `SHA256SUMS`; archive integrity PASS |
| Validation artifact | ID `10086298601`, digest `sha256:124f692d571dde12754a6b084075b4acff29d47ffcfb4fb9d321cc8f1934d18c` |
| Distribution artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |

The retained distribution artifact was independently downloaded and verified without rebuilding.

## Accepted publication checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Remaining work

| Order | Action | State |
|---:|---|---|
| 1 | Create `v3.0.0` tag and GitHub Release from latest canonical `main`, using exact retained candidate-produced bytes. | PENDING |
| 2 | Verify published GitHub asset hashes against the accepted checksums. | PENDING |
| 3 | Run current CTAN `pkgcheck` on the retained CTAN candidate. | PENDING |
| 4 | Perform actual CTAN upload only as an explicit action and preserve receipt/acceptance evidence if performed. | EXTERNAL / EXPLICIT |
| 5 | Synchronize final publication state and perform final Release verification before setting Release `CLOSED`. | PENDING |

Librarian item 33 remains fail-closed pending authoritative current NBR 6023:2025 evidence.

## Local continuation

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
git rev-parse HEAD
```

Then read `AGENTS.md`, `release/v3-roadmap.json`, and `docs/V3-CONTINUATION.md` before making changes.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Targeted checks never replace the accepted **phase-end regression**. The Release candidate remains the evidence anchor; publication verification is an additional closeout obligation.
