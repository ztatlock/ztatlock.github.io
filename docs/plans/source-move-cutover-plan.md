# Source Move Cutover Plan

Status: Implemented

This note defines the coordinated campaign that moved authored site source into
`site/` and made the route-aware build authoritative.

This is the first redesign phase that is intentionally large.
It should still land as a sequence of small, reviewable commits with explicit
stop-and-check points, but it should be treated as one short coordinated
campaign rather than a loose collection of unrelated follow-ups.

## Why This Phase Exists

The preview engine is now ready enough that the remaining work is no longer
about route-model exploration.
The remaining work is cutover.

The important audit result was:

- a pure source move was **not** enough
- the repo was still published from tracked root-level generated outputs
- so the source move, command-surface cutover, and deployment cutover had to be
  treated as one coordinated campaign

If we move source into `site/` without also cutting over the command surface and
Pages deployment shortly afterward, the repo will sit in an awkward half-state:

- the new engine will be authoritative in design
- but the old root-level outputs will still define what is actually published

That is exactly the split-brain state this plan is meant to avoid.

## Audited Current Inventory

Moved authored source:

- `27` ordinary top-level Djot pages:
  - `404.dj`
  - `about.dj`
  - `anxiety-carts-horses.dj`
  - `basic-advice.dj`
  - `build-simple-first.dj`
  - `calendar-theory.dj`
  - `collaborators.dj`
  - `contact.dj`
  - `course-recipe.dj`
  - `cv.dj`
  - `games.dj`
  - `index.dj`
  - `news.dj`
  - `notes.dj`
  - `paper-recipe.dj`
  - `proverbs-poems.dj`
  - `publications.dj`
  - `research.dj`
  - `response-recipe.dj`
  - `s-expressions.dj`
  - `service.dj`
  - `students.dj`
  - `talk-2023-05-egg-uiuc.dj`
  - `talk-recipe.dj`
  - `talks.dj`
  - `teaching.dj`
  - `why-skepticism.dj`
- `21` publication bundles moved from `pubs/` to `site/pubs/`
- `21` top-level `pub-*.dj` temporary legacy stubs deleted in this campaign
- root-level authored static/config files moved to `site/static/`:
  - `CNAME`
  - `robots.txt`
  - `style.css`
  - `zip-longitude.js`
  - `9ca38421ba63499eaa1e9c16bfe7be4c.txt`
- `3` authored standalone static HTML pages:
  - `anagram.html`
  - `demo-naive-union-find.html`
  - `sundial.html`
- root `img/` shared assets moved to `site/static/img/`
- root `templates/` moved to `site/templates/`

Source that was already in the intended area:

- `site/data/people.json`

Current deployment reality after the cutover:

- `.github/workflows/pages.yml` builds and deploys `build/`
- generated top-level root outputs are gone
- `README.md` and `AGENTS.md` now center `make build` / `make check` /
  `make routes`

## Final Invariants For This Campaign

At the end of the source-move campaign, these should all be true:

1. All authored site source lives under `site/`:
   - `site/pages/`
   - `site/pubs/`
   - `site/static/`
   - `site/templates/`
   - `site/data/`
2. `build/` is the only generated site artifact.
3. `make build` and `make check` are the authoritative build/check commands.
4. The authoritative build/check path does not depend on publication stubs.
5. The authoritative build/check path does not depend on repo-root static-route
   bridge logic.
6. The authoritative build/check path does not reverse-rewrite canonical
   publication links back to `pub-*.html`.
7. Top-level `pub-*.dj` stubs are gone.
8. Top-level generated `*.html`, `sitemap.txt`, and `sitemap.xml` are gone.
9. GitHub Pages deploys `build/` through a custom Actions workflow.
10. Old publication URLs do not need compatibility redirects.

These are the invariants that make the migration actually complete instead of
only moved-around.

## Recommended Final Command Surface

The post-cutover Make interface should be intentionally small:

- `make build`
  build the authoritative site into `build/`
- `make check`
  validate authoritative source + authoritative built artifacts
- `make test`
  focused Python unit tests
- `make inventory`
  publication artifact inventory
- `make routes`
  render the route table for inspection
- `make clean`
  remove generated local artifacts

Deliberately **not** part of this campaign unless absolutely necessary:

- preserving `make <page>.html` as the architectural center
- preserving `make all` as the main build command
- preserving a second legacy check path as a peer to `make check`

If a per-page build command still feels necessary after the cutover, it should
come back later as an explicit final-model command such as `make page
PAGE=about`, not as continued dependence on root `%.html` targets.

## Campaign Structure

This campaign should be executed as one coordinated effort with stop points.

Recommended sequence:

### Step 1: Cut Over The Command Surface First

Before moving files, flip the human-facing commands to the final shape.

Target changes:

- make `make build` call the current authoritative Python build into `build/`
- make `make check` call the current authoritative validation path for `build/`
- make `make routes` render the route table
- keep temporary legacy commands only if needed for the duration of the branch,
  and name them explicitly as legacy commands

This gives the move a stable interface before any file motion.

Stop and reflect:

- Is the new command surface small and obvious?
- Are contributors being taught the future commands now rather than later?

Required checks at this stop point:

- `make build`
- `make check`
- `make test`
- `make inventory`

### Step 2: Move Real Source Into `site/` And Flip Config Defaults

Move the authored source tree into the final layout:

- top-level ordinary `*.dj` pages -> `site/pages/`
- `pubs/` -> `site/pubs/`
- root static/config files -> `site/static/`
- root standalone static `*.html` -> `site/static/`
- root `img/` -> `site/static/img/`
- `templates/` -> `site/templates/`

Then flip `SiteConfig` defaults to the new roots:

- `page_source_dir = site/pages`
- `publications_dir = site/pubs`
- `templates_dir = site/templates`
- `static_source_dir = site/static`

`site/data/` should stay where it is.

This step should also update any remaining helpers whose defaults still point
at the old root layout.

Stop and reflect:

- Did the move stay mostly mechanical?
- Did any unexpected path truth remain outside `SiteConfig`?

Required checks at this stop point:

- `make build`
- `make check`
- `make test`
- `make inventory`

Additional targeted audit:

- no intended source file still lives at the repo root
- `build/` contains the expected copied static files, pages, publication pages,
  `404.html`, `sitemap.txt`, and `sitemap.xml`

### Step 3: Delete Bridge-Only Code In The Same Campaign

Once the moved source layout is working, delete the code that only existed to
bridge the old root layout:

- top-level `pub-*.dj` stubs
- gated publication-stub bridge validation
- root-only reverse-rewrite of canonical publication links
- repo-root static-route bridge behavior
- legacy-stub scaffolding defaults and options
- legacy root build/check wrappers that no longer serve a purpose

This is not optional cleanup debt.
If these branches survive too long, they become a second architecture again.

Stop and reflect:

- Is the new engine now simpler than before the move?
- Did we actually delete bridge code, or only stop using it?

Required checks at this stop point:

- `make build`
- `make check`
- `make test`
- `make inventory`
- `rg 'pub-.*\\.dj|validate_publication_bridge_metadata|publication-stub bridge|legacy publication-link reverse-rewrite'`
  should only find intentional historical/doc mentions

### Step 4: Add GitHub Pages Workflow And Switch Deployment Over To `build/`

Add a custom GitHub Pages workflow so the repo no longer depends on tracked
root outputs for deployment.

Current official GitHub docs indicate the custom-workflow path should use:

- `actions/configure-pages@v5`
- `actions/upload-pages-artifact@v4`
- `actions/deploy-pages@v4`

Recommended workflow shape:

- trigger on `push` to `main` and `workflow_dispatch`
- build job:
  - checkout
  - configure Pages
  - install prerequisites
  - run `make build`
  - upload `build/` as the Pages artifact
- deploy job:
  - `pages: write`
  - `id-token: write`
  - deploy uploaded artifact

Out-of-band repository settings to verify during this step:

- GitHub Pages publishing source is set to GitHub Actions
- the custom domain remains configured for `ztatlock.net`
- `CNAME` is present in `build/` via `site/static/CNAME`

Stop and reflect:

- Is deployment now explicit and reproducible from `build/`?
- Does anything still require committed root HTML for publication?

### Step 5: Remove Tracked Root Outputs And Flip The Docs

Once the workflow is in place, delete the legacy published artifacts from the
repo root:

- generated top-level `*.html`
- `sitemap.txt`
- `sitemap.xml`

Then update the human-facing docs and policies:

- `README.md`
- `AGENTS.md`
- `docs/policy/root-layout.md`
- any build/check instructions that still describe the root build as normal

This is the final visible step that makes the repo look like the new
architecture instead of the old one.

## Tests And Checks We Explicitly Want

These are the high-value checks for the campaign.

### Build/Check Surface

- `make build` succeeds from the moved source tree
- `make check` succeeds from the moved source tree
- `make test` remains green
- `make inventory` remains green

### Source Layout

- `load_site_config()` defaults point at `site/pages`, `site/pubs`,
  `site/templates`, and `site/static`
- the moved real repo builds correctly without passing custom config overrides
- new publication scaffolding defaults to bundle-only creation with no stub

### Bridge Removal

- no top-level authored `*.dj` remain except repo-support edge cases that are
  intentionally not site source
- no top-level `pub-*.dj` remain
- no authoritative path rewrites canonical publication links back to legacy
  `pub-*.html`
- no authoritative validator depends on publication stubs

### Deployment

- `build/` contains `CNAME`
- `build/404.html` exists
- `build/sitemap.txt` and `build/sitemap.xml` exist
- workflow YAML matches current GitHub Pages custom-workflow requirements

## Things That Should Make Us Pause

Stop and ask for a deliberate design check if any of these happen:

- the move starts requiring duplicate source trees
- the move starts requiring compatibility redirect pages
- the move starts requiring the legacy root build to remain a peer to the new
  build
- the move starts inventing a second permanent command surface
- the move starts preserving bridge-only code because deletion feels scary

Those are signs we are drifting away from the simplicity goal.

## Recommendation

Treat the source move as a short coordinated cutover campaign with several
small commits, not as a long transition where the old and new architectures
coexist indefinitely.

The cleanest shape is:

1. flip the command surface
2. move real source into `site/`
3. delete bridge code
4. switch GitHub Pages to deploy `build/`
5. delete root outputs and update docs

That is the simplest path that keeps the migration reviewable without carrying
the legacy architecture forward.
