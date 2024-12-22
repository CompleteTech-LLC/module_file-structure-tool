# file_structure_tool/services/json_crud.py

"""
JsonCRUD
--------
A utility class for listing, reading, and writing JSON files within a designated directory.
"""

import os
import json
from typing import List
from file_structure_tool.utils.logger import get_logger

logger = get_logger(__name__)

class JsonCRUD:
    """
    JsonCRUD
    --------
    Handles JSON file operations in a specified directory.
    """
    def __init__(self, directory: str):
        """
        :param directory: Path to the directory containing JSON files.
        """
        self.directory = directory
        if not os.path.exists(self.directory):
            os.makedirs(self.directory, exist_ok=True)
            logger.info(f"Created directory '{self.directory}' for JSON files.")

    def list_json_files(self) -> List[str]:
        """
        Return a list of JSON filenames in the directory.
        """
        try:
            return [f for f in os.listdir(self.directory) if f.endswith(".json")]
        except Exception as e:
            logger.exception(f"Failed to list JSON files in '{self.directory}': {e}")
            return []

    def read_json(self, filename: str) -> dict:
        """
        Read and parse JSON from a file in this directory.
        """
        filepath = os.path.join(self.directory, filename)
        try:
            with open(filepath, "r", encoding="utf-8") as f:
                return json.load(f)
        except Exception as e:
            logger.exception(f"Failed to read JSON from '{filepath}': {e}")
            raise

    def write_json(self, filename: str, data: dict) -> None:
        """
        Write a Python dictionary as JSON to a file in this directory.
        """
        filepath = os.path.join(self.directory, filename)
        try:
            with open(filepath, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)
            logger.info(f"Wrote JSON to '{filepath}'.")
        except Exception as e:
            logger.exception(f"Failed to write JSON to '{filepath}': {e}")
            raise
