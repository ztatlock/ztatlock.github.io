# Current Root Layout

This document records the current post-cutover root-level layout.
The repo root is now a workspace and orchestration surface, not the live site.

## Goals

- Make the repo root navigable and interpretable.
- Keep authored site source under `site/`.
- Keep generated site output under `build/`.
- Make it clear which files should not land at the top level anymore.

## Top-Level Directories

- `build/`
  Gitignored generated site artifact.
- `docs/`
  Human-authored policy, specs, and campaign notes.
- `manifests/`
  Small versioned structured manifests.
- `scripts/`
  Executable maintenance helpers.
- `site/`
  Authored site source:
  pages, publication bundles, static files, templates, and shared data.
- `state/`
  Local generated/runtime state and repo-local previews.
- `tests/`
  Focused unit tests for the route/data/build modules.

## Top-Level File Classes

Top-level files should now be support/orchestration material only.

Current examples include:

- repo support files such as `Makefile`, `README.md`, `AGENTS.md`, and
  `TODO.md`
- git and GitHub configuration such as `.gitignore` and `.github/workflows/`
- no authored site pages, publication bundles, or copied site static assets

## Root-Level Rules

- New human-authored support material should normally go under `docs/`,
  `scripts/`, `manifests/`, or `state/`, not at the repo root.
- New generated previews, reports, and runtime state should go under `state/`,
  not at the repo root.
- Generated site output should go under `build/`, not at the repo root.
- Authored site pages should go under `site/pages/`.
- Publication bundles should go under `site/pubs/`.
- Copied public static/config files should go under `site/static/`.
- Shared templates and refs should go under `site/templates/`.
- Shared structured site data should go under `site/data/`.

## Long-Term Direction

This root layout is now the intended architecture, not a temporary bridge.
Future structural work should preserve the same basic split:

- authored source under `site/`
- generated site under `build/`
- orchestration and support material at the repo root
