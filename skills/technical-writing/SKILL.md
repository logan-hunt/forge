---
name: technical-writing
description: Write or review developer documentation, RFCs, PR descriptions and commit messages for clear structure, precise instructions and concise prose.
disable-model-invocation: false
---

# Technical writing

Write so a developer can understand the document on the first read. Follow the adopter's terminology and documentation conventions.

## Choose the document's purpose

Use Diátaxis to choose the main structure:

- A tutorial helps someone learn by completing a real task. Show a useful result early.
- A how-to solves a concrete problem for a reader who knows the basics. State prerequisites and expected results.
- A reference describes exact interfaces, fields, constraints and errors. Match the code's organization.
- An explanation develops the reasons, tradeoffs and mental model behind a design.

Keep each section focused and link substantial supporting material. Combine forms when it helps the reader; do not create extra documents merely to satisfy a classification.

## Make instructions precise

Use the real file, symbol, option and command names. Match examples to the actual interface and test commands you change.

Put a condition before the step it controls. Say who acts and what result they should observe. Distinguish required steps from optional choices. Separate implementation, verification, publication and activation.

Use numbered steps for a sequence and bullets for parallel items. Give warnings only for concrete risks. Preserve uncertainty and known limitations rather than making the writing sound more certain than the evidence.

## Reduce reader effort

Prefer active voice and familiar words. Cut filler and repeated policy. Keep useful context and articles; do not compress sentences into jargon or fragments.

Split sentences that contain unrelated thoughts or ambiguous conditions. Keep one name for each concept. Explain an acronym when the audience needs it. Use headings and links that identify the task or destination.

Follow [Unslop](../unslop/SKILL.md) without erasing the author's meaning. Treat style rules as aids to clarity, not reasons to distort technical facts or impose a personal voice.

## Review the result

Check source claims, links, examples and described behavior. Keep facts separate from recommendations. Do not turn a proposal into a completed implementation through wording.

For a PR description, lead with the problem and resulting behavior, then give the verification and material gaps. Omit execution logs and details that do not help the reviewer. Use the repository's template when one exists.
