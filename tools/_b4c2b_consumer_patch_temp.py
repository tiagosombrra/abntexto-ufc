#!/usr/bin/env python3
from pathlib import Path

path = Path('tests/checks/validator_source.py')
text = path.read_text(encoding='utf-8')
old = 'if "não é enviado para servidor" not in html:'
new = 'if "is not sent to a server" not in html:'
if text.count(old) != 1:
    raise SystemExit(f'validator_source local-processing marker drift: {text.count(old)}')
path.write_text(text.replace(old, new), encoding='utf-8')
