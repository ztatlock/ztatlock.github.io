# Publication Artifact / WEBFILES Incremental Cleanup Campaign

Status: plan latched; slice 1 implemented

It builds on:

- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [publication-artifact-followup.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-artifact-followup.md)
- [../policy/publication-artifacts.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/publication-artifacts.md)
- the current local inventory under
  [state/inventory/](/Users/ztatlock/www/ztatlock.github.io/state/inventory/)
- the shared mailbox protocol at
  `/Users/ztatlock/Dropbox/PRIVATE-AGENTS/mailbox/PROTOCOL.md`

## Purpose

Do a lightweight, incremental cleanup pass over publication artifacts and
`WEBFILES` backups using the current repo, the current local archive, and
other agents when they can help cheaply.

This campaign is intentionally **not** the deep historical recovery pass.

The goal is:

- fix easy current-repo artifact gaps
- backfill easy repo-served slide/poster artifacts when they are already at
  hand
- backfill easy `WEBFILES` talk backups where public talk links already exist
- start using the curation manifest for confident judgments
- stop once the easy wins are exhausted

The later follow-on campaign can mine older website copies and other historical
archives more deeply.

## Why This Campaign Now

The publication model is now stable enough that artifact cleanup is no longer
blocked on schema churn.

The repo also now has:

- clear artifact policy in
  [../policy/publication-artifacts.md](/Users/ztatlock/www/ztatlock.github.io/docs/policy/publication-artifacts.md)
- a working artifact inventory generator in
  [build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)
- a checked-in curation manifest in
  [publication-artifact-curation.tsv](/Users/ztatlock/www/ztatlock.github.io/manifests/publication-artifact-curation.tsv)
- a local preservation/archive home in `~/Desktop/WEBFILES`
- a mailbox system for light coordination with other agents

That makes a bounded cleanup pass realistic and reviewable.

## Scope Guard

This campaign should stay lightweight.

It should:

- prefer easy wins over heroic recovery
- prefer current local sources over broad archival archaeology
- use mailbox coordination when another agent already has the right search
  machinery
- stop and defer the hard cases rather than turning into a sprawling
  excavation

This campaign should **not** initially do:

- a broad search across older website versions
- a large new artifact-hosting policy redesign
- a talks-domain redesign
- a publication-boundary redesign
- a guarantee that every old missing slide or poster will be recovered now

## Current Starting Point

From the current repo-local inventory:

- `69` publications total
- `21` local publication detail pages
- `1` required repo artifact gap
- `5` expected repo slide PDFs still missing
- `17` expected repo poster PDFs still missing
- `2` public talk links without `WEBFILES` backup
- `1` `WEBFILES` talk backup without a corresponding page talk link
- `0` manual curation judgments in
  [publication-artifact-curation.tsv](/Users/ztatlock/www/ztatlock.github.io/manifests/publication-artifact-curation.tsv)

The one current required-artifact gap is:

- `2023-plarch-lakeroad` missing repo meta image

## Main Execution Principle

Treat this as an **inventory-guided easy-wins campaign**, not as a hunt for
complete historical closure.

That means:

- use the inventory to pick a small next batch
- land the cheap clear wins
- record confident curation judgments where no artifact should be expected
- use the mailbox to ask other agents for targeted help when they already
  have the right search context
- rerun inventory after each coherent batch
- stop when the remaining work becomes archival/research-heavy

## Mailbox Coordination

Use the shared mailbox for narrow coordination only.

Good mailbox uses in this campaign:

- asking another agent to look for a specific slide deck, poster, or talk
  backup in a source it already knows well
- reporting that a missing item was found and where it lives
- reporting that a specific artifact now looks confidently `not-made`,
  `lost`, or `unknown`
- asking for help reconciling a page talk link with an existing `WEBFILES`
  backup

Bad mailbox uses:

- putting the artifacts themselves in the mailbox
- using the mailbox as a substitute for repo commits or `WEBFILES` placement
- vague “search everything” requests without a concrete target

## Recommended Slice Order

### Slice 1. Inventory Baseline And Triage

Refresh the current inventory and partition the work into:

- required repo-artifact fixes
- easy repo slide/poster backfills
- easy `WEBFILES` talk-backup backfills
- page-link mismatches
- clearly harder archival cases to defer

Deliverables:

- refreshed local inventory
- a short prioritized working set for the next slices

This slice is now implemented in:

- [publication-artifact-webfiles-slice-1-triage.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-artifact-webfiles-slice-1-triage.md)

### Slice 2. Required Gap And Early Curation Truth

Handle the one required-artifact gap first if it is easy.

At the same time, begin populating
[publication-artifact-curation.tsv](/Users/ztatlock/www/ztatlock.github.io/manifests/publication-artifact-curation.tsv)
with confident `not-made`, `lost`, or `unknown` judgments when those are
already known.

Goal:

- remove the current required-artifact error if feasible
- stop treating the curation manifest as purely empty scaffolding

### Slice 3. Easy Repo Artifact Backfill

Backfill missing repo-hosted slide/poster PDFs only when they are already easy
to obtain from current local sources or quick targeted agent help.

Examples:

- a slide PDF already exists locally and just needs to be copied into
  `site/pubs/<slug>/`
- a poster PDF is already on hand
- a source deck already exists and producing a PDF is cheap and obvious

Do not broaden this slice into a large archival dig.

### Slice 4. Easy `WEBFILES` Talk-Backup Cleanup

Resolve the small current talk-backup mismatches where possible:

- backfill `WEBFILES` talk backups for pages that already have public talk
  links
- review whether the existing `WEBFILES` backup without a page talk link
  should drive a page-link update or remain archive-only for now

This slice is especially appropriate for mailbox-assisted help from agents
that already work in the relevant archive/search domains.

### Slice 5. Reinventory And Stop/Reassess

Rerun the inventory and summarize:

- what easy wins were landed
- what confident curation judgments were added
- what still remains
- which remaining items are now clearly historical-archive work rather than
  current-repo tidying

That summary should explicitly decide whether to:

- stop here, or
- start a separate deeper campaign to mine older historical website copies and
  other archives

## Success Criteria

This campaign is successful if:

- the current required-artifact error is eliminated or explicitly explained by
  a confident curation/deferral decision
- the curation manifest gains real judgments
- some easy repo slide/poster gaps are closed
- some easy `WEBFILES` talk-backup gaps are closed
- the remaining backlog is smaller and more honestly classified

It is **not** a failure if many older artifacts remain missing.
That is acceptable as long as the repo and inventory become more truthful and
the hard cases are clearly separated from the easy ones.

## Follow-On Boundary

The likely follow-on after this campaign is:

- a separate historical website / archive mining campaign

That later campaign can use:

- older website snapshots
- deeper personal archives
- broader agent-assisted archival search

But it should start only after this lighter cleanup pass has removed the cheap
current-source wins.
