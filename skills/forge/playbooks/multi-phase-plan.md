# Multi-phase or multi-PR plan

The requested plan is the deliverable. Do not implement or create prototypes during a plan-only request unless that work is separately authorized.

1. Ground the current state, affected contracts and existing patterns. Use how/why and scoped parallel source reading when useful. Name uncertain facts and distinguish them from product decisions.
2. Define meaningful units with one owner and proof each. Separate independent work from dependencies; propose a stack only where layers depend on each other. Avoid manufacturing PR layers for incidental steps.
3. For each unit list outcome, paths, dependencies, allowed writes, implementation approach, tests and observable verification. Add performance checks only when performance is affected. Failure states should reflect real risk rather than a fixed lane count.
4. State delivery gates: local checkpoints, one coherent commit per intended PR layer, explicit first publication, existing-PR update behavior, and separate merge authorization. Use Graphite only in repositories that already use it.
5. State the execution playbook (Feature, Orchestrate, Autonomous run or Autopilot-stack), chosen mode and any requested review checkpoints. Mode can change as evidence develops.
6. List alternatives and unresolved decisions with the evidence that would settle them. Do not demand a human answer to a fact a permitted read can establish.
7. Return the plan in the requested surface. Save a file only if requested or authorized by the artifact workflow. Stop before execution on a plan-only request.

Suggested shape: Goal; Current evidence; Units and dependencies; Verification; Publication/merge gates; Open decisions. Adapt the shape to the task instead of filling irrelevant template sections.
