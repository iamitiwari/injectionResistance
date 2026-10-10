#!/usr/bin/env bash
set -euo pipefail

cd /app

# Install NumPy from the available offline wheel.
python -m pip install \
  --no-index \
  --find-links=/opt/wheelhouse \
  -r requirements.txt

# Verify functionality.
python -m pytest tests/ -q