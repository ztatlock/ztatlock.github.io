# News Campaign

Status: slices 1-3 implemented; later slices planned

It builds on:

- [site-architecture-spec.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/site-architecture-spec.md)
- [structured-content-roadmap.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/structured-content-roadmap.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)
- [teaching-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/teaching-campaign.md)
- [service-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/service-campaign.md)
- [collaborators-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/collaborators-campaign.md)

## Goal

Give news one clear, reviewable source of truth without pretending the page is
just another derived view over talks, publications, teaching, or service.

The point of a news campaign would be:

- remove duplicated hand-maintained news items across the homepage and
  the public news page
- keep the page prose-first in tone
- make future homepage news reuse explicit instead of silently copying entries
- leave room for later typed links back to canonical domains where that pays
  off

This should not begin as a giant cross-domain event schema.

## Why News Is Different

News is not just a secondary list view over another domain.

Unlike students, teaching, service, or funding, the current news items mix:

- invited talks
- publication presentations
- teaching announcements
- organizing/community activity
- project/tool releases
- media/press items
- career milestones
- short editorial commentary

That means the news page is not simply "facts from somewhere else."
The editorial selection and phrasing are themselves part of the canonical
surface.

Examples:

- `PLDI 2025 was a huge success!` is not a clean projection from service
- `Excited to start this quarter as Full Professor!` has no current canonical
  home elsewhere
- the `Haploid` item is partly about a student, partly about a project/tool
  release, and partly about research context

So if news becomes structured, the news records themselves should be canonical.
Existing domains can still become linked inputs later, but they should not be
forced to own the news prose.

## Current Surface Audit

Current explicit surfaces:

- [site/data/news.json](/Users/ztatlock/www/ztatlock.github.io/site/data/news.json)
  canonical ordered news records
- [site/news/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/news/index.dj)
  thin authored public news wrapper
- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
  authored homepage `## News` block

Route / wrapper facts:

- news is now an explicit wrapper page under `site/news/`
- its canonical public route is now `/news/`
- the homepage already behaves like a second consumer of the same news stream
- canonical shared news data lives in `site/data/news.json`

Current public page shape rendered from canonical records:

- `15` month buckets
- `23` individual news items

Current icon usage:

- `🗣️`: `14`
- `🧰`: `3`
- `🧑‍🏫`: `2`
- `🎯`: `1`
- `⛰️`: `1`
- `📰`: `2`

Important design note:

- the icons are not a stable ontology

For example:

- `🗣️` is used for invited talks, a Dagstuhl seminar, a publication highlight,
  a promotion milestone, and a summer-school seminar
- `🧰` is used for both a tool/project release and conference/community work

So a first structured model should treat the icon as display/editorial policy,
not as a trustworthy event kind.

## Initial Homepage Overlap Audit

Before slice 3, the homepage `## News` block was a second hand-maintained
consumer of the same underlying news stream.

Audit findings at that checkpoint:

- homepage news duplicates `13` of the `15` dated month buckets from the
  public news page
- homepage news duplicates `21` of the `23` individual news items

The current homepage omits exactly these two older news items:

- April 2023: Business Insider interview
- August 2017: Neutrons feature roundup

That is important because it means the homepage is not just "latest N news
items."
If the homepage later reuses canonical news records, it will likely need an
explicit curation policy rather than a naive count-based prefix.

## Canonical Overlap With Existing Domains

Many current news items already point at facts that also exist elsewhere:

- Brown 2026 and Cornell 2024 talks now exist in `site/talks/`
- Marktoberdorf 2024 exists in both `site/talks/` and `site/data/teaching.json`
- `Dagstuhl Seminar 26022: EGRAPHS` exists in `site/data/service.json`
- course announcements like CSE 507 and CSE 505 exist in
  `site/data/teaching.json`
- some conference presentation items point at canonical publication bundles
  with publication-local talk links
- `PNW PLSE` and `FPTalks` overlap the canonical service domain

But some current news items do not have a good canonical home yet:

- `PLDI 2025 was a huge success!`
- `Excited to start this quarter as Full Professor!`
- the Business Insider interview
- the Neutrons feature roundup
- parts of the `Haploid` item

This mixed shape is the strongest reason to treat news as its own editorial
domain rather than trying to derive it directly from other canonical records.

## Recommended Route / Source Shape

Recommended canonical source:

- `site/data/news.json`

Recommended public wrapper:

- `site/news/index.dj`

Recommended canonical public route:

- `/news/`

Why this shape:

- once news has canonical shared data plus a later homepage consumer, it is no
  longer just an ordinary prose page
- the wrapper/data split matches the rest of the repo's structured public
  domains honestly
- route churn buys a cleaner long-term architecture here rather than just
  symmetry for its own sake
- a small shared data file is a better fit than per-entry bundles for the
  current page shape
- later homepage reuse becomes straightforward
- later typed cross-links back to talks/publications/service/teaching/projects
  can grow from a clear canonical news domain

Important route-model note:

- this would require a deliberate ordinary-page to wrapper cutover, not just
  a data-file addition

That means:

- add a new explicit `news_index_page` route kind
- move the public wrapper out of `site/pages/news.dj`
- reject simultaneous legacy `site/pages/news.dj` and new `site/news/index.dj`
  wrappers, just as the repo already does for other wrapper routes
- rewrite lingering `news.html` links to `news/`

Current churn looks acceptable:

- the only current authored site link using `news.html` is in
  [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)

## Minimal Canonical Model

The first useful model should stay small, flat, and ordered by individual news
items rather than nested month buckets.

Recommended top-level shape:

- ordered `records`

Recommended slice-1 fields per record:

- `key`
  stable unique identifier
- `year`
- `month`
  integer month number
- optional `sort_day`
  integer tie-break within a month when we know a finer ordering than the
  public display shows
- `kind`
  primary editorial kind from a small approved list
- `emoji`
  explicit display symbol such as `🗣️`
- `body_djot`
  the authored news item text

Recommended approved `kind` list for slice 1:

- `talk`
- `publication`
- `teaching`
- `community`
- `release`
- `recognition`
- `student`
- `media`
- `funding`
- `other`

Important notes:

- the news prose itself should stay canonical in `body_djot`
- month/year grouping should be derived at render time from the flat record
  stream
- `kind` should be controlled and validated, but broad enough that new items
  usually fit without awkward ad hoc strings
- `kind` should capture the primary editorial angle of the item, not every
  possible dimension it touches
- `emoji` should remain explicit in slice 1 rather than being derived from
  `kind`
- `sort_day` should stay optional; when absent, file order remains the
  same-month tie-break
- do not require typed references to talks/publications/service/teaching in
  slice 1

Likely later optional fields, only if they earn their keep:

- `homepage_visible`
- lightweight tags beyond the primary `kind`
- `related_publication_keys`
- `related_talk_keys`
- `related_service_keys`
- `related_teaching_offerings`
- future `related_project_keys`

## What Should Stay Hand-Authored

Even if the repeated news items become canonical, the page should still keep:

- the page heading
- page-local metadata in front matter
- any future short intro or framing text
- the homepage section heading and local framing text

This campaign should not try to turn the news page into raw generated output.

## Recommended Slice Order

### Slice 1. Canonical News Model

Goal:

- capture the current news item stream in `site/data/news.json`
- define the smallest stable shared-data model before any route cutover

Invariant after slice 1:

- news entries have one canonical ordered source
- the canonical unit is an individual news item, not a month bucket
- each canonical item has explicit `kind` and explicit `emoji`
- same-month ordering is reviewable through file order plus optional
  `sort_day`
- no public rendering changes yet
- homepage and public news page remain authored consumers for the moment

### Slice 2. Public Wrapper / Route Cutover + News Projection

Goal:

- move the public news wrapper to `site/news/index.dj`
- canonicalize `/news/`
- project the repeated month-grouped news body from canonical news records
- keep the heading, metadata, and any short framing text authored in the
  wrapper

Invariant after slice 2:

- the public news page has a thin authored wrapper over canonical news records
- the canonical public route is `/news/`
- no hand-maintained repeated news item body remains in the wrapper
- renderer-owned month/year grouping reconstructs the current public page
  shape from the flat canonical record list
- homepage news remains explicitly separate for now

Current checkpoint note:

- the route cutover is landed at `site/news/index.dj` with canonical `/news/`
- the homepage now links to `news/`
- the public news body is projected from `site/data/news.json`
- rendered review showed only route/plumbing changes plus projection-owned HTML
  reflow, not news-content drift

### Slice 3. Homepage News Consumer

Goal:

- make the homepage `## News` block derive from the same canonical news
  records with explicit curation policy

Important design note:

- the agreed policy should stay deterministic and anchored to canonical news
  data, not the wall clock
- recency should remain primary
- a small optional stickiness signal can help in heavier-news periods without
  turning the homepage into a hand-curated second registry

Invariant after slice 3:

- homepage and news page can no longer drift silently
- the homepage remains a curated teaser consumer, not a second source of truth
- homepage inclusion policy is explicit and deterministic:
  trailing `12` months from the most recent canonical news month, hard cap
  `15`, always keep the `10` most recent items, and use optional
  `homepage_featured` only for older in-window stickiness when the window
  overflows

Current checkpoint note:

- the homepage `## News` body now projects from canonical news records instead
  of being hand-maintained in `site/pages/index.dj`
- the homepage uses the deterministic trailing-`12`-month rule with optional
  `homepage_featured` overflow stickiness
- at the current data checkpoint, that policy yields a visibly shorter
  homepage news block, which is intentional and expected until later news
  backfill expands the recent window

### Slice 4. Typed Cross-Domain Enrichment

Goal:

- add lightweight references from news items back to existing canonical
  domains only where that clearly earns its keep

Examples:

- related talk
- related publication
- related service item
- related teaching offering
- future related project

Invariant after slice 4:

- news remains canonically editorial, but selected entries can point back to
  stronger fact domains explicitly
- later typed links do not change the fact that news records themselves are
  canonical for the editorial prose

## Important Non-Goals

- deriving all news entries automatically from talks/publications/teaching
- forcing a large site-wide events schema
- mixing homepage current/recent cleanup into the first news slice
- solving the future `projects` domain in the news campaign

## Recommendation

This should be a real later campaign, but it should start narrowly.

The right first move is:

1. treat news as its own editorial domain
2. canonicalize the repeated news item stream
3. give it an honest wrapper route at `site/news/index.dj`
4. only then decide how much homepage reuse and cross-domain enrichment the
   repo actually wants

That is the sober path.
