# Funding Slice 2: Public Wrapper / Route Cutover

Status: implemented

It builds on:

- [funding-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/funding-campaign.md)
- [funding-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/funding-slice-1-canonical-model.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Add a thin public funding wrapper at `site/funding/index.dj`, canonicalize
`/funding/`, and project the repeated funding list from `site/data/funding.json`
while keeping the page framing hand-authored.

## Scope

In scope:

- `site/funding/index.dj`
- explicit `/funding/` route support
- public funding list projection from `site/data/funding.json`
- source validation for the wrapper shape
- focused renderer, projection, route, and page-rendering tests

Out of scope:

- CV funding projection
- homepage funding/highlights projection
- grant-to-publication associations
- grant-to-project associations
- sponsor normalization or derived funding analytics

## Public Render Policy

The public funding page should stay intentionally simple:

- preserve canonical record order from `site/data/funding.json`
- render one grant per bullet
- keep the grant title on the lead line
- render role, sponsor plus optional award id, amount, and year range on the
  second line

This keeps the first public wrapper faithful to the current funding substance
without inventing a richer funding presentation model yet.

## Invariant

After slice 2:

- the public funding page is a thin wrapper over canonical funding records
- the canonical public route is `/funding/`
- no repeated funding fact block remains in the wrapper
- the CV funding section remains hand-authored by explicit policy
- no grant-output associations are modeled yet

## Implemented Result

This slice landed as:

- `site/funding/index.dj`
- `scripts/funding_index.py`
- explicit funding route/config/render plumbing in the build
- source-validation rules requiring the funding wrapper and placeholder when
  canonical funding records exist
- focused coverage for route discovery, page rendering, projection, and source
  validation

## Design Notes

Important design choices for slice 2:

- keep the wrapper minimal rather than adding early editorial sections
- keep the renderer explicit and route-aware
- avoid adding a second funding schema or any generalized projection framework
- stop after the public funding page and reassess before any CV or research-page
  consumer work
