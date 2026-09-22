"""Integration regressions for packaging, using only temporary fixtures."""
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest


class ChatGPTPackagingTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name)
        self.script = self.root / 'scripts/configure-chatgpt.py'
        self.script.parent.mkdir()
        shutil.copy2(Path(__file__).resolve().parents[1] / 'scripts/configure-chatgpt.py', self.script)
        self.source = self.root / 'plugins/booked-chatgpt'
        (self.source / '.codex-plugin').mkdir(parents=True)
        (self.source / '.codex-plugin/plugin.json').write_text(json.dumps({
            'name': 'booked-chatgpt',
            'version': '0.4.0',
            'mcpServers': './.mcp.json',
            'skills': './skills/',
        }), encoding='utf-8')
        (self.source / '.mcp.json').write_text('{"mcpServers": {}}', encoding='utf-8')
        skill = self.source / 'skills/booked-fincas/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('Shared skill fixture.\n', encoding='utf-8')

    def run_packager(self, output):
        return subprocess.run(
            [sys.executable, str(self.script), '--app-id', 'connector_test', '--output', str(output)],
            capture_output=True, text=True, timeout=10,
        )

    def snapshot_source(self):
        return {
            str(path.relative_to(self.source)): path.read_bytes() if path.is_file() else None
            for path in self.source.rglob('*')
        }

    def test_external_output_builds_an_installable_package_without_changing_source(self):
        before = self.snapshot_source()
        output = self.root / 'dist/booked-chatgpt'
        result = self.run_packager(output)
        self.assertEqual(result.returncode, 0, result.stderr)
        manifest = json.loads((output / '.codex-plugin/plugin.json').read_text(encoding='utf-8'))
        self.assertEqual(manifest['apps'], './.app.json')
        self.assertNotIn('mcpServers', manifest)
        self.assertFalse((output / '.mcp.json').exists())
        self.assertEqual(json.loads((output / '.app.json').read_text(encoding='utf-8')),
                         {'apps': {'booked': {'id': 'connector_test'}}})
        self.assertEqual((output / 'skills/booked-fincas/SKILL.md').read_bytes(),
                         (self.source / 'skills/booked-fincas/SKILL.md').read_bytes())
        self.assertEqual(self.snapshot_source(), before)

    def test_source_itself_is_rejected_without_changes(self):
        before = self.snapshot_source()
        result = self.run_packager(self.source)
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(self.snapshot_source(), before)

    def test_descendant_output_is_rejected_before_copying(self):
        (self.source / 'dist').mkdir()
        before = self.snapshot_source()
        output = self.source / 'dist/booked-chatgpt'
        result = self.run_packager(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('outside the source package', result.stderr)
        self.assertFalse(output.exists())
        self.assertEqual(self.snapshot_source(), before)

    def test_symlink_to_descendant_output_is_rejected_before_copying(self):
        (self.source / 'dist').mkdir()
        alias = self.root / 'alias'
        alias.symlink_to(self.source / 'dist', target_is_directory=True)
        before = self.snapshot_source()
        output = alias / 'booked-chatgpt'
        result = self.run_packager(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertIn('outside the source package', result.stderr)
        self.assertFalse(output.exists())
        self.assertTrue(alias.is_symlink())
        self.assertEqual(self.snapshot_source(), before)

    def test_existing_output_is_preserved(self):
        output = self.root / 'dist/booked-chatgpt'
        output.mkdir(parents=True)
        before = self.snapshot_source()
        for nonempty in (False, True):
            with self.subTest(nonempty=nonempty):
                if nonempty:
                    (output / 'keep.txt').write_text('Existing package', encoding='utf-8')
                result = self.run_packager(output)
                self.assertNotEqual(result.returncode, 0)
                self.assertTrue(output.is_dir())
                self.assertEqual(list(output.iterdir()), [output / 'keep.txt'] if nonempty else [])
                if nonempty:
                    self.assertEqual((output / 'keep.txt').read_text(encoding='utf-8'), 'Existing package')
                self.assertEqual(self.snapshot_source(), before)

    def test_dangling_output_symlink_is_preserved(self):
        output = self.root / 'booked-chatgpt'
        target = self.root / 'missing-target'
        output.symlink_to(target, target_is_directory=True)
        before = self.snapshot_source()
        result = self.run_packager(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertTrue(output.is_symlink())
        self.assertEqual(output.readlink(), target)
        self.assertFalse(target.exists())
        self.assertEqual(self.snapshot_source(), before)

    def test_failed_build_removes_partial_output(self):
        (self.source / '.codex-plugin/plugin.json').write_text('{invalid JSON', encoding='utf-8')
        before = self.snapshot_source()
        output = self.root / 'dist/booked-chatgpt'
        result = self.run_packager(output)
        self.assertNotEqual(result.returncode, 0)
        self.assertFalse(output.exists())
        self.assertEqual(self.snapshot_source(), before)


if __name__ == '__main__':
    unittest.main()
