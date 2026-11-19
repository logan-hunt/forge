### Visual parity

**You own pixel-exact equivalence. The baseline is the spec. You do not touch it.** Equivalence is verified by image diff, not by eye.

1. Establish the baseline first, before any migration: a visual regression harness that screenshots the current component across its states, plus the target when matching two implementations. No baseline, no parity claim. A blocking prerequisite, not a follow-up.
2. Anti-shortcut clauses, stated and held: no harness modifications, no baseline tampering, no component restructuring to make a diff pass. If the baseline looks wrong, stop and ask, don't edit it.
3. Migrate one component at a time. Use disjoint write scopes in the starting checkout, one owner per component; sequence overlapping edits and use separate child checkouts only when explicitly requested by the user (the [separate-before-serializing-shared-state](../references/principles/separate-before-serializing-shared-state.md) principle). Shared primitives migrate first as a blocking phase.
4. Verify each component against its baseline via image diff on the matching surface via an available surface driver under the active host policy. A nonzero diff is a fail. Investigate the pixel delta. Repeat a bounded, evidence-led fix/check cycle per component until the diff is zero or a concrete blocker is reported.
5. Apply **Publication and PR updates** (`opening-a-pr.md`) per component or per safe batch.

**Reply:** components migrated, the diff result for each, the baseline harness location, what's left.
