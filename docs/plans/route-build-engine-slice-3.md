# Route/Build Engine Slice 3

Status: Initial implementation live in repo

This note defined the next implementation slice after the preview-builder
checkpoint and now records the first real implementation of that slice.

- future-oriented routes are live under `build/`
- the preview builder and legacy root build share a render core
- preview sitemap generation is route-driven
- legacy and preview builds now share HTML artifact-validation helpers

The key move in this slice was **not** to move files into `site/` yet.
The key move was to make the new engine **source-layout-aware** while still
pointing it at the current repo-root source layout.

Update:

- [site_config.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_config.py)
  now carries explicit source-root fields for pages, publications, templates,
  data, static files, and shared images
- route discovery now uses those configured source roots instead of hardcoded
  repo-root globs
- the shared render/source/metadata/publication loaders now accept explicit
  configured roots while keeping current-layout defaults for the legacy path
- metadata validation now also resolves page/publication image paths against
  configured source roots rather than assuming repo-root layout
- alternate-layout tests now prove the preview builder can read from a
  temporary `site/pages`, `site/pubs`, `site/templates`, `site/data`, and
  `site/static` tree without changing route/output semantics
- `SiteConfig.site_url` is now threaded through the preview render path so the
  new engine has one explicit site-URL truth instead of a split config/helper
  model

## Why This Slice Matters

The route/output side of the redesign is now far enough along that the main
remaining risk has shifted.

The biggest thing that *had been* preventing a later low-risk source move was
that the new engine hardcoded the current source layout in multiple places:

- [site_config.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_config.py)
- [route_discovery.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_discovery.py)
- [site_builder.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_builder.py)
- [page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_renderer.py)
- [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)

At the start of this slice, the preview path still assumed:

- ordinary pages are top-level `*.dj`
- publication stubs are top-level `pub-*.dj`
- publication bundles live under `pubs/`
- templates live under `templates/`
- shared data lives under `site/data/`
- copied static files are discovered from the repo root

This slice removed most of those assumptions from the new engine. The remaining
bridge constraints are now narrower:

- `page_source_dir` still contains both ordinary pages and `pub-*.dj` stubs
- static discovery is still a bridge model built around `static_source_dir`
  plus a separate image-root concept, not the final generalized
  `site/static/` model
- the legacy production build still points the config at the current repo-root
  layout

The next follow-up after this checkpoint is captured in
[route-build-engine-slice-4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/route-build-engine-slice-4.md):
remove the preview engine's remaining dependence on top-level publication
stubs and make publication discovery/status fully publication-local.

## Slice Goal

Make the preview engine source-layout-aware **without moving files yet**.

At the end of this slice:

- the preview engine should get its source locations from config rather than
  hardcoded repo-root assumptions
- the config should still point at the **current** layout
- the preview output and public URL model should stay exactly as it is now

This should make the later source move mostly mechanical.

## Core Principle

Do **not** invent a big abstraction framework here.

The right model is:

- one explicit config object
- a small number of explicit source-root fields
- existing loaders/renderers updated to use those fields

The goal is to replace hidden path assumptions with a small amount of explicit
path truth, not to build a general plugin system.

## Proposed Source-Layout Model

The current [SiteConfig](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_config.py)
is too small.

It should grow from:

- `root`
- `build_dir`
- `site_url`
- `webfiles_url`

to something more like:

```text
SiteConfig
  repo_root
  build_dir
  site_url
  webfiles_url

  page_source_dir
  publications_dir
  templates_dir
  data_dir
  static_source_dir
```

With simple derived paths such as:

- `people_data_path = data_dir / "people.json"`
- `manual_refs_path = templates_dir / "REFS"`

Important design choice:

- keep `page_source_dir` as the home of both ordinary pages and current
  `pub-*.dj` stubs for now

That keeps this slice focused on source-layout awareness, not publication-stub
retirement.

## What Should Change

### 1. `SiteConfig` Becomes The Path Truth

Route/build modules should stop deriving source paths from repo-root joins
directly.

Instead they should derive them from explicit config fields such as:

- `config.page_source_dir`
- `config.publications_dir`
- `config.templates_dir`
- `config.data_dir`
- `config.static_source_dir`

This is the most important change in the slice.

### 2. Route Discovery Uses Source Roots, Not Repo-Root Globs

[route_discovery.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_discovery.py)
should stop doing things like:

- `config.root.glob("*.dj")`
- `config.root.glob("pub-*.dj")`
- `config.root / "img"`

and instead use the explicit configured roots.

This is the direct prerequisite for moving pages/static files later.

### 3. Shared Render/Metadata/Source Loaders Must Be Path-Aware Too

This slice cannot stop at route discovery, because rendering still assumes the
same root layout.

At the start of the slice:

- [page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_renderer.py)
  read `templates/` from `root`
- [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
  found page sources at `root / f"{page}.dj"`
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
  loaded page/publication metadata from `root`
- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
  assumed publication bundles lived under `root / "pubs"`

So the source-layout awareness needs to reach the shared loaders too.

The clean rule is:

- preview-engine call paths should pass explicit configured source roots
- legacy root-build call paths should keep using current-layout defaults

### 4. Refs/Data Loading Should Also Use Config Paths

[site_builder.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_builder.py)
had also hardcoded:

- `site/data/people.json`
- `templates/REFS`

Those now come from derived config paths rather than literal joins against
repo root.

## Recommended Implementation Order

### Step 1: Expand `SiteConfig`

Add the explicit source-root fields with defaults pointing at the current
layout.

This step should not change behavior yet.

### Step 2: Refactor Preview-Side Discovery And Build Code

Update:

- [route_discovery.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/route_discovery.py)
- [site_builder.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/site_builder.py)
- [djot_refs.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/djot_refs.py)
- [page_renderer.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_renderer.py)

so they use the explicit config paths.

### Step 3: Parameterize Shared Loaders Used By The Preview Path

Refactor the shared helpers so they can load from explicit source roots:

- [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
- [publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)

The legacy build can keep passing current-layout roots.

### Step 4: Add Alternate-Layout Tests

Add focused tests that prove the new engine can read from a temporary
non-root layout, for example:

- pages under a temporary `site/pages/`
- templates under a temporary `site/templates/`
- publication bundles under a temporary `site/pubs/`
- static files under a temporary `site/static/`

without changing route/output semantics.

This is the real proof that the source-layout abstraction is doing its job.

## Lessons Learned

- Publication asset public paths cannot be derived relative to repo root once
  bundles move under configurable source roots. They must be derived relative
  to `publications_dir` and then mapped back to public `pubs/...` paths.
- Static-file handling is still intentionally transitional. The preview engine
  currently supports explicit top-level statics, configured shared images, and
  publication bundle assets; it does **not** yet model a fully general
  `site/static/` copy-through tree.
- Source-layout awareness has to include validation, not just discovery and
  rendering. Otherwise a future `site/` move would still fail on stale
  repo-root assumptions in metadata checks.
- `site_url` should be treated as config truth in the new engine. Helper code
  should not silently hard-code `https://ztatlock.net` when a route-aware
  preview path already has explicit site configuration.

### Step 5: Reassess Before Any File Move

Once the engine is source-layout-aware and tested, stop and inspect what is
still hardcoded before moving any real source files.

## What Slice 3 Should Not Do

Slice 3 should **not**:

- move actual source files into `site/`
- cut production deployment over to `build/`
- teach the new engine the legacy root sitemap model
- remove publication stubs
- add talks/students/CV projections yet
- redesign validation again

This is a source-layout-awareness slice, not the source-move slice itself.

## Why This Is The Right Next Move

This slice directly attacks the main remaining source of churn.

It is better than:

- legacy sitemap unification now
  because that would reintroduce temporary legacy route assumptions
- moving files now
  because the engine still assumes the old source layout too strongly
- adding new data projections now
  because the build/source architecture is still the bigger leverage point

So the recommended next phase is:

- make source roots explicit everywhere in the new engine
- keep them pointed at the current layout
- then move files later from a much safer base
