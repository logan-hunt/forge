"""Preview, expose or remove local Forge skill links without replacing instructions or installing hooks."""
import argparse
import os
from pathlib import Path

from forge_config import project_root

HOSTS = ('agents', 'claude', 'cursor')


def planned_links(source, root, hosts=HOSTS):
    return [(root / f'.{host}/skills' / skill.name, skill)
            for skill in sorted((source / 'skills').iterdir()) if (skill / 'SKILL.md').is_file()
            for host in hosts]


def inspect_links(links, root, remove=False):
    changes = []
    for link, target in links:
        for parent in link.parents:
            if parent == root:
                break
            if parent.is_symlink() or (parent.exists() and not parent.is_dir()):
                raise ValueError(f'Preserve existing parent; not an owned directory: {parent}')
        owned = link.is_symlink() and link.resolve() == target.resolve()
        if remove:
            if owned:
                changes.append((link, target))
        elif not owned:
            if link.exists() or link.is_symlink():
                raise ValueError(f'Collision; preserve existing asset: {link}')
            changes.append((link, target))
    return changes


def activate(source, root, apply=False, remove=False, hosts=HOSTS):
    source, root = source.resolve(), root.resolve()
    if not (source / 'skills/forge/SKILL.md').is_file():
        raise ValueError('Source must be the Forge package root')
    changes = inspect_links(planned_links(source, root, hosts), root, remove)
    for link, target in changes:
        print(f'{"REMOVE" if remove else "LINK"}{"" if apply else " (preview)"} {link} -> {target}')
    if apply:
        for link, target in changes:
            if remove:
                if link.is_symlink() and link.resolve() == target.resolve():
                    link.unlink()
            else:
                link.parent.mkdir(parents=True, exist_ok=True)
                link.symlink_to(os.path.relpath(target, link.parent))
    return changes


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
