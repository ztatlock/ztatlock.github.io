# Homepage / CV Curated Consumers Slice 5: Recent Publications

Status: implemented

It builds on:

- [homepage-cv-curated-consumers-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-campaign.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Replace the long literal `## Recent Publications` block on the homepage with a
small derived consumer over canonical publication bundles under `site/pubs/`.

This slice should:

- select from canonical non-draft indexed publication bundles
- use explicit and simple selection/order policy
- render a compressed homepage-specific publication teaser list
- preserve the authored trailing link to `pubs/`

It should not:

- reopen the publication bundle boundary
- force a new homepage-wide curation registry
- solve every future overflow/cap policy question now

## Latched Policy

The implemented policy is:

- anchor to the latest canonical publication year, not the current calendar
  year
- use a trailing 3-year window over bundle `pub_date`
- include all indexed publication bundles, not just `main`
- use no cap for now
- order by canonical `pub_date` descending with title tie-break, inherited
  from publication bundle discovery
- render each item in a compressed homepage-specific form:
  - `Title (Venue Year)`
- link the title to the canonical publication destination for that bundle:
  - local `pubs/<slug>/` page when present
  - otherwise the bundle's primary external publication link

## Why This Policy

The current canonical publication corpus makes this simple rule read well:

- a 2-year window (`2024-2025`) yields only 5 items and feels too narrow
- a 3-year window (`2023-2025`) yields 11 items and matches the homepage's
  current sense of “recent”
- a 4-year window (`2022-2025`) yields 15 items and starts to feel too broad

Anchoring to the latest publication year is important because publication
activity is not guaranteed every calendar year. Anchoring to the wall-clock
year would have made the homepage look artificially sparse in 2026.

## Future Overflow Note

No cap is implemented now.

If future publication density makes the plain trailing 3-year window too large,
the first follow-on should likely be a small explicit cap policy rather than a
new homepage metadata field.

The current best rough fallback idea is:

- keep the most recent core of entries by `pub_date`
- reserve a small number of additional “sticky” slots for especially
  important papers
- if those sticky slots ever matter, prefer:
  1. papers with badges/awards
  2. `main` publications
  3. `workshop` publications

That is only a future note, not current behavior.

## Invariant After This Slice

After slice 5:

- the homepage no longer hand-maintains repeated publication bibliography
  structure
- homepage recent-publications selection is explicit and deterministic
- the homepage and `/pubs/` now share canonical publication-bundle truth while
  still using different renderers
- the top-of-CV `Selected Publications` block remains authored by explicit
  policy
