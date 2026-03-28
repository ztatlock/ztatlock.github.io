# Publication Model Requirements

Status: requirements draft

It builds on:

- [publication-model-seams-and-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-seams-and-requirements.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-slice-5-recent-publications.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-5-recent-publications.md)
- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

## Goal

State the publication-model requirements independently of any specific schema
proposal.

This note is intentionally consumer-first.
It should answer:

- what the repo needs publication bundles to represent
- who needs that information
- what distinctions the model must preserve
- what future growth the model should be ready for

It should **not** decide the final schema.
That comes later.

## Why A Separate Requirements Note

The seam inventory and audit findings are useful, but they are still partly
diagnostic.

This repo now has enough real publication consumers that proposal work should
target a more explicit requirements statement first, the same way the service
redesign improved once requirements were separated from emerging solutions.

The current publication domain already serves at least:

1. individual publication pages
2. the publications index page
3. CV indexed-publication sections
4. homepage recent publications
5. collaborator derivation and related cross-domain uses
6. internal inventory/analysis tooling

And it is reasonable to expect more future consumers such as:

7. top-of-CV selected-publication/highlight rendering
8. richer collaborator/research cross-linking or overlays
9. future funding/research/publication analysis pipelines

## Domain Boundaries

The publication model should stay clear about what it is and is not
responsible for.

### In Scope

- canonical publication records
- optional local publication-page assets and extras
- publication pages
- publications index rendering
- downstream consumers over canonical publication records
- publication-related identifiers useful to the site and repo tooling

### Explicitly Distinct Domains

- invited/public talks under `site/talks/`
- service
- teaching
- news

Publication-local `talks` should remain publication-local unless the repo
later makes an explicit cross-domain design decision.

### Boundary Questions That Must Be Answerable

The model should make it possible to decide, deliberately, what happens with:

- book chapters
- books
- journal articles
- workshop papers
- thinner externally hosted indexed publications

It does **not** have to answer all of those immediately, but it must not hide
the boundary either.

Current explicit deferral:

- proposals may assume `Book Chapters` and `Books` stay outside the indexed
  publication bundle model for now
- but the model should not make that boundary impossible to revisit later

## Current And Expected Consumers

### 1. Individual Publication Pages

Current repo context:

- publication records currently live under `site/pubs/<slug>/publication.json`
- some records currently drive local pages at `/pubs/<slug>/`

What these consumers need:

- stable publication identity
- title
- author list
- full venue display
- publication year/date
- local-asset readiness information
- metadata text for page metadata and sharing
- publication-local links
- publication-local extras such as embedded talk/video material

Special constraint:

- a publication may be canonical without yet having a full local detail page

### 2. Publications Index Page

Current repo context:

- the public collection page is currently `/pubs/`

What it needs:

- deterministic ordering
- title links
- full bibliography-style title/authors/venue/badges rendering
- grouping suitable for the page shape
- stable inclusion/exclusion rules for non-draft indexed bundles

Special constraint:

- the page wants one canonical listing truth without hand-maintained repeated
  entry blocks

### 3. CV Indexed-Publication Sections

Current consumer:

- `site/cv/index.dj`

What it needs:

- the same underlying indexed publication truth as `/pubs/`
- a different, more compressed renderer
- bibliography-style venue display
- stable grouping into the current CV sections

Special constraint:

- the CV should be able to compress or restyle publication data without
  forcing the canonical model to mimic one exact page layout

### 4. Homepage Recent Publications

Current consumer:

- `site/pages/index.dj`

What it needs:

- recent-selection policy over canonical publications
- compact renderer
- compact venue display, not full bibliography venue display
- honest title-link policy

Special constraint:

- the homepage should not have to parse or heuristically compress one
  bibliography-facing field just to render a teaser line
- the homepage and other compact selectors may later need overflow policy
  refinement without requiring a separate homepage-only publication dataset

### 5. Collaborator / Research-Derived Consumers

Current and likely future consumers:

- collaborator derivation already uses publication authors
- future research/collaborator surfaces may want richer publication metadata

What they need:

- stable author information
- a clean relationship between author display labels and optional site-local
  identity resolution
- canonical publication identity
- enough publication metadata to support honest cross-linking

Special constraint:

- collaborators should not require publication bundles to pretend they are a
  collaborator profile system

Current author-identity seam to preserve or clarify:

- bibliography/display linking currently uses publication-local author refs
- cross-domain identity resolution currently also happens through site-local
  people/collaborator logic

The requirements do not force those mechanisms to unify immediately, but
proposals should account for the fact that both currently exist.

### 6. Internal Inventory / Analysis / Automation Uses

Current internal consumer:

- [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)

Likely future internal consumers:

- DOI/arXiv-aware scripts
- availability/paywall-aware analysis
- publication artifact completeness audits
- cross-domain reports

What these uses need:

- explicit canonical identifiers where useful
- explicit readiness / local-page status semantics
- stable link information
- a model that does not require scraping human-facing display strings

Special constraint:

- the repo should support useful analysis without requiring a giant BibTeX
  pipeline or a second publication database

### 7. Future Top-Of-CV Selected-Publication / Highlights Consumers

Likely future consumer:

- `Selected Publications` and other curated top-of-CV material

What it may need:

- stronger editorial compression than `/pubs/` or the current indexed CV
  sections
- compact venue display
- possibly future stickiness semantics such as award paper preference

Special constraint:

- this consumer should not drive premature over-modeling, but the publication
  model should not block it either

## Core Requirements

### Identity And Ordering

1. Every canonical publication must have a stable identity independent of
   title display.
2. Ordering for collection/index consumers must be deterministic.
3. The model must support both thin and rich local publication bundles without
   losing canonical identity.
4. Index-like publication consumers should default to publication-date
   descending ordering with a stable tie-break unless a narrower consumer
   policy explicitly says otherwise.

### Temporal Identity

1. The model must support a canonical publication year for display and
   year-level selection consumers.
2. It should also support more precise publication-date information when that
   is known and useful.
3. Canonical temporal semantics must not rely only on slug-embedded year text.
4. The model should tolerate older or partial backfill where publication year
   is known but exact publication date is not.
5. Proposals should explain the relationship between slug conventions,
   canonical publication year, and more precise dates when those differ.

### Author Identity And Cross-Domain Resolution

1. The model must preserve ordered publication authorship as publication-local
   bibliographic truth.
2. The model must also support optional cross-domain identity resolution for
   authors when that clearly exists elsewhere in the site.
3. Consumers must be able to render author names correctly even when no
   site-local identity resolution exists for a given author.
4. The model must not force every publication author into a heavier person or
   collaborator system just to render bibliographies honestly.
5. The model must distinguish between display-oriented author-link aliases and
   stable site-local identity resolution when both exist.
6. Proposals should be explicit about whether the current `author.ref`-style
   mechanism remains a display hint, becomes a stronger identity field, or is
   replaced by a clearer split between display and identity concerns.

### Full vs Compact Display

1. The model must support full bibliography-style venue display.
2. The model must also support compact consumer display such as homepage
   teasers.
3. Compact consumers must not need to reverse-engineer compact venue labels
   from full display strings.
4. Full-display data should not carry compact-display punctuation or
   duplication solely to serve a different consumer.
5. Compact venue display should not be assumed to be a simple derivable
   acronym rule over the full venue string; the model must allow honest
   compact labels for cases where acronym-style derivation is weak, ambiguous,
   or not the right display form.
6. Compact venue display should separate compact venue labeling from
   publication-year rendering; year/date semantics should come from canonical
   temporal metadata rather than being baked into compact venue text.
7. The compact venue label may be an acronym, a short series name, or another
   independently authored compact form; the requirements do not assume one
   universal pattern.

### Local Bundle Readiness

1. The model must distinguish between:
   - a canonical publication bundle existing
   - a full local publication detail page being available
2. That distinction must be explicit and understandable.
3. Consumers should not mistake “no local detail page yet” for “not canonical.”
4. The title-link policy should remain honest for both thin and rich bundles.
5. Thin externally hosted indexed bundles are a valid current mode; proposals
   should not assume that every canonical publication must immediately have a
   rich local page.
6. Proposals may assume the current readiness workflow is binary enough for
   now: a bundle is either a thin external-destination record or a richer
   local-page bundle, unless real consumers require a more granular
   mid-curation state later.

### Classification

1. The model must support the current `/pubs/` and CV grouping needs.
2. The model must not assume the current grouping is the only meaningful
   publication classification forever.
3. The model should allow later refinement without forcing a full venue
   ontology immediately.
4. The requirements pressure here includes at least two distinct questions:
   - publication type or venue kind
   - venue identity across papers
5. Proposals should be clear about whether they are addressing one of those
   pressures or both.
6. Concrete current and likely future pressure already includes distinctions
   such as conference vs journal, workshop vs non-workshop, and possibly later
   invited/refereed or venue-family distinctions, even if the current model
   does not encode them yet.

### Consumer Composability

1. A single canonical publication record must be sufficient input for all
   current public publication consumers.
2. Different consumers may render, filter, compress, group, and link the same
   canonical record differently without requiring separate consumer-local
   publication fact stores.
3. If a future consumer needs extra curation or selection semantics, proposals
   should be clear about whether that belongs in canonical publication data or
   in a deliberately separate curated layer, rather than relying on ad hoc
   duplicated publication metadata.

### Links And Identifiers

1. The model must support a canonical title destination for every indexed
   publication.
2. Different consumers must be able to make different honest link choices over
   the same canonical publication record when needed.
3. The model must preserve rich publication-local links such as:
   - publisher
   - project
   - code
   - event
   - teaser
   - talk
   - demo
4. The model should expose high-value canonical persistent identifiers directly
   when they materially help downstream use, interoperability, or analysis.
5. The model should support open-access- and paywall-aware tooling without
   requiring scripts to scrape human-facing display strings or reverse-engineer
   semantics from URLs.
6. Persistent identifiers and landing-page links are distinct kinds of fact.
   Proposals should explain whether identifier fields such as DOI supplement
   publisher links, can derive them in some cases, or are intentionally kept
   independently authored.

### Publication-Local Extras

1. Publication-local talks/videos must remain representable.
2. Publication-local talks must remain distinct from the invited/public talks
   domain unless a later design explicitly bridges them.
3. The model should support publication-local assets and extras without
   forcing every bundle to be equally rich.

### Badges / Awards

1. The model must continue to support visible badge rendering on
   bibliography-style consumers.
2. The model should be able to support future “award paper” style policy uses
   if those become worthwhile.
3. The model should not force a rich badge ontology unless real consumers
   require it.

### BibTeX Relationship

1. `publication.json` should remain the site-facing canonical metadata source
   for site consumers.
2. The model must coexist cleanly with publication-local BibTeX assets.
3. The repo should not require a perfect BibTeX parse/write/normalize pipeline
   just to maintain publication metadata.
4. Some intentional duplication between `publication.json` and `.bib` is
   acceptable.
5. Duplication should be tolerated when it meaningfully reduces code or
   maintenance complexity.
6. Proposals should explain which overlapping facts are intentionally
   duplicated between JSON and BibTeX and why.
7. For facts present in `publication.json`, site consumers should treat
   `publication.json` as authoritative unless a later design explicitly says
   otherwise.
8. Proposals do not need to require automatic cross-validation of every
   duplicated BibTeX field, but they should explain the intended authority
   boundary when shared facts disagree.

### Partial And Uncertain Historical Knowledge

1. The model must remain usable when older publications are only partially
   backfilled.
2. It must tolerate missing or currently unknown facts such as:
   - missing persistent identifiers
   - missing short-display metadata
   - missing local assets
   - missing richer external-link coverage
3. It must not force invented structure or fake precision just to satisfy
   schema shape.
4. The model should let backfill proceed incrementally while tolerating absent
   optional facts without requiring invented placeholder values or premature
   semantic distinctions stronger than the corpus can currently support.

### Backfill And Editability

1. The model must remain workable for a large future publication backfill.
2. The required canonical fields should be justified by real consumer needs.
3. The model should support thinner initial bundles when full local curation is
   not yet done.
4. Future refinement should not require reworking dozens of newly backfilled
   bundles just because the original model hid a known seam.
5. The physical authored representation should stay reviewable, diff-friendly,
   and reasonable to edit with human help from agents rather than assuming a
   custom data-management pipeline.

### Boundary Requirements

1. The model must make the boundary around `Book Chapters` explicit.
2. It should also be able to answer, later, whether `Books` belong in the same
   publication domain.
3. The existence of an authored CV section should not, by itself, force those
   records into the indexed publication bundle model.
4. The model should make it possible to distinguish:
   - indexed publication records intended to participate in public
     collection-style consumers
   - thinner externally hosted records
   - future non-indexed but publication-adjacent records

### Current Concrete Identifier Pressure

The requirements intentionally do not hardcode a final identifier field list.

But the current repo pressure strongly suggests that a good proposal should at
least evaluate explicit support for identifiers such as:

- DOI
- arXiv identifier
- ISBN later if books/chapters enter scope

Current likely stance:

- DOI looks especially high-value
- arXiv support is likely important enough to review explicitly
- neither of those statements, by itself, decides the final schema

## Non-Requirements

The next publication-model pass should **not** assume it must:

- build a perfect venue ontology
- emulate a complex BibTeX pipeline
- collapse publication-local talks into invited/public talks
- solve every future cross-domain popup/overlay idea now
- make every publication equally rich before the model is considered sound

## What A Good Next Proposal Should Be Able To Explain

A serious publication-model proposal should be able to answer, clearly:

1. What are the canonical temporal semantics for publication year, more
   precise publication dates, and slug conventions?
2. How does the model support both full and compact venue display?
3. What is the right explicit representation of local-page readiness?
4. What is the right role of `listing_group`, and is it enough?
5. How should display-oriented author refs and stronger identity resolution
   relate?
6. Which identifiers should become canonical fields now?
7. What intentional duplication with BibTeX is allowed?
8. How are publication-local talks kept distinct from invited/public talks?
9. What is the current publication boundary around:
   - indexed publications
   - book chapters
   - books

## Current Recommendation

The next step should be:

1. iterate on this requirements note
2. then draft one or more publication-model proposals against it

That is a better path than:

- immediately adding `venue_short`
- or immediately migrating many bundles

The requirements are now broad enough that publication proposals should be
judged against consumers and long-term backfill pressure, not just against the
homepage renderer that exposed the first visible seam.
