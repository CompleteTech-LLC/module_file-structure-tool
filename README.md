# File Structure Tool

A Python-based utility for managing an in-memory filesystem structure, complete with JSON-based persistence, directory/file operations, and logging.

## Features
- Directory & File Management: Create, delete, find directories and files in a hierarchical structure.
- JSON Persistence: Save and load the in-memory structure to/from disk using JSON.
- Logging: Comprehensive logging for all operations, configurable verbosity.
- Example Scripts: Demonstrates how to build and manipulate the file structure, then generate reports.

## Installation
1. Clone or copy the `file_structure_tool` directory into your project.
2. Install dependencies, if any, with:

    pip install -r requirements.txt

   (If a `requirements.txt` is provided.)

## Usage
1. **Initialize/Modify the Structure**:

    python -m file_structure_tool.main

2. **Generate a Full Report**:

    python -m file_structure_tool.reports.generate_reports

## Directory Layout
```bash
file_structure_tool/
├── __init__.py
├── main.py
├── models/
│   ├── __init__.py
│   ├── base.py
│   ├── directory.py
│   ├── file.py
│   └── file_structure.py
├── services/
│   ├── __init__.py
│   └── json_crud.py
├── tools/
│   ├── __init__.py
│   └── file_structure_tool.py
├── utils/
│   ├── __init__.py
│   ├── decorators.py
│   └── logger.py
├── reports/
│   └── generate_reports.py
└── docs/
    └── report_of_files.md
```
## Logging Configuration
- Adjust logging levels in `file_structure_tool/utils/logger.py`.
- Or set the environment variable `FILE_STRUCTURE_LOG_LEVEL` to `DEBUG`, `INFO`, `WARNING`, or `ERROR`:

    FILE_STRUCTURE_LOG_LEVEL=WARNING python -m file_structure_tool.main

## License
This tool is provided under an open license of your choice. Please see `LICENSE` for details.
