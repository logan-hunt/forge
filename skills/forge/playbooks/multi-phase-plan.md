# Multi-phase or multi-PR plan

The requested plan is the deliverable. Do not implement or create prototypes during a plan-only request unless that work is separately authorized.

1. Use the [Forge plan step](../SKILL.md#required-workflow) to present the decision. Ground the current state, affected contracts and existing patterns. Use how/why and scoped parallel source reading when useful. Name uncertain facts and distinguish them from product decisions.
2. Define meaningful units with one owner and proof each. Show why each dependency sets the order and how each intermediate state stays safe. Propose a stack only where layers depend on each other. Avoid manufacturing PR layers for incidental steps.
3. For each unit list outcome, paths, dependencies, allowed writes, implementation approach, tests and observable verification. Add performance checks only when performance is affected. Failure states should reflect real risk rather than a fixed lane count.
4. Explain why the proposed PR boundaries help review or keep rollout safe. State the next action covered by approval under [Forge policy](../../../docs/policy.md#publication-and-existing-prs).
5. State the execution playbook (Feature, Orchestrate, Autonomous run or Autopilot-stack), chosen mode and any requested review checkpoints. Mode can change as evidence develops.
6. List alternatives and unresolved decisions with the evidence that would settle them. Do not demand a human answer to a fact a permitted read can establish.
7. When the user wants tickets, verify the destination project and check for an existing issue that owns each outcome. Include the observed behavior, acceptance evidence and blocking dependencies from the plan. For plan-only requests, return the proposed mapping in the plan.
