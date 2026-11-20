# Verify and publish

Follow [Forge's required workflow](../../skills/forge/SKILL.md#required-workflow) and the [Forge policy](../policy.md#publication-and-existing-prs).

Checks must show the behavior the change claims. Use the existing test suite, targeted failure cases and a real surface when that is the claim. Static, fake integration, installed-artifact and live-service verification are distinct evidence.

Follow the [review contract](../../skills/forge/references/review.md) for evidence-based findings and scoped follow-up passes. A new round carries forward fixed and rejected findings instead of restarting an unrelated audit.

Browser routes follow the active host. Try another permitted available route after a bounded failure rather than treating one broken browser as the end of verification. Preserve sessions and profile ownership. A missing login may still require the user.

For publication, use the [opening-a-PR playbook](../../skills/forge/playbooks/opening-a-pr.md), including Graphite submission checks where applicable. T3 delivery follows the [host PR lifecycle](../harness/t3.md#pr-lifecycle).
