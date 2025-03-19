import os
import yaml
import json
import joblib
from box import ConfigBox
from pathlib import Path
from typing import Any
from ensure import ensure_annotations
from box.exceptions import BoxValueError
from src.mlproject import logger


@ensure_annotations
def read_yaml(path_to_yaml: Path) -> ConfigBox:
    """Reads a YAML file and returns the content as a ConfigBox.

    Args:
        path_to_yaml (Path): Path to the YAML file.

    Raises:
        ValueError: If the YAML file is empty or could not be loaded.
        e: Other exceptions raised by yaml.safe_load or file I/O.

    Returns:
        ConfigBox: Parsed YAML data as ConfigBox.
    """
    try:
        with open(path_to_yaml) as yaml_file:
            content = yaml.safe_load(yaml_file)
            if content is None:
                raise ValueError("YAML file is empty")
            logger.info(f"YAML file: {path_to_yaml} loaded successfully")
            return ConfigBox(content)
    except Exception as e:
        logger.error(f"Failed to load YAML file: {path_to_yaml}. Error: {e}")
        raise e


@ensure_annotations
def create_directories(path_to_directories: list, verbose=True):
    """Creates directories for the given list of paths.

    Args:
        path_to_directories (list): List of directory paths to create.
        verbose (bool, optional): If True, logs the directory creation. Defaults to True.
    """
    for path in path_to_directories:
        os.makedirs(path, exist_ok=True)
        if verbose:
            logger.info(f"Created directory at: {path}")


@ensure_annotations
def save_json(path: Path, data: dict):
    """Saves data as a JSON file.

    Args:
        path (Path): Path to save the JSON file.
        data (dict): Data to be saved in the JSON file.
    """
    try:
        with open(path, "w") as f:
            json.dump(data, f, indent=4)
        logger.info(f"JSON file saved at: {path}")
    except Exception as e:
        logger.error(f"Failed to save JSON file at: {path}. Error: {e}")
        raise e


@ensure_annotations
def load_json(path: Path) -> ConfigBox:
    """Loads data from a JSON file.

    Args:
        path (Path): Path to the JSON file.

    Returns:
        ConfigBox: Data as class attributes, not a plain dictionary.
    """
    try:
        with open(path) as f:
            content = json.load(f)
        logger.info(f"JSON file loaded successfully from: {path}")
        return ConfigBox(content)
    except Exception as e:
        logger.error(f"Failed to load JSON file from: {path}. Error: {e}")
        raise e


@ensure_annotations
def save_bin(data: Any, path: Path):
    """Saves data as a binary file.

    Args:
        data (Any): Data to be saved as a binary file.
        path (Path): Path to save the binary file.
    """
    try:
        joblib.dump(value=data, filename=path)
        logger.info(f"Binary file saved at: {path}")
    except Exception as e:
        logger.error(f"Failed to save binary file at: {path}. Error: {e}")
        raise e


@ensure_annotations
def load_bin(path: Path) -> Any:
    """Loads data from a binary file.

    Args:
        path (Path): Path to the binary file.

    Returns:
        Any: Object stored in the binary file.
    """
    try:
        data = joblib.load(path)
        logger.info(f"Binary file loaded from: {path}")
        return data
    except Exception as e:
        logger.error(f"Failed to load binary file from: {path}. Error: {e}")
        raise e


@ensure_annotations
def get_size(path: Path) -> str:
    """Gets the size of a file in KB.

    Args:
        path (Path): Path of the file.

    Returns:
        str: Size of the file in KB (rounded).
    """
    try:
        size_in_kb = round(os.path.getsize(path) / 1024)
        return f"~ {size_in_kb} KB"
    except Exception as e:
        logger.error(f"Failed to get size of the file at: {path}. Error: {e}")
        raise e
