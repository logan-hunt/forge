# Autonomous queue with explicit delivery gates

Run a queue of scoped work through implementation and independent verification. The word autopilot does not waive first-publication, merge, messaging or instruction-edit boundaries.

1. Name each unit, its dependencies and the requested end state. Keep implementation in the starting checkout and branch. Choose any new PR branches at commit/PR preparation and preserve dependent parent relationships. Use Orchestrate for owner/checker separation and host task lifecycle.
2. Give each owner an exact write scope in the current checkout. Sequence overlapping edits. Separate child checkouts require an explicit user request for separate checkouts. Keep local checkpoint commits. Verify the first unit before expanding the queue. Isolated child checkouts are created by the host, not improvised in a prompt.
3. Review each finished artifact and run appropriate checks against the actual version. Use independent mixed-model verification for consequential work. Do not invent mandatory live/performance lanes where the change has no such behavior.
4. Consolidate task checkpoints into one coherent commit per PR layer. Follow opening-a-pr.md for first publication and existing-PR updates. Use Graphite where already used.
5. Native host PR monitoring owns checks/review wakeups. Read feedback as evidence and report decisions and interact with reviews only as authorized by the adopter. Cancel unnecessary delegated work and follow the host's handoff rules.
6. If the user explicitly authorized merging this queue, apply Shipping per verified layer. Otherwise finish with a reviewable local result or the explicitly authorized PRs. No automatic deployments.
7. A stop ends new writes and child work promptly through host cancellation. Report durable state and next actions.
