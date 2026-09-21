#!/usr/bin/env python3
"""Validate package wiring, release versions and generated skills without network."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
subprocess.run([sys.executable, str(root / 'scripts/sync-skills.py'), '--check'], check=True)
market = json.loads((root / '.claude-plugin/marketplace.json').read_text())
versions = set()
for entry in market['plugins']:
    folder = root / entry['source']
    manifest = json.loads((folder / '.claude-plugin/plugin.json').read_text())
    assert manifest['name'] == entry['name'] == folder.name
    assert manifest['version'] == entry['version']
    versions.add(manifest['version'])
manifest = json.loads((root / 'plugins/booked-chatgpt/.codex-plugin/plugin.json').read_text())
assert manifest['name'] == 'booked-chatgpt'
versions.add(manifest['version'])
assert len(versions) == 1, 'All released packages must have the same version'
for name in ['booked', 'booked-oauth', 'booked-chatgpt']:
    connection = json.loads((root / f'plugins/{name}/.mcp.json').read_text())['mcpServers']['booked']
    assert connection['type'] == 'http'
    expected = 'https://booked.fincasdelavilla.com/mcp' + ('' if name == 'booked' else '/oauth')
    assert connection['url'] == expected
    if name != 'booked':
        assert 'headers' not in connection, 'OAuth must not contain a static bearer token'
        text = (root / f'plugins/{name}/skills/booked-fincas/SKILL.md').read_text()
        assert 'La autorización OAuth no caduca por tiempo.' in text
with tempfile.TemporaryDirectory() as temp:
    output = Path(temp) / 'booked-chatgpt'
    subprocess.run([sys.executable, str(root / 'scripts/configure-chatgpt.py'), '--app-id', 'plugin_asdk_app_test_fixture', '--output', str(output)], check=True, capture_output=True)
    built = json.loads((output / '.codex-plugin/plugin.json').read_text())
    assert built['apps'] == './.app.json' and 'mcpServers' not in built
    assert json.loads((output / '.app.json').read_text()) == {'apps': {'booked': {'id': 'plugin_asdk_app_test_fixture'}}}
    assert not (output / '.mcp.json').exists()
print('Packages, versions, connections, ChatGPT packaging and shared skills are valid.')
