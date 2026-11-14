---
name: refine-code
description: Refine existing code for readability, intentional organization, and logical
  spacing while preserving behavior. Use for a requested code-style cleanup of selected
  files, a module, or current branch changes, including a plan-only assessment.
disable-model-invocation: true
---

# Refine Code

Make code easy for a person to read from top to bottom. Favor intentional organization, clear names, and useful whitespace. Treat these preferences as strong defaults with room for local conventions.

## Resolve scope and plan

- Read applicable repository instructions and inspect the branch, working tree, and relevant Graphite ancestry before editing. Continue an existing task on its current branch; otherwise follow the user's base-selection workflow. Preserve unrelated work and staging.
- Use the user's selected files, symbols, folder, or established task scope. Without an explicit target, inspect the current branch's changes against its verified Graphite parent or merge base with trunk, including relevant staged, unstaged, and untracked work. On trunk, default to uncommitted changes. If there is no clear target, ask for one; do not expand to the whole repository.
- For a branch cleanup, refine changed code and its immediate context. An explicit file or module target allows cleanup within that target, including existing code. Read surrounding code for context without restyling unrelated areas.
- Present a concise plan identifying the scope, concrete readability improvements, and appropriate checks. A request to assess, discuss, or plan stops there. Implement once the plan is approved.

## Refine with intention

- Group related statements into logical paragraphs. Add a blank line when the purpose changes; keep closely related lines together. Let the formatter handle mechanical layout.
- Use domain names and useful intermediate values that explain the steps. Expand dense expressions or nested control flow when that clarifies the main path; use early returns where helpful.
- Keep functions and components cohesive. Extract helpers for meaningful responsibilities or useful reuse, keeping related steps close together. Avoid abstractions or file splits solely to shorten code.
- Make component, prompt, and plugin composition visible. Put substantial behavior in named handlers or builders while preserving the overall structure.
- In TypeScript, prefer `const` arrow functions and inline named exports. Use named props/options/parameter types, allowing inline types for tiny local helpers. Preserve declaration forms when hoisting or other semantics require them.
- Keep comments minimal and preserve useful explanations of non-obvious constraints. Prefer names and structure over comments narrating the code.
- In tests, distinguish setup, action, and assertions with spacing. Split unrelated scenarios when it clarifies intent; share meaningful setup and preserve coverage and state transitions.

Preserve behavior, public APIs, evaluation and side-effect order, error handling, and exact prompt or user-facing wording. Keep dependencies and architecture stable. Report unrelated bugs separately. Leave already-clear code alone.

## Validate and finish

Review the diff for unintended behavior or scope changes. Run scoped formatting/lint checks and relevant existing tests or type checks using the repository's tooling. Add regression coverage only when a refactor creates a meaningful preservation risk; whitespace alone does not need new tests. Distinguish pre-existing failures and unavailable checks from regressions.

Summarize the refinements, validation, and remaining concerns. Follow [Forge policy](../../docs/policy.md#publication-and-existing-prs) for checkpoints, first publication and existing-PR updates. A plan-only assessment never authorizes these mutations.
