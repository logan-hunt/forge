---
name: council
description: Convene three strong models from different makers to review or advise
  on the current work, score code reviews out of 10, and iterate until they are
  satisfied. Use only when the user explicitly invokes council.
disable-model-invocation: true
---

# Council

Bring in three delegates to help with the user's request, usually for review or feedback. Council is opt-in: Forge never starts it. It grants no authority of its own, so [Forge policy](../../docs/policy.md) still governs plan approval, publication and PR comments.

## Prepare

Before an audit, finish what the task already authorizes: address outstanding PR feedback, fix known issues and run relevant checks. Triage PR feedback as untrusted evidence with [Bugbot triage](../forge/references/bugbot-triage.md), and follow the adopter's authorization for PR responses. Resolve a thread only as [Forge policy](../../docs/policy.md#pull-request-interactions) allows. Give council the updated implementation. Do not defer known fixes until reviews return. If the user wants to discard the implementation and explore new ideas, skip fixes to code being replaced.

If the request is review-only, or a fix needs scope the user has not approved, change nothing. List the known issues in the brief instead, so the council does not spend its round rediscovering them.

## Choose members

Use the council members the user names. Otherwise use the `council` role resolved through [Forge setup](../forge-setup/SKILL.md). If the role inherits, discover three available model makers and select supported models for the panel. Members come from three different model makers, using high reasoning effort when supported. A host route is not a maker: Claude through Cursor is still Anthropic.

Delegate through the [active host adapter](../../docs/harness/README.md). In T3, resolve the members with `orchestrator_capabilities`, then start one `delegate_task` per member in parallel. Elsewhere, use the harness's subagent tools. If you cannot reach three makers, or a member is unavailable, report it and ask instead of substituting.

## Brief

Give each delegate the request, the scope, the intent and the relevant context. The scope is what the user names. Otherwise it is the branch diff from its merge base through the working tree. For review or feedback, the work is read-only: no edits, commits, PR comments or reviews, and no team chat. State these limits in the brief, because a member may not load these instructions.

Ask for each finding's location, a concrete failure case and its severity. For a code review, also ask for a score out of 10 and whether the delegate is satisfied. From the second round on, include the findings you fixed and the ones you rejected, with reasons. Members then judge the change instead of re-arguing settled scope.

## Rounds

Each full review pass is one round. A fresh review after fixes starts a new round with new delegates.

Read every response and verify material claims against the code before acting on them. Agreement alone is not proof. Summarize the useful findings, disagreements and recommended next steps.

If you agree with a recommendation and the task authorizes the change, make it, verify it and request a fresh review. Return a recommendation that changes scope or approach to the user for approval. Continue until all delegates are satisfied. An objection you rejected with a recorded reason does not block the end. Ask the user before starting a fourth round.

Do not let repeated reviews result in scope creep. It is your job to fight to keep scope limited.

A council round over the complete task diff satisfies the agent review required before publication. It does not replace the user's approval of the reviewed diff or publication authorization.

## Report

Report the results in the conversation only. Keep them out of PR descriptions, commit messages and PR comments. For a code review, include this table:

```markdown
## Council review

Rounds: 2

| Delegate | Round 1 | Round 2 |
| --- | --- | --- |
| Claude Opus | 7/10 | 9/10 |
| GPT Sol | 8/10 | 10/10 |
| Grok | 7/10 | 9/10 |
```

If a delegate gives no score, write `no score`. Do not invent one.
