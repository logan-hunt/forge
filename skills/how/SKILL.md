---
name: how
description: Explain how code works, including runtime flow, ownership and where changes belong. Use for walkthroughs, onboarding and module-placement questions. Use why for historical rationale.
disable-model-invocation: false
---

# How

Trace the code needed to answer the question. Explain the mechanism and ownership at the reader's level, without narrating every symbol.

For a narrow question, inspect the relevant module and callers and explain directly. For a subsystem, trace its entry points, data flow, boundaries and failure paths. State a reasonable interpretation when the scope is ambiguous and let the user redirect.

Follow the active [Forge mode](../forge/SKILL.md#lite-standard-and-max) and the parent brief for delegation. Lite stays solo unless the user requests delegates. When authorized parallel work adds useful coverage, choose independent slices and use the configured How roles through [Forge setup](../forge-setup/SKILL.md) and the [host adapter](../../docs/harness/README.md). Children do not launch their own workers without authorization.

[Explorer prompts](references/explorer-prompt.md) help scope independent reads. The [explainer prompt](references/explainer-prompt.md) provides a structure for direct explanation or synthesis. Use only the sections the question needs.

Ground the answer in source locations and actual call paths. Name important invariants, edge cases and coverage gaps. Read-only questions do not authorize implementation.
