# Choose the active host

Read only the adapter for the environment actually executing the task.

- In T3, including a Codex or Claude child running through T3, use [T3](t3.md).
- In native Claude Code outside T3, use [Claude Code](claude-code.md).
- In another native harness, use its exposed tools and runtime instructions. Resolve Forge roles through [forge-setup](../../skills/forge-setup/SKILL.md) only to capabilities that actually exist; do not call T3 APIs merely because this package documents them. Read sibling skills by file when no command is registered. A requested unavailable provider is a reported gap, never a silent substitution.

The adapters map capabilities; they do not expand task authorization. Read-only work remains nonmutating. Worktree creation, delegation, model options, completion and browser fallback follow the active host’s contract.
