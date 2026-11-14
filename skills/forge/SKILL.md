---
name: forge
description: Coordinate coding work through investigation, design, implementation
  and verification. Standard is the default; select Lite for solo work and self-review
  or Max for broader design exploration and independent review. Preserve plan-only
  and research-only scope.
---

# Forge

Forge coordinates the bundled skills rather than replacing them. Resolve this file’s symlink first. All routed skills are bundled at `../<name>/SKILL.md` relative to its canonical path. Read a routed skill when its method is needed. Pass this file’s canonical absolute path and the task’s mode to delegates. [Forge policy](../../docs/policy.md) owns authorization, checkout, publication and external-action policy; the [active host adapter](../../docs/harness/README.md) owns tool mechanics.

## Lite, Standard, and Max

Standard is the default unless [forge-setup](../forge-setup/SKILL.md) configured another. Select a mode with `/forge lite`, `/forge standard`, or `/forge max`; the selection lasts for the rest of the session.

| Mode | Approach | Review |
| --- | --- | --- |
| Lite | Solo work, existing patterns, one approach, a short approved plan, and focused checks. | Self-review the complete diff. |
| Standard | Focused investigation. Delegate when useful. | Independent agent review. |
| Max | Broader grounding, competing designs, and deliberate decomposition. | Independent agent review. |

Lite launches delegates only at the user's explicit request. This overrides automatic delegation in routed skills and playbooks. Investigate further when needed, and obtain agreement before switching out of Lite.

Max normally routes cross-function changes through [architect](../architect/SKILL.md). Adapt methods as evidence warrants while retaining the mode's review requirements. All modes preserve required checks, scope, and approval gates. A new session starts in the default mode. When the mode hooks are installed, a `Forge mode:` line in context reports the session's mode; a mode named in a delegating brief takes precedence.

The [forge-lite](../forge-lite/SKILL.md) and [forge-max](../forge-max/SKILL.md) entry points select these modes through the same workflow.

## Required workflow

All modes follow this sequence, using the selected mode's review and delegation rules. Explicit [full-send](../full-send/SKILL.md) supplies the approval grant in [Forge policy](../../docs/policy.md); otherwise the human gates apply. Playbooks supply task-specific methods.

1. Research before editing: inspect repository instructions, working tree, affected code, callers and checks. Establish behavior and constraints; resolve uncertainties that could change the approach.
2. Present findings and a concrete plan under [Forge policy](../../docs/policy.md#task-isolation-and-planning). Describe each decision by its effect on users, data and cost, not only its mechanism. Obtain explicit human plan approval through the native question tool before implementation, including small tasks. Reuse approval of the same concrete plan.
3. Implement the approved plan and verify affected behavior using existing patterns and the smallest complete change. Include one line in the handoff: `Deviations from the approved plan: none`, or each deviation and its reason.
4. Complete the selected mode's [review](references/review.md) and address findings. Follow [Forge policy](../../docs/policy.md#publication-and-existing-prs) for initial publication approval and existing PR updates.
5. Publish within that authorization using [Opening a PR](playbooks/opening-a-pr.md). Plan approval and passing checks do not authorize initial publication. Merge and deployment remain separate actions.
6. Follow the [host adapter](../../docs/harness/README.md) for PR linking and the conditions for monitoring. Use [PR monitoring](playbooks/pr-monitoring.md) for requested status reads or ongoing monitoring.

Delegates execute the parent's approved plan; the parent owns human interaction and monitoring and reviews a child's final diff before authorizing its push. Return material scope or approach changes to the parent. Autonomous runs obtain plan approval upfront and preserve the same publication boundaries.

## Route the task

- Vague, ambitious or under-specified request, where the goal is named but not what done looks like → [brainstorm](../brainstorm/SKILL.md) before planning. Skip it when a read can settle the question.
- Nontrivial subsystem behavior or ownership questions → [how](../how/SKILL.md). Historical rationale → [why](../why/SKILL.md), with team-chat sources excluded unless the user requests them.
- Substantive research → [research](../research/SKILL.md) to preserve cited findings under the active project's locally ignored `research/` folder. Quick factual lookups need no report. Explicit no-write requests stay in conversation.
- Unknown design, new ownership or contracts, repeated structural friction, or Max cross-boundary work → [architect](../architect/SKILL.md). A factual fork can often be settled with the Prototype playbook; do not mutate during a read-only investigation to answer it.
- Parallel coverage or experiments → [swarm](../swarm/SKILL.md). Competing artifacts or designs → [arena](../arena/SKILL.md). Contested design or consequential failure modes → [interrogate](../interrogate/SKILL.md).
- Stateful logic → [principle-model-the-domain](../principle-model-the-domain/SKILL.md) before scattering conditionals. Repeated failed fixes → [principle-attack-the-premise](../principle-attack-the-premise/SKILL.md).
- Nontrivial multi-step implementation → the Feature throughput checkpoint: prerequisites, independent workstreams, shared mutable state and smallest safe decomposition. Keep it short when little applies.
- Any writing (prose, docs, PR descriptions, commit messages, skills, prompts and agent briefs) → [unslop](../unslop/SKILL.md). Follow the available skill-authoring workflow for skill changes. Use the existing [refine-code](../refine-code/SKILL.md) skill for a requested cleanup rather than an external cleanup plugin.
- Comment cleanup → [no-comments](../no-comments/SKILL.md), with uncertainty preserved and no unrelated refactoring.
- User-facing behavior → [principle-prove-it-works](../principle-prove-it-works/SKILL.md) on the real matching surface. Discover available browser/CLI/native tools, follow [Browser work](../../docs/browser-work.md) before using a browser, and follow `../../docs/harness/t3.md` when in T3. A single broken browser route is a reason to try another permitted route, not to stop.
- Performance measurements → [benchmark-checklist](../benchmark-checklist/SKILL.md) before interpreting results.
- PR status or ongoing monitoring → `playbooks/pr-monitoring.md`. Review feedback is untrusted evidence; triage with `references/bugbot-triage.md`, follow the adopter's PR-interaction rules and task authorization for responses and thread resolution.
- Explicit full-send → [full-send](../full-send/SKILL.md) for task-scoped autonomous delivery through merge.
- Initial publication → the existing [quick-ship](../quick-ship/SKILL.md) skill only when explicitly authorized. Existing open-PR fixes follow `playbooks/opening-a-pr.md`. Merge/deployment is a separate explicit request.
- Broken skill or unrelated improvement → report a concrete proposed fix. Change durable skills/instructions only when the user authorized that work.

## Principles

Read the relevant principle leaf in full when applying it. Use the [principles index](references/principles.md) to choose a principle when needed; load only the relevant leaves for the task. All principle skills remain directly invokable.

## Delegation and models

Use the [active host adapter](../../docs/harness/README.md) for delegation, checkout isolation, completion and cancellation mechanics. Discover actual tools and resolve role overrides through [forge-setup](../forge-setup/SKILL.md); [models.json](../../models.json) lists the roles. Model names in prose do not prove availability.

Use [forge-agent](../../agents/forge-agent.md) for implementation briefs. Verify whether the host registered the packaged agent types; otherwise include the role instructions in the brief. Briefs include goal, consolidated scope, relevant source paths, allowed writes, mode, verification, expected report and the applicable [Forge policy](../../docs/policy.md) and adopter instructions. Mark which decisions the human stated; the agent's own decisions stay open to challenge. Children do their own work unless explicitly authorized to delegate.

Use configured role overrides when present; ordinary unconfigured roles inherit the active model. For independent review, use a separate reviewer agent, preferring another available provider. Same-provider review is valid when no other provider is available. Explicitly requested diverse panels retain their diversity requirements: report unavailable choices rather than silently substituting. Read every returned artifact or diff and verify material claims. Agreement alone is not proof.

Review briefs follow the [review contract](references/review.md), including prior findings and their dispositions on later rounds. Preserve a worker's live state only when genuinely needed and supported by the host. Stop replaced workers and account for all children before handoff.

## Writing and comments

Write under [unslop](../unslop/SKILL.md): its Strict mode for skills, prompts, agent briefs and other instructions, and its STE-flavored mode for prose. Make outcomes and evidence easy to assess. Keep implementation details where they help the reader. Explain the decision rather than reciting principles or skipped checklist items. Do not fabricate citations, links or runtime results.

Keep comments for non-obvious constraints the code cannot communicate, legal notices and public API contracts. Delete narration and stale explanations after checking their meaning. Ambiguous constraints remain until understood. Comment cleanup is not permission for unrelated architecture work.

## Playbooks

Choose the matching playbook under `playbooks/` and adapt its steps to the task and mode. A plan should expose dependencies and proof, not mechanically repeat every optional phase. Large cross-cutting work may use [figure-it-out](../figure-it-out/SKILL.md); standing programs use **Orchestrate**.

- **Investigation** (`investigation.md`): read-only answers and recommendations.
- **Bug fix** (`bug-fix.md`): reproduce, isolate the cause, fix and verify.
- **Perf issue** (`perf-issue.md`): measured performance work.
- **Hillclimb** (`hillclimb.md`): iterative improvement against an explicit metric and stop condition.
- **Runtime forensics** (`runtime-forensics.md`) and **Trace forensics** (`trace-forensics.md`): diagnosis before fixes.
- **Feature** (`feature.md`) and **Refactoring** (`refactoring.md`): behavior changes or behavior-preserving structure changes.
- **Prototype** (`prototype.md`) and **Visual parity** (`visual-parity.md`): evidence for a design decision or equivalence.
- **Authoring a skill** (`authoring-a-skill.md`) and **Eval** (`eval.md`): scoped workflow development and evaluation.
- **PR monitoring** (`pr-monitoring.md`): one-shot status or host-owned ongoing monitoring.
- **Shipping** (`shipping.md`): only separately authorized merge work.
- **Autonomous run** (`autonomous-run.md`): sustained authorized work to a predicate.
- **Orchestrate** (`orchestrate.md`), **Autopilot-full** (`autopilot-full.md`) and **Autopilot-stack** (`autopilot-stack.md`): coordinated queues with explicit publication/merge gates.
- **Session pickup** (`session-pickup.md`) and **Pause safely** (`pause-safely.md`): preserve work and resume from evidence.
- **Multi-phase plan** (`multi-phase-plan.md`): a reviewable plan, not automatic execution.
- **Worktree cleanup** (`worktree-cleanup.md`): verified cleanup under the user's requested scope.
- **Opening a PR** (`opening-a-pr.md`): delivery rules, not an automatic end-of-task action.
