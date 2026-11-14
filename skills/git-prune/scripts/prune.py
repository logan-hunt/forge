#!/usr/bin/env python3
"""Preview or apply cleanup of local branches and worktrees whose pull requests merged or closed.

A branch is deleted only when its newest same-repository PR is merged or closed and the
local tip is already contained in that PR's head, so nothing local-only is lost. A linked
worktree is removed only when it is clean and on such a branch, or detached at a commit
already on trunk. Everything else is kept and reported with the reason.
"""

from __future__ import annotations

import argparse
import json
import subprocess
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass
from pathlib import Path


@dataclass
class Worktree:
    path: Path
    head: str = ""
    branch: str | None = None
    locked: bool = False
    prunable: bool = False


@dataclass
class BranchPlan:
    name: str
    sha: str
    pr: dict | None
    keep_reason: str | None = None

    @property
    def deletable(self) -> bool:
        return self.keep_reason is None

    @property
    def pr_label(self) -> str:
        return f"PR #{self.pr['number']} {self.pr['state'].lower()}" if self.pr else "no PR"


@dataclass
class Plan:
    repo: Path
    trunk: str
    branches: dict[str, BranchPlan]
    remove_worktrees: list[Worktree]
    kept_worktrees: list[tuple[Worktree, str]]
    stale_worktrees: list[Worktree]
    switch_main_checkout_from: str | None


def run(args: list[str], cwd: Path, check: bool = True) -> subprocess.CompletedProcess:
    result = subprocess.run(args, cwd=cwd, capture_output=True, text=True)
    if check and result.returncode != 0:
        message = result.stderr.strip() or result.stdout.strip()
        raise SystemExit(f"`{' '.join(args)}` failed:\n{message}")
    return result


def git(cwd: Path, *args: str) -> str:
    return run(["git", *args], cwd).stdout.strip()


def git_succeeds(cwd: Path, *args: str) -> bool:
    return run(["git", *args], cwd, check=False).returncode == 0


def combined_output(result: subprocess.CompletedProcess) -> str:
    return "\n".join(part.strip() for part in (result.stdout, result.stderr) if part.strip())


def list_worktrees(repo: Path) -> list[Worktree]:
    worktrees: list[Worktree] = []
    current: Worktree | None = None

    for line in git(repo, "worktree", "list", "--porcelain").splitlines() + [""]:
        if line.startswith("worktree "):
            current = Worktree(path=Path(line.removeprefix("worktree ")).resolve())
        elif current is None:
            continue
        elif line.startswith("HEAD "):
            current.head = line.removeprefix("HEAD ")
        elif line.startswith("branch "):
            current.branch = line.removeprefix("branch refs/heads/")
        elif line.startswith("locked"):
            current.locked = True
        elif line.startswith("prunable"):
            current.prunable = True
        elif line == "":
            worktrees.append(current)
            current = None

    return worktrees


def resolve_trunk(repo: Path) -> str:
    graphite_trunk = run(["gt", "trunk", "--no-interactive"], repo, check=False)
    if graphite_trunk.returncode == 0 and graphite_trunk.stdout.strip():
        return graphite_trunk.stdout.strip().splitlines()[-1].strip()

    origin_head = run(["git", "symbolic-ref", "--short", "refs/remotes/origin/HEAD"], repo, check=False)
    if origin_head.returncode == 0:
        return origin_head.stdout.strip().removeprefix("origin/")

    return "main"


def find_pr(repo: Path, branch: str) -> dict | None:
    output = run(
        [
            "gh", "pr", "list",
            "--head", branch,
            "--state", "all",
            "--limit", "20",
            "--json", "number,state,headRefOid,isCrossRepository,url",
        ],
        repo,
    ).stdout
    prs = [pr for pr in json.loads(output) if not pr["isCrossRepository"]]

    open_prs = [pr for pr in prs if pr["state"] == "OPEN"]
    if open_prs:
        return open_prs[0]

    return max(prs, key=lambda pr: pr["number"], default=None)


def has_pr_head(repo: Path, pr: dict) -> bool:
    if git_succeeds(repo, "cat-file", "-e", f"{pr['headRefOid']}^{{commit}}"):
        return True

    git_succeeds(repo, "fetch", "--quiet", "origin", f"pull/{pr['number']}/head")
    return git_succeeds(repo, "cat-file", "-e", f"{pr['headRefOid']}^{{commit}}")


def plan_branch(repo: Path, name: str, sha: str, pr: dict | None) -> BranchPlan:
    plan = BranchPlan(name=name, sha=sha, pr=pr)

    if pr is None:
        plan.keep_reason = "no pull request"
    elif pr["state"] == "OPEN":
        plan.keep_reason = f"PR #{pr['number']} is open"
    elif not has_pr_head(repo, pr):
        plan.keep_reason = f"could not fetch PR #{pr['number']}'s head to verify nothing is lost"
    elif not git_succeeds(repo, "merge-base", "--is-ancestor", sha, pr["headRefOid"]):
        plan.keep_reason = f"has local commits that are not in PR #{pr['number']}"

    return plan


def is_clean(path: Path, include_untracked: bool = True) -> bool:
    untracked = "all" if include_untracked else "no"
    return git(path, "status", "--porcelain", f"--untracked-files={untracked}") == ""


def is_inside(path: Path, directory: Path) -> bool:
    return path == directory or directory in path.parents


def build_plan(repo: Path, invoking_dir: Path) -> Plan:
    trunk = resolve_trunk(repo)
    git_succeeds(repo, "fetch", "--quiet", "--prune", "origin")

    local_branches = dict(
        line.split("\0")
        for line in git(repo, "for-each-ref", "refs/heads", "--format=%(refname:short)%00%(objectname)").splitlines()
    )
    candidates = {name: sha for name, sha in local_branches.items() if name != trunk}

    with ThreadPoolExecutor(max_workers=8) as pool:
        prs = dict(zip(candidates, pool.map(lambda name: find_pr(repo, name), candidates)))
    branches = {name: plan_branch(repo, name, sha, prs[name]) for name, sha in candidates.items()}

    main_checkout, *linked_worktrees = list_worktrees(repo)
    trunk_ref = f"origin/{trunk}" if git_succeeds(repo, "rev-parse", "--verify", "--quiet", f"origin/{trunk}") else trunk

    remove_worktrees: list[Worktree] = []
    kept_worktrees: list[tuple[Worktree, str]] = []
    stale_worktrees: list[Worktree] = []

    for worktree in linked_worktrees:
        if worktree.prunable:
            stale_worktrees.append(worktree)
            continue

        branch_plan = branches.get(worktree.branch) if worktree.branch else None
        reason = None

        if worktree.locked:
            reason = "locked"
        elif is_inside(invoking_dir, worktree.path):
            reason = "the cleanup was started from inside it"
        elif worktree.branch is None:
            if not git_succeeds(repo, "merge-base", "--is-ancestor", worktree.head, trunk_ref):
                reason = f"detached HEAD has commits that are not on {trunk}"
        elif branch_plan is None:
            reason = f"on {worktree.branch}"
        elif not branch_plan.deletable:
            reason = f"{worktree.branch}: {branch_plan.keep_reason}"

        if reason is None and not is_clean(worktree.path):
            reason = "has uncommitted or untracked changes"

        if reason is None:
            remove_worktrees.append(worktree)
            continue

        kept_worktrees.append((worktree, reason))
        if branch_plan and branch_plan.deletable:
            branch_plan.keep_reason = f"checked out in kept worktree {worktree.path}"

    switch_main_checkout_from = None
    main_branch_plan = branches.get(main_checkout.branch) if main_checkout.branch else None
    if main_branch_plan and main_branch_plan.deletable:
        if is_clean(main_checkout.path, include_untracked=False):
            switch_main_checkout_from = main_checkout.branch
        else:
            main_branch_plan.keep_reason = "checked out in the main checkout, which has uncommitted changes"

    return Plan(
        repo=repo,
        trunk=trunk,
        branches=branches,
        remove_worktrees=remove_worktrees,
        kept_worktrees=kept_worktrees,
        stale_worktrees=stale_worktrees,
        switch_main_checkout_from=switch_main_checkout_from,
    )


def worktree_label(plan: Plan, worktree: Worktree) -> str:
    if worktree.branch is None:
        return f"{worktree.path}  [detached at {worktree.head[:10]}, already on {plan.trunk}]"
    return f"{worktree.path}  [{worktree.branch}, {plan.branches[worktree.branch].pr_label}]"


def print_plan(plan: Plan) -> None:
    deletable = [branch for branch in plan.branches.values() if branch.deletable]
    kept = [branch for branch in plan.branches.values() if not branch.deletable]

    print(f"Repository: {plan.repo}  (trunk: {plan.trunk})\n")

    print("Worktrees to remove:")
    for worktree in plan.remove_worktrees:
        print(f"  {worktree_label(plan, worktree)}")
    if not plan.remove_worktrees:
        print("  none")

    print("\nBranches to delete:")
    for branch in deletable:
        print(f"  {branch.name}  {branch.pr_label}  {branch.pr['url']}  (tip {branch.sha[:10]})")
    if not deletable:
        print("  none")

    if plan.switch_main_checkout_from:
        print(f"\nMain checkout: switch from {plan.switch_main_checkout_from} to {plan.trunk}")
    if plan.stale_worktrees:
        print(f"\nStale worktree entries to prune (directory missing): {len(plan.stale_worktrees)}")
        for worktree in plan.stale_worktrees:
            print(f"  {worktree.path}")

    print("\nKept:")
    for worktree, reason in plan.kept_worktrees:
        print(f"  worktree {worktree.path} — {reason}")
    for branch in kept:
        print(f"  branch {branch.name} — {branch.keep_reason}")
    if not plan.kept_worktrees and not kept:
        print("  nothing")


def delete_branch(repo: Path, name: str) -> subprocess.CompletedProcess:
    result = run(["gt", "delete", name, "--force", "--no-interactive"], repo, check=False)
    if result.returncode != 0 and "untracked branch" in combined_output(result):
        return run(["git", "branch", "-D", name], repo, check=False)
    return result


def apply_plan(plan: Plan) -> int:
    failures = 0
    print("\nApplying:")

    for worktree in plan.remove_worktrees:
        result = run(["git", "worktree", "remove", str(worktree.path)], plan.repo, check=False)
        if result.returncode == 0:
            print(f"  removed worktree {worktree.path}")
            continue

        failures += 1
        print(f"  FAILED to remove worktree {worktree.path}: {combined_output(result)}")
        if worktree.branch:
            plan.branches[worktree.branch].keep_reason = "its worktree could not be removed"

    if plan.switch_main_checkout_from:
        result = run(["gt", "checkout", plan.trunk, "--no-interactive"], plan.repo, check=False)
        if result.returncode == 0:
            print(f"  switched main checkout to {plan.trunk}")
        else:
            failures += 1
            print(f"  FAILED to switch main checkout to {plan.trunk}: {combined_output(result)}")
            plan.branches[plan.switch_main_checkout_from].keep_reason = "main checkout could not switch away"

    for branch in [branch for branch in plan.branches.values() if branch.deletable]:
        result = delete_branch(plan.repo, branch.name)
        if result.returncode == 0:
            print(f"  deleted {branch.name} (was {branch.sha[:10]}; {branch.pr_label})")
        else:
            failures += 1
            print(f"  FAILED to delete {branch.name}: {combined_output(result)}")

    if plan.stale_worktrees:
        git(plan.repo, "worktree", "prune")
        print(f"  pruned {len(plan.stale_worktrees)} stale worktree entries")

    sync = run(["gt", "sync", "--no-interactive"], plan.repo, check=False)
    print("\ngt sync --no-interactive:")
    print("  " + combined_output(sync).replace("\n", "\n  "))
    if sync.returncode != 0:
        failures += 1

    return 1 if failures else 0


def resolve_main_checkout(path: Path) -> Path:
    if not path.is_dir():
        raise SystemExit(f"{path} is not a directory")

    common_dir = Path(git(path, "rev-parse", "--path-format=absolute", "--git-common-dir"))
    return list_worktrees(common_dir)[0].path


def prune_repo(repo: Path, invoking_dir: Path, apply: bool) -> int:
    run(["gh", "auth", "status"], repo)
    run(["gt", "--version"], repo)

    plan = build_plan(repo, invoking_dir)
    print_plan(plan)

    if not apply:
        print("\nPreview only. Re-run with --apply to make these changes.")
        return 0

    return apply_plan(plan)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("repos", nargs="+", type=Path, help="One or more checkouts (main checkout or any worktree)")
    parser.add_argument("--apply", action="store_true", help="Make the changes; default is preview only")
    args = parser.parse_args()

    invoking_dir = Path.cwd().resolve()
    repos = list(dict.fromkeys(resolve_main_checkout(path.expanduser().resolve()) for path in args.repos))

    exit_code = 0
    for index, repo in enumerate(repos):
        if index:
            print("\n" + "=" * 72 + "\n")
        exit_code |= prune_repo(repo, invoking_dir, args.apply)

    return exit_code


if __name__ == "__main__":
    raise SystemExit(main())
