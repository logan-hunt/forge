---
name: principle-encode-lessons-in-structure
description: Apply when you catch yourself writing the same instruction a second time,
  or notice a recurring correction. Encode the rule as a lint, metadata flag, runtime
  check, or script instead of more text.
disable-model-invocation: false
---

# Encode Lessons in Structure

Propose changes to instructions, skills and checks unless that maintenance or enforcement change is explicitly within the authorized task. Saving a memory needs no proposal. A recurring correction is evidence, not permission to edit global rules.

## Before proposing a fix

**The bar.** Change nothing unless the mistake would otherwise recur. Ask whether someone working from the current files would still make it. A one-off, or a mistake the files already prevent, needs no change.

**The form order.** Take the cheapest fix that holds, in this order:

1. A check that fails when the mistake is made: a hook, a test, or a rule in `scripts/verify-forge.py`.
2. One line in the instruction or skill that owns the topic.
3. A decision record or a memory, only when neither of the first two can carry it.

If the lesson needs judgment and cannot be encoded, make the instruction more prominent and add an example of the failure mode.

**Corollary:** If the fix is structural, only use the structural fix. The instruction is the symptom.
