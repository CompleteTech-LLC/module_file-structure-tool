"""
Generate File Reports
---------------------
This script provides commands (functions) to enumerate all files known to the
FileStructureTool, collect their names and contents, and generate comprehensive
reports.

Usage Example (CLI):
--------------------
    python -m file_structure_tool.reports.generate_reports

Functionalities:
----------------
1) List all files along with their full paths and contents.
2) Generate a single README-like file summarizing the entire module.
3) Print or save this data to output files as desired.

Implementation Details:
-----------------------
- Relies on the `FileStructureTool` to read the existing file structure JSON.
- Iterates through directories and files to retrieve contents from disk.
- Merges them into a unified Markdown report.

NOTE:
-----
- Assumes files exist on disk matching the structure in the JSON representation.
- Error handling is minimal for demonstration purposes.
"""

import os
from typing import List, Tuple, Optional

from file_structure_tool.tools.file_structure_tool import FileStructureTool
from file_structure_tool.models.directory import Directory
from file_structure_tool.models.file import File
from file_structure_tool.utils.logger import get_logger

logger = get_logger(__name__)

def _collect_files_and_contents(path_prefix: str, directory: Directory) -> List[Tuple[str, str]]:
    """
    Recursively collect all files from the given directory along with their contents.

    :param path_prefix: The accumulated path leading to the current directory.
    :param directory:   The Directory instance to explore.
    :return: A list of (filepath, file_contents) tuples.
    """
    results = []
    # Collect file contents
    for filename, file_obj in directory.files.items():
        full_path = os.path.join(path_prefix, directory.name, filename)
        # Attempt to read file from disk if it actually exists
        try:
            with open(full_path, "r", encoding="utf-8") as f:
                contents = f.read()
            results.append((full_path, contents))
        except FileNotFoundError:
            logger.warning(f"File not found on disk: {full_path}")
            results.append((full_path, "<FILE NOT FOUND ON DISK>"))
        except Exception as e:
            logger.error(f"Could not read file '{full_path}': {e}")
            results.append((full_path, f"<ERROR: {e}>"))

    # Recurse into subdirectories
    for subdir_name, subdir_obj in directory.directories.items():
        results.extend(_collect_files_and_contents(
            os.path.join(path_prefix, directory.name),
            subdir_obj
        ))

    return results

def generate_full_report(json_directory: Optional[str] = None) -> str:
    """
    Generate a comprehensive report of all files (including contents) in the
    current FileStructure.

    :param json_directory: Path where the 'file_structure.json' is stored.
                           Defaults to an absolute path to the 'json_files' folder.
    :return: A Markdown-formatted string containing file paths and contents.
    """
    if not json_directory:
        base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
        json_directory = os.path.join(base_dir, "json_files")

    # Initialize the FileStructureTool
    tool = FileStructureTool(json_directory=json_directory)

    markdown_lines = [
        "# Comprehensive File Report",
        "",
        "Below is a list of files (with their absolute or combined paths) and their contents,",
        "as tracked by the current FileStructure."
    ]

    if not tool.file_structure.directories:
        markdown_lines.append("\n*(No directories found in the FileStructure.)*")
        return "\n".join(markdown_lines)

    # Iterate over each top-level directory
    for dirname, directory_obj in tool.file_structure.list_directories().items():
        markdown_lines.append(f"\n## Directory: `{dirname}`\n")

        # Collect files
        file_tuples = _collect_files_and_contents("", directory_obj)
        if not file_tuples:
            markdown_lines.append("*No files found in this directory.*")
            continue

        for (fp, content) in file_tuples:
            markdown_lines.append(f"### `{fp}`")
            markdown_lines.append("```")
            markdown_lines.append(content)
            markdown_lines.append("```\n")

    return "\n".join(markdown_lines)

def main():
    """
    CLI entry-point for generating a comprehensive file report.
    """
    # Define absolute path to the project’s root directory (optional override)
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    default_json_directory = os.path.join(base_dir, "json_files")

    report = generate_full_report(json_directory=default_json_directory)

    # Print to stdout
    print(report)

    # Optionally, write to a file
    output_file = "full_report.md"
    try:
        with open(output_file, "w", encoding="utf-8") as f:
            f.write(report)
        logger.info(f"Comprehensive file report written to '{output_file}'.")
    except Exception as e:
        logger.error(f"Failed to write the report to '{output_file}': {e}")

if __name__ == "__main__":
    main()
