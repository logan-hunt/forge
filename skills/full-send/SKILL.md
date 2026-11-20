---
name: full-send
description: Complete the task through merged PRs when the user explicitly requests full send. Authoring or discussing this skill does not activate it.
disable-model-invocation: true
---

# Full send

Explicit invocation grants task-scoped plan/diff approval, publication, necessary testing, and merge authority for all task-related PR layers. The invocation is that approval. Never ask for plan, diff, publication or merge approval for this task. Preserve unrelated work. It replaces only these Forge approval gates, including browser/runtime testing. Team-chat, system and harness restrictions still apply.

Use [Forge](../forge/SKILL.md) for the selected mode's investigation, implementation, verification, and review. Proceed without human approval, preserving the selected mode. Use [Quick Ship](../quick-ship/SKILL.md) to publish, the [host adapter](../../docs/harness/README.md) to link and monitor, and [Shipping](../forge/playbooks/shipping.md) to merge. Retain this grant across wakeups. It covers the task named at invocation and every follow-up on its PRs, until they merge or the user says stop. A later instruction from the user narrows it. A new, unrelated task in the same thread follows the normal gates unless the user invokes full-send again. Only the root monitors and merges. Delegates publish within their assigned scope. Follow native monitoring lifecycle.

Merge only when the latest head has direct proof, passing required checks, required approvals, no outstanding human change requests, an up-to-date base and confirmed mergeability. Bot reviews must also be complete, with findings resolved or dismissed with reasons recorded in the conversation. Request queues or auto-merge only after these gates pass. Honor repository merge methods and confirm merged state. Normal deploy-on-merge is allowed. Handle feedback and thread resolution under [Forge policy](../../docs/policy.md#pull-request-interactions). Never bypass protection. Follow the adopter's authorization for PR interactions. Task-branch rewrites may use only force-with-lease.

Use the native question tool only for:

- consequential ambiguity
- unavailable proof
- an unfixable merge gate (say what it checks and what evidence covers it instead)
- actions beyond this grant: manual deployments, direct production operations, data deletion, unrelated work, closing PRs or rewriting other branches

Unfixable merge gates include a missing required human approval and a person's unresolved thread that the base requires resolved. Report them and wait. Without an answer, leave the PR open and unmerged. Report PR links, merge commits, proof and decisions.
