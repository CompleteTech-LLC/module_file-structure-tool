# file_structure_tool/utils/decorators.py
"""
Decorators Module
-----------------
Houses optional decorators used across the file_structure_tool suite.
Example: require_directory_and_save for DirectoryManagerTool (if not defined inline).
"""

from functools import wraps
from typing import Callable, Any

def require_directory_and_save(func: Callable) -> Callable:
    """
    Ensures a directory path is valid before proceeding, then auto-saves changes.
    Typically used in DirectoryManagerTool methods for adding/removing files/directories.
    """
    @wraps(func)
    def wrapper(self, path: str, *args, **kwargs) -> Any:
        target_dir = self.file_structure.get_directory_by_path(path)
        if not target_dir:
            self.logger.error(f"Directory not found for path: '{path}'.")
            raise ValueError(f"Directory not found for path: '{path}'.")
        result = func(self, target_dir, *args, **kwargs)
        self.save()
        return result
    return wrapper
