# Build System Route Model

This note is a broader design reflection on the website build system after the
publication-local record migration.

The immediate trigger was the question:

- should publication pages stop building as root-level `pub-<slug>.html`
  and instead build under `pubs/<slug>/`?

That question exposed a deeper issue:

the current build is intentionally simple, but it is simple partly because it
assumes every page is a top-level `*.dj -> *.html` transformation.

That assumption has now become the main structural pressure point.

## The Four Path Concepts

These are the concepts that matter.

### 1. Source Path

The source path is the file or files we edit.

Examples:

- ordinary page:
  `about.dj`
- publication page:
  `pubs/2024-asplos-lakeroad/publication.json`
  plus canonical files in the same directory

### 2. Output Path

The output path is the generated file committed for hosting.

Examples:

- ordinary page today:
  `about.html`
- possible publication page output:
  `pubs/2024-asplos-lakeroad/index.html`

### 3. Public URL

The public URL is the site-relative address we link to from the rest of the
site.

Examples:

- ordinary page:
  `/about.html`
- index page:
  `/`
- possible publication page route:
  `/pubs/2024-asplos-lakeroad/`

### 4. Canonical URL

The canonical URL is the full absolute preferred public URL the page declares
in metadata for search engines, social sharing, and deduplication.

Examples:

- `https://ztatlock.net/about.html`
- `https://ztatlock.net/`
- `https://ztatlock.net/pubs/2024-asplos-lakeroad/`

## Why This Has Felt Invisible Until Now

In the current flat model, these concepts nearly collapse into one another:

- source path:
  `about.dj`
- output path:
  `about.html`
- public URL:
  `/about.html`
- canonical URL:
  `https://ztatlock.net/about.html`

That is why the current build feels so direct and understandable.

The problem is not that this model is bad.
The problem is that it only stays invisible while the site stays flat.

As soon as we want route-aware structure, the distinctions become real.

## What Is Good About The Current Build

The current homebrew build has important strengths we should preserve:

- it is small
- it is inspectable
- it is source-first
- it has very few moving parts
- it keeps Djot content plain and direct
- the common case is easy to understand

Those are real strengths.
We should not throw them away casually.

## What Is Actually Straining

The problem is not Djot itself.
The problem is that several responsibilities are currently coupled to the same
top-level filename convention.

Today the build mostly assumes:

- page discovery comes from top-level `*.dj`
- draft status comes from `# DRAFT` in that source file
- page title comes from that source file
- output path is `<stem>.html`
- public URL is `/<stem>.html`
- canonical URL is `https://ztatlock.net/<stem>.html`
- validation can scan only top-level `*.html`
- sitemap generation can list output files directly as public URLs

That coupling is what makes nested routes feel “too hard” in the current
system.

## Audit Summary

The assumption is deeply baked in:

- [Makefile](/Users/ztatlock/www/ztatlock.github.io/Makefile)
  discovers pages from top-level `*.dj`, generates `%.html: %.dj`, and builds
  sitemaps from those root-level outputs.
- [page_source.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_source.py)
  treats page identity as a top-level page stem and publication drafts as a
  special case of top-level stub files.
- [page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
  derives canonical URLs from page stems by appending `.html`.
- legacy `validate_site.py` (now retired) scanned top-level `*.html` and
  top-level `pub-*.html`.
- legacy `check.sh` (now retired) treated draft detection and
  generated-output cleanup as top-level-page logic.
- authored links in [index.dj](/Users/ztatlock/www/ztatlock.github.io/index.dj),
  [news.dj](/Users/ztatlock/www/ztatlock.github.io/news.dj), and
  [publications.dj](/Users/ztatlock/www/ztatlock.github.io/publications.dj)
  still target root-level publication outputs

So yes: route awareness is not a local change.

## The Right Design Goal

We do **not** want a highly dynamic, magical, or framework-heavy system.

We want:

- dead-simple editing
- rational structure
- modularity
- single source of truth
- a small number of explicit rules

That means the right move is not “generalize everything.”
The right move is to add the minimum explicit route model needed to support
the site we actually want.

## Good Simplicity Vs. Accidental Simplicity

This distinction matters.

### Good Simplicity

- a few explicit concepts
- clear defaults
- one obvious source of truth
- localized special cases

### Accidental Simplicity

- everything works only because filenames happen to line up
- one convention quietly carries multiple responsibilities
- exceptions feel expensive because there is no explicit model underneath

The current build has a lot of good simplicity, but this route problem is a
case of accidental simplicity.

## Minimal Route-Aware Architecture

The smallest sane route-aware design is:

- keep the ordinary-page workflow almost exactly as it is
- introduce one explicit route model in code
- support only two page classes for now:
  - ordinary pages
  - publication pages

That is enough.

We do **not** need:

- a giant route manifest
- a per-page handwritten routing table
- a plugin system
- a full conventional SSG immediately

## Recommended Core Abstraction

Introduce one small route model in Python, conceptually something like:

```text
Route
  kind
  key
  source inputs
  output path
  public url
  canonical url
  draft/public status
```

The key point is not the exact class shape.
The key point is that these concepts should be computed once in one place,
instead of being re-derived ad hoc across Makefile rules, metadata logic,
validators, and sitemaps.

## Two Page Classes Are Enough For Now

### Ordinary Page

Rule:

- source: top-level `<stem>.dj`
- output: top-level `<stem>.html`
- public URL: `/<stem>.html`, except `index -> /`
- canonical URL: absolute form of the public URL
- draft: `# DRAFT` in the Djot source

This keeps the common case exactly as simple as it is now.

### Publication Page

Rule:

- source: `pubs/<slug>/publication.json`
  plus canonical files in the same directory
- output: `pubs/<slug>/index.html`
- public URL: `/pubs/<slug>/`
- canonical URL: absolute form of the public URL
- draft: publication-local status, likely `draft: true`

This makes publication pages special in a controlled and explicit way, which
is already true in practice.

## Why This Still Counts As Simple

Because most authors will still only encounter one of two workflows:

### Ordinary Page Workflow

- edit `about.dj`
- run `make about.html`

### Publication Workflow

- edit `pubs/<slug>/publication.json`
- edit the abstract/BibTeX/assets in the same directory
- run the publication build target

That is still simple.

What changes is not the editing model.
What changes is that the build stops pretending every page is the same kind of
object.

## Where Route Awareness Should Live

The route model should become the small central place that answers:

- what pages exist
- whether a page is draft or public
- where a page builds to
- what its public URL is
- what its canonical URL is

Then these consumers should derive from that shared model:

- `Makefile`
- metadata rendering
- sitemap generation
- validation
- draft-output checks
- publication scaffolding

That is the real simplification.
It replaces many baked-in filename assumptions with one explicit rule source.

## Important Constraint: Keep The Defaults Strong

The route-aware system should still preserve strong defaults.

For example:

- ordinary pages should not need explicit route metadata
- publication routes should be derived from the slug and directory layout
- no page should need a custom route declaration unless there is a real reason

If the route model becomes a bunch of page-by-page exceptions, we have failed.

## What This Means For Publication Cutover

The publication output cutover is now clearly a **downstream** step, not the
first step.

The right sequence is:

1. define the route model
2. centralize route computation
3. make build/validation/sitemap use that model
4. only then move publication outputs into `pubs/<slug>/index.html`

That is safer and conceptually cleaner than treating publication cutover as an
isolated local refactor.

## What This Means For The Broader Site

This issue is not just about publications.
It is the first real sign that the current flat-root live-served repo model is
starting to push against its limits.

That does **not** mean we should jump to Jekyll tomorrow.

It does mean the bigger source/build/deploy design question is becoming more
important, because route awareness is one of the first things conventional
systems already model explicitly.

## Current Recommendation

Do not do the publication output cutover yet.

Instead:

1. accept the current publication-local record system as a good steady state
   for now
2. design the minimal route-aware build model
3. decide whether we still want to implement that model inside the current
   custom build
4. only then revisit publication output cutover

## Practical Next Design Question

The next real question is:

can we add one small explicit route layer while preserving the dead-simple
editing model we care about?

I think the answer is probably yes.
But that is the decision point we should examine carefully before doing any
more publication-output work.

## Recommendation Summary

The simplest long-term architecture is probably:

- ordinary pages remain top-level and flat by default
- publication pages become a second explicit page class
- one small shared route model defines source, output, public URL, canonical
  URL, and draft status
- all other build logic derives from that

That would give the repo more rational structure without sacrificing the
clarity that is currently one of its best qualities.
