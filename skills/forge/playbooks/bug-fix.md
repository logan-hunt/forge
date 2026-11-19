### Bug fix

**You own this task. Plan, review, verify.** Coordinate investigation and implementation; delegate independent work when useful under the current mode. Use the configured model role and supported host options, following Forge’s Delegation and models section.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Identify the action that triggers the failure from the report or available evidence. If the trigger is still unknown, ask “Which user action makes it fail?” Reproduce the failure yourself on the matching surface via an available surface driver under the active host policy, even when a debug or instrumentation protocol says to ask the user to reproduce. Ask the user only with a stated, specific reason the control surface cannot reach the target, and only after driving it as far as it goes. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with `how` over the affected subsystem and the [why](../../why/SKILL.md) skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with the host’s supported task lifecycle. Confirm the surviving *mechanism* with runtime evidence before the step-3 architect/interrogate fan-out.
3. Plan the fix. In Max, or when the fix changes ownership or contracts, use `architect` first. Use a scoped implementation delegate when the mode and task warrant it using your configured bug-fix model (role resolved through forge-setup; inherit when unconfigured) with a specific scope.
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Keep failing-before evidence and the passing fix together in the final PR-layer commit; local checkpoints may record their sequence. See the [tdd](../../tdd/SKILL.md) skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical [sequence-verifiable-units](../references/principles/sequence-verifiable-units.md) principle, the failing test first and the fix on top.
6. Apply **Publication and PR updates** (`opening-a-pr.md`).

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
