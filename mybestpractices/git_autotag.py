"""Precommit hook that add new git tags, as required."""
import pathlib
import subprocess

from mybestpractices.project import get_main_metadata


def git_autotag():
    """Add a new git tag, if required."""
    path = pathlib.Path(".").resolve()
    if not (path / ".git").is_dir():
        return
    name, version = get_main_metadata(path)
    if version is None:
        return
    cmd = ["git", "tag", "-l"]
    content = subprocess.check_output(cmd, cwd=path, encoding="utf-8")
    tags = {x.strip() for x in content.splitlines()}
    if version not in tags:
        try:
            subprocess.check_output(["git", "tag", version], cwd=path)
        except subprocess.SubprocessError:
            pass
