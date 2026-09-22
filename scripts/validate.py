#!/usr/bin/env python3
"""Validate package wiring, release versions and generated skills without network."""
import json
import subprocess
import sys
import tempfile
from pathlib import Path

root = Path(__file__).resolve().parents[1]
MANIFESTS = {
    'booked': '.claude-plugin/plugin.json',
    'booked-oauth': '.claude-plugin/plugin.json',
    'booked-chatgpt': '.codex-plugin/plugin.json',
}
MARKETPLACE_SOURCES = {
    'booked': './plugins/booked',
    'booked-oauth': './plugins/booked-oauth',
}


def check(condition, message):
    """Fail with a message; unlike assert, it survives python -O."""
    if not condition:
        raise SystemExit(f'validate.py: {message}')


def load(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8'))
    except (OSError, ValueError) as error:
        raise SystemExit(f'validate.py: cannot load {path}: {error}') from error
    check(isinstance(value, dict), f'{path}: expected a JSON object')
    return value


def package_path(folder, value, label, *, directory=False):
    """Resolve a package reference without accepting traversal or symlink escapes."""
    check(isinstance(value, str) and bool(value), f'{label}: expected a nonempty relative path')
    reference = Path(value)
    check(not reference.is_absolute(), f'{label}: expected a relative path')
    resolved = (folder / reference).resolve()
    check(resolved.is_relative_to(folder.resolve()), f'{label}: path escapes its package root')
    exists = resolved.is_dir() if directory else resolved.is_file()
    check(exists, f'{label}: missing {"directory" if directory else "file"} {value!r}')
    return resolved


def validate_skills(folder, manifest, label, *, explicit=False):
    check(not explicit or 'skills' in manifest, f'{label}: manifest must declare skills')
    references = manifest.get('skills', './skills/')
    if isinstance(references, str):
        references = [references]
    check(isinstance(references, list) and bool(references), f'{label}: skills must name at least one directory')
    expected = package_path(folder, 'skills/booked-fincas/SKILL.md', f'{label}: booked-fincas skill')
    discovered = set()
    for reference in references:
        skill_root = package_path(folder, reference, f'{label}: skills', directory=True)
        skills = list(skill_root.rglob('SKILL.md'))
        check(bool(skills), f'{label}: skills directory has no SKILL.md')
        for skill in skills:
            discovered.add(package_path(folder, str(skill.relative_to(folder)), f'{label}: SKILL.md'))
    check(expected in discovered, f'{label}: declared skills must include skills/booked-fincas/SKILL.md')


def validate_connection(folder, manifest, name):
    if name == 'booked-chatgpt':
        check('mcpServers' in manifest, f'{name}: source manifest must declare mcpServers')
    reference = manifest.get('mcpServers', './.mcp.json')
    connection_path = package_path(folder, reference, f'{name}: mcpServers')
    # Claude also automatically discovers .mcp.json even when a custom path is declared.
    paths = {connection_path, package_path(folder, './.mcp.json', f'{name}: .mcp.json')}
    for path in paths:
        servers = load(path).get('mcpServers')
        check(isinstance(servers, dict) and set(servers) == {'booked'},
              f'{name}: mcpServers must contain exactly the booked server')
        connection = servers['booked']
        check(isinstance(connection, dict), f'{name}: booked connection must be an object')
        check(connection.get('type') == 'http', f"{name}: connection type must be 'http'")
        expected = 'https://booked.fincasdelavilla.com/mcp' + ('' if name == 'booked' else '/oauth')
        check(connection.get('url') == expected, f'{name}: connection url must be {expected!r}')
        if name == 'booked':
            check(connection.get('headers') == {'Authorization': 'Bearer ${user_config.api_token}'},
                  'booked: headers must use the configured api_token as the only Authorization bearer')
        else:
            check('headers' not in connection and 'env' not in connection,
                  f'{name}: OAuth must not contain static credentials')
    if name == 'booked':
        config = manifest.get('userConfig', {})
        token = config.get('api_token') if isinstance(config, dict) else None
        check(isinstance(token, dict) and token.get('type') == 'string'
              and token.get('required') is True and token.get('sensitive') is True,
              'booked: userConfig.api_token must be a required, sensitive string')
    else:
        check(not manifest.get('userConfig'), f'{name}: OAuth must not configure static credentials')
        skill = package_path(folder, 'skills/booked-fincas/SKILL.md', f'{name}: OAuth guidance')
        check('La autorización OAuth no caduca por tiempo.' in skill.read_text(encoding='utf-8'),
              f'{name}: SKILL.md lacks the OAuth expiry guidance')


def main():
    # The release inventory is independent of the marketplace, so omitted entries
    # cannot hide a package or a divergent version from validation.
    manifests = {}
    for name, reference in MANIFESTS.items():
        folder = package_path(root, f'plugins/{name}', name, directory=True)
        manifest = load(package_path(folder, reference, f'{name}: manifest'))
        check(manifest.get('name') == name, f'{name}: manifest name must be {name!r}')
        check(isinstance(manifest.get('version'), str) and bool(manifest['version']),
              f'{name}: manifest must declare a version')
        manifests[name] = manifest
        validate_skills(folder, manifest, name, explicit=name == 'booked-chatgpt')
        validate_connection(folder, manifest, name)
    versions = {name: manifest['version'] for name, manifest in manifests.items()}
    check(len(set(versions.values())) == 1, f'All released packages must have the same version, got {versions}')

    market = load(package_path(root, '.claude-plugin/marketplace.json', 'marketplace'))
    entries = market.get('plugins')
    check(isinstance(entries, list) and all(isinstance(entry, dict) for entry in entries),
          'marketplace plugins must be an array of objects')
    names = [entry.get('name') for entry in entries]
    check(len(names) == len(MARKETPLACE_SOURCES)
          and all(names.count(name) == 1 for name in MARKETPLACE_SOURCES),
          'marketplace must contain exactly one booked and one booked-oauth entry')
    for entry in entries:
        name = entry['name']
        check(entry.get('source') == MARKETPLACE_SOURCES[name],
              f'{name}: marketplace source must be {MARKETPLACE_SOURCES[name]!r}')
        check(entry.get('version') == versions[name],
              f'{name}: marketplace and manifest versions must match')

    subprocess.run([sys.executable, str(root / 'scripts/sync-skills.py'), '--check'], check=True)
    with tempfile.TemporaryDirectory() as temp:
        output = Path(temp) / 'booked-chatgpt'
        result = subprocess.run([sys.executable, str(root / 'scripts/configure-chatgpt.py'), '--app-id',
                                 'plugin_asdk_app_test_fixture', '--output', str(output)],
                                capture_output=True, text=True)
        check(result.returncode == 0, f'configure-chatgpt.py failed:\n{result.stdout}{result.stderr}')
        built = load(package_path(output, '.codex-plugin/plugin.json', 'generated ChatGPT manifest'))
        check(built.get('name') == 'booked-chatgpt' and built.get('version') == versions['booked-chatgpt'],
              'generated ChatGPT manifest must preserve package name and version')
        validate_skills(output, built, 'generated ChatGPT', explicit=True)
        check(built.get('apps') == './.app.json' and 'mcpServers' not in built,
              'generated ChatGPT manifest must link .app.json and drop mcpServers')
        app_path = package_path(output, built['apps'], 'generated ChatGPT apps')
        check(load(app_path) == {'apps': {'booked': {'id': 'plugin_asdk_app_test_fixture'}}},
              'generated .app.json does not carry the app id')
        check(not (output / '.mcp.json').exists(), 'generated ChatGPT package must not keep .mcp.json')
    print('Packages, versions, connections, ChatGPT packaging and shared skills are valid.')


if __name__ == '__main__':
    main()
