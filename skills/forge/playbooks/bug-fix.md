### Bug fix

**You own this task. Plan, review, verify.** Coordinate investigation and implementation. Delegate independent work when useful under the current mode. Use the configured model role and supported host options, following Forge’s Delegation and models section.

Be scientific. Every shipped line traces to runtime evidence. Belt-and-suspenders that "might help" is a hypothesis, not a fix. It does not ship. When evidence refutes a hypothesis, revert what it motivated. The smallest change the evidence justifies ships, nothing more.

1. Identify the action that triggers the failure from the report or available evidence. If the trigger is still unknown, ask “Which user action makes it fail?” Even when a debug or instrumentation protocol says to ask the user to reproduce, reproduce the failure yourself. Use the matching surface via an available surface driver under the active host policy. Ask the user only after you drive the control surface as far as it goes. State the specific reason it cannot reach the target. If it won't reproduce directly, synthesize the trigger, tighten conditions, or instrument until it fires.
2. Binary-search the cause. Form the candidate hypotheses, then rule them out until one survives. Seed them with `how` over the affected subsystem and the [why](../../why/SKILL.md) skill for regression history. Each pass, take the split that cuts the most remaining problem space, get runtime evidence, eliminate. When program state is unclear, add instrumentation or logging and read it as the code runs. Don't guess. Drive a long or stubborn hunt with the host’s supported task lifecycle. Confirm the surviving *mechanism* with runtime evidence before the step-3 architect/adversarial-review fan-out.
3. Plan the fix. In Max, or when the fix changes ownership or contracts, use `architect` first. When the mode and task warrant it, use a scoped implementation delegate with a specific scope. Use your configured bug-fix model (role resolved through forge-setup, inherited when unconfigured).
4. Verify on the same surface. The original repro now passes. "Inconclusive" or wrong-surface is not a pass. Flag it. Unit tests show branch behavior, not bug absence.
5. Keep failing-before evidence and the passing fix together in the final PR-layer commit. Local checkpoints may record their sequence. See the [tdd](../../tdd/SKILL.md) skill for the failing-test-first cadence when the bug has a cheap local test path. Skip it when the test would be expensive, integration-heavy, or unclear.
   This is the canonical [sequence-verifiable-units](../references/principles/sequence-verifiable-units.md) principle, the failing test first and the fix on top.
6. Apply **Publication and PR updates** (`opening-a-pr.md`).

**Reply:** what was broken, root cause, fix, how you verified. Paste failing-then-passing repro output verbatim.
