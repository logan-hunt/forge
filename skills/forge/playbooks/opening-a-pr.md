# Publication and PR updates

Follow [Forge policy](../../../docs/policy.md#publication-and-existing-prs) for checkout, plan approval, mode-specific review and publication gates. Complete [Forge's required workflow](../SKILL.md#required-workflow) before submission.

1. Inspect the intended branch, parent and complete task diff. [Quick Ship](../../quick-ship/SKILL.md) supplies the submission commands for authorized initial publication. For an existing PR, apply the update rules in Forge policy. Use [Graphite](../../graphite/SKILL.md) for stack operations where configured and usable.
2. In Graphite repositories inspect the actual stack and dry-run submission. Also inspect the intended remote base and commit range. `--update-only` prevents new PR objects, not exposure of ancestor commits in a child push. If updating the PR would publish an unpublished ancestor or unrelated descendant, keep the validated fix committed locally. Then name the affected layer and request first-publication authorization. Do not reparent to bypass that gate. Revalidate descendants affected by changed parent behavior. Follow the repository's checks and the graphite/quick-ship command contracts.
3. Write the title and body under [PR descriptions](../references/pr-descriptions.md). Follow the adopter’s attribution and PR-interaction rules.
4. Verify each affected PR's actual head and base and report pending checks honestly. In T3, follow the [host PR lifecycle](../../../docs/harness/t3.md#pr-lifecycle). Outside T3, use the host's native monitor when requested or required.
