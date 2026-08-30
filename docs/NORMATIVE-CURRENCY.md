# Normative Currency Policy

Updated: 2026-08-30

`abntexto-ufc` follows the most recent applicable technical edition that is currently in force. An older ABNT edition does not govern an active requirement merely because it is cited by an older UFC guide.

## Decision rule

For technical requirements:

**current applicable ABNT standard → compatible/complementary current UFC requirement → current UFC guide → implementation**.

For institutional requirements:

**current UFC act → current UFC institutional requirement → current UFC guide → applicable technical standard → implementation**.

Current-source conflicts are review items and must not be resolved silently.

## Explicit technical supersessions

The following older editions are contextual only for the active v3 baseline:

- ABNT NBR 14724:2011 → ABNT NBR 14724:2024;
- ABNT NBR 6023:2018 → ABNT NBR 6023:2025;
- ABNT NBR 10520:2002 → ABNT NBR 10520:2023;
- ABNT NBR 12225:2004 → ABNT NBR 12225:2023;
- ABNT NBR 15287:2011 → ABNT NBR 15287:2025.

An older publication year does not imply obsolescence when no superseding edition exists. Currency is determined by normative status, not by year alone.

## UFC guides

UFC normalization guides are institutional sources interpreted under the precedence rule above. When a guide cites a superseded technical edition, compatible institutional guidance may remain useful, but the superseded edition does not become technically governing again.

## Scientific articles

Scientific-article support is intentionally outside the active foundation scope until V3-A1. The previously researched article source contract is preserved by Git history rather than by dormant v3 files. When V3-A1 starts, article sources and predicates must be reconfirmed against then-current technical and UFC institutional sources before runtime implementation resumes.

## Source updates

When a new technical edition or UFC act is identified:

1. review the source before changing runtime behavior;
2. identify every affected rule and locator;
3. update current machine-readable contracts under `standards/`;
4. remove superseded active authority from the current contract;
5. reconcile implementation, tests, validator behavior, and active documentation;
6. certify the exact candidate head only after the source transition is internally consistent.

Historical source states remain available through Git and release history; they are not duplicated into active repository archive directories.
