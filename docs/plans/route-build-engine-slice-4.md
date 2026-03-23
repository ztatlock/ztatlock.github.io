# Route/Build Engine Slice 4

Status: Implemented in preview engine

This note defines the next implementation slice after the source-layout-aware
preview-builder checkpoint in
[route-build-engine-slice-3.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/route-build-engine-slice-3.md).

The strategic decisions behind this slice are now explicit:

- the legacy root-served build has no long-term architectural value
- the legacy build should be frozen and treated only as a temporary reference
- preserving content matters; preserving old publication URLs does not
- redirect shims for old `pub-*.html` routes are explicitly a non-goal

So the next clean move is **not** to spend more effort teaching the old build
new tricks.

The next clean move is to make the **new** engine align more closely with the
final source model by removing its remaining dependence on top-level
publication stubs.

Current checkpoint:

- preview publication-page discovery now comes from
  `publications_dir/*/publication.json`
- preview publication draft/public status now lives in `publication.json`
- preview publication rendering no longer requires top-level `pub-*.dj` stubs
- ancillary publication tooling like the artifact inventory no longer needs
  top-level `pub-*.dj` discovery either
- the legacy root build still keeps the stubs temporarily, so scaffolded
  draft status must stay in sync in both places during the transition

## Why This Slice Matters

After slice 3, the preview engine is source-layout-aware, but it still carries
two important bridge assumptions:

- publication page discovery still depends on top-level `pub-*.dj` stubs
- publication draft/public status still lives in those stubs rather than in
  the publication-local record

Those assumptions are now the main thing preventing a later clean source move.

The publication-local migration is already complete, and the publication stubs
no longer carry real authored content. They are just operational leftovers from
the transition.

So this slice is about deleting one more layer of fake structure from the new
engine before any real file move.

## Slice Goal

Make the new engine treat publication bundles as the canonical source of
publication page existence and status.

At the end of this slice:

- publication-page discovery in the preview engine should come from
  `publications_dir/*/publication.json`
- publication draft/public state should live in `publication.json`
- the preview engine should no longer depend on `pub-*.dj` stubs to render
  publication pages
- the old route shape should not constrain the new engine

This should make the later source move much more direct:

- move real pages into `site/pages/`
- move real publication bundles into `site/pubs/`
- delete publication stubs instead of migrating them forward

This is now true for the preview engine. The remaining stub dependency is
legacy-build-only transition glue.

## Core Principle

Keep this slice narrow.

Do **not** try to solve every remaining cutover concern at once.

In particular, this slice should focus on the publication source model, not on:

- deployment cutover
- legacy root-build modernization
- full `site/static/` generalization
- talks/students/CV data projections

The point is to remove one major architectural mismatch cleanly.

## Strategic Position

The legacy build should now be treated like this:

- useful as a short-term oracle while the new system becomes authoritative
- not worth further architectural investment
- something to retire, not evolve indefinitely

That means we should prefer implementation work that strengthens the new engine
directly, even if it leaves the old build untouched for a little longer.

## What This Slice Should Change

### 1. Publication Draft Status Becomes Publication-Local

Add optional `draft: true` to `publication.json`.

Recommended rule:

- public publication records require the full canonical asset contract
- draft publication records require only the minimum fields needed to exist
  coherently in source

The current recommendation remains:

- use `draft: true`
- do not invent a more elaborate status model yet

This is the simplest way to make publication status part of the publication
bundle itself.

### 2. Publication Discovery Comes From Publication Records

The preview engine should discover publication pages from:

- `publications_dir/*/publication.json`

not from:

- `page_source_dir/pub-*.dj`

That means route discovery should treat publication bundles as the source of:

- publication existence
- publication page keys/slugs
- publication page draft/public status

This is the main architectural change in the slice.

### 3. Publication Rendering Must Not Require Stubs

The shared render/source path should be able to render a publication page from
publication-local inputs alone:

- `publication.json`
- abstract
- BibTeX
- canonical assets
- optional `extra.dj`

The simplest acceptable implementation may still use an internal synthetic
page identifier like `pub-<slug>` for some helpers during the transition.

That is okay **if**:

- it is purely internal
- publication existence does not depend on a stub file
- a later file move would not require bringing stubs forward

In other words: internal compatibility glue is acceptable; source-model
dependency on stubs is not.

### 4. Tests Must Prove Bundle-Only Publication Builds

Add focused tests that prove the new engine can:

- discover a publication page from `publication.json` alone
- honor `draft: true`
- render a publication page without a top-level stub
- reject invalid draft/public publication states cleanly

This is crucial.

The slice is only complete if the tests prove the engine no longer needs the
stub layer.

## What This Slice Should Explicitly Not Do

Slice 4 should **not**:

- move real repo files into `site/`
- change deployment
- add redirect pages or compatibility aliases
- keep old publication URLs alive
- fully redesign static-file handling
- change ordinary-page routing

Those can come later from a cleaner base.

## Recommended Implementation Order

### Step 1: Extend The Publication Record Schema

Add and validate optional:

- `draft: true`

Keep the schema minimal.

Suggested invariants:

- `draft` must be boolean if present
- public records require the current full canonical publication contract
- draft records may omit some public-only assets, but must still have coherent
  identity fields

Stop and reflect:

- is the draft/public rule simple enough to explain in one paragraph?
- is there any pressure to add more status states?

If yes, the slice is drifting.

### Step 2: Refactor Publication Route Discovery

Change the preview route-discovery path so publication routes come from
publication records, not stub pages.

Keep the route model simple:

- `kind = publication_page`
- `key = slug`
- `source_paths` derived from bundle-local canonical inputs
- `public_url = /pubs/<slug>/`
- `output_relpath = pubs/<slug>/index.html`

Stop and reflect:

- does the route model get simpler after this change?
- are we deleting assumptions, or adding transitional branching?

If the code becomes more conditional instead of more direct, reassess before
continuing.

### Step 3: Refactor Rendering To Be Bundle-First

Update the shared render/source path so publication pages can be rendered from
bundle-local inputs alone.

This may require:

- a new publication-page loader path keyed by slug
- or a slightly more route-aware render entrypoint

Prefer the smallest change that removes real stub dependency.

Do **not** redesign the whole rendering API unless it clearly simplifies the
code.

Stop and reflect:

- is the publication render path now easier to explain than before?
- is there still any fake authored source layer left in the preview engine?

### Step 4: Add Bundle-Only Integration Tests

Add focused unit/integration tests for:

- discovery without stubs
- rendering without stubs
- draft publication behavior
- public publication validation behavior

If a future source move would still feel scary after reading these tests, the
slice is not done yet.

### Step 5: Reassess Before Any File Move

At the end of the slice, pause and inspect:

- what publication-specific transitional assumptions still remain
- whether static handling now becomes the main remaining gap
- whether the next move should be:
  - one last focused source-move-readiness slice
  - or, if the audit is unexpectedly cleaner than expected, the actual source
    move into `site/`

## Lessons Learned

- Publication existence and draft/public status are much simpler when they
  live in the publication bundle instead of a separate stub file.
- The preview engine can still use an internal synthetic page stem like
  `pub-<slug>` without making that stub an authored-source dependency.
- During the bridge period, the legacy root build should validate that
  `pub-<slug>.dj` draft status stays in sync with `publication.json`.
- New scaffolds must default to `"draft": true`, otherwise record-driven
  publication discovery makes half-finished scaffolds appear public too early.
- Ancillary publication tooling should move to record-driven discovery early;
  otherwise those tools quietly become future cutover traps even after the
  main preview engine is clean.
- Publication-source cleanup is not the same as full source-move readiness.
  Static-tree behavior and authoritative new-path source validation still need
  their own final readiness slice before real file moves.

Do **not** roll directly into the file move without this checkpoint.

## Testing Expectations

This slice should add or expand tests for:

- publication record schema validation
- draft/public publication validation
- publication route derivation from records
- publication rendering without stubs
- end-to-end preview build from a temporary `site/pubs/` tree with no
  top-level publication pages

Keep the tests small and explicit.

The target is high confidence with narrow tests, not giant end-to-end fixtures.

## Why This Is The Right Size

This is smaller than a full source move because:

- it leaves real files where they are
- it does not change deployment
- it does not require ordinary-page changes

But it is larger than a trivial refactor because:

- it removes a whole fake source layer from the new engine
- it directly supports the final architecture
- it reduces the risk of the later `site/` move substantially

That makes it the right next chunk:

- reviewable
- meaningful
- architecturally clean

## Expected Checkpoint After Slice 4

After this slice, we should have:

- a preview engine whose publication model matches the intended steady state
- publication-local status and discovery
- no architectural dependence on top-level publication stubs in the new system

At that point, the next major move should be much clearer:

- either move real source into `site/`
- or do one last focused static-source cleanup if that is still the remaining
  awkward seam
