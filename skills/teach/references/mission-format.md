# MISSION.md format

`MISSION.md` is at the workspace root. It records the reason the user is learning this topic. Trace every teaching decision back to it: what to teach next, which resources to show, which exercises to design.

## Template

```md
# Mission: {Topic}

## Why
{1-3 sentences. The concrete real-world goal of the user. What changes in their life or work when they have this skill? Avoid abstract framings such as "to understand X". Ask for the underlying outcome.}

## Success looks like
- {A specific, observable thing the user will be able to do}
- {Another specific thing}
- {…}

## Constraints
- {Time, budget, prior commitments, learning preferences, anything that limits the approach}

## Out of scope
- {Adjacent topics the user does not want to follow now. This protects the zone of proximal development.}
```

## Rules

- **One mission for each workspace.** Two unrelated topics need two workspaces.
- **Concrete, not abstract.** "Run a half marathon by October" is better than "get fitter". "Ship a Rust CLI to my team" is better than "learn Rust".
- **Challenge a vague mission.** If the user cannot say why, interview them before you write anything. A bad mission is worse than no mission.
- **Revise when reality changes.** When the user's goal moves, update this file. A stale mission misdirects later sessions.
- **Keep it short.** A `MISSION.md` longer than one screen is a plan, not a compass.
