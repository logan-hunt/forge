---
name: to-tickets
description: Break a plan, a spec or the current conversation into tracer-bullet tickets, each with its blocking edges, and publish them to the project issue tracker. Use for /to-tickets.
disable-model-invocation: true
---

# To tickets

Break a plan, a spec or a conversation into a set of **tickets**. Each ticket is a tracer-bullet vertical slice. Each ticket declares the tickets that **block** it.

Find the tracker and the triage roles with the [issue tracker reference](../forge/references/issue-tracker.md).

## Process

### 1. Gather context

Work from what is already in the conversation. If the user passes a reference, such as a spec path, a saved Forge plan, an issue number or a URL, fetch it. Read its full body and comments.

When the source is a saved Forge plan, each unit under "Implementation and proof" is a candidate ticket. Its dependency is a blocking edge, and its success check is the ticket's proof.

### 2. Explore the codebase

If you did not explore the codebase already, do so now. Use the vocabulary in `GLOSSARY.md` in ticket titles and descriptions. Respect the ADRs in the area you touch.

Look for a prefactor that makes the implementation easier. "Make the change easy, then make the easy change."

### 3. Draft vertical slices

Break the work into tracer-bullet tickets.

<vertical-slice-rules>

- Each slice cuts a narrow but complete path through every layer (schema, API, UI, tests). It is vertical. It is not a horizontal slice of one layer.
- A completed slice can be demonstrated or verified by itself.
- Each slice fits in a single fresh context window.
- Prefactoring comes first.

</vertical-slice-rules>

Give each ticket its **blocking edges**: the other tickets that must complete before it can start. A ticket with no blockers can start immediately.

**A wide refactor is the exception to vertical slicing.** A wide refactor is one mechanical change, such as a renamed column or a retyped shared symbol, whose blast radius covers the whole codebase. A single edit breaks thousands of call sites, and no vertical slice can pass the checks. Sequence it as expand and contract:

1. Expand. Add the new form beside the old form, so that nothing breaks.
2. Migrate. Move the call sites in batches sized by blast radius, for each package or directory. Each batch is one ticket, blocked by the expand ticket. The checks pass after each batch because the old form still exists.
3. Contract. Delete the old form when no caller remains. This ticket is blocked by every migrate batch.

When the batches cannot pass the checks alone, keep the sequence and add a final integrate-and-verify ticket that all batches block. Only that ticket promises passing checks.

### 4. Quiz the user

Show the proposed set as a numbered list. For each ticket, show:

- **Title**: a short descriptive name
- **Blocked by**: the tickets that must complete first, if any
- **What it delivers**: the end-to-end behavior that this ticket makes work
- **Proof**: the observable check that shows the slice works

Ask the user:

- Is the granularity right, too coarse or too fine?
- Are the blocking edges correct? Does each ticket depend only on tickets that really gate it?
- Must any tickets be merged or split?

Iterate until the user approves the set.

### 5. Publish the tickets

Before you publish, search the tracker for an existing issue that already owns each outcome. Reuse that issue. Do not create a duplicate.

Publish the approved tickets. The tickets are the same on every tracker. Only the form of the blocking edges changes.

- **Local Markdown.** Write one file for each ticket under `.scratch/<feature-slug>/issues/<NN>-<slug>.md`. Number from `01` in dependency order, blockers first. Use the local ticket template.
- **A real tracker.** Publish one issue for each ticket in dependency order, blockers first, so that each blocking edge can reference a real identifier. Use the tracker's native blocking relation where it has one. Otherwise list the blockers under "Blocked by". If the source was an existing issue, make each ticket its sub-issue. Apply the `ready-for-agent` triage role unless the user says otherwise.

Do not close or modify a parent issue.

<local-ticket-template>

# <NN>: <Ticket title>

**What to build:** the end-to-end behavior that this ticket makes work, from the user's perspective. Not a layer-by-layer implementation list.

**Blocked by:** the numbers and titles of the tickets that gate this one, or "None (can start immediately)".

**Status:** ready-for-agent

**Proof:** the observable check that shows this slice works, such as a test at an agreed seam or an action on the real surface.

- [ ] Acceptance criterion 1
- [ ] Acceptance criterion 2

</local-ticket-template>

<issue-template>

## Parent

A reference to the parent issue on the tracker. Omit this section if the source was not an existing issue.

## What to build

The end-to-end behavior that this ticket makes work, from the user's perspective. Not a layer-by-layer implementation list.

## Acceptance criteria

- [ ] Criterion 1
- [ ] Criterion 2

## Proof

The observable check that shows this slice works, such as a test at an agreed seam or an action on the real surface.

## Blocked by

- A reference to each blocking ticket, or "None (can start immediately)". Omit this section when the blockers are native edges.

</issue-template>

In both forms, do not include specific file paths or code snippets. They become outdated quickly. Exception: a prototype snippet that encodes a decision more precisely than prose, such as a state machine, a reducer, a schema or a type shape. Include only the parts that carry the decision, and note that it came from a prototype.

To build the tickets, use [implement-spec](../implement-spec/SKILL.md).
