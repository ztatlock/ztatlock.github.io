# ztatlock.net

This is the repo for
  [Zachary Tatlock's website](https://ztatlock.net)
  mostly built with
  [djot](https://djot.net/) and
  [make](https://www.gnu.org/software/make/).

- All pages are at the top level.
- Each `.dj` file is compiled to an `.html` page.
- Pages whose source contains a `# DRAFT` heading are excluded from
  `make all` and the sitemaps.
- Use `make drafts` to build draft pages locally when needed.
- `REFS` provides global reference links included for each page.
- Each page includes a common header and footer (`HEAD`, `FOOT`).
- Each page's title is taken from the first line of its source `.dj`.
- All pages use the same, very simple `style.css`.
- Human-authored policy/spec docs live under [docs/](docs/README.md).
- Executable helpers live under `scripts/`.
- Small versioned structured manifests live under `manifests/`.
- Local generated/runtime state lives under `state/`.
- Common support entry points are exposed as `make` targets such as
  `make check`, `make inventory`, `make inventory-webfiles`,
  `make mkpub YCF=...`, and `make index-now`.
- Publication storage/linking policy is documented in
  [docs/policy/publication-artifacts.md](docs/policy/publication-artifacts.md).
- Repo-local inventory previews live under `state/inventory/`.
- The canonical archive copy of the publication artifact inventory lives in
  `~/Desktop/WEBFILES/inventory/` and can be refreshed with
  `make inventory-webfiles`.

Issues and/or PRs to fix typos or missing content are welcome!
