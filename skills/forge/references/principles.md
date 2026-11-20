# Principles

For simplicity, read [Simplify existing code](../../ponytail/SKILL.md#simplify-existing-code). Choose the entry that matches the task and read its guidance.

**Core**

- [Foundational Thinking](principles/foundational-thinking.md). Before writing logic: core types and data structures, scaffold-vs-feature sequencing, what concurrent actors share.
- [Redesign from First Principles](principles/redesign-from-first-principles.md). Integrating a new requirement into an existing design. Redesign as if it had been foundational from day one.
- [Attack the Premise](principles/attack-the-premise.md). Two or more fixes that share one premise have failed the same gate. Write the premise down and test it directly before you write another fix that assumes it.
- [Minimize Reader Load](principles/minimize-reader-load.md). Reviewing or shaping code that's hard to trace. Count layers and hidden state, collapse one-caller wrappers, shrink mutable scope.
- [Outcome-Oriented Execution](principles/outcome-oriented-execution.md). Planned rewrites and migrations with explicit phase boundaries. Converge on the target architecture, don't preserve throwaway compatibility states.
- [Experience First](principles/experience-first.md). Product, UX, or feature-scope tradeoffs. Choose user delight over implementation convenience.
- [Exhaust the Design Space](principles/exhaust-the-design-space.md). A novel interaction or architectural decision with no precedent. Build 2-3 competing prototypes and compare before committing.
- [Build the Lever](principles/build-the-lever.md). Any non-trivial work. Prefer a reusable tool that does or proves it. Reuse an existing test or command when sufficient. Create a lever when repeatability or proof earns its maintenance.

**Architecture**

- [Model the Domain](principles/model-the-domain.md). Writing stateful logic, or code that branches a lot or repeats a shape assumption across files. Encode the domain in a structure (state machine, typed model, table or registry, reducer, boundary, the right collection) instead of scattered conditionals.
- [Deep Modules](principles/deep-modules.md). Designing or reshaping a module, placing a seam, or judging whether a wrapper earns its place. Put much behavior behind a small interface and test through that interface.
- [Boundary Discipline](principles/boundary-discipline.md). Wiring validation, error handling, or framework adapters. Guards at system boundaries, trust internal types, keep business logic pure.
- [Type System Discipline](principles/type-system-discipline.md). Designing types or a signature in any typed language. Make illegal states unrepresentable, brand primitives, parse external data at boundaries.
- [Make Operations Idempotent](principles/make-operations-idempotent.md). Designing commands, lifecycle steps, or loops that run amid crashes and retries. Converge to the same end state.
- [Migrate Callers Then Delete Legacy APIs](principles/migrate-callers-then-delete-legacy-apis.md). Introducing a new internal API while old callers exist. Migrate and delete in one wave only when all consumers can move together. Otherwise, preserve external and persisted contracts.
- [Separate Before Serializing Shared State](principles/separate-before-serializing-shared-state.md). Concurrent actors might write the same file, branch, key, or object. Eliminate the sharing first.

**Verification**

- [Prove It Works](principles/prove-it-works.md). After a task, before declaring done. Verify against the real artifact, not a proxy or "it compiles".
- [Fix Root Causes](principles/fix-root-causes.md). Debugging. Trace each symptom back to the first place the system went wrong and fix it there. A guard is a fix only when the state it handles is legitimate.
- [Sequence Work into Verifiable Units](principles/sequence-verifiable-units.md). Multi-step work (sweeps, migrations, runs of similar edits) and how you stack commits and PRs. Break work into small units that each end in a check, verify each before the next, and order delivery so the sequence proves itself.
- [Test Behavior, Not Implementation](principles/test-behavior-not-implementation.md). Writing, changing, or keeping a test. Assert what the code's users can observe, so the test fails when that behavior breaks and keeps passing when only the internals change.
- [Explain the Number](principles/explain-the-number.md). Apply before you measure, and before you trust, report, or act on a number you measured (a speedup, regression, throughput, latency, or eval result). Find what limits it, and rule out that it measured something other than the work you think.

**Delegation**

- [Guard the Context Window](principles/guard-the-context-window.md). Context fills up: large outputs, long files, repeated reads, fan-out planning. Route bulk to subagents, keep summaries in the main thread.

**Meta**

- [Encode Lessons in Structure](principles/encode-lessons-in-structure.md). You catch yourself writing the same instruction a second time. Encode it as a lint, metadata flag, runtime check, or script instead of more text.
