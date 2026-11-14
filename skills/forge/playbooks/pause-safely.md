# Pause safely

1. Stop new work and cancel delegated tasks the host says must stop. Preserve task handles and meaningful state for anything explicitly handed off.
2. Record the branch/worktree, completed work, checks, remaining work and current blockers. Check the working tree before touching Git.
3. Local checkpoint commits may preserve this task's work. Stage only its files or hunks; do not sweep unrelated edits into a WIP commit. If the user requested uncommitted output, leave it that way.
4. Pausing alone does not authorize first publication. Finish an already authorized existing-PR update only when safe and within the user's stop instruction; otherwise report what is local.
5. Report the exact resume point and whether changes are committed locally, published or still uncommitted. Do not fabricate completion because work was checkpointed.
