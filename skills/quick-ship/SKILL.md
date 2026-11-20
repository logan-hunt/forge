---
name: quick-ship
description: Publish selected, reviewed changes as a pull request using the repository's Git and issue-tracking conventions. Use when explicitly invoked or called by full-send; implementation and connection checks alone do not authorize publication.
disable-model-invocation: true
metadata:
  invocation: explicit
---

# Quick ship

Take selected changes through validation, a coherent commit and a published PR. Follow [Forge policy](../../docs/policy.md) for plan approval, review, initial publication and existing-PR updates. Explicit quick-ship invocation or a task-scoped [full-send](../full-send/SKILL.md) grant authorizes the selected publication workflow. A request to install or edit this skill does not authorize shipping.

## Resolve scope and services

Inspect the actual checkout, Git remote, branch, working tree, complete index, repository instructions, PR templates and required checks. Include relevant committed changes and existing PRs when the working tree is clean. Preserve unrelated work and staging. Parse the remote's actual host, owner and repository. Verify support before using a github.com-only connector.

Use the repository's naming, issue tracker and ticket conventions. Reuse an existing relevant issue. Create or update a ticket only when the user or repository's workflow calls for it. Resolve its actual team, state and assignee rather than carrying defaults from another organization. Ticket creation is not a prerequisite when no tracker is required. Do not create duplicate issues on retries.

Discover available service tools and verify authenticated reads and repository access. Prefer a sufficient connected service. An authenticated CLI is a fallback. Do not print credentials or create dummy issues/PRs to test permissions. See [connections](references/connections.md) for recovery. Stop only the steps that need a missing connection.

## Prepare the change

Review the complete task diff. Run the required checks and relevant behavior verification, using scoped formatting/lint fixes where appropriate. Preserve unrelated formatting. Report existing failures and unverified behavior separately.

Use [Publication and PR updates](../forge/playbooks/opening-a-pr.md) for review gates, branch selection and stack scope. Stage only the selected changes. Inspect the full index before committing.

When publication needs a new branch, create it from the intended parent at this stage. Use [Graphite](../graphite/SKILL.md) where configured and usable. For ordinary Git, commit or amend the selected change and push to its verified upstream. Inspect remote work before updating a published branch. Use force-with-lease for an authorized rewrite.

## Publish and verify

Check for an existing task PR before creating one. Build its title and description from the final reviewed behavior and the repository's conventions, following [PR descriptions](../forge/references/pr-descriptions.md). Use the repository template or the bundled fallback. Include an actual issue reference when relevant, using a closing reference only when the PR completes that issue. Preserve unrelated prose and stack metadata.

Write multiline bodies to a temporary UTF-8 file or structured tool argument. With gh, use `--body-file`. Never interpolate document content into shell code. Create/update the PR on the verified base. Respect a requested draft state. Otherwise submit ready for review. Reviewer requests, comments, submitted reviews and thread resolution follow the adopter's rules and task authorization. Quick-ship itself grants no merge or deployment authority.

For UI changes, capture relevant screenshots when that verification surface is authorized. Keep evidence outside the repository and use [gh-pr-images](../gh-pr-images/SKILL.md) to attach it to the PR description. Report a blocked capture or upload instead of claiming it happened.

Follow the [active host](../../docs/harness/README.md) for immediate PR linking and monitoring. Retrieve the saved PR to verify URL, title/body, draft state, head and base. Read checks without treating pending checks as passing. Published and ready for review do not mean merged or deployed.

## Recover and hand off

After partial failure, inspect what already exists before retrying. Preserve the returned issue/PR identifiers, successful uploads and published commits. Continue only failed steps. Never delete an issue or branch as automatic cleanup.

Report the repository, issue link when applicable, PR URL, head/base, verification results, checks/review state and material blockers. Report deviations from the approved plan. Keep merge, deployment and production operations within their separate authorization.
