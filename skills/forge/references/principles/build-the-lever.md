# Build the Lever

When the work isn't trivial, build the tool that does it instead of doing it by hand.

A codemod, generator, or script does the work the same way every time and reruns for free. The tool is one artifact a reviewer can read and rerun to check the work. Hand-done changes can only be re-verified by redoing them. A deterministic script turns "trust me" into "run this".

Lean toward a lever when repetition or an otherwise uncheckable claim justifies it. First reuse an existing command, test, script or harness that already does or proves the work. A one-off can deserve a new lever, but a new artifact is not a requirement for every nontrivial task.

- Do the first unit by hand to learn the recipe, then build the tool. Prove it by rerunning it on that unit and diffing against your hand-done version. Make the lever safe to rerun.
- Codemod or script for edits, generator for repetitive files, a dump-to-sqlite query for analysis, a rerunnable check for verification.
- A deterministic lever beats fan-out. If the tool can process every unit in one pass, run it yourself. Don't fan out delegates to hand-apply what a script can do.
- When you fan work out to subagents, write the lever as one skill they all read. It holds the recipe, the verification contract, and the do-not-touch fences. Keep it outside the delegates' write scope so they can't quietly edit the contract.
- Report the lever used and the evidence it produced. An existing test or command can satisfy this. Do not manufacture a file merely to satisfy the workflow.
- Keep a useful new lever with the authorized task changes and follow the task’s checkpoint and publication policy.

The bar is whether the lever makes the work more repeatable or checkable than the tools already available. Build only what the task needs.

Distinct from [Encode Lessons in Structure](encode-lessons-in-structure.md), which makes a recurring instruction a durable guardrail. This is throughput and reviewability on the work in front of you. For scripting the verification itself, see [Prove It Works](prove-it-works.md).
