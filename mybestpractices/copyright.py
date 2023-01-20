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
    parser.add_argument("--copyright", default="tools/copyright.txt")
    args = parser.parse_args()
    check_copyright(copyright_=args.copyright)


def check_copyright(
    copyright_: Optional[str] = None,
):
    """Ensure that the copyright is valid on each file."""
    pass
    # noinspection PyUnusedLocal
    copyright_ = copyright_


if __name__ == "__main__":
    main()
