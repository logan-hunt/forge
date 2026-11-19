# Deliver a saved plan

Give the user a complete plan they can reopen before they decide. This workflow authorizes local plan artifacts for substantive planning, including plan-only requests. When a user, adopter or host requires chat-only or restricts artifact writes, return the complete plan in chat. Explain any host limitation. The lead owns the plan. Delegates reuse the parent’s approved version. Under Full Send, save the substantive plan and proceed within the grant. Keep the sandbox and implementation approval gate intact.

## Write the plan

Use the following sections in order. Size each to the decision.

1. **Decision.** Lead with the user outcome, recommendation, key evidence and tradeoff. When the design is settled, name the implementation scope awaiting approval.
2. **Before and after.** Show what the user or data does today and after the change. Diagram the handoffs when ownership, sequence or recovery changes. A short labeled text flow renders in both Markdown and HTML.
3. **Implementation and proof.** For each meaningful unit, give the affected scope, its dependency or reason for going next, and an observable success check. Use PR boundaries only where they improve review or rollout. Put requested ticket mappings, execution details and allowed writes alongside their units.
4. **Open questions and approval.** Identify blocking decisions and who can resolve them. State the next action and its actual authorization status. For a plan-only request, end at delivery.

## Save and present

- In the target checkout use `research/plans/<task-slug>/v1/plan.md`. Use the [research exclusion procedure](../../research/SKILL.md#exclude-only-this-repositorys-reports) and verify Git ignores the destination before writing. If the host prevents local exclusion, deliver the full plan in chat and explain why the files could not be saved. Select a fresh task folder for unrelated work. Outside Git, use the same layout under the project root. Respect an explicitly requested destination or format.
- For a material revision, create the next unused version directory under the same task. Preserve delivered versions. Open the new plan with what changed, why and its consequence, and link the preceding version using a relative link such as `../v1/plan.html`.
- Render that Markdown with `python3 <forge-root>/tools/research-report/build.py <version-folder>/plan.md`. Read the sibling `plan.html` and resolve any version links against its directory. Keep both files local.
- In the initiating chat give a phone-readable summary of the outcome, decision and proposed next action. Link the current Markdown and HTML. In T3, use absolute file paths for chat links, including the superseded plan on revision. Preview the saved HTML with `html_preview`, inspect the output, correct rendering issues and then display it with `html_render` at the supported preview height. If inline delivery fails, give the file links and say so. Ask for approval only when the [router](../SKILL.md#required-workflow) requires it. Put the decision and the action it authorizes in the approval question itself.
