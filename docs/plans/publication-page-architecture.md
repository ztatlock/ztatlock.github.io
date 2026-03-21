# Publication Page Architecture

This note captures a careful review of how publication pages currently work in
the website repo and proposes a target design for making them more
single-sourced, more local to their assets, and more predictable to maintain.

The goal is not to jump into a migration immediately.
The goal is to make the design space explicit and choose a direction that
preserves the strong template-y character of publication pages while reducing
duplication and root-level sprawl.

## Current State

As of March 20, 2026:

- 21 publication pages exist as top-level `pub-<slug>.dj` sources
- 21 publication asset directories exist under `pubs/<slug>/`
- publication page metadata is now in mixed mode:
  12 migrated pages now source metadata and page bodies from local
  `publication.json` records, while 9 untouched pages still fall back to
  `manifests/publication-metadata.json`
- top-level `pub-<slug>.dj` files remain as transition-time build anchors and
  draft/public status stubs
- publication assets already live locally and canonically in their own
  per-publication directories

This means the repo already has the *right locality for assets* but not yet
the right locality for the authored publication record.

## What Is Good About The Current Design

- Publication assets already live in the right place:
  `pubs/<slug>/`.
- Publication pages are intentionally highly regular.
- The visual structure is stable and easy to recognize.
- The current template is simple enough to understand.
- Small core artifacts are already local and repo-hosted by policy.

This is a good foundation.
The design problem is not that publication pages are chaotic.
The design problem is that the same publication facts are spread across too
many files.

## Audit Findings

### 1. The Page Structure Is Highly Template-Oriented

Across the 21 current `pub-*.dj` pages:

- 21 / 21 have an `Abstract` section
- 21 / 21 have a `BibTeX` section
- 13 / 21 have a `Talk` section
- 1 / 21 has an additional `Extra` section

The dominant section patterns are:

- 12 pages: `Abstract`, `Talk`, `BibTeX`
- 8 pages: `Abstract`, `BibTeX`
- 1 page: `Abstract`, `Talk`, `Extra`, `BibTeX`

That is a strong sign that the common publication-page skeleton should be
generated, not hand-maintained page by page.

### 2. The Asset Layout Is Already Very Regular

Across the 21 publication directories under `pubs/`:

- 21 / 21 have `<slug>.pdf`
- 21 / 21 have `<slug>.bib`
- 21 / 21 have `<slug>-abstract.md`
- 20 / 21 have `<slug>-absimg.png`
- 20 / 21 have `<slug>-meta.png`
- 16 / 21 have `<slug>-slides.pdf`
- 3 / 21 have `<slug>-slides.pptx`
- 4 / 21 have `<slug>-poster.pdf`

This is exactly the kind of regular filesystem shape that should be treated as
the canonical asset contract for a generated publication page.

### 3. The Current Pages Duplicate Content Already Stored In `pubs/<slug>/`

For a typical publication page, the following data is repeated:

- abstract text appears both in the page body and in `<slug>-abstract.md`
- BibTeX appears both in the page body and in `<slug>.bib`
- asset paths are repeated in the page body even though they are derivable
  from the slug and the canonical asset naming scheme

Examples:

- [pub-2024-asplos-lakeroad.dj](/Users/ztatlock/www/ztatlock.github.io/pub-2024-asplos-lakeroad.dj)
  duplicates both
  [2024-asplos-lakeroad-abstract.md](/Users/ztatlock/www/ztatlock.github.io/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad-abstract.md)
  and
  [2024-asplos-lakeroad.bib](/Users/ztatlock/www/ztatlock.github.io/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.bib).
- [pub-2021-iclr-dtr.dj](/Users/ztatlock/www/ztatlock.github.io/pub-2021-iclr-dtr.dj)
  duplicates both
  [2021-iclr-dtr-abstract.md](/Users/ztatlock/www/ztatlock.github.io/pubs/2021-iclr-dtr/2021-iclr-dtr-abstract.md)
  and
  [2021-iclr-dtr.bib](/Users/ztatlock/www/ztatlock.github.io/pubs/2021-iclr-dtr/2021-iclr-dtr.bib).

This duplication is the clearest signal that publication pages want a stronger
single source of truth than the current hand-maintained top-level `pub-*.dj`
files.

### 4. Publication Facts Are Repeated Outside The Page Too

A publication’s title and citation-level identity are duplicated at least
across:

- the publication page
- [publications.dj](/Users/ztatlock/www/ztatlock.github.io/publications.dj)
- sometimes [index.dj](/Users/ztatlock/www/ztatlock.github.io/index.dj)
- [manifests/publication-metadata.json](/Users/ztatlock/www/ztatlock.github.io/manifests/publication-metadata.json)

So the duplication problem is not only “page body vs. asset directory.”
It is also “publication page vs. site-wide lists.”

### 5. The Current URL Shape Is An Accident Of The Old Root-Heavy Design

Today publication pages live at root-level URLs such as:

- `pub-2024-asplos-lakeroad.html`

But the actual publication locality already lives under:

- `pubs/2024-asplos-lakeroad/`

Since backward compatibility with old URLs is explicitly not a goal, we are
free to choose a more rational final URL shape if that improves the design.

### 6. `templates/REFS` Is Part Of The Current Publication Rendering Model

Publication pages and publication listings currently rely on the global
reference registry in [templates/REFS](/Users/ztatlock/www/ztatlock.github.io/templates/REFS).

This matters especially for author rendering, where the current content uses
patterns like:

- `[Gus Henry Smith][Gus Smith]`
- `[Yisu Remy Wang][Remy Wang]`
- `[Ben Kushigian][]`

So the first-cut publication schema should **not** force us to solve a full
cross-site people registry immediately.
It should support a pragmatic author representation that can still render
through the existing global refs file.

### 7. `publications.dj` Is Broader Than The Detailed Publication Page Set

The site currently has:

- 21 local detailed publication pages
- 69 total publication entries in
  [publications.dj](/Users/ztatlock/www/ztatlock.github.io/publications.dj)

So the detailed publication pages are only a subset of the broader publication
record the site already maintains.

That means the long-term publication data model should eventually be able to
serve both:

- detailed publication pages with local assets
- bibliography-only or external-landing publication entries

However, the first migration does **not** need to solve that whole problem at
once.
It is still reasonable to start with the 21 existing detailed publication
pages, as long as we do not paint ourselves into a corner.

### 8. The Current Assembly Path Strongly Favors Generating Djot, Not Raw HTML

Today the page build path in
[Makefile](/Users/ztatlock/www/ztatlock.github.io/Makefile)
does this:

- renders the page head from shared templates
- takes the page body as Djot
- appends [templates/REFS](/Users/ztatlock/www/ztatlock.github.io/templates/REFS)
- runs the combined content through `djot`

This is important for publication design.

It means a generated publication page should probably emit Djot as its body
representation, not raw HTML.
That keeps publication pages aligned with the rest of the site and lets them
continue using the existing reference/link machinery naturally.

## What Actually Varies Across Publication Pages

The current pages are not all identical, but the variation is narrow and
understandable.

### Regular Core Data

Every publication page has some form of:

- title
- author list
- venue/year line
- preview image + paper link
- standard link cluster
- abstract
- BibTeX

### Optional But Common Data

Many publication pages also have:

- public talk URL
- slides
- poster
- project URL
- code URL
- arXiv URL
- publisher URL

### Rare / Custom Data

Only a small number need something beyond the standard pattern:

- teaser links
- demo links
- a special extra section
- talk embeds with page-specific prose
- unusual link labels like `event` or `VSCode`

This suggests a design with:

- a generated common page skeleton
- a structured standard link model
- a small escape hatch for rare extra content

## Design Constraints

Any new publication-page design should satisfy these constraints:

- keep publication assets local to `pubs/<slug>/`
- reduce duplication rather than just moving it around
- keep the strongly template-y structure of publication pages
- support optional extra sections without forcing all publications into
  identical content
- avoid introducing another giant central publication database too early if a
  per-publication local design can work first
- leave room for a later broader single source of truth that can also feed
  publication lists, the homepage, CV views, and artifact inventories

### Explicit Non-Goals

- preserving old publication-page URLs
- preserving root-level `pub-<slug>.dj` as a forever authored-source pattern
- solving the whole cross-site people/author identity problem in the first
  step
- solving every publication-derived list view in the same first migration

## Design Space

### Option A: Keep Handwritten `pub-<slug>.dj` Pages

This is the current model, perhaps with a few automatic includes.

#### Strengths

- lowest migration cost
- preserves maximum local page flexibility
- fits the existing build shape

#### Weaknesses

- keeps the most duplication
- leaves authored publication data split across root files, asset files, and
  manifests
- keeps the publication authored-source story root-heavy and less local than it
  should be

#### Assessment

This is workable, but it is not the direction the audit points toward.

### Option B: One Global Publication Database

Move all publication records into a single big manifest such as
`manifests/publications.json`, then generate pages/lists from it.

#### Strengths

- strongest central single source of truth
- easiest path to generating publications index, homepage listings, CV views,
  etc.

#### Weaknesses

- weak locality to publication assets
- a giant central file may become awkward to edit
- publication-specific extra content becomes harder to keep near the
  publication itself
- risks recreating the same “manifest far from content/assets” problem we just
  removed for ordinary pages

#### Assessment

This may be attractive later for aggregation, but it is probably not the best
*first* redesign step.

### Option C: Per-Publication Structured Record In `pubs/<slug>/`

Give each publication directory its own structured record, for example:

```text
pubs/2024-asplos-lakeroad/
  publication.json
  2024-asplos-lakeroad.pdf
  2024-asplos-lakeroad.bib
  2024-asplos-lakeroad-abstract.md
  2024-asplos-lakeroad-absimg.png
  2024-asplos-lakeroad-meta.png
  extra.dj              # optional
```

Then generate `pub-<slug>.html` from:

- the structured publication record
- the canonical local artifacts in the same directory
- an optional `extra.dj` or similar escape hatch

#### Strengths

- strongest locality to assets
- keeps publication data near the publication itself
- fits the current asset layout naturally
- reduces root clutter by removing top-level authored `pub-*.dj` pages
- gives a clean basis for later aggregation into publication lists
- aligns with your intuition that publications are highly template-driven

#### Weaknesses

- requires a new renderer/scaffold path for publication pages
- needs a careful answer for how to represent authors and venue formatting
- needs an escape hatch for genuinely custom sections

#### Assessment

This is the strongest target design.
It preserves the template-y nature of publication pages while making the
publication directory the actual home of the authored publication record.

## Recommended Target Design

The recommended target is:

### 1. One Publication Directory Per Publication

Each publication directory should become the canonical home of:

- the small repo-hosted publication artifacts
- the authored structured publication record
- any rare publication-specific extra content

### 2. A Per-Publication JSON Record

Use a file like:

- `pubs/<slug>/publication.json`

This record should hold the structured facts that are currently duplicated
across page body, publication metadata manifest, and publication listings.

Recommended first-cut authored fields:

- `title`
- `authors`
- `venue`
- `badges`
  for things like spotlight/distinguished paper notes
- `description`
  the share/metadata blurb currently living in
  `manifests/publication-metadata.json`
- `share_description`
  optional shorter social/share blurb when it differs from `description`
- `meta_image_path`
  optional override for the share image when it should not be derived from the
  canonical `<slug>-meta.*` asset
- `links`
  for external and optional links such as:
  `talk`, `teaser`, `project`, `code`, `demo`, `publisher`, `arxiv`, `event`,
  `vscode`
- `talks`
  optional ordered array of talk entries for pages that render a `Talk`
  section

The slug itself should remain implicit from the directory name.

For the first cut:

- `authors` should be simple structured entries that can still render through
  [templates/REFS](/Users/ztatlock/www/ztatlock.github.io/templates/REFS),
  for example plain names plus an optional ref key
- `venue` should optimize for clean rendering rather than overfitting a fully
  normalized conference ontology on day one

### 2a. Explicit Authored Vs. Derived Data

The first-cut schema should be disciplined about what is authored in
`publication.json` and what is derived from the directory name and canonical
asset layout.

#### Authored In `publication.json`

- `title`
- `authors`
- `venue`
- `badges`
- `description`
- `share_description`
- `meta_image_path`
- external or non-canonical `links`
- `talks`

#### Derived From The Slug And Asset Directory

- `slug`
  from the directory name
- `year`
  from the slug prefix
- publication page URL
  eventually `/pubs/<slug>/`
- paper link
  from `<slug>.pdf`
- BibTeX link
  from `<slug>.bib`
- abstract body
  from `<slug>-abstract.md`
- preview image for the page body
  from `<slug>-absimg.*`
- default share image
  from `<slug>-meta.*`
- local slides link when present
  from `<slug>-slides.pdf` with limited legacy support for
  `<slug>-slides.pptx`
- local poster link when present
  from `<slug>-poster.pdf`

This split is important.
The goal is to avoid repeating facts that are already encoded by the
filesystem contract.

### 2b. First-Cut Shape Of Key Fields

#### `authors`

Recommended shape:

```json
[
  { "name": "Gus Henry Smith", "ref": "Gus Smith" },
  { "name": "Zachary Tatlock" }
]
```

Rules:

- `name` is always the display text
- `ref` is optional and maps to an entry in
  [templates/REFS](/Users/ztatlock/www/ztatlock.github.io/templates/REFS)
- when `ref` is absent, the renderer should emit plain text rather than a
  broken Djot reference

#### `venue`

Recommended shape for the first cut:

```json
"Architectural Support for Programming Languages and Operating Systems (ASPLOS)"
```

This should remain a display-oriented string at first.
We can normalize venue structure later if it becomes clearly useful.

#### `links`

Recommended shape:

```json
{
  "talk": "https://www.youtube.com/watch?v=2XgOWAtJ8vs",
  "code": "https://github.com/gussmith23/lakeroad",
  "publisher": "https://doi.org/10.1145/3620665.3640387",
  "arxiv": "https://arxiv.org/abs/2401.16526"
}
```

Rules:

- only include links that are not already derived from canonical local assets
- the renderer should emit the standard ordered link cluster
- local `paper`, `slides`, `poster`, and `bib` links should be added
  automatically when their canonical files exist
- `links.talk` should be allowed for pages that have a public talk URL but do
  not render a full `Talk` section

#### `talks`

Recommended shape:

```json
[
  {
    "event": "ASPLOS 2024",
    "speakers": [{ "name": "Gus Smith", "ref": "Gus Smith" }],
    "url": "https://www.youtube.com/watch?v=2XgOWAtJ8vs",
    "embed": "https://www.youtube.com/embed/2XgOWAtJ8vs",
    "title": "ASPLOS 2024 talk by Gus Smith"
  }
]
```

Rules:

- if `talks` is non-empty, the page gets a `## Talk` section
- if `links.talk` is absent, the first talk entry provides the standard
  `talk` link in the link cluster
- additional talk entries render in the section but do not add extra link
  badges to the link cluster
- `speakers` should reuse the same simple author-like shape as `authors`

#### `extra.dj`

`extra.dj` should be the escape hatch for rare page-specific content.

It should contain Djot content directly.
The first-cut schema does **not** need a parallel JSON `extra` field.

### 3. Keep Long-Form Text And Canonical Small Artifacts As Files

Do **not** force everything into JSON.

Keep these as separate files in the publication directory:

- abstract in `<slug>-abstract.md`
- BibTeX in `<slug>.bib`
- paper/slides/poster/images in their canonical asset files

Reasons:

- long prose is better in Markdown than JSON strings
- BibTeX should remain a real `.bib`
- the asset files are already canonical and versionable

### 4. Generate The Common Publication Page Skeleton

The common generated publication page should include:

- title
- author list
- venue/year/badges line
- preview image linking to paper
- standard ordered link cluster
- abstract rendered from `<slug>-abstract.md`
- optional talk section if `talks` is non-empty
- BibTeX rendered from `<slug>.bib`
- optional appended extra content if `extra.dj` exists

The generated body should preferably be emitted as Djot and then pass through
the existing site build path, rather than generating raw HTML directly.

The standard link order should be fixed and generated by presence, for
example:

- paper
- teaser
- talk
- slides
- poster
- project
- code
- demo
- event
- VSCode
- publisher
- arXiv
- bib

Local canonical file links such as paper, BibTeX, slides, and poster should be
derived automatically from the slug and the asset files when present.
They should not need to be hand-written in the publication record.

For the first cut, the generator should support the current rare exceptions:

- local slides may be either PDF or legacy PPTX
- preview/share images may not all be PNG
- the `talk` badge in the link cluster should come from the first `talks`
  entry when present

### 5. Treat Extra Page Content As An Escape Hatch, Not The Default

Most publications do not need bespoke page prose beyond the standard template.

For rare cases like DTR’s extra embedded videos, allow an optional file such
as:

- `pubs/<slug>/extra.dj`

This avoids forcing unusual page content into JSON while keeping the common
page structure generated.

## Worked First-Cut Examples

### Example A: Clean Default Publication

```json
{
  "title": "FPGA Technology Mapping Using Sketch-Guided Program Synthesis",
  "authors": [
    { "name": "Gus Henry Smith", "ref": "Gus Smith" },
    { "name": "Benjamin Kushigian", "ref": "Ben Kushigian" },
    { "name": "Vishal Canumalla" },
    { "name": "Andrew Cheung" },
    { "name": "Steven Lyubomirsky" },
    { "name": "Sorawee Porncharoenwase" },
    { "name": "René Just" },
    { "name": "Gilbert Louis Bernstein", "ref": "Gilbert Bernstein" },
    { "name": "Zachary Tatlock" }
  ],
  "venue": "Architectural Support for Programming Languages and Operating Systems (ASPLOS)",
  "description": "Lakeroad applies sketch-guided program synthesis to FPGA technology mapping, improving mapping coverage while providing correctness guarantees.",
  "links": {
    "code": "https://github.com/gussmith23/lakeroad",
    "publisher": "https://doi.org/10.1145/3620665.3640387",
    "arxiv": "https://arxiv.org/abs/2401.16526"
  },
  "talks": [
    {
      "event": "ASPLOS 2024",
      "speakers": [{ "name": "Gus Smith", "ref": "Gus Smith" }],
      "url": "https://www.youtube.com/watch?v=2XgOWAtJ8vs",
      "embed": "https://www.youtube.com/embed/2XgOWAtJ8vs",
      "title": "ASPLOS 2024 talk by Gus Smith"
    }
  ]
}
```

Everything else should be derived from:

- the slug `2024-asplos-lakeroad`
- the canonical files in
  [pubs/2024-asplos-lakeroad](/Users/ztatlock/www/ztatlock.github.io/pubs/2024-asplos-lakeroad)

### Example B: Publication With Extra Structure

```json
{
  "title": "Dynamic Tensor Rematerialization",
  "authors": [
    { "name": "Marisa Kirisame" },
    { "name": "Steven Lyubomirsky" },
    { "name": "Altan Haan" },
    { "name": "Jennifer Brennan" },
    { "name": "Mike He" },
    { "name": "Jared Roesch" },
    { "name": "Tianqi Chen" },
    { "name": "Zachary Tatlock" }
  ],
  "venue": "International Conference on Learning Representations (ICLR)",
  "badges": ["★ Spotlight Paper"],
  "description": "Dynamic Tensor Rematerialization (DTR), is an online algorithm for checkpointing deep learning models. DTR enables training under restricted memory budgets by freeing intermediate activations from memory and recomputing them on demand. Unlike static checkpointing techniques, DTR supports dynamic models and achieves comparable performance. For example, DTR can train an N-layer linear feedforward network on an Ω(√ N) memory budget with only O(N) tensor operations. We prototyped in PyTorch simply by interposing on tensor allocations and operator calls.",
  "share_description": "DTR is an online algorithm for checkpointing deep learning models that enables training under restricted memory budgets by freeing intermediate activations from memory and recomputing them on demand.",
  "links": {
    "teaser": "https://www.youtube.com/watch?v=kxlbpwBJzA4",
    "project": "http://sampl.cs.washington.edu/projects/dtr.html",
    "code": "https://github.com/uwsampl/dtr-prototype",
    "publisher": "https://openreview.net/forum?id=Vfs_2RnOD0H",
    "arxiv": "https://arxiv.org/abs/2006.09616"
  },
  "talks": [
    {
      "event": "ICLR 2021",
      "speakers": [{ "name": "Steven Lyubomirsky" }],
      "url": "https://www.youtube.com/watch?v=S9KJ37Sx2XY",
      "embed": "https://www.youtube.com/embed/S9KJ37Sx2XY"
    }
  ]
}
```

In this case:

- the main page still comes from the standard generated skeleton
- the two extra embedded videos and prose should move into `extra.dj`
- local `slides`, `poster`, `paper`, and `bib` links should still be derived
  automatically

### 6. Prefer A Directory-Local Final URL Shape

The preferred final publication-page URL shape is:

- `https://ztatlock.net/pubs/<slug>/`

implemented as:

- `pubs/<slug>/index.html`

This is a better fit than root-level `pub-<slug>.html` because:

- it matches the actual asset locality
- it removes root-level publication-page clutter
- it makes the publication directory a self-contained unit

However, this should still be treated as a cutover step, not necessarily the
first implementation step.

## Important Non-Goal

Do **not** try to solve the whole people-data problem in the first step.

Author names currently have some formatting and alias variation, for example:

- `[Gus Henry Smith][Gus Smith]`
- `[Yisu Remy Wang][Remy Wang]`

So a future people registry may be worth having, but it should be treated as a
separate design problem.

The first publication-record design should be allowed to use a pragmatic
representation for authors, even if it is not the final forever model.

## Execution Plan

### Phase 1: Freeze The Target Model

Decide and write down:

- the first-cut `publication.json` schema
- the optional `extra.dj` escape hatch
- the preferred final URL shape:
  `pubs/<slug>/index.html`
- the canonical generated link order
- how authors are represented in the first cut
- whether the first migration scope is explicitly limited to the 21 current
  detailed publication pages

This phase should stay pragmatic.
Do not overfit for a future people registry yet.

### Phase 2: Build A Renderer Against One Stable Output Shape

Build a publication renderer that reads:

- `pubs/<slug>/publication.json`
- `<slug>-abstract.md`
- `<slug>.bib`
- canonical local assets
- optional `extra.dj`

and emits the publication page from the template.

For the first implementation step, it is acceptable to keep the current
output-path shape temporarily if that makes verification simpler.
Even though preserving old URLs is not a goal, separating:

- data-model migration
- URL cutover

will make the campaign easier to reason about.

### Phase 3: Pilot One Clean Publication

Pick one clean, representative publication and generate its page from:

- `pubs/<slug>/publication.json`
- `<slug>-abstract.md`
- `<slug>.bib`
- canonical assets in `pubs/<slug>/`

Do **not** migrate all publications immediately.

Success criteria:

- no output regression for the pilot page
- materially less duplicated data
- scaffold feels simpler, not more magical
- the resulting layout still feels like “our publication page template”

### Phase 4: Pilot One Publication With Non-Default Structure

Before broad migration, pilot one publication that exercises rarer structure,
for example:

- a real `Talk` section
- optional extra content
- unusual links like `demo`, `event`, or `VSCode`

This is the step that proves the escape hatch is good enough.

### Phase 5: Generate One List View From The Same Record

Before a broad migration, test whether the same pilot publication record can
also generate a publication-list entry for:

- `publications.dj` or its eventual replacement

This is the real proof that the publication record is becoming a useful
single source of truth rather than merely a new way to generate the same page.

### Phase 6: Broader Migration

If the pilot feels clearly better:

- migrate more publication pages in batches
- migrate publication metadata out of
  `manifests/publication-metadata.json` and into per-publication records
- remove top-level authored `pub-*.dj` sources

### Phase 7: URL Cutover

Once the generated publication-record path is working well:

- move publication page outputs to `pubs/<slug>/index.html`
- update site-wide links to point at `/pubs/<slug>/`
- remove old root-level `pub-*.html` outputs

Because backward compatibility is an explicit non-goal, this cutover can be
clean and decisive.

## Recommendation

The recommended target is:

1. keep publications highly template-driven
2. move the authored publication record into each publication directory
3. generate publication pages from a per-publication structured record plus
   local canonical files
4. keep long-form abstract/BibTeX as separate canonical files
5. allow a small `extra.dj` escape hatch for rare custom sections
6. later test whether the same publication record can also generate list views
7. cut over publication page URLs to directory-local paths once the generator
   is stable

This design best matches the current repo evidence and your stated intuition:
publication pages are special, regular, multi-part, and strongly asset-local.
They should behave more like generated structured records than like bespoke
ordinary pages.
