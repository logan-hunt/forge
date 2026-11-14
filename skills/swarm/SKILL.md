---
name: swarm
description: Fan out N parallel workers, drain them, and return one report. Use for
  /swarm, 'swarm this', or parallel coverage, races, gauntlets, and exploration.
disable-model-invocation: true
---

# Swarm

## Start

Open a todolist with one entry per phase before launching anything.

1. Frame
2. Fan out
3. Aggregate
4. Report

## Phase A: Frame

1. State the done predicate and the artifact or report the swarm must return.
2. Choose the shape. Partition into slices, race N workers on identical briefs, or mix both. For a race or mixed shape, declare `first pass`, `rank all`, or `best-of` before spawning.
3. Pick the `swarm workers` role from [Forge model configuration](../../models.json), using [host delegation](../../docs/harness/README.md). For a comparison, name each arm’s provider, model and settings. Do not replace an unavailable requested role without user direction.
4. Give each worker its own writable output when it writes. When workers verify or measure commits, each brief names the exact SHAs. A measurement brief also names the method (sample count, what one sample is, order). The worker records both in its result.

## Phase B: Fan out

Launch the workers through the active host. Keep the parent in its starting checkout. Use host-owned worktree isolation only when the user explicitly requests separate checkouts; otherwise use disjoint write scopes or sequence edits. Use separate writable artifacts for non-code work. Follow the host’s completion and cancellation instructions.

Name the verified base branch or commit in the delegation request using the host’s supported fields. A base need not be published merely to start local work.

Every brief stands alone. Include the goal, scope, exact slice or race arm, how to verify, and what to report. Reports use `PASS`, `ISSUES`, or `BLOCKED` with evidence. A worker that can prove a defect reports `ISSUES` and lists every issue it can prove, not only the first.

If a worker drops out, proceed with N-1 and note it.

## Phase C: Aggregate

Read the terminal results. Drop a result that does not record the SHAs and method its brief names, and respawn that worker once. After a second miss, record a gap. A gap does not count as a pass. For coverage, every required slice needs a result. For a race, apply the selection rule declared up front. Use first pass, rank all, or best-of. Do not paste raw worker dumps.

## Phase D: Report

Return one consolidated in-chat report with a result table, issue one-liners, gaps or dropouts, and the race rule when used.
