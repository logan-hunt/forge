# Stack repair and recovery

Use this reference when ancestry needs repair, an operation is interrupted, or the user requests a history change. Keep the repair within the requested scope. Inspect Git status, affected diffs, and Graphite relationships before choosing an operation.

## Register an untracked branch

Determine the actual intended parent from the task, commit graph, and existing stack. Useful evidence includes `git log --graph --oneline --decorate`, `git merge-base <branch> <candidate-parent>`, and `git log <candidate-parent>..<branch>`.

When that parent is already tracked and correct:

```bash
gt track <branch> --parent <verified-parent> --no-interactive
```

Tracking registers ancestry metadata. Do not temporarily invent a `main` parent, create a stack, and reparent it afterward. If the commits are based on the wrong branch, use a deliberate move rather than treating metadata changes as a substitute for rebasing.

## Restack or change the parent

Choose the narrowest scope that preserves the requested stack:

| Intent | Command |
| --- | --- |
| Restack one branch | `gt restack --branch <branch> --only --no-interactive` |
| Restack a branch and its descendants | `gt restack --branch <branch> --upstack --no-interactive` |
| Restack a branch and its ancestors | `gt restack --branch <branch> --downstack --no-interactive` |
| Move a branch to a different parent and restack descendants | `gt move --source <branch> --onto <new-parent> --no-interactive` |

`gt restack` operates on the current stack; it is not inherently a repository-wide operation. `gt sync` has broader effects, including remote synchronization, trunk updates, cleanup, and potentially restacking multiple stacks. Do not substitute it for a narrow repair.

Inspect descendants before moving or amending a branch. Worktree handling and flags such as `gt move --only` vary by version; check installed help before relying on them. Verify the resulting graph and parent-relative diffs after the operation.

## Continue an interrupted operation

Start with `git status` and inspect both unresolved paths and staged resolutions. Missing conflict markers alone do not prove a resolution is correct; check that it preserves the intended changes from both sides.

For a Graphite operation halted by conflicts, stage only the resolved paths and resume through Graphite:

```bash
git add -- <resolved-files>
gt continue --no-interactive
```

Use `gt abort` when deliberately abandoning that Graphite operation, accounting for resolution work that would be lost. For an independently started Git rebase, use Git's own continuation or abort commands. Identify which operation is active before choosing; do not start a second rebase over an interrupted one.

## Raw Git rebase as a fallback

Prefer scoped Graphite operations. If they cannot express an authorized repair, inspect the exact commits to replay and record the original branch tips before using Git directly. A simple `git rebase <target>` can replay unwanted ancestor commits when removing a dependency.

For a deliberate transplant, establish the old boundary and new parent before considering `git rebase --onto <new-parent> <old-boundary> <branch>`. Verify the resulting commit range and diff, then reconcile Graphite tracking with `gt track` if needed and restack only affected descendants. Do not use `gt modify` as metadata synchronization: it may amend a commit.

Skip a commit only after proving its patch is already present or intentionally obsolete. If the boundary or resolution is uncertain, preserve the state and explain the specific ambiguity instead of trying broader rewrites.

## Split, uncommit, or delete requested branches

For a requested split, inspect `gt split --help`. Choose commit, hunk, or file boundaries that produce coherent PRs. In 1.8.3, commit and hunk splitting require interaction; file splitting can run non-interactively. Do not substitute an arbitrary `git reset HEAD^` for an unsupported split mode.

If the user explicitly wants commits returned to unstaged changes, record the original tip and verify the precise boundary and working-tree contents before using a mixed reset. Account for existing staged and unstaged work; never use a hard reset for this purpose.

For requested branch deletion, inspect children and PR state first. `gt delete <branch>` deletes the local branch and Graphite metadata and restacks its children onto the parent. Remote branch deletion and PR closure are separate effects; check installed help for options that add them. Force deletion of unmerged work or deletion of ancestors/descendants must be within the specifically requested scope, not a default cleanup recipe.

## Unexpected changes after stack operations

Do not automatically include newly staged files in the next commit. Inspect `git status --porcelain=v2`, `git diff`, `git diff --cached`, and the relevant reflog. Compare unexpected patches with recent trunk changes to determine whether they are accidental reversals or intended work.

Before discarding a proven accidental patch, preserve the staged and unstaged diffs and relevant file contents in a task-specific backup. Restore only the demonstrated unintended paths or hunks within the authorized repair, preserving unrelated edits. If provenance remains unclear, leave the changes intact and report the evidence.
