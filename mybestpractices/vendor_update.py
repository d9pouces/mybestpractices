"""Run an external script on each commit."""
import argparse
import pathlib
import subprocess  # nosec
from typing import Optional


def main():
    """Run the update script."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--script", default="tools/update_third_party.sh")


def vendor_update(
    update_script: Optional[str] = "tools/update_third_party.sh",
):
    """Run the script that updates third-party components on each commit."""
    if update_script is None:
        return
    path = pathlib.Path(update_script)
    if not path.exists():
        return
    subprocess.check_call([path.resolve()], shell=True)  # nosec


if __name__ == "__main__":
    main()
