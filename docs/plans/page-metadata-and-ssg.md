# Page Metadata And SSG Direction

This note captures the likely direction for simplifying page metadata and
deciding whether the site should eventually migrate to a more conventional
static-site generator.

## Current Situation

Historically, the repo maintained one raw HTML `*.meta` sidecar per public
page. That system has now been replaced by structured metadata manifests for
all public pages, but the historical pain points still explain the migration
direction captured in this note.

That gives the site good social/share metadata, but it has real costs:

- the files are repetitive
- the format is brittle because it is raw copied HTML
- values can drift or become internally inconsistent
- agents have to reason about page content and page metadata separately

Examples of the current brittleness:

- page metadata is inserted as opaque HTML during the build
- common fields are duplicated in every file
- a page can have inconsistent `og:*` and `twitter:*` values without any
  structure-aware validation

## Current Repo Observations

The pre-migration corpus strongly suggested that most of the `*.meta` HTML was
mechanical rather than truly authored:

- 41 public `*.meta` files currently exist
- 41 / 41 set `og:type = website`
- 41 / 41 set `twitter:card = summary_large_image`
- 41 / 41 set `og:url` to the canonical page URL
- 40 / 41 `og:title` values match the current HTML page title exactly
- 36 / 41 images follow trivial defaults:
  16 use the site-wide fallback image and 20 use the predictable publication
  `pubs/<slug>/<slug>-meta.png` path
- only a small minority need genuinely special image overrides

This means the part we most need to preserve is not the raw HTML wrapper.
It is the smaller set of actual content decisions:

- the description blurb
- the occasional special share image
- the occasional intentional short title override

## What Problem Are We Actually Solving?

The main problem is not "we lack metadata."

The main problems are:

- too much repetitive hand-maintained metadata
- metadata stored in a weak format
- metadata living separately from the page source
- too much custom build behavior tied to the flat live-served repo root

## Recommendation

Do not rush into a full Jekyll migration just to solve metadata.

Instead:

1. keep metadata as a first-class concept
2. replace raw `*.meta` HTML sidecars with structured page metadata
3. generate sane defaults for most pages
4. keep an explicit future option to migrate the whole site later if the
   broader source/build/deploy split still points that way

## Why Not Jump To Jekyll Right Now?

Jekyll would solve several real problems:

- front matter
- layouts/includes
- conventional page organization
- a more standard static-site workflow

But it also has meaningful downsides here:

- it would require either giving up Djot or adding custom conversion glue
- Liquid is a real ergonomics cost
- the migration would mix several concerns at once:
  metadata, templating, directory layout, and deployment
- the current repo does not yet have a clean authored-source vs built-output
  split, so a Jekyll port now would likely be a large-bang rewrite

The biggest wins for agentic maintenance are not uniquely "Jekyll wins."
Agents mainly benefit from:

- conventional directories
- structured page metadata
- explicit defaults and overrides
- an intentional build/deploy pipeline

We can get those wins without immediately buying into Liquid.

## Recommended Target Design

### Metadata Should Be Structured

Page metadata should stop being raw copied HTML and instead become a small
structured record.

The ideal eventual shape is page-local structured metadata, for example YAML
front matter or an adjacent structured sidecar.

For agentic maintenance, YAML front matter is the strongest default because:

- it is common and recognizable
- it keeps metadata close to content
- it is easy to validate
- it maps cleanly to many future systems, including Jekyll

### Metadata Should Have Defaults

Most pages should not need fully custom metadata files.

The build should be able to derive defaults such as:

- canonical URL from page path
- page title from front matter or the first heading
- default share image from a site-wide image
- `og:type = website`
- `twitter:card = summary_large_image`
- `twitter:url = canonical URL`

Pages should only override what is actually special, typically:

- description
- share image
- explicit title override

### Publication Pages Need A Better Path

Publication pages are the clearest case where metadata matters and where the
historical sidecar pattern was annoying.

The build should be able to derive or accept structured values for:

- title
- description
- canonical URL
- share image

The publication scaffold should populate these fields directly, instead of
creating a raw HTML `*.meta` file.

## Migration Shape I Would Recommend

### Stage 1 (Completed For Public Pages)

Keep the current site generator and flat page layout, but introduce a
structured metadata format with generated defaults.

The least disruptive version was:

- allow structured metadata in shared manifests
- generate metadata tags from that structure
- keep draft pages flexible while they remain drafts

This stage simplified the metadata system without changing the overall site
architecture.

### Stage 2

Move the metadata source closer to content.

At this point we should choose one of:

- YAML front matter inside `*.dj`
- a structured adjacent sidecar such as `*.page.yaml`

My bias is toward YAML front matter because it is more conventional and gives
us a better bridge to future tools.

### Stage 3 (Completed For Public Pages)

Deprecate raw HTML `*.meta` files.

All public pages have now migrated to structured metadata plus defaults, and
the build rejects raw `*.meta` blobs.

### Stage 4

Handle the larger source/build/deploy migration as its own explicit campaign.

Only after that should we seriously reconsider whether the repo still wants a
custom Djot-based build or whether it is worth porting to Jekyll or another
static-site generator.

## Decision Framework For Jekyll Later

We should reconsider Jekyll later only if we conclude that we specifically
want most of the following:

- a conventional static-site layout now
- front matter and layout machinery managed by the framework
- deeper alignment with GitHub Pages conventions
- willingness to live with Liquid as the main templating system
- willingness to convert content away from the current Djot-centric build

If the main goals are instead:

- plain, inspectable content
- small custom logic
- Djot content preservation
- better agent ergonomics than Liquid provides

then the more likely right answer is:

- keep the custom build, but make it more explicit and conventional

## Tentative Decision

Current recommendation:

- keep Djot for now
- do not migrate to Jekyll in the near term
- move non-publication page metadata toward YAML front matter
- keep publication metadata under separate review while the broader
  publication-data model is still unsettled
- treat a full SSG migration as a later architectural campaign, not as the
  immediate fix for `.meta` file sprawl

## Current Incremental Implementation

As of March 20, 2026, all public pages have completed the first metadata
migration away from raw sidecars:

- public non-publication page metadata initially moved into
  `manifests/page-metadata.json`
- public publication metadata now lives in
  `manifests/publication-metadata.json`
- the build renders generated `<meta>` tags from those manifests
- public pages no longer use raw `*.meta` sidecars
- draft pages may still build without metadata while they remain drafts

This is a substantial milestone, but not the full metadata redesign.
The next design question is no longer how to move ordinary pages closer to
content. That has now happened. The remaining metadata-design question is
whether publication metadata should eventually fold into a broader publication
single source of truth.

As of the current prototype:

- all current public non-publication pages now use YAML front matter in
  `*.dj` (currently 20 public pages)
- the mixed-mode fallback has been removed for ordinary public pages
- publication pages remain on `manifests/publication-metadata.json`
- the current parser intentionally supports only the flat scalar metadata
  fields already in use: `description`, `share_description`, `image_path`,
  and `title`
