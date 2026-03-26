# Homepage / CV Curated Consumers Campaign

Status: planned; slice 1 next

It builds on:

- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [students-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/students-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [news-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/news-campaign.md)

## Goal

Decide which remaining homepage and CV "current/recent/highlights" blocks
should:

- remain hand-authored
- be trimmed
- become tiny projected consumers over existing canonical domains

The goal is not to create `site/data/homepage.json` or `site/data/cv.json`.
The goal is to remove the remaining duplicated factual maintenance where that
is obviously worth it, while keeping the more editorial cross-domain blocks
honestly authored.

## Current Audit

### Homepage

Current relevant source:

- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)

Relevant current blocks:

- `## News`
  now a derived consumer of [site/data/news.json](/Users/ztatlock/www/ztatlock.github.io/site/data/news.json)
- `## Current Students`
  8 entries
- `## Recent Service / Leadership`
  6 entries
- `## Recent Publications`
  14 full publication entries
- `## Recent Teaching`
  7 offering bullets

Current overlap assessment:

- `## News`
  already solved; no longer part of this campaign
- `## Current Students`
  a near-exact duplicate of the `current_students` section in
  [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)
- `## Recent Teaching`
  a flattened recent-offerings consumer over
  [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- `## Recent Service / Leadership`
  clearly curated across service categories rather than a simple "latest
  service terms" view
- `## Recent Publications`
  clearly repeated publication bibliography structure, but still a heavier
  editorial choice than the students/teaching blocks because the homepage
  wants a selective compressed subset rather than the whole canonical `/pubs/`
  view

### CV

Current relevant source:

- [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)

Relevant remaining authored cross-domain blocks:

- `## Selected Recent Highlights (2024-2026)`
  - `Leadership` with 5 bullets
  - `Invited Talks` with 3 bullets
  - `Selected Publications (2024-2025)` with 5 bullets
- `### _Book Chapters_`
  one authored bibliography entry outside the indexed publication-bundle
  boundary

Current overlap assessment:

- `Selected Recent Highlights`
  is a deliberately editorial cross-domain block rather than a simple repeated
  list from one source
- `Book Chapters`
  remains a publication-boundary decision, not a generic "current/recent"
  consumer question

## Main Conclusion

The remaining curated surfaces are not all alike.

There are two clear categories:

1. tiny factual consumers that now look safe to derive
2. editorial cross-domain blocks that should remain authored for now

### Good Tiny-Consumer Candidates

- homepage `## Current Students`
- homepage `## Recent Teaching`

Why these two look good:

- both already overlap a single clear canonical domain
- both are relatively small
- both are structurally list-shaped
- both can likely adopt explicit simple selection/order policy without
  inventing new metadata

### Still Clearly Editorial

- homepage `## Recent Service / Leadership`
- homepage `## Recent Publications`
- CV `## Selected Recent Highlights`

Why these should stay authored for now:

- each mixes curation, selection, and tone rather than just flattening one
  canonical list
- each would need explicit editorial policy before projection could be honest
- none has the same obvious "just mirror the canonical subset" shape that
  `Current Students` and `Recent Teaching` have

### Separate Boundary Question

- CV `### _Book Chapters_`

This should stay separate from the homepage/current-recent consumer work.
It is still the publication/bibliography boundary decision already called out
elsewhere in the repo.

## Design Recommendation

Treat the remaining work as a small campaign with narrow follow-on slices, not
as one giant "project all curated blocks" effort.

Recommended principle:

- keep editorial framing authored
- project only the obviously repeated factual bodies
- stop once the low-risk blocks are converted
- reassess before touching the more curated publication/service/highlights
  surfaces

This campaign should not:

- introduce a new homepage-wide registry
- introduce a new CV-wide registry
- try to unify homepage and CV curation policy into one schema
- force the CV highlights block into canonical data before that earns its keep

## Recommended Slice Order

### Slice 1. Homepage Current Students

Turn the homepage `## Current Students` block into a tiny derived consumer of
[site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json).

Invariant:

- homepage current students derives from the canonical `current_students`
  section
- homepage keeps its heading and trailing "students page" line authored
- selection and order are inherited from canonical students data

### Slice 2. Homepage Recent Teaching

Turn the homepage `## Recent Teaching` block into a tiny derived consumer of
[site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json).

Invariant:

- homepage recent teaching derives from canonical instructor-led offerings
- selection policy is explicit and deterministic
- the block stays a flattened homepage-specific view rather than reusing the
  richer public teaching renderer

### Stop And Reassess

After slices 1 and 2:

- the easiest homepage drift seams should be gone
- the remaining homepage `Recent Service / Leadership` and
  `Recent Publications` blocks can be reconsidered from a cleaner baseline
- the CV `Selected Recent Highlights` block can be evaluated separately as an
  editorial curation problem rather than by campaign inertia

### Later Possible Work

- homepage `Recent Service / Leadership` only if a real curation policy is
  worth formalizing
- homepage `Recent Publications` only if a homepage publication-selection
  policy becomes clear enough to justify another consumer slice
- CV highlights only if tiny curated consumers clearly beat hand authorship
- `Book Chapters` only through a separate publication-boundary decision

## Current Recommendation

The right next move is not "project everything."

The right next move is:

1. plan and review a small homepage `Current Students` slice
2. likely follow with homepage `Recent Teaching`
3. keep service/publications/highlights authored until a stronger editorial
   policy exists
