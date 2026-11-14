---
name: principle-prove-it-works
description: Apply after completing a task, before declaring done. Verify against
  the real artifact (run the feature, read the actual value, inspect the diff), not
  a proxy, self-report, or 'it compiles.'
disable-model-invocation: false
---

# Prove It Works

Verify every task output by checking the real thing directly. Do not infer from proxies, self-reports, or "it compiles."

**Why:** Unverified work has unknown correctness. Indirect verification (file mtimes, output freshness, agent self-reports, cached screenshots) feels cheaper than direct observation. Acting on a wrong inference costs far more than checking the source.

Check the real thing, not a proxy:
- Check process liveness directly, not indirectly through derived state
- Read the actual value, not a cached or derived representation
- When verification fails, suspect the observation method before suspecting the system

## Script the check when you can

The strongest proof is a deterministic script that re-runs the same comparison, not a one-time eyeball. Write the script, run it, and keep its output as an artifact a reviewer can re-run instead of trusting your word.

Keep verification evidence visible for the human. For UI changes, save, inspect, and show screenshots of the running changed surface at relevant states and viewport sizes before declaring completion or tearing down its environment. Save them outside the repository and temporary environment. If capture is blocked, report the gap before cleanup. Commit other evidence only when an auditable trail warrants it, like a big port or migration.
