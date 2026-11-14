---
name: git-prune
description: Prune local Graphite branches and git worktrees whose pull requests have
  merged or closed in one or more repos, then sync trunk and restack with gt sync.
  Use when the user asks to prune, clean up, or tidy local branches, stacks, or worktrees
  after PRs merge, or invokes /git-prune. Not for deleting branches with open PRs
  or unpushed work.
disable-model-invocation: true
---

# Git prune

Do what `gt sync` does when the user answers "yes" to every "delete merged/closed branch?" prompt, and also remove the worktrees that block those deletions. Invoking this skill authorizes deleting local branches and worktrees that pass the safety checks below, in the repos the user chose. It does not authorize touching remote branches, closing PRs, or deleting anything that fails a check.

## Choose the repos first

The user must say which repos to prune. Never default to the current directory.

- Use the repository paths or workspace root the user names. Resolve relative paths from the stated workspace, and confirm every target is a Git checkout.
- If the scope is missing, ask for repository paths before scanning or deleting anything. Do not assume a home-directory layout or turn "all" into an unbounded machine-wide search.


## Why worktrees need their own step

Git refuses to delete a branch that is checked out in any worktree, and `gt sync` skips those branches ("cannot be cleaned up while it is checked out in another worktree"). Removing the worktree first frees the branch. `git worktree remove` deletes the worktree directory, including ignored files like `node_modules`, and refuses if the worktree has modified or untracked files. A worktree whose directory was deleted by hand leaves a stale entry that `git worktree prune` clears.

## Run it

The script makes all decisions, so the run is the same every time. Pass one or more repos, each as a main checkout or any of its worktrees:

```bash
python3 <skill-dir>/scripts/prune.py /path/to/repo-a /path/to/repo-b            # preview
python3 <skill-dir>/scripts/prune.py /path/to/repo-a /path/to/repo-b --apply    # make the changes
```

1. Run the preview and read it. If no repo has anything to delete, report that and stop.
2. Run `--apply` with the same repos in the same invocation, without asking again. The user has already chosen to say yes to these deletions.

Start the script from a directory outside the repos' linked worktrees, such as a main checkout. It refuses to remove the worktree it was started from, and removing the harness's current directory would break the session.

## What the script decides

A **branch** is deleted only when all of these hold:
- It isn't trunk.
- Its newest same-repo PR is merged or closed, and no PR for it is open.
- The local tip is already contained in that PR's head. So squash merges qualify, but a branch with commits made after the PR merged is kept.
- It isn't checked out in a worktree that is being kept.
- If the main checkout is on it, that checkout has no uncommitted tracked changes. The script then switches it to trunk with `gt checkout`.

A **linked worktree** is removed only when it is unlocked, clean (no modified or untracked files), and not the directory the script started in. It must also be on a branch being deleted, or detached at a commit already on `origin/<trunk>`.

Graphite-tracked branches are deleted with `gt delete --force --no-interactive`, which also restacks their children onto the parent. Untracked branches fall back to `git branch -D`, because `gt delete` rejects them. The `--force` is safe here only because the script has already verified nothing is lost. Afterwards the script runs `git worktree prune` and `gt sync --no-interactive` to fast-forward trunk and restack what it can.

Everything else is kept and listed with its reason. Never delete a kept item by hand to "finish the job". Report it, and let the user decide.

## Report back

Give a short summary per repo:
- worktrees removed
- branches deleted, with their PR numbers
- whether the main checkout switched to trunk
- what `gt sync` restacked or skipped
- kept items worth the user's attention: dirty worktrees, branches with commits not in their PR, and closed-but-unmerged PRs that were deleted

Don't list every kept branch that simply has no PR unless asked; give a count.

Every deleted branch's tip is printed as `(was <sha>)`. To restore one, run `git branch <name> <sha>` in that repo, or `gh pr checkout <number>` for a branch whose PR still exists.

## When the script stops early

The script stops at the first repo that fails a check, so repos after it don't run. After fixing the problem, rerun the remaining repos.

- `gh auth status` fails: ask the user to run `gh auth login`.
- `gt` is missing, or the repo isn't initialized for Graphite: say so. Don't fall back to deleting branches with raw git.
- `gt sync` reports trunk is behind or diverged: follow the Graphite recovery rule (rerun `gt sync`). Never fix trunk with `git pull`, `git rebase`, or `git checkout`.
