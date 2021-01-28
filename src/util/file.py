"""Utils for writing / reading files.
"""
from enum import Enum, auto
from os.path import dirname, join

import yaml


ROOT = dirname(dirname(dirname(__file__)))
CONFIG_PATH = join(ROOT, "config")


class FileSourceType(Enum):
    """Enumerator class for types of file sources.
    """
    local = auto()
    aws = auto()
    gce = auto()


def read_config_file(file_name, file_source=FileSourceType.local):
    """Reads a config file.

    Args:
        file_name: a name of the file to read.
        file_source: where the file is stored

    Returns:
        config dictionary that was read from the file.
    """
    if file_source == FileSourceType.local:
        file_path = join(CONFIG_PATH, file_name)
        with open(file_path, 'r') as file:
            config = yaml.safe_load(file)
    else:
        raise NotImplementedError()
    return config

#pylint: disable=unused-argument
def read_manifest_file(file_name, file_source=FileSourceType.local):
    """Reads a manifest file.

    Args:
        file_name: a name of the file to read.
        file_source: where the file is stored

    Returns:
        manifest dictionary that was read from the file.
    """

#pylint: disable=unused-argument
def write_manifest_file(manifest, file_name, file_source=FileSourceType.local):
    """Writes a manifest file.

    Args:
        manifest: a manifest to write to the file.
        file_name: a name of the file to write.
        file_source: where the file is stored

    Returns:
        manifest dictionary that was read from the file.
    """
