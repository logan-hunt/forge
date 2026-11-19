---
name: brainstorm
description: Interview the user about a vague, ambitious or under-specified request before planning. Asks a few questions with the native question tool, then states the agreed outcome, scope and open decisions for Forge's plan step. Use for /brainstorm, "help me think this through", or a request that names a goal but not what done looks like.
---

# Brainstorm

Find out what the user wants before anyone plans how to build it. The result is a short brief in the conversation that [Forge's plan step](../forge/SKILL.md#required-workflow) starts from. A brief is not a plan and approves nothing.

Use it when the request names a goal and leaves open who it is for, what done looks like, or which of several different things is meant. Skip it when the request already states the outcome and scope, or when reading the code would answer the question. Under an active full-send, ask only where the ambiguity is consequential.

## 1. Look before asking

Read what a permitted read can settle: the code, the instructions, the ticket, earlier research and any decision records documented by the project. Never ask the user for a fact you can look up.

## 2. Restate

Say in one or two sentences what you think the goal is and what problem it solves, as [restate-goal](../restate-goal/SKILL.md) does. Name what you assumed.

## 3. Ask

Use the host's native question tool. Ask one round of at most four questions. Ask a second round only when an answer opens a new fork.

A question earns its place when the answer changes what gets built. For each one, offer two to four concrete options, put the one you recommend first, and say what each option means for users, data and cost. Make it readable on its own, because the user may see only the question.

Look for questions here:

- Who uses this, and what do they do today without it?
- What is the smallest version worth having? What is out of scope?
- What must not change?
- The four angles of [refine-prompt](../refine-prompt/SKILL.md): what an expert would do that was not asked for, the rawest material to start from, the methods and tools to use, and what other than you or the user would show the result is right.

Leave the user's choices open. Do not decide for them, and do not ask about how to build it; that belongs to the plan. Stop when another answer would not change the plan.

## 4. Write the brief

Reply with at most 15 lines:

- **Outcome:** what will be true when this is done.
- **For:** who uses it and when.
- **In scope** and **Out of scope**.
- **Decided:** each answer the user gave.
- **Still open:** what the plan must settle, and anything you assumed.
- **Proof:** how we will know it worked.

Mark each line as stated by the user or assumed by you. Write no file unless the user asks for one.

## 5. Hand off

If the user asked only to brainstorm, stop after the brief. Otherwise continue into Forge's plan step with the brief as its input. Plan approval happens there as usual; answering these questions is not approval.
