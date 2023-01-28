"""Check if required pre-commit hooks are actually checked."""
import pathlib
import sys
from collections import defaultdict
from typing import Dict, Tuple

try:
    from yaml import CLoader as Loader
    from yaml import load
except ImportError:
    from yaml import Loader, load


def main():
    """Check if all required precommit hooks are configured."""
    requirements = pathlib.Path(__file__).parent / "pre-commit-hooks.yaml"
    check_requirements(requirements)


def check_requirements(requirements):
    """Check against a requirement file."""
    expected_hooks = read_hooks(requirements)
    actual_hooks = read_hooks(".pre-commit-config.yaml")
    by_repo_url = defaultdict(lambda: [])
    for (key, hook_data) in sorted(expected_hooks.items()):
        repo_url, hook_id = key
        if (repo_url, hook_id) in actual_hooks:
            continue
        by_repo_url[repo_url].append(hook_data)
    if by_repo_url:
        print("Please add the following hooks to .pre-commit-config.yaml and run")
        print("`pre-commit autoupdate`:")
        for (repo_url, hooks) in sorted(by_repo_url.items()):
            print(f"""-   repo: {repo_url}\n    rev: 0.0.0\n    hooks:""")
            for hook_data in hooks:
                c = "-"
                for k, v in hook_data.items():
                    print(f"    {c}   {k}: {v}")
                    c = " "
        sys.exit(1)


def read_hooks(filename):
    """Fetch the list of defined hooks."""
    with open(filename) as fd:
        actual = load(fd, Loader=Loader)
    actual_hooks: Dict[Tuple[str, str], Dict] = {}
    for repo_data in actual["repos"]:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            actual_hooks[(repo_url, hook_id)] = hook_data
    return actual_hooks


if __name__ == "__main__":
    main()
