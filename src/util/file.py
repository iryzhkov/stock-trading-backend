"""Utils for writing / reading files.
"""
from enum import Enum, auto
from os.path import dirname, join, exists

import json
import pandas as pd
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
def read_manifest_file(file_path, file_source=FileSourceType.local):
    """Reads a manifest file.

    Args:
        file_path: a path to the manifest file.
        file_source: where the file is stored

    Returns:
        manifest dictionary that was read from the file.
    """
    if file_source == FileSourceType.local:
        file_path = join(ROOT, file_path)
        if exists(file_path):
            with open(file_path, 'r') as file:
                manifest = json.loads(file.read())
        else:
            manifest = {}
    else:
        raise NotImplementedError()
    return manifest

#pylint: disable=unused-argument
def write_manifest_file(manifest, file_path, file_source=FileSourceType.local):
    """Writes a manifest file.

    Args:
        manifest: a manifest to write to the file.
        file_path: a path for the file to write.
        file_source: where the file is stored.
    """
    if file_source == FileSourceType.local:
        file_path = join(ROOT, file_path)
        with open(file_path, 'w') as file:
            file.write(json.dumps(manifest, indent=2))
    else:
        raise NotImplementedError()

#pylint: disable=unused-argument
def read_csv_file(file_path, file_source=FileSourceType.local):
    """Reads a csv file.

    Args:
        file_path: a path to the manifest file.
        file_source: where the file is stored

    Returns:
        Pandas DataFrame with the contents of the file.
    """
    if file_source == FileSourceType.local:
        file_path = join(ROOT, file_path)
        data_frame = pd.read_csv(file_path, index_col=0)
    else:
        raise NotImplementedError()
    return data_frame

#pylint: disable=unused-argument
def write_csv_file(data_frame, file_path, file_source=FileSourceType.local):
    """Writes a csv file.

    Args:
        data_frame: a data_frame to write to the file.
        file_path: a path for the file to write.
        file_source: where the file is stored.
    """
    if file_source == FileSourceType.local:
        file_path = join(ROOT, file_path)
        data_frame.to_csv(file_path)
    else:
        raise NotImplementedError()
