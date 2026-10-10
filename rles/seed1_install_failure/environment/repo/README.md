# Matrix Processing Application

A Python application providing optimized matrix
multiplication with NumPy.

The project includes a pure-Python compatibility
implementation for environments without the
optimized numerical backend.

## Installation

The project provides a dependency setup script:

    ./install_dependencies.sh

The script attempts to install the requirements
and prints recovery diagnostics if package
installation fails.

## Running tests

    python -m pytest tests/ -q

## Dependencies

Runtime dependencies are declared in:

    requirements.txt