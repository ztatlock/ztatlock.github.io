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

# ENSURE pub fields complete
for field in 'TITLE' 'AUTHOR' 'CONF' 'YEAR'; do
  grep "$field" pub-*.dj \
  && error "ERROR: found incomplete pub field '$field'!"
done

# ensure meta fields complete
for field in 'DESCRIPTION' 'URL' 'TITLE' 'IMAGE'; do
  grep "$field" *.meta \
  && error "ERROR: found incomplete meta field '$field'!"
done

# warn about TODO pub fields
for field in 'TODO'; do
  grep "$field" pub-*.dj \
  && echo "WARNING: found incomplete pub field '$field'!"
done
