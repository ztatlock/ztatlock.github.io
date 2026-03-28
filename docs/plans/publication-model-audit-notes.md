# Publication Model Audit Notes

Status: initial deep audit complete

It builds on:

- [publication-model-seams-and-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-seams-and-requirements.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-slice-5-recent-publications.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-5-recent-publications.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)

## Executive Summary

The current publication bundle model is still fundamentally sound.

The repo should **not** throw away the bundle-local publication architecture
that now powers:

- `/pubs/`
- the indexed-publication CV sections
- the homepage recent-publications block

But the audit confirms that the publication model has accumulated enough real
consumer pressure that a focused design review is warranted before large
further backfill.

The strongest current seams are:

1. `venue` is overloaded and should no longer carry both full and compact
   display semantics.
2. `detail_page` is real but semantically awkward; it describes local-page
   readiness, not publication existence.
3. `listing_group` is page-shaped and intentionally coarse, but likely too weak
   as the only publication classification forever.
4. canonical identifiers in `publication.json` are too thin, especially DOI.
5. the publication boundary around `Book Chapters` and possible future `Books`
   is still unresolved.

The audit also confirms an important negative conclusion:

- publication-local `talks` are **not** the same domain as the invited/public
  talks bundles, and the model review should preserve that separation.

So the right next move is:

- a focused publication-model redesign/refinement pass
- not a service-scale rewrite
- not a one-field tactical patch either

## Current Corpus Facts

The current non-draft indexed publication corpus under `site/pubs/` contains:

- `69` non-draft publication bundles
- `21` bundles with `detail_page: true`
- `48` bundles with `detail_page: false`
- `58` bundles with `listing_group: main`
- `11` bundles with `listing_group: workshop`

Primary-link usage among non-draft bundles:

- `43` use `primary_link: publisher`
- `5` use `primary_link: event`
- `21` have no `primary_link` because they already have local detail pages

Sparse-but-real optional publication fields:

- `4` bundles have non-empty `badges`
- `13` bundles have publication-local `talks`
- `14` bundles expose an `arxiv` link
- `19` bundles expose a `code` link
- `13` bundles expose a `project` link
- `6` bundles expose an `event` link
- `2` bundles expose a `demo` link

Badge values are currently only:

- `★ Distinguished Paper` (`3`)
- `★ Spotlight Paper` (`1`)

## Consumer Audit

### `/pubs/`

The publications index and local publication pages want the full,
bibliography-facing venue label.

They also want:

- full author lists
- badge rendering
- local vs external title-link policy
- publication-local extras such as videos/talk embeds

The current model serves those consumers reasonably well.

### CV Indexed-Publication Sections

The CV indexed-publication sections also want bibliography-style rendering,
just more compressed than `/pubs/`.

They do **not** currently need:

- compact venue acronyms
- rich local-page extras
- different publication typing beyond the current indexed grouping

So the current model also serves this consumer reasonably well.

### Homepage Recent Publications

This is where the model pressure surfaced most clearly.

The homepage wants:

- a small selected recent subset
- a compact renderer
- compact venue labels
- stable title-link policy that is still honest for thinner bundles

The homepage renderer is therefore the first current consumer that wants venue
semantics different from the existing bibliography-facing `venue` field.

## Field-By-Field Audit

### `venue`

This is the clearest current seam.

Observed fact:

- `68` of `69` current non-draft venue strings end in a terminal parenthetical
  token such as `(PLDI)`, `(ASPLOS)`, or `(TOG)`.
- the only current exception is:
  - `<Programming>`

That means the current corpus is very clearly carrying compact venue identity
inside the full `venue` display string.

This helped earlier consumers because:

- `/pubs/` and the CV both wanted a single full venue line

But it is now the wrong shape for compact consumers.

Current conclusion:

- a split such as `venue` plus `venue_short` now looks justified
- if that split lands, canonical `venue` should be cleaned up to remove the
  embedded acronym suffix rather than preserving duplication in both fields

### `detail_page`

Current semantics in code:

- `detail_page: true`
  - publication has a full local detail page
  - description metadata is required
  - local assets are required for rendering the body
- `detail_page: false`
  - publication is still canonical and indexed locally
  - title links route to `links[primary_link]`
  - local publication-body requirements do not apply

So `detail_page` is not the publication-existence bit.
It is the local-page-readiness bit.

The field is therefore doing real work.
But its name and its downstream implications are a little awkward.

The biggest current conceptual seam is:

- a publication bundle can be fully canonical for indexing purposes while still
  canonically linking away from the site at its title

That is a real architectural distinction and probably wants cleaner naming or
clearer surrounding semantics in the next design pass.

### `listing_group`

Current semantics:

- it is effectively a projected grouping key for `/pubs/` and the CV indexed
  sections
- the allowed values are only `main` and `workshop`

This was the right small field for the initial bundle/index campaign.
But it is also clearly a page-shaped classification.

Current conclusion:

- it is too soon to force a grand publication taxonomy
- but it is also fair to ask whether `listing_group` should remain the only
  explicit classification field

The current homepage cap/stickiness discussion already hints at pressure here:

- some future policies may want distinctions more semantic than
  `main|workshop`

### `badges`

Current state:

- very sparse
- rendered as plain strings
- currently only used for visible display, not selection policy

This means badges are not yet a crisis seam.
But they are now a plausible future policy seam because “award papers are
sticky” is already an anticipated idea for homepage overflow handling.

Current conclusion:

- free-form strings are acceptable for now
- but the next design pass should explicitly decide whether badges remain
  purely display-facing or gain some light structure

### `links`

The current links model is practical and mostly healthy.

Observed current link-key frequencies:

- `publisher`: `63`
- `code`: `19`
- `arxiv`: `14`
- `project`: `13`
- `event`: `6`
- `talk`: `5`
- `teaser`: `3`
- `demo`: `2`
- `vscode`: `1`

The strongest current seam is not the presence of link keys.
It is that some higher-value identifiers still only exist indirectly through
link URLs.

In particular:

- DOI is not currently a canonical field
- arXiv identifier is not currently a canonical field

Current conclusion:

- the model likely needs a few explicit identifier fields
- but should still tolerate intentional duplication with BibTeX and links

### `talks`

This field is healthy **if** the repo preserves the current domain boundary.

Observed facts:

- `13` bundles have publication-local talks
- there are `14` total publication-local talk entries
- only `2` talk-bearing bundles have Zach as the only speaker
- `11` talk-bearing bundles have only non-Zach speakers
- none of the current talk-bearing bundles mix Zach plus non-Zach speakers in
  the same publication-local talk set

That strongly supports the documented boundary:

- publication-local talks are usually conference/student/publication-specific
  talks or videos
- they are not the same domain as the invited/public talks page

Current conclusion:

- the next publication model pass should preserve this separation explicitly
- this is a place where the repo already knows something important and should
  avoid “improving” the model by collapsing domains

### BibTeX Relationship

The current publication architecture already treats `.bib` files as canonical
bundle assets for richer local pages.

The repo should **not** try to make `publication.json` and `.bib` perfectly
redundancy-free.

The audit supports the following direction:

- some duplication between `publication.json` and `.bib` is acceptable
- publication JSON should carry the facts that are genuinely useful to the
  site’s canonical consumers
- BibTeX should continue to exist as a publication-local bibliographic asset,
  not as the thing the whole site has to parse and normalize for every field

Current high-value candidate for canonical JSON:

- DOI

Likely later candidates depending on boundary decisions:

- arXiv identifier
- ISBN for books/chapters if those enter the model

## Boundary Audit

### Publication-Local Talks vs Invited/Public Talks

The boundary here is good and should stay.

The talks campaign already states this clearly, and the corpus evidence
supports it.

### `Book Chapters`

The current CV still has one authored `Book Chapters` entry.
That has remained outside the publication bundle boundary by explicit policy.

The current audit conclusion is:

- this is still a real boundary question
- it should not be silently resolved by inertia during ordinary publication
  backfill

It is reasonable for the next publication-model review to also consider:

- `Book Chapters`
- and possibly `Books`

at the same time.

That does **not** mean the answer must be “pull them in now.”
It means the boundary should be revisited deliberately while publication field
semantics are already under review.

## Backfill Pressure

This is one of the most important results of the audit.

The repo expects heavy future publication backfill, and current bundle
readiness is mixed:

- older years are still dominated by `detail_page: false`
- more recent years contain a higher concentration of rich local pages, but
  not uniformly
- even very recent work still includes thinner external-first bundles

So future backfill is likely to surface more of:

- venue-shape cases
- identifier needs
- publication-kind ambiguity
- richer link patterns
- local-page-readiness edge cases

Current conclusion:

- now is the right time to improve the model
- not after another large wave of bundle backfill

## Preliminary Conclusions

### Strong Conclusions

1. The current publication bundle architecture is still the right overall
   foundation.
2. The next step should be a publication-model review, not more collection
   route/index cleanup.
3. `venue` is overloaded and should be reviewed first.
4. publication-local talks should remain distinct from the invited/public talks
   domain.
5. the model should likely gain a small number of explicit canonical
   identifiers, especially DOI.
6. some intentional duplication with BibTeX is healthy and should be allowed.

### Plausible Design Directions

The current audit makes the following future moves look plausible:

- split `venue` into something like:
  - full venue display
  - compact venue display
- reconsider `detail_page` naming/semantics as a local-page-readiness concept
- reconsider whether `listing_group` should remain the only explicit
  classification field
- evaluate a small identifier expansion in `publication.json`
- review publication boundary treatment for:
  - book chapters
  - books

### What This Does **Not** Yet Justify

The audit does **not** yet justify:

- a giant venue registry
- a perfect BibTeX round-tripping pipeline
- collapsing publication-local talks into the talks domain
- immediate schema churn without a design proposal pass

## Recommendation

The publication model now deserves a serious design review.

That review should probably be:

- deeper than an ordinary one-field refinement
- much narrower than the service redesign

The right sequence is:

1. seam/requirements note
2. audit note grounded in the actual corpus and consumers
3. one or more design proposals
4. review/comparison
5. only then schema migration and broad backfill

This is exactly the point where the service-redesign lessons should be reused:

- enough real consumer pressure exists
- seams are now visible in the canonical data
- and the cost of waiting is future backfill on a model we already know is
  imperfect
