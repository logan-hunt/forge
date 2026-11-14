---
name: forge-setup
description: Configure Forge model-role overrides, the default Forge mode and Ponytail level, and the optional Forge hook for project or user scope. Use for forge-setup or a request to install/remove the hook or change these settings.
disable-model-invocation: true
---

# Forge setup

Resolve this skill's canonical path. The package root is two directories above its folder. Use the bundled scripts by absolute path; do not assume where the package was installed. Installation exposes skills; hooks are an optional, separate action. Follow [Forge policy](../../docs/policy.md) and the [active host](../../docs/harness/README.md).

## Models, mode and Ponytail level

Read the effective configuration with `python3 <forge-root>/scripts/forge_config.py --project <project-root>`. It merges package role defaults, user settings at `~/.config/forge/config.json`, and project overrides at `~/.config/forge/projects/<project>-<hash>.json`, in that order. The file name is the project folder's name plus the first 12 hex characters of the SHA-256 of its resolved path, so moving or re-cloning a project to another path starts it without overrides. Project role entries replace the same user role. A null role uses the workflow default: ordinary roles inherit the active model, independent review prefers another available provider, and explicitly diverse panels discover the required model makers. Do not edit models.json or installed plugin caches to customize a user.

Discover providers, models and option schemas through the active host. Show current assignments and ask only for unresolved choices that affect cost, unavailable capabilities or an explicitly diverse panel. Do not launch test agents merely to list models. Ordinary roles inherit unless overridden; independent review still uses a separate agent and prefers another available provider. A configured or requested mixed-provider panel must not silently collapse to one provider.

For authorized changes, preview with the config script and apply the same command with `--apply`:

```sh
python3 <forge-root>/scripts/forge_config.py --scope project --project <project-root> --default-mode lite
python3 <forge-root>/scripts/forge_config.py --scope user --ponytail ultra
python3 <forge-root>/scripts/forge_config.py --scope user --role 'bug-fix' --target '{"providerInstanceId":"PROVIDER","model":"MODEL","options":{}}'
```

Use `--target null` to reset a role to inheritance. Panels use a JSON array of model selection objects. Validate actual providers, models and options against the live host before saving; the script checks data shape, not availability. Existing settings are preserved and changed files are backed up under `~/.config/forge/backups/`. Report what changed and what remains unavailable. `defaultMode` is `lite`, `standard` or `max` (Standard when unset); `ponytail` is `off`, `lite`, `full` or `ultra` (full when unset). A mode or level selected in a session lasts through it, including resume and compaction; new sessions use the effective defaults.

## Optional hook

The [installer](../../scripts/install-forge-hooks.py) installs one hook, [forge-mode.py](../../hooks/forge-mode.py), for Claude Code and Codex. Select the scope (`user` or `project`) and hosts. Default previews change nothing. An explicit request to install the specified hooks supplies that action's authorization; resolve genuinely missing scope or defaults before applying it.

```sh
python3 <forge-root>/scripts/install-forge-hooks.py --scope user --default-mode standard --ponytail full
python3 <forge-root>/scripts/install-forge-hooks.py --scope project --project <project-root> --host 'Claude Code'
```

Apply with `--apply`. Remove only this package's handlers with `--remove --apply`, using the same package, scope and hosts. User scope edits `~/.claude/settings.json` and/or `~/.codex/hooks.json`; project scope edits `<project>/.claude/settings.local.json` and/or `<project>/.codex/hooks.json`. The default is both hosts. Preserve unrelated settings and other packages' hooks. Backups go under `~/.config/forge/backups/`. Setup does not edit AGENTS.md or CLAUDE.md.

At session start, on prompts and in subagents the hook reports the Forge mode and the Ponytail level, and injects the [Ponytail rules](../ponytail/SKILL.md) for that level unless it is off. It tracks `/forge lite|standard|max`, `/ponytail lite|full|ultra|off`, "stop ponytail", and their namespaced forms; `/ponytail default <level>` saves the user default. Before a session's first edit it reminds the agent to read Forge; this reminder is not a plan-approval enforcement mechanism. `--default-mode` and `--ponytail` persist at the selected scope. The Ponytail level never selects the Forge mode or grants approval. Ponytail's band ledger, codebase map and status line are not included.

Tell users to start a new session after changing hooks. Codex requires review/trust in `/hooks` before changed hooks run; project hooks also depend on project trust. Verify the effective mode, level and a change of each in a new session when that runtime verification is authorized. Static validation is not proof of successful host loading.

## Local skill discovery

For a copied package, [activate-forge.py](../../scripts/activate-forge.py) previews project or user skill links without replacing existing skills or instructions. Use `--apply` to create them or `--remove --apply` to remove only this package's links. Marketplace installations normally expose skills themselves and do not need these extra links.

Project discovery, hooks and configuration use the same root: the nearest ancestor with `.git`, otherwise the supplied directory. A nested repository is a separate project. Use `--project` when the working directory does not identify the intended project.
