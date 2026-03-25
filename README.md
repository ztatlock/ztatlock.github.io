# ztatlock.net

Repo for [Zachary Tatlock's website](https://ztatlock.net), built from Djot
source with a small Python build engine behind `make`.

## Repo Layout

- `site/pages/`
  Authored Djot pages.
- `site/talks/<slug>/`
  Talk-local records for invited/public talks, with room for optional future
  talk-local prose or assets.
- `site/talks/index.dj`
  Authored talks collection index wrapper rendered at `/talks/`.
- `site/students/index.dj`
  Authored students landing-page wrapper rendered at `/students/`.
- `site/teaching/index.dj`
  Authored teaching landing-page wrapper rendered at `/teaching/`.
- `site/service/index.dj`
  Authored service landing-page wrapper rendered at `/service/`.
- `site/cv/index.dj`
  Authored CV consumer wrapper rendered at `/cv/`.
- `site/data/service.json`
  Canonical service-term records for the service page plus later homepage and
  CV reuse.
- `site/data/teaching.json`
  Canonical teaching/course records for the teaching page plus later homepage
  and CV reuse.
- `site/pubs/<slug>/`
  Publication records and local publication assets.
- `site/static/`
  Copied public static/config files, shared `img/`, and standalone authored
  static HTML pages.
- `site/templates/`
  Shared page wrappers and the tiny non-person `REFS` remainder.
- `site/data/people.json`
  Canonical people-link registry.
- `build/`
  Generated site artifact.
- `scripts/`
  Executable helpers and small reusable Python build modules.
- `tests/`
  Focused unit tests for route/data/build modules.
- `docs/`
  Human-authored policy/spec docs.
- `manifests/`
  Small versioned structured manifests.
- `state/`
  Local generated/runtime state.

Metadata rules:
- Public non-publication pages source metadata from YAML front matter in
  `site/pages/*.dj`.
- The talks index is projected from talk-local records under
  `site/talks/<slug>/talk.json` into `site/talks/index.dj`.
- The students landing page is projected from canonical advising records in
  `site/data/students.json` into `site/students/index.dj`.
- The teaching landing page is projected from canonical course records in
  `site/data/teaching.json` into `site/teaching/index.dj`, and later homepage
  and CV teaching facts should reuse the same records.
- The public service page is projected from canonical service-term records in
  `site/data/service.json` into `site/service/index.dj`, and later homepage
  and CV service facts should reuse the same records.
- Public publication pages source metadata from
  `site/pubs/<slug>/publication.json`.
- Draft pages may omit metadata while they remain drafts.

## Build and Validation

Prerequisites: `bash`, `make`, `python3`, `git`, `djot`, `rg`.
`wget` is only needed for `make index-now`.

Commands:
- `make build`
  Build the authoritative site into `build/`.
- `make check`
  Validate source invariants plus the built site under `build/`.
- `make routes`
  Render the authoritative route table to `state/routes.json`.
- `make test`
  Auto-discover and run focused unit tests under `tests/`.
- `make inventory`
  Build publication artifact inventory locally under `state/inventory/`.
- `make mkpub YCF=YEAR-CONF-SYS`
  Scaffold a new publication-local record.
- `make env-check`
  Verify local prerequisites and portability assumptions.
- `make index-now`
  Ping IndexNow after publishing.
- `make clean`
  Remove generated local build artifacts.

Optional personal-maintenance helper:
- `make inventory-webfiles`
  Refresh the local archive copy under `~/Desktop/WEBFILES/inventory/`.

## Editing Workflow

Multi-machine guardrail:
- At the start of a session, run `git status`, and if the tree is clean run
  `git pull --ff-only` before making changes.
- If the tree is dirty, stop and resolve that state before pulling.
- After each coherent commit, `git push` so other machines stay in sync.

Normal workflow:
1. Edit source under `site/`.
2. Update or add metadata in page front matter, shared data like
   `site/data/students.json`, `site/data/teaching.json`, or
   `site/data/service.json`, talk records under `site/talks/<slug>/talk.json`,
   or publication records under `site/pubs/<slug>/publication.json`.
3. Run `make build`.
4. Run `make check`.
5. Commit once the authoritative checks pass.

Notes:
- The repo root is a workspace, not the live served site.
- Do not hand-edit generated files under `build/`.
- Authored publication page links in Djot should use `pubs/<slug>/`, not
  `pub-<slug>.html`.
- Authored publications collection links in Djot should use `pubs/`, not
  `publications.html`.
- Authored talks index links in Djot should use `talks/`, not `talks.html`.
- Authored students index links in Djot should use `students/`, not
  `students.html`.
- Authored teaching index links in Djot should use `teaching/`, not
  `teaching.html`.
- Authored service index links in Djot should use `service/`, not
  `service.html`.
- Authored CV links in Djot should use `cv/`, not `cv.html`.
- Add or update person references in `site/data/people.json` when using
  `[Name][]` links.
  Keep `site/templates/REFS` only for non-person references such as `PGAS`
  or `UW`.

## Publication Bootstrap

Use:

```bash
make mkpub YCF=YEAR-CONF-SYS
```

This creates:
- `site/pubs/YEAR-CONF-SYS/publication.json`
- `site/pubs/YEAR-CONF-SYS/YEAR-CONF-SYS-abstract.md`
- `site/pubs/YEAR-CONF-SYS/YEAR-CONF-SYS.bib`

The scaffolded publication record starts with `"draft": true`.
Fill in placeholders, add canonical assets under `site/pubs/YEAR-CONF-SYS/`,
and remove `"draft": true` when the page is ready to publish.

Publication storage/linking policy is documented in
[docs/policy/publication-artifacts.md](docs/policy/publication-artifacts.md).

## Publishing

GitHub Pages deploys the generated `build/` artifact through
[.github/workflows/pages.yml](.github/workflows/pages.yml).
The repo Pages settings control the active custom domain.
`site/static/CNAME` is still copied into the generated artifact from
`site/static/`.

## Roadmap

- Use [ROADMAP.md](ROADMAP.md) for actionable backlog items.
- Use [TODO.md](TODO.md) and [docs/plans/](docs/plans/) for broader strategy
  and longer-horizon design work.
