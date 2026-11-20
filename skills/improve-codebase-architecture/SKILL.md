---
name: improve-codebase-architecture
description: Scan a codebase for deepening opportunities, present them as a visual research report, then grill through the one the user picks. Use for /improve-codebase-architecture.
disable-model-invocation: true
---

# Improve codebase architecture

Find architectural friction and propose **deepening opportunities**: refactors that turn shallow modules into deep ones. The aim is testability and code that an agent can navigate.

This skill is read-only for product code. It writes the research report, and the glossary and ADR entries that [domain-modeling](../domain-modeling/SKILL.md) permits. A chosen candidate becomes a normal Forge task with its own plan approval.

Three references apply:

- [Deep Modules](../forge/references/principles/deep-modules.md) for the architecture vocabulary: module, interface, depth, seam, adapter, leverage, locality. Use these terms exactly in every suggestion. Do not use "component", "service", "API" or "boundary".
- [Design red flags](../architect/references/design-red-flags.md) for the symptoms to look for.
- `GLOSSARY.md` for the domain. Its terms name good seams. The ADRs in `docs/adr/` record decisions that this skill does not argue again.

## Process

### 1. Explore

**Decide where to look before you look.** A deep module pays back when later changes to it are easier, so give more weight to the parts of the codebase that changed recently.

- If the user named a direction (a module, a subsystem, a pain point), take it.
- Otherwise, read a long stretch of the commit history (`git log --oneline`) to find the hot spots: the files and areas that appear again and again. Start there. If the changes are scattered, look more widely.

Read `GLOSSARY.md` and the ADRs in the area first.

Then explore the codebase. In Standard and Max, delegate the exploration to a fresh context with the `how explorer` role, under [Delegation and models](../forge/SKILL.md#delegation-and-models). In Max, split a large area between several explorers with [swarm](../swarm/SKILL.md). In Lite, explore it yourself.

Screen what you read against the [design red flags](../architect/references/design-red-flags.md). Do not follow them as a rigid checklist. Also note where you meet friction:

- Where must you move between many small modules to understand one concept?
- Where were pure functions extracted only for testability, while the real bugs hide in how they are called (no locality)?
- Which parts of the codebase are untested, or hard to test through their current interface?

Apply the **deletion test** to anything you suspect is shallow. Does its deletion concentrate complexity, or only move it? "It concentrates" is the signal you want.

Keep a candidate only when the deepening deletes code, branches or invalid states. A candidate that only adds a layer or a seam is not a candidate. This is the rule of the [Refactoring playbook](../forge/playbooks/refactoring.md) and of [Ponytail](../ponytail/SKILL.md#simplify-existing-code).

### 2. Present candidates as a research report

Save the review with the [research](../research/SKILL.md) skill, under `research/YYYY-MM-DD-architecture-<area>/` in the project. Follow its exclusion procedure, so that nothing in the folder is tracked.

- `findings.md` holds the candidates as text. It is the source copy.
- Each before and after diagram is an `.html` fragment in the same folder. Include it in `findings.md` with an `<!-- include: name.html -->` line.
- Build `report.html` with the shared builder, and present it as the research skill describes.

Each candidate is one section of `findings.md` with:

- **Files**: the files and modules involved
- **Problem**: why the current architecture causes friction
- **Solution**: a plain description of what changes
- **Benefits**: in terms of locality and leverage, and how the tests improve
- **Before / After diagram**: one fragment, side by side, drawn for this candidate, showing the shallow shape and the deep one
- **Recommendation strength**: `Strong`, `Worth exploring` or `Speculative`

End the report with a **Top recommendation** section: the candidate you would do first, and why.

Use `GLOSSARY.md` vocabulary for the domain and Deep Modules vocabulary for the architecture. If `GLOSSARY.md` defines "Order", write "the Order intake module", not "the FooBarHandler" and not "the Order service".

**ADR conflicts.** If a candidate contradicts an ADR, include it only when the friction is real enough to revisit the ADR. Mark it clearly in the section: "contradicts ADR-0007, but worth a second look because…". Do not list every refactor that an ADR forbids.

See [html-report.md](references/html-report.md) for the card layout, the diagram fragments and the tone.

Do not propose interfaces yet. After you present the report, ask the user which candidate to explore. Use the native question tool when the host has one.

### 3. Grilling loop

When the user picks a candidate, follow [grilling](../grilling/SKILL.md) through the decision tree. Cover the constraints, the dependencies, the shape of the deepened module, what sits behind the seam and which tests survive.

Keep the domain model current with [domain-modeling](../domain-modeling/SKILL.md) as decisions are made:

- **The deepened module is named after a concept that is not in `GLOSSARY.md`.** Add the term.
- **A fuzzy term becomes sharp in the conversation.** Update `GLOSSARY.md` at that moment.
- **The user rejects the candidate for a reason that a later review must know.** Offer an ADR: "Do you want me to record this as an ADR, so that later architecture reviews do not suggest it again?" Do not offer one for a temporary reason ("not worth it now") or an obvious one.
- **The user wants alternative interfaces for the deepened module.** Use [architect](../architect/SKILL.md) with a different design constraint for each runner.

To build the result, start a [Refactoring](../forge/playbooks/refactoring.md) task under the Forge workflow.
