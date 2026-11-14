# Prepare Forge for a team

## Choose the team's entry points

Start with Forge, Forge Lite and Forge setup. Standard is the default; use Lite for solo work. Plan approval, review and publication follow [Forge policy](policy.md). Install hooks only when requested.

The package keeps all bundled skills available. Treat these groups as capability scope, not a claim that every skill has been evaluated in every host:

| Group | When to use it |
| --- | --- |
| Core workflow | Forge modes, planning, implementation, verification and review. These are the team's starting entry points. |
| Optional methods | How, Why, research, cleanup, teaching and catch-up when the task needs them. |
| Advanced workflows | Arena, Swarm, autonomous queues, benchmarks and statechart tooling when their capabilities, scope and verification are available. |

Keep repository-specific checks, environments and PR-interaction rules in the adopting repository. Keep experimental team instructions outside the shared defaults until reviewed. Broad discovery-policy changes and skill removals need behavior evidence; installing this package does not make every method a required phase.

## Run the local checks

From the package directory, create a development environment and run the release check:

```sh
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements-dev.txt
.venv/bin/python -B scripts/check-release.py
```

Python 3.10 or newer and Node are required for these checks. PyYAML is a development dependency for metadata validation; activation, configuration and Forge hooks use Python's standard library. The repository CI runs the same local check on Linux and macOS. A passing local check does not establish that CI or a real host installation passed.

The validator parses YAML, checks required skill fields and invocation types, parses JSON and checks inline local Markdown file links and heading anchors. Its heading rules approximate GitHub Markdown. It does not check every Markdown construct, external URL or vendor schema. Run the host's current plugin validator as well when available.

## Check host behavior before claiming support

Use a disposable project and user configuration for installation checks. Observe discovery under the names the host actually exposes, project/user scope, optional hook trust, effective defaults, session mode changes and silent no-op hooks. Update or relocate the package, then verify that links and hook commands still execute the intended copy. Remove only Forge's registrations and preserve unrelated configuration.

Record the host/version, operating system, package revision and observed results. Manifests and subprocess tests establish different things from host loading. Keep an unavailable host, untested platform or blocked trust flow visible in the handoff.

## Exercise the workflow instructions

The [behavior cases](../evals/scenarios.json) cover approval, read-only scope, Lite delegation, provider fallback, repository rules and review follow-ups. They are host-independent prompts and expectations, not an automatic or scored agent benchmark.

Copy the [fixture](../evals/fixtures/greeter/greet.py) and [test template](../evals/fixtures/greeter/test_greet.py.template) into a disposable project outside the source checkout, naming the latter `test_greet.py`. Its test intentionally fails until the greeting is corrected. Read each case's setup before starting it. Use the real host's Forge invocation, and give the agent only the prompt and project context. Keep the expectations and other cases out of its task brief.

Inspect resulting files, relevant checks and the task's own tool trace. Record pass, fail or unverified for each expectation, with evidence. An agent saying it followed the workflow is insufficient. Do not turn an unavailable capability into a pass.

For a comparison, use the same task snapshots and host/model versions, repeat runs and record success, unauthorized actions, unnecessary questions, review rounds, elapsed time and reported usage separately. Keep denominators and unavailable measurements visible. Approval regressions block sharing regardless of average speed. No prompt-size reduction alone proves a performance gain.
