# Publication Model Requirements Review Synthesis

Status: synthesis note

It synthesizes two external review passes over:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
- [publication-model-seams-and-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-seams-and-requirements.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)

## Purpose

Capture what the external reviews improved, what they surfaced as real
requirement seams, and what still remains deliberately open before proposal
work.

This note is intentionally not another schema proposal.
It is a requirements-checkpoint note.

## Overall Assessment

Both external reviews were useful.

Neither review argued that the publication domain needs a service-scale reset.
Both instead converged on a narrower conclusion:

- the current publication bundle foundation is still basically right
- but the requirements needed tightening around a few real semantic seams
- after that tightening, proposals should be able to compete more cleanly

That is a good sign.
It means the review process is improving the target rather than reopening the
whole direction.

## What The Reviews Converged On

The two reviews, taken together, converged on these real requirements-level
pressures:

1. Temporal semantics must be made explicit.
   The current repo already uses more than one time representation:
   - slug-embedded year
   - `pub_date`
   - rendered year display
   The requirements should not leave that relationship implicit.

2. Compact venue display is a real consumer need, not just a homepage quirk.
   The requirements needed to say more clearly that compact venue display is a
   first-class need and must not be derived heuristically from bibliography
   display strings.

3. Author display linking and author identity resolution are related but not
   the same thing.
   The reviews correctly identified that the current repo has two parallel
   mechanisms:
   - publication-local display refs
   - site-local people/collaborator resolution
   The requirements needed to acknowledge both.

4. `detail_page` / local-page readiness is a real semantic seam.
   The requirements needed a clearer statement that:
   - thin external-destination bundles are valid current canonical records
   - rich local-page bundles are another mode
   - consumers should not confuse canonical existence with local-page richness

5. `listing_group` is not the whole classification story.
   The reviews correctly pushed the requirements to name the actual future
   pressure:
   - publication type / venue kind
   - venue identity across papers
   - current and likely future distinctions such as conference vs journal

6. The requirements needed a stronger single-source-of-truth stance.
   With `/pubs/`, the CV, the homepage, collaborator consumers, and future
   tooling all depending on the same publication corpus, the requirements
   should say clearly that canonical publication data must be sufficient input
   for current public consumers.

## What We Tightened In The Requirements

The current draft of
[publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)
now reflects the most useful review pressure.

The main improvements are:

- explicit temporal-identity requirements
- stronger compact-display requirements
- clearer author display-vs-identity requirements
- clearer local-page-readiness stance
- more concrete classification pressure
- explicit consumer composability over one canonical publication record
- clearer JSON/BibTeX authority language
- softer and more practical partial-backfill language
- explicit current deferral around `Book Chapters` / `Books`

This means the requirements are now much less likely to produce proposals that
quietly smuggle in assumptions about:

- slug year being the canonical year
- compact venue display always being a derivable acronym
- `author.ref` and collaborator identity being the same mechanism
- thin bundles being “not really canonical”
- `listing_group` being the only classification question forever

## What Still Remains Deliberately Open

The reviews were also helpful because they clarified which questions should
*not* be forced closed at the requirements stage.

These still remain deliberately open before proposals:

### 1. Exact Temporal Field Design

The requirements now say the model needs:

- a canonical publication year
- optional more precise publication-date information
- honest handling of partial historical date knowledge

But they do **not** decide:

- whether canonical year is stored separately from exact date
- whether exact dates remain year-month-day only
- whether approximate dates need a dedicated representation

That is proposal work.

### 2. Exact Compact-Venue Representation

The requirements now say compact venue labeling is a first-class need and is
not assumed to be derivable from the full venue string.

But they do **not** decide:

- whether the right field is `venue_short`
- whether compact display should be one field or a richer venue structure
- whether some compact labels should be authored manually while others are
  derivable

That is proposal work.

### 3. Exact Author Identity Schema

The requirements now distinguish:

- bibliographic author ordering and display
- display-oriented refs/aliases
- optional site-local identity resolution

But they do **not** decide:

- whether `author.ref` stays as-is
- whether a stronger `person_key`-style field should exist
- whether both should coexist

That is proposal work.

### 4. Exact Readiness / `detail_page` Encoding

The requirements now take a position on the current binary-enough workflow:

- thin external-destination canonical bundles are valid
- richer local-page bundles are valid

But they do **not** decide:

- whether the current boolean should survive
- whether a richer readiness enum is worthwhile
- whether long-horizon strategy should bias toward universal local pages

That is proposal work.

### 5. Exact Classification Structure

The requirements now name the real pressure more honestly.

But they do **not** decide:

- whether `listing_group` should be replaced
- whether it should be complemented by `pub_type`
- whether venue identity should be modeled separately from publication type

That is proposal work.

### 6. Exact DOI / Publisher / arXiv Field Relationships

The requirements now make identifiers a real first-class pressure and require
proposals to explain DOI/publisher-link interaction.

But they do **not** decide:

- whether DOI should become canonical immediately
- whether publisher links stay independently authored
- whether arXiv should be a first-class identifier, a link, or both

That is proposal work.

### 7. Explicit Homepage Overflow Policy

The reviews were right that publication density may grow with backfill.

But the requirements still intentionally do **not** require a cap, stickiness
policy, or homepage-only selection metadata yet.

That remains a future policy refinement, not a blocker for the publication
model itself.

## What We Intentionally Did Not Over-Specify

The external reviews raised several useful questions that still should not be
turned into hard requirements prematurely.

We intentionally did **not** force the requirements to decide:

- that every publication must eventually have a local page
- that BibTeX and JSON must be fully cross-validated
- that publication-local talk-link fallback logic is a core domain concept
- that `Book Chapters` or `Books` must enter scope now
- that a full publication-type ontology is required before proposals
- that a homepage cap/stickiness policy must exist now

Those are all real considerations, but they are not all requirements-level
facts yet.

## Current Judgment

After both external review passes, the requirements now feel strong enough to
anchor proposal work.

The remaining open questions are now mostly the *right* ones:

- representational choices
- field-ownership choices
- boundary choices
- migration/authoring tradeoffs

rather than hidden consumer requirements or accidental implementation quirks.

That is the state we wanted before asking proposals to compete.

## Recommendation

The next step should be:

1. treat the current requirements draft as the working requirements baseline
2. draft one or more publication-model proposals against it
3. judge those proposals on:
   - how cleanly they satisfy the requirements
   - how well they handle long-horizon backfill
   - how much accidental complexity they introduce
   - how cleanly they separate canonical semantics from consumer rendering

That is now a better use of time than continuing to churn on requirements.
