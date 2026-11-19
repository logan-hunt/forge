# PR descriptions

- Write PR descriptions for reviewers: what changed, why, and how the behavior was verified. Write them under the [Clarify Writing](../../clarify-writing/SKILL.md) skill in its STE-flavored mode.
- Use the repository's PR template when present. If it has none, use [the bundled PR template](../../../templates/pull_request_template.md). Include an issue reference only when relevant to the repository's workflow. Omit AI signatures.
- Leave out the noise from producing the change:
  - local environment problems (failing local typecheck/lint/hooks, dependency drift, `--no-verify`, flaky local setup)
  - routine checks CI already reports (lint, typecheck, test counts)
  - local tooling details (dev scripts, ports, test accounts)
  - how the change evolved (reverted attempts, review iterations)
- In the testing section, describe the tests added or changed and the behavior verified manually, not the commands that were run.
- Choose evidence that lets the reviewer judge the approved behavior. Use the example that fits the change.
  - UI: “Clicking **Show the page** used to leave the scan on the previous page. It now opens the selected question’s page.” Attach the before-and-after captures when available.
  - Migration: “Existing papers with numeric scores receive a total. Rolling back the app leaves those totals in place.” State what happens to the source data if the schema rolls back.
- Identify any remaining gap that affects the reviewer’s decision. Report local environment issues in chat.
