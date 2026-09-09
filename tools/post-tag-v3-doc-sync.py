#!/usr/bin/env python3
"""Synchronize v3.0.0 post-tag GitHub publication evidence into control docs."""

from __future__ import annotations

import json
import re
import sys
from pathlib import Path
from textwrap import dedent

CERTIFIED = "05399473827da7cf6b6c8bac36edc7115481773f"
TAG_OBJECT = "7354cf912ffa5abb171128554cabce61392ecd84"
RELEASE_ID = 385743477
RELEASE_URL = "https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0"
RELEASE_PUBLISHED_AT = "2026-09-09T18:14:57Z"
DIST_ARTIFACT = 10117679639
DIST_DIGEST = "7ee1b6bf4b1d54ac041db1e624d8bfcf52a1dc43897c1542b9fd969b971f40df"
CTAN_SHA = "d04efb618abb3dd4d99f0b3a5f3ddef3f845381e117aadfec0de087354854f71"
TEMPLATE_SHA = "456df0fb9b82896741fd2a716abe94da6ea34630e6ed1aadb1333e6c9f1d6230"
OVERLEAF_SHA = "b4a3619d2f000e452efdaf8d3465cfafd274dd5a6b2c5c5a42dbc448363001f6"
SUMS_SHA = "bfcf882f2d6764d392bac885e4b2307ce439f78c6349a4bbc41758b5fe532b13"
PKGCHECK_RUN = 34386932488
PKGCHECK_ARTIFACT = 10118176687
PKGCHECK_DIGEST = "e6a4d926d68f68657caca2bab4c1f2ea46cad81bd523c6c55e7f0fa73ea4c4e3"
RELEASE_RUN = 34387825056
RELEASE_EVIDENCE_ARTIFACT = 10118391678
RELEASE_EVIDENCE_DIGEST = "c8ac53d61e6fd1789748163cba6f22d334f4224c1966651baa7a11a334116abc"
LINUX_RELEASE_RUN = 34383793519


def block(value: str) -> str:
    return dedent(value).strip()


def replace_once(root: Path, relative: str, old: str, new: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    if text.count(old) != 1:
        raise SystemExit(f"Expected exactly one match in {relative}: {old!r}")
    path.write_text(text.replace(old, new, 1), encoding="utf-8", newline="\n")


def replace_section(root: Path, relative: str, start: str, end: str, body: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?ms)^{re.escape(start)}\n.*?(?=^{re.escape(end)}\n)")
    replacement = start + "\n\n" + block(body) + "\n\n"
    updated, count = pattern.subn(lambda _: replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace section {start!r} in {relative}")
    path.write_text(updated, encoding="utf-8", newline="\n")


def replace_tail(root: Path, relative: str, start: str, body: str) -> None:
    path = root / relative
    text = path.read_text(encoding="utf-8")
    pattern = re.compile(rf"(?ms)^{re.escape(start)}\n.*?\Z")
    replacement = start + "\n\n" + block(body) + "\n"
    updated, count = pattern.subn(lambda _: replacement, text, count=1)
    if count != 1:
        raise SystemExit(f"Could not replace tail section {start!r} in {relative}")
    path.write_text(updated, encoding="utf-8", newline="\n")


def update_readme(root: Path) -> None:
    marker = "O guia de migração está em [`docs/MIGRATING-TO-V3.md`](docs/MIGRATING-TO-V3.md)."
    replacement = marker + block(
        """

        A versão **3.0.0 está publicada no GitHub** em [`v3.0.0`](https://github.com/tiagosombrra/abntexto-ufc/releases/tag/v3.0.0). O pacote destinado à CTAN já foi certificado, mas a submissão/aceitação pela CTAN ainda não é reivindicada neste repositório; esse estado só será atualizado após evidência externa.
        """
    )
    replace_once(root, "README.md", marker, replacement)


def update_ctan_release(root: Path) -> None:
    replace_section(
        root,
        "docs/CTAN-RELEASE.md",
        "## Current Release state",
        "## Prior CTAN feedback and v3 resolution",
        f"""
        | Fact | State |
        |---|---|
        | Roadmap phase | **Release — GitHub published; CTAN submission pending** |
        | Certified source SHA | `{CERTIFIED}` |
        | Immutable tag | `v3.0.0` → annotated tag object `{TAG_OBJECT}` → certified source SHA |
        | GitHub Release | **PUBLISHED** — [abntexto-ufc 3.0.0]({RELEASE_URL}) |
        | Release publication time | `{RELEASE_PUBLISHED_AT}` |
        | Distribution artifact | Actions artifact `{DIST_ARTIFACT}` — `sha256:{DIST_DIGEST}` |
        | Canonical CTAN ZIP | `abntexto-ufc-3.0.0.zip` — `sha256:{CTAN_SHA}` |
        | CTAN runtime shape | **one generated monolithic `abntexto-ufc.cls`; zero project-owned `.def` files** |
        | `pkgcheck` | **PASS** — 4.1.0, exit 0, 0 warnings, 0 errors/fatals; run `{PKGCHECK_RUN}`, artifact `{PKGCHECK_ARTIFACT}` |
        | GitHub publication verification | **PASS** — recovery run `{RELEASE_RUN}`, evidence artifact `{RELEASE_EVIDENCE_ARTIFACT}` |
        | CTAN submission | **PENDING — not yet claimed** |
        | CTAN acceptance/install | **PENDING — explicit external evidence required** |

        The immutable release bytes are frozen. Post-tag documentation commits may move `main`, but they do not change the source or assets identified by `v3.0.0`.

        The old Actions artifact `10086299397` remains historical regression evidence only and must never be published as v3.0.0.
        """,
    )
    replace_section(
        root,
        "docs/CTAN-RELEASE.md",
        "## Monolithic-class equivalence gate",
        "## pkgcheck is a pre-tag gate",
        f"""
        **PASS on the final publication bytes.** Final certification on `{CERTIFIED}` proved:

        - all 14 tracked project-owned runtime modules incorporated exactly once;
        - no project-owned module remains referenced through `\\input`;
        - no module-level `\\ProvidesFile{{abntexto-ufc/...}}` remains in the generated class;
        - zero `.def` files in the CTAN ZIP;
        - isolated example compilation with only the generated class plus external `abntexto.cls`;
        - deterministic distribution rebuild and checksum verification;
        - no UFC institutional marks or proprietary Microsoft fonts redistributed.

        The final distribution artifact is `{DIST_ARTIFACT}` (`sha256:{DIST_DIGEST}`).
        """,
    )
    replace_section(
        root,
        "docs/CTAN-RELEASE.md",
        "## pkgcheck is a pre-tag gate",
        "## Final certification and publication sequence",
        f"""
        **PASS before tag creation.** CTAN `pkgcheck 4.1.0` was run against the exact canonical ZIP with SHA-256 `{CTAN_SHA}`.

        Evidence: workflow run `{PKGCHECK_RUN}`, artifact `{PKGCHECK_ARTIFACT}` (`sha256:{PKGCHECK_DIGEST}`). Result: exit code 0, zero warnings, zero errors/fatals. The only reported diagnostic was informational (`I0002`).

        Any future package-content change requires a new candidate/version cycle; the v3.0.0 bytes are frozen.
        """,
    )
    replace_section(
        root,
        "docs/CTAN-RELEASE.md",
        "## Final certification and publication sequence",
        "## Proposed CTAN metadata",
        f"""
        Completed and evidenced:

        1. exact canonical source frozen at `{CERTIFIED}`;
        2. Static, complete Linux integration and Linux release check passed on that SHA;
        3. deterministic three-ZIP distribution + `SHA256SUMS` built and retained as artifact `{DIST_ARTIFACT}`;
        4. canonical CTAN ZIP manually audited: one generated class, zero `.def`, isolated compile PASS;
        5. CTAN `pkgcheck 4.1.0` passed with zero warnings/errors before tag creation;
        6. publication hashes frozen; no rebuild occurred;
        7. immutable annotated `v3.0.0` created and verified against the certified SHA;
        8. GitHub Release `{RELEASE_ID}` created with exactly the frozen assets;
        9. draft and published Release assets were re-downloaded and proved byte-identical;
        10. GitHub Release published at `{RELEASE_PUBLISHED_AT}`.

        Pending external CTAN work:

        11. submit **only `abntexto-ufc-3.0.0.zip`** to CTAN;
        12. preserve the CTAN submission receipt and submitted-file identity;
        13. preserve CTAN acceptance/catalog/install evidence;
        14. synchronize final post-CTAN state and close Release.

        Invariant already satisfied for GitHub publication:

        ```text
        certified source SHA == tagged v3.0.0 SHA == source SHA of published GitHub Release bytes
        ```
        """,
    )


def update_handoff(root: Path) -> None:
    replace_section(
        root,
        "docs/HANDOFF-V3.0.0.md",
        "## Current checkpoint",
        "## Completed publication-hardening evidence",
        f"""
        | Fact | Current state |
        |---|---|
        | Repository | `tiagosombrra/abntexto-ufc` |
        | Active phase | **Release — CTAN submission pending** |
        | Certified/tagged source | `{CERTIFIED}` |
        | Immutable tag | `v3.0.0`; tag object `{TAG_OBJECT}` resolves to the certified source |
        | GitHub Release | **PUBLISHED** — {RELEASE_URL} |
        | GitHub publication evidence | run `{RELEASE_RUN}`; artifact `{RELEASE_EVIDENCE_ARTIFACT}` (`sha256:{RELEASE_EVIDENCE_DIGEST}`) |
        | Final distribution artifact | `{DIST_ARTIFACT}` (`sha256:{DIST_DIGEST}`) |
        | Canonical CTAN ZIP | `abntexto-ufc-3.0.0.zip` (`sha256:{CTAN_SHA}`) |
        | CTAN runtime | **one generated `abntexto-ufc.cls`; zero project-owned `.def` files** |
        | `pkgcheck` | **PASS** — 4.1.0, exit 0, 0 warnings/errors; run `{PKGCHECK_RUN}` |
        | Librarian review | **34 PASS / 0 PARTIAL / 0 FAIL / 0 NORMATIVE-REVIEW** |
        | CTAN submission/acceptance | **PENDING; no claim without external evidence** |

        `main` may advance after the immutable tag for documentation/state updates. Git authority for the released source is the `v3.0.0` tag resolving to `{CERTIFIED}`.
        """,
    )
    replace_section(
        root,
        "docs/HANDOFF-V3.0.0.md",
        "## Remaining Release work",
        "## Mandatory operating discipline",
        """
        1. submit only `abntexto-ufc-3.0.0.zip` to CTAN using the frozen GitHub Release asset;
        2. preserve the CTAN submission receipt and submitted-file identity/hash;
        3. wait for explicit CTAN acceptance/catalog evidence; do not infer acceptance from submission;
        4. verify the accepted package identity/version and, when available, installation/catalog propagation;
        5. synchronize post-CTAN documentation and machine state;
        6. mark Release `CLOSED` only after external publication verification.

        The GitHub tag and Release must not be rebuilt, replaced or retargeted.
        """,
    )


def update_continuation(root: Path) -> None:
    replace_once(
        root,
        "docs/V3-CONTINUATION.md",
        "Status: RELEASE — FINAL EXACT-MAIN RECERTIFICATION",
        "Status: RELEASE — GITHUB PUBLISHED / CTAN PENDING",
    )
    replace_section(
        root,
        "docs/V3-CONTINUATION.md",
        "## Canonical starting point",
        "## What publication hardening already closed",
        f"""
        | Fact | Current state |
        |---|---|
        | Repository | `tiagosombrra/abntexto-ufc` |
        | Released source | `{CERTIFIED}` |
        | Immutable tag | `v3.0.0` → `{CERTIFIED}` |
        | GitHub Release | **PUBLISHED** — {RELEASE_URL} |
        | Final distribution artifact | `{DIST_ARTIFACT}` (`sha256:{DIST_DIGEST}`) |
        | Canonical CTAN upload | `abntexto-ufc-3.0.0.zip` (`sha256:{CTAN_SHA}`) |
        | CTAN runtime contract | one generated `abntexto-ufc.cls`; **zero project-owned `.def` files** |
        | `pkgcheck` | **PASS** — 4.1.0, exit 0, zero warnings/errors; run `{PKGCHECK_RUN}` |
        | GitHub publication verification | **PASS** — run `{RELEASE_RUN}`; evidence artifact `{RELEASE_EVIDENCE_ARTIFACT}` |
        | CTAN status | **NOT YET CLAIMED — submission/acceptance pending** |

        For released-source authority, resolve `v3.0.0`; do not treat a later post-tag `main` commit as the v3.0.0 source.
        """,
    )
    replace_section(
        root,
        "docs/V3-CONTINUATION.md",
        "## Remaining work",
        "## Local continuation",
        f"""
        1. obtain the exact `abntexto-ufc-3.0.0.zip` asset from the published GitHub Release;
        2. verify SHA-256 `{CTAN_SHA}`;
        3. submit only that archive to CTAN;
        4. preserve submission receipt and package metadata;
        5. after CTAN acceptance, verify catalog/install evidence;
        6. update control docs/machine state and close the Release phase.

        No v3.0.0 source or asset rebuild is permitted.
        """,
    )


def update_roadmap(root: Path) -> None:
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## Current status",
        "## R0 — Publication documentation and package identity",
        f"""
        **Release is ACTIVE — GitHub publication is complete; CTAN submission/acceptance remains.** The immutable `v3.0.0` tag resolves to `{CERTIFIED}`, and GitHub Release `{RELEASE_ID}` is published with byte-verified frozen assets.

        | Phase | Status | Exit requirement |
        |---|---|---|
        | Regression Audit | CLOSED | accepted |
        | Core Corrections | CLOSED | accepted phase-end regression |
        | Reference PDF Validation | CLOSED | 55/55 visual PASS + Static/Linux |
        | Scientific Article | CLOSED | complete Linux + 5/5 visual PASS |
        | Final Certification | CLOSED | heavy technical matrix accepted |
        | Release | **ACTIVE — CTAN PENDING** | GitHub publication PASS; submit canonical ZIP to CTAN, preserve receipt/acceptance evidence, then close |

        ## Current Release facts

        | Predicate | Current result |
        |---|---|
        | Certified source SHA | `{CERTIFIED}` |
        | Immutable tag | `v3.0.0` → `{CERTIFIED}` |
        | GitHub Release | **PUBLISHED** — {RELEASE_URL} |
        | Distribution artifact | `{DIST_ARTIFACT}` (`sha256:{DIST_DIGEST}`) |
        | CTAN upload archive | `abntexto-ufc-3.0.0.zip` only (`sha256:{CTAN_SHA}`) |
        | CTAN project runtime | **`abntexto-ufc.cls` only; 0 `.def`** |
        | `pkgcheck` | **PASS** — 4.1.0, zero warnings/errors |
        | GitHub asset re-download | **PASS / byte-identical** |
        | CTAN submission | **PENDING** |
        | CTAN acceptance/install | **PENDING** |
        """,
    )
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## R3 — Final exact-main recertification",
        "## R4 — CTAN `pkgcheck`",
        f"""
        **CLOSED / PASS.** Exact source `{CERTIFIED}` passed Static, complete Linux integration, Linux release check (`SCOPE=complete PASS=38 FAIL=0 SKIP=0`), deterministic distribution and final package audit.
        """,
    )
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## R4 — CTAN `pkgcheck`",
        "## R5 — Freeze, tag and GitHub Release",
        f"""
        **CLOSED / PASS.** `pkgcheck 4.1.0` passed on `{CTAN_SHA}` with exit 0, zero warnings and zero errors/fatals. Evidence run `{PKGCHECK_RUN}` / artifact `{PKGCHECK_ARTIFACT}`.
        """,
    )
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## R5 — Freeze, tag and GitHub Release",
        "## R6 — CTAN submission",
        f"""
        **CLOSED / PASS.** Frozen bytes were tagged as immutable `v3.0.0`, published in GitHub Release `{RELEASE_ID}`, re-downloaded before and after publication and proved byte-identical. Recovery verification run `{RELEASE_RUN}` retained evidence artifact `{RELEASE_EVIDENCE_ARTIFACT}`.
        """,
    )
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## R6 — CTAN submission",
        "## R7 — Release closeout",
        """
        **ACTIVE / PENDING EXTERNAL ACTION.** Submit exactly one file: `abntexto-ufc-3.0.0.zip`. Preserve receipt, submitted hash and later acceptance/catalog/install evidence.
        """,
    )
    replace_section(
        root,
        "docs/ROADMAP-V3.0.0.md",
        "## R7 — Release closeout",
        "## Operating discipline",
        """
        **BLOCKED ONLY BY R6 EXTERNAL VERIFICATION.** After CTAN acceptance/catalog evidence, synchronize final state and mark Release `CLOSED`.
        """,
    )


def update_readiness(root: Path) -> None:
    replace_once(
        root,
        "docs/V3-RELEASE-READINESS.md",
        "Status: ACTIVE — FINAL EXACT-MAIN RECERTIFICATION",
        "Status: ACTIVE — GITHUB PUBLISHED / CTAN PENDING",
    )
    replace_section(
        root,
        "docs/V3-RELEASE-READINESS.md",
        "## Phase readiness",
        "## Completed Release hardening",
        f"""
        | Phase | State | Evidence / pending work |
        |---|---|---|
        | Regression Audit | CLOSED | phase-end regression accepted |
        | Core Corrections | CLOSED | accepted |
        | Reference PDF Validation | CLOSED | 55/55 visual PASS |
        | Scientific Article | CLOSED | complete Linux + article PDF 5/5 visual PASS |
        | Final Certification | CLOSED | technical/runtime certification accepted |
        | Release | **ACTIVE — CTAN PENDING** | exact source certified; pkgcheck/tag/GitHub publication PASS; only CTAN external submission/acceptance remains |

        GitHub v3.0.0 publication is complete and byte-verified. The Release phase remains active only because CTAN submission and acceptance are external gates.
        """,
    )
    replace_section(
        root,
        "docs/V3-RELEASE-READINESS.md",
        "## Remaining gates",
        "## Current blockers",
        f"""
        | Order | Gate | State |
        |---:|---|---|
        | 1 | Publication-hardening integration | **PASS / MERGED** |
        | 2 | Post-merge control-plane synchronization | **PASS / MERGED** |
        | 3 | Exact resulting source SHA resolved | **PASS — `{CERTIFIED}`** |
        | 4 | Static + complete Linux + Linux release check on exact SHA | **PASS** |
        | 5 | Deterministic three-ZIP distribution + `SHA256SUMS` | **PASS — artifact `{DIST_ARTIFACT}`** |
        | 6 | Final CTAN ZIP audit: one class, zero `.def`, isolated compile | **PASS** |
        | 7 | Current CTAN `pkgcheck` | **PASS — 4.1.0, zero warnings/errors** |
        | 8 | Freeze hashes/evidence; prohibit rebuild | **PASS** |
        | 9 | Immutable `v3.0.0` on certified SHA | **PASS** |
        | 10 | GitHub Release + re-download/hash verification | **PASS — Release `{RELEASE_ID}`** |
        | 11 | Submit canonical ZIP to CTAN; preserve receipt/acceptance evidence | **PENDING EXTERNAL ACTION** |
        | 12 | Synchronize final CTAN facts and close Release | **BLOCKED BY 11** |
        """,
    )
    replace_tail(
        root,
        "docs/V3-RELEASE-READINESS.md",
        "## Current blockers",
        """
        - the canonical ZIP has not yet been submitted to CTAN with retained receipt evidence;
        - CTAN acceptance/catalog/install evidence does not yet exist.

        GitHub publication is complete and verified. No v3.0.0 source or asset rebuild is permitted. Every subsequent material advance updates affected documentation and machine state in the same work cycle.
        """,
    )


def update_phase_end(root: Path) -> None:
    replace_once(
        root,
        "docs/V3-RELEASE-PHASE-END.md",
        "Status: FINAL EXACT-MAIN RECERTIFICATION REQUIRED",
        "Status: PASS — GITHUB PUBLICATION VERIFIED / CTAN EXTERNAL CLOSEOUT PENDING",
    )
    replace_section(
        root,
        "docs/V3-RELEASE-PHASE-END.md",
        "## Purpose",
        "## Historical candidates",
        f"""
        This document records the completed technical Release phase-end regression for v3.0.0 and the remaining external CTAN closeout boundary. The released source is immutable at `{CERTIFIED}`; GitHub publication is complete and verified, while CTAN submission/acceptance is still pending explicit external evidence.
        """,
    )
    replace_section(
        root,
        "docs/V3-RELEASE-PHASE-END.md",
        "## Final candidate definition",
        "## Minimum final evidence",
        f"""
        The accepted Release candidate is `{CERTIFIED}`. It is the exact source commit certified by the final gates and resolved by immutable annotated tag `v3.0.0` through tag object `{TAG_OBJECT}`.

        The GitHub Release uses only frozen assets produced from that source. Later post-tag documentation commits may move `main`; they do not alter the v3.0.0 source or publication bytes.

        Required invariant is satisfied:

        ```text
        certified source SHA == tagged v3.0.0 SHA == source SHA of published release bytes
        ```
        """,
    )
    replace_section(
        root,
        "docs/V3-RELEASE-PHASE-END.md",
        "## Minimum final evidence",
        "## Canonical CTAN package",
        f"""
        All pre-publication technical gates are **PASS**:

        1. Static contract on `{CERTIFIED}` — PASS;
        2. automatic complete Linux integration on `{CERTIFIED}` — PASS;
        3. Linux release check run `{LINUX_RELEASE_RUN}` — `SCOPE=complete PASS=38 FAIL=0 SKIP=0`;
        4. applicable platform/font/PDF-A evidence — PASS;
        5. deterministic three-ZIP distribution + `SHA256SUMS` — PASS;
        6. canonical CTAN structural/semantic gate — PASS;
        7. exactly one project-owned runtime implementation file (`abntexto-ufc.cls`) — PASS;
        8. zero project-owned `.def` files and no nested runtime module directory — PASS;
        9. all 14 project-owned runtime modules inlined exactly once — PASS;
        10. isolated minimal CTAN example compilation — PASS;
        11. CTAN `pkgcheck 4.1.0` on SHA-256 `{CTAN_SHA}` — exit 0, 0 warnings, 0 errors/fatals;
        12. frozen asset hashes and retained pre-tag evidence — PASS.

        GitHub Release publication and post-publication re-download comparison are also PASS. The only remaining Release boundary is external CTAN submission/acceptance evidence.
        """,
    )
    replace_section(
        root,
        "docs/V3-RELEASE-PHASE-END.md",
        "## Required order",
        "Every material repository modification updates affected documentation and machine state in the same work cycle. The public README does not carry transient branch or CI state.",
        f"""
        Completed:

        1. protected-main control-plane synchronization;
        2. exact source resolution at `{CERTIFIED}`;
        3. Static, complete Linux integration and Linux release check;
        4. final CTAN ZIP retention/manual audit;
        5. current `pkgcheck` on the exact canonical bytes;
        6. byte/hash freeze;
        7. immutable `v3.0.0` tag;
        8. GitHub Release publication and byte-identical re-download verification.

        Pending:

        9. submit the one canonical ZIP to CTAN and retain receipt evidence;
        10. verify CTAN acceptance/catalog/install state, synchronize documentation/machine state and close Release.
        """,
    )


def update_candidate_json(root: Path) -> None:
    path = root / "release/v3-release-candidate.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["schema_version"] = max(int(data.get("schema_version", 0)) + 1, 5)
    data["purpose"] = "Immutable v3.0.0 GitHub publication record; CTAN submission and acceptance remain pending external evidence"
    data["candidate_semantics"] = f"certified source {CERTIFIED}, tagged immutably as v3.0.0 and published with frozen GitHub Release assets"
    data["final_candidate"] = {
        "status": "certified-tagged-github-release-published-ctan-pending",
        "source_branch_at_certification": "main",
        "certified_source_sha": CERTIFIED,
        "static_status": "PASS",
        "complete_linux_status": "PASS",
        "linux_release_run": LINUX_RELEASE_RUN,
        "linux_release_summary": "SCOPE=complete PASS=38 FAIL=0 SKIP=0",
        "distribution_artifact_id": DIST_ARTIFACT,
        "distribution_artifact_sha256": DIST_DIGEST,
        "ctan_zip_sha256": CTAN_SHA,
        "pkgcheck": {
            "version": "4.1.0",
            "run_id": PKGCHECK_RUN,
            "artifact_id": PKGCHECK_ARTIFACT,
            "artifact_sha256": PKGCHECK_DIGEST,
            "exit_code": 0,
            "warnings": 0,
            "errors_or_fatals": 0,
            "status": "PASS",
        },
        "tag": "v3.0.0",
        "tag_object_sha": TAG_OBJECT,
        "tag_resolves_to_certified_source": True,
        "github_release": {
            "id": RELEASE_ID,
            "url": RELEASE_URL,
            "published_at": RELEASE_PUBLISHED_AT,
            "draft": False,
            "prerelease": False,
            "asset_count": 4,
            "recovery_verification_run": RELEASE_RUN,
            "evidence_artifact_id": RELEASE_EVIDENCE_ARTIFACT,
            "evidence_artifact_sha256": RELEASE_EVIDENCE_DIGEST,
            "assets_byte_identical_after_redownload": True,
        },
        "no_pre_tag_commits_after_acceptance": True,
        "publication_rebuild_allowed": False,
    }
    data["ctan_upload"].update(
        {
            "archive_sha256": CTAN_SHA,
            "submission_status": "pending-not-submitted",
            "acceptance_status": "pending-no-external-evidence",
        }
    )
    data["final_tag_contract"].update(
        {
            "status": "satisfied",
            "tag_object_sha": TAG_OBJECT,
            "certified_source_sha": CERTIFIED,
        }
    )
    data["github_publication"] = {
        "status": "published-and-byte-verified",
        "release_id": RELEASE_ID,
        "release_url": RELEASE_URL,
        "published_at": RELEASE_PUBLISHED_AT,
        "asset_sha256": {
            "abntexto-ufc-3.0.0.zip": CTAN_SHA,
            "abntexto-ufc-template-3.0.0.zip": TEMPLATE_SHA,
            "abntexto-ufc-overleaf-3.0.0.zip": OVERLEAF_SHA,
            "SHA256SUMS": SUMS_SHA,
        },
    }
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def update_roadmap_json(root: Path) -> None:
    path = root / "release/v3-roadmap.json"
    data = json.loads(path.read_text(encoding="utf-8"))
    data["schema_version"] = int(data.get("schema_version", 0)) + 1
    data["status"] = "ACTIVE"
    data["phase_end_regression"]["candidate_state"] = "certified-tagged-github-release-published"
    active = data["active_work"]
    active["release_state"] = "github-release-published-ctan-submission-pending"
    active["current_correction_batch"] = [
        "Submit the frozen canonical abntexto-ufc-3.0.0.zip to CTAN",
        "Preserve CTAN submission receipt and submitted-file identity",
        "Verify CTAN acceptance/catalog/install evidence",
        "Synchronize final publication state and close Release",
    ]
    active["pending_acceptance_gates"] = [
        "Submit exactly one frozen canonical ZIP to CTAN and preserve receipt evidence",
        "Verify CTAN acceptance/catalog/install evidence",
        "Record final external publication verification before Release closure",
    ]
    active["release_blockers"] = [
        "CTAN submission receipt has not yet been recorded",
        "CTAN acceptance/catalog/install evidence has not yet been recorded",
    ]
    active["distribution_contract"].update(
        {
            "state": "final-publication-bytes-frozen-and-github-published",
            "final_distribution_artifact_id": DIST_ARTIFACT,
            "final_distribution_artifact_sha256": DIST_DIGEST,
            "ctan_archive_sha256": CTAN_SHA,
            "pkgcheck_version": "4.1.0",
            "pkgcheck_status": "PASS",
            "pkgcheck_run_id": PKGCHECK_RUN,
            "pkgcheck_artifact_id": PKGCHECK_ARTIFACT,
            "github_release_id": RELEASE_ID,
            "github_release_url": RELEASE_URL,
            "github_assets_byte_verified": True,
            "ctan_submission_status": "pending-not-submitted",
            "ctan_acceptance_status": "pending-no-external-evidence",
        }
    )
    active["final_candidate_contract"].update(
        {
            "state": "certified-tagged-and-github-published",
            "certified_source_sha": CERTIFIED,
            "tag_object_sha": TAG_OBJECT,
            "tag_resolves_to_certified_source": True,
            "github_release_published": True,
            "github_release_id": RELEASE_ID,
            "github_assets_byte_verified": True,
        }
    )
    active["github_publication"] = {
        "status": "PASS",
        "certified_source_sha": CERTIFIED,
        "tag": "v3.0.0",
        "tag_object_sha": TAG_OBJECT,
        "release_id": RELEASE_ID,
        "release_url": RELEASE_URL,
        "published_at": RELEASE_PUBLISHED_AT,
        "distribution_artifact_id": DIST_ARTIFACT,
        "canonical_ctan_zip_sha256": CTAN_SHA,
        "pkgcheck_run_id": PKGCHECK_RUN,
        "pkgcheck_version": "4.1.0",
        "pkgcheck_warnings": 0,
        "pkgcheck_errors_or_fatals": 0,
        "release_verification_run_id": RELEASE_RUN,
        "release_verification_artifact_id": RELEASE_EVIDENCE_ARTIFACT,
        "release_verification_artifact_sha256": RELEASE_EVIDENCE_DIGEST,
    }
    data["branch_plan"].update(
        {
            "current_work_branch": "main",
            "current_work_state": "post-github-publication-ctan-pending",
            "released_source_is_tag_authoritative": True,
            "released_source_sha": CERTIFIED,
            "post_tag_main_commits_do_not_change_v3_release_source": True,
        }
    )
    path.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8", newline="\n")


def main() -> None:
    root = Path(sys.argv[1] if len(sys.argv) > 1 else ".").resolve()
    update_readme(root)
    update_ctan_release(root)
    update_handoff(root)
    update_continuation(root)
    update_roadmap(root)
    update_readiness(root)
    update_phase_end(root)
    update_candidate_json(root)
    update_roadmap_json(root)

    for relative in ("release/v3-release-candidate.json", "release/v3-roadmap.json"):
        json.loads((root / relative).read_text(encoding="utf-8"))

    print("Post-tag v3.0.0 publication documentation synchronized; CTAN remains explicitly pending.")


if __name__ == "__main__":
    main()
