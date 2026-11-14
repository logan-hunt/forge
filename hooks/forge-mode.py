#!/usr/bin/env python3
"""Report the active Forge mode and Ponytail level to Claude Code and Codex through lifecycle hooks.

Reads one hook payload on stdin and prints a hookSpecificOutput JSON object with a
`Forge mode:` line and, unless Ponytail is off, a `Ponytail level:` line followed by
the Ponytail rules for that level. A mode selected with /forge lite|standard|max,
/forge-lite or /forge-max, and a level selected with /ponytail lite|full|ultra|off,
last for the rest of that session.

Also refuses the first file edit of a session that has not opened Forge's SKILL.md,
once, so the retry goes through.
"""
import contextlib
import io
import json
from pathlib import Path
import re
import sys

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / 'scripts'))
from forge_config import PONYTAIL_LEVELS, config_path, load_config, project_root, update_config

PACKAGE = Path(__file__).resolve().parents[1]
MODES = ('lite', 'standard', 'max')
FALLBACK_SETTINGS = {'defaultMode': 'standard', 'ponytail': 'full'}
SELECTOR = re.compile(r'[/$](?:forge:)?forge(?: (lite|standard|max)|-(lite|max))(?=\s|$)')
FORGE_COMMAND = re.compile(r'[/$](?:forge:)?forge(?:-lite|-max)?(?=\s|$)')
FORGE_SKILL = 'skills/forge/SKILL.md'
# A command that prints the file, not one that only names its path (realpath, wc, a delegate's brief).
SHELL_READ = re.compile(r'\b(?:cat|sed|head|tail|nl|less|bat|awk)\b[^|;&\n]*' + re.escape(FORGE_SKILL))
READ_FORGE_FIRST = (
    f'Read {Path(__file__).resolve().parents[1] / FORGE_SKILL} before editing: it routes the task and sets the plan-approval step. '
    'This check runs once per session; retry the edit if Forge does not apply to this work.'
)
SESSION_ID = re.compile(r'[A-Za-z0-9_.-]{1,200}')
SWITCH_HINT = 'Switch with /forge lite, /forge standard or /forge max.'
PRECEDENCE = 'A mode named in a delegating brief or requested explicitly in conversation takes precedence.'

PONYTAIL_SKILL = PACKAGE / 'skills/ponytail/SKILL.md'
# /ponytail-review is a separate one-shot skill, so the command must end at whitespace or the prompt's end.
PONYTAIL_COMMAND = re.compile(r'[/$@](?:forge:)?ponytail(?=\s|$)(.*)', re.S)
PONYTAIL_OFF_PHRASES = ('stop ponytail', 'normal mode')
PONYTAIL_HINT = 'Switch with /ponytail lite, /ponytail full, /ponytail ultra or /ponytail off.'
# The level table rows and worked examples are the only level-specific lines in the Ponytail skill.
LEVEL_TABLE_ROW = re.compile(r'^\|\s*\*\*(.+?)\*\*\s*\|')
LEVEL_EXAMPLE = re.compile(r'^-\s*([^:]+):\s*"')


def defaults(home, cwd=None):
    try:
        return load_config(home, project_root(cwd or Path.cwd()))
    except (OSError, ValueError, AttributeError):
        return FALLBACK_SETTINGS


def default_mode(home, cwd=None):
    return defaults(home, cwd)['defaultMode']


def default_ponytail(home, cwd=None):
    return defaults(home, cwd)['ponytail']


def state_file(home, session_id, folder='modes'):
    if not isinstance(session_id, str) or not SESSION_ID.fullmatch(session_id) or session_id.strip('.') == '':
        return None
    return home / '.local/state/forge' / folder / session_id


def settle_edit_check(home, session_id):
    """Record that this session's first-edit check is settled; return whether it already was."""
    path = state_file(home, session_id, 'edit-checks')
    if not path:
        return True
    path.parent.mkdir(parents=True, exist_ok=True)
    try:
        # Exclusive creation lets only one of several parallel edits see the check as unsettled.
        path.touch(exist_ok=False)
    except FileExistsError:
        return True
    return False


def reads_forge(tool, tool_input):
    if tool == 'Read':
        return str(tool_input.get('file_path')).endswith(FORGE_SKILL)
    if tool == 'Skill':
        return tool_input.get('skill') in ('forge', 'forge:forge')
    return tool == 'Bash' and bool(SHELL_READ.search(str(tool_input.get('command'))))


def opens_forge(line):
    """Whether a transcript line holds a tool call that reads Forge: a Claude Code tool_use or a Codex *_call item."""
    if 'forge' not in line:
        return False
    try:
        entry = json.loads(line)
    except ValueError:
        return False

    payload = entry.get('payload')
    if entry.get('type') == 'response_item' and isinstance(payload, dict) and str(payload.get('type')).endswith('_call'):
        return bool(SHELL_READ.search(str(payload.get('input') or payload.get('arguments'))))
    if entry.get('type') != 'assistant':
        return False
    content = (entry.get('message') or {}).get('content') or []
    return any(reads_forge(block.get('name'), block.get('input') or {})
               for block in content if isinstance(block, dict) and block.get('type') == 'tool_use')


def has_opened_forge(transcript_path):
    try:
        with open(transcript_path, errors='replace') as transcript:
            return any(opens_forge(line) for line in transcript)
    except (OSError, TypeError):
        # An unreadable transcript cannot show a skipped read, so do not refuse.
        return True


def saved_value(home, session_id, folder, allowed):
    path = state_file(home, session_id, folder)
    try:
        value = path.read_text().strip() if path else None
    except OSError:
        return None
    return value if value in allowed else None


def save_value(home, session_id, folder, value):
    path = state_file(home, session_id, folder)
    if not path:
        return
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(value + '\n')


def saved_mode(home, session_id):
    return saved_value(home, session_id, 'modes', MODES)


def save_mode(home, session_id, mode):
    save_value(home, session_id, 'modes', mode)


def saved_ponytail(home, session_id):
    return saved_value(home, session_id, 'ponytail', PONYTAIL_LEVELS)


def ponytail_rules(level):
    """The Ponytail skill body without frontmatter, keeping only this level's table row and examples."""
    try:
        text = PONYTAIL_SKILL.read_text()
    except OSError:
        return f'Read {PONYTAIL_SKILL} and apply it at this level.'

    def keep(line):
        label = LEVEL_TABLE_ROW.match(line) or LEVEL_EXAMPLE.match(line)
        name = label.group(1).strip().lower() if label else None
        return name not in PONYTAIL_LEVELS or name == level

    body = re.sub(r'^---\n.*?\n---\s*', '', text, count=1, flags=re.S)
    return '\n'.join(line for line in body.splitlines() if keep(line)).strip()


def ponytail_report(level, origin):
    if level == 'off':
        return f'Ponytail level: Off ({origin}). Turn it on with /ponytail lite, /ponytail full or /ponytail ultra.'
    return f'Ponytail level: {level.capitalize()} ({origin}). {PONYTAIL_HINT}\n\n{ponytail_rules(level)}'


def session_ponytail(payload, home, saved_origin, default_origin):
    level = saved_ponytail(home, payload.get('session_id'))
    if level:
        return ponytail_report(level, saved_origin)
    return ponytail_report(default_ponytail(home, payload.get('cwd')), default_origin)


def ponytail_prompt(payload, home):
    """Apply a Ponytail command in the prompt and describe the result, or return None for ordinary prompts."""
    text = str(payload.get('prompt') or '').strip().lower()
    session_id = payload.get('session_id')
    command = PONYTAIL_COMMAND.match(text)

    if text.rstrip('.!? ') in PONYTAIL_OFF_PHRASES:
        words = ['off']
    elif command:
        words = command.group(1).split()
    else:
        return None

    if not words:
        current = saved_ponytail(home, session_id)
        if current and current != 'off':
            return ponytail_report(current, 'unchanged')
        default = default_ponytail(home, payload.get('cwd'))
        words = ['full' if default == 'off' else default]

    if words[0] == 'default' and len(words) > 1 and words[1] in PONYTAIL_LEVELS:
        with contextlib.redirect_stdout(io.StringIO()):
            update_config(config_path('user', home, None), {'ponytail': words[1]}, home, apply=True)
        return f'Ponytail default: {words[1].capitalize()}. New sessions start at this level; this session is unchanged.'

    level = words[0]
    if level not in PONYTAIL_LEVELS:
        return f'Ponytail: "{level}" is not a level. {PONYTAIL_HINT}'
    save_value(home, session_id, 'ponytail', level)
    return ponytail_report(level, 'selected by this prompt; it lasts for the rest of this session')


def selected_mode(prompt):
    match = SELECTOR.match(prompt.strip().lower())
    if not match:
        return None
    return match.group(1) or match.group(2)


def on_session_start(payload, home):
    mode = saved_mode(home, payload.get('session_id'))
    if mode:
        origin = 'selected earlier in this session'
    else:
        mode = default_mode(home, payload.get('cwd'))
        origin = 'configured default; no mode selected in this session'
    ponytail = session_ponytail(payload, home, 'selected earlier in this session',
                                'configured default; no level selected in this session')
    return f'Forge mode: {mode.capitalize()} ({origin}). {SWITCH_HINT} {PRECEDENCE}\n\n{ponytail}'


def on_user_prompt(payload, home):
    prompt = str(payload.get('prompt') or '')
    if FORGE_COMMAND.match(prompt.strip().lower()):
        settle_edit_check(home, payload.get('session_id'))

    reports = []
    mode = selected_mode(prompt)
    if mode:
        save_mode(home, payload.get('session_id'), mode)
        reports.append(f'Forge mode: {mode.capitalize()} (selected by this prompt; it lasts for the rest of this session).')
    ponytail = ponytail_prompt(payload, home)
    if ponytail:
        reports.append(ponytail)
    return '\n\n'.join(reports) or None


def on_subagent_start(payload, home):
    mode = saved_mode(home, payload.get('session_id'))
    if mode:
        origin = 'selected in the parent session'
    else:
        mode = default_mode(home, payload.get('cwd'))
        origin = 'configured default; the parent session has not selected a mode'
    ponytail = session_ponytail(payload, home, 'selected in the parent session',
                                'configured default; the parent session has not selected a level')
    return f'Forge mode: {mode.capitalize()} ({origin}). A mode named in your brief takes precedence.\n\n{ponytail}'


def on_first_edit(payload, home):
    if settle_edit_check(home, payload.get('session_id')) or has_opened_forge(payload.get('transcript_path')):
        return None
    return {'permissionDecision': 'deny', 'permissionDecisionReason': READ_FORGE_FIRST}


HANDLERS = {
    'SessionStart': on_session_start,
    'UserPromptSubmit': on_user_prompt,
    'SubagentStart': on_subagent_start,
    'PreToolUse': on_first_edit,
}


def main():
    try:
        payload = json.loads(sys.stdin.read().lstrip('﻿') or '{}')
        event = payload.get('hook_event_name')
        handler = HANDLERS.get(event)
        result = handler(payload, Path.home()) if handler else None
    except Exception:
        return

    if result:
        fields = {'additionalContext': result} if isinstance(result, str) else result
        sys.stdout.write(json.dumps({'hookSpecificOutput': {'hookEventName': event, **fields}}))


if __name__ == '__main__':
    main()
