# Authoring or modifying a skill

Use the host’s skill-creator workflow when available. Otherwise use this playbook directly. Preserve the selected source and scope. Never edit a plugin cache as a shortcut.

Before proposing changes to instructions, skills or workflow, read relevant decision records identified by the adopter or repository. A fix for a friction entry or repeated correction must pass the bar and follow the form order in [Encode lessons in structure](../references/principles/encode-lessons-in-structure.md). Start with the actual request and relevant source. Prefer copying existing reusable material and making targeted changes when that preserves behavior. Keep descriptions precise and guidance progressive. Reference shared capabilities instead of copying conflicting authorization rules into every leaf.

Write skill and instruction text under the [Clarify Writing](../../clarify-writing/SKILL.md) skill in its Strict mode, and run its `scripts/ste-lint.py` on the files you change.

Validate frontmatter, names, references and executable helpers. For substantial behavioral changes, use independent realistic scenarios with permitted side effects. Static validation does not prove good decisions. Check the edit in a new session. The authoring session knows the change and does not re-read a skill it already invoked. Before deleting an instruction because the strongest model did not need it, check a weaker model you run. A tie on the strongest model does not show the instruction is unused. Existing instructions change only under user authorization. Incidental lessons are proposals.

Finish with the changes and evidence. Delivery follows opening-a-pr.md. Authoring a skill does not automatically publish it.
