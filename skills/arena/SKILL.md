---
name: arena
description: Spawn N parallel candidates at the same task, pick a base, graft the
  strongest parts of the losers into it. Use for /arena, 'arena this', 'throw it in
  the arena', or when one attempt at a non-trivial artifact would lock in the wrong
  shape.
disable-model-invocation: true
---

# Arena

Open a todolist with one entry per phase (Frame, Fan out, Cross-judge, Pick, Graft, Verify) before launching anything.

## Phase A: Frame

Every candidate gets the same prompt, so the prompt is the contract.

1. State the artifact each candidate is producing.
2. Derive the rubric, 3-6 concrete gradeable criteria for what success looks like on *this* task. It is the picker's tool in Phase D. Candidates only see the task.
3. Pick runners from the `arena runners` role resolved through [Forge setup](../forge-setup/SKILL.md), using [host delegation](../../docs/harness/README.md). When the role inherits, use separate candidates on the active model. Preserve explicitly configured or requested provider diversity. If a requested role is unavailable, report the missing capability and ask for an alternative instead of silently substituting a model. Use the same model for multiple candidates only when the task calls for generation diversity rather than a mixed-model review.
4. Give each candidate its own output location, per the [separate-before-serializing-shared-state](../forge/references/principles/separate-before-serializing-shared-state.md) principle. Use separate checkouts only when explicitly requested by the user, through the active host; never create a child checkout in the shell. Otherwise use separate scratch artifacts or sequence edits in the starting checkout. For plan-only or read-only requests, candidates return their packages in the delegation result without creating checkouts or writing files. Only an explicit artifact request authorizes the corresponding output files. When implementation candidates need the current uncommitted state, provide the scoped patch and base identity through the host-supported mechanism; do not assume a fresh worktree contains it.

## Phase B: Fan out

Launch the candidates through the active host, each with the task, shared grounding, an isolated output location (or response-only output for read-only tasks) and a short rationale naming alternatives. Follow host completion notifications and cancellation rules; do not create a parallel polling loop.

If a candidate produces no output, proceed with N-1 and note the dropout.

## Phase C: Cross-judge

After all Phase B candidates complete, resolve the `arena cross-judge pool` role and select a separate read-only judge, preferring another available provider. Preserve explicitly requested cross-model judgment; report a missing required provider rather than silently substituting. Same-provider judgment is valid when diversity was not required. Validate the selection through the host. The judge sees the rubric and candidates by path label and recommends a base with rationale. Do not start judging while candidates are still writing.

## Phase D: Pick a base

Read every candidate end to end before picking. Score each against the rubric criterion by criterion, not on holistic feel, and compare with the cross-judge when Phase C ran one. Agreement on the base confirms the pick. Disagreement means one of you is biased or the rubric was ambiguous. Read both rationales before deciding.

Pick the base a future maintainer can extend most easily without breaking invariants. When two feel tied, prefer the cleaner boundary or smaller API.

## Phase E: Graft

Walk each losing candidate once more for what is worth porting into the base, usually one or two things per candidate, not most of it. Fold each graft in by hand, per the [redesign-from-first-principles](../forge/references/principles/redesign-from-first-principles.md) principle, so the result stays coherent under one mental model. Don't paste mechanically.

If the candidates converge on one shape, that is strong agreement. Note it and ship the consensus shape. No graft is needed. If they wildly diverge, Phase A was under-specified. Reframe and re-run rather than averaging the divergence.

## Phase F: Verify

Verify the synthesized artifact like any other output, per the [prove-it-works](../forge/references/principles/prove-it-works.md) principle. If verification finds a problem the arena missed, either Phase A was wrong (re-frame and re-run) or a candidate caught it and you missed the graft (go back to Phase E). Don't paper over it.

## Outputs

One synthesized artifact, with a short synthesis note alongside naming the base and why, the cross-judge's verdict or that Phase C skipped the judge, each graft with its source candidate, what was rejected and why, any convergence or dropouts, and the verification result.
