# Below is an example "setup.py" that you would place in your project's root directory
# (the same directory that contains the "file_structure_tool" folder).
# It provides enough fields to perform basic packaging and distribution.

from setuptools import setup, find_packages

setup(
    name="file_structure_tool",
    version="0.1.0",
    packages=find_packages(),
    description="A Python-based utility for managing an in-memory filesystem structure",
    long_description=open("README.md", "r", encoding="utf-8").read(),
    long_description_content_type="text/markdown",
    author="Timothy Gregg",
    author_email="Timothy.Greggl@complete.tech",
    license="MIT",
    python_requires=">=3.7",
    install_requires=[],  # Add any runtime dependencies here
)

# Explanation:
# 1. Place this file (setup.py) at the top level of your project, e.g.:
#    .
#    ├── file_structure_tool/
#    ├── README.md
#    ├── setup.py   <--- Goes here
#    └── ...
#
# 2. This is a minimal setup file. Adjust fields (name, author, etc.) as needed.
# 3. To build and upload:
#      python setup.py sdist bdist_wheel
#      twine upload dist/*
