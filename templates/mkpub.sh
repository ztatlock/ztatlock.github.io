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

# check and get args
if [ $# -ne 1 ] || [ -z "$1" ]; then
  error "Usage: $0 YEAR-CONF-SYS"
fi
ycf="$1"

# set up pub template and files dir
cp templates/pub.dj "pub-${ycf}.dj"
sed -i '' "s/YEAR-CONF-SYS/${ycf}/g" "pub-${ycf}.dj"
mkdir "pubs/${ycf}"
