---
name: handoff
description: Compact the current conversation into a handoff document so that another agent can continue the work. Use for /handoff.
disable-model-invocation: true
argument-hint: "What will the next session be used for?"
---

# Handoff

Write a handoff document that summarizes the current conversation, so that a fresh agent can continue the work.

If the user passed arguments, they describe what the next session will do. Fit the document to that purpose.

## 1. Collect the state

Record the branch and worktree, the completed work, the checks, the remaining work and the current blockers. When the user is also pausing the work, follow [Pause safely](../forge/playbooks/pause-safely.md). Otherwise leave running work and delegates as they are. Check the working tree and the state of every delegate. Do not rely on memory of the session.

Use [recap-chat](../recap-chat/SKILL.md) to list the decisions that still wait on the user.

A handoff makes no commit, push or publication.

## 2. Write the document

Save the document as `research/handoffs/<task-slug>-<timestamp>.md` in the project. Follow the [research exclusion procedure](../research/SKILL.md#exclude-only-this-repositorys-reports), and confirm that Git ignores the path before you write. Outside a Git repository, or when the user asked for no file in the project, use the OS temp directory. Use `$TMPDIR` if it is set, otherwise `/tmp`.

Include these sections:

- **Goal**: what the user wants, in their words, and what done looks like.
- **Source session**: the link or identifier of this conversation, so that the next agent can read it. In T3, give the thread link.
- **State**: the checkout path, the branch, and whether the changes are uncommitted, committed locally or published.
- **Done and verified**: each completed item with the check that proved it.
- **Remaining**: the next action first, then the rest in order.
- **Decisions**: each decision marked as stated by the user or made by the agent. The agent's decisions stay open to challenge.
- **Waiting on the user**: open questions and approvals. An approval does not carry over unless the user gave it for the same concrete plan.
- **Suggested skills**: the skills the next agent should read, starting with the [Session pickup](../forge/playbooks/session-pickup.md) playbook.

Do not duplicate content that another artifact already holds: specs, saved plans under `research/plans/`, research reports, ADRs, issues, commits and diffs. Reference them by path or URL.

Redact sensitive information, such as API keys, passwords and personal data.

## 3. Report

Give the user the absolute path of the document and a prompt of one line that starts the next session from it. Start a new thread or session only when the user asks for one.
