# Source, Build, And Deploy Redesign

This note captures a broader architectural reflection on the website after the
publication-local record migration and the route-model audit.

The key conclusion is:

the next meaningful structural step is **not** just publication output
cutover.

If we want:

- route-aware pages
- less root clutter
- clearer single sources of truth
- a more modular layout
- a simpler long-term mental model

then we should treat the next move as a larger explicit redesign of:

- site source layout
- site build layout
- site data layout
- deployment model

That is a major campaign and should be planned accordingly.

## External Research Findings

I reviewed the official documentation for several established static-site
systems and GitHub Pages:

- [Jekyll directory structure](https://jekyllrb.com/docs/structure/)
- [Zola content overview](https://www.getzola.org/documentation/content/overview/)
- [Hugo directory structure](https://gohugo.io/getting-started/directory-structure/)
- [Eleventy](https://www.11ty.dev/)
- [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [What is GitHub Pages?](https://docs.github.com/en/pages/getting-started-with-github-pages/what-is-github-pages)

The common patterns are striking:

### 1. Source And Output Are Usually Separate

This is extremely standard:

- Jekyll builds into `_site`
- Zola builds into `public`
- Hugo builds into `public`
- Eleventy builds into `_site`

So the source/build split is not a weird custom idea.
It is the baseline architecture for mature static-site systems.

### 2. Mature Systems Usually Organize Source By Role, Not Perfect Output Mirror

This is also very consistent:

- Jekyll uses `_layouts`, `_includes`, `_posts`, `_data`
- Zola uses `content`, `static`, `templates`
- Hugo uses `content`, `layouts`, `static`, `data`, `assets`

That means a perfect 1:1 source tree mirroring the public output tree is **not**
the standard pattern.

### 3. Static Files Are The Main Place Where Source And Output Mirror

What *does* usually mirror output is the direct-copy/static area:

- Zola copies `static/` to `public/`
- Hugo copies `static/` to `public/`
- Jekyll copies ordinary non-special files into `_site`

So the strongest argument for source/output mirroring applies to copied public
files, not to templates or generated route-bearing content in general.

### 4. Draft State Usually Lives With The Source Record

Examples:

- Jekyll has `_drafts`
- Zola commonly uses `draft = true`

That supports moving publication draft/public state into the publication-local
record instead of preserving synthetic top-level stubs forever.

### 5. Flexibility And Structure Can Coexist

Eleventy is especially relevant because its philosophy is close to what we
value:

- it separates output cleanly
- it emphasizes control over output
- it explicitly says it works with an existing directory structure rather than
  forcing a single app/pages convention

That suggests we do not need a heavy framework to gain a more explicit build
model.

## Non-Negotiable Design Goals

These are the goals this redesign should optimize for.

### Keep The Site Dead Simple

The current site has real strengths:

- plain text content
- small build surface
- low magic
- easy local inspection

The redesign should preserve those strengths.

### Become Route-Aware

The site should no longer assume every page is:

- top-level source
- top-level output
- top-level URL

That assumption is now a real architectural limitation.

### Separate Authored Source From Built Output

The repo root should stop serving as both:

- the source tree
- the deployed site

That coupling is now one of the main reasons the build model feels strained.

### Keep Djot

Djot still fits the site well.

The current problem is not “we chose Djot.”
The current problem is that the build/deploy model is too tightly coupled to a
flat live-served root.

### Move Toward Cleaner Single Sources Of Truth

We already moved:

- ordinary-page metadata into front matter
- publication-page metadata/body into publication-local records

The next architecture should reinforce that direction, not undo it.

The redesign should also support a few carefully chosen structured data
domains for facts that genuinely appear in many places, for example:

- people / URLs / aliases
- talks
- students
- CV records

But it should **not** turn the whole site into a giant database.

The rule should be:

- canonical shared facts live in structured records
- authored prose lives near prose
- publication-local facts stay local to publication bundles when appropriate

One concrete current example is `templates/REFS`.
An audit during this redesign found that it is already overwhelmingly a
people-link registry, with only a very small non-person remainder.
That made it a strong candidate for splitting into:

- generated people references from `site/data/people.json`
- a tiny hand-maintained remainder for organizations, projects, and similar
  non-person references

That split is now live in the current build and serves as an early proof point
for the broader redesign.

## Current Repo Reality

Today the repo has:

- no `.github/workflows/` Pages workflow
- an explicit non-production preview output directory at `build/`
- top-level generated HTML committed directly in the repo root
- GitHub Pages-style root-serving setup through committed files like
  [CNAME](/Users/ztatlock/www/ztatlock.github.io/CNAME) and
  [robots.txt](/Users/ztatlock/www/ztatlock.github.io/robots.txt)

So the current model is now split in two:

- production path:
  - edit source in the repo root
  - generate outputs into the same repo root
  - commit generated outputs
  - let Pages serve that branch/root layout directly
- preview path:
  - read from the current repo-root source layout
  - build a future-oriented preview site into `build/`
  - validate that preview separately before any later cutover

The production path is still the main thing preventing cleaner structure.
The preview path is the current bridge toward a better source/build split.

## Why Publication Cutover Exposed The Bigger Problem

The publication work exposed that the site lacks a true route model.

Right now the build quietly conflates:

- source path
- output path
- public URL
- canonical URL
- draft/public status
- page discovery

That works in a flat site, but it stops working once a page wants:

- source in one place
- output in another
- URL in a third shape

So the publication question is really a symptom of the broader build model.

## What A Cleaner Architecture Should Look Like

The simplest strong target is:

```text
repo/
  docs/
  scripts/
  manifests/
  state/
  site/
    pages/
    pubs/
    data/
    static/
    templates/
  build/
```

Where:

- `site/` is the single source root for website content and assets
- `build/` is the generated output tree
- repo support material stays outside the site source root

## The Real Layout Design Space

The tension between “mirror the public site tree” and “organize by build role”
is real.

There are three serious options.

### Option A: Source Tree Mirrors Public Routes Closely

Example shape:

```text
site/
  index.dj
  about.dj
  publications.dj
  pubs/
    2024-asplos-lakeroad/
      publication.json
      ...
  img/
  robots.txt
  CNAME
  _templates/
```

#### Strengths

- route-bearing content is very easy to find
- source/output/public relationships are visually obvious
- public URL intuition stays strong

#### Weaknesses

- source-only build inputs still need special underscore-prefixed exceptions
- `site/` root can become noisy again
- copied public files and route-bearing pages get mixed together more heavily

#### Assessment

This is attractive for route clarity, but it risks rebuilding the same flat
structure one level down.

### Option B: Source Tree Organized Purely By Build Role

Example shape:

```text
site/
  pages/
  pubs/
  data/
  static/
  templates/
```

#### Strengths

- very clean separation by responsibility
- easiest implementation model
- simplest build internals

#### Weaknesses

- source path and public route are less visually close
- route-bearing content is split between `pages/` and `pubs/`
- can feel slightly more “compiler-ish” than “site-ish”

#### Assessment

Mechanically strong, but maybe one abstraction layer less direct than we want.

### Option C: Hybrid Route-First For Public Content, Role-First For Non-Public Inputs

Example shape:

```text
site/
  pages/
    index.dj
    about.dj
    publications.dj
  pubs/
    2024-asplos-lakeroad/
      publication.json
      ...
  data/
    people.json
    talks.json
    students.json
  static/
    img/
    CNAME
    robots.txt
    anagram.html
  templates/
```

This is close to Option B, but interpreted more intentionally:

- `pages/` and `pubs/` are the two route-bearing content classes
- `data/` holds shared structured facts
- `static/` is “copy directly to output”
- `templates/` is explicitly non-public

#### Strengths

- keeps build-role boundaries clear
- keeps route-bearing content conceptually central
- makes exceptions principled and few
- aligns with the patterns used by mature static-site systems

#### Weaknesses

- not a perfect source/output mirror
- requires one extra rule:
  public routes are built from `pages/`, `pubs/`, and `static/`, while
  `data/` and `templates/` are support inputs rather than public routes

#### Assessment

This is the best tradeoff.

It is not maximal symmetry, but it gives a cleaner and more teachable model
than either a perfectly mirrored tree or a purely role-first tree.

## Proposed Source Layout

### `site/pages/`

Ordinary Djot pages, for example:

- `site/pages/index.dj`
- `site/pages/about.dj`
- `site/pages/publications.dj`

Draft ordinary pages would live here too.

### `site/pubs/`

Publication-local records and canonical publication assets, for example:

- `site/pubs/2024-asplos-lakeroad/publication.json`
- `site/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.pdf`
- `site/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad.bib`
- `site/pubs/2024-asplos-lakeroad/2024-asplos-lakeroad-abstract.md`

### `site/data/`

Small structured records for facts intentionally reused across multiple pages.

Likely first-cut candidates:

- `site/data/people.json`
  canonical names, URLs, and aliases
- `site/data/talks.json`
  if the talks page becomes data-driven
- `site/data/students.json`
  if the students page becomes data-driven
- `site/data/cv/` or a small set of CV-related JSON files
  if CV sections become generated from structured records

### `site/static/`

Files copied to the built site as-is, for example:

- `CNAME`
- `robots.txt`
- `style.css`
- `zip-longitude.js`
- `img/`
- static standalone HTML pages such as `anagram.html`
- verification files

### `site/templates/`

Site template fragments and global references, for example:

- `HEAD.1`
- `HEAD.2`
- `FOOT`
- `REFS`

This keeps all website-authored source under one clear root.

This is intentionally a hybrid layout:

- route-bearing authored page content lives in `pages/` and `pubs/`
- shared structured facts live in `data/`
- copied public files live in `static/`
- non-public build inputs live in `templates/`

That is slightly less mirrored than a literal public-tree clone, but much
cleaner than forcing templates and build-only files to masquerade as public
paths.

## Proposed Build Layout

Generated site output should go to:

- `build/`

Examples:

- `build/index.html`
- `build/about.html`
- `build/publications.html`
- `build/pubs/2024-asplos-lakeroad/index.html`
- `build/img/...`
- `build/CNAME`
- `build/robots.txt`

This makes the deploy artifact explicit and inspectable without mixing it into
the source tree.

## Route Model

The smallest viable route-aware model should distinguish:

- source inputs
- output path
- public URL
- canonical URL
- draft/public status

It should stay separate from the structured data model.

That is:

- route resolution decides where pages live and how they build
- structured data resolution decides what shared facts pages can render from

It should support exactly two page classes at first:

- ordinary page
- publication page

That is enough to get the structure we want without inventing a full
framework.

## Build Orchestration Options

### Option A: Keep Make As The Main Build Engine

Continue using `Makefile` as the real dependency engine, but make it
route-aware and build into `build/`.

#### Strengths

- preserves the current top-level command style
- leverages existing familiarity

#### Weaknesses

- route-aware page discovery and nested outputs are awkward in make
- the current repo already shows that Make is carrying too much implicit
  filename logic
- the more the site becomes structured, the more fragile the pattern-rule
  approach becomes

#### Assessment

Possible, but probably not the cleanest long-term engineering choice.

### Option B: Replace Make Entirely With Python

Use Python as both the internal build engine and the public command-line
interface.

#### Strengths

- simplest internal implementation model
- easier to express route graphs, validation, copying, and nested outputs
- more portable than Make-specific logic

#### Weaknesses

- loses the nice top-level `make all`, `make check`, `make clean` workflow
- changes more user muscle memory than necessary

#### Assessment

Technically attractive, but it gives up a useful simple interface we still
like.

### Option C: Thin Make Wrapper Over Python Build Orchestration

Keep `Makefile` as the public command surface, but move the actual site graph,
route logic, and build orchestration into Python.

Examples:

- `make build`
- `make check`
- `make clean`
- `make page PAGE=about`
- `make page PAGE=pubs/2024-asplos-lakeroad`

with Python handling:

- structured data loading
- people/alias resolution
- route discovery
- draft/public filtering
- output path computation
- metadata/canonical URL computation
- sitemap generation
- copy/build decisions

#### Strengths

- preserves the simple Make interface
- removes the flaky/awkward part of using Make as a route-aware build engine
- gives us a clean place to express page classes and routes
- likely easiest to test and maintain

#### Weaknesses

- one more layer than pure Python-only
- requires redefining some current command patterns

#### Assessment

This is the best fit for the goals.

It keeps the human-facing simplicity of Make while moving the real complexity
into a saner implementation language.

## Engineering Commitments

This redesign should explicitly commit to the following implementation style:

- pure Python modules with narrow responsibilities
- explicit schemas and invariants
- small unit tests for route and data resolution
- thin Make commands on top

These are not optional niceties.
They are part of the intended architecture.

### What That Means Concretely

#### Pure Python Modules With Narrow Responsibilities

Examples of the module split we should aim for:

- route discovery / route model
- source loading
- structured data loading
- people/alias resolution
- page rendering
- sitemap generation
- validation

Each module should do one thing clearly.

#### Explicit Schemas And Invariants

Structured records should have documented invariants and validation.

Examples:

- people records must have a stable key
- alias mappings must be unambiguous
- publication records must satisfy their canonical asset contract
- every route must have one output path and one canonical URL

#### Small Unit Tests For Route/Data Resolution

The key logic should be testable without running the whole site build.

That means focused tests for things like:

- ordinary route resolution
- publication route resolution
- canonical URL computation
- draft filtering
- people alias resolution
- structured-data validation failures

#### Thin Make Commands On Top

Make should remain the public command surface, not the place where the real
site graph logic lives.

That means commands like:

- `make build`
- `make check`
- `make clean`

should mostly delegate to focused Python entry points.

## Deployment Model

The redesign should stop depending on “commit generated HTML to the source
branch root.”

The recommended target is:

- build the site into `build/`
- deploy `build/` through a GitHub Pages Actions workflow

This aligns with GitHub’s current custom Pages workflow model, where a build
job uploads a Pages artifact and a deploy job publishes it. Official docs:

- [Using custom workflows with GitHub Pages](https://docs.github.com/en/pages/getting-started-with-github-pages/using-custom-workflows-with-github-pages)
- [What is GitHub Pages?](https://docs.github.com/pages/getting-started-with-github-pages/about-github-pages)

This gives us:

- explicit deploy artifact
- no need to keep generated output committed in source
- cleaner separation between editing and publishing

## Why This Is Better Than More Incremental Routing Hacks

Because the path problem is not an isolated publication quirk.

If we want a structured site, then the clean thing is to make the site model
structured at the same time:

- source tree
- build output tree
- route model
- deploy model

Trying to force only publication pages through a more structured path while the
rest of the system still assumes root-level served outputs would create
unnecessary transitional complexity.

## Why I Do Not Recommend A Perfect 1:1 Source/Build Mirror

Because some source files are not public routes:

- templates
- shared references
- build-only configuration
- validation/build orchestration inputs

If we force the source tree to mirror the public output tree too literally,
those files either:

- get hidden behind ad hoc underscore-prefixed exceptions, or
- pollute the route-bearing source tree

The cleaner design is to make the route-bearing parts explicit and keep the
non-route-bearing parts separate.

That is still simple.
It is just honest about the fact that not all source files are public pages.

## Recommended Campaign Shape

This should be treated as a major redesign campaign with explicit phases.

### Phase 1: Freeze The Target Architecture

Decide and document:

- source root name
  recommendation: `site/`
- output root name
  recommendation: `build/`
- build orchestration model
  recommendation: thin Make wrapper over Python
- route model shape
- ordinary vs publication page class rules
- deploy model
  recommendation: GitHub Pages Actions artifact deployment

### Phase 2: Build The New Route-Aware Build Engine

Start with a future-oriented preview slice:

- explicit route model
- deterministic route discovery from the current source tree
- real preview builds into `build/`
- route invariants and preview-build validation

Use the intended future output layout immediately, especially for publication
pages.

Later in this phase, implement in Python:

- page discovery
- route computation
- ordinary-page build
- publication-page build
- metadata rendering
- sitemap generation
- static-file copying
- validation against the new layout

At this phase, local preview builds should target `build/`, while the current
root-level build remains the production path temporarily.

The immediate next cleanup inside this phase should be:

- one shared render core for:
  - route-aware metadata rendering
  - page HTML document assembly
- route-driven sitemap generation for `build/`

That is the first point where the new engine starts replacing duplicated legacy
logic instead of merely previewing future routes.

### Phase 3: Finalize The New Engine's Source Model

Before moving real files, remove the biggest remaining mismatch between the new
engine and the intended steady state:

- publication discovery should come from `site/pubs/*/publication.json`
- publication draft/public status should become publication-local
- the new engine should stop depending on top-level `pub-*.dj` stubs
- backward compatibility for old `pub-*.html` URLs should remain a non-goal

This phase should strengthen the new engine directly, not evolve the legacy
root-served build.

### Phase 4: Migrate Source Into `site/`

Move:

- top-level Djot pages into `site/pages/`
- `pubs/` into `site/pubs/`
- static site assets/config into `site/static/`
- templates into `site/templates/`

Keep repo support material at root:

- `docs/`
- `scripts/`
- `manifests/`
- `state/`
- `Makefile`
- `README.md`

This source move should happen only after the preview builder is trusted
enough that the source migration is mostly mechanical rather than
architecturally exploratory.

### Phase 5: Add GitHub Pages Workflow

Add:

- `.github/workflows/pages.yml`

to:

- build the site into `build/`
- upload the build artifact
- deploy it through GitHub Pages

At that point, generated site output should no longer need to be committed.

### Phase 6: Remove Old Root-Level Generated Site Outputs

Delete the old committed generated outputs once the workflow is trusted:

- generated top-level `*.html`
- `sitemap.txt`
- `sitemap.xml`

Those should become build artifacts, not tracked source files.

### Phase 7: Clean Up Transitional Assumptions

Remove:

- publication stubs
- root-level publication outputs
- root-layout policy assumptions that only existed for the live-served root

## Practical Recommendation

The best next implementation direction is:

- keep Make as the public command interface
- move build orchestration into Python
- introduce `site/` and `build/`
- deploy `build/` through GitHub Pages Actions

In the near term, the clean next slice is:

- freeze the legacy build as a temporary oracle only
- simplify the new engine's publication model
- then decide whether static-source cleanup should happen separately or as part
  of the real source move

That is the cleanest way to preserve simplicity while making the repo more
rational, modular, and route-aware.

## Recommendation Summary

If we are going to do this, we should do it as a larger explicit model change:

- one source root
- one build root
- one small route-aware build engine
- one explicit deploy workflow

That is a major redesign, but it is also the shape that most directly serves
the long-term goals we have been converging toward.
