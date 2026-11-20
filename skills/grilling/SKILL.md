---
name: grilling
description: Interview the user relentlessly about a plan, decision or idea until every branch of the design tree is resolved. Use for /grilling, "grill me", "grill this plan", or when the user wants to stress-test their thinking.
---

# Grilling

Interview the user relentlessly until you reach a shared understanding. Map the subject as a **design tree**: each decision branches into the decisions that depend on it.

Use [brainstorm](../brainstorm/SKILL.md) instead when a few questions are enough to settle what a vague request means. Both skills end with the same brief.

## Rounds

Work the tree in rounds. The **frontier** is every decision whose prerequisites are settled. These are the questions you can ask now, with no guess about an answer you did not hear yet.

Ask the whole frontier in one round. Give your recommended answer for each question. Then wait for the user's answers before the next round.

Each round of answers changes the tree. Settled decisions move the frontier outward and unblock the questions that depended on them. Compute the frontier again and ask the next round. A question whose answer depends on another open question in this round belongs to a later round.

### How to ask a round

Use the host's native question tool when the round fits it: at most four questions, each with two to four concrete options. Put the option you recommend first. Say what each option means for users, data and cost. Make each question readable by itself, because the user may see only the question.

When the frontier is larger, or a question needs a free answer, ask the round in chat. Number each question and word it so that "yes" accepts your recommended answer:

```
**Q1. <question title>**
<question body, possibly several paragraphs, with the choices>
Recommended: <your recommended answer>

**Q2. <question title>**
<question body>
Recommended: <your recommended answer>
```

Do not split one frontier across several tool calls to fit the tool. Ask it in chat.

Under an active [full-send](../full-send/SKILL.md) grant, ask only the questions whose answer is consequential. Record your choice for the others as assumed.

## Facts and decisions

You find the facts. Do not ask the user for anything you can look up in the code, the instructions, the tracker or the documentation.

When a frontier question needs a fact, find it before you ask the questions that depend on it. Ask the rest of the frontier now. Delegate the search only under the active [Forge mode](../forge/SKILL.md#lite-standard-and-max) rules.

The user makes the decisions. Put each decision to the user and wait.

## Done

The session is done when the frontier is empty: you visited every branch of the design tree, and nothing is silently assumed.

Then write the brief in the conversation, in the form [brainstorm](../brainstorm/SKILL.md#4-write-the-brief) uses, with no limit on its length:

- **Outcome:** what will be true when this is done.
- **For:** who uses it and when.
- **In scope** and **Out of scope**.
- **Decided:** each decision, in tree order, with the answer the user gave.
- **Still open:** what the plan must settle, and anything you assumed.
- **Proof:** how we will know it worked.

Mark each line as stated by the user or assumed by you. Write no file unless the user asks for one.

Ask the user to confirm that the brief is the shared understanding. Do not act on it before that. Answers to these questions are not approval of a plan. If the user asked only for a grilling, stop at the confirmed brief. Otherwise continue into the [Forge plan step](../forge/SKILL.md#required-workflow) with the brief as its input. [to-spec](../to-spec/SKILL.md) can publish a confirmed brief as a spec.
