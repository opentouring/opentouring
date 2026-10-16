#!/usr/bin/env bash
# SPDX-License-Identifier: Apache-2.0
# Checks text files against the writing rules in AGENTS.md.
# Usage: tools/check-writing.sh FILE... (exits 1 on any finding)
set -u
status=0
banned='\b(delve|dive in|deep dive|unpack|navigate|foster|leverage|harness|unlock|elevate|streamline|robust|seamless|cutting-edge|game-changer|holistic|tapestry|landscape|ecosystem|boasts|arguably)\b'
american='\b(organization|organizations|color|colors|optimize|optimized|optimization|behavior|behaviors|center|centers|analyze|analyzed|catalog)\b'
for file in "$@"; do
  [ -f "$file" ] || continue
  case "$file" in
    LICENSES/*|AGENTS.md|tools/check-writing.sh|package-lock.json) continue ;;
  esac
  grep -Iq . "$file" || continue
  if grep -nE $'\xe2\x80\x94|\xe2\x80\x93' "$file"; then echo "  ^ $file: em or en dash" >&2; status=1; fi
  if grep -niE "$banned" "$file"; then echo "  ^ $file: banned word (see AGENTS.md)" >&2; status=1; fi
  case "$file" in
    *.md|*.yaml|*.yml)
      if grep -nE "$american" "$file" | grep -v -E '`[^`]*`|https?://' | grep -viE "\"[^\"]*$american[^\"]*\""; then echo "  ^ $file: American spelling (use Australian)" >&2; status=1; fi ;;
  esac
done
exit $status
