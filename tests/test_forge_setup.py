import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import shutil
import subprocess
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / 'scripts'))
import forge_config


def module(name, filename):
    spec = importlib.util.spec_from_file_location(name, PACKAGE / 'scripts' / filename)
    result = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(result)
    return result


activation = module('activate_forge', 'activate-forge.py')
installer = module('install_hooks', 'install-forge-hooks.py')


class SetupTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='forge setup ')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name).resolve()
        self.home = self.root / 'home'
        self.project = self.root / 'project'
        self.home.mkdir()
        self.project.mkdir()
        (self.project / '.git').mkdir()

    def run_installer(self, **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.run(PACKAGE, self.home, sys.executable, **options)

    def test_local_discovery_is_scoped_idempotent_and_preserves_instructions(self):
        for root in (self.home, self.project):
            with self.subTest(root=root), contextlib.redirect_stdout(io.StringIO()):
                (root / 'AGENTS.md').write_text('owned instructions')
                preview = activation.activate(PACKAGE, root)
                self.assertTrue(preview)
                self.assertFalse((root / '.agents').exists())
                activation.activate(PACKAGE, root, apply=True)
                self.assertEqual(activation.activate(PACKAGE, root, apply=True), [])
                for host in ('agents', 'claude', 'cursor'):
                    link = root / f'.{host}/skills/forge'
                    self.assertEqual(link.resolve(), PACKAGE / 'skills/forge')
                self.assertFalse((root / '.codex/hooks.json').exists())
                self.assertFalse((root / '.claude/settings.json').exists())
                activation.activate(PACKAGE, root, apply=True, remove=True)
                self.assertFalse((root / '.agents/skills/forge').exists())
                self.assertEqual((root / 'AGENTS.md').read_text(), 'owned instructions')

    def test_discovery_collision_stops_before_any_skill_is_linked(self):
        existing = self.project / '.cursor/skills/why'
        existing.mkdir(parents=True)
        (existing / 'SKILL.md').write_text('existing skill')
        with self.assertRaisesRegex(ValueError, 'Collision'):
            activation.activate(PACKAGE, self.project, apply=True)
        self.assertFalse((self.project / '.agents').exists())
        self.assertEqual((existing / 'SKILL.md').read_text(), 'existing skill')

    def test_upgrade_removes_only_links_to_retired_skills_from_this_source(self):
        source = self.root / 'forge'
        (source / 'skills/forge').mkdir(parents=True)
        (source / 'skills/forge/SKILL.md').touch()
        links = self.home / '.agents/skills'
        links.mkdir(parents=True)
        retired_source = source / 'skills/teach'
        retired_source.mkdir()
        local_note = retired_source / 'local-note.md'
        local_note.touch()
        owned = links / 'teach'
        owned.symlink_to(os.path.relpath(source / 'skills/teach', owned.parent))
        alternate = self.root / 'alternate'
        (alternate / 'vendor').mkdir(parents=True)
        (alternate / 'teach').mkdir()
        (source / 'skills/vendor').symlink_to(alternate / 'vendor')
        redirected = self.home / '.claude/skills/teach'
        redirected.parent.mkdir(parents=True)
        redirected.symlink_to(source / 'skills/vendor/../teach')
        alias = self.root / 'my-skill'
        alias.symlink_to(source / 'skills/principle-subtract-before-you-add')
        indirect = links / 'principle-subtract-before-you-add'
        indirect.symlink_to(alias)
        foreign = links / 'principle-laziness-protocol'
        foreign.symlink_to(self.root / 'other/skills/principle-laziness-protocol')

        with contextlib.redirect_stdout(io.StringIO()):
            activation.activate(source, self.home)
            self.assertTrue(owned.is_symlink())
            activation.activate(source, self.home, apply=True)
            self.assertFalse(owned.is_symlink())
            self.assertTrue(foreign.is_symlink())
            self.assertTrue(indirect.is_symlink())
            self.assertEqual(redirected.resolve(), alternate / 'teach')
            self.assertTrue(local_note.is_file())
            self.assertEqual(activation.activate(source, self.home, apply=True), [])

    def test_discovery_refuses_redirected_parent(self):
        elsewhere = self.root / 'elsewhere'
        elsewhere.mkdir()
        (self.project / '.agents').symlink_to(elsewhere)
        with self.assertRaisesRegex(ValueError, 'parent'):
            activation.activate(PACKAGE, self.project, apply=True)
        self.assertEqual(list(elsewhere.iterdir()), [])

    def test_uninstall_removes_current_skill_reached_through_package_alias(self):
        alias = self.root / 'package-alias'
        alias.symlink_to(PACKAGE)
        link = self.project / '.agents/skills/how'
        link.parent.mkdir(parents=True)
        link.symlink_to(alias / 'skills/how')

        with contextlib.redirect_stdout(io.StringIO()):
            preview = activation.activate(PACKAGE, self.project, remove=True)
            self.assertIn((link, PACKAGE / 'skills/how'), preview)
            self.assertTrue(link.is_symlink())
            activation.activate(PACKAGE, self.project, apply=True, remove=True)
        self.assertFalse(link.is_symlink())
        self.assertTrue(alias.is_symlink())

    def test_uninstall_preserves_another_packages_link(self):
        other = self.root / 'other-skill'
        other.mkdir()
        link = self.project / '.agents/skills/forge'
        link.parent.mkdir(parents=True)
        link.symlink_to(other)
        with contextlib.redirect_stdout(io.StringIO()):
            activation.activate(PACKAGE, self.project, apply=True, remove=True)
        self.assertEqual(link.resolve(), other)

    def test_renamed_reviewer_role_preserves_user_and_project_overrides(self):
        legacy = 'interrogate reviewers'
        role = 'adversarial-review reviewers'
        user = forge_config.config_path('user', self.home, self.project)
        project = forge_config.config_path('project', self.home, self.project)
        project.parent.mkdir(parents=True)
        target = [{'providerInstanceId': 'provider', 'model': 'reviewer'}]
        user.write_text(json.dumps({'roles': {legacy: target}}))

        effective = forge_config.load_config(self.home, self.project)['roles']
        self.assertEqual(effective[role], target)
        self.assertNotIn(legacy, effective)
        self.assertIn(legacy, json.loads(user.read_text())['roles'])

        project.write_text(json.dumps({'roles': {legacy: target, role: None}}))
        self.assertIsNone(forge_config.load_config(self.home, self.project)['roles'][role])
        with contextlib.redirect_stdout(io.StringIO()):
            forge_config.update_config(project, {'roles': {legacy: target}}, self.home, apply=True)
        self.assertEqual(json.loads(project.read_text())['roles'], {role: target})

    def test_model_overrides_merge_by_role_and_null_restores_inheritance(self):
        user = forge_config.config_path('user', self.home, self.project)
        project = forge_config.config_path('project', self.home, self.project)
        user.parent.mkdir(parents=True)
        target = {'providerInstanceId': 'test-provider', 'model': 'test-model', 'options': {'effort': 'high'}}
        user.write_text(json.dumps({'defaultMode': 'lite', 'roles': {'bug-fix': target, 'feature': target}, 'custom': True}))
        with contextlib.redirect_stdout(io.StringIO()):
            forge_config.update_config(project, {'defaultMode': 'max', 'roles': {'bug-fix': None}}, self.home)
            self.assertFalse(project.exists())
            forge_config.update_config(project, {'defaultMode': 'max', 'roles': {'bug-fix': None}}, self.home, apply=True)
        self.assertEqual(project.parent, self.home / '.config/forge/projects')
        self.assertTrue(project.name.startswith('project-'))
        self.assertFalse((self.project / '.agents').exists())
        settings = forge_config.load_config(self.home, self.project)
        self.assertEqual(settings['defaultMode'], 'max')
        self.assertIsNone(settings['roles']['bug-fix'])
        self.assertEqual(settings['roles']['feature'], target)
        self.assertIsNone(settings['roles']['perf-issue'])
        self.assertTrue(settings['custom'])
        nested = self.project / 'src/nested'
        nested.mkdir(parents=True)
        self.assertEqual(forge_config.project_root(nested), self.project)

    def test_config_rejects_invalid_input_without_writing_and_backs_up_changes(self):
        path = self.home / '.config/forge/config.json'
        with contextlib.redirect_stdout(io.StringIO()):
            with self.assertRaises(ValueError):
                forge_config.update_config(path, {'roles': {'bug-fix': {'model': 'missing-provider'}}}, self.home, apply=True)
            self.assertFalse(path.exists())
            forge_config.update_config(path, {'defaultMode': 'lite', 'custom': 'keep'}, self.home, apply=True)
            previous = path.read_text()
            forge_config.update_config(path, {'defaultMode': 'standard'}, self.home, apply=True)
            self.assertEqual(json.loads(path.read_text())['custom'], 'keep')
            backups = list((self.home / '.config/forge/backups').glob('*/config.json'))
            self.assertEqual(len(backups), 1)
            self.assertEqual(backups[0].read_text(), previous)
            self.assertFalse(forge_config.update_config(path, {'defaultMode': 'standard'}, self.home, apply=True))

    def test_project_hooks_use_project_settings_preserve_others_and_execute(self):
        settings = self.project / '.claude/settings.local.json'
        settings.parent.mkdir()
        settings.write_text(json.dumps({'permissions': {'allow': ['Read']}}))
        self.run_installer(project=self.project, default_mode='max')
        self.assertFalse((self.project / '.codex/hooks.json').exists())
        self.run_installer(project=self.project, default_mode='max', apply=True)
        self.assertFalse((self.home / '.codex/hooks.json').exists())
        self.assertFalse((self.home / '.config/forge/config.json').exists())
        data = json.loads(settings.read_text())
        self.assertEqual(data['permissions'], {'allow': ['Read']})
        command = data['hooks']['SessionStart'][0]['hooks'][0]['command']
        env = {'HOME': str(self.home), 'PATH': os.environ['PATH'], 'PYTHONDONTWRITEBYTECODE': '1'}
        payload = {'hook_event_name': 'SessionStart', 'session_id': 'scope-test', 'cwd': str(self.project)}
        result = subprocess.run(shlex.split(command), input=json.dumps(payload), text=True, capture_output=True,
                                env=env, check=True)
        self.assertIn('Forge mode: Max', json.loads(result.stdout)['hookSpecificOutput']['additionalContext'])
        self.assertEqual(self.run_installer(project=self.project, default_mode='max', apply=True), [])
        self.run_installer(project=self.project, install=False, apply=True)
        remaining = json.loads(settings.read_text())
        self.assertEqual(remaining['permissions'], {'allow': ['Read']})
        self.assertEqual(remaining.get('hooks', {}), {})
        self.assertTrue(list((self.home / '.config/forge/backups').iterdir()))

    def test_hook_removal_does_not_match_a_script_name_substring(self):
        script = str(PACKAGE / 'hooks/forge-mode.py')
        other = {'type': 'command', 'command': f'python3 {shlex.quote(script + ".other") }'}
        data = {'hooks': {'SessionStart': [{'hooks': [other]}]}}
        result = installer.with_hooks(data, {'SessionStart': 'unused'}, {script}, False, {})
        self.assertEqual(result, data)

    def test_hook_removal_preserves_script_paths_used_as_data(self):
        script = str(PACKAGE / 'hooks/forge-mode.py')
        commands = [
            shlex.join(['echo', script]),
            shlex.join(['shasum', script]),
            shlex.join(['python3', '-c', 'print(1)', script]),
            shlex.join(['/usr/bin/env', 'PONYTAIL_DEFAULT_MODE=lite', 'echo', script]),
            shlex.join(['python3', script, '&&', 'echo', 'keep this']),
        ]
        for command in commands:
            with self.subTest(command=command):
                handler = {'type': 'command', 'command': command}
                settings = {'hooks': {'SessionStart': [{'hooks': [handler]}]}}
                removed = installer.with_hooks(settings, {'SessionStart': 'unused'}, {script}, False, {})
                self.assertEqual(removed, settings)

    def test_project_setup_commands_agree_when_started_in_a_subdirectory(self):
        nested = self.project / 'src/nested'
        nested.mkdir(parents=True)
        for script, arguments in (
            ('activate-forge.py', ['--host', 'agents']),
            ('install-forge-hooks.py', ['--host', 'Codex']),
            ('forge_config.py', ['--default-mode', 'lite']),
        ):
            subprocess.run([sys.executable, '-B', str(PACKAGE / 'scripts' / script),
                            '--scope', 'project', '--home', str(self.home), '--apply', *arguments],
                           cwd=nested, text=True, capture_output=True, check=True)
        self.assertEqual((self.project / '.agents/skills/forge').resolve(), PACKAGE / 'skills/forge')
        self.assertTrue((self.project / '.codex/hooks.json').is_file())
        project_config = forge_config.config_path('project', self.home, self.project)
        self.assertEqual(json.loads(project_config.read_text())['defaultMode'], 'lite')
        self.assertFalse((self.project / '.agents/forge.json').exists())
        self.assertFalse((nested / '.agents').exists())
        self.assertFalse((nested / '.codex').exists())

    def test_interpreter_alias_is_managed_across_reinstall_and_removal(self):
        alias = self.root / 'python-runner'
        alias.symlink_to(sys.executable)
        with contextlib.redirect_stdout(io.StringIO()):
            installer.run(PACKAGE, self.home, str(alias), hosts=['Codex'], apply=True)
        self.run_installer(hosts=['Codex'], apply=True)
        settings = json.loads((self.home / '.codex/hooks.json').read_text())
        self.assertEqual(len(settings['hooks']['SessionStart']), 1)
        self.run_installer(hosts=['Codex'], install=False, apply=True)
        self.assertEqual(json.loads((self.home / '.codex/hooks.json').read_text())['hooks'], {})

    def test_project_root_respects_nested_repositories_and_non_git_projects(self):
        nested = self.project / 'nested-repo'
        (nested / '.git').mkdir(parents=True)
        standalone = self.root / 'standalone'
        standalone.mkdir()
        for project in (nested, standalone):
            with self.subTest(project=project):
                subprocess.run([sys.executable, '-B', str(PACKAGE / 'scripts/activate-forge.py'),
                                '--scope', 'project', '--project', str(project), '--host', 'agents', '--apply'],
                               text=True, capture_output=True, check=True)
                self.assertEqual((project / '.agents/skills/forge').resolve(), PACKAGE / 'skills/forge')
        self.assertFalse((self.project / '.agents').exists())

    def test_namespaced_forge_command_and_skill_read_are_recognized(self):
        env = {'HOME': str(self.home), 'PATH': os.environ['PATH'], 'PYTHONDONTWRITEBYTECODE': '1'}
        def call(event, **fields):
            payload = {'hook_event_name': event, 'session_id': 'namespace', 'cwd': str(self.project), **fields}
            result = subprocess.run([sys.executable, str(PACKAGE / 'hooks/forge-mode.py')], input=json.dumps(payload),
                                    env=env, text=True, capture_output=True, check=True)
            return json.loads(result.stdout)['hookSpecificOutput'] if result.stdout else None
        self.assertIn('Lite', call('UserPromptSubmit', prompt='/forge:forge lite')['additionalContext'])
        self.assertIn('Lite', call('SessionStart')['additionalContext'])
        transcript = self.root / 'transcript.jsonl'
        transcript.write_text(json.dumps({'type': 'assistant', 'message': {'content': [
            {'type': 'tool_use', 'name': 'Skill', 'input': {'skill': 'forge:forge'}}]}}))
        # A distinct session has no settled edit reminder yet.
        payload = {'hook_event_name': 'PreToolUse', 'session_id': 'namespace-read', 'transcript_path': str(transcript)}
        result = subprocess.run([sys.executable, str(PACKAGE / 'hooks/forge-mode.py')], input=json.dumps(payload),
                                env=env, text=True, capture_output=True, check=True)
        self.assertEqual(result.stdout, '')

    def test_project_ponytail_level_lives_in_the_project_config_and_reaches_both_hosts(self):
        nested = self.project / 'src'
        nested.mkdir()
        self.run_installer(project=forge_config.project_root(nested), ponytail='lite', apply=True)
        project_config = forge_config.config_path('project', self.home, self.project)
        self.assertEqual(json.loads(project_config.read_text()), {'ponytail': 'lite'})
        self.assertFalse((self.home / '.config/forge/config.json').exists())
        self.assertFalse((self.home / '.config/ponytail').exists())
        self.assertEqual(self.run_installer(project=self.project, apply=True), [])

        env = {'HOME': str(self.home), 'PATH': os.environ['PATH'], 'PYTHONDONTWRITEBYTECODE': '1'}
        for path in (self.project / '.codex/hooks.json', self.project / '.claude/settings.local.json'):
            with self.subTest(path=path):
                command = json.loads(path.read_text())['hooks']['SessionStart'][0]['hooks'][0]['command']
                payload = {'hook_event_name': 'SessionStart', 'session_id': path.name, 'cwd': str(nested)}
                result = subprocess.run(shlex.split(command), input=json.dumps(payload), env=env, text=True,
                                        capture_output=True, check=True)
                self.assertIn('Ponytail level: Lite', result.stdout)

    def test_copied_package_runs_from_a_path_with_spaces(self):
        copied = self.root / 'copied forge'
        shutil.copytree(PACKAGE, copied, ignore=shutil.ignore_patterns('__pycache__', 'node_modules', '.venv'))
        env = {'HOME': str(self.home), 'PATH': os.environ['PATH'], 'PYTHONDONTWRITEBYTECODE': '1'}
        def command(script, *arguments):
            return subprocess.run([sys.executable, '-B', str(copied / 'scripts' / script), *arguments],
                                  text=True, capture_output=True, env=env, check=True)
        command('activate-forge.py', '--scope', 'project', '--project', str(self.project), '--apply')
        self.assertEqual((self.project / '.agents/skills/forge').resolve(), copied / 'skills/forge')
        command('forge_config.py', '--scope', 'project', '--project', str(self.project),
                '--role', 'feature', '--target', '{"providerInstanceId":"test","model":"test"}', '--apply')
        effective = json.loads(command('forge_config.py', '--project', str(self.project)).stdout)
        self.assertEqual(effective['roles']['feature']['model'], 'test')
        command('install-forge-hooks.py', '--scope', 'project', '--project', str(self.project),
                '--host', 'Codex', '--apply')
        settings = json.loads((self.project / '.codex/hooks.json').read_text())
        hook = settings['hooks']['SessionStart'][0]['hooks'][0]['command']
        result = subprocess.run(shlex.split(hook), input=json.dumps({'hook_event_name': 'SessionStart',
                                'session_id': 'relocated', 'cwd': str(self.project)}),
                                text=True, capture_output=True, env=env, check=True)
        self.assertIn('Forge mode: Standard', result.stdout)
        command('verify-forge.py')
        self.assertFalse((self.home / '.claude/settings.json').exists())


if __name__ == '__main__':
    unittest.main()
