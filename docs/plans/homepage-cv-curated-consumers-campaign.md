# Homepage / CV Curated Consumers Campaign

Status: slices 1-5 implemented; the remaining top-of-CV highlights work is now
framed as a broader authored executive-summary question, with slice-1
purpose/guidance implemented

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
  now a derived consumer of [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)
- `## Recent Teaching`
  now a derived consumer of [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- `## Recent Service / Leadership`
  now a derived consumer over canonical service runs
- `## Recent Publications`
  now a derived compressed consumer over canonical publication bundles

Current overlap assessment:

- `## News`
  already solved; no longer part of this campaign
- `## Current Students`
  now solved as a tiny derived consumer of the canonical `current_students`
  section in [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)
- `## Recent Teaching`
  now solved as a flattened recent-teaching consumer over
  [site/data/teaching.json](/Users/ztatlock/www/ztatlock.github.io/site/data/teaching.json)
- `## Recent Service / Leadership`
  now solved as a run-native derived consumer over canonical service with
  explicit current-year/trailing-window/category/link policy
- `## Recent Publications`
  now solved as a derived compressed consumer over canonical publication
  bundles with explicit recent-year policy

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

There is now one clear remaining category in scope:

- editorial cross-domain blocks that should remain authored unless a very
  small, explicit follow-on policy clearly improves them

### Remaining Clearly Editorial Surface

- CV `## Selected Recent Highlights`

Why this still stays authored for now:

- it mixes service, talks, publications, and broader participation
- it is intentionally selective and presentational rather than a thin recent
  list from one domain
- the remaining question is no longer whether the homepage should derive more
  factual consumers, but whether any tiny part of the CV highlights block
  should later derive from canonical domains without flattening its editorial
  character

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
- reassess before touching the more curated highlights surface

This campaign should not:

- introduce a new homepage-wide registry
- introduce a new CV-wide registry
- try to unify homepage and CV curation policy into one schema
- force the CV highlights block into canonical data before that earns its keep

## Recommended Slice Order

### Slice 1. Homepage Current Students

Implemented.

Invariant:

- homepage current students derives from the canonical `current_students`
  section
- homepage keeps its heading and trailing "students page" line authored
- selection and order are inherited from canonical students data

Implemented outcomes so far:

- the literal homepage current-students list is gone from
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- the section now projects from canonical students data with no intended
  visible HTML change
- the homepage current-students body can no longer drift from
  [site/data/students.json](/Users/ztatlock/www/ztatlock.github.io/site/data/students.json)

### Slice 2. Homepage Recent Teaching

Implemented.

Invariant:

- homepage recent teaching derives from canonical teaching data
- selection policy is explicit and deterministic
- the block stays a flattened homepage-specific view rather than reusing the
  richer public teaching renderer

Implemented outcomes so far:

- the literal homepage recent-teaching bullets are gone from
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- the homepage now derives recent teaching from canonical `uw_courses`,
  `special_topics`, and `summer_school` data inside a deterministic trailing
  3-year window anchored to the most recent teaching year
- the homepage remains a slim single-line-per-item teaching teaser rather than
  a second staffing-aware teaching page

### Stop And Reassess

After slices 1 and 2:

- the easiest homepage drift seams should be gone
- the remaining homepage `Recent Service / Leadership` and
  `Recent Publications` blocks can be reconsidered from a cleaner baseline
- the CV `Selected Recent Highlights` block can be evaluated separately as an
  editorial curation problem rather than by campaign inertia

That later work has now landed for both homepage service and homepage recent
publications. The main remaining curated block in scope is therefore the
authored top-of-CV highlights surface.

That surface is now better understood as a likely authored executive-summary
layer rather than merely a tiny leftover projection seam. The current planning
artifacts are:

- [cv-top-summary-executive-block-plan.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-top-summary-executive-block-plan.md)
- [../policy/cv-top-summary.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/cv-top-summary.md)

### Slice 3. Service Data Audit

Audit the canonical service model before any homepage recent-service
projection.

Invariant:

- the repo has an explicit reviewed understanding of grouped/coalesced service
  semantics as they matter for homepage selection
- any needed canonical service cleanups are identified before homepage
  projection logic depends on them

Why this slice belongs first:

- homepage service should select from grouped/coalesced service entries rather
  than from raw yearly service terms
- the current grouped service behavior is already good, but not obviously final
  enough to harden into homepage policy without review
- recurring service concepts with year-specific instance links may need a
  stronger long-term service-model story than the current term-only grouping
  rules provide
- future service years and repeated annual series make service recency
  selection trickier than news or teaching
- the audit did conclude that a more explicit service redesign should happen
  before homepage recent-service projection depends more heavily on the current
  flat term model

### Slice 4. Homepage Recent Service / Leadership

Only plan this after the service audit clarifies the right grouped source scope
and coalescing semantics, and after the service redesign moves from proposal
to implementation/migration planning.

### Later Possible Work

- CV highlights only if tiny curated consumers clearly beat hand authorship
- `Book Chapters` only through a separate publication-boundary decision

## Current Recommendation

The next move is no longer another homepage factual consumer slice.

The main remaining curated question in this campaign is now the authored
top-of-CV executive-summary redesign and whether any tiny follow-on helpers
there would actually improve clarity rather than over-automate it.
