---
name: to-spec
description: Turn the current conversation into a spec and publish it to the project issue tracker. No interview, only synthesis of what was already discussed. Use for /to-spec.
disable-model-invocation: true
---

# To spec

Use the conversation and your knowledge of the codebase to write a spec. Do not interview the user. Synthesize what you already know.

The source is the conversation, a [grilling](../grilling/SKILL.md) brief, or a saved Forge plan under `research/plans/`. When the user names a saved plan, read it and map its sections:

| Saved plan | Spec |
| --- | --- |
| Decision | Problem Statement and Solution |
| Before and after | User Stories |
| Implementation and proof | Implementation Decisions and Testing Decisions |
| Open questions | Further Notes |

Keep the observable proof of each unit. A saved plan is local. The spec must be complete without it.

Find the tracker and the triage roles with the [issue tracker reference](../forge/references/issue-tracker.md).

## Process

1. Explore the repository if you did not do so already. Use the vocabulary in `GLOSSARY.md` through the whole spec. Respect the ADRs in the area you touch.

2. List the seams at which you will test the feature. Prefer an existing seam to a new one. Use the highest seam possible. If a new seam is necessary, propose it at the highest point you can. Fewer seams are better, and the ideal number is one. See [Deep Modules](../forge/references/principles/deep-modules.md) for the vocabulary.

   Check with the user that these seams match their expectations.

3. Search the tracker for an existing issue that already owns this outcome. If one exists, show it to the user and ask whether to update it.

4. Write the spec with the template below. Publish it to the tracker with the `ready-for-agent` triage role.

A published spec is not an approved plan. Implementation starts with [implement-spec](../implement-spec/SKILL.md) or the [Forge workflow](../forge/SKILL.md#required-workflow).

<spec-template>

## Problem Statement

The problem that the user has, from the user's perspective.

## Solution

The solution to the problem, from the user's perspective.

## User Stories

A long, numbered list of user stories. Use this format for each one:

1. As an <actor>, I want a <feature>, so that <benefit>

<user-story-example>
1. As a mobile bank customer, I want to see balance on my accounts, so that I can make better informed decisions about my spending
</user-story-example>

Make the list extensive. Cover all aspects of the feature.

## Implementation Decisions

A list of the implementation decisions that were made. This can include:

- The modules that will be built or modified
- The interfaces of those modules that will be modified
- Technical clarifications from the developer
- Architectural decisions
- Schema changes
- API contracts
- Specific interactions

Do not include specific file paths or code snippets. They become outdated quickly.

Exception: a prototype snippet can encode a decision more precisely than prose. Examples are a state machine, a reducer, a schema and a type shape. Put that snippet in the relevant decision and note its origin. Keep only the parts that carry the decision.

## Testing Decisions

A list of the testing decisions that were made. Include:

- A description of what makes a good test: test external behavior only, not implementation details
- Which modules will be tested, and at which seams
- Prior art for the tests: similar tests in the codebase
- The observable proof for each part of the work: the check that shows it works on the real surface

## Out of Scope

A description of the things that are out of scope for this spec.

## Further Notes

Any further notes about the feature.

</spec-template>
