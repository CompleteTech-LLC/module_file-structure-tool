# file_structure_tool/tools/file_structure_tool.py

import os, logger
from typing import Optional
from file_structure_tool.models.file import File
from file_structure_tool.models.directory import Directory
from file_structure_tool.models.file_structure import FileStructure
from file_structure_tool.services.json_crud import JsonCRUD


class FileStructureTool:
    """
    A tool to manage the file structure with CRUD operations on JSON representations.
    """

    def __init__(self, json_directory: str):
        """
        Initialize the FileStructureTool.

        :param json_directory: Directory where the JSON file representing the file structure is stored.
        """
        self.json_crud = JsonCRUD(directory=json_directory)
        self.file_structure: Optional[FileStructure] = None
        self.json_filename = "file_structure.json"

        # Load existing file structure if it exists
        if self.json_filename in self.json_crud.list_json_files():
            self.file_structure = FileStructure.from_json(os.path.join(json_directory, self.json_filename))
            print("Loaded existing file structure.")
        else:
            self.file_structure = FileStructure()
            self.save()
            print("Initialized new file structure.")

    def save(self) -> None:
        """
        Save the current file structure to the JSON file.
        """
        if self.file_structure:
            # Use the write_json method instead of create_json/update_json
            # (Since those do not exist in JsonCRUD)
            self.json_crud.write_json(self.json_filename, self.file_structure.to_dict())
            print("File structure saved.")
        else:
            print("No file structure to save.")

    def load(self) -> None:
        """
        Load the file structure from the JSON file.
        """
        data = self.json_crud.read_json(self.json_filename)
        if data:
            self.file_structure = FileStructure.from_dict(data)
            print("File structure loaded successfully.")
        else:
            print("No existing file structure found.")

    def add_directory(self, path: str, directory: Directory) -> None:
        """
        Add a directory to the file structure at the specified path.

        :param path: Path where the directory should be added (e.g., 'f:/langchain_project/langchain').
        :param directory: Directory instance to add.
        """
        parts = path.strip("/").split("/")
        current_dirs = self.file_structure.directories
        current_dir = None
        for part in parts:
            if part in current_dirs:
                current_dir = current_dirs[part]
                current_dirs = current_dir.directories
            else:
                print(f"Path '{path}' does not exist.")
                return
        if current_dir:
            current_dir.add_directory(directory)
            self.save()
            print(f"Added directory '{directory.name}' at path '{path}'.")
        else:
            print(f"Directory '{path}' not found.")

    def add_file(self, path: str, file: File) -> None:
        """
        Add a file to the file structure at the specified path.

        :param path: Path where the file should be added (e.g., 'f:/langchain_project/langchain').
        :param file: File instance to add.
        """
        parts = path.strip("/").split("/")
        current_dirs = self.file_structure.directories
        current_dir = None
        for part in parts:
            if part in current_dirs:
                current_dir = current_dirs[part]
                current_dirs = current_dir.directories
            else:
                print(f"Path '{path}' does not exist.")
                return
        if current_dir:
            current_dir.add_file(file)
            self.save()
            print(f"Added file '{file.name}' at path '{path}'.")
        else:
            print(f"Directory '{path}' not found.")

    def delete_file(self, path: str, filename: str) -> None:
        """
        Delete a file from the file structure at the specified path.

        :param path: Path where the file is located (e.g., 'f:/langchain_project/langchain').
        :param filename: Name of the file to delete.
        """
        parts = path.strip("/").split("/")
        current_dirs = self.file_structure.directories
        current_dir = None
        for part in parts:
            if part in current_dirs:
                current_dir = current_dirs[part]
                current_dirs = current_dir.directories
            else:
                print(f"Path '{path}' does not exist.")
                return
        if current_dir:
            file_to_remove = next((f for f in current_dir.files if f.name == filename), None)
            if file_to_remove:
                current_dir.files.remove(file_to_remove)
                self.save()
                print(f"Deleted file '{filename}' from path '{path}'.")
            else:
                print(f"File '{filename}' not found in path '{path}'.")
        else:
            print(f"Directory '{path}' not found.")

    def delete_directory(self, path: str, directory_name: str) -> None:
        """
        Delete a directory from the file structure at the specified path.

        :param path: Path where the directory is located (e.g., 'f:/langchain_project').
        :param directory_name: Name of the directory to delete.
        """
        parts = path.strip("/").split("/")
        current_dirs = self.file_structure.directories
        current_dir = None
        for part in parts:
            if part in current_dirs:
                current_dir = current_dirs[part]
                current_dirs = current_dir.directories
            else:
                print(f"Path '{path}' does not exist.")
                return
        if current_dir:
            if directory_name in current_dir.directories:
                del current_dir.directories[directory_name]
                self.save()
                print(f"Deleted directory '{directory_name}' from path '{path}'.")
            else:
                print(f"Directory '{directory_name}' not found in path '{path}'.")
        else:
            print(f"Directory '{path}' not found.")

    def display_structure(self):
        """
        Display the current file structure.
        """
        print(self.file_structure)
