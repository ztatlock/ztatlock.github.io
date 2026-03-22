# Publication Output Cutover

This note focuses on the next publication-architecture question after the
publication-local record migration:

- should top-level `pub-<slug>.dj` stubs survive?
- should publication pages keep building as root-level `pub-<slug>.html`?
- or should publication pages live directly under `pubs/<slug>/`?

The broader publication-record design is already settled enough for this note:

- public publication page body and metadata now come from
  `pubs/<slug>/publication.json`
- top-level `pub-<slug>.dj` files are no longer real page bodies
- backward compatibility with old publication URLs is explicitly a non-goal

So this is no longer a question of how to model publication data.
It is now a question of output shape, source-of-truth boundaries, and cleanup.

## Current State

As of March 21, 2026:

- 21 public detailed publication pages exist
- all 21 use `pubs/<slug>/publication.json` as the canonical publication record
- all 21 still build to root-level `pub-<slug>.html`
- all 21 still have top-level `pub-<slug>.dj` stubs

That means each detailed publication currently occupies:

- one top-level `pub-<slug>.dj` stub
- one top-level `pub-<slug>.html` generated page
- one `pubs/<slug>/` directory containing the real record and assets

So the current steady state still keeps `42` publication-specific files at the
repo root that no longer represent the true home of the publication.

## What The Stubs Still Do Today

The top-level `pub-<slug>.dj` files are now redundant as authored content, but
they still serve three operational roles:

1. publication discovery for `make`
2. publication draft/public status
3. top-level publication page naming and route shape

Those roles are the real reason the stubs still exist.

If we remove the stubs, we must replace all three responsibilities explicitly.

## Additional Audit Findings

### Root-Level Publication Links Are Still Widespread But Contained

Current authored content still links to root-level publication pages from:

- [index.dj](/Users/ztatlock/www/ztatlock.github.io/index.dj)
- [news.dj](/Users/ztatlock/www/ztatlock.github.io/news.dj)
- [publications.dj](/Users/ztatlock/www/ztatlock.github.io/publications.dj)

That is a real cutover cost, but it is a bounded one.
The publication URL shape is not scattered arbitrarily across the repo.

### Current Generated Publication Bodies Assume A Root-Level Output

The publication renderer in
[publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
currently emits body links like:

- `pubs/<slug>/<slug>.pdf`
- `pubs/<slug>/<slug>.bib`
- `publications.html`

Those are correct for a page living at root as `pub-<slug>.html`.
They are **not** correct for a page living at `pubs/<slug>/index.html`.

So moving publication outputs into their own directories requires a route-aware
link model, not just a different output filename.

### Current Extra Content Does Not Block The Move

The current `extra.dj` usage is light.
The only existing extra content file,
[extra.dj](/Users/ztatlock/www/ztatlock.github.io/pubs/2021-iclr-dtr/extra.dj),
contains only external links and embedded iframes.

The current abstract files also do not contain relative local asset links.

That means the cutover does **not** currently require a widespread content
rewrite inside `extra.dj` or abstract files.

### There Are No Current Draft Publication Pages

At the moment, there are no active `# DRAFT` publication stubs.

That matters because it makes draft-model replacement easier:
we do not need to convert a live set of draft publication pages before
changing the draft/public mechanism.

## Decision Criteria

We should judge the next step by:

- source-of-truth clarity
- locality to publication assets
- reduction of root clutter
- build simplicity
- validator simplicity
- future compatibility with a broader source/build/deploy split
- migration risk
- ergonomics for creating a new publication draft

## Options

### Option A: Keep The Current Stub + Root Output Model

Keep:

- top-level `pub-<slug>.dj`
- top-level `pub-<slug>.html`
- publication-local record under `pubs/<slug>/`

#### Strengths

- lowest immediate implementation cost
- no route cutover work
- no draft-model redesign

#### Weaknesses

- leaves the source-of-truth story visibly split
- keeps 42 publication-specific files at the repo root unnecessarily
- keeps the publication URL shape detached from the actual publication locality
- preserves a transition mechanism after the transition is already done

#### Assessment

This is a workable steady state, but not a good long-term design.

### Option B: Remove Stubs But Keep Root-Level `pub-<slug>.html`

Generate root-level publication pages directly from `pubs/<slug>/publication.json`
and delete the top-level `pub-<slug>.dj` stubs.

#### Strengths

- removes the fake page-source layer
- simplifies new publication scaffolding
- avoids route cutover for now

#### Weaknesses

- keeps root-level publication output clutter
- keeps the URL shape detached from publication locality
- solves only half the design problem
- still requires a new publication-local draft/public mechanism

#### Assessment

This is a reasonable intermediate shape, but it feels like an optimization for
avoiding the harder cutover rather than the cleanest long-term design.

### Option C: Remove Stubs And Move Publication Outputs To `pubs/<slug>/index.html`

Make the publication directory the self-contained home of:

- `publication.json`
- abstract/BibTeX/assets
- optional `extra.dj`
- generated public page output as `index.html`

#### Strengths

- strongest locality
- clearest source-of-truth story
- biggest reduction in root clutter
- best match for the broader repo-structure direction
- best final URL shape:
  `https://ztatlock.net/pubs/<slug>/`

#### Weaknesses

- requires route-aware body-link generation
- requires a new publication-local draft/public mechanism
- requires updating all authored links to publication pages
- requires validator and sitemap changes

#### Assessment

This is the strongest target and the one most consistent with the long-term
direction we have already been moving toward.

## Recommendation

Choose **Option C** as the target design.

That means the intended steady state should be:

- no top-level `pub-<slug>.dj` files
- no top-level `pub-<slug>.html` files
- publication pages generated as `pubs/<slug>/index.html`
- publication URLs linked as `pubs/<slug>/`

This is the cleanest design because it lets each publication directory become
the complete unit of publication state:

- canonical structured record
- canonical local artifacts
- optional extra content
- generated public page

## Key Design Decisions For Option C

### 1. Replace Stub-Based Draft Status With Publication-Local Draft Status

The stubs currently carry draft/public status via `# DRAFT`.
If stubs go away, that status must move into the publication-local record.

Recommended first cut:

- support optional `"draft": true` in `publication.json`

Rules:

- if `draft` is absent or false, the publication is public
- if `draft` is true, `make all` excludes the publication page
- `make drafts` includes draft publication pages for local preview

Why this is the right fit:

- it keeps status local to the canonical record
- it avoids introducing another marker file
- it aligns new-publication scaffolding with the real publication source of
  truth

### 2. Use Different Path Strategies For Head Metadata Vs. Body Links

These should not be treated the same.

#### Head Metadata

Canonical URLs and social image URLs should remain absolute URLs derived from
the final public route:

- canonical URL:
  `https://ztatlock.net/pubs/<slug>/`
- image URL:
  `https://ztatlock.net/pubs/<slug>/<slug>-meta.png`
  or fallback image as appropriate

#### Body Links

Generated Djot body links should be relative to the publication output
directory:

- paper: `<slug>.pdf`
- bib: `<slug>.bib`
- slides: `<slug>-slides.pdf` or `<slug>-slides.pptx`
- poster: `<slug>-poster.pdf`
- preview image: `<slug>-absimg.*`
- backlink to publication index: `../../publications.html`

Why relative body links are preferable:

- they preserve publication-directory locality
- they keep publication pages self-contained
- they avoid forcing root-relative path handling everywhere else

### 3. Build Publication Pages From Publication Discovery, Not `*.dj` Discovery

Today publication pages exist because `Makefile` sees top-level `pub-*.dj`.

After cutover, publication discovery should come from:

- `pubs/*/publication.json`

That implies a separate publication-page target list in `Makefile`, distinct
from ordinary top-level `*.dj` pages.

The publication build rule should produce:

- `pubs/<slug>/index.html`

from:

- `pubs/<slug>/publication.json`
- canonical local assets
- optional `extra.dj`

### 3a. Treat Publication Routes, File Paths, And Sitemap Paths Separately

After cutover, these are related but not identical:

- output file path:
  `pubs/<slug>/index.html`
- public route:
  `pubs/<slug>/`
- canonical URL:
  `https://ztatlock.net/pubs/<slug>/`

That distinction should stay explicit in the implementation.

In particular:

- generated `<link rel="canonical">` should use `/pubs/<slug>/`
- OpenGraph and Twitter URLs should use `/pubs/<slug>/`
- sitemap entries should also use `/pubs/<slug>/`, not `/pubs/<slug>/index.html`

### 4. Make Draft Publication Validation Conditional

Today public publication records require complete core assets.
That should stay true for public pages.

For draft publications, validation should be lighter.

Recommended draft rule:

- draft publication pages only require a valid `title`
- public publication pages require the full current publication record plus
  canonical assets

That lets `make mkpub` create a minimally useful draft without forcing paper,
BibTeX, abstract, and images to exist immediately.

### 5. Update Publication Scaffolding To Be Directory-Local

After cutover, `make mkpub` should create:

- `pubs/<slug>/publication.json`
  with `"draft": true`
- `pubs/<slug>/<slug>-abstract.md`
- `pubs/<slug>/<slug>.bib`

It should **not** create a top-level `pub-<slug>.dj` stub anymore.

### 6. Treat Site-Wide Link Updates As Part Of The Cutover

The cutover is not complete until authored links are updated.

Current authored root-level publication links live mainly in:

- [index.dj](/Users/ztatlock/www/ztatlock.github.io/index.dj)
- [news.dj](/Users/ztatlock/www/ztatlock.github.io/news.dj)
- [publications.dj](/Users/ztatlock/www/ztatlock.github.io/publications.dj)

These should be updated from:

- `pub-<slug>.html`

to:

- `pubs/<slug>/`

### 6a. Make Validation And Cleanup Aware Of Nested Publication HTML

Today several checks only look at top-level `*.html` files or top-level draft
page outputs.

After cutover, they need to understand nested publication outputs too:

- placeholder checks must scan `pubs/*/index.html`
- broken-link checks must scan both top-level and publication-directory HTML
- draft-output checks must ensure draft publication `pubs/<slug>/index.html`
  files are not tracked
- `make clean` must remove generated `pubs/*/index.html` outputs

### 7. Delete Root-Level Publication Outputs Decisively

Because backward compatibility is a non-goal, the clean end state is:

- delete all top-level `pub-<slug>.dj`
- delete all top-level `pub-<slug>.html`
- do not add redirect shims

This should be a clean cut, not a long dual-route compatibility period.

## Recommended Execution Plan

### Phase 1: Add Route And Status Abstractions

Before changing public output paths, introduce the internal concepts needed for
the new model:

- publication-local draft status in `publication.json`
- publication route helpers for:
  - canonical URL
  - body-link generation
  - output file path
- validation that understands publication discovery from `pubs/*/publication.json`

This phase is about making the code understand the new model cleanly.

### Phase 2: Flip Publication Outputs To `pubs/<slug>/index.html`

In one coherent cutover:

- change publication output targets
- update sitemap generation
- update metadata canonical URLs
- update generated body links
- update authored publication links in root pages
- update validators/checks for nested publication HTML

At the end of this phase, publication pages should already be served from:

- `pubs/<slug>/index.html`

### Phase 3: Remove Root-Level Publication Stubs And Outputs

Once the cutover build is correct:

- delete top-level `pub-<slug>.dj`
- delete top-level `pub-<slug>.html`
- update `mkpub` scaffolding
- update repo docs and root-layout policy

Conceptually, this is a cleanup phase.
Practically, it may land in the same commit as Phase 2 if the implementation
is clean enough.

## Why This Should Happen Now

The publication-local record migration is already complete.

That means the publication stubs are no longer carrying real authored content;
they are just an operational relic from the migration path.

So the next clean structural simplification is exactly this one:

- move publication output to the publication directory
- remove the fake top-level publication layer

This is the point where the repo can become more rational without taking on a
different large campaign at the same time.

## Open Questions

These are the only meaningful design questions still left before
implementation:

1. `draft: true` vs. a separate status field in `publication.json`
   Recommendation: use `draft: true` first.
2. Whether to land Phase 1 and Phase 2 separately or together
   Recommendation: separate conceptually, but decide based on code cleanliness.
3. Whether to add a convenience alias for building one publication page
   after the cutover
   Recommendation: optional, not required for the first implementation.

## Recommendation Summary

The recommended long-term steady state is:

- ordinary pages continue as top-level `*.dj` -> top-level `*.html`
- publication pages become `pubs/<slug>/publication.json` ->
  `pubs/<slug>/index.html`
- the top-level publication stubs and root-level publication outputs disappear

That is the cleanest and most coherent publication layout for this repo.
