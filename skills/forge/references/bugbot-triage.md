# Bugbot triage

Use this reference when the PR monitoring playbook (`../playbooks/pr-monitoring.md`) handles Bugbot or review-automation comments. The goal is not to ignore Bugbot by default. The goal is to stop treating every comment as a required code change.

## Decision rubric

Classify each Bugbot thread before acting:

- `fix`: The comment identifies a plausible correctness, security, privacy, data loss, auth, billing, migration, idempotency, race, or shipped-behavior issue. When fixing is authorized, fix it in the lowest owning PR and report the evidence and commit in this conversation. Follow the adopter's authorization for responses and thread resolution.
- `dismiss`: The comment matches a documented low-risk noisy pattern, and the current code/context proves the concern does not need a code change. Report the concrete reason and follow the adopter's authorization for responses and thread resolution.
- `ask`: The comment is novel, high-severity, security/privacy/data-related, or ambiguous. Ask the user instead of guessing.

When in doubt, ask. Skipping a noisy code-quality comment is cheap. Skipping a real data or security bug is not.

## Resolving bot threads

Follow [Forge policy](../../../docs/policy.md#pull-request-interactions) and the adopter's instructions. Resolving a thread is an external write and needs task authorization. Fixing or dismissing a finding does not itself grant resolution authority. Verify the thread's current state and author before an authorized resolution. Leave unresolved findings open.

List the threads, 100 at a time. While `hasNextPage` is true, run it again with `-f after=<endCursor>`:

```bash
gh api graphql -f owner=<owner> -f repo=<repo> -F number=<number> -f query='
query($owner:String!,$repo:String!,$number:Int!,$after:String){repository(owner:$owner,name:$repo){pullRequest(number:$number){
  reviewThreads(first:100,after:$after){pageInfo{hasNextPage endCursor} nodes{id isResolved path
    comments(first:1){nodes{author{__typename login} body}}}}}}}'
```

Resolve one thread. This writes no comment:

```bash
gh api graphql -f id=<thread id> -f query='mutation($id:ID!){resolveReviewThread(input:{threadId:$id}){thread{isResolved}}}'
```

## Learned pattern format

Add future patterns in this shape:

```markdown
### <short pattern name>

- Confidence: candidate | recurring | strong
- Skip when: <conditions that must be true>
- Do not skip when: <risk boundaries>
- Example signal: <phrases or code context that identify the pattern>
```

Use `candidate` for one or two examples. Use `recurring` after multiple real dismissals. Use `strong` only when the pattern is narrow, repeatedly verified, and low-risk.

## Recurring skip candidates

### Intentional UI or design-system visual changes

- Confidence: candidate
- Skip when: The PR description, screenshots, design review, or nearby code makes the visual change explicit. The Bugbot comment only restates that a shared visual default changed.
- Do not skip when: The comment points to accessibility, focus visibility, keyboard navigation, color contrast, or a component API contract that the PR did not intentionally change.
- Example signal: Comments about focus outlines, button sizes, spacing, or shared component visual defaults where the owner replies "intentional" or "intended".

### Upstack or stack-local usage Bugbot cannot see

- Confidence: candidate
- Skip when: Bugbot flags an export, component, helper, or file as unused. The active forge's PR list and diffs, upper-stack diffs, or PR context show that a later PR in the stack uses it.
- Do not skip when: The current PR is not in a stack, the symbol is public API, or you cannot verify the supposed upstack use.
- Example signal: "Exported component is never used" with a human reply like "used upstack".

### Temporary duplication during parallel implementation

- Confidence: candidate
- Skip when: The PR intentionally duplicates a little code to keep a new path parallel to an old path. The old path is being deleted, replaced, or proven out.
- Do not skip when: The duplicated code changes security, billing, data access, API behavior, or a long-lived shared abstraction would clearly reduce risk.
- Example signal: "Significant duplication" or "duplicated validation logic" where the owner explains the old path will be deleted or the duplicate logic is intentionally local.

### Existing framework or component invariant covers the warning

- Confidence: candidate
- Skip when: A shared component, framework contract, type invariant, or single source of truth already guarantees the concern. That guarantee is visible in the current diff or nearby code.
- Do not skip when: The invariant is assumed but not enforced, depends on timing, or crosses async/state boundaries where values can diverge.
- Example signal: Comments about missing max-height on an inner popover when the shared popover enforces viewport bounds. Comments about nullable values where the local checked value and passed value share one source.

### Owner-declared follow-up or deferred cleanup

- Confidence: candidate
- Skip when: The PR owner explicitly says the issue is a known follow-up. The current PR does not make the behavior worse. The comment is not about a high-risk area.
- Do not skip when: The agent is acting without owner input, the issue is medium/high severity product behavior, or deferring would merge a new regression.
- Example signal: "I'll worry about that later" or "we'll delete this eventually".

### Self-withdrawn or explicit false-positive rule comments

- Confidence: recurring
- Skip when: The comment body or a later Bugbot reply explicitly says the finding is withdrawn, compliant, or a false positive. The agent can verify the relevant rule locally.
- Do not skip when: The only evidence is a human saying "false positive" on a high-risk issue without explanation.
- Example signal: A file-naming rule comment whose body says the file is already compliant.

## Ask by default

Do not auto-skip these categories, even if a previous PR dismissed something similar:

- Security, privacy, auth, billing, data retention, training-data, and permission-boundary findings.
- High-severity findings.
- Migration, schema, idempotency, concurrency, and cross-system behavior findings.
- Comments where the suggested fix is small and clearly reduces risk without changing product intent.

Historical data showed humans sometimes dismiss security/data-flow comments. Treat those as owner judgment calls, not team-wide skip rules.

## Inherited candidate examples

These examples are hypotheses to verify against the current code. Durable edits require explicit authorization.

Propose new candidate learnings during or after review when they look team-useful but not yet mature. Prefer promoting recurring candidates into the section above once several PRs confirm the pattern.

### Manual reimplementations of native browser behavior

- Confidence: candidate
- Skip when: Practically never. When a diff replaces native browser behavior with a manual equivalent, Bugbot's logic-bug findings against that code have been consistently legitimate. Examples: native sticky → JS-positioned clones, native scroll targeting → forwarded wheel/touch events, paint-order occlusion → masks/clip-path.
- Do not skip when: The finding concerns mask/clip hit-testing divergence, observer-vs-React state timing races, or event-forwarding gaps in such code. The gaps include wheel deltaMode, touch pans, scroll-chaining at edges, and tap slop. Default to fix.
- Example signal: "masks do not affect hit-testing", "overlay blocks wheel scroll", "ignores deltaMode", "runs in the IntersectionObserver callback before React applies state".

### Contract-test drift claims are cheaply verifiable — run the test first

- Confidence: candidate
- Skip when: Never skip the verification itself. It costs one command. Some PRs
  ship a contract test that pins protocol or documentation prose (regexes over
  a SKILL.md, snapshot of doc wording). If Bugbot claims "the test no longer
  matches the doc" (or vice versa), run that test on the PR tip before
  classifying. A red run confirms the claim empirically. A green run is a
  concrete disproof for the report to the user.
- Do not skip when: n/a. This is a verification shortcut, not a dismissal
  pattern. Repeat-pass lean-dismiss heuristics would misfire here.
  Prose-pinning tests drift precisely BECAUSE earlier fix rounds edit the prose.
- Example signal: "Contract test omits the pre-fix wait" on a PR whose earlier
  fix commits reworded the pinned passage. The test run on the tip failed on
  exactly the cited assertion.
  pass 7 despite every earlier pass being fixed-and-resolved.

### Stale security-review finding already fixed later in the same PR

- Confidence: candidate
- Skip when: An agentic security review (or similar) claims a missing authz/validation call, and the current PR tip clearly includes that exact gate (with tests). A later hardening commit typically added the gate after the review ran.
- Do not skip when any applies:
  - The cited helper is a no-op for the principal under discussion.
  - The check runs after the side effect it guards.
  - Coverage for the claimed principal is missing.
- Example signal: A HIGH "missing authorization check" finding while the exact guard is already called before the side effect on the tip.

### Widening a deliberately narrow error condition would mask the real error

- Confidence: candidate
- Skip when: The finding asks to broaden a narrow error condition (a specific
  `errno`, error code, or status class) into a catch-all. That narrowness
  encodes a real distinction. The canonical shape is a dependency fallback
  gated on `ENOENT`. There, "binary is not installed" differs from
  "the command ran and failed". Retrying on any non-zero exit would re-run a
  legitimate failure (not found, expired auth, network) against the fallback.
  It would then report the fallback's error, not the true one.
- Do not skip when any applies:
  - The narrow condition misses a case in the SAME category (another "binary
    unusable" errno such as `EACCES`, another transport-level failure).
  - The unhandled path loses data or leaves partial state.
  - The retry is idempotent AND the original error is still surfaced.
- Example signal: "only retries when X fails with ENOENT … never tries the
  fallback even when a working Y exists". The comment points at code whose
  fallback exists for a missing dependency rather than a failed operation.
  than a failed command.
