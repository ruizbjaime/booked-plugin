#!/usr/bin/env python3
"""Render platform skills from one source; --check is used by CI."""
import argparse
from pathlib import Path

root = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('--check', action='store_true')
args = parser.parse_args()
template = (root / 'shared/booked-fincas.md').read_text(encoding='utf-8')
for plugin, authentication in [('booked', 'manual'), ('booked-oauth', 'oauth'), ('booked-chatgpt', 'oauth')]:
    text = template.replace('{{AUTH_GUIDANCE}}', (root / f'shared/auth-{authentication}.md').read_text(encoding='utf-8').rstrip())
    target = root / f'plugins/{plugin}/skills/booked-fincas/SKILL.md'
    if args.check:
        if not target.exists() or target.read_text(encoding='utf-8') != text:
            raise SystemExit(f'{target.relative_to(root)} is stale; run python3 scripts/sync-skills.py')
    else:
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(text, encoding='utf-8')
