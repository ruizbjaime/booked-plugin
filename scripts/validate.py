#!/usr/bin/env python3
"""Validate package wiring, release versions and generated skills without network."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]


def check(condition, message):
    """Fail with a message; unlike assert, it survives python -O."""
    if not condition:
        raise SystemExit(f'validate.py: {message}')


def load(path):
    return json.loads(path.read_text(encoding='utf-8'))


subprocess.run([sys.executable, str(root / 'scripts/sync-skills.py'), '--check'], check=True)
market = load(root / '.claude-plugin/marketplace.json')
versions = {}
for entry in market['plugins']:
    folder = root / entry['source']
    manifest = load(folder / '.claude-plugin/plugin.json')
    check(manifest['name'] == entry['name'] == folder.name,
          f"name mismatch: plugin.json says {manifest['name']!r}, marketplace.json says {entry['name']!r}, folder is {folder.name!r}")
    check(manifest['version'] == entry['version'],
          f"{entry['name']}: plugin.json says {manifest['version']} and marketplace.json says {entry['version']}")
    versions[entry['name']] = manifest['version']
manifest = load(root / 'plugins/booked-chatgpt/.codex-plugin/plugin.json')
check(manifest['name'] == 'booked-chatgpt', f"booked-chatgpt manifest is named {manifest['name']!r}")
versions['booked-chatgpt'] = manifest['version']
check(len(set(versions.values())) == 1, f'All released packages must have the same version, got {versions}')
for name in ['booked', 'booked-oauth', 'booked-chatgpt']:
    connection = load(root / f'plugins/{name}/.mcp.json')['mcpServers']['booked']
    check(connection['type'] == 'http', f"{name}: connection type is {connection['type']!r}, expected 'http'")
    expected = 'https://booked.fincasdelavilla.com/mcp' + ('' if name == 'booked' else '/oauth')
    check(connection['url'] == expected, f"{name}: connection url is {connection['url']!r}, expected {expected!r}")
    if name != 'booked':
        check('headers' not in connection, f'{name}: OAuth must not contain a static bearer token')
        text = (root / f'plugins/{name}/skills/booked-fincas/SKILL.md').read_text(encoding='utf-8')
        check('La autorización OAuth no caduca por tiempo.' in text, f'{name}: SKILL.md lacks the OAuth expiry guidance')
with tempfile.TemporaryDirectory() as temp:
    output = Path(temp) / 'booked-chatgpt'
    result = subprocess.run([sys.executable, str(root / 'scripts/configure-chatgpt.py'), '--app-id', 'plugin_asdk_app_test_fixture', '--output', str(output)], capture_output=True, text=True)
    check(result.returncode == 0, f'configure-chatgpt.py failed:\n{result.stdout}{result.stderr}')
    built = load(output / '.codex-plugin/plugin.json')
    check(built.get('apps') == './.app.json' and 'mcpServers' not in built, 'generated ChatGPT manifest must link .app.json and drop mcpServers')
    check(load(output / '.app.json') == {'apps': {'booked': {'id': 'plugin_asdk_app_test_fixture'}}}, 'generated .app.json does not carry the app id')
    check(not (output / '.mcp.json').exists(), 'generated ChatGPT package must not keep .mcp.json')
print('Packages, versions, connections, ChatGPT packaging and shared skills are valid.')
