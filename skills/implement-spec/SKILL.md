---
name: implement-spec
description: Implement a spec and its tickets as a task graph, working the ready frontier through Forge's queue playbooks. Use for /implement-spec after to-spec and to-tickets.
disable-model-invocation: true
---

# Implement spec

The user gave you a spec. The spec has tickets that describe how to implement it. Find both with the [issue tracker reference](../forge/references/issue-tracker.md).

The goal is the whole spec implemented, with every ticket closed in the way the tracker closes work.

The tickets are not a list of steps. They are a **task graph** with blocking edges. At every moment the graph has a **frontier**: the tickets whose blockers are all done.

A ticket is **done** when its check passes and you verified the result. Done decides the frontier. A ticket is **closed** when the tracker's rule for closing work is met, which can be later, for example when its pull request merges.

This skill maps the task graph to Forge's queue playbooks. It adds no gate and removes none. The [Forge workflow](../forge/SKILL.md#required-workflow), the active mode and [Forge policy](../../docs/policy.md) apply without change.

## 1. Read the graph

Read the spec and the tickets. State the title of each ticket. Draw the task graph and name the first frontier.

## 2. Present the plan

The spec and the ticket graph are the plan. Present them under the Forge plan step with these additions:

- **Units.** Each ticket is one unit under [Orchestrate](../forge/playbooks/orchestrate.md). A blocking edge is a dependency between units.
- **Seams.** The seams under test, from the spec. Each unit is built with [tdd](../tdd/SKILL.md) at those seams.
- **Proof.** The observable check for each unit, from the ticket's Proof line and acceptance criteria.
- **PR layers.** One ticket is one PR layer. Stack a layer on its parent only where the ticket depends on that parent. Tickets with no dependency between them are separate PRs. A ticket that depends on several tickets needs one base that contains them all. Order those tickets as one stack, state the order, and put the dependent ticket on top. Combine tickets in one layer only where a ticket cannot pass the checks alone, and say why.
- **Owners.** Which units you build yourself and which you delegate.

Wait for approval before you edit. An active [full-send](../full-send/SKILL.md) grant is that approval.

## 3. Run the queue

Run the units with [Orchestrate](../forge/playbooks/orchestrate.md). It owns the partition, the first representative unit, the briefs, supervision and the verification of each unit. This skill adds only the ticket mapping:

- The frontier decides which units can start. Tickets on the frontier are independent.
- In Standard and Max, run frontier tickets in parallel with delegates when that helps. In Lite, work them one at a time yourself.
- Delegates use the `feature` role and a [forge-agent](../../agents/forge-agent.md) brief. Point each brief to the spec, the ticket, the research notes and the current diff. Do not copy what a pointer already supplies.
- When several tickets need the same exploration, do it once. Save the notes under the project's `research/` folder with the [research](../research/SKILL.md) exclusion procedure.
- When a unit is done, compute the frontier again and start the tickets that are now ready. On a local Markdown tracker, close the ticket now.

## 4. Review and deliver

When all tickets are complete, run the full test suite once. Complete the mode's [review](../forge/references/review.md) on the whole diff and address the findings.

Deliver with [Autopilot-stack](../forge/playbooks/autopilot-stack.md) when layers depend on each other, and with [Publication and PR updates](../forge/playbooks/opening-a-pr.md) otherwise. First publication needs its own authorization under Forge policy.

## 5. Close the tickets

Close each remaining ticket when the tracker's rule for closing work is met. When a pull request closes the work, put the tracker's closing reference for that layer's ticket in the PR description.

Report one line for each ticket: its title, its PR layer, its check result and whether it is closed. Report every ticket that stays open, and why.
