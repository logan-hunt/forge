# Orchestrate

Own the program's scope, dependencies and evidence. Use this for an explicitly delegated multi-part program; a single sustained task belongs to Autonomous run.

## Partition

- One owner per writable artifact or task branch. Independent file groups can share the parent worktree; sequence overlapping changes. Use host-managed isolated child checkouts only when the user explicitly requests separate checkouts; keep the parent in its starting checkout.
- Start with a representative unit before scaling the queue. Validate the brief and proof before reproducing a flawed setup across many agents.
- Each brief contains the user's goal, current decisions, source paths, allowed writes, dependencies, mode, publication boundaries, checks and expected report.
- A deeper mode is not a requirement to maximize fan-out. Stay within actual concurrency and budget. Do not spawn nested coordinators unless the assignment requires them and explicitly permits delegation.

## Supervise

- Follow the current host's delegation contracts and completion notifications. Read ../../../docs/harness/t3.md when using T3. Never poll a delegate whose contract says completion wakes the parent.
- Read the artifact and evidence, not just the summary. A verification result belongs to the version tested. New behavior, changed dependencies or conflict resolutions may invalidate it.
- Use a fresh independent review task where needed. Different-family review uses the configured, available provider; report unavailable diversity rather than silently substituting.
- Cancel replaced or unnecessary workers through the host task handle. Every child ends completed, cancelled or explicitly handed off under the host's rules.
- Fix small review findings yourself when that is faster and preserves ownership. Re-scope repeated failures instead of spawning equivalent retries.

## Deliver

Keep local checkpoints, one coherent commit per intended PR layer, and meaningful dependency order. Follow opening-a-pr.md for first publication and existing-PR updates. PR interactions require the adopter's authorization. Do not read team chat autonomously or merge/deploy without authorization. When the user separately authorizes merges, use Shipping. Ongoing PR monitoring belongs to the host.

Report completed scope, verification, changed paths or PR links, pending decisions and concrete blockers. Keep the decision trail useful for resumption.
