# Prompts worth copying

Swap in the real paths, skills, and done checks. Informal wording works.

## Understand

- `/forge read <thread>. restate the underlying issue in your own words, in plain english.`
- `/in-your-own-words <long or messy ask>`
- `/sharpen <the prompt you're about to send>`
- `/forge investigate why <symptom>. give me what we know, what data you used, and your best hypotheses. don't change any code yet.`
- `use /how to understand <subsystem>. then use /why to find out why it broke recently.`
- `/recall my work on <topic> from last week, then read <issue>.`
- `/how does the change you just made work? walk me through the diff and show where its tradeoff matters for the caller.`
- `/forge take over this branch. read the decision log, find what's done, and continue. don't redo finished work.`

## Build

- Solo fix: `/forge lite fix <small bug>. use existing patterns and verify the affected behavior.`
- Bug: `/forge <symptom>. repro first, then fix and verify.`
- Bug in an app: `/forge repro this with /verify-<app>. if it repros on main, fix it and show me a video as proof.`
- Bug with a cheap test: `/forge repro <bug> first. if there's a cheap test path, /tdd it. then fix and rerun.`
- Feature: `/forge add <behavior>. <current output> stays byte-identical. verify both.`
- Refactor: `/forge move <code> into one module, zero behavior change. record the current output first and prove it's unchanged after.`
- Perf: `/forge <operation> takes <time> on <fixture>. trace it, fix the measured cause, show me before and after.`

## Design and plan

- `/forge prototype a few options for <feature>. take screenshots or videos for me to compare.`
- `/forge we need <feature>. /architect it first, and answer open questions with prototypes. let me review before proceeding.`
- `/how would i use <new package>? walk me through one example and compare it with the current package.`
- `ask /arena for a second opinion on this thread and our approach.`
- `/forge turn this design into a plan. small verifiable PRs, each with its own verification steps.`
- `/forge plan the migration of <library> to <target>. small verifiable PRs. the result must match the original exactly, bugs included.`

## Review and ship

- `/interrogate the whole branch, but skeptically. don't change anything yet. no nitpicks unless it's a real bug or regression.` Read the Dropped list too.
- `/council review this branch. scores out of 10. fix what you agree with and keep scope tight.`
- `/swarm check every package under <dir> against its check script. one worker per package. one report.`
- `/quick-ship publish this selected change. one coherent commit per PR layer.`
- `/forge monitor this PR through T3. report new failures.` For status only: `/forge check on pr <number>. anything outstanding?`
- `/forge land the stack.`

## Away and back

- `/forge im going to bed. <goal> in a fresh worktree off <base>. done means <checks>. keep a decision log. continue through the host task lifecycle until done. if you're truly stuck after a few hours, stop and write up why.`
- `/ketchup` catches you up on this chat since your last message and lists every call that waits on you.
- `/forge max implement this queue. each item is independent. keep initial publication gated.`
- `/forge autopilot these changes, but don't merge. i'll land them.`
- `/reflect propose durable changes from what we learned. do not apply them yet.` Approve only edits that change a future decision.
- `/bro` restates the last reply in plain words.
