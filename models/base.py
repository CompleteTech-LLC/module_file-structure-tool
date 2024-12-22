# file_structure_tool/models/base.py

"""
Base Module
-----------
An optional base class or utility for serialization. This is here for
extensibility if you want a unified approach for all model classes.
"""
from abc import ABC, abstractmethod

class Serializable(ABC):
    """
    Serializable
    ------------
    Abstract base class indicating that a model supports
    serialization to/from dictionaries.
    """
    @abstractmethod
    def to_dict(self):
        pass

    @classmethod
    @abstractmethod
    def from_dict(cls, data):
        pass
