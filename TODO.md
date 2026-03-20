# TODO

## Near Term

- Keep improving repo structure and discoverability without doing a risky
  source/build/deploy migration yet.
- Keep the current root-level file classes documented in
  `docs/policy/root-layout.md`.
- Keep small self-describing docs current when support directories change.
- Keep publication metadata under separate design review while ordinary pages
  now use YAML front matter directly.
- Revisit which generated outputs are intentionally tracked in git and which
  eventually deserve a better home than the repo root.

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
- Revisit whether the eventual source/build/deploy split should stay custom or
  migrate to Jekyll or another more conventional SSG.
- Create and integrate a replacement first-party Neutrons project page, since
  the historical external site is gone.
- Search older website copies and personal archives for missing publication
  artifacts.
