# file_structure_tool/models/directory.py

"""
Directory Model
---------------
Represents a directory (folder), which may contain subdirectories
and files. It supports nested operations such as finding/adding/
removing both files and subdirectories.

Naming Conventions:
- Class: Directory (CamelCase).
- Methods: snake_case, describing actions (find_directory, add_file, etc.).
"""

from dataclasses import dataclass, field
from typing import Dict, List, Optional, Any
import json

from file_structure_tool.models.file import File
from file_structure_tool.utils.logger import get_logger
from .base import Serializable

logger = get_logger(__name__)

@dataclass
class Directory(Serializable):
    """
    Directory
    ---------
    Holds zero or more files and subdirectories. Allows basic filesystem-like operations.
    """
    name: str
    files: Dict[str, File] = field(default_factory=dict)
    directories: Dict[str, "Directory"] = field(default_factory=dict)

    def add_directory(self, directory: "Directory") -> None:
        """
        Add a subdirectory, ensuring no duplication. Raises ValueError if
        a directory of the same name already exists.
        """
        if directory.name in self.directories:
            logger.error(f"Subdirectory '{directory.name}' already exists.")
            raise ValueError(f"Subdirectory '{directory.name}' already exists.")
        self.directories[directory.name] = directory
        logger.info(f"Added subdirectory '{directory.name}' to directory '{self.name}'.")

    def remove_directory(self, directory_name: str) -> None:
        """
        Remove a subdirectory by name. Raises KeyError if the subdirectory
        does not exist.
        """
        if directory_name not in self.directories:
            logger.error(f"Subdirectory '{directory_name}' not found in '{self.name}'.")
            raise KeyError(f"Subdirectory '{directory_name}' not found in '{self.name}'.")
        del self.directories[directory_name]
        logger.info(f"Removed subdirectory '{directory_name}' from directory '{self.name}'.")

    def find_directory(self, directory_name: str) -> Optional["Directory"]:
        """
        Return a subdirectory by name, or None if not found.
        """
        return self.directories.get(directory_name, None)

    def add_file(self, file: File) -> None:
        """
        Add a file to the directory. Raises ValueError if a file with the same name
        already exists.
        """
        if file.name in self.files:
            logger.error(f"File '{file.name}' already exists in directory '{self.name}'.")
            raise ValueError(f"File '{file.name}' already exists in directory '{self.name}'.")
        self.files[file.name] = file
        logger.info(f"Added file '{file.name}' to directory '{self.name}'.")

    def remove_file(self, filename: str) -> None:
        """
        Remove a file by name. Raises KeyError if the file does not exist.
        """
        if filename not in self.files:
            logger.error(f"File '{filename}' not found in directory '{self.name}'.")
            raise KeyError(f"File '{filename}' not found in '{self.name}'.")
        del self.files[filename]
        logger.info(f"Removed file '{filename}' from directory '{self.name}'.")

    def find_file(self, filename: str) -> Optional[File]:
        """
        Return a file by name, or None if not found.
        """
        return self.files.get(filename, None)

    def to_dict(self) -> Dict[str, Any]:
        """
        Serialize this directory into a dictionary, including files and subdirectories.
        """
        return {
            "files": [file_obj.to_dict() for file_obj in self.files.values()],
            "directories": {
                dir_name: dir_obj.to_dict() for dir_name, dir_obj in self.directories.items()
            }
        }

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "Directory":
        """
        Create a Directory from a dictionary representation. 'name' must be set manually
        by the caller after initialization, if needed, since JSON doesn't store it.
        """
        # Typically, you'd require the 'name' from outside or store it in 'data'
        new_dir = cls(name="")  # name can be assigned later
        files_data = data.get("files", [])
        for file_info in files_data:
            file_obj = File.from_dict(file_info)
            new_dir.add_file(file_obj)

        directories_data = data.get("directories", {})
        for sub_dir_name, sub_dir_info in directories_data.items():
            sub_dir = cls.from_dict(sub_dir_info)
            sub_dir.name = sub_dir_name
            new_dir.directories[sub_dir_name] = sub_dir

        return new_dir
