import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

REPOSITORY = Path(__file__).resolve().parents[1]
HOOK = REPOSITORY / 'hooks/forge-mode.py'


class PonytailLevelTests(unittest.TestCase):
    def setUp(self):
        temp = tempfile.TemporaryDirectory()
        self.addCleanup(temp.cleanup)
        self.home = Path(temp.name)
        self.project = self.home / 'project'
        (self.project / '.git').mkdir(parents=True)

    def run_hook(self, event, session='session-1', **fields):
        payload = json.dumps({'hook_event_name': event, 'session_id': session, 'cwd': str(self.project), **fields})
        result = subprocess.run([sys.executable, '-B', str(HOOK)], input=payload, capture_output=True, text=True,
                                env={'PATH': '/usr/bin:/bin', 'HOME': str(self.home)}, check=True, timeout=10)
        self.assertEqual(result.stderr, '')
        return json.loads(result.stdout)['hookSpecificOutput']['additionalContext'] if result.stdout else None

    def ponytail(self, context):
        return context.split('\n\n', 1)[1] if context else None

    def write_config(self, **settings):
        config = self.home / '.config/forge/config.json'
        config.parent.mkdir(parents=True, exist_ok=True)
        config.write_text(json.dumps(settings))

    def test_session_start_reports_the_mode_then_the_level_and_its_rules(self):
        context = self.run_hook('SessionStart')
        self.assertTrue(context.startswith('Forge mode: Standard'))
        ponytail = self.ponytail(context)
        self.assertTrue(ponytail.startswith('Ponytail level: Full (configured default'))
        self.assertIn('## Select the level', ponytail)
        self.assertIn('| **full** |', ponytail)
        self.assertNotIn('| **ultra** |', ponytail)
        self.assertNotIn('name: ponytail', ponytail)

    def test_configured_level_sets_the_start_and_off_reports_one_line(self):
        self.write_config(ponytail='ultra')
        self.assertTrue(self.ponytail(self.run_hook('SessionStart')).startswith('Ponytail level: Ultra'))
        self.write_config(ponytail='off')
        self.assertEqual(self.ponytail(self.run_hook('SessionStart')).count('\n'), 0)

    def test_project_level_overrides_the_user_level(self):
        self.write_config(ponytail='lite')
        subprocess.run([sys.executable, '-B', str(REPOSITORY / 'scripts/forge_config.py'), '--scope', 'project',
                        '--project', str(self.project), '--home', str(self.home), '--ponytail', 'ultra', '--apply'],
                       check=True, capture_output=True)
        self.assertTrue(self.ponytail(self.run_hook('SessionStart')).startswith('Ponytail level: Ultra'))

    def test_level_switch_lasts_the_session_and_reaches_subagents(self):
        switched = self.run_hook('UserPromptSubmit', prompt='/ponytail lite')
        self.assertTrue(switched.startswith('Ponytail level: Lite (selected by this prompt'))
        self.assertIn('| **lite** |', switched)
        self.assertIsNone(self.run_hook('UserPromptSubmit', prompt='fix the bug'))
        self.assertTrue(self.ponytail(self.run_hook('SubagentStart')).startswith('Ponytail level: Lite (selected in the parent'))
        self.assertTrue(self.ponytail(self.run_hook('SessionStart', source='compact')).startswith('Ponytail level: Lite'))
        self.assertTrue(self.ponytail(self.run_hook('SessionStart', session='other')).startswith('Ponytail level: Full'))

    def test_namespaced_and_codex_commands_switch_the_level(self):
        for prompt, level in (('/forge:ponytail ultra', 'Ultra'), ('$ponytail lite', 'Lite')):
            with self.subTest(prompt=prompt):
                self.assertTrue(self.run_hook('UserPromptSubmit', prompt=prompt).startswith(f'Ponytail level: {level}'))

    def test_stop_ponytail_turns_it_off_and_bare_command_turns_it_back_on(self):
        self.assertTrue(self.run_hook('UserPromptSubmit', prompt='Stop ponytail.').startswith('Ponytail level: Off'))
        self.assertTrue(self.ponytail(self.run_hook('SubagentStart')).startswith('Ponytail level: Off'))
        self.assertTrue(self.run_hook('UserPromptSubmit', prompt='/ponytail').startswith('Ponytail level: Full (selected'))
        self.assertTrue(self.run_hook('UserPromptSubmit', prompt='/ponytail').startswith('Ponytail level: Full (unchanged)'))

    def test_default_command_saves_the_user_level_without_changing_the_session(self):
        reply = self.run_hook('UserPromptSubmit', prompt='/ponytail default lite')
        self.assertTrue(reply.startswith('Ponytail default: Lite'))
        self.assertEqual(json.loads((self.home / '.config/forge/config.json').read_text()), {'ponytail': 'lite'})
        self.assertTrue(self.ponytail(self.run_hook('SessionStart', session='new')).startswith('Ponytail level: Lite'))

    def test_review_skill_and_unknown_levels_do_not_change_the_level(self):
        self.assertIsNone(self.run_hook('UserPromptSubmit', prompt='/ponytail-review the diff'))
        self.assertIn('is not a level', self.run_hook('UserPromptSubmit', prompt='/ponytail band'))
        self.assertTrue(self.ponytail(self.run_hook('SessionStart')).startswith('Ponytail level: Full (configured'))

    def test_forge_mode_prompt_reports_only_the_mode(self):
        reply = self.run_hook('UserPromptSubmit', prompt='/forge lite')
        self.assertEqual(reply, 'Forge mode: Lite (selected by this prompt; it lasts for the rest of this session).')


if __name__ == '__main__':
    unittest.main()
