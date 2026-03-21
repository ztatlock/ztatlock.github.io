# Metadata Source Comparison

This note compares the plausible places page metadata could live after the
completion of the raw `*.meta` cleanup.

The goal here is not to make an implementation leap immediately.
The goal is to compare the options in the context of this repo as it exists
today, make the tradeoffs explicit, and choose a direction that biases toward
the long-term design.

## Current State

As of March 21, 2026:

- 41 public `*.dj` pages exist
- 20 public non-publication pages currently source metadata from YAML front
  matter in `*.dj`
- all current public publication pages now source metadata from
  `pubs/<slug>/publication.json`
- `manifests/publication-metadata.json` is currently empty and retained only
  as a temporary legacy fallback
- 7 draft pages exist and may intentionally omit metadata while they remain
  drafts
- public pages no longer use raw `*.meta` sidecars

The current structured metadata schema is intentionally small:

- required:
  - `description`
- optional:
  - `share_description`
  - `image_path`
  - `title`

In practice, the old fallback publication manifest is now empty. This is a
strong sign that defaults are working and that the core question is
mostly about *where* metadata should live, not about inventing a richer
metadata schema.

## Design Constraints

Any next-step design should respect these constraints:

- bias toward the long-term architecture, not just the smallest local change
- avoid reintroducing raw copied HTML metadata
- keep Djot as the current content format for now
- avoid a risky big-bang Jekyll or SSG migration
- preserve straightforward validation and scaffolding
- preserve draft flexibility
- avoid making the already-flat repo root harder to navigate
- improve agent ergonomics by reducing split-brain edits across files

## Candidate A: Shared Manifests

Keep the current model:

- `manifests/publication-metadata.json` for publication pages

### Strengths

- already implemented and stable for publications
- easy to validate centrally
- easy to inspect global metadata coverage
- low migration cost because the repo already uses the publication manifest
- no Djot parsing changes required
- shared metadata is easy to audit globally when it exists

### Weaknesses

- metadata is still physically separate from page content
- editing a page often means touching two files
- the split between page source and metadata is still artificial
- two manifests means the system is only partially unified
- shared manifests are less conventional than front matter
- this is not the strongest bridge to a future SSG

### Assessment

This was the initial publication-side transition model, but it is no longer
the current steady state.

## Candidate B: Page-Local Sidecars

Move metadata next to each page source in adjacent structured files, for
example:

- `about.page.yaml`
- `pub-2024-asplos-lakeroad.page.yaml`

### Strengths

- metadata moves closer to content
- avoids parsing front matter out of Djot sources
- can be adopted incrementally page by page
- easier to reason about a single page in isolation than with shared manifests

### Weaknesses

- increases file count substantially
- worsens discoverability in an already flat root directory
- still keeps content and metadata in separate files
- less conventional than front matter
- does not buy as much future SSG compatibility as front matter
- publications already have many related files, so more sidecars may feel noisy

### Assessment

This is a plausible transitional design, but it feels like the worst of both
worlds here: more clutter than manifests, but less unity than front matter.

## Candidate C: YAML Front Matter In `*.dj`

Store metadata at the top of each Djot page source, for example:

```yaml
---
description: Where and how to reach me.
image_path: img/favicon-meta.png
---
```

followed by the existing Djot page body.

### Strengths

- strongest locality: content and metadata live together
- one file per page instead of a page plus manifest row or sidecar
- common pattern that humans and agents both recognize easily
- strongest long-term bridge to Jekyll or another SSG
- reduces the cognitive split between page body and page metadata
- avoids adding even more files to the flat root

### Weaknesses

- Djot does not treat YAML front matter specially today
- the build would need a front-matter extraction step before title parsing and
  before feeding content to `djot`
- current title extraction from the first line of the file would need to change
- migration would touch many page source files
- scaffolding and validators would need another round of updates

### Assessment

This is the strongest long-term model if we keep the site custom for now but
still want to bias toward a future conventional SSG path.

## Comparison Summary

### Long-Term Architectural Fit

- best: YAML front matter
- middle: shared manifests
- weakest: page-local sidecars

### Short-Term Migration Risk

- safest: shared manifests
- middle: page-local sidecars
- riskiest: YAML front matter

### Repo Navigability In A Flat Root

- best: YAML front matter
- middle: shared manifests
- weakest: page-local sidecars

### Current Build Simplicity

- best: shared manifests
- middle: page-local sidecars
- weakest: YAML front matter

### Future SSG Compatibility

- best: YAML front matter
- middle: page-local sidecars
- weakest: shared manifests

## Recommendation

The recommendation is:

1. keep the current shared-manifest system as the stable operational state
2. choose YAML front matter as the long-term target for non-publication pages
3. keep publication metadata intentionally open for now
4. prototype front matter in a controlled mixed-mode implementation for
   non-publication pages first

This recommendation biases toward the long-term vision without forcing a
high-risk migration before we have tested the build and ergonomics or decided
whether publications eventually want a richer single source of truth than
"page metadata".

## Proposed Controlled Plan

### Phase 1: Mixed-Mode Prototype

Teach the build to support page-local front matter for non-publication pages
*in addition to* the current manifests.

This phase is now implemented and all current public non-publication pages
have migrated. The ordinary-page fallback path has now been removed because it
was empty and added complexity without adding real capability.

Rules:

- if a non-publication page has front matter, it wins
- publication pages now use `pubs/<slug>/publication.json`
- draft pages may still omit metadata entirely

This kept the repo safe while testing the long-term direction.

### Phase 2: Tiny Pilot

Pilot front matter on a very small non-publication set:

- one simple non-publication page
- one non-publication page with overrides such as `share_description`,
  `image_path`, or `title`

Success criteria:

- no output regressions
- title extraction still works cleanly
- build logic stays understandable
- editing ergonomics feel better, not worse
- the publication metadata path stays untouched during the pilot

Phase 2 succeeded and the migration broadened to all current public
non-publication pages without output regressions.

### Phase 3: Decision Point

After the pilot, decide explicitly:

- continue migrating to front matter
- or keep manifests as the long-term model

Do not drift into a migration accidentally.

### Phase 4: Broader Migration

If the pilot is clearly better, migrate in batches:

- public non-publication pages first
- revisit publications only after deciding whether they should remain
  metadata-only or become part of a broader publication data model
- ordinary pages now use front matter directly; revisit only if a future need
  for a shared ordinary-page manifest reappears

## Open Questions

- Should front matter carry only head metadata, or eventually other structured
  page-local facts too?
- Should publication pages eventually keep more structured publication data in
  the page source, or should publications move toward a broader canonical
  publication record that feeds pages, metadata, CV views, and inventories?
- If front matter lands, do we still want separate shared manifests for any
  cross-page global data in the future?
