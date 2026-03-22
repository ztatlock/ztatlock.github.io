# Route/Build Engine Slice 1

Status: Initial prototype live in repo

This note defines the first implementation slice of the broader route-aware
source/build/deploy redesign.

The slice is no longer purely hypothetical.
The repo now has an initial working prototype behind:

- `make routes-preview`
- `make build-preview`
- `make check-preview`

The rest of this note describes the intended shape and limits of that slice.

The key priority is now:

- adopt the **future output and URL model** immediately
- keep the **current source layout** temporarily
- build a real preview site into `build/`
- delay the `site/` source move until the new builder is trusted

That order minimizes split-brain risk.

## Why This Order Is Better

The earlier idea was:

1. centralize the current root-level route model
2. later change it to the future `build/` and nested publication layout

That looks incremental, but it creates the wrong kind of temporary
complexity.

It would force the new engine to learn a route model we already know we want
to delete:

- publication pages at `pub-<slug>.html`
- root-served build assumptions
- root-level sitemap/canonical expectations

Then we would have to rework all of that again.

The cleaner order is:

1. keep current sources for now
2. use the future route/output model now
3. build into `build/` now
4. move source into `site/` later

That way the only major later migration is source relocation, not route-model
replacement.

## Slice Goal

Build a small Python preview builder that:

- reads the current source layout
- computes routes using the intended future public/output model
- writes a coherent preview site into `build/`

This should be the first place where the new architecture becomes real.

## The Core Principle

For slice 1:

- **source layout** remains current
- **route/output layout** becomes future-oriented

So the new engine should think in terms of the future site shape even while it
still reads from the current repo layout.

## Scope

Slice 1 should do four things:

1. route discovery
2. route validation
3. preview rendering into `build/`
4. copying the minimum required public assets into `build/`

That is a real vertical slice, not just a route dump.

## Explicit Non-Goals

Slice 1 should **not**:

- move source files into `site/`
- change the production/root-level build path yet
- change the live deployment path yet
- remove committed generated HTML yet
- add GitHub Pages Actions yet
- redesign every page/data class at once
- fully retire the current Makefile-driven production build

The preview builder should be real, but still non-production at first.

## Next Planned Follow-Up

The next slice after this prototype is not another route-discovery change.

It is a consolidation slice:

- extract one shared render core for:
  - route-aware metadata rendering
  - page HTML document assembly
- then add route-driven sitemap generation for `build/`

That follow-up is captured in
[route-build-engine-slice-2.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/route-build-engine-slice-2.md).

## Future Route Model Now

This slice should use the intended future output rules.

### Ordinary Pages

- source: current top-level `<stem>.dj`
- preview output: `build/<stem>.html`
- public URL: `/<stem>.html`, except `index -> /`
- canonical URL: absolute form of the public URL

### Publication Pages

- source: current `pub-<slug>.dj` stub plus `pubs/<slug>/publication.json`
- preview output: `build/pubs/<slug>/index.html`
- public URL: `/pubs/<slug>/`
- canonical URL: absolute form of the public URL

### Static/Copied Files

Slice 1 does not need a grand static-route theory, but it does need enough
copy support to make the preview site coherent.

That means the preview build should copy the currently relevant public files
into `build/`, for example:

- `img/`
- `style.css`
- `zip-longitude.js`
- `CNAME`
- `robots.txt`
- standalone static HTML pages
- publication-local assets already linked from publication pages

This is enough to make `build/` inspectable and internally consistent.

## Why Not Move Source First

Because that creates the worse split brain.

If we move source into `site/` before the new builder exists, we would need
some awkward transition like:

- duplicate source trees
- mirroring
- temporary compatibility shims
- or half-migrated live build logic

That is exactly the kind of complexity we want to avoid.

The current source tree should remain the source of truth until the preview
builder is working well enough that a source move becomes mostly mechanical.

## Route Model For Slice 1

The model should stay small.

Recommended shape:

```text
Route
  kind
  key
  source_paths
  output_relpath
  public_url
  canonical_url
  is_draft
```

### Field Notes

- `kind`
  One of:
  - `ordinary_page`
  - `publication_page`
  - `static_file`

- `key`
  Stable internal identifier.

- `source_paths`
  The exact current source inputs for the route.

- `output_relpath`
  Path relative to `build/`.

- `public_url`
  URL path form intended for the future site shape.

- `canonical_url`
  Absolute site URL derived from `public_url`.

- `is_draft`
  Draft/public status for rendered page routes.

## Invariants

Slice 1 should validate at least:

- every route key is unique within its kind
- every public route has a unique `output_relpath`
- every public route has a unique `public_url`
- every public route has a unique `canonical_url`
- every `output_relpath` is normalized and relative
- publication slugs and current stub names agree
- every public publication route has its required local record
- copied output paths do not collide with rendered page outputs

These invariants are one of the main reasons to build the route layer first.

## Key Design Constraint: Reuse Existing Rendering Logic Where Practical

Slice 1 should **not** rewrite everything.

Where possible, it should reuse or wrap existing logic such as:

- [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- [render_meta.py](/Users/ztatlock/www/ztatlock.github.io/scripts/render_meta.py)
- the current site refs composition

This is important for keeping the first slice small.

The new value of slice 1 is:

- route truth
- build/output truth
- preview artifact in `build/`

not a full renderer rewrite.

## Proposed Module Boundaries

Recommended first-cut modules:

- `scripts/sitebuild/site_config.py`
  Shared config values like repo root and site URL.

- `scripts/sitebuild/route_model.py`
  `Route` dataclass plus route validation helpers.

- `scripts/sitebuild/route_discovery.py`
  Discover future-oriented routes from the current source tree.

- `scripts/sitebuild/preview_builder.py`
  Render/copy the preview site into `build/`.

- `scripts/render_routes.py`
  Optional diagnostic route-table output for humans/tests.

- `scripts/build_preview_site.py`
  Thin CLI entry point for the preview builder.

This is enough for slice 1.

## Command Surface

Keep Make thin.

Recommended commands:

- `make build-preview`
  Build the preview site into `build/`.

- `make check-preview`
  Run focused validation against the preview site.

Optional:

- `make routes-preview`
  Emit a deterministic route table to `state/routes.json`.

The main artifact should be the preview build itself, not only a route dump.

## Testing Plan

Slice 1 should add small unit tests for:

- ordinary route derivation
- `index` special-case URL handling
- publication route derivation to `pubs/<slug>/index.html`
- draft detection
- canonical URL computation
- duplicate output/public URL detection
- copied-output collisions
- publication stub/record mismatch failures

And a smaller integration check for:

- successful preview build into `build/`
- expected presence of a few representative outputs

## Acceptance Criteria

Slice 1 is successful if:

1. `build/` contains a coherent preview site using the future route/output
   layout
2. publication preview pages build to `build/pubs/<slug>/index.html`
3. route invariants are enforced by unit-tested Python code
4. the current production/root-level build remains unchanged
5. the new preview builder is small enough that its responsibilities are easy
   to explain

## What Slice 2 Should Do Next

Once slice 1 works, the next slice should be:

- strengthen preview validation
- make more of the current checks consume the new route/build model
- reduce duplication between the preview builder and the legacy build path

Only after the preview builder feels trustworthy should we take on:

- moving source into `site/`
- switching deployment to `build/`
- removing tracked generated root outputs

## Recommendation

Do **not** make the first new engine slice learn the old root-level
publication route model.

Make the first slice future-oriented in its route/output layout, but keep it
non-production and keep current source locations for now.

That is the cleanest way to get real architectural progress without creating
temporary route-model debt we already know we do not want.
