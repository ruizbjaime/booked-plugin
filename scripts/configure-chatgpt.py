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
if args.output.name != 'booked-chatgpt' or args.output.exists():
    parser.error('Output must be a new folder named booked-chatgpt.')
source = Path(__file__).resolve().parents[1] / 'plugins/booked-chatgpt'
shutil.copytree(source, args.output)
manifest_path = args.output / '.codex-plugin/plugin.json'
manifest = json.loads(manifest_path.read_text())
manifest.pop('mcpServers', None)
manifest['apps'] = './.app.json'
manifest_path.write_text(json.dumps(manifest, ensure_ascii=False, indent=2) + '\n')
(args.output / '.mcp.json').unlink()
(args.output / '.app.json').write_text(json.dumps({'apps': {'booked': {'id': args.app_id}}}, indent=2) + '\n')
print(f'ChatGPT package: {args.output}')
