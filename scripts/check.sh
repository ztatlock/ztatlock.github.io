#!/usr/bin/env bash

set -euo pipefail

trap 'handle_err $LINENO' ERR

function handle_err {
  error "Error occurred near line $1"
}

function error {
  echo "$1" 2>&1
  exit 1
}

function cleanup {
  if [ -n "${scratch_dir:-}" ] && [ -d "$scratch_dir" ]; then
    rm -rf "$scratch_dir"
  fi
}

repo_root="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
scratch_dir="$(mktemp -d "${TMPDIR:-/tmp}/ztatlock-check.XXXXXX")"
trap cleanup EXIT

cd "$repo_root" || exit

draft_pages=()
while IFS= read -r src; do
  [ -n "$src" ] || continue
  draft_pages+=("$src")
done < <(rg -l '^# DRAFT$' *.dj 2>/dev/null || true)

for src in "${draft_pages[@]}"; do
  html="${src%.dj}.html"
  if git ls-files --error-unmatch "$html" >/dev/null 2>&1; then
    error "ERROR: tracked draft output $html should not be committed"
  fi
done

rsync -a \
  --exclude '.git/' \
  --exclude 'state/' \
  "$repo_root/" "$scratch_dir/"

cd "$scratch_dir" || exit

generated_html=()
for src in *.dj; do
  generated_html+=("${src%.dj}.html")
done
rm -f "${generated_html[@]}" sitemap.txt sitemap.xml

make all >/dev/null

for src in "${draft_pages[@]}"; do
  html="${src%.dj}.html"
  if [ -e "$html" ]; then
    error "ERROR: draft page $html was built by make all"
  fi
  if rg -q "https://ztatlock.net/$html" sitemap.txt sitemap.xml; then
    error "ERROR: draft page $html is listed in the sitemap"
  fi
done

python3 scripts/validate_site.py --root .
