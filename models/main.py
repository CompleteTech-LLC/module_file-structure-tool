# file_structure_tool/main.py
import logger
"""
Main Script to Demonstrate FileStructureTool Usage
"""

import os
from file_structure_tool.models.file import File
from file_structure_tool.models.directory import Directory
from file_structure_tool.models.file_structure import FileStructure
from file_structure_tool.tools.file_structure_tool import FileStructureTool


def setup_initial_structure(tool: FileStructureTool):
    """
    Set up the initial file structure based on the inferred structure.
    """
    # Create 'f:/langchain_project/' directory
    langchain_project = Directory(name="f:/langchain_project")
    langchain_project.add_file(File(name="env.py"))
    langchain_project.add_file(File(name="toolkit.py"))
    langchain_project.add_file(File(name="workflow.py"))
    langchain_project.add_file(File(name="__init__.py"))

    # Create 'langchain/' subdirectory within 'f:/langchain_project/'
    langchain_subdir = Directory(name="langchain")
    langchain_subdir.add_file(File(name="load_env.py"))
    langchain_project.add_directory(langchain_subdir)

    # Create 'tests/' subdirectory within 'f:/langchain_project/'
    tests_subdir = Directory(name="tests")
    tests_subdir.add_file(File(name="test_agents.py"))
    tests_subdir.add_file(File(name="test_managers.py"))
    tests_subdir.add_file(File(name="test_team.py"))
    tests_subdir.add_file(File(name="test_toolkit.py"))
    tests_subdir.add_file(File(name="test_tools.py"))
    langchain_project.add_directory(tests_subdir)

    # Add 'f:/langchain_project/' to the file structure
    tool.file_structure.add_directory(langchain_project)

    # Similarly, create 'f:/langchain/' directory
    langchain_root = Directory(name="f:/langchain")

    # Create 'langchain_/' subdirectory
    langchain_ = Directory(name="langchain_")
    langchain_.add_file(File(name="toolkit.py"))
    langchain_.add_file(File(name="workflow.py"))
    langchain_.add_file(File(name="__init__.py"))
    langchain_root.add_directory(langchain_)

    # Create 'langchain/' subdirectory
    langchain = Directory(name="langchain")
    langchain.add_file(File(name="toolkit.py"))
    langchain.add_file(File(name="workflow.py"))
    langchain.add_file(File(name="__init__.py"))
    langchain_root.add_directory(langchain)

    # Add 'f:/langchain/' to the file structure
    tool.file_structure.add_directory(langchain_root)

    # Save the initial structure
    tool.save()
    logger.info("Initial file structure setup completed.")


def main():
    # Define the directory where JSON files will be stored
    json_directory = "json_files"

    # Initialize the FileStructureTool
    tool = FileStructureTool(json_directory=json_directory)

    # Check if the file structure is empty; if so, set up the initial structure
    if not tool.file_structure.directories:
        setup_initial_structure(tool)
    else:
        logger.info("File structure already exists. Skipping initial setup.")

    # Display the current file structure
    logger.info("\nCurrent File Structure:")
    tool.display_structure()

    # Example: Add a new directory
    try:
        new_dir = Directory(name="new_directory")
        tool.add_directory(path="f:/langchain_project/langchain", directory=new_dir)
    except ValueError as ve:
        logger.error(ve)

    # Example: Add a new file
    try:
        new_file = File(name="new_file.py")
        tool.add_file(path="f:/langchain_project/langchain/new_directory", file=new_file)
    except ValueError as ve:
        logger.error(ve)

    # Display the updated file structure
    logger.info("\nUpdated File Structure:")
    tool.display_structure()

    # Example: Find a directory
    found_dir = tool.file_structure.find_directory("f:/langchain_project")
    if found_dir:
        logger.info(f"Found directory: {found_dir}")

    # Example: Remove a directory
    try:
        tool.remove_directory("f:/langchain")
    except KeyError as ke:
        logger.error(ke)

    # Display the final file structure
    logger.info("\nFinal File Structure:")
    tool.display_structure()


if __name__ == "__main__":
    main()
