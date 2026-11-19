# Worktree cleanup

Use the repository’s configured Git or Graphite workflow for requested cleanup. Follow any cleanup procedure supplied by the adopter.

Inventory worktrees from git worktree list, branches, PR state and dirty/untracked work. Verify a checkout is neither in use by the user nor owned by an active task. A clean or old directory alone does not prove it is disposable. An untracked file is not automatically throwaway.

Remove only the requested, confirmed disposable worktrees. Do not force-remove dirty work or delete caches, simulators or other application state as an incidental cleanup. Preserve unpublished commits and branches. Report removed paths and the reason each retained candidate remains.
