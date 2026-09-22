"""Regression checks for the release validator using isolated package copies."""
import json
import shutil
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANUAL = 'plugins/booked/.claude-plugin/plugin.json'
OAUTH = 'plugins/booked-oauth/.claude-plugin/plugin.json'
CHATGPT = 'plugins/booked-chatgpt/.codex-plugin/plugin.json'
MARKETPLACE = '.claude-plugin/marketplace.json'


class ValidationTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'repo'
        for name in ('scripts', 'shared', 'plugins', '.claude-plugin'):
            shutil.copytree(ROOT / name, self.root / name)

    def edit_json(self, reference, change):
        path = self.root / reference
        value = json.loads(path.read_text(encoding='utf-8'))
        change(value)
        path.write_text(json.dumps(value), encoding='utf-8')

    def validate(self, message=None):
        result = subprocess.run([sys.executable, str(self.root / 'scripts/validate.py')],
                                capture_output=True, text=True, timeout=15)
        output = result.stdout + result.stderr
        if message is None:
            self.assertEqual(result.returncode, 0, output)
        else:
            self.assertNotEqual(result.returncode, 0, output)
            self.assertIn(message, output)

    def test_current_packages_pass(self):
        self.validate()

    def test_manual_bearer_is_required(self):
        self.edit_json('plugins/booked/.mcp.json', lambda value: value['mcpServers']['booked'].pop('headers'))
        self.validate('headers must use the configured api_token')

    def test_manual_bearer_cannot_be_hardcoded(self):
        self.edit_json('plugins/booked/.mcp.json', lambda value: value['mcpServers']['booked']['headers'].update(
            Authorization='Bearer test-fixture-not-a-real-token'))
        self.validate('headers must use the configured api_token')

    def test_manual_token_security_flags_are_required(self):
        for field in ('required', 'sensitive'):
            with self.subTest(field=field):
                settings = {'required': True, 'sensitive': True, field: False}
                self.edit_json(MANUAL, lambda value: value['userConfig']['api_token'].update(settings))
                self.validate('userConfig.api_token must be a required, sensitive string')

    def test_manual_token_type_is_required(self):
        self.edit_json(MANUAL, lambda value: value['userConfig']['api_token'].update(type='number'))
        self.validate('userConfig.api_token must be a required, sensitive string')

    def test_manual_user_config_is_required(self):
        self.edit_json(MANUAL, lambda value: value.pop('userConfig'))
        self.validate('userConfig.api_token must be a required, sensitive string')

    def test_oauth_rejects_static_credentials(self):
        self.edit_json('plugins/booked-oauth/.mcp.json', lambda value: value['mcpServers']['booked'].update(
            headers={'Authorization': 'Bearer test-fixture-not-a-real-token'}))
        self.validate('OAuth must not contain static credentials')

    def test_missing_skills_path_is_rejected(self):
        self.edit_json(CHATGPT, lambda value: value.update(skills='./does-not-exist/'))
        self.validate('skills: missing directory')

    def test_empty_skills_directory_is_rejected(self):
        (self.root / 'plugins/booked-chatgpt/empty-skills').mkdir()
        self.edit_json(CHATGPT, lambda value: value.update(skills='./empty-skills/'))
        self.validate('skills directory has no SKILL.md')

    def test_unrelated_skill_directory_is_rejected(self):
        skill = self.root / 'plugins/booked-chatgpt/other-skills/unrelated/SKILL.md'
        skill.parent.mkdir(parents=True)
        skill.write_text('Unrelated skill', encoding='utf-8')
        self.edit_json(CHATGPT, lambda value: value.update(skills='./other-skills/'))
        self.validate('declared skills must include skills/booked-fincas/SKILL.md')

    def test_skill_path_cannot_escape_package(self):
        self.edit_json(CHATGPT, lambda value: value.update(skills='../booked/skills/'))
        self.validate('skills: path escapes its package root')

    def test_skill_symlink_cannot_escape_package(self):
        folder = self.root / 'plugins/booked-chatgpt'
        (folder / 'external-skills').symlink_to(self.root / 'plugins/booked/skills', target_is_directory=True)
        self.edit_json(CHATGPT, lambda value: value.update(skills='./external-skills/'))
        self.validate('skills: path escapes its package root')

    def test_missing_mcp_path_is_rejected(self):
        self.edit_json(CHATGPT, lambda value: value.update(mcpServers='./absent.json'))
        self.validate('mcpServers: missing file')

    def test_mcp_path_cannot_escape_package(self):
        self.edit_json(CHATGPT, lambda value: value.update(mcpServers='../booked-oauth/.mcp.json'))
        self.validate('mcpServers: path escapes its package root')

    def test_omitted_marketplace_package_is_rejected(self):
        self.edit_json(MARKETPLACE, lambda value: value['plugins'].pop())
        self.validate('marketplace must contain exactly one booked and one booked-oauth entry')

    def test_version_of_omitted_package_is_still_checked(self):
        self.edit_json(MARKETPLACE, lambda value: value['plugins'].pop())
        self.edit_json(OAUTH, lambda value: value.update(version='9.9.9'))
        self.validate('All released packages must have the same version')

    def test_duplicate_marketplace_package_is_rejected(self):
        self.edit_json(MARKETPLACE, lambda value: value['plugins'].append(value['plugins'][0]))
        self.validate('marketplace must contain exactly one booked and one booked-oauth entry')

    def test_unexpected_marketplace_source_is_rejected(self):
        self.edit_json(MARKETPLACE, lambda value: value['plugins'][0].update(source='./plugins/booked-oauth'))
        self.validate('marketplace source must be')

    def test_package_name_must_match_its_directory(self):
        self.edit_json(OAUTH, lambda value: value.update(name='another-package'))
        self.validate('manifest name must be')

    def test_generated_skill_path_is_checked(self):
        script = self.root / 'scripts/configure-chatgpt.py'
        corruption = """
import json
import sys
from pathlib import Path
fixture_output = Path(sys.argv[sys.argv.index('--output') + 1])
fixture_path = fixture_output / '.codex-plugin/plugin.json'
fixture_manifest = json.loads(fixture_path.read_text(encoding='utf-8'))
fixture_manifest['skills'] = './missing-generated-skills/'
fixture_path.write_text(json.dumps(fixture_manifest), encoding='utf-8')
"""
        script.write_text(script.read_text(encoding='utf-8') + corruption, encoding='utf-8')
        self.validate('generated ChatGPT: skills: missing directory')


if __name__ == '__main__':
    unittest.main()
