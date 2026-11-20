# Separately authorized merge

A request to build, fix, publish a PR, or get checks green does not authorize merging. Use it for an explicit merge/land request covering named PRs or an active [full-send](../../full-send/SKILL.md) grant covering task-related PRs.

1. Read the current PR heads, bases, checks, review requirements and intended merge order. Independent verification must describe the actual code, not an earlier head. Green CI alone is not proof of behavior.
2. For a stack, only the contiguous verified run from its root can land. A verified child above an unverified parent waits. Keep unrelated PRs outside the operation.
3. Use the repository's stack tooling. In Graphite repositories follow graphite for synchronization, restacking and supported merge mechanics. Do not manually rewrite Graphite-managed parent relationships. In ordinary Git repositories use the existing forge workflow.
4. Merge only the explicitly authorized scope after required checks/reviews pass. Never bypass a forge approval gate. If checks or reviews are still pending, use the host's native monitoring under its lifecycle instead of blocking in a polling loop.
5. Read back the resulting state: queued is not merged. Revalidate affected remaining layers after a parent changes. Do not deploy unless separately authorized. Report actual merged state and any remaining blockers.
