"""Check if required pre-commit hooks are actually checked."""
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
    for repo_data in expected:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            expected_hooks.add((repo_url, hook_id))
    with open(".pre-commit-config.yaml") as fd:
        actual = load(fd, Loader=Loader)
    actual_hooks: Set[Tuple[str, str]] = set()
    for repo_data in actual:
        repo_url = repo_data["repo"]
        for hook_data in repo_data["hooks"]:
            hook_id = hook_data["id"]
            actual_hooks.add((repo_url, hook_id))
    for (repo_url, hook_id) in sorted(expected_hooks):
        if (repo_url, hook_id) in actual_hooks:
            continue
        c = f"""-   repo: {repo_url}\n    hooks:\n    -   id: {hook_id}\n"""
        print("Please add the following hook to .pre-commit-config.yaml:")
        print(c)
