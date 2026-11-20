---
name: review-comments
description: Review comments in a scoped change, remove redundant narration, and preserve
  useful explanations and contracts. Use for /review-comments or comment cleanup before
  review.
disable-model-invocation: false
---

# Review Comments

Use the caller’s files or diff. Otherwise inspect the current task diff against its verified base, including relevant working-tree changes. Preserve unrelated files.

## Review

Ask the `comment-reviewer` agent for a focused review through the active host when independent review is useful. It returns findings. The parent owns any edits. Read its definition at `../../agents/comment-reviewer.md`.

Delete comments that merely narrate visible code, stale explanations, redundant banners, and commented-out dead code when the surrounding behavior confirms they are obsolete.

Keep legal and license text, public API contracts, and concise explanations of non-obvious constraints, including external platform behavior, ordering, concurrency or compatibility requirements. If a constraint is ambiguous, preserve it while seeking evidence and report the uncertainty. Do not delete first and reconstruct the reason later.

## Improve within scope

A clearer name or a small local simplification may make a comment unnecessary. Do not launch architecture work or change behavior merely to remove explanatory prose. Report broader improvements separately.

Inspect lint and TypeScript suppressions against the actual rule and code. Remove one only when the cause is fixed or the suppression is proven obsolete. An unresolved correctness suppression is a finding, not permission to break the build.

Follow the repository's source-comment conventions. Preserve a constraint’s meaning in code or concise prose rather than inventing its rationale.

## Validate and report

For an authorized cleanup, run the relevant formatting and checks and inspect the final diff. A review-only request returns findings without modifying files. Report substantive deletions, preserved uncertain constraints and any remaining correctness issues. Publication follows the task’s normal policy.
