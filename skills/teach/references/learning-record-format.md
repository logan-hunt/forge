# Learning record format

Learning records are in `./learning-records/` and use sequential numbers: `0001-slug.md`, `0002-slug.md`, and so on. Create the directory only when you write the first record.

They are the teaching equivalent of ADRs. They record non-obvious lessons, key insights and stated prior knowledge that steer later sessions. Use them to calculate the zone of proximal development.

## Template

```md
# {Short title of what was learned or established}

{1-3 sentences: what was learned (or what prior knowledge was established), and why it matters for later sessions.}
```

That is the whole format. A learning record can be a single paragraph. Its value is the record that the user now knows this, and why that changes what to teach next.

## Optional sections

Include these only when they help. Most records do not need them.

- **Status** frontmatter (`active | superseded by LR-NNNN`). Use it when a later record replaces an earlier, wrong understanding.
- **Evidence**. How the user showed the understanding: a question answered, an exercise completed, prior experience cited. Use it when the claim may be revisited.
- **Implications**. What this makes possible or rules out for later sessions. Record it when it is not obvious.

## Numbering

Scan `./learning-records/` for the highest existing number and add one.

## When to write a learning record

Write one when any of these is true:

1. **The user showed real understanding of something non-trivial.** Exposure is not enough. You need evidence that they can use the concept correctly. This sets a new floor for what to teach next.
2. **The user disclosed prior knowledge.** "I already know X." Record it, with the depth the user claims, so that later sessions do not teach it again.
3. **A misconception was corrected.** The user believed something wrong and now sees why. These records predict where the user will stumble on related topics.
4. **The mission changed because of what the user learned.** The user found that they care about something different. Update `MISSION.md` and link to it from the record.

### What does not qualify

- Material that was only covered. Coverage is not learning. Wait for evidence.
- Information that `GLOSSARY.md` already records as a term definition. Do not duplicate it.
- A log of session activity. A learning record is an insight that changes a later decision, not a journal entry.

## Supersession

When a later record contradicts an earlier one, mark the old record `Status: superseded by LR-NNNN`. Do not delete it. The history of how the understanding changed is useful.
