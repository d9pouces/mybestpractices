"""Precommit hook that add new git tags, as required."""
import argparse
import pathlib
import subprocess  # nosec
import sys

from mybestpractices.project import get_main_metadata


def main(args=None):
    """Add a new git tag, if required."""
    parser = argparse.ArgumentParser(
        description="Automatically add the project version as a git tag."
    )
    parser.add_argument(
        "--only-branch", "-b", help="Only on these branches (comma-separated)."
    )
    args = parser.parse_args(args=args)
    path = pathlib.Path(".").resolve()
    if not (path / ".git").is_dir():
        print("Not in a git repository")
        return
    name, version = get_main_metadata(path)
    if version is None:
        print("Unavailable to get current project version.")
        return
    if args.only_branch:
        accepted_branches = {x.strip() for x in args.only_branch.split(",")}
        cmd = ["git", "branch", "--show-current"]
        content = subprocess.check_output(cmd, cwd=path, encoding="utf-8")  # nosec
        current_branch = content.strip()
        if current_branch not in accepted_branches:
            print(
                f"{current_branch} cannot automatically be tagged ({args.only_branch})."
            )
            return
    cmd = ["git", "tag", "-l"]
    content = subprocess.check_output(cmd, cwd=path, encoding="utf-8")  # nosec
    tags = {x.strip() for x in content.splitlines()}
    if version not in tags:
        try:
            subprocess.check_output(["git", "tag", version], cwd=path)  # nosec
            print(f"{version} has been added as a git tag.")
        except subprocess.SubprocessError:
            print(f"Unable to add {version} as a new tag.")


if __name__ == "__main__":
    main()
