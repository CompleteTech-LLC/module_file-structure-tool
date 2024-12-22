# file_structure_tool/models/file.py
"""
File Model
----------
Represents an individual file within a directory.

Naming Conventions:
- Class: File (CamelCase).
- Methods: from_dict / to_dict for consistent (de)serialization.
"""

from dataclasses import dataclass
from typing import Dict, Any
from .base import Serializable

@dataclass
class File(Serializable):
    """
    File
    ----
    Minimal representation of a file, storing only its 'name'.
    """
    name: str

    def to_dict(self) -> Dict[str, Any]:
        return {"name": self.name}

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> "File":
        return cls(name=data["name"])
