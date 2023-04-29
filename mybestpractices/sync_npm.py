"""Ensure that package.json has the same version as the Python package."""
import argparse
import json
import pathlib

from mybestpractices.project import get_main_metadata


def main(args=None):
    """Ensure that package.json has the same version as the Python package."""
    parser = argparse.ArgumentParser(
        description="Automatically add the project version as a git tag."
    )
    parser.add_argument(
        "--path",
        "-p",
        help="Path to the `package.json` (default to './package.json').",
        default=pathlib.Path("./package.json"),
        type=pathlib.Path,
    )
    args = parser.parse_args(args=args)
    path = pathlib.Path(".").resolve()
    name, version = get_main_metadata(path)
    package_path: pathlib.Path = args.path
    if version is None:
        print(f"Unavailable to get current project version from {path}.")
        return
    elif not package_path.is_file():
        print(f"{package_path} is not a JSON file.")
        return
    with open(package_path) as fd:
        content = json.load(fd)
    content["version"] = version
    with open(package_path, "w") as fd:
        json.dump(content, fd, indent=2)


if __name__ == "__main__":
    main()
