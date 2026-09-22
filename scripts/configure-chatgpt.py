#!/usr/bin/env python3
"""Build a separate installable package using the real ChatGPT connection ID."""
import argparse
import json
import re
import shutil
from pathlib import Path

parser = argparse.ArgumentParser()
parser.add_argument('--app-id', required=True)
parser.add_argument('--output', type=Path, required=True, help='New output folder named booked-chatgpt')
args = parser.parse_args()
if not re.fullmatch(r'(plugin_asdk_app|connector)_[A-Za-z0-9_-]+', args.app_id):
    parser.error('Use the technical ID of the registered ChatGPT MCP connection.')
if args.output.name != 'booked-chatgpt' or args.output.exists() or args.output.is_symlink():
    parser.error('Output must be a new folder named booked-chatgpt.')
source = (Path(__file__).resolve().parents[1] / 'plugins/booked-chatgpt').resolve()
output = args.output.resolve()
if output == source or source in output.parents:
    parser.error('Output must be outside the source package.')
# Reserve the destination before cleanup can run, so an existing path is never
# removed, including when another process creates it after the initial check.
output.mkdir(parents=True, exist_ok=False)
try:
    shutil.copytree(source, output, dirs_exist_ok=True)
    manifest_path = output / '.codex-plugin/plugin.json'
    manifest = json.loads(manifest_path.read_text(encoding='utf-8'))
    manifest.pop('mcpServers', None)
    manifest['apps'] = './.app.json'
    manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n', encoding='utf-8')
    (output / '.mcp.json').unlink()
    (output / '.app.json').write_text(json.dumps({'apps': {'booked': {'id': args.app_id}}}, indent=2) + '\n', encoding='utf-8')
except BaseException:
    shutil.rmtree(output)
    raise
print(f'ChatGPT package: {args.output}')
