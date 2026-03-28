# Publication Model Lessons From Xavier Leroy's Bibliography

Status: external-inspiration note

Relevant external sources:

- [Xavier Leroy bibliography source](https://xavierleroy.org/bibrefs/leroy_bib.html)
- [Xavier Leroy publications by year](https://xavierleroy.org/publi-by-year.html)
- [Xavier Leroy publications by topic](https://xavierleroy.org/publi-by-topic.html)
- [Xavier Leroy publications by kind](https://xavierleroy.org/publi-by-kind.html)

## Why This Note Exists

Before going further on publication-model proposals, it is worth extracting
the useful lessons from Xavier Leroy's publication system without copying its
much heavier BibTeX-centric pipeline.

The point is not to emulate the whole system.
The point is to learn which semantic distinctions are clearly real in a mature
publication corpus.

## What Xavier's System Tracks

His bibliography tracks much richer metadata than the current site uses,
including:

- core bibliographic kind via BibTeX entry type
- usual bibliographic fields such as title, authors/editors, journal or
  booktitle, publisher, series, volume, number, pages, year, and month
- explicit identifiers such as DOI, HAL, and ISBN
- multiple destinations such as local PDF, publisher page, arXiv, and HAL
- abstract text
- custom semantic fields such as:
  - `xtopic`
  - `xranking`
  - `popularscience`

It also projects one canonical corpus into multiple public views:

- reverse chronological
- grouped by topic
- grouped by kind

## Main Lessons That Seem Useful For This Repo

### 1. Publication Metadata Really Has Multiple Semantic Axes

His corpus cleanly distinguishes more than one kind of semantic classification:

- bibliographic kind
- research topic
- rough prominence/ranking

This strongly reinforces a lesson already visible in the current repo:

- `listing_group` is not the only meaningful classification axis

That does **not** mean this repo needs a large taxonomy immediately.
It does mean a good publication design should leave room for more than one
semantic axis over time.

### 2. Identifiers And Landing URLs Are Different Facts

His entries often include both:

- an explicit DOI or other identifier
- a publisher or archive landing URL

This strongly supports the current requirements stance that:

- DOI should not just remain hidden inside `links.publisher`
- identifiers and landing pages are different kinds of fact

### 3. Broader Publication Kinds Are Real, Not Hypothetical

His grouped-by-kind view includes at least:

- books
- journal articles
- book chapters
- conference papers
- workshop papers
- technical reports
- edited proceedings
- miscellaneous items

That does not force this repo to bring `Books` or `Book Chapters` into the
indexed publication model immediately.
It does reinforce that the boundary should stay explicit and revisitable.

### 4. One Canonical Corpus Can Support Multiple Honest Projections

His system is a strong example of one source corpus supporting:

- by-year views
- by-topic views
- by-kind views

This is a useful confirmation for this repo's direction.
The publication model should support multiple projections cleanly without
requiring separate consumer-specific publication data stores.

## What Does *Not* Transfer Cleanly

### 1. The Full BibTeX-Centric Pipeline

His system appears to lean heavily on rich BibTeX metadata and projection
logic.

This repo has already decided that it does **not** want:

- a giant BibTeX parse/write/normalize pipeline
- full bibliography-tooling complexity just to maintain site metadata

So the right lesson is:

- preserve useful semantic distinctions

not:

- copy the whole toolchain

### 2. Rich Topic / Ranking Metadata As An Immediate Requirement

Fields such as `xtopic` and `xranking` are useful evidence that topic and
prominence can matter.

But the current repo does not yet have enough concrete consumers to require:

- a full topic taxonomy
- ranking fields
- popularity/prominence metadata

Those remain future pressures, not immediate requirements.

## Current Recommendation

The Xavier review should influence proposal work in three main ways:

1. Keep identifiers explicit and distinct from landing-page links.
2. Treat publication type / kind as a real future semantic axis, not just a
   page-grouping accident.
3. Keep the design open to broader publication boundaries and future multiple
   projections without copying a heavyweight BibTeX pipeline.

That is enough to sharpen the current proposal comparison without redirecting
the publication campaign into a much larger system than this repo wants.
