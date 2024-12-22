# file_structure_tool/models/file_structure.py

"""
FileStructure Model
-------------------
Represents an entire filesystem-like structure in memory. This data model is
primarily used by the DirectoryManagerTool to reflect and persist changes.

Naming Conventions & Best Practices:
- Class name: FileStructure (CamelCase for a data model).
- Methods: snake_case (in line with Python norms).
- Logging: consistent, minimal usage to track major actions and errors.

Primary Responsibilities:
-------------------------
1) Hold a mapping of top-level directories.
2) Provide methods to add, remove, or find directories.
3) Support serialization to/from a dictionary or JSON for persistence.

Related Modules:
---------------
- Directory (models.directory) : Describes a folder with subdirectories and files.
- File (models.file)           : Describes an individual file entity.
- JsonCRUD (services.json_crud): For reading/writing JSON files.
- Logger (utils.logger)        : For consistent logging.
- DirectoryManagerTool         : Higher-level tool that manipulates FileStructure objects.

Example:
--------
    file_structure = FileStructure()
    file_structure.add_directory(Directory(name="root"))
    # Convert to dict or JSON, save, etc.

"""

from __future__ import annotations
import json
from dataclasses import dataclass, field
from typing import Dict, Optional, Any
from file_structure_tool.models.directory import Directory
from file_structure_tool.utils.logger import get_logger

@dataclass
class FileStructure:
    """
    FileStructure
    -------------
    In-memory representation of a filesystem structure, storing top-level directories
    in a dictionary keyed by their names.
    """
    directories: Dict[str, Directory] = field(default_factory=dict)

    # Use the logger for consistent logs across methods
    logger = get_logger(__name__)

    def add_directory(self, directory: Directory) -> None:
        """
        Adds a top-level directory to the file structure. Raises ValueError if
        a directory with the same name already exists.
        """
        if directory.name in self.directories:
            self.logger.error(f"Top-level directory '{directory.name}' already exists.")
            raise ValueError(f"Top-level directory '{directory.name}' already exists.")
        self.directories[directory.name] = directory
        self.logger.info(f"Added top-level directory '{directory.name}'.")

    def remove_directory(self, directory_name: str) -> None:
        """
        Removes a top-level directory by name. Raises KeyError if the directory
        does not exist.
        """
        if directory_name not in self.directories:
            self.logger.error(f"Top-level directory '{directory_name}' not found.")
            raise KeyError(f"Top-level directory '{directory_name}' not found.")
        del self.directories[directory_name]
        self.logger.info(f"Removed top-level directory '{directory_name}'.")

    def find_directory(self, directory_name: str) -> Optional[Directory]:
        """
        Retrieves a top-level directory by name. Returns None if not found.
        """
        directory = self.directories.get(directory_name)
        if directory:
            self.logger.info(f"Top-level directory '{directory_name}' found.")
        else:
            self.logger.warning(f"Top-level directory '{directory_name}' not found.")
        return directory

    def list_directories(self) -> Dict[str, Directory]:
        """
        Returns a dictionary of all top-level directories in the structure.
        """
        self.logger.info("Listing all top-level directories.")
        return self.directories

    def get_directory_by_path(self, path: str) -> Optional[Directory]:
        """
        Retrieves a directory by its full path (e.g., "f:/langchain_project/langchain").
        Returns None if the path cannot be resolved.
        """
        parts = path.strip("/").split("/")
        if not parts or not parts[0]:
            self.logger.warning("Empty or invalid path provided.")
            return None

        # Start at top-level
        current_dir = self.directories.get(parts[0])
        if not current_dir:
            self.logger.warning(f"Root directory '{parts[0]}' not found.")
            return None

        # Traverse deeper
        for sub_name in parts[1:]:
            current_dir = current_dir.find_directory(sub_name)
            if not current_dir:
                self.logger.warning(f"Subdirectory '{sub_name}' not found in path '{path}'.")
                return None

        self.logger.info(f"Path '{path}' resolved to directory '{current_dir.name}'.")
        return current_dir

    def to_dict(self) -> Dict[str, Any]:
        """
        Serializes the entire file structure to a Python dictionary.
        """
        return {
            dir_name: directory.to_dict()
            for dir_name, directory in self.directories.items()
        }

    def to_json(self, filepath: str) -> None:
        """
        Serializes the file structure to JSON and writes it to the given filepath.
        """
        try:
            with open(filepath, 'w', encoding='utf-8') as f:
                json.dump(self.to_dict(), f, indent=4)
            self.logger.info(f"Serialized file structure to '{filepath}'.")
        except Exception as e:
            self.logger.exception(f"Failed to serialize file structure to '{filepath}': {e}")
            raise

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> FileStructure:
        """
        Deserializes a FileStructure from a Python dictionary.
        """
        fs = cls()
        for dir_name, dir_data in data.items():
            directory_obj = Directory.from_dict(dir_data)
            fs.directories[dir_name] = directory_obj
            cls.logger.debug(f"Deserialized directory '{dir_name}' from data.")
        cls.logger.info("Created FileStructure from dictionary.")
        return fs

    @classmethod
    def from_json(cls, filepath: str) -> FileStructure:
        """
        Deserializes a FileStructure from JSON stored at filepath.
        """
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            fs = cls.from_dict(data)
            cls.logger.info(f"Deserialized file structure from '{filepath}'.")
            return fs
        except FileNotFoundError:
            cls.logger.error(f"JSON file '{filepath}' not found.")
            raise
        except json.JSONDecodeError as e:
            cls.logger.exception(f"Invalid JSON format in '{filepath}': {e}")
            raise
        except Exception as e:
            cls.logger.exception(f"Failed to deserialize from '{filepath}': {e}")
            raise

    def __repr__(self) -> str:
        """
        Returns a string representation of the FileStructure, in JSON format if possible.
        """
        try:
            return json.dumps(self.to_dict(), indent=4)
        except Exception as e:
            self.logger.exception(f"Failed to generate JSON repr for FileStructure: {e}")
            return super().__repr__()
