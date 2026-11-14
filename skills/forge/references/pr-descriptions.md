# PR descriptions

- Write PR descriptions for reviewers: what changed, why, and how the behavior was verified.
- Use the repository's PR template when present. If it has none, use [the bundled PR template](../../../templates/pull_request_template.md). Include an issue reference only when relevant to the repository's workflow.
- Leave out the noise from producing the change:
  - local environment problems (failing local typecheck/lint/hooks, dependency drift, `--no-verify`, flaky local setup)
  - routine checks CI already reports (lint, typecheck, test counts)
  - local tooling details (dev scripts, ports, test accounts)
  - how the change evolved (reverted attempts, review iterations)
- In the testing section, describe the tests added or changed and the behavior verified manually, not the commands that were run.
- Report local environment issues to the user in chat instead.
