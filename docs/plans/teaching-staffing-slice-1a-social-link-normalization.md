# Teaching Staffing Slice 1A: Social-Link Normalization

Status: planned

It builds on:

- [teaching-staffing-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-campaign.md)
- [teaching-staffing-slice-1-people-linkability.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-staffing-slice-1-people-linkability.md)
- [people-registry-semantics.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/people-registry-semantics.md)
- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)

## Goal

Normalize the seeded `site/data/people.json` records so the new public-link
schema is used consistently before the later teaching-staffing data import
adds many more people.

This slice should be a pure cleanup:

- no new people
- no new links
- no teaching staffing facts
- no intended visible site changes

## Why This Slice Now

Teaching-staffing slice 1 already landed the new linkability contract:

- `url`, `linkedin`, and `github` are now optional public-link fields
- generated Djot refs use a derived `primary_url`
- structured consumers can tolerate linkless people

But the seeded registry still carries many social-profile links in `url`:

- `19` LinkedIn profiles
- `7` GitHub profiles
- `0` seeded `linkedin` fields
- `0` seeded `github` fields

So the contract is landed, but the data is not yet normalized to use it.

Doing this cleanup now keeps the registry clearer before a larger staffing
import increases the surface area.

## Scope

In scope:

- normalize existing obvious LinkedIn-only and GitHub-only `url` values into
  typed `linkedin` and `github` fields
- add focused regression tests
- update docs and backlog so the repo tells the truth about the new checkpoint
- do an explicit before/after rendered HTML diff review

Out of scope:

- adding any new people
- adding any new URLs
- changing `name`, `aliases`, or person keys
- changing public render policy
- teaching staffing schema work
- co-instructor or TA canonicalization

## Normalization Rules

Use these exact rules:

1. If a record's `url` host is `linkedin.com` or `www.linkedin.com`,
   move that exact string from `url` to `linkedin`.
2. If a record's `url` host is `github.com` or `www.github.com`,
   move that exact string from `url` to `github`.
3. Preserve the exact URL string during the move:
   - do not rewrite casing
   - do not add or remove trailing slashes
   - do not rewrite paths
4. Do not touch non-social `url` values.
   Personal homepages, university pages, lab pages, and other ordinary public
   URLs stay in `url`.
5. Do not infer or add new links.
   This is normalization only, not enrichment.
6. If a record ever already has both `url` and `linkedin` or `github`,
   review it explicitly rather than auto-merging it.
7. Do not change `name`, `aliases`, or the alias-resolution namespace in this
   slice.

## Invariant

After this slice:

- `url` is used for preferred general public homepage-style links
- LinkedIn-only public links live in `linkedin`
- GitHub-only public links live in `github`
- the seeded registry uses the new typed social-link fields consistently for
  the obvious current cases
- `primary_url` behavior is unchanged, so current rendered site output should
  remain unchanged

## Why No Visible Change Is Expected

The slice-1 `primary_url` rule is already:

1. `url`
2. `linkedin`
3. `github`

So moving:

- `url: https://www.linkedin.com/...` -> `linkedin: https://www.linkedin.com/...`
- `url: https://github.com/...` -> `github: https://github.com/...`

should preserve the same effective link target everywhere the site currently
renders those people.

That makes this a strong no-visible-change regression test for the new people
semantics.

## Test Targets

Focused tests should cover:

- seeded regression checks that representative social-only people now use
  typed `linkedin` / `github` fields
- `primary_url` remains unchanged for those representative people
- no seeded `url` values in `site/data/people.json` still point at LinkedIn or
  GitHub after normalization
- existing generated-ref and audit tests continue to pass unchanged

Verification should include:

- focused people-registry and people-ref tests
- `make build`
- `make test`
- `make check`

## Rendered Diff Review

This slice should include an explicit before/after rendered HTML diff review.

Recommended review:

1. build the site before the normalization
2. snapshot the rendered `build/` tree
3. apply the normalization
4. rebuild
5. diff the old/new rendered HTML

Expected outcome:

- no rendered HTML changes anywhere

If any rendered page changes, the diff must be explained explicitly before the
slice is accepted.

## Docs / Backlog

When this slice lands, update:

- `docs/plans/teaching-staffing-campaign.md`
- `docs/plans/teaching-staffing-slice-1-people-linkability.md`
- `docs/plans/people-registry-semantics.md`
- `docs/plans/site-architecture-spec.md`
- `docs/plans/structured-content-roadmap.md`
- `ROADMAP.md`

The repo should then show that:

- the linkability contract is implemented
- the seeded data is normalized to use the typed social-link fields
- slice 2 can start from a cleaner and more consistent registry

## Stop Point

Stop after this cleanup and reassess.

The next slice should then be the actual teaching-staffing schema foundation,
not further people-registry enrichment.
