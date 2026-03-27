# Service Redesign Requirements

Status: draft

It builds on:

- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [service-slice-1-canonical-model.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-slice-1-canonical-model.md)
- [homepage-cv-curated-consumers-slice-3-service-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md)
- [homepage-cv-curated-consumers-slice-3-service-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit-notes.md)

## Purpose

This note captures the requirements for any future service-data redesign.

It is intentionally **requirements-only**.
It does not propose a final schema, file shape, or helper API.

The point is to record:

- what the service domain must represent
- which consumers must use it
- which invariants must remain true over time
- which corner cases and stress cases the design must survive
- which parts of the current model feel trustworthy
- which parts of the current model are producing design pressure

## Current Context

Current canonical service data lives in
[site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json).

Current main code surfaces are:

- [scripts/service_record_a4.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_record_a4.py)
- [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)

Current public/secondary consumers are:

- public service page wrapper:
  [site/service/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/service/index.dj)
- homepage recent-service block:
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- CV service section:
  [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)

Current public headings are useful views, but they are **not** the whole
ontology:

- `Reviewing`
- `Organizing`
- `Mentoring`
- `Department`

Any redesign must treat these as consumer-facing view buckets, not as the only
possible semantic structure of the data.

Current corpus scale at the time of this note:

- `117` canonical service records
- `64` current service identities if grouped by `series_key` or record key
- `19` multi-record identities
- `2` currently non-contiguous multi-run identities
- `3` current multi-instance identities with varying URLs
- `1` current multi-instance identity with varying role

That current cleanliness is helpful, but it is not enough reason to assume the
current design will continue to scale gracefully under future backfill.

## Primary Consumers

Any redesign must support at least these consumers.

### Public `/service/` Page

The public service page needs:

- grouped presentation that is materially easier to scan than the current flat
  lists
- sectioned rendering by current public headings:
  - `Reviewing`
  - `Organizing`
  - `Mentoring`
  - `Department`
- support for grouped summaries
- support for instance-level expansion when links or roles differ
- stable anchors for visible entries
- preservation of the hand-authored `Aggregators` section

### Homepage `Recent Service / Leadership`

The homepage needs:

- a compact one-line-per-item summary consumer
- deterministic selection over recent service
- ability to summarize longer appointments cleanly
- ability to summarize recurring series cleanly
- ability to link either:
  - directly to an external service URL
  - or internally to the corresponding `/service/` entry when external linking
    would otherwise be lossy or ambiguous
- ability to draw from a principled subset of service, which may or may not
  align exactly with one existing view bucket such as `organizing`

### CV Service Section

The CV needs:

- a compressed service representation
- reuse of canonical service truth
- support for range-style summaries and `Present`
- ability to keep selectively authored prose notes when they still add value

### Future Consumers

The redesign should also anticipate likely future consumers even if they are
not part of the next slice:

- richer homepage service summaries
- richer service-page formatting and grouping
- collaborator summaries
- future project/research summaries
- future per-person overlays or popups showing all collaboration/service modes
- future news/service consistency audits

## Granularity Requirements

The redesign must not assume that every relevant fact lives at exactly one
level.

There are potentially meaningful facts at several different granularities:

- an exact service participation instance
- a contiguous run of related service
- a broader recurring identity across multiple runs
- in some cases, metadata about the broader committee/event/community itself
  that is not reducible to one service instance

The redesign does **not** need to model all of those levels explicitly today.
But it must leave room for facts to exist at more than one level without
forcing awkward duplication or false precision.

## Core Representation Requirements

Any redesign must support the following facts explicitly and cleanly.

### 1. Atomic Facts Must Remain Preservable

The model must preserve the finest-grained intended service facts.

Examples:

- `2025 FPTalks` with its specific URL
- `2024 PLDI Workshops` with its specific URL
- `2025 PLDI Program Committee Chair` with its specific supporting links
- `2026 Dagstuhl Seminar 26022: EGRAPHS` with multiple detail links

No redesign should make it hard to recover these exact per-instance facts.

### 2. One-Off Entries Must Remain First-Class

Not every service fact belongs to a recurring series.

The model must support true singletons cleanly, without forcing them into a
fake series layer.

Examples:

- `2026 Dagstuhl Seminar 26022: EGRAPHS`
- many reviewing entries that are just one year and one role

### 3. Recurring Identity Must Be Representable

Some service entries are clearly related across years and should be
understandable as one recurring identity or lane of service.

Examples:

- `FPTalks`
- `PLDI Workshops`
- `PACMPL Advisory Board`
- `PLDI Steering Committee`
- `UW CSE Undergraduate Admissions Committee`

The redesign must support this recurring identity explicitly enough that later
renderers and consumers do not have to re-infer it from ad hoc string
matching.

It must also leave room for the possibility that some future recurring
identities may want their own metadata distinct from any one instance.

### 4. Non-Contiguous Runs Must Be Representable

A recurring identity may have multiple separate runs with gaps.

This is not hypothetical.
It already exists in current data and is likely to become more common.

Current examples:

- `pnw-plse`
- `uw-cse-undergraduate-admissions-committee`

Likely future examples:

- future returns to faculty recruiting
- future returns to graduate or undergraduate admissions
- future returns to recurring community or advisory roles after gaps

The redesign must support separate runs without lying with fake continuous year
ranges.

### 5. Multi-Group Membership Must Remain Valid

A service fact may appear in more than one rendered section.

Current concrete example:

- `2025 PLDI Program Committee Chair` belongs to both:
  - `reviewing`
  - `organizing`

Any redesign must support multi-group membership explicitly.
It must not assume each service fact belongs to exactly one view bucket.

It must also not assume that a higher-level recurring identity or run has one
uniform `view_groups` set that applies unchanged to every instance forever.
Group membership may need to remain meaningful at more than one granularity.

### 6. Titles Alone Are Not Reliable Identity

The corpus already contains repeated titles that should **not** automatically
collapse into one recurring identity.

Examples:

- `PLDI`
- `POPL`
- `ASPLOS`
- `ICFP`

These titles recur across years and roles but currently represent distinct
records rather than one clean recurring series.

The redesign must not derive identity from title alone.

It should also tolerate the possibility that one recurring identity may evolve
its public title over time without ceasing to be the same underlying service
lane.

### 7. Role Must Be Representable At The Right Granularity

The model must support role semantics that may differ:

- across unrelated records with the same title
- across instances within one recurring identity
- across runs of one recurring identity

Current examples:

- `pnw-plse` has `Organizer` and `Co-Organizer`
- `PACMPL Advisory Board` has a stable role
- some entries have no role at all

The model must also tolerate the fact that current role strings are not fully
normalized.

Current normalization seam:

- `Co-chair` vs `Co-Chair`

Any redesign must either:

- represent roles in a way that survives such variation cleanly
- or define a normalization contract precise enough to validate consistently

### 8. URL Semantics Must Support More Than One Level

The service domain needs to support several different link situations:

- singleton with one primary URL
- recurring identity where every instance has a different best URL
- recurring identity where all instances share the same URL
- recurring identity where some instances have URLs and others do not
- entries with no URL
- entries with a primary URL plus additional supporting links

Current examples:

- `FPTalks`:
  each year has a different best URL
- `PNW PLSE`:
  multiple instances currently share one URL
- `PACMPL Advisory Board`:
  no URL
- `2025 PLDI Program Committee Chair`:
  one primary URL plus supporting detail links

The redesign must not collapse these cases into one oversimplified link model.

### 9. Details Must Be Representable Without Becoming A Dumping Ground

The model must support additional supporting information when it is genuinely
part of the service record.

Current examples:

- `2026 Dagstuhl Seminar 26022: EGRAPHS`
  with multiple detail links
- `UW Faculty Skit`
  with the repeated collaborator note
- `2025 PLDI Program Committee Chair`
  with review-committee and announcement links

The redesign must answer all of these cleanly:

- which details belong to a fine-grained instance
- which details can be understood as uniform across a whole recurring identity
- which details can be understood as uniform across a specific run
- which details are present only on some instances within a run or identity
- how to preserve those facts without duplicating them awkwardly in every
  renderer

It must also preserve the fact that current details are authored rich-text
content, not just opaque plain strings.
That includes:

- links
- person references
- later validation hooks over those references

### 10. Time Must Support Display Without Pretending To Know More Than We Know

The current data is year-granular, but displayed summaries sometimes imply
something more like academic-year service.

Important current wrinkle:

- for Allen School and similar academic service, `2020 - 2021` often means the
  `2020-2021 academic year`, not literal full-calendar-year coverage

The redesign must:

- preserve useful year-based querying and grouping
- support renderer-facing summaries like `2020 - 2021`
- avoid claiming false month-level precision unless the data really supports it

It should also tolerate partial historical knowledge, where the repo may know:

- a year or run broadly
- a role broadly
- or a recurring identity broadly

without yet knowing every exact boundary, URL, or connection confidently.

### 11. Same-Year Multiplicity Must Remain Possible

The redesign must not assume there is at most one relevant service instance for
one recurring identity in one calendar year.

That may be true for many current series, but it is not a safe long-term
invariant.

The redesign should therefore support future cases where:

- the same broader recurring identity has multiple meaningful instances in one
  year
- one year contains multiple service sub-events that should remain distinct
- ordering or labeling cannot rely on `identity + year` alone

## Rendering Requirements

These are requirements on what the model must make possible.

They are not themselves a final rendering design.

### Public Service Page

The model must support all of the following render patterns:

- one-line summary for a stable long-running appointment
- one-line summary plus instance sub-bullets for a recurring run with
  year-specific links
- multiple visible runs for one recurring identity with gaps
- current section membership under multiple headings

The model must also support readable labels that avoid the current awkward
year-first style.

It must also support the fact that not every visible summary can be generated
well by one universal string template.

Current stress cases:

- grouped summaries such as `FPTalks Co-Organizer, 2020 - 2025`
- singleton summaries such as `PNW PLSE 2023, Co-Organizer`
- titled singleton events such as `Dagstuhl Seminar 26022: EGRAPHS`

Current preferred label direction:

- grouped run summary:
  - `FPTalks Co-Organizer, 2020 - 2025`
  - `PACMPL Advisory Board Member, 2026 - 2029`
- single-instance summary:
  - `PNW PLSE 2023, Co-Organizer`
- instance bullets:
  - `[FPTalks 2025](...)`, `Co-Organizer`
  - `[PLDI Workshops 2024](...)`, `Co-chair`

Any redesign must make this kind of rendering straightforward.

### Homepage

The model must support homepage summaries that are:

- compact
- deterministic
- recent
- not lossy

In particular, the model must make it possible to express:

- if a recurring identity has multiple distinct instance URLs, the homepage may
  need to link to the corresponding `/service/` entry instead of to any one
  external URL
- if a recurring identity is a singleton or all of its instances share one
  URL, the homepage may link directly to that URL

The model must therefore support stable internal targets for whatever visible
unit the homepage links to.

It must also support deterministic selection and deterministic ordering, even
when multiple candidate items share the same year or same broader identity.

### Stable Internal Anchors

The model must support stable anchors for visible `/service/` entries.

Those anchors must survive:

- future appended years
- future backfill of older years
- future second or third non-contiguous runs
- multiple rendered sections

Those anchors must also avoid ambiguity when the same canonical fact can appear
in more than one rendered section.

Current concrete stress case:

- `2025 PLDI Program Committee Chair`
  appears under both `Reviewing` and `Organizing`

This is currently one of the highest-risk requirements.

The model must not force anchor identity to depend on fragile assumptions such
as:

- the series always having only one run
- the visible entry always living in only one section
- start/end years never changing after backfill

If anchors are not section-aware, the redesign must still explain how it avoids
collisions and ambiguity for multi-view records.

## Ordering Requirements

Any redesign must support deterministic ordering rules at every level that a
consumer may render.

That includes:

- ordering among top-level visible service entries in one section
- ordering among runs inside one recurring identity
- ordering among instances inside one run
- ordering among homepage-selected recent-service items

The design must not leave these as accidental side effects of file order unless
that file order is itself explicitly treated as canonical and stable.

## Validation Requirements

Any future design should remain strictly checkable.

Minimum requirements:

- explicit keys or identities at the levels the model actually uses
- validation for duplicate identifiers
- validation for illegal or malformed links
- validation for impossible combinations of recurring identity / run /
  instance facts
- validation for schema drift
- validation for multi-group membership semantics
- validation for whichever role normalization rule the model adopts
- validation for anchor identity rules once those exist
- validation for whichever level owns details and URLs in grouped renderers
- validation for ordering/tie-break assumptions if the redesign depends on them
- validation for any future uncertainty/partial-knowledge markers if those are
  introduced

The redesign should reduce hidden derivation, not increase it.

## Editing Requirements

The data must remain hand-editable.

That means:

- the canonical source should stay understandable in normal text review
- identifiers should be auditable by eye
- future backfill should feel like adding facts, not reverse-engineering a
  private code generator
- the required amount of metadata should be justified by real consumer needs

Any redesign that becomes too abstract to edit confidently by hand is a bad
fit for this repo.

That includes over-reliance on inferred formatting or identity rules that are
hard to see in code review.

## Current Stress Cases

These examples should be treated as mandatory design tests.

### Recurring Identity With Varying URLs

- `fptalks`
- `pldi-workshops`
- `egraphs-workshop`

The redesign must support:

- one recurring identity
- one or more visible runs
- per-instance external URLs
- non-lossy service-page rendering
- non-lossy homepage linking

It should also allow for the possibility that future backfill changes the
oldest or newest known instance without forcing a brittle redesign of visible
identity.

### Non-Contiguous Identity

- `pnw-plse`
- `uw-cse-undergraduate-admissions-committee`

The redesign must support:

- one recurring identity
- multiple separated runs
- no fake continuous range
- stable visible identifiers or anchors for each visible run
- potential future title drift across runs
- potential future same-year multiplicity if one year contains more than one
  relevant instance

### Multi-View Record

- `2025-pldi-program-committee-chair`

The redesign must support:

- one canonical fact
- appearance in more than one rendered section
- no anchor collisions
- no accidental duplication of truth

### Uniform Repeated Detail

- `uw-faculty-skit`

The redesign must support:

- long recurring identity
- stable repeated detail text
- no needless per-render duplication decisions

### Singleton With Rich Supporting Links

- `2026-dagstuhl-seminar-26022-egraphs`
- `2025-pldi-program-committee-chair`

The redesign must support:

- primary URL
- additional supporting links
- rich authored detail text that survives validation and projection
- clean rendering without flattening everything into a single string field

### Role Normalization Pressure

Current concrete examples:

- `Co-chair`
- `Co-Chair`

Current punctuation and formatting stress cases:

- `Writer, Producer, and Director`
- `Co-Organizer and Speaker`
- `Student Hackathon Organizer`

The redesign must survive future backfill without brittle false distinctions.

It must also not assume that roles are short, comma-free, or stylistically
uniform enough to be safely parsed or reformatted by naive string splitting.

### Labeling And Formatting Pressure

The redesign must support renderer-friendly labels without forcing canonical
fields to carry display-only hacks.

Current labeling stress cases include:

- grouped labels that should read as `title role, years`
- singleton labels that should read as `title year, role`
- titled events where a generic `title year` rule may read awkwardly
- roles that already contain commas
- future cases where a recurring identity may want a better shared display
  title than any one instance title alone

The redesign should therefore separate:

- canonical identity facts
- canonical authored labels where needed
- renderer formatting rules

cleanly enough that future projection work does not have to reverse-engineer
presentation from incidental field choices.

## Known Current Model Seams

The current model is not obviously broken, but it does leave several seams
exposed.

1. `series_key` currently expresses recurring identity, but only implicitly.
2. The current grouping/rendering code splits on `url`, `role`, and `details`,
   which is too presentation-driven for some future consumers.
3. The current model has no explicit place to talk about non-contiguous runs.
4. The current model has no explicit place to talk about stable internal
   targets for visible grouped entries.
5. The current model has no explicit place to talk about run-level versus
   instance-level supporting details.
6. The current model does not yet define a robust normalization story for
   roles.
7. The current model does not yet define how multi-view records should behave
   under grouped-anchor rendering.
8. The current model encourages renderer code to infer more than the schema
   states directly.
9. The current model does not clearly separate consumer-facing section buckets
   from deeper semantic structure.
10. The current model does not clearly state where higher-level recurring
    identity metadata would live if future backfill needs it.
11. The current model does not state deterministic ordering rules at every
    rendered level.
12. The current model assumes more certainty and regularity than future
    historical backfill is likely to support.

## Requirements For Any Successful Redesign

A redesign should be considered successful only if it:

- preserves all currently intended service facts
- makes recurring identity explicit enough to be trusted
- supports one-offs cleanly
- supports non-contiguous runs cleanly
- supports multi-view records cleanly
- supports per-instance links and supporting details cleanly
- supports stable internal anchors for visible entries
- supports section-safe internal anchors for multi-view records
- supports deterministic ordering and tie-breaks
- supports partial historical knowledge without forcing invented structure
- remains hand-editable
- remains strictly validateable
- reduces ad hoc derivation pressure in renderers
- makes future homepage and service-page projections easier rather than harder

## Explicit Non-Requirements

This note does **not** require:

- a specific final JSON shape
- a specific number of model layers
- a specific decision on whether an explicit top-level series registry is
  needed
- a styling redesign for `/service/`
- a final homepage selection policy
- month-level or term-level service timing semantics right now

Those are later design decisions.
This note is only intended to state what the eventual design must accomplish.
