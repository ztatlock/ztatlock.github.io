# Service Slice 1: Canonical Term Model

This note records the first slice of the service campaign.

Status: implemented

It builds on:

- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Purpose

Establish a canonical service model before any public wrapper or projection
work lands.

This slice should solve two problems first:

- repeated service facts currently live in multiple hand-authored pages
- the current section headings are not sufficient as the sole canonical schema
  because some records belong in more than one view bucket

## Recommendation

Start with `site/data/service.json`, not page projection.

The canonical shape should be:

- top-level ordered `records`
- one record per service term per year
- optional shared `series_key` for longer appointments or recurring roles
- explicit multi-group `view_groups`

## Why One Record Per Year

Exploding longer appointments into yearly terms gives a cleaner long-term base:

- easy year-based queries later
- easy “all years of this role” queries via `series_key`
- later renderers can still collapse consecutive terms into year ranges where
  that presentation is better

This is a better foundation than storing only hand-authored display ranges like
`2026 - 2029`.

## Minimum Field Set

Slice 1 should start with:

- `key`
- optional `series_key`
- `year`
- optional `ongoing`
- ordered `view_groups`
- `title`
- optional `role`
- optional `url`
- optional ordered `details`

Important field semantics:

- `view_groups` capture current public/CV grouping buckets only
- `ongoing` belongs only on the latest currently open-ended term in a series
- `details` should stay small and rare in slice 1
- homepage-specific curation metadata should stay out of slice 1 unless the
  backfill proves it is unavoidable

## What Landed

This slice established:

- canonical service terms in `site/data/service.json`
- strict loading/validation in `scripts/service_record.py`
- source-validation integration so the public service page now requires the
  canonical registry to exist
- a backfill that already reconciles the known public/CV drift items in
  canonical data even before any rendering cutover

## Data Backfill Scope

The slice should backfill:

- all intended public service-page entries
- all intended CV service entries
- homepage recent-service entries only as audit inputs, not as a reason to add
  dedicated homepage-selection fields yet

And it should explicitly reconcile the already-known drift:

- `2024 FPTalks Co-Organizer`
- `2022 - Present EGRAPHS Community Advisory Board`
- `2026 Dagstuhl Seminar 26022: EGRAPHS`

## Validation Contract

The loader/validator for this slice should enforce:

- top-level `records` exists and is a non-empty array
- every record key is unique
- every record year is a four-digit integer
- every record has at least one `view_group`
- `view_groups` contain only supported values
- `series_key` may repeat, but `key` must not

The validator should not yet require:

- public wrapper placeholders
- CV projection fields
- homepage-selection fields or ordering rules

## Invariant After This Slice

After slice 1:

- `site/data/service.json` is the canonical service fact source
- every intended service fact is represented exactly once per year-term
- multi-group membership is explicit rather than duplicated by hand
- public page, homepage, and CV are still hand-authored consumers

## Explicit Non-Goals

This slice should not:

- move the public service page yet
- canonicalize `/service/` yet
- rewrite `service.html` links yet
- add homepage-selection metadata yet
- project the homepage service slice yet
- project the CV service section yet
