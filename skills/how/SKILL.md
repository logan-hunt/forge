---
name: how
description: Explain how code works, including runtime flow, ownership and where changes belong. Use for teaching, walkthroughs, onboarding and module-placement questions. Use why for historical rationale and teach for a course over several sessions.
disable-model-invocation: false
---

# How

Start with what the code does for the reader’s case. Match the depth to their question and experience. For a walkthrough, trace a concrete example through the code, including the tradeoff and failure mode that matter to the reader. Let follow-up questions set the next level of detail. Use a diagram or screenshot when it clarifies the flow. Use [Why](../why/SKILL.md) when the reader asks what historical evidence explains a design choice.

For a narrow question, inspect the relevant module and callers and explain directly. For a subsystem, trace its entry points, data flow, boundaries and failure paths. State a reasonable interpretation when the scope is ambiguous and let the user redirect.

Follow the active [Forge mode](../forge/SKILL.md#lite-standard-and-max) and the parent brief for delegation. Lite stays solo unless the user requests delegates. When authorized parallel work adds useful coverage, choose independent slices and use the configured How roles through [Forge setup](../forge-setup/SKILL.md) and the [host adapter](../../docs/harness/README.md). Children do not launch their own workers without authorization.

[Explorer prompts](references/explorer-prompt.md) help scope independent reads. The [explainer prompt](references/explainer-prompt.md) provides a structure for direct explanation or synthesis. Use only the sections the question needs.

Ground the answer in source locations and actual call paths. Name important invariants, edge cases and coverage gaps. Read-only questions do not authorize implementation.
