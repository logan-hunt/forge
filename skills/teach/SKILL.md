---
name: teach
description: Explain code or a subsystem plainly, connecting what it does, how it works and why it was designed that way. Use for teaching, onboarding or understanding a change.
disable-model-invocation: false
---

# Teach

Help the reader understand the work at the depth their question needs. Keep the explanation read-only unless they separately authorize changes.

1. Infer their purpose and existing knowledge from the conversation. Inspect the relevant code or diff before explaining it.
2. Use [How](../how/SKILL.md) for runtime flow and ownership, and [Why](../why/SKILL.md) when historical rationale matters. Load only what the question needs. Follow the active [Forge mode](../forge/SKILL.md#lite-standard-and-max) for delegation.
3. Start with what the thing does and connect it to the case in front of the reader. Explain the important mechanism, tradeoff and failure mode. Keep evidence and uncertainty from Why intact.
4. Use a small diagram, example or actual screenshot when it makes the explanation clearer. Choose the medium for the idea; multiple diagrams and image generation are optional.
5. Give a complete answer to the question, then let follow-up questions set the next level of detail. Do not quiz the reader or turn the explanation into a report about your process.

Follow the adopter's writing style and [Unslop](../unslop/SKILL.md). Preserve useful qualifications rather than removing them for a cleaner story.
