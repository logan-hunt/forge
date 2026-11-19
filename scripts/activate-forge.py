"""Preview, expose or remove local Forge skill links without replacing instructions or installing hooks."""
import argparse
import os
from pathlib import Path

from forge_config import project_root

HOSTS = ('agents', 'claude', 'cursor')
RETIRED_SKILLS = (
    'figure-it-out',
    'in-your-own-words',
    'interrogate',
    'ketchup',
    'no-comments',
    'recall',
    'sharpen',
    'statechart',
    'typescript-best-practices',
    'unslop',
    'git-prune',
    'principle-attack-the-premise',
    'principle-boundary-discipline',
    'principle-build-the-lever',
    'principle-encode-lessons-in-structure',
    'principle-exhaust-the-design-space',
    'principle-experience-first',
    'principle-explain-the-number',
    'principle-fix-root-causes',
    'principle-foundational-thinking',
    'principle-guard-the-context-window',
    'principle-laziness-protocol',
    'principle-make-operations-idempotent',
    'principle-migrate-callers-then-delete-legacy-apis',
    'principle-minimize-reader-load',
    'principle-model-the-domain',
    'principle-outcome-oriented-execution',
    'principle-prove-it-works',
    'principle-redesign-from-first-principles',
    'principle-separate-before-serializing-shared-state',
    'principle-sequence-verifiable-units',
    'principle-subtract-before-you-add',
    'principle-test-behavior-not-implementation',
    'principle-type-system-discipline',
    'teach',
    'technical-writing',
)


def planned_links(source, root, hosts=HOSTS):
    return [(root / f'.{host}/skills' / skill.name, skill)
            for skill in sorted((source / 'skills').iterdir()) if (skill / 'SKILL.md').is_file()
            for host in hosts]


def points_directly_to(link, target):
    if not link.is_symlink():
        return False
    return link.readlink() in (target, Path(os.path.relpath(target, link.parent)))


def resolves_to(link, target):
    return link.is_symlink() and link.resolve() == target.resolve()


def inspect_links(links, root, remove=False, matches=resolves_to):
    changes = []
    for link, target in links:
        for parent in link.parents:
            if parent == root:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError(f'Preserve existing parent; not an owned directory: {parent}')
        if remove:
            if matches(link, target):
                changes.append((link, target))
        elif not matches(link, target):
            if link.exists() or link.is_symlink():
                raise ValueError(f'Collision; preserve existing asset: {link}')
            changes.append((link, target))
    return changes


def activate(source, root, apply=False, remove=False, hosts=HOSTS):
    source, root = source.resolve(), root.resolve()
    if not (source / 'skills/forge/SKILL.md').is_file():
        raise ValueError('Source must be the Forge package root')
    links = planned_links(source, root, hosts)
    retired = [(root / f'.{host}/skills' / name, source / 'skills' / name)
               for name in RETIRED_SKILLS if not (source / 'skills' / name / 'SKILL.md').is_file()
               for host in hosts]
    retirements = inspect_links(retired, root, remove=True, matches=points_directly_to)
    removals = []
    additions = []
    if remove:
        removals = inspect_links(links, root, remove=True)
    else:
        additions = inspect_links(links, root)

    for changes, matches in ((retirements, points_directly_to), (removals, resolves_to)):
        for link, target in changes:
            print(f'REMOVE{"" if apply else " (preview)"} {link} -> {target}')
            if apply and matches(link, target):
                link.unlink()

    for link, target in additions:
        print(f'LINK{"" if apply else " (preview)"} {link} -> {target}')
        if apply:
            link.parent.mkdir(parents=True, exist_ok=True)
            link.symlink_to(os.path.relpath(target, link.parent))
    return retirements + removals + additions


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--apply', action='store_true')
    parser.add_argument('--remove', action='store_true')
    parser.add_argument('--scope', choices=('user', 'project'), default='user')
    parser.add_argument('--home', type=Path, default=Path.home())
    parser.add_argument('--project', type=Path, default=Path.cwd())
    parser.add_argument('--host', action='append', choices=HOSTS, help='repeat to select discovery roots; default: all')
    parser.add_argument('--source', type=Path, default=Path(__file__).resolve().parents[1])
    args = parser.parse_args()
    try:
        root = args.home if args.scope == 'user' else project_root(args.project)
        activate(args.source.resolve(), root.resolve(), args.apply, args.remove, args.host or HOSTS)
    except (OSError, ValueError) as error:
        parser.exit(1, f'{error}\n')


if __name__ == '__main__':
    main()
