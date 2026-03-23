# Route/Build Engine Slice 5

Status: Implemented

This note defines the next implementation slice after the publication-bundle
checkpoint in
[route-build-engine-slice-4.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/route-build-engine-slice-4.md).

Slice 4 removed the new engine's architectural dependence on top-level
publication stubs. That was the last big publication-specific mismatch.

Two pre-source-move gaps remain:

- the preview path still does not own source-level metadata validation
- static handling is still bridge-shaped instead of a true `site/static/`
  copy-tree model

This slice exists to close those two gaps cleanly before any real source files
move into `site/`.

## Why This Slice Matters

Right now the new system is close, but not yet ready for the real source move.

What is already true:

- the preview builder is route-aware
- the preview builder is source-layout-aware
- publication pages are bundle-first in the new engine
- preview sitemaps and artifact validation are route-driven

What is now true after this slice:

- `check-preview` validates source invariants, built preview artifacts, and
  route-driven preview sitemaps
- `check-preview` also carries the temporary publication-stub bridge check, so
  the top-level command surface stays coherent during the transition
- config-driven source validation lives in the new path instead of only in the
  legacy validator
- a non-root `static_source_dir` behaves like a true recursive copy tree
- `site/static/img/...` is now treated as part of the static tree, not as a
  separate conceptual source root
- repo-root static handling remains sharply isolated as transitional bridge
  behavior

If we move source files into `site/` before fixing those two things, the source
move will still be partly architectural instead of mostly mechanical.

That is exactly what this slice is meant to avoid.

## Slice Goal

Make the preview path authoritative enough that the actual source move is
mostly:

- moving files
- flipping config defaults
- deleting bridge assumptions

not inventing more architecture during the move.

## Final Invariants For This Slice

At the end of slice 5, these are now true:

1. `check-preview` validates both:
   - source invariants
   - built artifacts
2. Source validation for the new path is driven by configured roots, not by
   root-only assumptions.
3. A configured `static_source_dir` that is **not** the repo root behaves like
   a simple recursive copy tree.
4. The current repo-root bridge still works without introducing a second
   permanent architecture.
5. Generated preview artifacts such as `sitemap.txt` and `sitemap.xml` are
   explicit reserved names, not silent static-file collisions.
6. The preview path remains simpler and more truthful after the change, not
   more conditional overall.

These are the things that must be true before the real `site/` move.

## Design Principle

This slice should still be narrow.

It should not:

- move real repo files into `site/`
- change deployment
- retire the legacy build
- redesign talks/students/CV projections

It should only do the last readiness work that the real source move depends on.

## Key Simplification Targets

### 1. New-Path Source Validation Becomes Real

Today:

- [validate_site.py](/Users/ztatlock/www/ztatlock.github.io/scripts/validate_site.py)
  owns source metadata validation
- [validate_preview_build.py](/Users/ztatlock/www/ztatlock.github.io/scripts/validate_preview_build.py)
  only validates built preview HTML plus sitemaps

That is not good enough for the eventual authoritative build.

We want:

- one config-driven source-validation layer usable by the new path
- one artifact-validation layer for built output
- one thin preview entrypoint that runs both

Legacy-only stub-sync validation may remain separate as bridge glue, but the
new path should not depend on legacy-only validation for ordinary source
correctness.

### 2. `site/static/` Must Mean What It Says

The final architecture says:

- ordinary static source files under `site/static/` are copied into `build/`
  unchanged
- generated build artifacts such as sitemaps are not source files and therefore
  use explicit reserved names

Before this slice, the preview path still used bridge logic:

- curated root filenames
- root `*.txt`
- root standalone `*.html`
- a separate conceptual `img/` source root

That was the right bridge shape, but it is not the final model.

So this slice should make the configured `static_source_dir` behave as a true
copy tree when we point it at a real `site/static/` layout.

The bridge behavior for the current repo root may remain temporarily, but it
should be isolated and obviously transitional.

## Recommended Implementation Order

### Step 1: Extract Shared Source Validation For The New Path

Add a small config-driven source-validation module under `scripts/sitebuild/`.

Suggested responsibilities:

- validate ordinary-page front matter from configured `page_source_dir`
- validate publication metadata/image-path invariants from configured
  `publications_dir`
- validate any new-path source assumptions that should hold before rendering

Keep legacy-only concerns separate:

- raw `*.meta` rejection can stay legacy-only
- publication stub-sync validation can stay a bridge-specific check

Stop and reflect:

- Is the split between source validation and artifact validation cleaner after
  this step?
- Are we keeping the new path free of legacy-root assumptions?

If not, stop and simplify before proceeding.

### Step 2: Make `check-preview` Run Source Validation Too

Update the preview validation path so it validates:

- source correctness from configured roots
- built artifact correctness under `build/`
- preview sitemap correctness

The preview path should then become the first place where the future system's
full safety story is visible.

Keep the entrypoint thin.

Do not merge all validation into one giant module.

Stop and reflect:

- Is `check-preview` now closer to the eventual authoritative validator?
- Did we add any validation logic that obviously belongs somewhere else?

### Step 3: Generalize Static Discovery For Real Static Trees

Refactor static route discovery into two explicit ideas:

1. current root-layout bridge behavior
2. real recursive static-tree behavior

The goal is not to keep both forever.
The goal is to isolate the bridge and make the final model obvious.

The preferred end state for configured non-root static trees is:

- every file under `static_source_dir` becomes one static route
- output path is the file's path relative to `static_source_dir`
- no curated filename list
- no separate `img/` special case in the final model

If the bridge still needs a temporary special case while `static_source_dir`
points at the repo root, keep that logic sharply isolated so it can be deleted
after the source move.

Stop and reflect:

- Did this step reduce long-term complexity, or only move it around?
- Is the bridge behavior now clearly separable from the final model?

If the answer is no, stop and simplify before continuing.

### Step 4: Add Alternate-Layout End-To-End Tests

Add focused tests using a temp layout shaped like the real target:

- `site/pages/`
- `site/pubs/`
- `site/static/`
- `site/templates/`
- `site/data/`

The tests should prove:

- preview build works from the target-style layout
- recursive static copy works for nested files
- metadata image-path validation works from configured roots
- `check-preview` fails for bad source metadata, not just bad built artifacts

Keep the tests small and explicit.

They should read like executable invariants, not giant fixtures.

### Step 5: Reassess Before The Real Source Move

At the end of the slice, stop and inspect:

- whether any real blocker to the actual file move still remains
- whether the bridge static behavior is the only clearly temporary branch left
- whether `build-preview` / `check-preview` are now close enough to become the
  authoritative build/check commands after the source move

If the answer is yes, the next phase should be the actual move into `site/`.

## Tests We Explicitly Want

These are the high-value tests this slice should add or strengthen.

### Source Validation Tests

- ordinary page with front-matter `image_path` under configured
  `site/static/img/` passes
- ordinary page with missing configured image path fails
- publication metadata with configured publication-local image path passes
- publication metadata with missing configured image path fails

### Static Route Tests

- nested files under configured `site/static/` become static routes
- standalone static HTML under configured `site/static/` copies through
- `site/static/img/...` works without a separate conceptual source root in the
  final model

### End-To-End Preview Tests

- target-style temp tree builds into `build/` correctly
- `check-preview` catches source metadata problems before or alongside artifact
  checks
- publication bundle routes still work in the target-style layout

## What To Watch For

If any of these happen, stop and ask for help before continuing:

- static-route logic starts needing more than one or two tightly bounded
  bridge-specific branches
- source validation starts wanting access to built artifacts
- preview validation grows into a single giant mixed-responsibility module
- the slice starts implying deployment or source-file moves directly

Those would be signs the scope is drifting.

## Lessons Learned

- Draft publication records should not be forced to satisfy public-asset
  metadata requirements. Draft status needs to short-circuit publication
  metadata image validation just like it short-circuits public-page emission.
- Source validation is cleaner when canonical record validation and temporary
  bridge validation are separate concerns. The new path should validate
  publication bundles directly, while legacy stub-sync checks remain bridge
  glue only.
- Recursive static-tree behavior is easy to explain and test once the bridge
  root-layout logic is isolated into its own branch instead of being mixed
  through the final model.
- `site/static/img/...` is simpler when it is treated as ordinary static-tree
  content all the way through route discovery and metadata validation, instead
  of keeping a second path knob alive in config.
- A small direct integration test for `validate_preview_build.py` was worth
  having. It proved that preview validation now reports source metadata
  problems, not just built-artifact problems.
- Generated preview outputs like `sitemap.txt` and `sitemap.xml` need to be
  explicit reserved names in the static-tree model. Failing fast is cleaner
  than silently copying and then clobbering those files.

## Expected Outcome

If slice 5 goes well, we should be able to say:

- the new build path understands the final source layout well enough
- the new validation path is authoritative enough
- the remaining work is mostly moving files and flipping defaults

That is the checkpoint we want before the real source move.
