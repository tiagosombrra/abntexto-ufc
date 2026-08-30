#!/usr/bin/env python3
from __future__ import annotations

import re
import subprocess
from collections import defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SELF = 'tests/v2-repository-audit.py'
CANONICAL_CLASS = 'abntexto-ufc.cls'
LEGACY_CLASS = 'ufctex.cls'

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
FORBIDDEN_LEGACY_PREFIXES = ('lib/', 'tests/compat/')
LEGACY_CONTENT_EXEMPT = (SELF,)
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
# Pending-work markers are intentionally case-sensitive. In Portuguese prose,
# the common word "todo" must not be interpreted as the technical marker TODO.
TODO_PATTERN = re.compile(r'\b(?:TODO|FIXME|HACK|XXX|MIGRATION_PENDING)\b')
ABSOLUTE_PATH_PATTERNS = (
    re.compile(r'\b[A-Za-z]:[\\/](?:Users|Documents and Settings)[\\/]', re.IGNORECASE),
    re.compile(r'/home/[A-Za-z0-9._-]+/'),
    re.compile(r'/Users/[A-Za-z0-9._-]+/'),
    re.compile(r'file:///'),
)
CS_PATTERN = re.compile(r'\\cs_(?:new|set)(?:_protected)?:Npn\s+(\\[A-Za-z@:_]+)')
KEY_PATTERN = re.compile(r'(?m)^\s*([a-z][a-z0-9-]*)\s*\.(?:choice|code|meta|tl_gset):')
SETUP_KEY_PATTERN = re.compile(r'(?m)^\s*([a-z][a-z0-9-]*)\s*=')
ACTION_USE_PATTERN = re.compile(r'(?m)^\s*-?\s*uses:\s*([^\s@]+)@([^\s#]+)')
SHA40_PATTERN = re.compile(r'^[0-9a-f]{40}$', re.IGNORECASE)
MODULE_PATTERN = re.compile(r'\\input\{((?:abntexto-ufc|ufctex)/[^}]+\.def)\}')


def tracked_files() -> list[Path]:
    output = subprocess.check_output(
        ['git', '-c', f'safe.directory={ROOT}', 'ls-files', '-z'], cwd=ROOT
    )
    return [ROOT / item.decode('utf-8') for item in output.split(b'\0') if item]


def relative(path: Path) -> str:
    return path.relative_to(ROOT).as_posix()


def is_text(path: Path) -> bool:
    return path.name in {'Makefile', 'LICENSE'} or path.suffix.lower() in TEXT_SUFFIXES


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


def canonical_modules(texts: dict[str, str], errors: list[str]) -> list[str]:
    cls = texts.get(CANONICAL_CLASS, '')
    modules = MODULE_PATTERN.findall(cls)
    if not modules:
        errors.append(f'{CANONICAL_CLASS}: no UFC modules are loaded')
        return []
    if len(modules) != len(set(modules)):
        errors.append(f'{CANONICAL_CLASS}: duplicate module input')
    for module in modules:
        if module not in texts:
            errors.append(f'{CANONICAL_CLASS}: missing module: {module}')
    return modules


def audit_versions(texts: dict[str, str], errors: list[str]) -> str | None:
    makefile = texts.get('Makefile', '')
    match = re.search(r'^VERSION\s*:?=\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', makefile, re.MULTILINE)
    if not match:
        errors.append('Makefile: VERSION is missing or invalid')
        return None
    version = match.group(1)

    cls = texts.get(CANONICAL_CLASS, '')
    cls_match = re.search(
        rf'\\ProvidesClass\{{abntexto-ufc\}}\[(\d{{4}}/\d{{2}}/\d{{2}})\s+v{re.escape(version)}\s+UFC academic document class\]',
        cls,
    )
    if not cls_match:
        errors.append(f'{CANONICAL_CLASS}: class version does not match {version}')

    legacy = texts.get(LEGACY_CLASS, '')
    if '\\LoadClass{abntexto-ufc}' not in legacy:
        errors.append(f'{LEGACY_CLASS}: compatibility wrapper must load abntexto-ufc')
    if 'deprecated' not in legacy.lower():
        errors.append(f'{LEGACY_CLASS}: compatibility wrapper must emit a deprecation warning')

    ctan = texts.get('docs/README-CTAN.md', '')
    ctan_match = re.search(r'^Version:\s*([0-9]+\.[0-9]+\.[0-9]+)\s*$', ctan, re.MULTILINE)
    if not ctan_match or ctan_match.group(1) != version:
        current = ctan_match.group(1) if ctan_match else 'missing'
        errors.append(f'docs/README-CTAN.md: expected {version}, got {current}')

    changelog = texts.get('docs/CHANGELOG-CTAN.md', '')
    release_match = re.search(
        rf'^##\s+{re.escape(version)}\s+[—-]\s+(\d{{4}}-\d{{2}}-\d{{2}})\s*$',
        changelog,
        re.MULTILINE,
    )
    if not release_match:
        errors.append(f'docs/CHANGELOG-CTAN.md: release candidate {version} is missing')
    elif cls_match and cls_match.group(1).replace('/', '-') != release_match.group(1):
        errors.append(f'{CANONICAL_CLASS} and docs/CHANGELOG-CTAN.md: release dates differ')

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


def audit_setup_keys(texts: dict[str, str], modules: list[str], errors: list[str]) -> None:
    definitions = '\n'.join(texts.get(name, '') for name in modules)
    defined = set(KEY_PATTERN.findall(definitions))
    for name, text in texts.items():
        if not (name.endswith('.tex') or name.endswith('.md')):
            continue
        for block in extract_braced_calls(text, 'ufcsetup'):
            for key in sorted(set(SETUP_KEY_PATTERN.findall(block))):
                if key not in defined:
                    errors.append(f'{name}: unknown \\ufcsetup key: {key}')


def audit_modules(texts: dict[str, str], modules: list[str], errors: list[str]) -> None:
    by_basename = {Path(module).name: index for index, module in enumerate(modules)}
    if 'academic-works.def' in by_basename and 'research-projects.def' in by_basename:
        if by_basename['academic-works.def'] > by_basename['research-projects.def']:
            errors.append(f'{CANONICAL_CLASS}: academic-works.def must load before research-projects.def')

    definitions: dict[str, list[str]] = defaultdict(list)
    for name in modules:
        text = texts.get(name, '')
        for command in CS_PATTERN.findall(text):
            definitions[command].append(name)
    for command, locations in sorted(definitions.items()):
        unique = sorted(set(locations))
        if len(unique) > 1:
            errors.append(f'internal command {command} defined in multiple modules: {", ".join(unique)}')


def audit_release_docs(texts: dict[str, str], errors: list[str]) -> None:
    normas = texts.get('docs/NORMAS.md', '')
    if 'ufctex/compat-v1.def' in normas or re.search(r'compatibilidade\s+V1', normas, re.IGNORECASE):
        errors.append('docs/NORMAS.md: retired V1 compatibility is still described as active')

    readme = texts.get('README.md', '')
    ctan = texts.get('docs/README-CTAN.md', '')
    stale = re.compile(
        r'classification\s+must\s+be\s+confirmed\s+before\s+a\s+CTAN\s+submission|classifica[cç][aã]o\s+para\s+redistribui[cç][aã]o',
        re.IGNORECASE,
    )
    if stale.search(readme) or stale.search(ctan):
        errors.append('release documentation: obsolete coat-of-arms licensing wording is still present')


def audit_workflow_pins(texts: dict[str, str], errors: list[str]) -> None:
    for name, text in texts.items():
        if not name.startswith('.github/workflows/') or not name.endswith(('.yml', '.yaml')):
            continue
        for action, ref in ACTION_USE_PATTERN.findall(text):
            if action.startswith('./'):
                continue
            if not SHA40_PATTERN.fullmatch(ref):
                errors.append(f'{name}: external action is not pinned to a full commit SHA: {action}@{ref}')


def main() -> None:
    errors: list[str] = []
    files = tracked_files()
    texts: dict[str, str] = {}

    for path in files:
        name = relative(path)
        lower = name.lower()
        if name in FORBIDDEN_LEGACY_PATHS or any(name.startswith(prefix) for prefix in FORBIDDEN_LEGACY_PREFIXES):
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
    modules = canonical_modules(texts, errors)
    audit_setup_keys(texts, modules, errors)
    audit_modules(texts, modules, errors)
    audit_release_docs(texts, errors)
    audit_workflow_pins(texts, errors)

    if errors:
        unique = sorted(set(errors))
        for error in unique:
            print(error)
        raise SystemExit(f'Repository audit failed with {len(unique)} issue(s).')

    print(f'Repository audit passed: {len(files)} tracked files checked.')


if __name__ == '__main__':
    main()
