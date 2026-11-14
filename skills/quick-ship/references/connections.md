# Connection checks and recovery

Discover capabilities in the active host rather than copying tool names from another environment. Read-only connection checks do not authorize publication or configuration changes.

- Git hosting: verify the authenticated identity, target host and repository access with the available connector or CLI. For GitHub CLI, use `gh auth status` and a repository read. Never display tokens.
- Issue tracking: needed only when the task or repository workflow uses it. Discover the actual tracker, team/project, state and assignee. A missing optional tracker does not block a PR.
- Graphite: use only for repositories already configured for it. Inspect installed CLI help, authentication and stack metadata. Follow the bundled Graphite skill and preserve the intended branch/base when falling back to Git.

Use the host's supported authentication/configuration flow and preserve unrelated settings. Check project overrides as well as user configuration. Do not install duplicate integrations or broaden token permissions to work around an unexplained failure. Reload connections or start a new session after authorized changes when required.

Connection configuration and credentials belong to the adopter's environment, outside this package. Do not create issues, branches or PRs merely to test write access.
