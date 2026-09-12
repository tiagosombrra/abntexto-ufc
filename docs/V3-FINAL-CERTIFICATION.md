# V3 Final Certification

> **Historical evidence — not current release authority.** Retained unchanged in substance for auditability. Use the current v3.0.1 continuation, finalization plan and machine state for live phase/status. See `docs/V3.0.1-DOCUMENT-LIFECYCLE.md` for classification.


Updated: 2026-09-08
Status: CLOSED — ACCEPTED

## Purpose

Final Certification proved the accepted V3 product without reopening closed shared or Scientific Article semantics. Every **material advance** was synchronized with roadmap, handoff, readiness and machine state. Closure required one immutable **phase-end regression** candidate to pass the complete applicable matrix.

## Final step status

| Step | Certification surface | State | Accepted evidence |
|---:|---|---|---|
| 1 | Entry synchronization | ACCEPTED | control plane reconciled |
| 2 | Linux release baseline | ACCEPTED | complete release matrix green |
| 3 | Profile/engine matrix | ACCEPTED | current matrix accepted |
| 4 | Literal Times New Roman/Arial + Unicode + embedding | ACCEPTED | proof `34219229025`; cleanup green |
| 5 | Scientific Article PDF/A-2b | ACCEPTED | bounded + cleanup accepted |
| 6 | Distribution/public bundle integrity | ACCEPTED | bundle integrity accepted |
| 7 | Deterministic release reference PDF / issue #18 | ACCEPTED | `34231038578`; cleanup `34e6bf8...`; issue closed |
| 8 preparation | Release-matrix PR transport | ACCEPTED | `4d94e9c...`; Static `34235990523`; complete Linux `34235990383` |
| 8 candidate `fc907856...` | Phase-end regression | REJECTED | mandatory complete Linux did not execute |
| 8 candidate `22f7ba845...` | Phase-end regression | **ACCEPTED** | Static `34239890649`; complete Linux `34239890614`; release check `34239890548` |

## Phase-end acceptance

Candidate `22f7ba845a8f5ab9c08d4a72ba05a9ff8ebbc1f9` is immutable and accepted:

- Static contract: `34239890649` SUCCESS;
- Linux integration: `34239890614` SUCCESS, `SCOPE=complete PASS=36 FAIL=0 SKIP=0`;
- Linux release check: `34239890548` SUCCESS, `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
- Scientific Article PDF/A-2b PASS;
- distribution/public bundles: 4 artifacts, checksum/archive integrity PASS, proprietary fonts not redistributed;
- release-reference reproducibility: two builds, identical SHA-256 `ae4d7755d18e05abd572a0ad95e5696e54302f9ac236b1efc004d46f57216479`, embedding/PDF validator/PDF-A-2b/Unicode PASS;
- temporary certification executor absent;
- librarian item 33 remains explicit and fail-closed.

`docs/V3-FINAL-CERTIFICATION-PHASE-END.md` is the closure authority for this phase.

## Transition

Final Certification is closed. The synchronized transition removes the one-shot candidate marker and activates **Release**. Release must preserve all accepted certification evidence and conclude with its own complete **phase-end regression** before the phase can be marked closed.
