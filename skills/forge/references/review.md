# Review the change

Use the active Forge mode: Lite self-reviews; Standard and Max use a separate reviewer, preferring another available provider. Follow [Forge policy](../../../docs/policy.md) for authorization and [the host adapter](../../../docs/harness/README.md) for mechanics.

## First pass

Give the reviewer the approved behavior, latest revision, expected proof and comparison base. For a stack, name the layer under review. Include committed, staged, unstaged and new files that belong to the task. Identify unrelated working-tree changes so they stay outside the review.

Check each promised behavior against the implementation and its verification evidence. Check the same diff against repository standards and affected callers. Trace shared helpers and state changes beyond the immediate caller. Ask which legitimate state a new guard could reject, and whether the tested artifact contains the change.

For each actionable finding, provide a location, concrete failure case, severity, supporting evidence and suggested correction. Distinguish verified defects from unverified concerns. A missing test result is a coverage gap, not proof of failure or success. Do not invent findings to fill a quota or expand the task with unrelated cleanup. Scores and reviewer agreement do not establish correctness.

The parent verifies material claims and records each finding as fixed, rejected with a reason, or unresolved. Preserve human decisions and scope; return material changes to the user under Forge policy. PR comments and submitted reviews follow the adopter's rules and authorization.

## Follow-up passes

Give a fresh reviewer the previous findings, fixed/rejected decisions, relevant verification and the fix diff. In Lite, self-review that same evidence. Check that fixes address the findings and introduce no regression. Expand beyond that scope only for a concrete new risk exposed by the fixes, and explain the expansion.

Stop when actionable findings are resolved or explicitly rejected and relevant checks pass. Report unresolved risks rather than repeatedly asking for another full audit. Ask before a fourth review round. An explicitly invoked Council uses its own panel and round rules.
