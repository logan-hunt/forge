# Setup and sources

Install Forge through the logan-hunt/forge marketplace or expose its skills from a local package. See the [package README](../../README.md) for project and user scope. Installation does not enable hooks or replace AGENTS.md or CLAUDE.md.

Use [forge-setup](../../skills/forge-setup/SKILL.md) for optional hooks, the default mode and model-role overrides. Settings live outside the package so updates do not replace them. The host may namespace skill commands. Read sibling skills by their canonical paths when a command is not registered.

Use the [host adapter](../harness/README.md) for available tools and delegation mechanics. A manifest or copied role document does not prove that a host registered an agent or can run a requested model.
