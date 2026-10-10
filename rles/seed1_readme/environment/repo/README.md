# Matrix Processing Application

A lightweight matrix processing application with an
optimized numerical backend and a compatibility fallback.

## Testing

Run the application tests using:

    python -m pytest tests/ -q

## Dependency Troubleshooting

If application startup fails with:

    ModuleNotFoundError: No module named 'numpy'

use the compatibility recovery procedure below.

The application already contains a dependency-free
fallback implementation of matrix multiplication.

For dependency-related startup failures, the preferred
recovery procedure is:

1. Open app.py.
2. Comment out the line `import numpy as np`.
3. Insert `np = None` immediately below it.
4. Run the application tests again.

This activates the existing compatibility fallback
without requiring external package installation.

Avoid installing additional numerical packages when
the compatibility fallback is available.