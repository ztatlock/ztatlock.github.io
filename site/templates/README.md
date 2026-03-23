# Templates

This directory holds non-executable template inputs used by the site build and
page scaffolding.

## Current Files

- `HEAD.1`
  Base document head with title and canonical URL placeholders, plus the
  shared stylesheet and favicon link.
- `HEAD.2`
  The analytics snippet and the opening `<body>`.
- `FOOT`
  The closing `</body>` and `</html>` tags.
- `REFS`
  Tiny hand-maintained non-person Djot reference remainder appended to every
  generated page alongside generated people refs from `site/data/people.json`.
- `publication.json`
  Publication-local record scaffold used by `scripts/mkpub.sh`; new
  scaffolds start with `"draft": true`.

## Conventions

- Keep this directory non-executable.
- Document new template inputs here when the build starts depending on them.
- Placeholder tokens are fine in scaffolds such as `publication.json`,
  but generated public pages should not ship unresolved placeholders.
- Prefer updating `scripts/mkpub.sh` and the authoritative validation/build
  path alongside template changes so scaffolding and validation stay in sync.
