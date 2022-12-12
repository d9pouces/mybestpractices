"""Check if required pre-commit hooks are actually checked."""
import sys
from collections import defaultdict
from importlib.resources import open_text
from typing import Set, Tuple

try:
    from yaml import CLoader as Loader
    from yaml import load
except ImportError:
    from yaml import Loader, load


def required_precommit_hooks():
    """Check if all required precommit hooks are used."""
    with open_text("mybestpractices", "pre-commit-hooks.yaml") as fd:
        expected = load(fd, Loader=Loader)
    expected_hooks: Set[Tuple[str, str]] = set()
    for repo_data in expected["repos"]:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            expected_hooks.add((repo_url, hook_id))
    with open(".pre-commit-config.yaml") as fd:
        actual = load(fd, Loader=Loader)
    actual_hooks: Set[Tuple[str, str]] = set()
    for repo_data in actual["repos"]:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            actual_hooks.add((repo_url, hook_id))
    by_repo_url = defaultdict(lambda: [])
    for (repo_url, hook_id) in sorted(expected_hooks):
        if (repo_url, hook_id) in actual_hooks:
            continue
        by_repo_url[repo_url].append(hook_id)
    if not by_repo_url:
        return
    print("Please add the following hooks to .pre-commit-config.yaml and run")
    print("`pre-commit autoupdate`:")
    for (repo_url, hook_ids) in sorted(by_repo_url.items()):
        print(f"""-   repo: {repo_url}\n    rev: 0.0.0\n    hooks:""")
        for hook_id in hook_ids:
            print(f"    -   id: {hook_id}")
    sys.exit(1)


if __name__ == "__main__":
    required_precommit_hooks()
