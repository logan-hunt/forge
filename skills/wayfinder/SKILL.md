---
name: wayfinder
description: Plan work that is too large for one agent session as a shared map of decision tickets on the issue tracker. Resolve the tickets one at a time until the way to the destination is clear. Use for /wayfinder.
disable-model-invocation: true
---

# Wayfinder

A loose idea arrives. It is too large for one agent session, and the way from here to the **destination** is not visible yet. Wayfinding finds that way. This skill charts the way as a **shared map** on the issue tracker. It then works the map's **decision tickets** one at a time until the route is clear. A decision ticket is a question whose resolution is a decision. It is not a slice of a build.

The destination is different for each effort. To name it is the first act of charting, because it shapes every ticket. It can be a spec to hand off, a decision to lock before planning, or a change made in place, such as a data-structure migration. The map suits any domain: engineering work, course content, or other work with this shape.

## Plan, do not do

Wayfinder is planning by default. Each ticket resolves a decision. The map is done when the way is clear and nothing is left to decide before someone does the work. The urge to do the work is usually the signal that you reached the edge of the map and it is time to hand off. An effort can override this in its **Notes** and carry execution into the map. Without that note, produce decisions, not deliverables.

Notes describe the scope of an effort. They do not grant approval. A code change still needs plan approval under the [Forge workflow](../forge/SKILL.md#required-workflow). An action on an external system still needs the user's authorization under [Forge policy](../../docs/policy.md#external-actions-and-durable-changes). An invocation of this skill and a confirmed tracker authorize tracker writes only.

## Refer by name

Every map and ticket is an issue, so it has a name: its title. In everything the human reads, refer to it by that name, never by a bare id, number or slug. A row of `#42, #43, #44` is illegible. The name wraps the link to the issue.

## The map

The map is a single issue on the project's tracker with the label `wayfinder:map`. Its tickets are child issues of the map.

The map is an index, not a store. It lists the decisions made and points at the tickets that hold their detail. A decision lives in one place, its ticket. The map gives one line and a link.

The tracker decides where the map, the child tickets, the blocking edges and the frontier query live. Read "Wayfinding operations" in the [issue tracker reference](../forge/references/issue-tracker.md). If the project has no tracker, use the local Markdown tracker.

### The map body

The body is the whole map at low resolution. Each session loads it once. The body does not list open tickets. A query finds them.

```markdown
## Destination

<what the end of this map looks like: the spec, decision or change this effort is finding its way to. One or two lines. Every session reads it before it chooses a ticket.>

## Notes

<domain. Skills that every session must read. Standing preferences for this effort.>

## Decisions so far

<!-- the index: one line for each closed ticket, enough to judge relevance, with a link to the ticket for the detail -->

- [<closed ticket title>](link): <one-line summary of the answer>

## Not yet specified

<!-- see "Fog of war": in-scope questions that are not sharp enough to ticket yet -->

## Out of scope

<!-- see "Out of scope": work ruled beyond the destination. It is closed and does not return. -->
```

### Tickets

Each ticket is a child issue of the map. Its body is the question, sized to one agent session:

```markdown
## Question

<the decision or investigation this ticket resolves>
```

Each ticket has one `wayfinder:<type>` label: `research`, `prototype`, `grilling` or `task`. See [Ticket types](#ticket-types). A map and its tickets carry only `wayfinder:` labels. They do not carry a triage role such as `ready-for-agent`, because they are decisions, not implementation work.

A session **claims** a ticket before any work: it assigns the ticket to the developer who drives the map. Concurrent sessions skip a claimed ticket. An open ticket with no assignee is unclaimed.

Blocking uses the tracker's native dependency relation, because the tracker's own view then shows the frontier. Use a body convention only where the tracker has no native blocking. A ticket is **unblocked** when every ticket that blocks it is closed. The **frontier** is the set of open, unblocked, unclaimed children.

The answer is not part of the body. Record it on resolution. Link the assets you created for a ticket from the issue. Do not paste them into it.

## Ticket types

Every ticket is **HITL** (human in the loop) or **AFK** (the agent works alone). A HITL ticket resolves only through a live exchange with the human. The agent never answers for the human.

- **Research** (AFK). Read documentation, third-party APIs or local resources to find a fact that a decision waits on. Resolve it with the [research](../research/SKILL.md) skill. Put the findings in the resolution comment, because the saved report is local.
- **Prototype** (HITL). Make a cheap, rough, concrete artifact for the human to react to: an outline, a stub, or UI or logic code. Use the [Prototype playbook](../forge/playbooks/prototype.md). Link the prototype as an asset. Use this type when "how does it look" or "how does it behave" is the key question.
- **Grilling** (HITL). A conversation. This is the default type. Follow [grill-with-docs](../grill-with-docs/SKILL.md).
- **Task** (HITL or AFK). Manual work that must happen before a decision can be made. Examples: sign up for a service to judge its API, provision access, or move data to see its shape. The agent does the task alone only when it is read-only or the user authorized it. Otherwise it gives the human a precise checklist. For steps that only a human can perform, use [wizard](../wizard/SKILL.md). The ticket is resolved when the work is done. The answer records what was done and the facts that later tickets depend on. Examples are new URLs, row counts and where the credentials are stored.

## Fog of war

The map is incomplete on purpose. Do not chart what you cannot see yet. Beyond the live tickets is the **fog of war**. It holds the decisions and investigations that you know are ahead but cannot state yet, because they depend on open questions. When you resolve a ticket, some of the fog ahead of it becomes specifiable. Make those parts into new tickets.

The **Not yet specified** section of the map records the fog: the suspected question, the area to visit later. Everything in it is in scope. It is only not sharp enough to ticket. Write as loosely or as fully as the view allows.

Fog or ticket? The test is whether you can state the question precisely now. Whether you can answer it now does not matter.

- **Ticket** when the question is already sharp, even if it is blocked.
- **Not yet specified** when you cannot phrase it that sharply. Do not cut the fog into ticket-sized pieces in advance. One patch can become several tickets, or none.

**Not yet specified** excludes what is already decided, what is already a live ticket, and what is out of scope.

## Out of scope

The destination fixes the scope. Work beyond the destination is out of scope. It is not fog, and it does not belong in **Not yet specified**. It goes in the map's **Out of scope** section.

Out-of-scope work does not return unless the destination is redrawn. It then returns as a new effort.

When an existing ticket turns out to be past the destination, close it. Add one line to the **Out of scope** section: the summary, why it is out of scope, and a link to the closed ticket. Do not add it to **Decisions so far**, which records the route taken.

## Invocation

The skill has two modes. In both, resolve at most one ticket in a session. Research tickets are the exception.

### Chart the map

The user invokes the skill with a loose idea.

1. **Name the destination.** Follow [grill-with-docs](../grill-with-docs/SKILL.md) to establish what this map finds its way to. The destination fixes the scope, so settle it first.
2. **Map the frontier.** Grill again, breadth-first: cover the whole space, and do not go deep on one thread. Find the open decisions and the first steps that can start now. If you find no fog, the journey fits in one session and no map is necessary. Stop and ask the user how to proceed.
3. **Create the map** with the label `wayfinder:map`. Fill in Destination and Notes. Leave Decisions so far empty. Put the fog in **Not yet specified**.
4. **Create the tickets that you can specify now** as child issues of the map. Then add the blocking edges and the cross-references in a second pass, because an issue needs an id before another issue can reference it. Write each cross-reference with a real id. A placeholder such as `#<n>` links to an unrelated issue. Everything that you cannot specify yet stays in **Not yet specified**.
5. **Resolve the research tickets.** For each `research` ticket you created, run the research and record the resolution. Run them in parallel with delegates when the active Forge mode allows delegation.
6. Stop. Charting is one session's work.

### Work through the map

The user invokes the skill with a map (a URL or a number). A ticket is optional. Without one, you choose the next decision.

1. Load the **map**: the low-resolution view, not every ticket body.
2. Choose the ticket. If the user named one, use it. Otherwise take the first frontier ticket in order. **Claim it** before any work.
3. Resolve it as the type that its `wayfinder:<type>` label names. Read the label, because the body does not state the type. Fetch the full body of a related or closed ticket when you need it. Read the skills that the map's Notes name. If in doubt, follow [grill-with-docs](../grill-with-docs/SKILL.md).
4. Record the resolution. Post the answer as a resolution comment, close the issue, and add a context pointer to the map's **Decisions so far**.
5. Add the tickets that the answer revealed: create them, then add their edges. Move the fog that is now specifiable from **Not yet specified** into new tickets. If the answer shows that a ticket is beyond the destination, rule it out of scope. If the decision invalidates other parts of the map, update or delete those tickets.

The user can run unblocked tickets in parallel. Expect other sessions to edit the tracker at the same time.

### Reach the destination

The map is done when no ticket is open and **Not yet specified** is empty. Tell the user, and name the next step for the destination:

- A spec → [to-spec](../to-spec/SKILL.md), with the map's **Decisions so far** as the source. Then [to-tickets](../to-tickets/SKILL.md).
- A change to build now → the [Forge plan step](../forge/SKILL.md#required-workflow), with the decisions as its input.
- A decision → an ADR through [domain-modeling](../domain-modeling/SKILL.md), when it meets the three conditions.

Do not start that step until the user asks for it.
