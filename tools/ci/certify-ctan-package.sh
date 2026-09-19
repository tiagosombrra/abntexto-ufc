#!/bin/sh
set -eu

: "${SOURCE_COMMIT_SHA:?SOURCE_COMMIT_SHA is required}"
: "${RELEASE_VERSION:?RELEASE_VERSION is required}"

mkdir -p artifacts/validation /tmp/ctan-pkgcheck /tmp/ctan-candidate
test -s .ci-downloads/pkgcheck.zip
cp .ci-downloads/pkgcheck.zip /tmp/pkgcheck.zip
unzip -q /tmp/pkgcheck.zip -d /tmp/ctan-pkgcheck

PKGCHECK="$(find /tmp/ctan-pkgcheck -type f \
  \( -name 'pkgcheck-x86_64-unknown-linux-musl' -o -name 'pkgcheck' \) \
  -print -quit)"
if [ -z "$PKGCHECK" ]; then
  for candidate in $(find /tmp/ctan-pkgcheck -type f -name 'pkgcheck-x86_64-unknown-linux-musl*' -print | sort); do
    case "$(basename "$candidate")" in
      *.asc|*.sha*|*.sig|*.txt)
        continue
        ;;
    esac
    PKGCHECK="$candidate"
    break
  done
fi
if [ -z "$PKGCHECK" ]; then
  echo 'Current CTAN pkgcheck archive did not contain a supported Linux binary.'
  find /tmp/ctan-pkgcheck -maxdepth 4 -type f -printf '%P\n' | sort
  exit 1
fi

chmod +x "$PKGCHECK"
"$PKGCHECK" --version > artifacts/validation/pkgcheck-version.txt 2>&1
cat artifacts/validation/pkgcheck-version.txt

sha256sum "dist/abntexto-ufc-$RELEASE_VERSION.zip" > artifacts/validation/pkgcheck-archive.sha256
unzip -q "dist/abntexto-ufc-$RELEASE_VERSION.zip" -d /tmp/ctan-candidate

if ! "$PKGCHECK" --no-colors -d /tmp/ctan-candidate/abntexto-ufc \
  > artifacts/validation/pkgcheck.log 2>&1; then
  cat artifacts/validation/pkgcheck.log
  echo 'CTAN pkgcheck failed.'
  exit 1
fi

cat artifacts/validation/pkgcheck.log
printf '%s\n' \
  "FINAL-CERTIFICATION-EVIDENCE surface=ctan-pkgcheck status=PASS source_sha=$SOURCE_COMMIT_SHA archive=abntexto-ufc-$RELEASE_VERSION.zip" \
  | tee artifacts/validation/pkgcheck-evidence.txt

# Produce exact-source material for the mandatory human review gate only after
# technical release and CTAN package checks have passed.
sh tests/integration/release-review-pairs.sh
