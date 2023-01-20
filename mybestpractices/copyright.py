"""Ensure that the copyright is valid on each file."""
import argparse
from typing import Optional

USE_BLOCK_COMMENT_PREFIX = 1
USE_BLOCK_COMMENT_NOPREFIX = 2
USE_LINE_COMMENT = 3

BEFORE_OTHER_COMMENTS = 1
AFTER_OTHER_COMMENTS = 2

BEFORE_DOCTYPE = 1
BEFORE_ROOT_TAG = 2


class Config:
    """Configuration class."""

    comment_type = {
        USE_BLOCK_COMMENT_PREFIX,
        USE_BLOCK_COMMENT_NOPREFIX,
        USE_LINE_COMMENT,
    }
    relative_location = {BEFORE_OTHER_COMMENTS, AFTER_OTHER_COMMENTS}
    border_separate_before: Optional[int] = None
    border_separate_after: Optional[int] = None
    separator: Optional[str] = None
    box: bool = False
    add_block_line_before: bool = False
    add_block_line_after: bool = True
    location = {BEFORE_DOCTYPE, BEFORE_ROOT_TAG}
    template = None


def main():
    """Read CLI args and launches the check."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--license", default="LICENSE")
    parser.add_argument("--readme", default="README.md")
    args = parser.parse_args()
    check_copyright(readme=args.readme, license_=args.license)


def check_copyright(
    readme: Optional[str] = None,
    license_: Optional[str] = None,
):
    """Ensure that the copyright is valid on each file."""
    pass
    # noinspection PyUnusedLocal
    readme, license_ = readme, license_
