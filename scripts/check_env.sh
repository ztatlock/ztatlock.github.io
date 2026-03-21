#!/usr/bin/env bash

set -euo pipefail

trap 'handle_err $LINENO' ERR

function handle_err {
  printf 'ERROR: unexpected failure near line %s\n' "$1" >&2
  exit 1
}

function cleanup {
  if [ -n "${tmpdir:-}" ] && [ -d "$tmpdir" ]; then
    rm -rf "$tmpdir"
  fi
}

function ok {
  printf 'OK   : %s\n' "$1"
}

function warn {
  printf 'WARN : %s\n' "$1"
  warnings=$((warnings + 1))
}

function fail {
  printf 'FAIL : %s\n' "$1" >&2
  failures=$((failures + 1))
}

function check_required_command {
  local name="$1"
  if command -v "$name" >/dev/null 2>&1; then
    ok "found required command '$name'"
  else
    fail "missing required command '$name'"
  fi
}

function check_optional_command {
  local name="$1"
  local purpose="$2"
  if command -v "$name" >/dev/null 2>&1; then
    ok "found optional command '$name' for ${purpose}"
  else
    warn "missing optional command '$name' for ${purpose}"
  fi
}

trap cleanup EXIT

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$repo_root" || exit

tmpdir="$(mktemp -d "${TMPDIR:-/tmp}/ztatlock-env.XXXXXX")"
failures=0
warnings=0

for cmd in bash make python3 git djot rg rsync; do
  check_required_command "$cmd"
done

check_optional_command "wget" "make index-now"

printf '\n'
if [ "$failures" -gt 0 ]; then
  printf 'Environment check failed with %s required issue(s) and %s warning(s).\n' \
    "$failures" "$warnings" >&2
  exit 1
fi

if [ "$warnings" -gt 0 ]; then
  printf 'Environment check passed with %s warning(s).\n' "$warnings"
else
  printf 'Environment check passed with no warnings.\n'
fi
