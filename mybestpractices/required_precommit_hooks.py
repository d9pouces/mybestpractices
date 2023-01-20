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


def main():
    """Check if all required precommit hooks are configured."""
    with open_text("mybestpractices", "pre-commit-hooks.yaml") as fd:
        expected_hooks = read_hooks(fd)
    with open(".pre-commit-config.yaml") as fd:
        actual_hooks = read_hooks(fd)
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


def read_hooks(fd):
    """Fetch the list of defined hooks."""
    actual = load(fd, Loader=Loader)
    actual_hooks: Set[Tuple[str, str]] = set()
    for repo_data in actual["repos"]:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            actual_hooks.add((repo_url, hook_id))
    return actual_hooks


if __name__ == "__main__":
    main()
