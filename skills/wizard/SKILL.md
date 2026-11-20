---
name: wizard
description: Generate an interactive bash wizard that walks a human through steps only they can perform. Use to provision infrastructure, set up credentials or CI secrets, walk an unfamiliar third-party dashboard, or run a one-off migration or cutover. Do not use for steps the agent can perform itself.
---

# Wizard

A **wizard** is a bash script that walks a human, step by step, through a manual procedure. It opens each URL, says exactly what to click and copy, captures the values, and writes them where they belong (`.env`, GitHub secrets). It confirms at every stage and shows how many stages are left. A wizard can configure third-party services, run a one-off migration, or move the project from one state to another.

[template.sh](template.sh) already supplies the user experience:

- stage-by-stage progress and confirmation gates
- URL opening on every platform, including WSL
- hidden secret entry and idempotent `.env` upserts
- `gh secret` and `gh variable` writes
- a closing summary

**Your job is only to scope the procedure and author its stages.** The library above the `STAGES` marker is identical in every wizard. Never edit it.

A wizard is ephemeral by default: built for one run, saved to a scratch path or a `scripts/` path, and deleted when the job is done. Commit it only when the user wants a repeatable setup path in the repository.

The human runs the wizard and types every secret into it. Never ask for a secret in chat. Never print, log or read back a secret.

## Process

### 1. Scope the procedure

Find every manual step the human must take and every value that the wizard captures. Read the repository first. Do not ask before you read.

- For setup: `.env.example`, the names of the keys in `.env` and `.env.*`, `README`, `docker-compose*`, the framework config, and `.github/workflows/*`. Every `secrets.*` and `vars.*` reference is a value the wizard must produce.
- For a migration or a transition: the current state, the target state, and the irreversible actions between them.

Then show the user the ordered list of stages and the values each one produces. The user can add, remove or reorder stages. Wait for the user to confirm the list.

**Done when** every stage is named in order, and you know three things for each captured value:

- where the human gets it
- where the wizard writes it: `.env`, a GitHub secret, both, or nowhere
- whether it is secret or public

### 2. Map the journey of each stage

For each stage, write the precise path a human follows. Name the URL to open, the action there, where the value appears and the variable it fills. Example: "Dashboard → Developers → API keys → Reveal test key → copy".

Where you do not know the current UI or the exact command, say so. Ask the user or check the documentation. Never invent a step that may not exist.

**Done when** every stage traces to concrete instructions that a stranger can follow.

### 3. Author the wizard

Copy `template.sh` to the target path. Replace the example stage with one `stage` for each step, in dependency order. Use the library helpers: `stage`, `say`, `step`, `open_url`, `ask`, `ask_secret`, `write_env`, `set_secret`, `set_var`, `pause` and `confirm`. Set `TOTAL_STAGES` to the number of stages you wrote.

Keep the standard the template sets:

- Open the URL before you ask for its value.
- Use `ask_secret` for anything secret.
- Use `write_env` for every value that persists.
- Use `set_secret` only for the values that CI needs.
- Use `confirm` before any irreversible action.
- Keep each stage to one focused task. Each `stage` clears the screen, so only the current step is visible.

Do not change the library above the marker.

### 4. Verify and hand off

- Run `bash -n <script>`. Run `shellcheck` if it is available.
- Run `chmod +x <script>`.
- Do not run the wizard end to end. It opens browsers and blocks on human input. Trace it statically: every value from step 1 is captured and lands where step 1 said, and every `set_secret` name exactly matches a `secrets.*` reference in CI.
- Tell the user how to run it. For a repeatable setup path, propose a commit and a link from the README.
