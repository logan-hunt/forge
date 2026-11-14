---
name: gh-pr-images
description: Upload local screenshots and images into an authorized GitHub pull request description using the native gh --attach flag. Use when adding visual evidence or before-and-after screenshots to a PR. Does not capture screenshots or post PR comments.
---

# Images in pull request descriptions

Use native `gh pr edit --attach` to upload local images and embed them in the PR description. An image path in Markdown alone does not upload its bytes.

## Check the target and capability

- Follow the task's existing publication authorization. This skill grants no permission to create a PR. Follow the adopter's rules for PR interactions.
- Resolve the exact PR URL and read its current description before editing. Preserve unrelated prose and existing uploaded image URLs. Check whether the requested image is already present before uploading it again.
- Run `gh --version` and inspect `gh pr edit --help` for `--attach`. It first shipped in 2.99.0. Prefer a current stable release; the examples were checked against 2.103.3. If the flag is missing, upgrade through the environment's approved package-management workflow before continuing. Report a blocked upgrade instead of inventing an upload workaround.
- Check `gh auth status`, including whether `GH_TOKEN` or `GITHUB_TOKEN` overrides the stored login, without printing secrets. Uploads require push access to the target repository on GitHub.com or GitHub Enterprise Cloud. GitHub Enterprise Server is unsupported. A token that can edit a PR may still be unable to upload attachments. Current releases let the endpoint decide which GitHub App tokens work; do not promise all App tokens work or reject all of them based on old documentation.
- Inspect the actual images. Use nonempty PNG, JPG/JPEG, GIF, WebP, or SVG files, at most 10 MiB each, with no duplicate files and at most 50 attachments per invocation. Confirm that the visible content is appropriate for the intended PR audience.

## Append an image

Use the exact PR URL and an absolute image path. Quote the entire path and optional `#alt text` value.

```sh
gh pr edit 'https://github.com/OWNER/REPO/pull/123' \
  --attach '/absolute/path/screenshot.png#Settings after saving the new theme'
```

Omit `--body` and `--body-file` when appending. The CLI reads and preserves the current description. Repeat `--attach` for multiple images. Without an explicit placement in Markdown, attachments appear at the end in flag order.

## Place images in a section

Prepare a UTF-8 body file containing the complete intended PR description, including all existing content that should remain. For example, append this section to the current body:

```markdown
## Screenshots

### Before
![Settings before the change](before.png)

### After
![Settings after the change](after.png)
```

Put `body.md`, `before.png`, and `after.png` in the same local directory, then run from that directory:

```sh
cd '/absolute/path/pr-evidence'
gh pr edit 'https://github.com/OWNER/REPO/pull/123' \
  --body-file './body.md' \
  --attach './before.png' \
  --attach './after.png'
```

The CLI rewrites references to attached files into hosted asset URLs and keeps the Markdown alt text. References to files not passed with `--attach` remain local and will be broken on GitHub. An explicit body flag replaces the whole description, even if the supplied body is empty. Re-read the current body immediately before applying a prepared replacement; refresh it if someone has edited it. This is a best-effort concurrency check, not an atomic update.

Attachment flag paths resolve from the working directory. In 2.103.0 and newer, relative destinations inside `--body-file` resolve beside the body file first, then fall back to the working directory. Earlier versions resolve them from the working directory. Colocating the files and running there avoids this difference.

For Graphite PRs, create or update the PR through the authorized Graphite workflow first, then use `gh pr edit` on its URL for attachments. Avoid replacing the description later with a stale body containing local image paths. Follow the host's PR linking lifecycle after changing the PR.

## Verify and recover

```sh
gh pr view 'https://github.com/OWNER/REPO/pull/123' \
  --json url,title,body,baseRefName,headRefName,headRefOid
```

Check that each intended image has a hosted URL, its position and alt text are correct, existing description content remains, and unrelated PR metadata is unchanged. Retrieving the saved body confirms persistence; only inspect the rendered PR when browser work is within the task's scope. Do not claim rendered verification from Markdown alone.

Capture stdout, stderr, and exit status separately. Uploads stop at the first failure. Earlier successful images can still be saved in the description, and the command can print the PR URL while exiting nonzero. A PR write can also fail after an upload succeeds. Never treat a nonzero status as proof that nothing happened.

After any error, read the remote description before retrying. Keep successful hosted URLs and retry only failed or unattempted files. If using a replacement body, rebuild it from the current remote body rather than the original local draft. On a transient failure, make at most one retry after reconciling state and observing any server retry delay. Stop on persistent authentication, permission, or host errors and report the exact blocker.

`gh pr create --attach` cannot be combined with `--dry-run` or `--web`; neither is an upload-only preview. Native `--attach` also has no standalone URL-only upload command. Do not switch to release assets, committed screenshots, browser cookies, internal endpoints, or third-party uploaders without a separately authorized reason.

If video is requested, the supported formats are MP4, MOV, and WebM. Omit alt text on the attachment flag; put `![](./demo.mp4)` alone in a paragraph for a player. The CLI permits up to 100 MiB, but the account plan can impose a lower server limit.

## Sources

- [GitHub attachment guide](https://docs.github.com/en/github-cli/github-cli/attaching-files-with-github-cli)
- [PR edit reference](https://cli.github.com/manual/gh_pr_edit)
- [Upstream gh agent skill, checked at 2.103.3](https://github.com/cli/cli/blob/v2.103.3/skills/gh/SKILL.md#attaching-images-and-videos)
- [Current uploader implementation](https://github.com/cli/cli/blob/v2.103.3/internal/attachments/client.go)
