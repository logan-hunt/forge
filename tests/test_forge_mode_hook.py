import contextlib
import importlib.util
import io
import json
import os
from pathlib import Path
import shlex
import subprocess
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
HOOK = REPOSITORY / 'hooks/forge-mode.py'

import sys
sys.path.insert(0, str(REPOSITORY / 'scripts'))

spec = importlib.util.spec_from_file_location('install_forge_hooks', REPOSITORY / 'scripts/install-forge-hooks.py')
installer = importlib.util.module_from_spec(spec)
spec.loader.exec_module(installer)


class TemporaryHome(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.home = Path(self.temp.name)


class ModeHookTests(TemporaryHome):
    def hook_output(self, event, session='session-1', **fields):
        payload = {'hook_event_name': event, 'session_id': session, **fields}
        result = subprocess.run([sys.executable, str(HOOK)], input=json.dumps(payload), capture_output=True,
                                text=True, env={**os.environ, 'HOME': str(self.home)}, check=True)
        if not result.stdout:
            return None
        output = json.loads(result.stdout)['hookSpecificOutput']
        self.assertEqual(output['hookEventName'], event)
        return output

    def run_hook(self, event, session='session-1', **fields):
        output = self.hook_output(event, session, **fields)
        return output and output['additionalContext']

    def first_edit(self, *transcript, session='session-1'):
        path = self.home / f'{session}.jsonl'
        path.write_text(''.join(json.dumps(entry) + '\n' for entry in transcript))
        return self.hook_output('PreToolUse', session, tool_name='Edit', transcript_path=str(path))

    def write_config(self, text):
        config = self.home / '.config/forge/config.json'
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(text)

    def test_new_session_reports_standard_by_default(self):
        context = self.run_hook('SessionStart', source='startup')
        self.assertTrue(context.startswith('Forge mode: Standard (configured default; no mode selected in this session).'))

    def test_new_session_uses_configured_default(self):
        self.write_config('{"defaultMode": "lite"}')
        self.assertTrue(self.run_hook('SessionStart', source='startup').startswith('Forge mode: Lite (configured default'))

    def test_invalid_config_falls_back_to_standard(self):
        for text in ('{"defaultMode": "turbo"}', 'not json', '[]'):
            with self.subTest(text=text):
                self.write_config(text)
                self.assertTrue(self.run_hook('SessionStart', source='startup').startswith('Forge mode: Standard'))

    def test_selector_prompt_switches_mode_for_the_session(self):
        for prompt, mode in (('/forge lite fix the bug', 'Lite'), ('/forge-max', 'Max'),
                             ('$forge-lite plan it', 'Lite'), ('  /Forge Standard', 'Standard')):
            with self.subTest(prompt=prompt):
                context = self.run_hook('UserPromptSubmit', prompt=prompt)
                self.assertTrue(context.startswith(f'Forge mode: {mode} (selected by this prompt'))
                self.assertIn(f'Forge mode: {mode} (selected earlier', self.run_hook('SessionStart', source='compact'))

    def test_other_prompts_add_nothing_and_keep_the_mode(self):
        self.run_hook('UserPromptSubmit', prompt='/forge max')
        for prompt in ('fix the bug', 'use /forge lite later', '/forge-help', '/forge litefoo', '/forge'):
            with self.subTest(prompt=prompt):
                self.assertIsNone(self.run_hook('UserPromptSubmit', prompt=prompt))
        self.assertIn('Forge mode: Max (selected earlier', self.run_hook('SessionStart', source='resume'))

    def test_sessions_keep_separate_modes(self):
        self.run_hook('UserPromptSubmit', session='first', prompt='/forge lite')
        self.assertIn('Forge mode: Standard (configured default', self.run_hook('SessionStart', session='second', source='startup'))

    def test_subagent_inherits_the_parent_session_mode(self):
        self.assertIn('Forge mode: Standard (configured default; the parent session has not selected',
                      self.run_hook('SubagentStart', agent_type='Explore'))
        self.run_hook('UserPromptSubmit', prompt='/forge-max')
        self.assertIn('Forge mode: Max (selected in the parent session)', self.run_hook('SubagentStart', agent_type='Explore'))

    def test_unsafe_session_id_is_not_used_as_a_path(self):
        self.run_hook('UserPromptSubmit', session='../escape', prompt='/forge lite')
        self.assertFalse((self.home / '.local/state/forge/escape').exists())
        self.assertIn('Forge mode: Standard', self.run_hook('SessionStart', session='../escape', source='resume'))

    def test_forked_session_start_is_reported(self):
        self.assertIn('Forge mode: Standard', self.run_hook('SessionStart', session='forked', source='fork'))

    @staticmethod
    def claude_call(name, **tool_input):
        return {'type': 'assistant', 'message': {'content': [{'type': 'tool_use', 'name': name, 'input': tool_input}]}}

    @staticmethod
    def codex_call(command):
        return {'type': 'response_item', 'payload': {'type': 'custom_tool_call', 'name': 'exec', 'input': command}}

    def test_first_edit_is_refused_once_when_forge_was_only_named(self):
        forge = str(HOOK.parents[1] / 'skills/forge/SKILL.md')
        named_only = [
            {'type': 'user', 'message': {'content': f'Use `{forge}` for coding.'}},
            {'type': 'response_item', 'payload': {'type': 'message', 'content': forge}},
            self.claude_call('Bash', command=f'realpath {forge}; wc -l {forge}'),
            self.claude_call('Agent', prompt=f'Forge workflow at {forge}. Review the diff.'),
            self.codex_call(f'text(await tools.exec_command({{cmd:"realpath {forge}"}}))'),
        ]

        refusal = self.first_edit(*named_only)
        self.assertEqual(refusal['permissionDecision'], 'deny')
        self.assertIn('forge/skills/forge/SKILL.md', refusal['permissionDecisionReason'])
        self.assertIsNone(self.first_edit(*named_only))

    def test_parallel_first_edits_are_refused_only_once(self):
        transcript = self.home / 'parallel.jsonl'
        transcript.write_text('')
        payload = json.dumps({'hook_event_name': 'PreToolUse', 'session_id': 'parallel', 'transcript_path': str(transcript)})

        hooks = [subprocess.Popen([sys.executable, str(HOOK)], stdin=subprocess.PIPE, stdout=subprocess.PIPE, text=True,
                                  env={**os.environ, 'HOME': str(self.home)}) for _ in range(12)]
        outputs = [hook.communicate(payload)[0] for hook in hooks]
        self.assertEqual(sum('deny' in output for output in outputs), 1)

    def test_first_edit_passes_when_forge_was_opened(self):
        opened = {
            'claude-read': self.claude_call('Read', file_path='/home/me/.agents/forge/skills/forge/SKILL.md'),
            'claude-skill': self.claude_call('Skill', skill='forge'),
            'claude-shell': self.claude_call('Bash', command="sed -n '1,120p' ~/.claude/skills/forge/SKILL.md"),
            'codex-shell': self.codex_call('text(await tools.exec_command({cmd:"cat /example/forge/skills/forge/SKILL.md"}))'),
        }
        for session, entry in opened.items():
            with self.subTest(session=session):
                self.assertIsNone(self.first_edit(entry, session=session))

    def test_first_edit_passes_after_a_typed_forge_command_or_without_a_transcript(self):
        self.run_hook('UserPromptSubmit', session='typed', prompt='/forge')
        self.assertIsNone(self.first_edit(session='typed'))
        self.assertIsNone(self.hook_output('PreToolUse', 'no-transcript', tool_name='Edit', transcript_path=None))

    def test_unknown_event_and_bad_payload_are_silent(self):
        self.assertIsNone(self.run_hook('Stop'))
        result = subprocess.run([sys.executable, str(HOOK)], input='not json', capture_output=True, text=True,
                                env={**os.environ, 'HOME': str(self.home)})
        self.assertEqual((result.returncode, result.stdout), (0, ''))


class InstallerTests(TemporaryHome):
    PYTHON = '/usr/bin/python3'
    FORGE_SCRIPT = installer.HOOK_SCRIPT

    def setUp(self):
        super().setUp()
        self.claude = self.home / '.claude/settings.json'
        self.codex = self.home / '.codex/hooks.json'
        self.config = self.home / '.config/forge/config.json'
        self.claude.parent.mkdir()
        self.unrelated = {'type': 'command', 'command': 'echo keep'}
        self.claude.write_text(json.dumps({
            'permissions': {'allow': ['Bash(ls)']},
            'hooks': {'SessionStart': [{'hooks': [self.unrelated]}]},
        }))

    def run_installer(self, **options):
        with contextlib.redirect_stdout(io.StringIO()):
            return installer.run(REPOSITORY, self.home, self.PYTHON, **options)

    def commands(self, path, event, script):
        groups = json.loads(path.read_text())['hooks'].get(event, [])
        return [handler['command'] for group in groups for handler in group['hooks'] if script in handler['command']]

    def forge_commands(self, path, event):
        return self.commands(path, event, self.FORGE_SCRIPT)

    def test_preview_changes_nothing(self):
        before = self.claude.read_text()
        self.assertEqual(len(self.run_installer()), 2)
        self.assertEqual(self.claude.read_text(), before)
        self.assertFalse(self.codex.exists())

    def test_apply_adds_hooks_and_keeps_unrelated_settings(self):
        self.run_installer(apply=True, default_mode='standard')

        settings = json.loads(self.claude.read_text())
        self.assertEqual(settings['permissions'], {'allow': ['Bash(ls)']})
        self.assertEqual(settings['hooks']['SessionStart'][0]['hooks'], [self.unrelated])
        for path in (self.claude, self.codex):
            for event in installer.EVENTS:
                self.assertEqual(self.forge_commands(path, event), [f'{self.PYTHON} {REPOSITORY / self.FORGE_SCRIPT}'])
        self.assertEqual(json.loads(self.config.read_text()), {'defaultMode': 'standard'})

        backups = list((self.home / '.config/forge/backups').iterdir())
        self.assertEqual(len(backups), 1)
        self.assertEqual(len(json.loads((backups[0] / 'files.json').read_text())), 3)

    def test_first_edit_check_is_installed_for_edit_tools_on_both_hosts(self):
        self.run_installer(apply=True)
        for path in (self.claude, self.codex):
            groups = json.loads(path.read_text())['hooks']['PreToolUse']
            self.assertEqual([group['matcher'] for group in groups], [installer.EDIT_TOOLS])
            self.assertEqual(self.forge_commands(path, 'PreToolUse'), [f'{self.PYTHON} {REPOSITORY / self.FORGE_SCRIPT}'])

    def test_apply_twice_is_unchanged(self):
        self.run_installer(apply=True)
        self.assertEqual(self.run_installer(apply=True), [])

    def test_reinstall_replaces_an_old_forge_entry_in_place(self):
        self.run_installer(apply=True)
        self.PYTHON = '/opt/homebrew/bin/python3'
        self.run_installer(apply=True)
        self.assertEqual(self.forge_commands(self.claude, 'SessionStart'), [f'{self.PYTHON} {REPOSITORY / self.FORGE_SCRIPT}'])
        self.assertEqual(json.loads(self.claude.read_text())['hooks']['SessionStart'][0]['hooks'], [self.unrelated])

    def test_remove_takes_out_only_forge_hooks(self):
        self.run_installer(apply=True)
        self.run_installer(apply=True, install=False)
        settings = json.loads(self.claude.read_text())
        self.assertEqual(settings['hooks'], {'SessionStart': [{'hooks': [self.unrelated]}]})
        self.assertEqual(json.loads(self.codex.read_text()), {'hooks': {}})

    def test_forge_handler_sharing_a_group_is_moved_out_and_removed_without_losing_others(self):
        shared = {'matcher': 'startup', 'hooks': [self.unrelated, {'type': 'command', 'command': f'python3 {REPOSITORY / self.FORGE_SCRIPT}'}]}
        self.claude.write_text(json.dumps({'hooks': {'SessionStart': [shared]}}))

        self.run_installer(apply=True)
        groups = json.loads(self.claude.read_text())['hooks']['SessionStart']
        self.assertEqual(groups[0], {'matcher': 'startup', 'hooks': [self.unrelated]})
        self.assertEqual(self.forge_commands(self.claude, 'SessionStart'), [f'{self.PYTHON} {REPOSITORY / self.FORGE_SCRIPT}'])
        self.assertEqual(self.run_installer(apply=True), [])

        self.run_installer(apply=True, install=False)
        self.assertEqual(json.loads(self.claude.read_text())['hooks'], {'SessionStart': [{'matcher': 'startup', 'hooks': [self.unrelated]}]})

    def test_one_hook_carries_both_defaults(self):
        self.run_installer(apply=True, default_mode='max', ponytail='lite')
        self.assertEqual(json.loads(self.config.read_text()), {'defaultMode': 'max', 'ponytail': 'lite'})
        for path in (self.claude, self.codex):
            for event in installer.EVENTS:
                self.assertEqual(len(self.forge_commands(path, event)), 1)
        self.assertNotIn('node', self.codex.read_text())

    def test_hooks_from_another_checkout_are_left_alone(self):
        other = {'type': 'command', 'command': f'python3 /opt/vendor/{self.FORGE_SCRIPT}'}
        self.claude.write_text(json.dumps({'hooks': {'SessionStart': [{'hooks': [other]}]}}))

        self.run_installer(apply=True)
        self.run_installer(apply=True, install=False)
        self.assertEqual(json.loads(self.claude.read_text())['hooks']['SessionStart'], [{'hooks': [other]}])

    def test_defaults_must_be_valid(self):
        for options in ({'default_mode': 'full'}, {'ponytail': 'standard'}):
            with self.subTest(options=options), self.assertRaises(ValueError):
                self.run_installer(apply=True, **options)
        self.assertFalse(self.codex.exists())

    def test_malformed_hooks_are_refused_without_writing(self):
        self.claude.write_text(json.dumps({'hooks': {'SessionStart': {}}}))
        with self.assertRaises(ValueError):
            self.run_installer(apply=True)
        self.assertFalse(self.codex.exists())


if __name__ == '__main__':
    unittest.main()
