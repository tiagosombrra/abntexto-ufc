# abntexto-ufc v3.0.0 — Canonical Handoff

Updated: 2026-09-07

## Current checkpoint

| Fact | State |
|---|---|
| Repository | `tiagosombrra/abntexto-ufc` |
| Canonical `main` | `22e3c19235fa5245505b92d919a09d31eb2bfecb` |
| Active branch / PR | `cert/v3-final-certification` / #289 |
| Active phase | **Final Certification** |
| Entry synchronization checkpoint | `aa6cc4a1754bae4ee1b9b89b58441e6cf44d7951` |
| Entry Static | `34161228915` — SUCCESS |
| Entry Linux | `34161228823` — SUCCESS; documentation-only heavy integration skipped |
| Scientific Article phase-end candidate | `923d11ef668b02ec4de3cad4906ad5ac1f527eaf` |
| Article phase-end Static | `34154045481` — SUCCESS |
| Article phase-end Linux | `34154045509` — SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0` |
| Article PDF | build `f62ac703...`; PDF SHA-256 `0152134e22b673318201d345ae1ee42b2f76f29e370dda03923e3dbe8658c9db`; 5/5 visual PASS |
| Scientific Article | **CLOSED** |
| Final Certification | **ACTIVE — LINUX RELEASE BASELINE** |
| Librarian review | **33 PASS / 0 PARTIAL / 0 FAIL / 1 NORMATIVE-REVIEW** |
| Release blocker | issue #18 — deterministic release reference PDF |

## Entry synchronization accepted

The certification branch was created from exact canonical main `22e3c192...`. Checkpoint `aa6cc4a...` synchronized branch/main facts and passed Static `34161228915`. Linux `34161228823` also succeeded and correctly skipped heavy integration because that checkpoint changed documentation/control state only. This closes Final Certification Step 1.

## Immediate action

| Order | Action | Acceptance |
|---:|---|---|
| 1 | Establish current Linux release baseline | execute `make release-check` under the permanent release environment before changing certification machinery |
| 2 | Record baseline result and remove any temporary transport executor | no temporary workflow remains in the accepted checkpoint |
| 3 | Inventory existing profile/engine, literal-font, Unicode, embedding and PDF/A proof routes | reuse valid provenance; identify only genuine final-candidate gaps |
| 4 | Inventory public/distribution bundle checks | no redundant/speculative implementation |
| 5 | Implement/validate issue #18 deterministic reference-PDF proof | pinned epoch, two clean builds, identical SHA-256, existing validation preserved |
| 6 | Assemble final immutable certification candidate | all required proof surfaces bound to one SHA |
| 7 | Run Final Certification phase-end regression | required before Release can become active |

If direct workflow dispatch is unavailable through the active automation surface, a temporary PR executor may call the exact permanent `make release-check` command/environment. It is transport only, must be documented, and must be removed before accepting the baseline checkpoint.

## Hard boundaries

- Preserve accepted shared and Scientific Article behavior unless a real certification regression is discovered.
- Do not use issue #18 to change normative semantics.
- Item 33 remains fail-closed.
- Linux release evidence does not replace literal-font/platform/PDF-A certification.
- Do not redistribute proprietary fonts.
- CTAN/external publication remains blocked until **Release**.

## Mandatory operating discipline

Every **material advance** updates the relevant execution documentation and this handoff in the same work cycle. Every phase requires a complete **phase-end regression** on one immutable SHA; targeted/scoped checks never authorize a phase transition by themselves.
