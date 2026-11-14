# Autonomous run

Own the exit condition and drive the authorized task to it.

1. State a checkable predicate before starting: the original repro passes, all named migration callers move, or the agreed performance target holds. A merge predicate requires explicit merge authorization.
2. Use the host's task lifecycle and event notifications for delegated or externally waiting work. T3 tasks follow their returned next instructions; PRs use native monitoring. Do not invent a polling loop to imitate another harness.
3. Each iteration makes the smallest evidence-supported change, verifies it, and checkpoints useful progress locally. Revert only your unsuccessful experiment, never unrelated work. Initial publication and existing-PR updates follow opening-a-pr.md.
4. Fix supporting issues within the authorized scope. Record unrelated bugs and broken skills as proposals; do not create extra PRs, backlog tickets or durable instruction edits on your own. Team-chat reads and sends remain explicit-request-only.
5. Maintain a useful decision trail. State new evidence, action and result, not every tool call.
6. Stop when the predicate is met or a concrete blocker prevents progress. Try a materially different hypothesis before repeating a failure. Do not relax the predicate or consume unbounded time on equivalent attempts.
