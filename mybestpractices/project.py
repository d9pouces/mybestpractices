"""Discover some project metadata."""
import pathlib

try:
    import tomllib
except ImportError:
    tomllib = None
    import toml

from setuptools.config import read_configuration


def get_main_metadata(path: pathlib.Path):
    """Get project name and version from the source path.

    >>> get_main_metadata(pathlib.Path(__file__).parent.parent)[0]
    'allbestpractices'

    :param path:
    :return:
    """
    name, version = None, None
    if (path / "setup.cfg").is_file():
        config = read_configuration(path / "setup.cfg")
        # config["license"]
        # config['classifiers']
        # 'License :: OSI Approved :: CEA CNRS Inr[...]on 2.1 (CeCILL-2.1)'
        # 'Programming Language :: Python :: 3.10'
        name = config.get("metadata").get("name")
        version = config.get("metadata", {}).get("version")
    if (path / "pyproject.toml").is_file():
        if tomllib is not None:
            with open(path / "pyproject.toml", "rb") as fd:
                data = tomllib.load(fd)
        else:
            with open(path / "pyproject.toml") as fd:
                data = toml.load(fd)
        if version is None:
            version = data.get("project", {}).get("version")
        if name is None:
            name = data.get("project", {}).get("name")
        if version is None:
            version = data.get("tool", {}).get("poetry", {}).get("version")
        if name is None:
            name = data.get("tool", {}).get("poetry", {}).get("name")
        # bs = data['build-system']['build-backend']
        # module = importlib.import_module(bs)
    return name, version
