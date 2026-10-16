#!/bin/bash
# SPDX-License-Identifier: Apache-2.0
# Claude Code PreToolUse hook: blocks destructive git commands before they run.
# Adapted from Matt Pocock's git-guardrails skill. Pushing a feature branch is
# allowed, because agents open pull requests. Force pushes, pushes to main,
# discarding work and skipping hooks are blocked.

COMMAND=$(jq -r '.tool_input.command // ""')

block() {
  echo "BLOCKED: '$COMMAND' matches '$1'. This repository does not allow agents to do this. Ask the maintainer." >&2
  exit 2
}

grep -qE 'git[^|;&]*push[^|;&]*(--force|-f( |$)|--force-with-lease|--mirror|--delete|-d( |$))' <<<"$COMMAND" && block "force, mirror or delete push"
grep -qE 'git[^|;&]*push[^|;&]*( |:|/)(main|HEAD:main)( |$)' <<<"$COMMAND" && block "push to main"
grep -qE 'git[^|;&]*reset[^|;&]*--hard' <<<"$COMMAND" && block "reset --hard"
grep -qE 'git[^|;&]*clean[^|;&]*-[a-zA-Z]*f' <<<"$COMMAND" && block "clean -f"
grep -qE 'git[^|;&]*branch[^|;&]*-D' <<<"$COMMAND" && block "branch -D"
grep -qE 'git[^|;&]*(checkout|restore)[^|;&]* \.( |$)' <<<"$COMMAND" && block "checkout or restore of the whole tree"
grep -qE 'git[^|;&]*(commit|push)[^|;&]*--no-verify' <<<"$COMMAND" && block "--no-verify"
grep -qE 'git[^|;&]*stash[^|;&]*(drop|clear)' <<<"$COMMAND" && block "stash drop or clear"
exit 0
