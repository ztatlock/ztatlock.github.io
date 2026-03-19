# Publication Artifact Policy

This document defines the intended storage and linking policy for
publication artifacts on `ztatlock.net`.

## Goals

- Keep the public website stable.
- Keep the website self-contained for small, core publication artifacts.
- Keep local archival backups of hard-to-replace artifacts.
- Avoid storing large, unstable, or source-only artifacts in git unless there
  is a strong reason to do so.
- Distinguish clearly between:
  - what the public website should link to
  - what the repo should store
  - what the local archive should preserve

## Canonical Locations

### Repo

The git repo is canonical for small, public publication artifacts that the site
should serve directly.

These normally live under `pubs/<slug>/`.

Canonical repo artifacts:

- paper PDF
- BibTeX
- abstract markdown
- publication preview image (`-absimg`)
- publication social/meta image (`-meta`)
- slides PDF, if slides exist
- poster PDF, if poster exists

### WEBFILES

`~/Desktop/WEBFILES` is canonical for large local archival copies and bulky
working artifacts that should not live in git.

Canonical `WEBFILES` artifacts:

- talk video backups
- teaser video backups
- slide source decks such as `.key` and large `.pptx`
- other large or fragile originals

`WEBFILES` is an archive/preservation store, not the primary link target for
the public website.

## Public Website Linking Rules

### Talks

The website should normally link to the canonical public watch URL for a talk,
usually YouTube.

The corresponding local backup, when it exists, should live in `WEBFILES`.
The local backup is for preservation and recovery, not the default public link
target.

### Slides

The website should prefer a local repo-hosted slide PDF.

If a slide source deck exists and is large, the source deck should normally
live in `WEBFILES`, while the site serves only the slide PDF from the repo.

### Posters

The website should prefer a local repo-hosted poster PDF.

### Publishers / arXiv / code / demos

These are expected to remain external links.

They are not first-party hosted artifacts and do not need local repo copies in
order for the site to be considered self-contained.

## Required vs Expected Artifacts

### Required Repo Artifacts

These should be treated as errors when missing:

- paper PDF
- BibTeX
- abstract markdown
- preview image (`-absimg`)
- meta image (`-meta`)

### Expected Repo Artifacts

These should be treated as warnings when missing, unless later marked
otherwise by manual curation:

- slides PDF
- poster PDF

### Expected Archive Artifacts

These should be treated as warnings when missing if the corresponding public
artifact exists:

- local talk backup in `WEBFILES` when a public talk URL exists
- local source slide deck in `WEBFILES` when a slide deck exists and the
  source is worth preserving

## Inventory Semantics

The inventory should distinguish:

- site-served repo artifacts
- page link targets
- archive backups in `WEBFILES`
- manual curation judgments stored in `manifests/publication-artifact-curation.tsv`

The generated canonical inventory state should live in:

- `~/Desktop/WEBFILES/inventory/publication-artifact-inventory.md`
- `~/Desktop/WEBFILES/inventory/publication-artifact-inventory.tsv`

Repo-local preview outputs may live under:

- `state/inventory/`

The inventory is observational by default. It should not assume that a missing
artifact was never made or is permanently lost.

### Observation Status Values

The generated inventory may use these automatically observed values:

- `present`
- `missing`

### Manual Curation Status Values

Manual curation should use values like:

- `present`
- `not-made`
- `lost`
- `unknown`

`present` is reserved for cases where archive-presence heuristics miss a known
existing archival copy.

We should not use `present` to override a missing canonical repo-served file or
a missing page link.

The key distinction is:

- `missing` is an observed filesystem fact
- `not-made`, `lost`, and `unknown` are human judgments

## Practical Rules Of Thumb

- If the site needs to serve it directly and it is modest in size, it belongs
  in the repo.
- If it is large, fragile, or an authoring/source artifact, it belongs in
  `WEBFILES`.
- Public talk pages should still point to YouTube or the canonical public watch
  page even when a local archival backup exists.
- We should avoid introducing new external first-party links for slides or
  posters when a local repo-hosted copy is feasible.

## Follow-Up Work

- Populate the manual curation manifest over time with `not-made`, `lost`, and
  `unknown` judgments where we have enough confidence.
- Backfill missing repo slide PDFs and poster PDFs from local sources.
- Backfill missing `WEBFILES` talk backups where public talk URLs exist.
- Search older website copies and personal archives for lost artifacts.
