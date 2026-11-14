---
name: forge-help
description: Explain Forge modes, task routes and Ponytail levels. Use for Forge
  help, Ponytail help or choosing a workflow or level.
---

# Forge help

Answer the user's question from the current [Forge router](../forge/SKILL.md) and [guide](../../docs/guide/README.md). Keep the explanation focused on their task.

Explain Lite, Standard, and Max from the [mode rules](../forge/SKILL.md#lite-standard-and-max). Standard is the default unless `/forge-setup` configured another, and a selected mode lasts for the rest of the session. Mode selection preserves tests and approval gates.

Useful entry points: [brainstorm](../brainstorm/SKILL.md) to settle what a vague request means before planning, sharpen for a better-scoped prompt, how for runtime behavior, why for rationale, architect/arena for design alternatives, interrogate for executable adversarial review, recall for bounded context, [council](../council/SKILL.md) for a scored three-model review panel, and no-comments for careful comment cleanup. Explicit [full-send](../full-send/SKILL.md) grants autonomous delivery through merge for the task. Publication uses the existing quick-ship and conditional Graphite workflow. Ongoing PR monitoring belongs to the host.

Do not install tools, change models or edit instructions merely because the user asks for help. Resolve user and project model overrides through forge-setup; use `/forge-setup` only when asked to configure models, the default mode or the mode hooks.

For substantive investigations, [research](../research/SKILL.md) saves cited Markdown and standalone HTML under the active project’s `research/YYYY-MM-DD-topic/`, adds a repository-local Git exclusion, and previews/renders that HTML inline in T3. Explicit analysis-only/no-write requests produce conversation output only.

For Ponytail help, saved defaults and level selection, read [Ponytail levels](references/ponytail.md). For example prompts, see [recipes](references/recipes.md).
