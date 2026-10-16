#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Runs the JSON Schema validator in a local virtual environment (.tools/venv).
set -euo pipefail
root=$(git rev-parse --show-toplevel)
venv="$root/.tools/venv"
if [ ! -x "$venv/bin/python" ]; then
  python3 -m venv "$venv"
  "$venv/bin/pip" install -q -r "$root/schema/tools/requirements.txt"
fi
exec "$venv/bin/python" "$root/schema/tools/validate.py"
