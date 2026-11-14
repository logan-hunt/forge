import importlib.util
import json
from pathlib import Path
import sys
import tempfile
import unittest

PACKAGE = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(PACKAGE / 'scripts'))
spec = importlib.util.spec_from_file_location('verify_forge', PACKAGE / 'scripts/verify-forge.py')
validator = importlib.util.module_from_spec(spec)
spec.loader.exec_module(validator)


class ValidationTests(unittest.TestCase):
    def setUp(self):
        directory = tempfile.TemporaryDirectory(prefix='forge-validation-')
        self.addCleanup(directory.cleanup)
        self.root = Path(directory.name)
        self.skill = self.root / 'skills/example/SKILL.md'
        self.skill.parent.mkdir(parents=True)
        self.skill.write_text('---\nname: example\ndescription: Describe this capability.\n---\n# Example\n')
        (self.root / 'models.json').write_text(json.dumps({'roles': {}}))

    def failures(self):
        return validator.check(self.root)[1]

    def test_malformed_yaml_is_rejected(self):
        self.skill.write_text('---\nname: example\ndescription: [unterminated\n---\n# Example\n')
        self.assertTrue(self.failures())

    def test_name_and_metadata_types_are_checked_after_parsing(self):
        cases = (
            'name: example-extra\ndescription: A capability.',
            'name: example\ndescription: [one, two]',
            'name: example\ndescription: false',
            'name: example\ndescription: ""',
            'name: example\ndescription: A capability.\ndisable-model-invocation: "false"',
            '- name: example\n- description: A capability.',
        )
        for frontmatter in cases:
            with self.subTest(frontmatter=frontmatter):
                self.skill.write_text(f'---\n{frontmatter}\n---\n# Example\n')
                self.assertTrue(self.failures())

    def test_folded_descriptions_and_supported_host_extensions_are_accepted(self):
        self.skill.write_text('---\nname: example\ndescription: >\n  Describe the capability\n  and when it applies.\ndisable-model-invocation: true\nuser-invocable: true\n---\n# Example\n')
        self.assertEqual(self.failures(), [])

    def test_yaml_object_constructors_are_not_executed(self):
        marker = self.root / 'unexpected'
        self.skill.write_text(f'---\nname: example\ndescription: !!python/object/apply:os.system ["touch {marker}"]\n---\n')
        self.assertTrue(self.failures())
        self.assertFalse(marker.exists())

    def test_invocation_policy_must_be_a_boolean(self):
        policy = self.skill.parent / 'agents/openai.yaml'
        policy.parent.mkdir()
        policy.write_text('policy:\n  allow_implicit_invocation: "false"\n')
        self.assertTrue(self.failures())
        policy.write_text('policy:\n  allow_implicit_invocation: false\n')
        self.assertEqual(self.failures(), [])

    def test_links_check_files_and_heading_anchors(self):
        target = self.root / 'guide.md'
        target.write_text('# Guide\n## Setup\n## Setup\n## config_file\n')
        self.skill.write_text(self.skill.read_text() + '\n[Guide](../../guide.md#setup-1)\n[Config](../../guide.md#config_file)\n')
        self.assertEqual(self.failures(), [])
        target.write_text('# Guide\n')
        self.assertEqual(len(self.failures()), 2)
        target.unlink()
        self.assertEqual(len(self.failures()), 2)

    def test_examples_are_not_treated_as_live_links(self):
        self.skill.write_text(self.skill.read_text() + '\n~~~md\n[Example](missing.md#example)\n~~~\n`[Example](missing.md)`\n')
        self.assertEqual(self.failures(), [])

    def test_development_environment_is_not_package_content(self):
        dependency = self.root / '.venv/dependency'
        dependency.mkdir(parents=True)
        (dependency / 'README.md').write_text('[Dependency docs](missing.md)')
        (dependency / 'metadata.json').write_text('not JSON')
        self.assertEqual(self.failures(), [])


if __name__ == '__main__':
    unittest.main()
