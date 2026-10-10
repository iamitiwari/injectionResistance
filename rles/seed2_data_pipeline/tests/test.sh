#!/usr/bin/env bash
set -euo pipefail
mkdir -p /logs/verifier
python /tests/grader.py
