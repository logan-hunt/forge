# Prompts worth copying

These examples use Claude plugin commands such as `/forge:forge`. With local skill links, use the bare name, such as `/forge`. Replace placeholders with your paths and checks.

## Understand

- `/forge:forge read <thread>. restate the underlying issue in your own words, in plain english.`
- `/forge:restate-goal <long or messy ask>`
- `/forge:refine-prompt <the prompt you're about to send>`
- `/forge:forge investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use /forge:how to understand <subsystem>. then use /forge:why to find out why it broke recently.`
- `/forge:total-recall my work on <topic> from last week, then read <issue>.`
- `/forge:how does the change you just made work? walk me through the diff and show where its tradeoff matters for the caller.`
- `/forge:forge take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Solo fix: `/forge:forge lite fix <small bug>. use existing patterns and verify the affected behavior.`
- Bug: `/forge:forge <symptom>. repro first, then fix and verify.`
- Bug in an app: `/forge:forge reproduce <symptom> through the app as a user would. after the approved fix, repeat the interaction and show the result.`
- Bug with a cheap test: `/forge:forge repro <bug> first. if there's a cheap test path, /forge:tdd it. then fix and rerun.`
- Feature: `/forge:forge add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `/forge:forge move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `/forge:forge <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `/forge:forge prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `/forge:forge we need <feature>. /forge:architect it first, and answer open questions with prototypes. let me review before proceeding.`
- `/forge:how would i use <new package>? walk me through one example and compare it with the current package.`
- `ask /forge:arena for a second opinion on this thread and our approach.`
- `/forge:forge turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `/forge:forge plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `/forge:adversarial-review the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `/forge:council review this branch. scores out of 10. fix what you agree with and keep scope tight.`
- `/forge:swarm check every package under <dir> against its check script. one worker per package. one report.`
- `/forge:quick-ship publish this selected change. one coherent commit per PR layer.`
- `/forge:forge monitor this PR through T3. report new failures.` For status only: `/forge:forge check on pr <number>. anything outstanding?`
- `/forge:forge land the stack.`

## Away and back

- `/forge:forge im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. continue through the host task lifecycle until done. if you're truly stuck after a few hours, stop and write up why.`
- `/forge:recap-chat` catches you up on this chat since your last message and lists every call that waits on you.
- `/forge:forge max implement this queue. each item is independent. keep initial publication gated.`
- `/forge:forge autopilot these changes, but don't merge. i'll land them.`
- `/forge:reflect propose durable changes from what we learned. do not apply them yet.` Approve only edits that change a future decision.
- `/forge:bro` restates the last reply in plain words.
