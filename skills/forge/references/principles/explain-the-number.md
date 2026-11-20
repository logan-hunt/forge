# Explain the Number

- **Write the decision before you run.** Name the result that would change a decision, and the noise floor. Stop when the run-to-run spread is larger than the effect.
- **Ask "why not double?"** Name the resource or code path that bounds the result, such as a core, a lock, the disk, the network, or the load generator itself. Get it from a profile or from system counters taken during a run, then map it to source. A guess from reading the code is not a limiter. If you cannot say why the number is not twice as good, you do not know what you measured.
- **List what else the number could be measuring, and rule out each one with evidence.** The usual suspects are errors, skipped or cached work, and code that never ran. Others are an untuned side (left on default settings), noise, and a piece too small to matter end to end.
- **Keep the evidence with the number.** Put the run count, the spread, and the limiter in the notes or a linked artifact.

For a performance number, run the full procedure with the [benchmark-checklist](../../../benchmark-checklist/SKILL.md) skill. For an eval result, ask the same of the trials. Did every run do the task? Does the gap hold across trials and models? Does the scenario matter?

You skipped this when any applies:

- A run started without the result that would change a decision.
- A number's evidence has no run count, no spread, or no named limiter.
- The time saved exceeds the time the changed piece took.

Distinct from [Prove It Works](prove-it-works.md), which checks that an output is real.
