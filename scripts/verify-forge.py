"""Check the self-contained Forge package without changing user settings or discovery links."""
from collections import Counter
import json
from pathlib import Path
import re
import sys
import unicodedata
from urllib.parse import unquote

try:
    import yaml
except ImportError:
    sys.exit(f'Install validation dependencies: python3 -m pip install -r {Path(__file__).resolve().parents[1] / "requirements-dev.txt"}')

from forge_config import validate_config


def read_yaml(text):
    value = yaml.safe_load(text)
    if not isinstance(value, dict):
        raise ValueError('expected a YAML mapping')
    return value


def check_skill(skill):
    frontmatter = re.match(r'\A---\r?\n(.*?)\r?\n---(?:\r?\n|\Z)', skill.read_text(), re.S)
    if not frontmatter:
        raise ValueError('missing YAML frontmatter')
    metadata = read_yaml(frontmatter[1])
    name = metadata.get('name')
    if not isinstance(name, str) or len(name) > 64 or not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*', name):
        raise ValueError('name must be 1-64 lowercase letters, digits and single hyphens')
    if name != skill.parent.name:
        raise ValueError('name differs from directory')
    description = metadata.get('description')
    if not isinstance(description, str) or not description.strip() or len(description) > 1024:
        raise ValueError('description must be a nonempty string of at most 1024 characters')
    for field in ('disable-model-invocation', 'user-invocable'):
        if field in metadata and not isinstance(metadata[field], bool):
            raise ValueError(f'{field} must be a boolean')


def check_invocation_metadata(path):
    metadata = read_yaml(path.read_text())
    interface = metadata.get('interface', {})
    if not isinstance(interface, dict):
        raise ValueError('interface must be a mapping')
    for field in ('display_name', 'short_description', 'default_prompt'):
        if field in interface and (not isinstance(interface[field], str) or not interface[field].strip()):
            raise ValueError(f'interface.{field} must be a nonempty string')
    policy = metadata.get('policy', {})
    if not isinstance(policy, dict):
        raise ValueError('policy must be a mapping')
    if 'allow_implicit_invocation' in policy and not isinstance(policy['allow_implicit_invocation'], bool):
        raise ValueError('policy.allow_implicit_invocation must be a boolean')


def markdown_prose(text):
    return re.sub(r'(?ms)^\s*(```|~~~).*?^\s*\1[^\n]*(?:\n|$)', '', text)


def heading_anchors(text):
    anchors, counts = set(), Counter()
    for heading in re.findall(r'^#{1,6}\s+(.+?)\s*#*$', markdown_prose(text), re.M):
        title = re.sub(r'[`*]', '', heading).strip().lower()
        slug = ''.join(char for char in title if char in ('-', '_', ' ') or unicodedata.category(char)[0] in ('L', 'N')).replace(' ', '-')
        anchors.add(slug + (f'-{counts[slug]}' if counts[slug] else ''))
        counts[slug] += 1
    return anchors


def check(package):
    package = package.resolve()
    failures = []
    skills = sorted((package / 'skills').glob('*/SKILL.md'))
    for skill in skills:
        try:
            check_skill(skill)
        except (ValueError, yaml.YAMLError) as error:
            failures.append(f'{skill.relative_to(package)}: {error}')

    for path in package.glob('skills/*/agents/openai.yaml'):
        try:
            check_invocation_metadata(path)
        except (ValueError, yaml.YAMLError) as error:
            failures.append(f'{path.relative_to(package)}: {error}')

    for path in package.rglob('*.md'):
        if any(part in ('node_modules', '.venv') for part in path.parts):
            continue
        prose = markdown_prose(path.read_text())
        prose = re.sub(r'`[^`\n]*`', '', prose)
        for target in re.findall(r'(?<!!)\[[^\]]*\]\(([^)]+)\)', prose):
            filename, _, anchor = target.partition('#')
            if '://' in filename or filename.startswith('mailto:') or any(c in filename for c in '<>*| '):
                continue
            destination = (path.parent / unquote(filename)).resolve() if filename else path
            if not destination.is_relative_to(package) or not destination.exists():
                failures.append(f'{path.relative_to(package)}: missing/external local link {target}')
            elif anchor and destination.suffix == '.md' and unquote(anchor) not in heading_anchors(destination.read_text()):
                failures.append(f'{path.relative_to(package)}: missing heading anchor {target}')

    for path in package.rglob('*.json'):
        if any(part in ('node_modules', '.venv') for part in path.parts):
            continue
        try:
            json.loads(path.read_text())
        except ValueError as error:
            failures.append(f'{path.relative_to(package)}: {error}')
    try:
        validate_config(json.loads((package / 'models.json').read_text()))
    except ValueError as error:
        failures.append(f'models.json: {error}')
    return skills, failures


if __name__ == '__main__':
    package = Path(__file__).resolve().parents[1]
    skills, failures = check(package)
    for failure in failures:
        print(failure)
    print(f'{len(skills)} skills; {len(failures)} validation errors')
    sys.exit(bool(failures))
