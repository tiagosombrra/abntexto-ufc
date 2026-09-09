# V3.0.0 Continuation Handoff

Updated: 2026-09-09
Status: RELEASE PUBLICATION CLOSEOUT

This file is the shortest safe entry point for continuing V3 work from a new ChatGPT conversation, Codex session, or local clone.

## Canonical starting point

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical branch | `main` |
| Last merged publication-closeout synchronization checkpoint | `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Release work branch | `release/v3-release`, synchronized to the canonical `main` checkpoint |
| Release PR #293 | merged by squash as `add52f2183f18d6cea3e9477f2a45416a13cfc36` |
| Publication-closeout PR #294 | merged as `c39af06e236b6b61fcf6d11bc383ac5752093cec` |
| Superseded PR #292 | closed; historical evidence only |
| Active roadmap phase | **Release** |
| Immutable Release candidate | `75ead435eabe5157ed17c295ac26fce76438b0ca` — accepted |
| Librarian review | `33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW` |

Always begin by fetching `origin/main`; do not assume a hardcoded HEAD remains the newest commit after later documentation synchronization.

## Accepted Release evidence

| Gate | Accepted result |
|---|---|
| Static contract | `34303586782` — SUCCESS |
| Complete Linux integration | `34303586778` — SUCCESS |
| Linux release check | `34303586773` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0` |
| Reference PDF reproducibility | PASS, SHA-256 `2223030afafdd165b1b7747ea69a95b7e37a58ba4c2122bc2408d97c43547f65`, 450652 bytes |
| Distribution artifact | ID `10086299397`, digest `sha256:c7c6a29bcd34d828883d762d728c4a3a2394f9dc6e796efd4cb50fb3bdc28222` |
| Independent distribution verification | exact five-file set, `SHA256SUMS` PASS, all four ZIP integrity checks PASS |
| Post-merge publication-closeout Static on canonical `main` | `34333350711` — SUCCESS |

Accepted publication assets must be taken from the retained candidate artifact. Do not rebuild them after acceptance.

## Remaining work to finish V3

| Order | Action | State |
|---:|---|---|
| 1 | Create the `v3.0.0` tag and GitHub Release from canonical `main`, attaching the exact retained candidate-produced bytes. | PENDING |
| 2 | Verify every published GitHub asset SHA-256 against the accepted checksums. | PENDING |
| 3 | Run the current CTAN `pkgcheck` on the retained CTAN ZIP. | PENDING |
| 4 | If an actual CTAN upload is performed, retain submission/acceptance evidence; never infer acceptance. | EXTERNAL / EXPLICIT |
| 5 | Synchronize final publication facts in the control plane and perform final Release verification. | PENDING |
| 6 | Mark Release `CLOSED` only after all required publication-closeout evidence is recorded. | BLOCKED BY 1–5 |

Librarian item 33 remains a deliberate authority gap and is not a hidden Release implementation task.

## Local continuation commands

```bash
git fetch --all --prune
git switch main
git pull --ff-only origin main
git status
```

Then read, in this order:

1. `AGENTS.md`
2. `release/v3-roadmap.json`
3. `docs/HANDOFF-V3.0.0.md`
4. `docs/ROADMAP-V3.0.0.md`
5. `docs/V3-RELEASE-READINESS.md`
6. `docs/V3-RELEASE-PHASE-END.md`
7. `docs/CTAN-RELEASE.md`
8. this file

For publication work, create a new short-lived branch from the latest `main`. Do not resume an old superseded PR branch.

## Operating rule

Every **material advance** must update the relevant control documents in the same work cycle. The accepted immutable **phase-end regression** remains the Release evidence anchor; publication verification is an additional closeout obligation and does not authorize rebuilding accepted assets.
