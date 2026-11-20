---
name: to-questionnaire
description: Turn a decision the user cannot answer alone into a Markdown questionnaire for the one person who can. Use for /to-questionnaire.
disable-model-invocation: true
---

# To questionnaire

Turn something the user cannot answer alone into a **questionnaire**: a Markdown document that they give to one person. That person fills it in alone, or the two fill it in together in a meeting. The recipient has knowledge that the user lacks. The questionnaire gets it from them.

**Grill the send, not the subject.** Interview the user only about the send, which they can always answer: who receives it, and what the user needs back. The questions in the document then target the **gap** between what the recipient knows and what the user needs.

1. **Who receives it?** Ask, in one exchange, for the recipient's role, expertise and relationship to the user. This fixes the tone and how much context the document must carry. Done when you know who the recipient is and what they know that the user does not.

2. **What do you need back?** Ask, in one exchange, for the specific decisions or facts that the user cannot resolve alone. Done when you have a concrete list of what the user must be able to do or decide afterward.

3. **Write the questionnaire.** Draft questions aimed at the gap from steps 1 and 2. Follow the document structure below. Write it to `to-questionnaire-<slug>.md`, with a slug from the topic, and report the path. Use the current directory. If the current directory is inside a Git repository, use the OS temp directory unless the user names a path. Done when the file exists and a question covers every item from step 2.

Do not send the questionnaire. The user sends it.

## Document structure

Frame the document as a **discovery questionnaire**: the user lacks context, and the recipient has it. Put the most important questions first, because the recipient may answer only once. When the document has more than a few questions, group them by theme under `##` headings. Use the template below.

<questionnaire-template>

# <Questionnaire title>

**Purpose:** why this questionnaire exists and the decision that depends on it.

**From:** <the user>, **To:** <the recipient>, **How your answers will be used:** <where they go>

## Context

One paragraph for a recipient who does not know the user's situation. Enough to answer well, not a page.

## How to answer

The deadline and the rough effort. Partial answers and "I don't know" are useful. Flag anything you are unsure of. Do not skip it.

## <Theme heading>

One `##` section for each theme. Under each, its questions, most important first. Every question is one idea, never compound. Put an answer stub directly below it. Add a one-line _why this matters_ only where the question could be misread or could invite a throwaway answer.

<question-example>
### What load is the system expected to handle at launch?

_Why this matters: it decides whether we provision for burst traffic now or defer it._

>
</question-example>

## Anything else?

A closing catch-all: anything we did not ask that we should know?

</questionnaire-template>
