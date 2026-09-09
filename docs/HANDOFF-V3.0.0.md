# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-09

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `e34037f3241aab013b80645b338f38954e02bcda` |
| Active branch / PR | `release/v3-release` / #293 |
| Active phase | **Release** |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — **ACCEPTED** |
| Candidate Static | `34303586782` — SUCCESS |
| Candidate Linux | `34303586778` — SUCCESS with required complete scope |
| Candidate Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Retained distribution artifact | ID `10086299397`, `abntexto-ufc-v3.0.0-distribution-34303586773` |
| Artifact upload digest | `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Independent artifact verification | download digest matches GitHub artifact digest; exact five-file set; inner checksums and all ZIP integrity checks PASS |
| Current batch | **Release publication — PR merge/tag/GitHub Release verification pending** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |

Canonical control documents include `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-RELEASE-READINESS.md`, `docs/V3-RELEASE-PHASE-END.md`, `docs/CTAN-RELEASE.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Accepted Release phase-end regression

Candidate `75ead435eabe5157ed17c295ac26fce76438b0ca` is immutable and accepted. It was not amended after CI started.

| Gate | Accepted evidence |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Linux integration | `34303586778` — SUCCESS, complete scope |
| Linux release check | `34303586773` — SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reference PDF reproducibility | PASS; 2 builds; SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`; 450652 bytes |
| Distribution bundle contract | PASS; four ZIPs + `SHA256SUMS`; archive integrity PASS; proprietary fonts redistributed = false |
| Validation artifact | ID `10086298601`, digest `sha256:124f692d571dde12754a6b084075b4acff29d47ffcfb4fb9d321cc8f1934d18c` |
| Distribution artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |

The retained distribution artifact was downloaded after workflow completion. Its downloaded archive digest matched GitHub metadata. `SHA256SUMS` verified all four publication ZIPs, and `unzip -tq` passed for each ZIP. No publication bundle was rebuilt for this verification.

## Accepted publication checksums

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.0.zip` | `c38fe32bc6b51ff3b7723b4ef118574d130cea97f29d443c1fc4d08b24e0b207` |
| `abntexto-ufc-ctan-3.0.0.zip` | `45a8c74f1c36970b8c2f18663e76920d4c53aa9c165922b4151cd13f75b75b60` |
| `abntexto-ufc-overleaf-3.0.0.zip` | `6c099a8510a3deb267da1b383df88a8fce310ba41ae5d58a2a4b80c26100d41b` |
| `abntexto-ufc-template-3.0.0.zip` | `4d8ebea5e97317823d05202dfa52c8f40b2b09dd993e8379c220eedf64aef791` |

## Next actions

| Order | Action | State |
|---:|---|---|
| 1 | Commit synchronized candidate-acceptance documentation and require its Static contract to remain green. | ACTIVE |
| 2 | Merge PR #293 to `main`. | QUEUED |
| 3 | Create `v3.0.0` tag and GitHub Release using the exact retained candidate-produced bytes. | QUEUED |
| 4 | Verify published GitHub asset hashes against the accepted checksums above. | QUEUED |
| 5 | Run current CTAN `pkgcheck`; perform actual CTAN upload only as an explicit publication action and retain receipt/evidence. | QUEUED / EXTERNAL |
| 6 | Synchronize final publication state and perform Release closeout verification before marking Release CLOSED. | QUEUED |

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

The Release phase-end regression is accepted, but the Release phase remains ACTIVE until publication and post-publication verification are recorded. Do not rebuild publication ZIPs, do not weaken tests, do not redistribute proprietary fonts, and do not claim CTAN acceptance without explicit submission/acceptance evidence.
