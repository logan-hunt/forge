# Issue tracker

The tracker skills ([to-spec](../../to-spec/SKILL.md), [to-tickets](../../to-tickets/SKILL.md), [implement-spec](../../implement-spec/SKILL.md), [wayfinder](../../wayfinder/SKILL.md) and [triage](../../triage/SKILL.md)) read and write the project's issue tracker. This reference tells them which tracker to use and how each operation works there.

A write to a tracker is an external action under [Forge policy](../../../docs/policy.md#external-actions-and-durable-changes). An explicit invocation of a tracker skill authorizes the writes that skill describes, for that task, on the confirmed tracker.

## Find the tracker

Use the first source that answers:

1. The repository's instructions (`AGENTS.md`, `CLAUDE.md`) or `docs/agents/issue-tracker.md`, when one names the tracker.
2. Evidence in the project: ticket identifiers in branch names and commits, a connected tracker tool, the Git remote.
3. The local Markdown tracker, when the project has a `.scratch/` folder or no remote.

Before the first write in a session, tell the user the tracker and the team, project or repository you will write to. Wait for the user to confirm it. Ask which tracker to use when the evidence points to more than one.

Do not write to a repository or workspace that the user does not own or work in. In a fork, `gh` can default to the upstream parent. Check the target with `gh repo view --json nameWithOwner` before the first `gh issue create`.

## Choose the tool

Prefer a connected tracker tool or the host's issue tools when one can do the operation. An authenticated CLI is the fallback. Discover the current tool names and parameters before the first call. The sections below give each operation and, for GitHub, its CLI form.

Follow the [active host adapter](../../../docs/harness/README.md) to link an issue to the session. In T3, link every issue you file or work on.

## Triage roles

The skills use five canonical state roles and two category roles. The label or status names in the tracker can differ.

| Role | Meaning |
| --- | --- |
| `needs-triage` | A maintainer must evaluate the issue |
| `needs-info` | Waiting for more information from the reporter |
| `ready-for-agent` | Fully specified, ready for an agent that works without a human |
| `ready-for-human` | Needs a human to implement it |
| `wontfix` | Will not be actioned |
| `bug` | Category: something is broken |
| `enhancement` | Category: a new feature or an improvement |

Use the mapping in the repository's instructions or `docs/agents/triage-labels.md` when one exists. Otherwise use a tracker label with the same name as the role. Before you create a label that the tracker lacks, list the labels you will create and wait for the user to confirm them.

## GitHub

The `gh` CLI form of each operation follows. `gh` infers the repository from the Git remote.

- **Create an issue:** `gh issue create --title "..." --body "..."`. Use a heredoc for a body with more than one line.
- **Read an issue:** `gh issue view <number> --json number,title,body,labels,comments`.
- **List issues:** `gh issue list --state open --json number,title,body,labels,comments` with `--label` and `--state` filters.
- **Make a sub-issue:** `gh issue create --parent <parent> ...`, or `gh issue edit <parent> --add-sub-issue <child>` (`gh` 2.94 or later). Without sub-issues, put `Part of #<parent>` at the top of the child body.
- **Blocking:** use GitHub's native issue dependencies. Add an edge with `gh issue create --blocked-by <n>,<n> ...` or `gh issue edit <child> --add-blocked-by <blocker>` (`gh` 2.94 or later). Where dependencies are not available, put a `Blocked by: #<n>, #<n>` line at the top of the child body. A ticket is unblocked when every blocker is closed.
- **Count open blockers:** `gh issue view <n> --json blockedBy --jq '[.blockedBy.nodes[] | select(.state == "OPEN")] | length'`. Zero means the ticket can start.
- **Comment:** `gh issue comment <number> --body "..."`.
- **Labels:** `gh issue edit <number> --add-label "..."` or `--remove-label "..."`.
- **Close:** post the explanation with `gh issue comment`, then run `gh issue close <number>`.

GitHub shares one number space across issues and pull requests. Resolve a bare `#42` with `gh issue view 42`. Pull-request comments, reviews and thread resolution follow the adopter's rules in [Forge policy](../../../docs/policy.md#pull-request-interactions).

## Linear

Use the connected Linear tools. Discover their current names and parameters before the first call.

- **Create an issue:** save an issue with a team, a title and a Markdown description. Search for a matching issue first.
- **Read an issue:** get the issue by its identifier, then list its comments. The issue body does not include the discussion.
- **List issues:** filter by team, project, label, state, assignee or parent.
- **Make a sub-issue:** set the parent on the child issue.
- **Blocking:** use Linear's native blocked-by relation on the child issue. A ticket is unblocked when every blocker is completed or canceled.
- **Comment:** save a comment on the issue.
- **Labels:** add or remove single labels. Do not replace the full label set.
- **Close:** post the explanation as a comment, then set the state to the team's completed or canceled state.

Triage roles map to labels. Where the team already uses a Linear status for a role (for example Triage for `needs-triage`), use that status.

## Local Markdown

Issues and specs are Markdown files under `.scratch/` in the project.

- One feature per directory: `.scratch/<feature-slug>/`.
- The spec is `.scratch/<feature-slug>/spec.md`.
- Each ticket is one file: `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`. Never combine tickets in one file.
- A `Status:` line near the top of each ticket file records the state. For a triaged ticket, the state is the triage role. A closed ticket has `Status: resolved`.
- A `Blocked by: NN, NN` line near the top records the blocking edges. A ticket is unblocked when every file it lists has `Status: resolved`. Close a ticket as soon as its acceptance criteria pass, so that the tickets it blocks can start.
- Comments go at the bottom of the file under a `## Comments` heading.
- **Close:** add the explanation under `## Comments`, then set `Status: resolved`.

To publish, create the file. To fetch a ticket, read the file at the path or number the user gave. The files are ordinary untracked files. Commit them only when the user asks.

## Wayfinding operations

[Wayfinder](../../wayfinder/SKILL.md) keeps a map and one child ticket for each decision.

| Operation | GitHub | Linear | Local Markdown |
| --- | --- | --- | --- |
| Map | One issue with the label `wayfinder:map` | One issue with the label `wayfinder:map` | `.scratch/<effort>/map.md` |
| Child ticket | A sub-issue of the map, with a `wayfinder:<type>` label | A sub-issue of the map, with a `wayfinder:<type>` label | `.scratch/<effort>/issues/NN-<slug>.md` with a `Type:` line and `Status: open` |
| Blocking | Native dependencies | Native blocked-by relation | A `Blocked by: NN, NN` line |
| Frontier | Open children with no open blocker and no assignee, in map order | Open children with no open blocker and no assignee, in map order | Files with `Status: open` and no unresolved blocker, lowest number first |
| Claim | `gh issue edit <n> --add-assignee @me` | Assign the issue to the user | Set `Status: claimed` and save |
| Resolve | Comment with the answer, then close | Comment with the answer, then set the completed state | Add the answer under `## Answer`, set `Status: resolved` |
| Rule out of scope | Comment with the reason, then close | Comment with the reason, then set the canceled state | Add the reason under `## Comments`, set `Status: resolved` |

After each resolution, add a context pointer to the map's **Decisions so far** section. It is the ticket title as a link and a one-line summary of the answer.

The `<type>` is one of `research`, `prototype`, `grilling` or `task`.
