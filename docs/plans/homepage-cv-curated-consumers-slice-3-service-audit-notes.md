# Homepage / CV Curated Consumers Slice 3: Service Audit Notes

Status: in progress

This note records concrete findings from the service-audit slice planned in
[homepage-cv-curated-consumers-slice-3-service-audit.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md).

## Snapshot

Current canonical service data:

- raw canonical records in
  [site/data/service.json](/Users/ztatlock/www/ztatlock.github.io/site/data/service.json)
- grouped/coalesced view logic in
  [scripts/service_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/service_index.py)

Current grouped-view counts:

- `reviewing`: `32`
- `organizing`: `22`
- `mentoring`: `8`
- `department`: `12`

Current homepage block in
[site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj):

- `2026 - 2029 PLDI Steering Committee`
- `2026 - 2029 PACMPL Advisory Board Member`
- `2022 - Present EGRAPHS Community Advisory Board`
- `2025 FPTalks Co-Organizer`
- `2025 PLDI Program Committee Chair`
- `2024 PLDI Workshops Co-chair`

## What Looks Strong

The current service model already does several important things well.

1. Per-year canonical terms are explicit.

- longer appointments like `PLDI Steering Committee` and
  `PACMPL Advisory Board` are represented as one record per year
- ongoing series like `EGRAPHS Community Advisory Board` and `UW Faculty Skit`
  use the current `ongoing` marker cleanly

2. Grouped/coalesced rendering already works for stable multi-year series.

Examples:

- `2026 - 2029 PACMPL Advisory Board Member`
- `2026 - 2029 PLDI Steering Committee`
- `2022 - Present EGRAPHS Community Advisory Board`
- `2025 - 2027 UW CSE Faculty Graduate Admissions Co-chair`

3. The homepage service block is fully explainable from canonical data.

Every current homepage item is visible in the grouped `organizing` view.
So there is no immediate data-loss bug analogous to a dropped record set.

## Main Seam: Concept Versus Instance

The audit confirms that the central service-model seam is **not** missing
facts. It is the tension between:

- a stable recurring service **series**
- year-specific service **instances** with distinct URLs

This is most obvious for recurring annual series:

- `FPTalks` (`2020` through `2025`)
- `PLDI Workshops` (`2023`, `2024`)
- `EGRAPHS Workshop` (`2022`, `2023`)

Today these remain year-specific in the grouped public view because the current
grouping signature includes `url`.

That behavior is understandable:

- the per-year URL is often the actual best public link for that service term

But it also means the grouped view is currently doing two jobs at once:

- deciding whether terms represent one conceptual recurring role
- deciding whether a single grouped summary entry can still point at a stable
  public URL

Those are related, but they are not the same problem.

One additional clarification from the audit:

- not every service instance needs to belong to a multi-year series
- one-off service entries are valid and expected
- the current discomfort is mainly about recurring entries where a series
  clearly exists, but only implicitly through `series_key`

## Current Series Audit

### Stable Series That Collapse Cleanly Today

These already look good under the current model:

- `pacmpl-advisory-board`
- `pldi-steering-committee`
- `egraphs-community-advisory-board`
- `uw-cse-faculty-graduate-admissions`
- `uw-cse-faculty-recruiting`
- `uw-faculty-skit`

Why they work:

- same conceptual role across years
- no year-local public URL pressure
- current grouped signature collapses them naturally

### Recurring Series That Look Over-Split

These are the clearest current seams:

- `fptalks`
- `pldi-workshops`
- `egraphs-workshop`

Why they are interesting:

- they clearly describe recurring concepts
- they also clearly have year-local instance URLs
- current grouping keeps them split year by year because of those URL changes

This is probably correct for some current consumers, but it is not obviously
the best long-term model for every future consumer.

One useful concrete observation from the current data:

- for the recurring series under pressure, `title` is already stable across
  instances
- the main variation is `url`, with `role` only varying in a small number of
  cases such as `pnw-plse`

So the current seam is less about missing series naming data and more about
how to summarize and link recurring series without losing instance-level facts.

### Series-By-Series Provisional Read

`FPTalks`

- recurring concept is very strong
- each year has its own distinct event URL
- current grouped view keeps each year separate
- provisional read:
  - current instance-by-instance public rendering is defensible
  - future consumers would likely benefit from a stronger concept-level story
    that can still expose per-year instance links

`PLDI Workshops`

- recurring concept is real, but the public meaning is more year-local than
  `FPTalks`
- each year has a distinct organizing-committee URL
- provisional read:
  - probably fine to keep year-local in current public/homepage rendering
  - but still a useful test case for whether later grouped summaries should be
    able to show one concept with multiple year links

`EGRAPHS Workshop`

- recurring concept is real across `2022` and `2023`
- each year has a distinct PLDI-hosted URL
- provisional read:
  - similar to `PLDI Workshops`
  - keep year-local for now, but treat as another example of concept-versus-
    instance pressure on the model

`PNW PLSE`

- same broad concept, but years are non-contiguous and role text changes
- provisional read:
  - current `series_key` still expresses a real recurring identity
  - future grouped helpers should likely keep one series entry structurally
    while rendering it conservatively
  - the current best candidate is:
    - homepage: latest run or latest instance only
    - service page: neutral summary title plus instance bullets

`SRC JUMP: Applications Driving Architectures (ADA)`

- adjacent years
- same URL
- same role
- already collapses cleanly today
- provisional read:
  - current model handles this series well

### Mixed / Special Cases

- `pldi-program-committee-chair`
  appears in both `reviewing` and `organizing`
- `pnw-plse`
  has separated years (`2018`, `2023`) and differing roles
  (`Organizer`, `Co-Organizer`), so it should likely remain non-contiguous even
  if the broader concept is recurring

These cases reinforce that a future concept/instance model, if it ever lands,
would need to remain flexible rather than forcing every same-title series into
one collapsed bucket.

## Homepage Implications Under Current Grouping Semantics

If the homepage recent-service block were derived today from the grouped
`organizing` view using:

- anchor year = current calendar year `2026`
- trailing 3-year window = `2024-2026`

the in-window grouped entries would be:

- `2026 - 2029 PACMPL Advisory Board Member`
- `2026 - 2029 PLDI Steering Committee`
- `2026 Dagstuhl Seminar 26022: EGRAPHS`
- `2022 - Present EGRAPHS Community Advisory Board`
- `2025 FPTalks Co-Organizer`
- `2025 PLDI Program Committee Chair`
- `2024 FPTalks Co-Organizer`
- `2024 PLDI Workshops Co-chair`

So a straight grouped-organizing projection would currently produce `8` items,
not the manually curated `6`.

This is useful because it gives a concrete simulation baseline.

## Early Model Reflection

The current model is still defensible, but the audit is surfacing a real future
question:

Should recurring service series eventually be modeled with a clearer split
between:

- a stable series-level identity
- one or more year-specific instances

That could help future consumers such as:

- homepage summaries
- richer service page summaries
- later highlights blocks
- later cross-domain or per-person summaries

Potential directions to revisit later if the audit concludes they are worth it:

1. keep the current per-year term model, but strengthen grouping/render helpers
   to optionally expose multiple instance links for one grouped concept
2. add stronger concept-level fields while preserving the current term records
3. introduce a fuller concept/instance split only if simpler helper-level
   improvements prove insufficient

Important current interpretation:

- `series_key` is currently only a grouping hint shared by instance records
- it does **not** point at a separate series registry or series object
- that is a legitimate source of design unease, because the repo already
  acknowledges series-like identity without yet giving series any explicit home

That still does not mean an explicit series layer is automatically the right
next move.
It may remain better to keep series implicit in canonical data and add richer
derived grouped helpers in code first.

No recommendation is final yet.
The current conclusion is only that the question is real and worth keeping
explicit during the audit.

## Current Preferred Render Direction

The strongest current design candidate is:

- keep canonical service truth as per-year instances
- add richer derived **series** helpers in code
- let those helpers compute contiguous **runs** within a series
- let `/service/` and the homepage consume those helpers differently

### Summary Label Shape

Current preference:

- grouped series summary with uniform role:
  - `FPTalks Co-Organizer, 2020 - 2025`
  - `PACMPL Advisory Board Member, 2026 - 2029`
- grouped series summary without role:
  - `PLDI Steering Committee, 2026 - 2029`
  - `EGRAPHS Community Advisory Board, 2022 - Present`
- single-instance summary with role:
  - `PNW PLSE 2023, Co-Organizer`
- single-instance summary without role:
  - `Dagstuhl Seminar 26022: EGRAPHS 2026`

Important preferences:

- do not render year-first labels like `2025 FPTalks`
- do not use comma-separated `title, year, role` labels like
  `FPTalks, 2025, Co-Organizer`
- for grouped summaries, prefer `title role, years`
- for single instances, prefer `title year, role`

### Instance Bullets On `/service/`

If grouped series expose instance bullets, those bullets should never be bare
years.

Current preference:

- `[FPTalks 2025](...)`, `Co-Organizer`
- `[FPTalks 2024](...)`, `Co-Organizer`
- `[PLDI Workshops 2024](...)`, `Co-chair`
- `[PNW PLSE 2023](...)`, `Co-Organizer`

The important point is that each bullet should stand on its own:

- title repeated
- year repeated
- role repeated when present

### Link Target Policy

Current preferred policy:

- if a grouped series has multiple distinct instance URLs, homepage projections
  should link to the corresponding entry on `/service/`, not to any one
  external instance URL
- if a series is a singleton or all of its instances share one URL, homepage
  projections should link directly to that external URL when present
- if there is no URL, the homepage entry can remain unlinked

This keeps recurring annual series like `FPTalks` or `PLDI Workshops`
coalesced on the homepage without throwing away the richer per-instance links.

### Anchor Direction

The current leading anchor policy is:

- treat `series_key` as the stable conceptual identity
- derive one or more contiguous **runs** inside each series
- anchor visible `/service/` entries at the run level, not just the series
  level
- if a series has only one run, its anchor can still just be `series_key`
- if a series has multiple runs, each run needs its own stable anchor
- if a visible `/service/` entry is a singleton with no `series_key`, use the
  instance `key`

So under the current preferred design:

- `FPTalks Co-Organizer, 2020 - 2025` would likely anchor at
  `/service/#fptalks`
- `PLDI Workshops Co-chair, 2023 - 2024` would likely anchor at
  `/service/#pldi-workshops`
- `PNW PLSE 2023, Co-Organizer` would likely anchor at
  `/service/#pnw-plse--2023-2023`
- `PNW PLSE 2018, Organizer` would likely anchor at
  `/service/#pnw-plse--2018-2018`

If a future repeated committee or appointment returns after a gap, this run
layer keeps the anchor design stable. For example, a later second run of
`uw-cse-undergraduate-admissions-committee` would not collide with the first.

### Non-Contiguous Series

For non-contiguous series such as `PNW PLSE`, the current preferred behavior
is:

- homepage:
  - show the latest run if there is one
  - otherwise show the latest instance
- `/service/`:
  - allow a neutral series title like `PNW PLSE`
  - render one visible block per run
  - let instance bullets carry the actual years and roles inside each run if
    needed

This avoids misleading fake ranges like `2018 - 2023` while still preserving
the recurring-series connection.

## Academic-Year Semantics Wrinkle

One additional interpretation seam is worth making explicit now:

- for Allen School and similar academic service, a rendered year range like
  `2020 - 2021` often means the `2020-2021 academic year`
- it usually does **not** mean continuous calendar-year coverage from
  January 2020 through December 2021

Current recommendation:

- keep canonical service data at year granularity for now
- allow grouped run summaries like `2020 - 2021` to remain as display
  shorthand
- document that some service ranges should be read as academic-year spans
  rather than literal full-calendar-year intervals

This is important context for future service modeling and rendering, even if it
does not justify a schema change today.

## Rendering / Presentation Seam

The current public service page is factually much better than the old manually
maintained version, but the rendered projection is still visually rough.

Observed current issues from
[build/service/index.html](/Users/ztatlock/www/ztatlock.github.io/build/service/index.html):

- long sections of flat bullets feel dense and monotonous
- nested detail links help, but the overall page still reads like a large
  undifferentiated list dump
- repeated annual organizer/event entries make the `Organizing` section feel
  especially noisy

This is a separate problem from the current audit.
The data-model and grouping audit should come first, but the repo should retain
an explicit later backlog item for service-page formatting/projection polish.

## Current Rendering Direction That Seems Most Promising

The audit is converging on a stronger render split between the public service
page and the homepage.

### Public Service Page

The strongest current candidate is:

- render one grouped summary line per visible run
- then, when a run has distinct yearly links or meaningful instance-level
  variation, render instance sub-bullets underneath

Important rendering preference from the audit:

- year-first labels like `2025 FPTalks` feel unnatural
- prefer year-last labels such as `FPTalks 2025`

And for instance sub-bullets:

- do **not** render just bare years
- repeat enough context to make each instance line readable on its own
- when role matters, repeat the role too

So a plausible future service-page rendering shape would be:

- `FPTalks Co-Organizer, 2020 - 2025`
  - `[FPTalks 2025](...)`, `Co-Organizer`
  - `[FPTalks 2024](...)`, `Co-Organizer`
  - `[FPTalks 2023](...)`, `Co-Organizer`

And similarly:

- `PLDI Workshops Co-chair, 2023 - 2024`
  - `[PLDI Workshops 2024](...)`, `Co-chair`
  - `[PLDI Workshops 2023](...)`, `Co-chair`

This is much stronger than a structure where the sub-bullets are just years.

### Homepage

The homepage likely wants a different consumer policy:

- one selected item per recurring series
- no instance sub-bullets
- select a specific visible run for each included series
- if the included series has multiple distinct instance URLs, link the
  homepage item to the corresponding `/service/` run anchor
- if the included series is a singleton or all of its instances share one URL,
  link directly to that URL when present
- otherwise leave the item unlinked

That would let the homepage stay compact while the public service page becomes
more informative.

## Provisional Conclusions

Current provisional conclusions:

- there is no evidence yet that the current service data is fundamentally
  broken
- there is strong evidence that recurring annual series with year-specific URLs
  are the main stress case for the current grouping semantics
- there is also real design unease around the current halfway status of
  `series_key`: series-like identity exists, but only as an implicit grouping
  hint rather than as an explicit modeled layer
- homepage recent-service policy should **not** be finalized until we decide
  how much conceptual collapsing we actually want for recurring series
- the audit has now produced two concrete follow-on design candidates:
  - richer derived series/run helpers over the current flat instance model
  - a fuller redesign with explicit `series`, `runs`, and nested `instances`
- the service audit should continue by reviewing the recurring annual series one
  by one and deciding whether each should remain instance-driven or gain a
  clearer concept-level story

## Open Questions

1. Should `FPTalks` remain year-specific in homepage and public grouped views,
   or should later consumers be able to show one collapsed `FPTalks` concept
   with multiple instance links?
2. Should `PLDI Workshops` and `EGRAPHS Workshop` behave similarly to
   `FPTalks`, or are they better left year-local?
3. Should homepage `Recent Service / Leadership` ultimately draw only from
   `organizing`, or also include some grouped `department` leadership roles?
4. Is the current single `url` field on a service term enough for future
   grouped summaries, or do recurring concepts eventually want richer link
   support?
5. Once the grouping/model questions are settled, what service-page projection
   and CSS changes would make `/service/` materially easier to scan?
6. Is a future explicit series layer actually needed, or would richer derived
   grouping/render helpers over the existing instance records be enough?
