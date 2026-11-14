#!/usr/bin/env python3
"""Preview, install or remove the Forge hook (Forge mode and Ponytail level) for Claude Code and Codex."""
import argparse
import copy
import json
from pathlib import Path
import re
import shlex
import shutil
import sys

from forge_config import (MODES, PONYTAIL_LEVELS, config_path, new_backup_folder, project_root, read_json,
                          validate_config, write_json)

EVENTS = ('SessionStart', 'UserPromptSubmit', 'SubagentStart')
# Claude Code names its edit tools; Codex reports every file edit as apply_patch.
EDIT_TOOLS = 'Edit|Write|NotebookEdit|apply_patch'
TIMEOUT_SECONDS = 10
HOSTS = {'Claude Code': '.claude/settings.json', 'Codex': '.codex/hooks.json'}
HOOK_SCRIPT = 'hooks/forge-mode.py'
SCRIPTS = {event: HOOK_SCRIPT for event in (*EVENTS, 'PreToolUse')}
MATCHERS = {'PreToolUse': EDIT_TOOLS}


def hook_command(interpreter, script, env):
    words = [interpreter, str(script)]
    if env:
        words = ['/usr/bin/env', *(f'{name}={value}' for name, value in env.items()), *words]
    return shlex.join(words)


def hook_group(command, matcher=None):
    group = {'hooks': [{'type': 'command', 'command': command, 'timeout': TIMEOUT_SECONDS}]}
    return {'matcher': matcher, **group} if matcher else group


def owned_command_environment(handler, scripts):
    if not isinstance(handler, dict) or handler.get('type') != 'command':
        return None
    try:
        words = shlex.split(str(handler.get('command', '')))
    except ValueError:
        return None

    environment = {}
    if words and words[0] in ('env', '/usr/bin/env'):
        words = words[1:]
        while words and re.match(r'^[A-Za-z_][A-Za-z_0-9]*=', words[0]):
            name, value = words.pop(0).split('=', 1)
            environment[name] = value

    if len(words) == 1 and words[0] in scripts:
        return environment
    if len(words) == 2 and words[1] in scripts:
        interpreter = Path(words[0]).resolve().name
        if re.fullmatch(r'python(?:\d+(?:\.\d+)*t?)?', interpreter, re.I):
            return environment
    return None


def is_owned_handler(handler, scripts):
    return owned_command_environment(handler, scripts) is not None


def without_owned_handlers(group, scripts):
    """Split a hook group into its remainder without our handlers (None when nothing is left) and whether it held ours."""
    handlers = group.get('hooks') if isinstance(group, dict) else None
    if not isinstance(handlers, list) or not any(is_owned_handler(handler, scripts) for handler in handlers):
        return group, False

    others = [handler for handler in handlers if not is_owned_handler(handler, scripts)]
    return ({**group, 'hooks': others} if others else None), True


def with_hooks(settings, commands, scripts, install, matchers):
    """Return a copy of settings with our handlers replaced in place, appended, or removed.

    `commands` maps each event to the command to install; `scripts` holds the absolute script paths we execute,
    so another checkout's copy of the same hooks is left alone. `matchers` limits an event's
    handler to the tools it names.
    """
    updated = copy.deepcopy(settings)
    hooks = updated.get('hooks', {})
    if not isinstance(hooks, dict):
        raise ValueError('"hooks" is not an object')

    for event, command in commands.items():
        groups = hooks.get(event, [])
        if not isinstance(groups, list):
            raise ValueError(f'"hooks.{event}" is not a list')

        kept = []
        replaced = False
        for group in groups:
            remainder, held_ours = without_owned_handlers(group, scripts)
            if remainder is not None:
                kept.append(remainder)
            elif install and held_ours and not replaced:
                kept.append(hook_group(command, matchers.get(event)))
                replaced = True
        if install and not replaced:
            kept.append(hook_group(command, matchers.get(event)))

        if kept:
            hooks[event] = kept
        elif event in hooks:
            del hooks[event]

    if hooks or 'hooks' in settings:
        updated['hooks'] = hooks
    return updated


def planned_changes(source, home, python, install, settings, project=None, hosts=None):
    scripts = {str(source / HOOK_SCRIPT)}
    action = 'install' if install else 'remove'
    changes = []
    for host, relative_path in HOSTS.items():
        if hosts and host not in hosts:
            continue
        path = (project or home) / relative_path
        if project and host == 'Claude Code':
            path = project / '.claude/settings.local.json'
        try:
            current = read_json(path)
            env = {'CLAUDE_PROJECT_DIR': str(project)} if project else {}
            commands = {event: hook_command(python, source / script, env) for event, script in SCRIPTS.items()}
            desired = with_hooks(current, commands, scripts, install, MATCHERS)
        except ValueError as error:
            raise ValueError(f'{host} {path}: {error}') from error
        if desired != current:
            changes.append((f'{host} Forge hooks ({action})', path, desired))

    if settings:
        path = config_path('project' if project else 'user', home, project)
        current = read_json(path)
        validate_config(current)
        desired = {**current, **settings}
        if desired != current:
            described = ', '.join(f'{key} {value}' for key, value in settings.items())
            changes.append((f'Forge defaults ({described})', path, desired))
    return changes


def back_up(paths, home):
    backup = new_backup_folder(home)

    originals = []
    for path in paths:
        entry = {'path': str(path), 'existed': path.exists()}
        if path.exists():
            saved = backup / str(len(originals))
            shutil.copy2(path, saved)
            entry['contents'] = str(saved)
        originals.append(entry)
    (backup / 'files.json').write_text(json.dumps(originals, indent=2) + '\n')
    return backup


def run(source, home, python, install=True, default_mode=None, ponytail=None, apply=False, project=None, hosts=None):
    if not (source / HOOK_SCRIPT).is_file():
        raise ValueError(f'Missing hook script: {source / HOOK_SCRIPT}')
    if default_mode and default_mode not in MODES:
        raise ValueError(f'Forge default mode must be one of: {", ".join(MODES)}')
    if ponytail and ponytail not in PONYTAIL_LEVELS:
        raise ValueError(f'Ponytail level must be one of: {", ".join(PONYTAIL_LEVELS)}')

    settings = {key: value for key, value in (('defaultMode', default_mode), ('ponytail', ponytail)) if value}
    changes = planned_changes(source, home, python, install, settings, project, hosts)
    if not changes:
        print(f'UNCHANGED: Forge hooks already {"installed" if install else "absent"}')
        return changes
    for label, path, _ in changes:
        print(f'{"UPDATE" if apply else "WOULD UPDATE"} {label}: {path}')
    if not apply:
        return changes

    backup = back_up([path for _, path, _ in changes], home)
    for _, path, desired in changes:
        write_json(path, desired)
    print(f'Backed up previous files to {backup}')
    print('Start a new session to load the change. Codex runs new or changed hooks only after you trust them in /hooks.')
    return changes


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true', help='write the changes (default: preview)')
    parser.add_argument('--remove', action='store_true', help='remove the hooks instead of installing them')
    parser.add_argument('--default-mode', choices=MODES, help='the Forge mode new sessions start in')
    parser.add_argument('--ponytail', choices=PONYTAIL_LEVELS, help='the Ponytail level new sessions start at')
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--host', action='append', choices=sorted(HOSTS), help='repeat to select hosts; default: both')
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--python', default=shutil.which('python3') or sys.executable)
    args = parser.parse_args()
    try:
        run(args.source.resolve(), args.home.absolute(), args.python, not args.remove, args.default_mode,
            args.ponytail, args.apply, project_root(args.project) if args.scope == 'project' else None, args.host)
    except (ValueError, OSError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
