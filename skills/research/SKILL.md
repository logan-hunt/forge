---
name: research
description: Conduct substantive project research, save cited Markdown and HTML reports in the project's locally ignored research folder, and present the HTML inline in T3. Use for research requests or substantial investigations; not routine factual lookups. Honor explicit no-file requests.
---

# Research

Use the [Forge investigation playbook](../forge/playbooks/investigation.md) for the investigation itself. Keep the researched code, instructions and external services unchanged. The standing research workflow authorizes only its local evidence artifacts and repository-local Git exclusion; an explicit analysis-only/no-write instruction overrides that permission and keeps findings in conversation.

## Keep findings with the project

- Identify the target project from the request and current workspace, not the skill's directory. In Git, use `git rev-parse --show-toplevel` in the active project checkout/worktree. Outside Git, use the established project root. Ask only if the project is genuinely ambiguous.
- Save substantive findings as `findings.md` and a standalone `report.html` under `research/YYYY-MM-DD-topic/`, using the user's local date and a descriptive slug. Markdown is the readable source copy; HTML presents the same findings and citations. Reuse the directory when continuing the same investigation; otherwise choose a distinct name. Preserve existing artifacts. Do not create a worktree solely to store research.
- Include the question and scope, concise findings, exact source locations or links, evidence versus hypotheses, relevant limitations and recommended next steps. Keep raw logs and sensitive data out unless needed and authorized. Add supporting files only when they materially help verify the conclusions.
- Link the saved findings in the response and summarize the answer. Research artifacts are not an implementation, checkpoint commit or publication request.

## Present the report inline

In T3, deliver the research through its inline HTML tools as well as saving it. Discover the current `html_preview` and `html_render` contracts and follow their layout/theme requirements. Use a concise, readable report with evidence links; add charts for trends/comparisons and expandable details only when they help. Keep findings and uncertainty consistent with the Markdown copy.

Build `report.html` from `findings.md` with the shared [builder](../../tools/research-report/build.py): `python3 <forge-root>/tools/research-report/build.py <research-folder>`. Its [template](../../tools/research-report/template.html) is self-contained, uses T3 theme variables with fallback values for standalone reading, and keeps the outer document transparent and fluid as the renderer requires. Rebuild after every change to `findings.md` so both copies agree.

For a chart or other markup that Markdown cannot express, save it as an `.html` fragment in the research folder and put `<!-- include: name.html -->` on its own line in `findings.md`. The template styles `.hbar` bar rows and `.legend`. Do not write a one-off build script; when a report needs something the template lacks, extend the template. Fragments use inline styles and any needed scripts, with no required CDN assets or remote fetches, and escaped source excerpts. Evidence links may open their original sources.

Read the saved HTML, pass those exact contents to `html_preview`, inspect the result and console output, and correct material rendering issues in the saved file. Then pass the final same HTML to `html_render`, using the preview height within the tool's allowed range. A file link, screenshot or browser tab alone does not fulfill inline delivery. Do not start a server or use browser preview tools to display the report.

Keep the final text brief and link both saved files rather than duplicating the rendered report. If the HTML tools are unavailable or fail after a bounded useful retry, retain the saved reports, give the findings in conversation and state that inline delivery failed. Outside T3, provide the saved reports and a concise answer using the host's available presentation surface.

For explicit analysis-only/no-file requests, skip filesystem writes and Git exclusions; render HTML from memory when permitted. Respect a request for plain text or no visualization instead of rendering.

## Exclude only this repository's reports

Before saving, inspect `git ls-files -- research` and the existing destination. Never overwrite tracked reports or untrack files. Existing tracked research remains tracked; select a new untracked report path.

Use `git rev-parse --path-format=absolute --git-path info/exclude` to find the repository's personal exclusion file. This also resolves correctly from a linked worktree. Preserve its contents and append the exact root-anchored `/research/` line only if absent, preserving a newline before the entry. Create the parent directory/file if needed. Verify the actual new report path with `git check-ignore -v -- <path>` before writing it. If it is still not ignored, diagnose the applicable rule rather than claiming success or changing shared ignore rules.

Do not add a blanket `research/` pattern to the global excludes file or edit the project's tracked `.gitignore`. The repository-local exclusion applies to its worktrees without affecting other repositories. If the project is not a Git repository, save there and state that no Git exclusion applies. Never follow an existing `research` or report-directory symlink outside the selected project without explicit authorization.
