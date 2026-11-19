# Recipes and pitfalls

- A small scoped change: Lite, direct investigation, a short approved plan, focused checks, and self-review.
- A familiar bug: standard, reproduce the behavior, trace the cause, implement and verify. Use broader design methods if the cause exposes a consequential design problem.
- A new execution lifecycle: Max, how/why grounding, architect/arena alternatives, scoped implementation and adversarial-review. Exercise retries and interrupted state, not only the happy path.
- A plan request: return a grounded plan and unresolved choices. Do not begin implementation because an architecture skill normally proceeds further.
- A review of an open PR: review-only stays read-only. A request to fix findings updates that existing PR under [opening-a-pr.md](../../skills/forge/playbooks/opening-a-pr.md), without writing comments.
- A new feature with no PR: checkpoints stay local until first publication is explicitly requested.
- A missing model: report the requested unavailable model; do not silently turn mixed-provider review into several copies of one family.
- A browser failure: inspect the error, make bounded retries and use another permitted route. Preserve sessions and distinguish real blockers from a broken tool.
- A repeated correction: propose the smallest durable fix supported by provenance, rather than rewriting global instructions automatically.
