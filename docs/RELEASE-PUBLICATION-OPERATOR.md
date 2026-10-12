# v3.0.5 publication handoff — authenticated operator

This runbook records the current external publication dependency. Before action, reconcile live GitHub state; do not infer it from this dated snapshot. Authority: `release/v3-release-candidate.json`, `docs/RELEASE-STATE.md`, and issue #475.

## Identity and gates

- **Certified and visually ACCEPTED publication source:** `30ff9b7bc777db28584fce7e96930e748ee1a661` (tree `4b2a64e5c318ef761d84364877000086d51f1664`). **Not** the later control-plane `main`.
- **Frozen control-plane baseline:** `9e0de03d805798650bb6972f282741ff9164b301` from PR #481 (Static `38065763832`, complete Linux Integration `38065763807`, Linux Release `38065763818` — all PASS).
- **Explicit maintainer ACCEPT:** 2026-10-10, exact-source seven-profile artifact `11670542808`, sha256 `8aaff1d8b317034470470d4acd10af20518e1ac791b3d7e8b7ba5231817f1886`.
- **Original distribution artifact:** Actions run `38052629238`, artifact ID `11670527758`, name `abntexto-ufc-v3.0.5-distribution-38052629238`. Outer ZIP sha256 `ed4eb70d1b06e09c38e70b35d505e552c90f72c9d3cc982874b79f0f2020df1c`.
- **Certified inner release bytes:**

| Asset | SHA-256 |
|---|---|
| `abntexto-ufc-3.0.5.zip` | `b57e2f4f17d5a707e93a30f5fe701f0f14606fc39c01d6f09b6e8a3781e652e8` |
| `abntexto-ufc-template-3.0.5.zip` | `a6433d7e698a8e89a39761a7ea5951b267cce2169844827410fdc958da39196a` |
| `abntexto-ufc-overleaf-3.0.5.zip` | `082255fddec80f6e6aeee17f6781d579d3c488c8571a456018aa3524eade7e3d` |
| `SHA256SUMS` | `6fcb6ce5c8c56cee4c08c5f719280bf36e8422d81950c052db63b4f142e9df95` |

## Operator sequence (PowerShell; authenticated `git` and `gh` required)

1. Confirm GitHub `v3.0.5` annotated tag and release **do not yet exist** (if they exist, inspect them, do not overwrite). Confirm frozen marker still accepts only the source above, source certification and maintainer acceptance, and three post-merge runs green. Confirm available permissions with `gh auth status`. If `main` advanced, reconcile every changed path; stop if any freeze/publication input changed.
2. Retrieve **existing** distribution artifact by Actions run and artifact name (or use a byte-identical previously downloaded archive). Example:

   ```powershell
   gh run download 38052629238 --repo tiagosombrra/abntexto-ufc --name abntexto-ufc-v3.0.5-distribution-38052629238 --dir .\v305-certified
   ```

   GitHub CLI may extract this artifact directly into that directory. Verify the four SHA256 above with `Get-FileHash`, verify `SHA256SUMS`, and do not modify any file.
3. From an authenticated local clone with the accepted source reachable, ensure the remote is exactly this repository and no remote `v3.0.5` tag exists. Create an **annotated** tag on the *source*:

   ```powershell
   git fetch origin main --tags
   git tag -a v3.0.5 30ff9b7bc777db28584fce7e96930e748ee1a661 -m 'abntexto-ufc v3.0.5 - certified maintainer accepted source'
   git rev-parse 'v3.0.5^{commit}'
   git push origin refs/tags/v3.0.5:refs/tags/v3.0.5
   ```

   The peeled result **must** equal `30ff9b7bc777db28584fce7e96930e748ee1a661`. On GitHub, verify ref type is `tag` (not lightweight `commit`), then the annotated tag object targets that exact commit.
4. Create a **draft** GitHub Release on that *existing* tag using `gh release create v3.0.5 ... --repo tiagosombrra/abntexto-ufc --verify-tag --draft`, passing **all four certified original files**, release title and reviewed notes. Inspect `gh api repos/tiagosombrra/abntexto-ufc/releases/tags/v3.0.5`: server-reported asset `digest`, size and names must match the four certified originals.
5. **Only after four matching remote digests**, publish the draft with `gh release edit v3.0.5 --repo tiagosombrra/abntexto-ufc --draft=false --latest`. Recheck the annotated tag target, server asset digests and that the GitHub release is actually published. Record immutable GitHub Release ID, published timestamp, annotated tag object SHA and asset IDs/digests in issue #475.
6. Synchronize `release/v3-release-candidate.json`, `docs/RELEASE-STATE.md`, AGENTS and roadmap to actual `PUBLISHED` **in a separate, green-gated PR**, preserving the historical v3.0.4 receipt. Then open the CTAN submission follow-up with the *exact* already-published canonical ZIP; GitHub publication does not imply CTAN acceptance.

**Failure policy:** no force push, tag retarget, release overwrite, `--clobber` or rebuilt zip. If publication fails after creating tag or draft, stop and reconcile what actually exists; do not silently delete a remotely visible tag or release.

**Connected-tool boundary as of 2026-10-12:** GitHub connector cannot create annotated Git tags or upload GitHub Release assets. Publication requires an authenticated maintainer environment and explicit verification of all server-side receipts. An optional verified distribution-and-PowerShell operator kit was delivered in the maintainers' conversation; this runbook plus the retained Actions artifacts is sufficient if the kit is unavailable.
