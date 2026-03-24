# Publications Slice 4: Publication Dates

Status: Implemented

This note records the implementation of the publication-date slice of the
publications structured-content campaign.

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [publications-slice-3-route-cutover.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-slice-3-route-cutover.md)

## Why This Slice Was Needed

The publications collection is now in a good structural state:

- the wrapper lives at `site/pubs/index.dj`
- the canonical collection route is `/pubs/`
- every indexed publication has a canonical local bundle

The next planned step had been to add projection for the repeated publication
entry blocks.

But a sober audit found one important problem first:

- the current publication order is not derivable from slug sort alone

That means the projection slice needs a real ordering fact before it can
replace the hand-authored list body cleanly.

## Slice Goal

Add canonical publication dates to publication bundles and backfill them across
the publications collection so later projected index ordering can be derived
from bundle truth instead of a temporary order manifest or hand-maintained
wrapper text.

## Landed Scope

This slice did these things:

1. extend `publication.json` with a required `pub_date` field for published
   bundles
2. use full ISO date strings:
   - `YYYY-MM-DD`
3. validate and parse that field in publication loading code
4. backfill `pub_date` for all current non-draft publication bundles
5. define the derived index ordering rule for the later projection slice:
   - `pub_date` descending
   - `title` ascending as a stable tie-break
6. stop and reassess before projection

## Non-Goals

This slice should not:

- change the collection route away from `/pubs/`
- project the index yet
- add a collection-owned order manifest
- recover missing local publication artifacts
- add a richer venue taxonomy than the current `listing_group`
- change local detail-page routing

## Final Invariants For This Slice

At the end of this slice:

1. every non-draft publication bundle has a valid `pub_date`
2. `pub_date` is stored as an ISO `YYYY-MM-DD` string
3. publication loading exposes `pub_date` as structured data, not raw text
4. validation rejects published bundles missing `pub_date`
5. the publications campaign has one clear future ordering rule:
   - descending `pub_date`
   - ascending `title` tie-break
6. the projection slice no longer needs a temporary order manifest design

## Design Choices

### 1. Treat `pub_date` As Publication Truth

Unlike a collection order manifest, publication date is a real
publication-local fact.

That makes it the better foundation for index ordering because it:

- lives naturally in `publication.json`
- will likely be useful beyond the index
- avoids a second source of truth for collection order

### 2. Use Full ISO Dates

This slice should use:

- `YYYY-MM-DD`

not:

- year-only strings
- partial dates
- collection-local ranking fields

The user expectation is that exact dates should be discoverable from publisher
or venue pages, and that is the simpler long-term model if we can fill them
reliably now.

### 3. Keep The Rule Small

The later projection slice should sort by:

1. `pub_date` descending
2. `title` ascending

That is enough to make ordering deterministic without adding another field.

If two publications truly share the same date, title order is a stable and
reviewable tie-break.

## What Landed

### Step 1: Extend The Publication Schema

Add `pub_date` to the publication model and validation rules.

Landed shape in `publication.json`:

```json
{
  "pub_date": "2024-06-03"
}
```

Landed validation:

- drafts may omit it
- non-draft publications must provide it
- the string must match `YYYY-MM-DD`
- it must be parseable as a real calendar date

Tests added:

- accept valid ISO date
- reject missing `pub_date` on published bundle
- reject malformed date
- reject impossible date

### Step 2: Backfill The Dates

`pub_date` was backfilled for all current non-draft publication bundles.

Primary sources used:

- publisher pages
- venue pages
- other authoritative publication pages as needed

This slice will likely require careful web research because exact publication
dates are not stable knowledge and need verification.

Backfill rule:

- prefer the publisher-labeled `Published` assertion when available
- otherwise use `published-online`
- otherwise `published`
- otherwise `published-print`
- when DOI metadata was missing or insufficient, use official venue or
  publisher pages for an exact date

Result:

- every non-draft bundle has `pub_date`
- validation stays green

### Step 3: Verify Derived Ordering

The current hand-authored index ordering was then compared against the derived
rule:

1. `pub_date` descending
2. `title` ascending

The result was good enough to proceed: the derived order is plausible for both
the `main` and `workshop` groups without introducing a temporary collection
order manifest.

### Step 4: Final Verification

Run the normal repo checks and stop.

Verification run:

- `make test`
- `make inventory`
- `make check`
- `git diff --check`

Also verified:

- `*.html`
- `sitemap.txt`
- `sitemap.xml`

This slice remained schema/data only and did not change tracked generated
outputs.

## Tests

Add focused tests for:

- `pub_date` parsing and validation
- published bundle missing `pub_date`
- malformed ISO date
- impossible ISO date
- acceptance of mixed richer/minimal bundles with valid dates

## Follow-On Question For The Next Slice

Because this slice landed cleanly, the next slice is now simpler:

- replace repeated publication-entry blocks with projection from bundle data
- sort the projected lists by `pub_date` descending, then title

That later slice should keep:

- `site/pubs/index.dj` as wrapper
- framing and `Aggregators` hand-authored

## Outcome

`pub_date` now feels like the right source of truth for publication ordering.
Exact dates were tractable to verify with DOI metadata plus a smaller manual
fallback set from official venue/publisher pages. The campaign can now move on
to projection without inventing a second ordering source.
