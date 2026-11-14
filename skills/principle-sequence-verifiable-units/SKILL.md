---
name: principle-sequence-verifiable-units
description: Apply to multi-step work (sweeps, migrations, runs of similar edits)
  and to how you stack commits and PRs. Break work into small units that each end
  in a verifiable state, check each before the next, and order delivery so the sequence
  proves itself to a reviewer.
disable-model-invocation: false
---

# Sequence work into verifiable units

Order work as a sequence of small units, each ending in a state you can check, and don't advance until the current one is green.

**Why:** A break caught at the unit that caused it is cheap to localize. A break caught after a batch is buried, and you have already built further on a broken base. Sequencing those same units into a delivery a reviewer can replay turns "trust me" into "watch it go red, then green."

**Execution.** In a sweep, migration, or any run of similar edits, verify each change before starting the next. Each unit is a before/after bracket: known-good state, one change, run the check, then proceed. Record the current baseline and preserve the starting checkout and branch; do not rebase as verification setup. When a lever does the edits, the per-unit check is nearly free. Run it anyway.

**Delivery.** Order local work so each step produces evidence: reproduce before fixing, capture a baseline before treatment, establish a scaffold before dependent features. Local checkpoints can preserve that sequence. Before publication, consolidate task checkpoints into one coherent, validated commit per PR layer. Stack layers by real dependency and preserve their ancestry; do not publish a failing-test-only layer merely to narrate development.

The sequencing complement to the [prove-it-works](../principle-prove-it-works/SKILL.md) principle skill, which keeps each check real, and the [build-the-lever](../principle-build-the-lever/SKILL.md) principle skill, which makes the per-unit check cheap.
