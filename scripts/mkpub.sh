#!/usr/bin/env bash

set -e

trap 'handle_err $LINENO' ERR

function handle_err {
  error "Error occurred near line $1"
}

function error {
  echo "$1" >&2
  exit 1
}

# go to repo root
cd "$(dirname "${BASH_SOURCE[0]}")/.." || exit

# check and get args
if [ $# -ne 1 ] || [ -z "$1" ]; then
  error "Usage: $0 YEAR-CONF-SYS"
fi
ycf="$1"

python3 -m scripts.scaffold_publication --root . --slug "${ycf}"
