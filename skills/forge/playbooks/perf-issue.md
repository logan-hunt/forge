### Perf issue

**You own the measurement story. Plan, review, verify the numbers.** Tie every fix to a measurement, don't read source instead of measuring.

1. Capture a baseline trace via the matching available surface driver. Vet the baseline, and each later number, with the [benchmark-checklist](../../benchmark-checklist/SKILL.md) skill.
2. `how` to ground hypotheses. Don't claim a perf ceiling without running it first.
   Try the performance mantras in order, cheapest first:
   1. Don't do it. Stop work whose result nothing uses rather than cheapening it.
   2. Do it, but don't do it again.
   3. Do it less.
   4. Do it later.
   5. Do it when they're not looking.
   6. Do it concurrently.
   7. Do it cheaper.

   When an earlier mantra meets the target, stop.
3. Plan the fix from the trace. In Max, or when the fix changes ownership or contracts, use `architect` first. Use a scoped implementation delegate when the mode and task warrant it using your configured perf-issue model (role resolved through forge-setup; inherit when unconfigured). Use the configured model role and supported host options, following Forge’s Delegation and models section. Review the diff. Capture a post-fix trace.
   Apply the [sequence-verifiable-units](../references/principles/sequence-verifiable-units.md) principle, verifying each attempt before trying the next.
4. Parse and compare the artifacts (JSON to sqlite, diff). "Inconclusive" or wrong-surface is not a pass. Flag it.
5. Cite the measurement in the result and in an authorized PR description when one is published.
6. Apply **Publication and PR updates** (`opening-a-pr.md`).

For sustained improvement against a metric rather than a one-off fix, use the Hillclimb playbook (`hillclimb.md`).

**Reply:** baseline number, post-fix number, delta, artifact path.
