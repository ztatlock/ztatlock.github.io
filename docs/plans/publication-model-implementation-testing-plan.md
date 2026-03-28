# Publication Model Implementation / Testing / Migration Plan

Status: slice 1 implemented; slices 2-4 pending

It builds on:

- [publication-model-proposal-a-conservative-refinement.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-proposal-a-conservative-refinement.md)
- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-corpus-reality-check.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-reality-check.md)
- [publication-model-corpus-refinement-pass.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-corpus-refinement-pass.md)
- [publication-model-full-review-synthesis.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-full-review-synthesis.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [service-redesign-implementation-testing-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-redesign-implementation-testing-plan.md)

## Purpose

This note switches the publication-model work from design review into
implementation, testing, and migration planning.

The design question is now narrow enough:

- Proposal A is the leading authored-schema direction

So the next job is not to keep redesigning the authored shape.
It is to decide how to land that shape safely, test it well, and migrate the
real publication corpus without paying for avoidable compatibility cruft.

## Goal

Implement Proposal A in a way that:

- preserves canonical publication facts
- keeps the build/check path trustworthy throughout migration
- retires slug-year display semantics everywhere they still survive
- gives current consumers honest access to:
  - canonical publication year
  - compact venue labels
  - semantic `pub_type`
  - clearer `local_page` semantics
  - explicit identifiers
- and avoids a long-lived dual-schema publication layer

## Main Execution Principle

Treat this as a **fixture-first loader foundation plus coordinated cutover**
problem, not as a long compatibility-bridge campaign.

Why this is different from service:

- the current publication domain is still one bundle-local corpus under
  `site/pubs/`
- the current live consumers are bounded and known
- the schema changes are meaningful but still relatively local:
  - `pub_year`
  - `venue_short`
  - `pub_type`
  - `detail_page -> local_page`
  - `identifiers`
- and a long publication compatibility shim would mostly add confusion rather
  than durable value

That means:

- first make the Proposal A schema executable in code and tests on focused
  fixtures
- then make the real migration decisions explicitly against the real corpus
- then migrate canonical bundle data and cut live publication consumers over
  together
- then clean up dead old-field assumptions immediately rather than keeping a
  second publication model around

Important framing:

- Proposal A is primarily the authored on-disk schema direction
- it still allows richer normalized in-memory publication objects after parse
  if that makes consumer or tooling code cleaner

So the implementation may use richer loaded structures internally without
forcing the authored JSON to mirror that full grouping directly.

## Recommended Slice Order

### Slice 1. Loader / Validator Foundation

Implement the Proposal A schema and validation rules in code before touching
the real publication corpus.

This foundation slice is now implemented in side-by-side code and focused
tests:

- [publication_record_a.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record_a.py)
- [test_publication_record_a.py](/Users/ztatlock/www/ztatlock.github.io/tests/test_publication_record_a.py)

Scope:

- extend or replace the current publication loader so the target authored
  schema is executable:
  - `local_page`
  - `listing_group`
  - required `pub_type`
  - `pub_year`
  - optional `pub_date`
  - `venue`
  - `venue_short`
  - `primary_link`
  - `identifiers`
- keep the first-pass author model conservative:
  - ordered `authors`
  - `name`
  - optional `ref`
- make the first-pass `pub_type` vocabulary explicit and validated
- define the canonical collection-ordering rule once so optional `pub_date`
  does not leave consumers guessing:
  - use exact `pub_date` when present
  - fall back to `pub_year`
  - keep a stable tie-break
- preserve current publication-local `talks` support without conflating it
  with the invited/public talks domain
- explicitly support the thin/rich local-page split:
  - thin external-destination bundle
  - richer local-page bundle
- if useful, introduce a richer normalized in-memory publication object after
  parse, but keep that an internal code detail rather than a second authored
  schema
- do **not** migrate real `site/pubs/*/publication.json` files yet
- do **not** cut any live consumer over yet

Why first:

- it turns Proposal A into executable contract
- it isolates loader/validation mistakes from corpus-migration mistakes
- it proves that “simple authored JSON, richer loaded model” is viable before
  touching real data

Invariant after slice 1:

- Proposal A is executable in code on focused fixtures
- the repo has tests covering the new field semantics directly
- current live publication data and consumers are still unchanged

### Slice 2. Corpus Migration Tables And Reality-Checked Decisions

Turn the already completed review/audit work into explicit migration inputs for
the real indexed corpus.

Scope:

- produce or check in the exact corpus-backed assignment tables needed for the
  real cutover:
  - `pub_year`
  - cleaned `venue`
  - `venue_short`
  - `pub_type`
  - `local_page`
- record the known year-mismatch cases that must remain honest after cutover:
  - `2016-nsv-fpbench`
  - `2017-icalepcs-neutrons`
  - `2018-popl-disel`
- record the known `listing_group` / semantic-type divergence pressure:
  - `2016-netpl-bagpipe`
  - `2018-mapl-relay`
- record the current compact-venue equality or awkward-label cases so the
  migration does not drift into heuristics:
  - `<Programming>`
  - `SECURITY`
  - `CORRECTNESS`
  - `SPLASH-E`
- decide the first-pass identifier backfill posture:
  - what is required now
  - what may remain absent
  - what is worth adding opportunistically during the main migration
- keep `listing_group` explicit as a retained current-consumer grouping field,
  not as authoritative semantics

Why this deserves its own slice:

- the main migration risk is no longer abstract schema shape
- it is making the real 69-bundle corpus decisions once, consistently, and
  visibly
- doing that work explicitly avoids ad hoc bundle-by-bundle drift during the
  actual cutover

Invariant after slice 2:

- the exact migration decisions for the indexed corpus are explicit
- unresolved semantic cases are narrow and named
- the actual cutover can be executed as a deliberate migration instead of a
  sprawling series of guesses

### Slice 3. Coordinated Canonical Data And Consumer Cutover

Migrate the real publication corpus and cut live consumers over in one bounded
slice.

This should be the main implementation slice.
Unlike service, it should not rely on a long-lived compatibility adapter.

Scope:

- migrate all non-draft `site/pubs/*/publication.json` bundles to Proposal A:
  - add `pub_year`
  - clean `venue`
  - add `venue_short`
  - rename `detail_page` to `local_page`
  - keep or set `primary_link` for thin bundles
  - add required `pub_type`
  - add `identifiers` where chosen by slice-2 policy
- update the canonical publication loader and validator to expect only the new
  authored schema
- update all current publication consumers and helpers that still depend on
  old field semantics:
  - `scripts/publication_record.py`
  - `scripts/publication_index.py`
  - `scripts/sitebuild/page_projection.py`
  - `scripts/build_pub_inventory.py`
  - `scripts/page_source.py`
  - `scripts/page_metadata.py`
  - `scripts/sitebuild/route_discovery.py`
  - `scripts/sitebuild/source_validate.py`
- retire slug-year display in all current publication renderers:
  - `/pubs/`
  - CV indexed publications
  - homepage recent publications
- update homepage recent-publication selection to anchor to canonical latest
  `pub_year`, not `pub_date.year` or slug parsing
- keep slug year as path identity / validation convention only, not display
  truth
- keep current public grouping behavior through retained `listing_group`
  placeholders
- make homepage compact rendering consume:
  - `venue_short`
  - canonical year from `pub_year`
- keep `primary_link` explicit for title-destination policy on thin bundles
- update current inventory and metadata tooling to use `local_page` and other
  new field names directly
- delete the old field assumptions immediately instead of preserving a dual
  publication schema

Why one coordinated slice:

- the live publication surface is bounded enough that the real cutover can be
  reviewed as one semantic change
- a compatibility bridge would mostly preserve old names like `detail_page`
  and old habits like slug-year rendering longer than necessary
- the corpus migration is already large enough that splitting it into “new
  data with old consumers” and “old consumers with new data” would add more
  tension than safety

Invariant after slice 3:

- the canonical publication corpus uses Proposal A
- all live publication consumers and validators use Proposal A directly
- no live code still depends on:
  - `detail_page`
  - slug-year display parsing
  - the old field contract
- current `/pubs/`, CV, homepage, and inventory behavior remain coherent and
  trustworthy

### Slice 4. Post-Cutover Cleanup And Follow-On Enrichment

After the main cutover, clean up the remaining narrow seams without reopening
the model.

Scope:

- remove dead helper code, tests, and docs that still assume the old field
  names
- tighten or expand identifier backfill where it clearly pays off
- consider whether any obvious publisher-link derivations from DOI are now
  worth doing
- revisit scaffolding/templates so newly created publication bundles start in
  the new schema immediately
- only after the model cutover settles, revisit downstream curation questions
  such as the top-of-CV `Selected Recent Highlights` block

Invariant after slice 4:

- the repo no longer carries dead publication-model terminology
- new publication authoring starts from the new schema by default
- remaining publication work is enrichment or new-consumer work, not migration

## Testing Strategy

The publication-model migration should be tested in layers.

### Schema / Validation Tests

Add focused tests for:

- required vs optional fields in the new schema
- `local_page` rules for:
  - thin bundles
  - richer local-page bundles
- `primary_link` validity for thin bundles
- required small-vocabulary `pub_type`
- `listing_group` remaining validated but conceptually distinct from
  `pub_type`
- `pub_year` required for indexed non-draft bundles
- `pub_date` optional exact-date semantics
- collection-ordering fallback when exact `pub_date` is absent
- `venue_short` required for indexed non-draft bundles
- `identifiers` object validation
- author shape remaining conservative:
  - `name`
  - optional `ref`
- publication-local `talks` still validating independently of the talks domain

### Normalization / Internal-Model Tests

If the implementation introduces a richer normalized in-memory publication
object, add focused tests for:

- authored flat field parsing into normalized time/venue/classification
  concepts
- canonical year sourced from `pub_year`, not slug parsing
- title-destination policy sourced from:
  - `local_page`
  - `primary_link`
- compact-publication rendering using `venue_short`
- inventory/tooling access to identifiers without scraping display strings

### Corpus Migration Tests

Add focused tests or audits for:

- every non-draft indexed bundle now carrying:
  - `pub_year`
  - `venue_short`
  - `pub_type`
  - `local_page`
- cleaned `venue` strings no longer duplicating compact labels in
  parenthetical suffixes
- known year-mismatch bundles remaining honest after migration
- known `listing_group` / semantic `pub_type` divergences remaining explicit
- compact-label equality cases such as `<Programming>` staying honest

### Consumer Regression Tests

Add or update tests for:

- `/pubs/` rendering canonical year from `pub_year`
- CV indexed-publication rendering canonical year from `pub_year`
- homepage recent-publication rendering using:
  - canonical year from `pub_year`
  - compact venue from `venue_short`
- homepage recent-publication selection anchoring to latest canonical
  `pub_year`
- title-link behavior for:
  - thin bundles
  - rich local pages
- current grouping behavior still flowing through retained `listing_group`

### Inventory / Metadata / Validation Tests

Add or update tests for:

- `build_pub_inventory.py` using `local_page`
- publication metadata validation skipping thin bundles via `local_page`
- route discovery using `local_page`
- source validation rejecting old-field assumptions once the cutover lands

## Migration-Sensitive Corpus Cases

The plan should keep these specific current cases visible during execution:

- canonical year vs exact-date mismatches:
  - `2016-nsv-fpbench`
  - `2017-icalepcs-neutrons`
  - `2018-popl-disel`
- likely `listing_group` / semantic `pub_type` divergence:
  - `2016-netpl-bagpipe`
  - `2018-mapl-relay`
- honest compact-label equality:
  - `<Programming>`
- venue/container seam worth preserving as a named future question:
  - `2019-siga-carpentry`

These should be explicit fixture or corpus-check cases, not just remembered
informally during the migration.

## Non-Goals For This Plan

This implementation plan should **not** silently expand into:

- a venue registry
- canonical venue identity across papers
- a `person_key` author-identity campaign
- unifying publication-local `talks` with the invited/public talks domain
- forcing `Book Chapters` or `Books` into the indexed publication model
- a full DOI/BibTeX/publisher-link normalization pipeline
- a top-of-CV highlights redesign

Those may become later slices.
They are not prerequisites for landing Proposal A.

## Recommended Pre-Commit Verification

Use the repo’s sequential authoritative verification path:

- `make verify`

Do **not** run overlapping build/check commands in parallel.
