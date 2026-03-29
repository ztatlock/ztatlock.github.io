# ROADMAP

Last updated: 2026-03-29.

This is the working checklist for maintenance and collaboration.
Use this file as the actionable backlog for concrete repo tasks.
Use `TODO.md` and `docs/plans/` for broader strategy and longer-horizon design
notes.

## How To Use This File

- Add new work as unchecked items (`- [ ]`).
- Mark done work as checked (`- [x]`) and keep file references.
- When a source file keeps a `TODO` marker intentionally, track it here too.

## Collaboration Foundation

- [x] Add minimal collaboration guide (`AGENTS.md`).
- [x] Update README with real workflow and structure (`README.md`).
- [x] Document multi-machine pull/push workflow in `AGENTS.md` and `README.md`.
- [x] Add a safe sequential verification target and agent guidance so
  `make test`, `make build`, and `make check` have one obvious non-parallel
  pre-commit path, and keep overlapping git actions out of normal workflow
  (`Makefile`, `AGENTS.md`).

## Near-Term Next Steps

- [ ] Continue the teaching-enrollment campaign with slice 2 and slice 3 now
  that slice 1 has landed: add Spring 2026 `CSE P590` under the
  `uw-cse-507` / CARS family, backfill enrollment for settled historical
  instructor-led UW offerings, and review the homepage recent-teaching diff
  from the newer latest-year window explicitly rather than letting it surface
  by surprise
  (`docs/plans/teaching-enrollment-policy-note.md`,
  `docs/plans/teaching-domain-audit-before-enrollment.md`,
  `docs/plans/teaching-enrollment-implementation-testing-plan.md`,
  `site/data/teaching.json`, `scripts/teaching_record.py`,
  `scripts/sitebuild/page_projection.py`).
- [ ] Review peer CVs from Adam Chlipala, Xavier Leroy, Nate Foster, Emina
  Torlak, Pavel Panchekha, Michael Ernst, and Derek Dreyer for structure
  inspiration and calibration before any broader CV front-matter follow-on
  (`docs/plans/cv-top-summary-executive-block-plan.md`, `site/cv/index.dj`,
  `site/pages/index.dj`).
- [ ] Decide which talks actually need talk-local detail pages instead of
  index-only bundles (`site/talks/`,
  `site/pages/talk-2023-05-egg-uiuc.dj`).
- [ ] Decide whether the authored `Book Chapters` CV subsection should remain
  prose-first or move into a separate publication/bibliography boundary slice
  rather than broadening the current indexed-publication bundle model by
  inertia (`docs/plans/cv-slice-5-publications-projection.md`,
  `site/cv/index.dj`, `site/pubs/`).

## Recent Completed Milestones

- [x] Decide how to represent non-service research/community-participation
  honors such as Dagstuhl attendance on the site and CV so those facts are not
  lost when they are removed from canonical service: keep them in authored/news
  surfaces for now, not in the service domain, and revisit only if enough
  similar facts accumulate to justify a separate structured honors/activities
  domain (`site/cv/index.dj`, `site/data/news.json`,
  `docs/plans/cv-campaign.md`, `docs/plans/structured-content-roadmap.md`).
- [x] Plan and implement the homepage recent-publications projection so the
  repeated recent-publications block on `site/pages/index.dj` derives from
  canonical publication bundles under `site/pubs/` with explicit selection,
  ordering, and low-link policy (`docs/plans/publications-campaign.md`,
  `docs/plans/structured-content-roadmap.md`, `site/pubs/`,
  `site/pages/index.dj`).
- [x] Do a publication-model seam audit and design review pass before large
  further publication backfill so field semantics, compact-consumer needs,
  identifier handling, and publication-boundary questions are improved on the
  canonical bundle model before dozens more bundles need the same migration;
  Proposal A is now the leading authored-schema direction, while still
  allowing richer normalized in-memory publication objects after parse
  (`docs/plans/publication-model-seams-and-requirements.md`,
  `docs/plans/publication-model-audit-notes.md`,
  `docs/plans/publication-model-requirements.md`,
  `docs/plans/publication-model-proposal-a-conservative-refinement.md`,
  `docs/plans/publication-model-corpus-refinement-pass.md`,
  `docs/plans/publications-campaign.md`, `site/pubs/`,
  `scripts/publication_record.py`).
- [x] Plan the publication-model implementation/testing/migration path around
  the now-leading Proposal A direction before large further publication
  backfill, so canonical year, compact venue labels, `pub_type`,
  `local_page`, and identifier handling can land deliberately rather than via
  ad hoc bundle cleanup (`docs/plans/publication-model-proposal-a-conservative-refinement.md`,
  `docs/plans/publication-model-implementation-testing-plan.md`,
  `docs/plans/publications-campaign.md`, `site/pubs/`,
  `scripts/publication_record.py`, `scripts/publication_index.py`,
  `scripts/sitebuild/page_projection.py`).
- [x] Implement slice 1 of the Proposal A publication-model plan as a
  side-by-side loader/validator foundation with focused fixture tests, while
  leaving the live publication corpus and consumers unchanged
  (`scripts/publication_record.py`,
  `tests/test_publication_record.py`,
  `docs/plans/publication-model-implementation-testing-plan.md`).
- [x] Execute slice 2 of the Proposal A publication-model plan by making the
  real corpus migration decisions explicit for indexed publication bundles:
  `pub_year`, cleaned `venue`, `venue_short`, `pub_type`, and `local_page`,
  with the known year-mismatch and `listing_group`/semantic-type divergence
  cases carried forward as named migration checks
  (`docs/plans/publication-model-implementation-testing-plan.md`,
  `docs/plans/publication-model-corpus-refinement-pass.md`,
  `manifests/publication-model-a-migration.tsv`,
  `tests/test_publication_model_a_migration.py`, `site/pubs/`).
- [x] Execute slice 3 of the Proposal A publication-model plan: migrate the
  canonical publication bundles and cut `/pubs/`, the CV indexed-publication
  sections, the homepage recent-publications projection, inventory tooling,
  and validation over to the new Proposal A field contract in one coordinated
  bounded slice, without keeping a long-lived compatibility bridge
  (`docs/plans/publication-model-implementation-testing-plan.md`,
  `manifests/publication-model-a-migration.tsv`,
  `scripts/publication_record.py`, `scripts/publication_index.py`,
  `scripts/sitebuild/page_projection.py`, `scripts/build_pub_inventory.py`,
  `site/pubs/`).
- [x] Execute slice 4 of the Proposal A publication-model plan: do the
  post-cutover cleanup and narrower follow-on enrichment now that the live
  corpus and consumers use Proposal A directly, including retiring remaining
  side-by-side scaffolding if it no longer earns its keep and tightening
  template/scaffold/default authoring paths around the settled schema
  (`docs/plans/publication-model-implementation-testing-plan.md`,
  `docs/plans/publications-campaign.md`, `scripts/publication_record.py`,
  `tests/test_publication_record.py`, `site/templates/publication.json`).
- [x] Plan the top-of-CV executive-summary rethink now that the publication
  slice-4 cleanup has settled the current publication boundary and compact
  rendering semantics, so the remaining authored highlights structure can be
  reconsidered as a broader authored summary layer rather than by inertia
  (`site/cv/index.dj`, `site/pages/index.dj`,
  `docs/plans/cv-campaign.md`,
  `docs/plans/homepage-cv-curated-consumers-campaign.md`,
  `docs/plans/cv-top-summary-executive-block-plan.md`).
- [x] Execute slice 1 of the top-of-CV executive-summary plan by writing down
  the purpose, audience, authorship boundary, maintenance guidance, and
  homepage-relationship policy for the authored top layer before any live CV
  rewrite (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/plans/cv-campaign.md`,
  `docs/plans/homepage-cv-curated-consumers-campaign.md`,
  `docs/policy/cv-top-summary.md`).
- [x] Execute slice 2 of the top-of-CV executive-summary plan: audit
  trustworthy summary inputs and candidate summary statistics across canonical
  domains, then compare them against the authored homepage top summary before
  proposing concrete top-of-CV rewrite shapes
  (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/policy/cv-top-summary.md`,
  `docs/plans/cv-top-summary-slice-2-audit.md`, `site/cv/index.dj`,
  `site/pages/index.dj`, `site/data/news.json`, `site/data/students.json`,
  `site/data/teaching.json`, `site/data/service.json`,
  `site/data/funding.json`, `site/talks/`, `site/pubs/`).
- [x] Execute slice 3 of the top-of-CV executive-summary plan: draft and
  compare a few authored top-of-CV shapes over the now-audited inputs, then
  choose a leading direction before editing the live CV
  (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/plans/cv-top-summary-slice-2-audit.md`,
  `docs/policy/cv-top-summary.md`, `site/cv/index.dj`,
  `site/pages/index.dj`).
- [x] Execute slice 4 of the top-of-CV executive-summary plan: rewrite the
  live top of `site/cv/index.dj` around the now-leading
  narrative-plus-small-stat-row-plus-mixed-signals shape, while keeping the
  result fully authored and reviewing its relationship to the homepage top
  summary explicitly
  (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/plans/cv-top-summary-slice-2-audit.md`,
  `docs/plans/cv-top-summary-slice-3-shape-proposals.md`,
  `docs/policy/cv-top-summary.md`, `site/cv/index.dj`,
  `site/pages/index.dj`).
- [x] Execute slice 5 of the top-of-CV executive-summary plan: reassess the
  authored homepage top summary against the new CV `Overview` block and decide
  whether the homepage prose should stay as-is or be lightly retuned in tone,
  emphasis, or summary framing
  (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/plans/cv-top-summary-slice-2-audit.md`,
  `docs/plans/cv-top-summary-slice-3-shape-proposals.md`,
  `docs/plans/cv-top-summary-slice-4-rewrite.md`,
  `docs/plans/cv-top-summary-slice-5-homepage-reassessment.md`,
  `docs/policy/cv-top-summary.md`, `site/cv/index.dj`,
  `site/pages/index.dj`).

## Migrated Backlog From TODO.md

- [x] Establish the canonical publication-bundle pattern under `site/pubs/` for publication pages that have local records today.
- [x] Implement the slice-1 canonical advising-record model for `site/data/students.json`, including required `person_key`, ordered section/record structure, and typed detail items (`docs/plans/students-slice-1-canonical-model.md`, `site/data/students.json`, `scripts/student_record.py`).
- [x] Implement the students index-wrapper/projection slice: move the public wrapper to `site/students/index.dj`, canonicalize `/students/`, and project the repeated section bodies from `site/data/students.json` while preserving authored framing (`docs/plans/students-slice-2-index-projection.md`, `site/data/students.json`, `site/students/index.dj`).
- [x] Implement the slice-1 canonical teaching-record model for `site/data/teaching.json`, including ordered teaching groups, structured course/summer-school records, and offering/event invariants (`docs/plans/teaching-campaign.md`, `docs/plans/teaching-slice-1-canonical-model.md`, `site/data/teaching.json`, `scripts/teaching_record.py`).
- [x] Plan and implement the public teaching wrapper/projection slice so the public teaching page moves to `site/teaching/index.dj`, canonicalizes `/teaching/`, and projects repeated teaching blocks from `site/data/teaching.json` while keeping the award note and related section hand-authored (`docs/plans/teaching-campaign.md`, `site/data/teaching.json`, `site/teaching/index.dj`).
- [x] Capture the missing Marktoberdorf Summer School 2024 teaching entry during the teaching campaign backfill so the canonical teaching record is more complete than the current public teaching page (`site/data/teaching.json`, `site/pages/index.dj`, `site/news/index.dj`, `site/cv/index.dj`, `docs/plans/teaching-campaign.md`).
- [x] Move the public teaching wrapper to `site/teaching/index.dj`, canonicalize `/teaching/`, project the repeated public teaching blocks from `site/data/teaching.json`, and rewrite lingering `teaching.html` links to `teaching/` (`docs/plans/teaching-slice-2-index-projection.md`, `site/data/teaching.json`, `site/teaching/index.dj`, `site/pages/index.dj`).
- [x] Start the teaching-staffing campaign with the people-linkability/ref-guardrail slice so `site/data/people.json` can represent linkable and linkless people honestly, generated Djot refs exist only for linkable people, and authored/structured Djot source cannot silently depend on linkless generated people refs before later staffing data import begins (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-1-people-linkability.md`, `docs/plans/people-registry-semantics.md`, `site/data/people.json`, `scripts/sitebuild/people_registry.py`, `scripts/sitebuild/people_refs.py`, `scripts/sitebuild/source_validate.py`).
- [x] Normalize the seeded social-profile links in `site/data/people.json` so obvious LinkedIn/GitHub fallback URLs use the new typed `linkedin` / `github` fields before the teaching-staffing schema and staffing backfill slices expand the registry (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-1a-social-link-normalization.md`, `docs/plans/people-registry-semantics.md`, `site/data/people.json`).
- [x] Continue the teaching-staffing campaign with the teaching-staffing schema-foundation slice so instructor-led offerings in `site/data/teaching.json` can later carry ordered `co_instructors` and ordered `teaching_assistants` keyed through `site/data/people.json`, while keeping the current `teaching_assistant` history group separate and leaving public rendering unchanged (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-2-schema-foundation.md`, `docs/plans/teaching-campaign.md`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Continue the teaching-staffing campaign with the co-instructor canonicalization slice so the small confirmed co-instructor set becomes canonical in `site/data/teaching.json`, the one missing co-instructor person record is added to `site/data/people.json`, and any redundant co-teaching prose note is reviewed explicitly before the larger TA import begins (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-3-co-instructor-canonicalization.md`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Continue the teaching-staffing campaign with the teaching-assistant canonicalization slice so confirmed TA facts become canonical on instructor-led offerings in `site/data/teaching.json`, keyed through `site/data/people.json`, while keeping tutor handling and public staffing rendering deferred (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-4-teaching-assistant-canonicalization.md`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Continue the teaching-staffing campaign with the tutor-canonicalization slice so the distinct tutor role exposed by the canonical teaching-staffing facts becomes explicit in `site/data/teaching.json` rather than being silently dropped or folded into `teaching_assistants` (`docs/plans/teaching-staffing-campaign.md`, `docs/plans/teaching-staffing-slice-5-tutor-canonicalization.md`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Plan and implement the public teaching staffing/layout slice so the UW course section on `/teaching/` moves from flowing offering columns to vertical offering lists and can visibly render canonical `co_instructors`, `teaching_assistants`, and `tutors` without changing homepage/CV consumers (`docs/plans/teaching-campaign.md`, `docs/plans/teaching-slice-4-public-page-staffing-layout.md`, `site/teaching/index.dj`, `scripts/sitebuild/page_projection.py`, `site/data/teaching.json`, `site/data/people.json`).
- [x] Plan and implement the special-topics teaching-page follow-on so the `Special Topics Graduate Courses` section also uses a staffing-aware offering layout and stops acting like a staffing-blind exception to the canonical teaching staffing model (`docs/plans/teaching-campaign.md`, `docs/plans/teaching-slice-4a-special-topics-staffing-layout.md`, `site/teaching/index.dj`, `scripts/sitebuild/page_projection.py`, `site/data/teaching.json`, `site/data/people.json`).
- [ ] Plan a later teaching-page styling/polish campaign so the richer, more consistent staffing-aware projections can be made more visually intentional without reopening the canonical teaching data model (`docs/plans/teaching-campaign.md`, `docs/plans/structured-content-roadmap.md`, `scripts/sitebuild/page_projection.py`, `site/static/style.css`).
- [ ] Revisit the unresolved `jack-zhang` normalization seam only if stronger evidence or direct confirmation emerges about whether `Yue Zhang` should be added as an alias, so we do not overfit an uncertain name mapping into `site/data/people.json` prematurely (`site/data/people.json`, `site/data/teaching.json`).
- [x] Plan and implement the slice-1 canonical service model in `site/data/service.json`, using flat per-year service terms with multi-group view membership so the service domain has one shared source of truth without assuming the current hand-authored section headings are the full ontology; defer homepage/CV consumer projection to later cross-cutting cleanup work (`docs/plans/service-campaign.md`, `docs/plans/service-slice-1-canonical-model.md`, `site/data/service.json`).
- [x] Plan and implement the public service wrapper/projection slice so the service page moves to `site/service/index.dj`, canonicalizes `/service/`, and projects repeated public service blocks from `site/data/service.json` while keeping the Aggregators section hand-authored (`docs/plans/service-campaign.md`, `docs/plans/service-slice-2-index-projection.md`, `site/data/service.json`, `site/service/index.dj`, `site/pages/index.dj`).
- [x] Plan and implement the CV route/wrapper cutover slice so the CV moves from `site/pages/cv.dj` to `site/cv/index.dj`, canonicalizes `/cv/`, and rewrites lingering `cv.html` links to `cv/` before any CV section projection begins (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-1-route-cutover.md`, `site/cv/index.dj`, `site/pages/index.dj`, `site/pages/notes.dj`).
- [x] Plan and implement the students CV-projection slice so the duplicated advising sections in `site/cv/index.dj` render from `site/data/students.json` with an intentionally more compressed CV-specific view (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-2-students-projection.md`, `site/data/students.json`, `site/cv/index.dj`).
- [x] Decide the CV visiting-section heading and Ian Briggs policy together during the students CV slice so the rendered heading and inclusion rule stay consistent (`site/students/index.dj`, `site/cv/index.dj`, `docs/plans/cv-campaign.md`, `docs/plans/cv-slice-2-students-projection.md`).
- [x] Reassess the next cross-domain CV consumer slice after the first students-backed checkpoint instead of automatically broadening into teaching, service, talks, or publications (`docs/plans/cv-campaign.md`, `docs/plans/structured-content-roadmap.md`, `site/cv/index.dj`).
- [x] Plan and implement the teaching CV-projection slice so the duplicated teaching section bodies in `site/cv/index.dj` render from `site/data/teaching.json` with an explicit CV-specific teaching view, while preserving the teaching-award note and allowing reviewed format improvements where they help the generated CV (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-3-teaching-projection.md`, `site/data/teaching.json`, `site/cv/index.dj`).
- [x] Plan and implement the service CV-projection slice so the duplicated service subsection bodies in `site/cv/index.dj` render from `site/data/service.json` with an explicit CV-specific service view, while preserving the faculty-skit prose note and reviewing visible service-section changes against rendered HTML (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-4-service-projection.md`, `site/data/service.json`, `site/cv/index.dj`).
- [x] Plan and implement the indexed-publications CV-projection slice so the duplicated `Conference and Journal Papers` and `Workshop Papers` bodies in `site/cv/index.dj` render from canonical publication bundles under `site/pubs/`, while preserving the authored `Book Chapters` subsection and reviewing visible publications-section changes against rendered HTML (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-5-publications-projection.md`, `site/pubs/`, `site/cv/index.dj`).
- [x] Plan and implement the full invited-talks CV-projection slice so the duplicated `## Invited Talks` body in `site/cv/index.dj` renders from canonical talk bundles under `site/talks/`, while preserving the heading and reviewing visible talks-section changes against rendered HTML (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-6-talks-projection.md`, `site/talks/`, `site/cv/index.dj`).
- [ ] Work through the remaining top-of-CV executive-summary slices: audit
  trustworthy summary inputs and candidate stats across canonical domains,
  compare authored shape alternatives, then rewrite the top of the CV before
  reassessing the homepage top summary
  (`docs/plans/cv-top-summary-executive-block-plan.md`,
  `docs/policy/cv-top-summary.md`, `site/cv/index.dj`,
  `site/pages/index.dj`, `docs/plans/cv-campaign.md`).
- [x] Plan and execute the service data audit slice so the repo reviews whether recurring service concepts and year-specific service instances are modeled and grouped correctly before any homepage `Recent Service / Leadership` projection hardens the current service semantics into another consumer (`docs/plans/homepage-cv-curated-consumers-campaign.md`, `docs/plans/homepage-cv-curated-consumers-slice-3-service-audit.md`, `docs/plans/service-campaign.md`, `site/data/service.json`, `scripts/service_index.py`).
- [x] Review the service redesign brief/proposal set and choose a leading long-horizon service model direction before homepage recent-service or richer service-page grouping build further on the current flat term model (`docs/plans/service-redesign-requirements.md`, `docs/plans/service-redesign-proposal.md`, `docs/plans/service-redesign-proposal-a4.md`, `docs/plans/service-campaign.md`).
- [x] Plan and execute the service redesign implementation/testing foundation so the latched A4 `series` / `run` / `instance` model becomes executable in loader/validator code before canonical data migration and before homepage recent-service projection depends on the old flat term model (`docs/plans/service-redesign-proposal-a4.md`, `docs/plans/service-redesign-implementation-testing-plan.md`, `site/data/service.json`, `scripts/service_index.py`, `scripts/service_record_a4.py`, `tests/test_service_record_a4.py`).
- [ ] Plan a later service-page formatting/projection polish slice so `/service/` becomes materially easier to scan now that the canonical service projection is correct but visually rough, especially in the long `Organizing` and `Reviewing` sections (`site/service/index.dj`, `scripts/service_index.py`, `scripts/sitebuild/page_projection.py`, `style.css`).
- [x] Remove `Dagstuhl Seminar 26022: EGRAPHS` from the service domain so homepage recent-service and projected service/CV consumers stop treating it as service by inertia, while preserving the useful public facts through existing news/current homepage surfacing (`site/data/service.json`, `site/data/news.json`, `site/pages/index.dj`, `docs/plans/service-redesign-slice-4-homepage-recent-service.md`).
- [x] Plan and implement the news slice-1 canonical model so the current public news stream is captured as one ordered flat record source in `site/data/news.json` with explicit `kind` and explicit `emoji` before any `/news/` wrapper cutover or homepage consumer change (`docs/plans/news-campaign.md`, `docs/plans/news-slice-1-canonical-model.md`, `site/data/news.json`, `site/pages/index.dj`, `scripts/news_record.py`).
- [x] Plan and implement the news slice-2 public wrapper / route cutover so the public news page moves to `site/news/index.dj`, canonicalizes `/news/`, and projects its repeated month-grouped body from `site/data/news.json` while the homepage remains a separate authored consumer for now (`docs/plans/news-campaign.md`, `docs/plans/news-slice-2-public-wrapper-and-projection.md`, `site/data/news.json`, `site/news/index.dj`, `site/pages/index.dj`, `scripts/news_index.py`).
- [x] Plan and implement the news slice-3 homepage consumer so the homepage `## News` block becomes an explicit curated consumer of canonical `site/data/news.json` records, using a deterministic trailing-`12`-month window with a hard cap of `15` items and optional `homepage_featured` stickiness for older in-window items when the window overflows (`docs/plans/news-campaign.md`, `docs/plans/news-slice-3-homepage-consumer.md`, `site/data/news.json`, `site/news/index.dj`, `site/pages/index.dj`).
- [x] Plan and implement the homepage `Current Students` consumer so the repeated current-students block on `site/pages/index.dj` derives from the canonical `current_students` section in `site/data/students.json` while preserving the section heading, columns wrapper, and trailing students-page sentence (`docs/plans/homepage-cv-curated-consumers-campaign.md`, `docs/plans/homepage-cv-curated-consumers-slice-1-current-students.md`, `site/pages/index.dj`, `site/data/students.json`, `scripts/sitebuild/page_projection.py`, `scripts/sitebuild/source_validate.py`).
- [x] Plan and implement the homepage recent-teaching projection so the repeated recent-teaching bullets on `site/pages/index.dj` derive from `site/data/teaching.json` with explicit recent-window, ordering, and link policy across `uw_courses`, `special_topics`, and `summer_school` while excluding the historical `teaching_assistant` group (`docs/plans/teaching-campaign.md`, `docs/plans/homepage-cv-curated-consumers-slice-2-recent-teaching.md`, `docs/plans/structured-content-roadmap.md`, `site/data/teaching.json`, `site/pages/index.dj`).
- [x] Plan and implement the homepage recent-service / leadership projection so the curated block on `site/pages/index.dj` derives from canonical service runs using the latched current-year trailing-3-year non-`department` policy, no cap for now, direct links for single-URL runs, internal `/service/#<run.key>` links for multi-URL runs, and a retained trailing service-page sentence (`docs/plans/service-campaign.md`, `docs/plans/service-redesign-slice-4-homepage-recent-service.md`, `docs/plans/service-redesign-implementation-testing-plan.md`, `site/data/service.json`, `site/pages/index.dj`).
- [x] Plan and implement the homepage recent-publications projection so the repeated recent-publications block on `site/pages/index.dj` derives from canonical publication bundles under `site/pubs/` using latest-publication-year anchoring, a trailing 3-year window, no cap for now, and a compressed homepage-specific renderer (`docs/plans/publications-campaign.md`, `docs/plans/homepage-cv-curated-consumers-slice-5-recent-publications.md`, `docs/plans/structured-content-roadmap.md`, `site/pubs/`, `site/pages/index.dj`).
- [x] Delete the legacy flat-model service compatibility shim now that canonical service data, `/service/`, the CV, validation, and homepage recent-service all consume the A4 model directly, and make the homepage current-year anchoring rule explicit in code/tests/docs (`scripts/service_record_a4.py`, `scripts/service_index.py`, `scripts/page_source.py`, `scripts/sitebuild/route_discovery.py`, `scripts/sitebuild/source_validate.py`, `tests/test_service_index.py`, `docs/plans/service-redesign-implementation-testing-plan.md`).
- [x] Plan and implement the funding slice-1 canonical model in `site/data/funding.json`, capturing the current funding facts from the CV in a small shared-data record model while explicitly deferring grant-to-paper/project associations (`docs/plans/funding-campaign.md`, `docs/plans/funding-slice-1-canonical-model.md`, `site/data/funding.json`).
- [x] Plan and implement the public funding wrapper/projection slice so a public funding page lands at `site/funding/index.dj` with canonical `/funding/`, projecting repeated funding records from `site/data/funding.json` while keeping page framing hand-authored (`docs/plans/funding-campaign.md`, `docs/plans/funding-slice-2-index-projection.md`, `site/data/funding.json`, `site/funding/index.dj`).
- [x] Plan the CV funding-projection slice so the duplicated funding list in `site/cv/index.dj` will render from canonical `site/data/funding.json` with an explicit CV-specific formatting policy and a rendered HTML diff review focused on the `Funding` section (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-7-funding-projection.md`, `site/data/funding.json`, `site/cv/index.dj`).
- [x] Implement the CV funding-projection slice so the duplicated funding list in `site/cv/index.dj` renders from canonical `site/data/funding.json` with an explicit CV-specific formatting policy and a rendered HTML diff review focused on the `Funding` section (`docs/plans/cv-campaign.md`, `docs/plans/cv-slice-7-funding-projection.md`, `site/data/funding.json`, `site/cv/index.dj`).
- [x] Plan and implement the collaborators wrapper/coauthor-projection slice so the public collaborators page moves to `site/collaborators/index.dj`, canonicalizes `/collaborators/`, and derives its coauthor list from publication bundles plus `site/data/people.json` with explicit familiar-name and unresolved-name policy (`docs/plans/collaborators-campaign.md`, `docs/plans/collaborators-slice-1-wrapper-and-coauthor-projection.md`, `site/collaborators/index.dj`, `site/data/people.json`).
- [x] Plan and implement the about-page collaborator alphabet-stats projection so the collaborator-coverage joke on `site/pages/about.dj` derives from the same projected collaborator display set as `/collaborators/`, without moving the surrounding prose out of authored Djot (`docs/plans/collaborators-campaign.md`, `docs/plans/collaborators-slice-2-alphabet-stats-projection.md`, `site/collaborators/index.dj`, `site/pages/about.dj`).
- [x] Plan and implement the people-registry semantics cleanup so `site/data/people.json` treats `name` as the default site-facing canonical label and `aliases` as resolution-only alternate spellings, normalizes the small alias-bearing set to fit that rule, and removes the collaborators shortest-label heuristic before teaching staffing or richer collaborator modeling build more on the registry (`docs/plans/people-registry-semantics.md`, `site/data/people.json`, `scripts/sitebuild/people_registry.py`, `scripts/collaborators_index.py`).
- [x] Plan and execute the research-collaborator audit slice so the repo explicitly reviews non-coauthor `Research Collaborators`, confirms no hidden historical non-coauthor set was lost during projection, and concludes that the next near-term collaborators expansion can proceed from existing canonical domains without a temporary collaborator-specific registry (`docs/plans/collaborators-campaign.md`, `docs/plans/collaborators-slice-3-research-collaborator-audit.md`, `docs/plans/collaborators-slice-3-research-collaborator-audit-notes.md`, `docs/plans/students-campaign.md`, `site/data/students.json`, `site/data/people.json`).
- [x] Plan and implement the sectioned collaborators-page slice so `/collaborators/` grows from a coauthor list into explicit `Research Collaborators` and flat `Teaching Collaborators` sections over existing canonical sources, while keeping the heading and intro hand-authored and keeping the about-page alphabet joke policy explicit (`docs/plans/collaborators-campaign.md`, `docs/plans/collaborators-slice-4-sectioned-page.md`, `site/collaborators/index.dj`, `site/data/students.json`, `site/data/teaching.json`, `site/pubs/`).
- [ ] Later plan a structured `projects` domain for research work that may not map cleanly to publications, so some collaborator-inclusion facts can eventually move out of residual collaborator-specific data and into a stronger canonical home (`docs/plans/collaborators-campaign.md`, `docs/plans/structured-content-roadmap.md`, `site/data/people.json`, `site/pubs/`).
- [ ] Plan the longer-term funding-enrichment campaign so grant-to-publication/project associations, selection policy, and downstream consumer surfaces across funding, research, and publication views are explicit before new cross-links are added (`docs/plans/funding-campaign.md`, `docs/plans/structured-content-roadmap.md`, `site/data/funding.json`, `site/pages/research.dj`, `site/pubs/`).
- [ ] Later enrich canonical funding records with explicit related publication and project associations only if that cross-domain mapping clearly earns its complexity, so the site can eventually reflect grant outputs across funding, research, and publication views (`docs/plans/funding-campaign.md`, `site/data/funding.json`, `site/pages/research.dj`, `site/pubs/`).
- [ ] Later projection/validation-layer cleanup: load shared student/teaching-style data once per projected page render and review whether tiny per-domain helper splits or a tiny projection registry now earn their keep after the current funding-backed checkpoint (`scripts/sitebuild/page_projection.py`, `scripts/sitebuild/source_validate.py`).
- [ ] Review whether the current centralized explicit route-kind plumbing still earns its keep or whether a small route/renderer registry helper would simplify future wrapper cutovers without obscuring the build (`scripts/sitebuild/route_model.py`, `scripts/sitebuild/route_discovery.py`, `scripts/sitebuild/page_renderer.py`, `scripts/page_metadata.py`).

## Open TODOs In Source Files

### General Site Content

- [ ] Decide what the August 2017 Neutrons news item should link to now that
  the historical project page is gone (`site/data/news.json`).
- [ ] Decide what the stale Neutrons project link on the research page should
  point to until a replacement page exists (`site/pages/research.dj`).
- [ ] Implement or remove `canon` TODO in the union-find demo (`site/static/demo-naive-union-find.html`).
- [ ] Refactor union-find demo state/history for easier "back" behavior (`site/static/demo-naive-union-find.html`).

### Publication Pages

- [ ] Decide whether `2008-oopsla-dtar` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2008-oopsla-dtar/publication.json`).
- [ ] Decide whether `2009-pldi-pec` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2009-pldi-pec/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose a code link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2012-security-quark` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2012-security-quark/publication.json`).
- [ ] Decide whether `2019-conga-sinkingpoint` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2019-conga-sinkingpoint/publication.json`).
- [ ] Decide whether `2021-arith-herbie` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2021-arith-herbie/publication.json`).
- [ ] Decide whether `2021-oopsla-ruler` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2021-oopsla-ruler/publication.json`).
- [ ] Decide whether `2021-sff-3dp` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2021-sff-3dp/publication.json`).
- [ ] Decide whether `2022-ecoop-cakemlfp` should expose a public talk link and, if so, add it to the canonical publication record (`site/pubs/2022-ecoop-cakemlfp/publication.json`).
- [ ] Decide whether `2022-ecoop-cakemlfp` should expose an arXiv link and, if so, add it to the canonical publication record (`site/pubs/2022-ecoop-cakemlfp/publication.json`).
- [ ] Decide whether `2022-tog-carpentry` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2022-tog-carpentry/publication.json`).
- [ ] Decide whether `2023-plarch-lakeroad` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2023-plarch-lakeroad/publication.json`).
- [ ] Decide whether `2023-pldi-egglog` should expose a public talk link and, if so, add it to the canonical publication record (`site/pubs/2023-pldi-egglog/publication.json`).
- [ ] Decide whether `2023-popl-babble` should expose a project link and, if so, add it to the canonical publication record (`site/pubs/2023-popl-babble/publication.json`).
- [ ] Decide whether `2023-popl-babble` should expose a poster link and, if so, add it to the canonical publication record (`site/pubs/2023-popl-babble/publication.json`).

### Template Placeholders (Intentional Scaffolding)

- [ ] Keep or revise placeholder values for new publication scaffolds (`site/templates/publication.json`).
- [ ] Confirm unresolved placeholder policy still matches the authoritative validator (`scripts/validate_build.py`, `scripts/sitebuild/artifact_validate.py`).

## Known Non-TODO Follow-Ups From Review

- [x] Canonicalize authored publication links to `pubs/<slug>/` paths (`site/pages/index.dj`, `site/news/index.dj`, `site/pages/publications.dj`).
- [x] Mirror the publications collection under `site/pubs/index.dj` with canonical `/pubs/`, and update publication detail backlinks accordingly (`site/pubs/index.dj`, `scripts/publication_record.py`, `docs/plans/structured-content-roadmap.md`).
- [ ] Decide whether unresolved scaffold placeholders in draft publication records should remain acceptable until publication (`site/templates/publication.json`, `scripts/validate_build.py`, `scripts/sitebuild/artifact_validate.py`).
