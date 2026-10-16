#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Runs the JSON Schema validator, and the formatting check on its Python code,
# in a local virtual environment (.tools/venv). The environment is rebuilt
# from schema/tools/requirements.txt whenever that file changes.
set -euo pipefail
root=$(git rev-parse --show-toplevel)
venv="$root/.tools/venv"
requirements="$root/schema/tools/requirements.txt"
stamp="$venv/requirements.installed"
if [ ! -x "$venv/bin/python" ]; then
  python3 -m venv "$venv"
fi
if ! cmp -s "$requirements" "$stamp"; then
  "$venv/bin/pip" install -q --disable-pip-version-check -r "$requirements"
  cp "$requirements" "$stamp"
fi
"$venv/bin/ruff" format --check "$root/schema/tools"
exec "$venv/bin/python" "$root/schema/tools/validate.py"
