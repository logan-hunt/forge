---
name: graphite
description: Manage branches and stacked pull requests with the Graphite CLI (gt), including stack inspection, navigation, authorized commits and submission, and ancestry repair. Use for Graphite or stacked-PR work, not ordinary code edits merely because the repository uses Graphite.
---

# Graphite

Use Graphite to preserve branch relationships and make each PR reviewable against its intended parent.

## Scope and authorization

Use this skill in repositories already using Graphite. Follow [Forge policy](../../docs/policy.md#publication-and-existing-prs) for checkout, naming, plan approval, review and publication policy, plus the repository's validation requirements. Invoking this skill supplies Graphite guidance. It does not authorize every operation described here.

Use this route only when Graphite is already configured and usable. If it is unavailable, unauthenticated, or rejects an unsynced repository, fall back to ordinary Git and GitHub within the existing authorization. Keep the branch, intended base, remote work, and force-with-lease protection. Local metadata alone is not a reason to require Graphite setup or another permission request.

## `gt` or raw Git

### Use `gt` for

- Creating branches: `gt create -m "<msg>"` instead of `git checkout -b ... && git commit`.
- Amending the current commit: `gt modify` (with staged changes) instead of `git commit --amend`.
- Adding a follow-up commit on the same branch: `gt modify -c -m "<msg>"` instead of `git commit -m "<msg>"`.
- Pushing / opening or updating a PR: `gt submit --no-interactive --no-verify` instead of `git push` + `gh pr create`.
- Updating local trunk and restacking: `gt sync` instead of `git checkout main && git pull && git rebase`.
- Switching between stacked branches: `gt checkout` / `gt up` / `gt down` instead of `git checkout`.

### Still use raw git for

- Inspection: `git status`, `git log`, `git diff`, `git show`, `git rev-parse`.
- Staging: `git add` (Graphite has no equivalent first-class staging command).
- Soft/mixed resets to reshape staged content before a `gt modify` (e.g. `git reset --soft HEAD~1`).

### Recovery rule

If `gt` reports the trunk is behind upstream, run `gt sync` and retry the failed command. Examples: "Trunk branch (main) is behind its upstream branch", "Please run gt get to update", "Aborting submit due to out of date trunk branch". Never use `git checkout main`, `git pull`, `git fetch` or `git rebase` to fix trunk. It breaks Graphite's branch metadata.

## Inspect the base and stack

Before changing files or branch state, inspect the relevant repository:

```bash
git status --short --branch
git diff --stat
git diff --cached --stat
gt log short
gt info
```

Read the actual diffs when needed to distinguish task changes from unrelated work. Check `git worktree list` when another checkout could constrain navigation or rewriting.

- For an existing task or stack, stay on its task branch and preserve the intended parent. A feature-branch parent may be correct. Do not flatten a stack onto trunk automatically.
- If Graphite reports an untracked branch, or ancestry is unclear, read [Stack repair and recovery](references/stack-recovery.md) before changing metadata.

Prefer small PRs with one coherent purpose. Each layer should validate with its ancestors. Dependent layers do not need to work without their parents. Split at meaningful review boundaries, without maximizing the number of PRs as an end in itself.

## Navigate and inspect

| Intent | Command |
| --- | --- |
| Show stack relationships | `gt log short` |
| Inspect a branch and its parent diff | `gt info <branch>` / `gt info <branch> --diff` |
| Move to a child / parent | `gt up` / `gt down` |
| Move to the stack tip / first branch above trunk | `gt top` / `gt bottom` |
| Select a known branch | `gt checkout <branch>` |

Use explicit branch names when there are multiple children. Check the working tree before navigation.

## Create or update an authorized commit

Run the checks appropriate to the change using the repository's instructions. Before committing, inspect the entire index so unrelated staged work is not swept into the commit. Stage only the authorized files or hunks. Avoid broad `git add .` or `--all` shortcuts in a shared working tree.

At commit/PR preparation, use the verified current base for an authorized new branch:

```bash
git add -- <selected-files>
git diff --cached
gt create <branch-name> -m "Commit message" --no-interactive
```

For an existing task branch, reuse it. When an amendment is authorized:

```bash
git add -- <selected-files>
git diff --cached
gt modify --no-interactive
```

`gt modify` amends by default and automatically restacks descendants. Use `-m "Updated message"` to replace the message, or `--commit -m "New message"` when a new commit is intended. Do not use `gt modify` merely to refresh Graphite metadata.

Inspect the resulting stack and parent-relative diff. Revalidate affected descendants when changed parent behavior or conflict resolutions warrant it. For interrupted operations, reparenting, splitting, deletion, or unexpected diffs, read [Stack repair and recovery](references/stack-recovery.md).

## Submit the authorized scope

In T3, follow the [host PR lifecycle](../../docs/harness/t3.md#pr-lifecycle) during submission.

Verify the intended ancestry and submission scope with a dry run before pushing:

```bash
gt submit --dry-run --no-interactive
```

Inspect the intended remote base and commit range. A child push can expose unpublished ancestor commits even without creating another PR. Keep the fix local and request first-publication authorization if an ancestor would be exposed. Do not reparent to evade that boundary. For an existing-PR update, use `--update-only` and inspect the dry run so no unpublished layer is created. Default submission includes the current branch and its ancestors. `--stack` also includes descendants. `--update-only` limits submission to branches with existing PRs. It does not mean "only this branch." Use `--branch <branch>` to select the starting branch without checking it out. Where supported, `--no-stack` explicitly excludes descendants, but still includes ancestors.

Use the same scope flags for the dry run and actual submission. If the preview would change branches or PRs outside the authorized task, narrow the operation. If that cannot preserve the intended stack, explain the concrete affected branches before asking for expanded scope.

```bash
gt submit --no-interactive
```

Add `--draft` or `--publish` only to match the requested review state. Preserve Graphite's default force-with-lease protection. Use `gt submit --no-verify` after completing the required validation, including existing-PR updates. This skips Git hooks, not the checks themselves. Never use `--force` or `--ignore-out-of-sync-trunk` to bypass a failure. Resolve the cause and repeat the preview. If the preview would overwrite remote commits, such as layers Graphite's merge rebased onto trunk, save local-only fixes as a patch. Then take the remote versions with `gt get <branch> --force --no-restack --no-interactive`, reapply the patch and confirm each layer with `git range-diff`. Stop if recovery would still overwrite remote work or require an unrelated history rewrite.

After submission, verify the resulting PRs' head, base, title, body and review state. Report links and validation results, including any checks still pending.

## PR titles and descriptions

Follow [PR descriptions](../forge/references/pr-descriptions.md) and the repository template. Lead with the concrete problem and resulting behavior, then explain validation. Add brief stack context when it helps a reviewer understand this layer's role or dependency. Keep small changes concise rather than requiring fixed headings.

For authorized metadata edits, prefer structured tool arguments. With `gh`, write exact Markdown to a task-specific temporary file using a file-writing tool or safely quoted script, then use `--body-file`:

```bash
gh pr edit <number> --title "Clear title" --body-file <body-file>
```

Preserve unrelated description content and stack-navigation metadata. Avoid shell interpolation of Markdown or commands embedded in the body.

## Command compatibility

The examples were checked against local `gt` 1.8.3. Verify version-sensitive flags with `gt <command> --help`. Newer Graphite documentation may include flags unavailable locally. Consult the [official command reference](https://graphite.com/docs/command-reference) for current semantics.

## One commit per PR layer

Inspect `gt squash --help` for the installed version before consolidating checkpoint commits. Squash only the selected task branch's commits above its verified parent, never a whole stack or another contributor's work. Amend an existing single-commit PR with `gt modify` and inspect restacked descendants. Use the same bounded scope for the submit dry run and actual update. If the installed commands cannot express that scope, stop the dependent publication and report the exact affected branches.
