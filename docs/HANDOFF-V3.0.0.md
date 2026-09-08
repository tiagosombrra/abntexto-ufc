# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-08

## Current checkpoint

| Fact | Current state |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Steps 1-3 | ACCEPTED |
| Steps 5-6 | ACCEPTED |
| Step 4 proof | PASS — bounded run `34219229025`, source `fae338e16304ad45c353067a0b7982f73a8363c5` |
| Step 4 evidence | Times New Roman/Arial × pdfLaTeX/LuaLaTeX; literal identity, Unicode, embedding and PDF/A-2b PASS |
| Step 4 artifact | generated PDFs only, artifact `10053151610`, digest `sha256:6b0cd0a6ac2543017a8496a1af7feeca70640f2b73862311a4325a981dc5fb60`, one-day retention |
| Temporary executor | `.github/workflows/final-cert-literal-fonts.yml` REMOVED after successful evidence capture |
| Current batch | **Step 4 — cleanup Static/Linux validation** |
| Next blocker | issue #18 deterministic reference PDF |
| Item 33 | remains fail-closed; not a release implementation task |

Canonical control documents are `release/v3-roadmap.json`, `docs/ROADMAP-V3.0.0.md`, `docs/V3-FINAL-CERTIFICATION.md`, `docs/V3-RELEASE-READINESS.md`, `docs/LINUX-INTEGRATION-SCOPES.md`, `docs/UFC-LIBRARIAN-REVIEW.md`, and this handoff.

## Step 4 result and cleanup boundary

Run `34219229025` completed successfully on `fae338e...`. The Windows job generated four strict PDFs using fonts already present on the Windows runner. The downstream Linux job certified all four combinations and emitted the structured PASS record for literal family identity, Unicode extraction, embedding and PDF/A-2b. No raw proprietary font files were transported.

The proof-only workflow has been removed. Step 4 remains open until the resulting cleanup checkpoint passes both Static contract and Linux integration. A cleanup failure must be classified before any correction; the accepted proof predicates are not weakened.

## Immediate action

1. finish the current documentation/machine-state synchronization after removal of the temporary workflow;
2. wait for Static and Linux on the cleanup checkpoint;
3. if both pass, mark Step 4 ACCEPTED and record the cleanup SHA/run IDs;
4. resolve issue #18 deterministic reference-PDF reproducibility;
5. execute Final Certification **phase-end regression** on one immutable SHA;
6. only then activate Release.

## Mandatory operating discipline

Every **material advance** updates relevant execution documentation, this handoff, roadmap and machine state in the same work cycle. Targeted checks never replace the **phase-end regression**.

## Hard boundaries

- Preserve accepted shared and Scientific Article semantics absent a concrete regression.
- Do not weaken tests to obtain green CI.
- Do not redistribute proprietary Microsoft fonts.
- Librarian item 33 remains fail-closed.
- Do not perform CTAN or other external publication before **Release**.
