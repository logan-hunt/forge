# Out-of-scope knowledge base

The `.out-of-scope/` directory in a repository holds the records of rejected feature requests. It has two purposes:

1. **Institutional memory.** It keeps the reason a feature was rejected after the issue is closed.
2. **Deduplication.** When a new issue matches an earlier rejection, the skill shows the earlier decision, so that nobody argues it again from the start.

## Directory structure

```
.out-of-scope/
├── dark-mode.md
├── plugin-system.md
└── graphql-api.md
```

Use one file for each **concept**, not for each issue. Group the issues that request the same thing in one file.

## File format

Write the file in a relaxed, readable style, like a short design document and not a database entry. Use paragraphs, code samples and examples, so that a first-time reader understands the reasoning.

```markdown
# Dark Mode

This project does not support dark mode or user-facing theming.

## Why this is out of scope

The rendering pipeline assumes a single color palette defined in
`ThemeConfig`. Supporting multiple themes would require:

- A theme context provider wrapping the entire component tree
- Per-component theme-aware style resolution
- A persistence layer for user theme preferences

This is a significant architectural change that doesn't align with the
project's focus on content authoring. Theming is a concern for downstream
consumers who embed or redistribute the output.

```ts
// The current ThemeConfig interface is not designed for runtime switching:
interface ThemeConfig {
  colors: ColorPalette; // single palette, resolved at build time
  fonts: FontStack;
}
```

## Prior requests

- #42: "Add dark mode support"
- #87: "Night theme for accessibility"
- #134: "Dark theme option"
```

### Name the file

Use a short, descriptive kebab-case name for the concept, such as `dark-mode.md`, `plugin-system.md` or `graphql-api.md`. A person who reads the directory listing must understand what was rejected without opening the file.

### Write the reason

Give a substantive reason. "We don't want this" is not a reason. A good reason refers to one of these:

- Project scope or philosophy ("This project focuses on X. Theming is a downstream concern.")
- Technical constraints ("Supporting this would require Y, which conflicts with our Z architecture")
- Strategic decisions ("We chose to use A instead of B because...")

Give a durable reason. A temporary circumstance, such as "we're too busy right now", is a deferral and not a rejection.

## When to check `.out-of-scope/`

In step 1 of triage (Gather context), read all files in `.out-of-scope/`. When you evaluate a new issue:

- Check whether the request matches an existing out-of-scope concept.
- Match by concept, not by keyword. "Night theme" matches `dark-mode.md`.
- If you find a match, tell the maintainer: "This is similar to `.out-of-scope/dark-mode.md`. We rejected this before because [reason]. Do you still feel the same way?"

The maintainer has three options:

- **Confirm.** Add the new issue to the file's "Prior requests" list, then close the issue.
- **Reconsider.** Delete or update the out-of-scope file. The issue continues through normal triage.
- **Disagree.** The issues are related but distinct. Continue with normal triage.

## When to write to `.out-of-scope/`

Write here only when an **enhancement**, not a bug, is rejected as `wontfix`.

Do not write here when an issue is closed as `wontfix` because the feature is **already implemented**. That feature was built, not rejected. A record of it would make later deduplication checks report a false rejection. The closing comment points to where the feature is.

The flow:

1. The maintainer decides that a feature request is out of scope.
2. Check whether a matching `.out-of-scope/` file exists.
3. If it exists, add the new issue to its "Prior requests" list.
4. If it does not exist, create a file with the concept name, the decision, the reason and the first prior request.
5. Post a comment on the issue that gives the decision and the reason. Name the concept. Do not link to the `.out-of-scope/` file until it is published.
6. Close the issue with the `wontfix` label.

## Update or remove an out-of-scope file

If the maintainer reverses an earlier rejection:

- Delete the `.out-of-scope/` file.
- Leave the old issues closed. They are historical records.
- The new issue that caused the change continues through normal triage.
