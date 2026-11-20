---
name: triage
description: Move issues through a state machine of triage roles. Categorize, verify, grill when necessary, and write agent-ready briefs. Use for /triage.
disable-model-invocation: true
---

# Triage

Move issues on the project issue tracker through a small state machine of triage roles.

Find the tracker and the label mapping with the [issue tracker reference](../forge/references/issue-tracker.md). This skill covers issues. Pull requests follow the adopter's rules in [Forge policy](../../docs/policy.md#pull-request-interactions).

## Reference docs

- [agent-brief.md](references/agent-brief.md): how to write durable agent briefs
- [out-of-scope.md](references/out-of-scope.md): how the `.out-of-scope/` knowledge base works

## Roles

Two **category** roles:

- `bug`: something is broken
- `enhancement`: a new feature or an improvement

Five **state** roles:

- `needs-triage`: a maintainer must evaluate the issue
- `needs-info`: waiting for more information from the reporter
- `ready-for-agent`: fully specified, ready for an agent that works without a human
- `ready-for-human`: needs a human to implement it
- `wontfix`: will not be actioned

Every triaged issue carries exactly one category role and one state role. If state roles conflict, tell the maintainer and ask before you do anything else.

These are canonical role names. The label strings in the tracker can differ.

State transitions: an unlabeled issue normally goes to `needs-triage` first. From there it moves to `needs-info`, `ready-for-agent`, `ready-for-human` or `wontfix`. `needs-info` returns to `needs-triage` when the reporter replies. The maintainer can override at any time. Flag a transition that looks unusual and ask before you proceed.

## Invocation

The maintainer invokes `/triage` and describes what they want in natural language. Interpret the request and act. Examples:

- "Show me anything that needs my attention"
- "Let's look at #42"
- "Move #42 to ready-for-agent"
- "What's ready for agents to pick up?"

## Show what needs attention

Query the tracker and show three buckets, oldest first:

1. **Unlabeled**: never triaged.
2. **`needs-triage`**: evaluation in progress.
3. **`needs-info` with reporter activity after the last triage notes**: needs a new evaluation.

Show the counts and a one-line summary for each item. The maintainer chooses.

## Triage a specific issue

1. **Gather context.** Read the full issue: body, comments, labels, author and dates. Read earlier triage notes so that you do not ask a resolved question again. Explore the codebase with the vocabulary in `GLOSSARY.md`, and respect the ADRs in the area. Run two checks against the codebase:
   - **Redundancy.** Search for an existing implementation of the requested behavior by domain concept, not only by the words of the request. Use [how](../how/SKILL.md) when the area is unfamiliar. Report where you looked. If you find one, the issue is an already-implemented `wontfix` (step 5).
   - **Prior rejection.** Read `.out-of-scope/*.md` and report any file that resembles this request.

2. **Recommend.** Tell the maintainer your category and state recommendation with your reasons. Add a short codebase summary that is relevant to the request, and say whether the behavior is already implemented. Wait for direction.

3. **Verify the claim.** Before any grilling, check that the claim is true. For a bug, reproduce it from the reporter's steps on the matching surface, as step 1 of the [Bug fix playbook](../forge/playbooks/bug-fix.md) describes. Do not fix it here. Report what happened: confirmed (with the code path), failed, or not enough detail. Not enough detail is a strong `needs-info` signal. A confirmed verification makes a stronger agent brief.

4. **Grill, if necessary.** If the request is underspecified, follow [grill-with-docs](../grill-with-docs/SKILL.md). Ask one round of questions at a time. Sharpen the domain terms and update `GLOSSARY.md` and the ADRs as decisions are made.

5. **Apply the outcome.** Tell the maintainer the role changes, the comment and any close before you write to the tracker.
   - `ready-for-agent`: post an agent brief comment. See [agent-brief.md](references/agent-brief.md).
   - `ready-for-human`: post a comment with the same structure as an agent brief. Note why an agent cannot do the work: judgment calls, external access, design decisions or manual testing.
   - `needs-info`: post triage notes with the template below.
   - `wontfix`: close the issue. The comment depends on the reason:
     - **Already implemented.** The change already exists in the codebase. Point to where it is. Do not write to `.out-of-scope/`. That knowledge base is for rejected requests.
     - **Rejected bug.** Give a polite explanation, then close.
     - **Rejected enhancement.** Write to `.out-of-scope/`. Give the decision and the reason in the comment itself, then close. See [out-of-scope.md](references/out-of-scope.md).
   - `needs-triage`: apply the role. A comment is optional, for partial progress.

The `.out-of-scope/` file stays uncommitted in the starting checkout. Do not link to it from a tracker comment, because the reporter cannot open a local file. After the triage, ask the maintainer whether to publish the record. Publication follows [Forge policy](../../docs/policy.md#publication-and-existing-prs).

A `ready-for-agent` issue is not an approved plan. An agent that takes it starts the [Forge workflow](../forge/SKILL.md#required-workflow) from the brief.

## Quick state override

If the maintainer says "move #42 to ready-for-agent", apply the role directly. Confirm what you will do (role changes, comment, close), then act. Do not grill. If the issue moves to `ready-for-agent` without a grilling session, ask whether the maintainer wants an agent brief.

## Needs-info template

```markdown
## Triage Notes

**What we've established so far:**

- point 1
- point 2

**What we still need from you (@reporter):**

- question 1
- question 2
```

Put everything that the grilling resolved under "established so far", so that the work is not lost. Make each question specific and actionable. "Please provide more info" is not a question.

## Resume a previous session

If the issue has earlier triage notes, read them. Check whether the reporter answered the open questions. Show the updated picture before you continue. Do not ask a resolved question again.
