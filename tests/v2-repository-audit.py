#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tests/v2-repository-audit.py'

TEXT_SUFFIXES = {
    '.bib', '.cls', '.def', '.md', '.py', '.sh', '.tex', '.txt', '.yml', '.yaml',
    '.ps1', '.cpp', '.c', '.h', '.hpp', '.json', '.toml', '.cfg', '.rc',
}
GENERATED_SUFFIXES = {
    '.aux', '.bbl', '.bcf', '.blg', '.fdb_latexmk', '.fls', '.glg', '.glo', '.gls',
    '.idx', '.ilg', '.ind', '.lof', '.log', '.lot', '.out', '.run.xml', '.synctex.gz',
    '.toc', '.pyc', '.zip',
}
FORBIDDEN_LEGACY_PATHS = {
    'ufctex/compat-v1.def',
    'tests/v1-regression-check.sh',
    'tests/v2-posttextual-compat-check.sh',
}
FORBIDDEN_LEGACY_PREFIXES = (
    'lib/',
    'tests/compat/',
)
LEGACY_CONTENT_EXEMPT = (
    SELF,
    'tests/v2-distribution-check.sh',
)
LEGACY_PATTERNS = {
    'abntex2': re.compile(r'\babntex2\b', re.IGNORECASE),
    'legacy lib reference': re.compile(
        r'(?<![A-Za-z0-9_-])lib/(?:logo-ufc(?:\.PNG)?|preambulo|ufctex)',
        re.IGNORECASE,
    ),
    'legacy logo': re.compile(r'logo-ufc\.PNG', re.IGNORECASE),
    'legacy Caption': re.compile(r'\\Caption\b'),
    'legacy Fonte': re.compile(r'\\Fonte\b'),
    'legacy UFC object helper': re.compile(r'\\UFC(?:fig|tab|qua)\b'),
    'legacy project type': re.compile(r'\bprojetocego\b'),
}
TODO_PATTERN = re.compile(r'\b(?:TODO|FIXME|HACK|XXX|MIGRATION_PENDING)\b', re.IGNORECASE)
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r'\b[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]', re.IGNORECASE),
    re.compile(r'/home/[A-Za-z0-9._-]+/'),
    re.compile(r'/Users/[A-Za-z0-9._-]+/'),
    re.compile(r'file:///'),
)
CS_PATTERN = re.compile(r'\\cs_(?:new|set)(?:_protected)?:Npn\s+(\\[A-Za-z@:_]+)')
KEY_PATTERN = re.compile(r'(?m)^\s*([a-z][a-z0-9-]*)\s*\.(?:choice|code|meta):')
SETUP_KEY_PATTERN = re.compile(r'(?m)^\s*([a-z][a-z0-9-]*)\s*=')


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ['git', '-c', f'safe.directory={ROOT}', 'ls-files', '-z'],
        cwd=ROOT,
    )
    return [ROOT / item.decode('utf-8') for item in output.split(b'\0') if item]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_text(path: Path) -> bool:
    if path.name in {'Makefile', 'LICENSE'}:
        return True
    return path.suffix.lower() in TEXT_SUFFIXES


def read_text(path: Path, errors: list[str]) -> str | None:
    try:
        data = path.read_bytes()
    except OSError as exc:
        errors.append(f'{relative(path)}: cannot read file: {exc}')
        return None
    if b'\0' in data:
        return None
    try:
        text = data.decode('utf-8')
    except UnicodeDecodeError as exc:
        errors.append(f'{relative(path)}: text file is not valid UTF-8: {exc}')
        return None
    if text.startswith('\ufeff'):
        errors.append(f'{relative(path)}: UTF-8 BOM is not allowed')
    if '\r\n' in text or '\r' in text:
        errors.append(f'{relative(path)}: CRLF/CR newline found')
    if text and not text.endswith('\n'):
        errors.append(f'{relative(path)}: missing final newline')
    return text


def extract_braced_calls(text: str, command: str) -> list[str]:
    result: list[str] = []
    marker = '\\' + command
    pos = 0
    while True:
        pos = text.find(marker, pos)
        if pos < 0:
            break
        brace = text.find('{', pos + len(marker))
        if brace < 0:
            break
        depth = 0
        i = brace
        while i < len(text):
            char = text[i]
            if char == '{' and (i == 0 or text[i - 1] != '\\'):
                depth += 1
            elif char == '}' and (i == 0 or text[i - 1] != '\\'):
                depth -= 1
                if depth == 0:
                    result.append(text[brace + 1:i])
                    pos = i + 1
                    break
            i += 1
        else:
            break
    return result


def audit_versions(texts: dict[str, str], errors: list[str]) -> str | None:
    makefile = texts.get('Makefile', '')
    match = re.search(r'^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', makefile, re.MULTILINE)
    if not match:
        errors.append('Makefile: VERSION is missing or invalid')
        return None
    version = match.group(1)

    cls = texts.get('ufctex.cls', '')
    if f'v{version} UFC academic document class' not in cls:
        errors.append(f'ufctex.cls: class version does not match {version}')

    ctan = texts.get('docs/README-CTAN.md', '')
    ctan_match = re.search(r'^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', ctan, re.MULTILINE)
    if not ctan_match or ctan_match.group(1) != version:
        current = ctan_match.group(1) if ctan_match else 'missing'
        errors.append(f'docs/README-CTAN.md: expected {version}, got {current}')

    changelog = texts.get('docs/CHANGELOG-CTAN.md', '')
    if changelog and not re.search(rf'^##\s+{re.escape(version)}\b', changelog, re.MULTILINE):
        errors.append(f'docs/CHANGELOG-CTAN.md: release candidate {version} is missing')

    readme = texts.get('README.md', '')
    published = re.search(
        r'Versão\s+publicada\s+atual:\s*(?:\*\*)?([0-9]+\.[0-9]+\.[0-9]+)',
        readme,
        re.IGNORECASE,
    )
    candidate = re.search(
        r'Versão\s+candidata\s+em\s+preparação:\s*(?:\*\*)?([0-9]+\.[0-9]+\.[0-9]+)',
        readme,
        re.IGNORECASE,
    )
    if not published:
        errors.append('README.md: published version is missing')
    if not ((published and published.group(1) == version) or (candidate and candidate.group(1) == version)):
        errors.append(f'README.md: current VERSION {version} is neither published nor candidate')
    return version


def audit_setup_keys(texts: dict[str, str], errors: list[str]) -> None:
    definitions = '\n'.join(
        text for name, text in texts.items()
        if name.startswith('ufctex/') and name.endswith('.def')
    )
    defined = set(KEY_PATTERN.findall(definitions))
    for name, text in texts.items():
        if not (name.endswith('.tex') or name.endswith('.md')):
            continue
        for block in extract_braced_calls(text, 'ufcsetup'):
            for key in sorted(set(SETUP_KEY_PATTERN.findall(block))):
                if key not in defined:
                    errors.append(f'{name}: unknown \\ufcsetup key: {key}')


def audit_modules(texts: dict[str, str], errors: list[str]) -> None:
    cls = texts.get('ufctex.cls', '')
    modules = re.findall(r'\\input\{(ufctex/[^}]+\.def)\}', cls)
    if len(modules) != len(set(modules)):
        errors.append('ufctex.cls: duplicate module input')
    for module in modules:
        if module not in texts:
            errors.append(f'ufctex.cls: missing module: {module}')
    if 'ufctex/trabalhos.def' in modules and 'ufctex/projetos.def' in modules:
        if modules.index('ufctex/trabalhos.def') > modules.index('ufctex/projetos.def'):
            errors.append('ufctex.cls: trabalhos.def must load before projetos.def')

    definitions: dict[str, list[str]] = defaultdict(list)
    for name, text in texts.items():
        if name.startswith('ufctex/') and name.endswith('.def'):
            for command in CS_PATTERN.findall(text):
                definitions[command].append(name)
    for command, locations in sorted(definitions.items()):
        unique = sorted(set(locations))
        if len(unique) > 1:
            errors.append(f'internal command {command} defined in multiple modules: {", ".join(unique)}')


def main() -> None:
    errors: list[str] = []
    files = tracked_files()
    texts: dict[str, str] = {}

    for path in files:
        name = relative(path)
        lower = name.lower()
        if name in FORBIDDEN_LEGACY_PATHS or any(
            name.startswith(prefix) for prefix in FORBIDDEN_LEGACY_PREFIXES
        ):
            errors.append(f'{name}: retired legacy path is not allowed')
        if any(lower.endswith(suffix) for suffix in GENERATED_SUFFIXES):
            errors.append(f'{name}: generated artifact must not be tracked')
        if name in {'.DS_Store', 'Thumbs.db'} or '/__pycache__/' in f'/{name}/':
            errors.append(f'{name}: editor/runtime artifact must not be tracked')

        if not is_text(path):
            continue
        text = read_text(path, errors)
        if text is None:
            continue
        texts[name] = text

        if name != SELF:
            if TODO_PATTERN.search(text):
                errors.append(f'{name}: pending-work marker found')
            for pattern in ABSOLUTE_PATH_PATTERNS:
                if pattern.search(text):
                    errors.append(f'{name}: machine-specific absolute path found')
                    break

        if name not in LEGACY_CONTENT_EXEMPT:
            for label, pattern in LEGACY_PATTERNS.items():
                if pattern.search(text):
                    errors.append(f'{name}: {label} found outside anti-legacy test scope')

    audit_versions(texts, errors)
    audit_setup_keys(texts, errors)
    audit_modules(texts, errors)

    if errors:
        unique = sorted(set(errors))
        for error in unique:
            print(error)
        raise SystemExit(f'Repository audit failed with {len(unique)} issue(s).')

    print(f'Repository audit passed: {len(files)} tracked files checked.')


if __name__ == '__main__':
    main()
