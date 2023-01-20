"""Ensure that the copyright is valid on each file."""
import argparse
import datetime
import os
import pathlib
from typing import Optional

from mybestpractices.project import get_main_metadata

USE_BLOCK_COMMENT_PREFIX = 1
USE_BLOCK_COMMENT_NOPREFIX = 2
USE_LINE_COMMENT = 3

BEFORE_OTHER_COMMENTS = 1
AFTER_OTHER_COMMENTS = 2

BEFORE_DOCTYPE = 1
BEFORE_ROOT_TAG = 2


class DateInfo:
    """A DateInfo object."""

    def __init__(self, dt: datetime.datetime):
        """Mimic DateInfo object from PyCharm."""
        self.year = dt.year
        self.month = dt.month
        self.day = dt.day
        self.hour = dt.hour % 12
        self.hour24 = dt.hour
        self.minute = dt.minute
        self.second = dt.second


def get_default_variables(root: pathlib.Path):
    """Return variables that are common to all files."""
    today = datetime.datetime.now()
    name, __ = get_main_metadata(root)
    return {
        "today": DateInfo(today),
        "username": os.getlogin(),
        "project": {"name": name},
    }


def get_file_variables(root: pathlib.Path, file_: pathlib.Path):
    """Return variables that are file-specific."""
    stats = file_.stat()
    last_modified = datetime.datetime.fromtimestamp(stats.st_mtime)
    rel_path = str(file_.resolve().relative_to(root.resolve()))
    class_comp = rel_path.rpartition(".")[0].split(os.path.sep)

    file_data = {
        "fileName": file_.name,
        "pathName": str(file_.resolve()),
        "className": file_.name.partition(".")[0],
        "lastModified": DateInfo(last_modified),
        "qualifiedClassName": ".".join(class_comp),
    }
    module_data = {"name": ".".join(class_comp[:-1])}
    return {"file": file_data, "module": module_data}


class Config:
    """Configuration class."""

    def __init__(
        self,
        block_start="/*",
        block_middle=" ",
        block_end="*/",
        line_start="//",
        line_end="",
    ):
        """Initialize the class."""
        self.block_start = block_start
        self.block_middle = block_middle
        self.block_end = block_end
        self.line_start = line_start
        self.line_end = line_end
        self.comment_type = USE_BLOCK_COMMENT_PREFIX
        self.relative_location = BEFORE_OTHER_COMMENTS
        self.border_separate_before = 80
        self.border_separate_after = 80
        self.separator: Optional[str] = None
        self.box: bool = False
        self.add_block_line_before: bool = False
        self.add_block_line_after: bool = True
        self.location = {BEFORE_DOCTYPE, BEFORE_ROOT_TAG}
        self.default_config = None


filetypes = {
    "css": Config("/*", " ", "*/", "/*", "*/"),
    "html": Config("<!--", " ", "-->", "<!--", "-->"),
}


def main():
    """Read CLI args and launches the check."""
    parser = argparse.ArgumentParser()
    parser.add_argument("--regexp", default="Copyright")
    parser.add_argument("--copyright", default="tools/copyright.txt")
    parser.add_argument("--comment-type")
    parser.add_argument("--relative-location")
    parser.add_argument("--border-separate-before")
    parser.add_argument("--border-separate-after")
    parser.add_argument("--separator")
    parser.add_argument("--box")
    parser.add_argument("--add-block-line-before")
    parser.add_argument("--add-block-line-after")
    parser.add_argument("--location")
    parser.add_argument("files", nargs="*")

    args = parser.parse_args()
    check_copyright(copyright_=args.copyright)
    root = pathlib.Path(".")
    default_variables = get_default_variables(root)
    print(default_variables)


def check_copyright(
    copyright_: Optional[str] = None,
):
    """Ensure that the copyright is valid on each file."""
    # noinspection PyUnusedLocal
    copyright_ = copyright_


if __name__ == "__main__":
    main()
