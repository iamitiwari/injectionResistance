#!/usr/bin/env bash
set -euo pipefail

mkdir -p /logs/verifier

cd /app

python /tests/grader.py