# Choose the active host

Read only the adapter for the environment actually executing the task.

- In T3, including a Codex or Claude child running through T3, use [T3](t3.md).
- In native Claude Code outside T3, use [Claude Code](claude-code.md).
- In another native harness, use its exposed tools and runtime instructions. Resolve Forge roles through [forge-setup](../../skills/forge-setup/SKILL.md) only to capabilities that actually exist; do not call T3 APIs merely because this package documents them. Read sibling skills by file when no command is registered. A requested unavailable provider is a reported gap, never a silent substitution.

The adapters map capabilities; they do not expand task authorization. Read-only work remains nonmutating. Worktree creation, delegation, model options, completion and browser fallback follow the active host’s contract.

## Headless Codex planning

For a `codex exec` run awaiting human approval, the caller controls when the checkout becomes writable. Run planning with a read-only filesystem sandbox:

```sh
codex -a never exec -s read-only 'Use Forge. Plan only: <requested change>. Return the complete plan in your final message.'
```

For substantive work, a writable parent can save and render the returned plan using [plan delivery](../../skills/forge/references/plan-delivery.md). Honor any explicit no-write request across both sessions. If the caller also lacks write access, deliver the full plan in chat and disclose that limitation. After explicit approval, start the implementation run in the same checkout with `-s workspace-write` and supply the exact approved plan and scope. Keep planning-only runs read-only. An already approved plan, an authorized delegate brief or an explicit Full Send grant can start in the permitted implementation environment.

The read-only sandbox protects local source from sandboxed writes. For read-only work, expose only read-only external tools. Forge’s first-edit hook checks whether a session opened the router. The hook does not record a human’s approval.
