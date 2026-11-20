---
name: tdd
description: Test-driven development for features and bug fixes, one vertical slice at a time at seams agreed with the user. Use when the user asks for TDD, red-green-refactor, a failing test or a regression test, or when an approved plan names the seams to test.
disable-model-invocation: true
---

# Test-driven development

TDD is the red → green loop. This skill makes that loop produce tests worth keeping: what a good test is, where tests go, the anti-patterns, and the rules of the loop. Every section applies on every cycle.

When you explore the codebase, read `GLOSSARY.md` if it exists, so that test names and interface vocabulary match the project's domain language. Respect the ADRs in the area you touch.

## What a good test is

A test verifies behavior through a public interface, not implementation details. The code can change entirely, and the test must not. A good test reads like a specification. "User can checkout with valid cart" tells you which capability exists, and it survives a refactor.

[Test Behavior, Not Implementation](../forge/references/principles/test-behavior-not-implementation.md) gives the two edits to judge a test against. See [tests.md](references/tests.md) for examples and [mocking.md](references/mocking.md) for mocking guidelines.

## Seams: where tests go

A **seam** is the public boundary you test at: the interface where you observe behavior and do not reach inside. Tests live at seams, never against internals.

**Test only at seams agreed in advance.** Before you write a test, write down the seams under test and confirm them with the user. Put them in the plan you present for approval. You cannot test everything. Agreed seams put the testing effort on the critical paths and the complex logic.

Ask: "What is the public interface, and which seams do we test?" Give each proposed seam a one-line note on what it catches and what it misses.

When the shape of the interface is itself the question, read [Deep Modules](../forge/references/principles/deep-modules.md) for the vocabulary: module, interface, depth, seam, adapter, leverage and locality.

## Anti-patterns

- **Implementation-coupled.** The test mocks internal collaborators, tests private methods, or verifies through a side channel, such as a database query in place of the interface. The sign: the test breaks when you refactor, but the behavior did not change.
- **Tautological.** The assertion computes the expected value the way the code does, such as `expect(add(a, b)).toBe(a + b)`. The test passes by construction and cannot disagree with the code. Take expected values from an independent source: a known-good literal, a worked example, the spec.
- **Horizontal slicing.** You write all tests first, then all implementation. Tests written in bulk verify imagined behavior. Work in **vertical slices**: one test, one implementation, repeat. Each test is a tracer bullet that responds to what the last cycle taught you.

## Rules of the loop

- **Red before green.** Write the failing test first. Run it, and confirm that it fails for the intended reason. Then write only enough code to pass it. Do not anticipate later tests or add speculative features.
- **One slice at a time.** One seam, one test, one minimal implementation for each cycle.
- **Refactoring is not part of the loop.** Refactor after the slices pass and before the Forge review, with the tests passing. Use [refine-code](../refine-code/SKILL.md) for a larger cleanup.

## Bug fixes

For a bug, the first slice is the regression test.

1. Identify the intended behavior, the current behavior and the smallest observable reproduction.
2. Write the smallest test at an agreed seam that fails because of the bug.
3. Fix the root cause with the smallest change. Run the test again.

Do not change a test to match a wrong implementation. Do not weaken an existing assertion unless the expected behavior changed and the reason is clear.

## When a failing test is impractical

Prefer no new test to a bad test. A test is bad when it:

- mostly tests mocks
- encodes implementation details
- depends on timing or unrelated global state
- needs expensive infrastructure for a small change

In that case, use the closest executable check. Examples are a targeted script, a manual reproduction command, browser automation, a snapshot comparison, a log assertion and a focused integration check.

## Final response

Report the evidence, not only the outcome:

- Name the seams under test.
- Name each failing-before test or executable check and the failure it produced.
- Name the passing-after run and the nearby validation you did.
- If you could not show failing-before evidence, state why, and describe the closest check you used.
