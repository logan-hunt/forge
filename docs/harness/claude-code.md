# Forge in native Claude Code

When running through T3, use [the T3 adapter](t3.md), including its cross-provider and worktree rules. This file covers native Claude Code outside T3.

Discover the actual tool schema. Map a delegated task to the available `Agent` tool and include the role document from `../../agents/` when a named agent type is not registered. Use inherited settings for routine work. Resolve model-role overrides through [forge-setup](../../skills/forge-setup/SKILL.md) and verify availability; do not replace an OpenAI role with Claude and call the result a diverse-model panel. If the native host cannot supply the requested provider, report the limitation and ask for a supported route.

Skills can be discovered through the installed plugin or project/user skill links. Plugin skill commands may be namespaced, such as `/forge:forge`. Read sibling SKILL.md files directly when a skill is not exposed. Follow the adopter's AGENTS.md and CLAUDE.md; setup does not replace them.

Follow [Forge policy](../policy.md#task-isolation-and-planning) for checkout and approval policy. Discover `AskUserQuestion` and use it for plan approval when exposed and allowed. Use the host's supported worktree/delegation lifecycle and check actual fields instead of copying parameters from another harness. No host limitation expands authorization.

For scoped history, inspect native Claude records under `~/.claude/projects/`, preserving session/workspace provenance and coverage. Do not treat user-role text as proven human origin. Cross-harness history requires the user's scope and each harness's native reader or documented records.

Choose the available browser route under shared policy. Prefer an existing persistent agent-browser session outside a host-mandated browser. On failure, use another permitted available route rather than repeatedly retrying the same failure; preserve sessions and report actual login/capability blockers.
