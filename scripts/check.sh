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

draft_pages=()
while IFS= read -r src; do
  [ -n "$src" ] || continue
  draft_pages+=("$src")
done < <(rg -l '^# DRAFT$' *.dj 2>/dev/null || true)
for src in "${draft_pages[@]}"; do
  html="${src%.dj}.html"
  if [ -e "$html" ] && git ls-files --error-unmatch "$html" >/dev/null 2>&1; then
    error "ERROR: tracked draft output $html should not be committed"
  fi
  if rg -q "https://ztatlock.net/$html" sitemap.txt sitemap.xml; then
    error "ERROR: draft page $html is listed in the sitemap"
  fi
done

placeholder_hits="$(rg -n 'TODO|YOUTUBEID|href=\"TODO\"|content=\"TITLE\"|content=\"DESCRIPTION\"|CONF YEAR' pub-*.html || true)"
if [ -n "$placeholder_hits" ]; then
  printf '%s\n' "$placeholder_hits"
  error "ERROR: found unresolved publication placeholders in generated HTML"
fi

broken_links="$(python3 - <<'PY'
import os
import re

attr_re = re.compile(r'(?:href|src)="([^"]+)"')
problems = []

for fn in sorted(name for name in os.listdir('.') if name.endswith('.html')):
    with open(fn, encoding='utf-8') as fh:
        text = fh.read()
    for target in attr_re.findall(text):
        if target.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:', 'javascript:')):
            continue
        path = target.split('#', 1)[0].split('?', 1)[0]
        if not path:
            continue
        if not os.path.exists(path):
            problems.append(f'{fn}: {target}')

print('\n'.join(problems))
PY
)"
if [ -n "$broken_links" ]; then
  printf '%s\n' "$broken_links"
  error "ERROR: found broken local links in generated HTML"
fi

for page in *.dj; do
  rg -q '^# DRAFT$' "$page" && continue
  [ -f "$(basename "$page" .dj).meta" ] \
  || echo "WARNING: missing meta for $page"
done
