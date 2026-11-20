"""Read or preview/update user and project Forge settings outside the package."""
import argparse
from datetime import datetime, timezone
import hashlib
import json
import os
from pathlib import Path
import shutil
import tempfile

PACKAGE = Path(__file__).resolve().parents[1]
MODES = ('lite', 'standard', 'max')
PONYTAIL_LEVELS = ('off', 'lite', 'full', 'ultra')


def project_root(directory):
    directory = Path(directory).resolve()
    for parent in (directory, *directory.parents):
        if (parent / '.git').exists():
            return parent
    return directory


def project_key(project):
    """Name a project's settings file by its folder name plus a hash of its full path."""
    digest = hashlib.sha256(str(project).encode()).hexdigest()[:12]
    return f'{project.name}-{digest}'


def settings_path(config_dir, scope, project):
    return config_dir / 'config.json' if scope == 'user' else config_dir / 'projects' / f'{project_key(project)}.json'


def config_path(scope, home, project):
    return settings_path(home / '.config/forge', scope, project)


def new_backup_folder(home):
    stamp = datetime.now(timezone.utc).strftime('%Y%m%dT%H%M%S%fZ')
    folder = home / '.config/forge/backups' / stamp
    folder.mkdir(parents=True)
    return folder


def read_json(path):
    if not path.exists():
        return {}
    value = json.loads(path.read_text().lstrip('\ufeff'))
    if not isinstance(value, dict):
        raise ValueError(f'Expected a JSON object: {path}')
    return value


def validate_target(target):
    if target is None:
        return
    if isinstance(target, list):
        if not target:
            raise ValueError('A panel needs at least one model selection')
        for member in target:
            if not isinstance(member, dict):
                raise ValueError('Panel members must be model selection objects')
            validate_target(member)
        return
    if not isinstance(target, dict) or any(not isinstance(target.get(key), str) or not target[key].strip()
                                           for key in ('providerInstanceId', 'model')):
        raise ValueError('A model selection needs providerInstanceId and model strings, or null for the workflow default')
    options = target.get('options', {})
    if not isinstance(options, dict) or any(not isinstance(value, (str, bool)) for value in options.values()):
        raise ValueError('Model options must be an object of string or boolean values')


def validate_config(config):
    if 'defaultMode' in config and config['defaultMode'] not in MODES:
        raise ValueError(f'defaultMode must be one of {", ".join(MODES)}')
    if 'ponytail' in config and config['ponytail'] not in PONYTAIL_LEVELS:
        raise ValueError(f'ponytail must be one of {", ".join(PONYTAIL_LEVELS)}')
    roles = config.get('roles', {})
    if not isinstance(roles, dict):
        raise ValueError('roles must be an object')
    known = read_json(PACKAGE / 'models.json')['roles']
    for role, target in roles.items():
        if role not in known:
            raise ValueError(f'Unknown Forge role: {role}')
        validate_target(target)


RENAMED_ROLES = {
    'interrogate reviewers': 'adversarial-review reviewers',
    'reflect tooling': 'retro tooling',
    'reflect judgment': 'retro judgment',
}


def settings_with_current_roles(settings):
    roles = settings.get('roles')
    if isinstance(roles, dict) and RENAMED_ROLES.keys() & roles.keys():
        roles = roles.copy()
        for legacy, role in RENAMED_ROLES.items():
            if legacy in roles:
                roles.setdefault(role, roles.pop(legacy))
        settings = {**settings, 'roles': roles}
    validate_config(settings)
    return settings


def load_config(home, project):
    result = {'defaultMode': 'standard', 'ponytail': 'full', 'roles': read_json(PACKAGE / 'models.json')['roles']}
    for scope in ('user', 'project'):
        settings = settings_with_current_roles(read_json(config_path(scope, home, project)))
        result = {**result, **settings, 'roles': {**result['roles'], **settings.get('roles', {})}}
    return result


def write_json(path, value):
    target = path.resolve() if path.is_symlink() else path
    target.parent.mkdir(parents=True, exist_ok=True)
    temporary_path = None
    try:
        with tempfile.NamedTemporaryFile('w', dir=target.parent, prefix='.forge-', delete=False) as temporary:
            temporary_path = Path(temporary.name)
            json.dump(value, temporary, indent=2)
            temporary.write('\n')
        if target.exists():
            shutil.copymode(target, temporary_path)
        os.replace(temporary_path, target)
    finally:
        if temporary_path and temporary_path.exists():
            temporary_path.unlink()


def update_config(path, changes, home, apply=False):
    stored = read_json(path)
    current = settings_with_current_roles(stored)
    changes = settings_with_current_roles(changes)
    desired = {**current, **changes}
    roles = {**current.get('roles', {}), **changes.get('roles', {})}
    if roles:
        desired['roles'] = roles
    if desired == stored:
        return False
    print(f'{"UPDATE" if apply else "WOULD UPDATE"} {path}')
    if apply:
        if path.exists():
            shutil.copy2(path, new_backup_folder(home) / path.name)
        write_json(path, desired)
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--default-mode', choices=MODES)
    parser.add_argument('--ponytail', choices=PONYTAIL_LEVELS, help='the Ponytail level new sessions start at')
    parser.add_argument('--role', help='role to override; --target null restores the workflow default')
    parser.add_argument('--target', help='JSON model selection or panel, validated against live capabilities by forge-setup')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    if bool(args.role) != bool(args.target):
        parser.error('--role and --target must be supplied together')
    try:
        home, project = args.home.resolve(), project_root(args.project)
        changes = {}
        if args.default_mode:
            changes['defaultMode'] = args.default_mode
        if args.ponytail:
            changes['ponytail'] = args.ponytail
        if args.role:
            changes['roles'] = {args.role: json.loads(args.target)}
        if changes:
            update_config(config_path(args.scope, home, project), changes, home, args.apply)
        else:
            print(json.dumps(load_config(home, project), indent=2))
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
