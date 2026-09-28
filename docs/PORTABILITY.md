# Portability coverage

This document describes the bounded cross-platform CI evidence retained by `abntexto-ufc`. Linux remains the release-grade authority; Windows and macOS add targeted portability proofs rather than duplicate the complete release matrix.

## Linux

Linux CI owns the full integration and release certification surface. The release workflow executes the complete repository release contract, distribution/public bundle checks, canonical-reference reproducibility, CTAN pkgcheck and release-review-pair generation.

## Windows

`.github/workflows/windows-smoke.yml` proves the repository's Windows-specific literal-font path on Windows Server 2025.

It provisions pinned TeX Live 2026, runs the repository-owned Times New Roman/Arial preparation pipeline, compiles strict pdfLaTeX and LuaLaTeX proofs and uploads only generated PDFs. A dependent Ubuntu job certifies literal font identity, Unicode extraction, embedding and PDF/A-2b. Microsoft font binaries are never tracked or uploaded.

Detailed support rules remain in [WINDOWS-FONT-SUPPORT.md](WINDOWS-FONT-SUPPORT.md).

## macOS

`.github/workflows/macos-smoke.yml` provides a distinct Darwin/Apple-Silicon portability proof.

The build job is pinned to `macos-26` and fails unless the host reports Darwin on `arm64`. TeX Live 2026 is provisioned explicitly through the same SHA-pinned setup action used by the Windows smoke.

The macOS job materializes the repository-pinned upstream `abntexto` source and compiles the canonical public tutorial `template/main.tex` with both pdfLaTeX and LuaLaTeX through the normal Makefile entry point. It uploads exactly two generated PDFs.

A dependent Ubuntu job reuses the existing font-embedding and PDF/A-2b contracts against those exact macOS-produced PDFs. The macOS smoke intentionally does not run the full release suite and does not reproduce the Windows literal-Microsoft-font preparation path.

## Boundaries

- Linux is the authoritative full release-grade environment.
- Windows proves Windows-specific path/font preparation behavior.
- macOS proves Darwin + ARM64 public-template compilation.
- Cross-platform smokes fail closed; `continue-on-error` is not an accepted portability policy.
- Published v3.0.4 release/tag/archive bytes remain immutable.
- No cross-platform workflow may redistribute proprietary system fonts.
