"""Utils for writing / reading files.
"""
from enum import Enum, auto


class FileSourceType(Enum):
    """Enumerator class for types of file sources.
    """
    local = auto()
    aws = auto()
    gce = auto()


#pylint: disable=unused-argument
def read_config_file(file_name, file_source=FileSourceType.local):
    """Reads a config file.

    Args:
        file_name: a name of the file to read.
        file_source: where the file is stored

    Returns:
        config dictionary that was read from the file.
    """

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
