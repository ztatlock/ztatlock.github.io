# Publication Artifact / WEBFILES Slice 1 Triage

Status: implemented triage checkpoint

It builds on:

- [publication-artifact-webfiles-cleanup-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-artifact-webfiles-cleanup-campaign.md)
- [publication-artifact-followup.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-artifact-followup.md)
- [../policy/publication-artifacts.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/publication-artifacts.md)
- the refreshed local inventory under
  [state/inventory/](/Users/ztatlock/www/ztatlock.github.io/state/inventory/)

## Purpose

Refresh the publication-artifact inventory and partition the current backlog
into:

- immediate required fixes
- easy repo-hosted backfills
- easy `WEBFILES` backup work
- page-link mismatches
- clearly deferred archive-heavy cases

This slice is about establishing a trustworthy working set, not landing the
artifact fixes themselves.

## Baseline

After refreshing the inventory and fixing summary/detail scope mismatches in
[build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py),
the current local baseline is:

- `69` publications total
- `21` local publication detail pages
- `48` indexed publications without local detail pages yet
- `1` required repo artifact gap
- `5` expected repo slide PDFs still missing
- `17` expected repo poster PDFs still missing
- `4` local publication pages without public talk links
- `2` public talk links without `WEBFILES` backup
- `1` `WEBFILES` talk backup without a corresponding page talk link
- `0` manual curation judgments in
  [publication-artifact-curation.tsv](/Users/ztatlock/www/ztatlock.github.io/manifests/publication-artifact-curation.tsv)

## Prioritized Working Set

### 1. Immediate Required Repo-Artifact Fix

There is one current required-artifact gap:

- `2023-plarch-lakeroad`
  - missing repo meta image
  - all other required repo artifacts are already present
  - current local files already include:
    - paper PDF
    - BibTeX
    - abstract markdown
    - abstract image
    - slides PDF

Judgment:

- highest-priority slice-2 target
- likely easy if the missing meta image can be produced quickly from current
  local materials

### 2. Easy Repo Slide-PDF Wins From Current Local Sources

The current inventory shows two local publication pages with missing slide PDFs
but an obvious current repo slide-source file already present:

- `2008-oopsla-dtar`
  - repo slide source: `2008-oopsla-dtar-slides.pptx`
- `2009-pldi-pec`
  - repo slide source: `2009-pldi-pec-slides.pptx`

Judgment:

- best current slice-3 candidates
- likely cheap because the source decks are already in the repo
- no broader archival search appears necessary before trying these

### 3. Easy `WEBFILES` Talk-Backup Wins

The current inventory shows two local publication pages with public talk links
but no `WEBFILES` backup yet:

- `2023-oopsla-enumo`
  - public talk URL: `https://youtu.be/cwMpjtNJba8`
- `2024-asplos-lakeroad`
  - public talk URL: `https://www.youtube.com/watch?v=2XgOWAtJ8vs`

Judgment:

- best current slice-4 candidates
- mailbox-assisted help is reasonable here if another agent already has the
  right download/archive workflow

### 4. Page-Link Mismatch To Review

The current inventory shows one local publication page with a `WEBFILES` talk
backup already present but no public talk link on the page:

- `2023-pldi-egglog`
  - `WEBFILES` backup present:
    `archive/pub-talks/2023-pldi-egglog.mkv`

Judgment:

- worth explicit review during slice 4
- do not assume the page should automatically gain a public talk link
- decide whether the backup corresponds to a public canonical watch URL we
  actually want to surface

## Clearly Deferred Cases

### Slide-PDF Gaps Without Obvious Current Source

These local publication pages still lack slide PDFs, but the current inventory
does not show an obvious repo or `WEBFILES` source candidate:

- `2023-uist-odyssey`
- `2024-asplos-lakeroad`
- `2024-programming-magicmarkup`

Judgment:

- not first-wave easy wins
- defer unless direct local sources appear quickly or a mailbox request turns
  up a concrete lead

### Poster-PDF Gaps

There are currently `17` local publication pages missing poster PDFs.

From the current inventory alone, these do **not** yet separate cleanly into a
small obvious “easy” batch.
Most have:

- no current page poster link
- no explicit current archive candidate in the inventory

Judgment:

- do not start by chasing all poster gaps
- only promote specific poster items into slice 3 if a current local source is
  already known or a mailbox request turns up an immediate win

### Curation Manifest Judgments

The curation manifest is still empty.

Judgment:

- slice 2 should begin adding `not-made`, `lost`, or `unknown` only when we
  already have strong confidence
- do not fabricate judgments from inventory absence alone

## Mailbox-Appropriate Follow-On

Narrow mailbox requests make sense for:

- the two missing `WEBFILES` talk backups
- any specific missing slide/poster item where another agent already knows the
  likely source location
- the `2023-pldi-egglog` talk-link/back-up mismatch if another agent can
  confirm the public watch URL or explain why the backup should remain
  archive-only

Broad “search everything” requests do **not** belong in the next slice.

## Outcome

Slice 1 succeeded if judged as a triage pass:

- the inventory baseline is now internally coherent
- the current easy-win batch is explicit
- the next slices can stay lightweight
- the harder historical/archive-mining work is clearly separated out

## Recommended Next Move

Proceed to slice 2:

- fix the required `2023-plarch-lakeroad` meta-image gap if that is easy
- start adding only high-confidence curation judgments

Do **not** broaden into general poster or historical-website recovery yet.
