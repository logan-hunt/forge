---
name: domain-modeling
description: Build and sharpen a project's domain model. Use when the user discusses codebase terminology, writes or edits a GLOSSARY.md, or records or edits an ADR.
---

# Domain modeling

Build and sharpen the project's domain model while you design. This is the active discipline: challenge terms, invent edge-case scenarios, and write the glossary and the decisions at the moment they become clear.

To read `GLOSSARY.md` for vocabulary is not this skill. Every skill does that. Use this skill when you change the model.

## File structure

Most repositories have one context:

```
/
├── GLOSSARY.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

A `GLOSSARY-MAP.md` at the root means the repository has more than one context. The map points to each one:

```
/
├── GLOSSARY-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── GLOSSARY.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── GLOSSARY.md
│       └── docs/adr/
```

Create files only when you have something to write. Create `GLOSSARY.md` when the first term is resolved. Create `docs/adr/` when the first ADR is necessary. When the repository's instructions name other locations, use those.

## When to write

- The user invoked [grill-with-docs](../grill-with-docs/SKILL.md), [triage](../triage/SKILL.md), [wayfinder](../wayfinder/SKILL.md) or [improve-codebase-architecture](../improve-codebase-architecture/SKILL.md): write each entry at the moment the term or decision is resolved. Do not collect entries for later.
- In all other cases: propose the entry in the conversation and write it after the user agrees.

This permission covers `GLOSSARY.md`, `GLOSSARY-MAP.md` and ADR files only. Leave the files uncommitted. Publication follows [Forge policy](../../docs/policy.md#publication-and-existing-prs).

## During the session

### Challenge against the glossary

When the user uses a term that conflicts with `GLOSSARY.md`, say so immediately. "Your glossary defines 'cancellation' as X, but you seem to mean Y. Which is it?"

### Sharpen fuzzy language

When the user uses a vague or overloaded term, propose a precise canonical term. "You say 'account'. Do you mean the Customer or the User? Those are different things."

### Discuss concrete scenarios

When the discussion is about domain relationships, test them with specific scenarios. Invent scenarios that probe edge cases and force a precise line between concepts.

### Cross-reference with code

When the user states how something works, check whether the code agrees. If you find a contradiction, show it. "Your code cancels entire Orders, but you said partial cancellation is possible. Which is right?"

### Update GLOSSARY.md

Use the format in [glossary-format.md](references/glossary-format.md).

`GLOSSARY.md` contains no implementation details. It is not a spec, a scratch pad, or a store for implementation decisions. It is a glossary and nothing else.

### Offer ADRs sparingly

Offer an ADR only when all three conditions are true:

1. **Hard to reverse.** A later change of mind has a meaningful cost.
2. **Surprising without context.** A future reader will ask why the team did it this way.
3. **The result of a real trade-off.** Real alternatives existed, and you chose one for specific reasons.

If one condition is false, do not write the ADR. Use the format in [adr-format.md](references/adr-format.md).

## For skills that read the model

Before you explore an area, read `GLOSSARY.md` and the ADRs that apply to it. If the files do not exist, continue without comment.

- Name each domain concept with the glossary term, in issue titles, proposals, hypotheses and test names. Do not use a synonym that the glossary lists under _Avoid_.
- If your output contradicts an ADR, say so explicitly: "Contradicts ADR-0007 (event-sourced orders), but worth a second look because…"
