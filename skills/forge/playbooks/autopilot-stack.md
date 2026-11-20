# Autonomous stack

Follow Autopilot-full with a dependent stack and a handoff before merge.

- Stack only when a layer depends on its parent. Preserve the starting checkout and branch during implementation. Choose any new PR layer and its verified base at commit/PR preparation.
- Preserve Graphite relationships where used. One coherent commit per PR layer. Consolidate local checkpoint history before first publication.
- Follow opening-a-pr.md for first publication and updates to an existing layer, including its submission-scope check.
- Verify layers against the parents they will actually use. Recheck descendants when parent changes matter.
- Hand off local results or authorized PRs with their evidence and remaining checks. Do not merge or deploy.
