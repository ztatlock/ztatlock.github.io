# CV Slice 7: Funding Projection

Status: reviewed and ready to implement

It builds on:

- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [funding-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/funding-campaign.md)
- [funding-slice-2-index-projection.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/funding-slice-2-index-projection.md)

## Goal

Replace only the duplicated funding list body in the CV with projection from
canonical `site/data/funding.json`, while keeping the `## Funding` heading
hand-authored in `site/cv/index.dj`.

## Why Funding Next

Funding is now the cleanest remaining cross-domain CV consumer slice because:

- canonical funding truth now exists in `site/data/funding.json`
- the public funding wrapper at `site/funding/index.dj` already proves the
  base funding architecture
- the CV still contains a literal repeated funding list in one hand-maintained
  block
- the current canonical funding render already reproduces the CV substance
  almost exactly, so this is a low-risk downstream-consumer cleanup rather
  than a new modeling effort

## Scope

1. Keep the CV wrapper at `site/cv/index.dj`.
2. Preserve the `## Funding` heading hand-authored.
3. Replace only the repeated funding list body with a placeholder.
4. Add an explicit CV-specific funding renderer over canonical funding data.
5. Add source validation for the placeholder-based CV funding section.

Likely placeholder:

- `__CV_FUNDING_LIST__`

## Important Rendering Principle

This slice should not blindly reuse the public funding page renderer just
because the public and CV views are very close.

Instead:

- reuse canonical funding record order and substance from `site/data/funding.json`
- keep the CV renderer explicit so the CV-specific formatting policy remains
  reviewable

Recommended first-slice CV funding policy:

- preserve the current two-line entry shape
- preserve plain-text titles with no links
- preserve plain-text sponsor / award-id text
- preserve comma-formatted USD amounts
- preserve the current CV year-range style with an en dash

This policy should keep the rendered CV as close as possible to the current
hand-authored section while still removing the duplicate source of truth.

## Out Of Scope

- no public funding-page changes
- no funding-schema expansion
- no CV/public funding unification framework
- no grant-to-publication associations
- no grant-to-project associations
- no homepage funding/highlights work
- no `site/data/cv.json`

## Expected Invariants After This Slice

- the CV funding list derives from canonical funding records
- the public funding page and the CV now share one canonical funding source
  while keeping separate consumer renderers
- no literal duplicated funding-entry block remains in the CV funding section
- visible changes in that section are explainable as either:
  - explicit CV renderer policy
  - canonical correction from funding data truth

## Expected Visible Changes

If the CV renderer preserves the current entry shape and en-dash policy, the
old/new rendered diff for the `Funding` section should ideally be identical or
nearly identical.

Any visible difference should be called out explicitly and should remain minor,
for example:

- punctuation normalization
- whitespace normalization
- a canonical correction if the data file and the old CV diverged

Nothing outside the `Funding` section should change.

## Verification Targets

- focused renderer/projection tests for the CV funding view:
  - canonical record order
  - sponsor plus optional award-id formatting
  - comma-formatted USD amounts
  - en-dash year-range policy
- validation that the required CV funding placeholder is present
- validation that literal duplicated funding-entry blocks are rejected in the
  projected CV `Funding` section
- compare old and new rendered CV HTML with attention to the `## Funding`
  section specifically:
  - only the intended funding body should change
  - surrounding sections should remain stable
  - visible differences should be explainable by explicit renderer policy or
    canonical correction
- `make test`
- `make build`
- `make check`

## Stop Point

Stop after the CV `Funding` projection and reassess.

The next funding-related question should then remain deliberate:

- keep grant-output associations deferred longer
- or plan a separate later enrichment slice only if that cross-domain mapping
  clearly earns its complexity

Do not automatically broaden from this slice into research-page consumers,
homepage consumers, or grant/publication association work.
