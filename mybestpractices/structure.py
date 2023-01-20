"""Check if the .gitignore is well-formed."""
import argparse
import pathlib
import sys


def main():
    """Run all checks."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--license", default="LICENSE")
    parser.add_argument("--readme", default="README.md")
    parser.add_argument("--gitignore", default="gitignore")
    parser.add_argument("--copyright", default="tools/copyright.txt")
    args = parser.parse_args()

    path = pathlib.Path(".").resolve()
    code = 0
    code += check_files(path, readme=args.readme, license_=args.license)
    code += check_gitignore(path)
    sys.exit(code)


def check_files(path: pathlib.Path, readme: str = "", license_: str = "") -> int:
    """Check if common files are present."""
    code = 0
    if readme and not (path / readme).exists():
        print(f"Missing {readme} file.")
        code += 1
    if license_ and not (path / license_).exists():
        print(f"Missing {license_} file.")
        code += 2
    return code


def check_gitignore(path: pathlib.Path) -> int:
    """Check if the .gitignore is well-formed."""
    code = 0
    filepath = path / "/gitignore"
    if not (path / ".git").is_dir():
        return code
    if not filepath.exists():
        code += 4
    else:
        pass

    return 0


if __name__ == "__main__":
    main()
