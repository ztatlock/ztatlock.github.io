# TODO

## Near Term

- Keep improving repo structure and discoverability without doing a risky
  source/build/deploy migration yet.
- Add small self-describing docs where useful, e.g. a `templates/README.md`.
- Review which generated outputs are intentionally tracked in git and which are
  just build artifacts.

## Publication Artifacts

- Do not try to grind through full publication-artifact curation in one pass.
- Chip away at `manifests/publication-artifact-curation.tsv` incrementally over
  time.
- Start with the highest-signal cases:
  - `2023-plarch-lakeroad` missing repo meta image
  - public talk links without `WEBFILES` backups
  - `WEBFILES` talk backups without corresponding page talk links
- Treat missing slide PDFs and poster PDFs as cleanup work, not as a same-day
  fire drill, until manually curated.

## Future Campaigns

- Make the authored-source vs built-output split explicit.
- Move toward an intentional build/deploy pipeline instead of serving the repo
  root directly.
- Search older website copies and personal archives for missing publication
  artifacts.
