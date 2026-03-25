# Funding Slice 1: Canonical Model

Status: planning

It builds on:

- [funding-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/funding-campaign.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)

## Goal

Establish a canonical funding data source in `site/data/funding.json` without
changing any public page rendering yet.

This slice should make it possible to represent the current funding facts in
one place before any public wrapper or CV projection decisions happen.

## Scope

In scope:

- `site/data/funding.json`
- loader and validator code
- focused unit tests
- backfilled canonical records for the current intended funding facts

Out of scope:

- adding `site/funding/index.dj`
- canonicalizing `/funding/`
- CV funding projection
- homepage funding/highlights projection
- grant-to-publication associations
- grant-to-project associations

## Current Audit Facts

The current explicit funding content is the `## Funding` section in
`site/cv/index.dj`.

That section currently contains `10` entries.

Each current entry includes:

- title
- role
- sponsor
- optional award identifier embedded in sponsor text
- dollar amount
- year range

Important current facts:

- there is no public funding page yet
- there is no canonical `site/data/funding.json` yet
- there is no current structured association between funding records and
  research projects or publications

So slice 1 should backfill the intended current funding facts, not merely
prepare a future graph.

## Recommended Schema

Use a small shared-data shape similar in spirit to `site/data/service.json`:

- top-level ordered `records`

Each `record` should have:

- `key`
- `title`
- `role`
- `sponsor`
- optional `award_id`
- `amount_usd`
- `start_year`
- `end_year`

## Validation Contract

The loader/validator for this slice should enforce:

- top-level `records` exists and is a non-empty array
- every record key is unique
- every record title is a non-empty string
- every record role is a non-empty string
- every record sponsor is a non-empty string
- `award_id`, when present, is a non-empty string
- `amount_usd` is a positive integer
- `start_year` and `end_year` are four-digit integers
- `start_year <= end_year`
- unknown fields are rejected

The validator should not yet require:

- public wrapper placeholders
- CV projection placeholders
- project/publication association fields
- sponsor registries or normalized role taxonomies

## Invariants

After slice 1:

- `site/data/funding.json` is the canonical funding fact source
- every intended current grant fact is represented exactly once
- record order in `site/data/funding.json` is canonical
- current public pages and the CV remain unchanged
- no grant-output associations are modeled yet

## Design Notes

Important design choices for slice 1:

- keep the model flat and explicit
- preserve sponsor names as plain strings
- preserve amounts as integer USD values
- separate `award_id` from `sponsor` when the current CV text includes it
- avoid adding fields "for later" unless a current funding record needs them

This slice should remain intentionally small.
Its job is to make the later public funding wrapper simple and reviewable.
