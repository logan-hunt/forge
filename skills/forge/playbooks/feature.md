# Feature

Own the design, scope and proof. Coordinate the supporting skills rather than treating this as a checklist that must always expand.

1. Ground the affected subsystem with how. Lite and Standard can use a focused read when the shape is familiar. Max normally uses broader grounding and architect for cross-boundary design; adapt methods to the selected mode.
2. Name the data shape, owning module and observable behavior. Use architect when ownership, contracts or the design space require it. Competing designs use arena; contested decisions can use interrogate.
3. State the throughput checkpoint: blocking prerequisites, independent workstreams, shared mutable state and smallest safe decomposition. A single owner is valid. Isolate overlapping writes; preserve dependencies.
4. Implement directly or delegate the scoped slice using the `feature` role under Forge's host/model rules. Max favors separate implementation and review. A child without delegation authorization owns its diff directly. Choose meaningful names, cohesive structure and the smallest complete change; keep validation, accessibility and error handling.
5. Build a lever when repeatability or proof earns it; reuse an existing command or harness when it already does the job. Verify the real affected behavior and relevant failure states. An unavailable surface is a gap, not a pass; try permitted alternative routes.
6. Keep local checkpoints and review the complete diff. Use the [publication playbook](opening-a-pr.md) for authorized delivery.
7. Report the behavior, important design choice, verification and remaining concerns. Explain a deeper method when it affected the result, not as a ritual list of principles.
