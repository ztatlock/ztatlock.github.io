#!/usr/bin/env bash

set -e

trap 'handle_err $LINENO' ERR

function handle_err {
  error "Error occurred near line $1"
}

function error {
  echo "$1" 2>&1
  exit 1
}

# go to repo root
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit

DOM="https://ztatlock.net"
KEY="9ca38421ba63499eaa1e9c16bfe7be4c"

# construct url update request
function index-now-url {
  echo "https://www.bing.com/indexnow?url=${DOM}/${1}&key=${KEY}"
}

PREV="templates/index-now-prev.txt"
LOG="templates/index-now-log.txt"

# get previous run date
prev="$(cat "$PREV")"

# submit any updated pages
for page in *.html pubs/*/*.pdf; do
  mod="$(git log -1 --pretty='format:%cs' "$page")"
  if [ "$prev" \< "$mod" ]; then
    echo "SUBMIT : $page" | tee -a "$LOG"
    wget -a "$LOG" -O /dev/null "$(index-now-url "$page")"
    echo >> "$LOG"
    printf "=%.0s" $(seq 80) >> "$LOG"
    echo >> "$LOG"
  fi
done

# save this run date to avoid dupes
date +%Y-%m-%d > "$PREV"
