#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# commit-msg hook: every commit needs a Developer Certificate of Origin sign-off.
if ! grep -qE '^Signed-off-by: .+ <.+>' "$1"; then
  echo "Missing DCO sign-off. Commit with: git commit -s" >&2
  exit 1
fi
