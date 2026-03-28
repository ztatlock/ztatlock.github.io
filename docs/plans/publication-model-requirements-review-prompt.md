# Publication Model Requirements Review Prompt

Please do a careful, skeptical review of the publication-model requirements in
this repo.

Primary document to review:

- [publication-model-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-requirements.md)

Supporting context:

- [publication-model-seams-and-requirements.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-seams-and-requirements.md)
- [publication-model-audit-notes.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publication-model-audit-notes.md)
- [publications-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/publications-campaign.md)
- [cv-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/cv-campaign.md)
- [homepage-cv-curated-consumers-slice-5-recent-publications.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/homepage-cv-curated-consumers-slice-5-recent-publications.md)
- [talks-campaign.md](/Users/ztatlock/www/ztatlock.github.io/docs/plans/talks-campaign.md)
- [service-redesign-retrospective-and-playbook.md](/Users/ztatlock/www/ztatlock.github.io/docs/lessons/service-redesign-retrospective-and-playbook.md)

Relevant current implementation/context files if you need to inspect actual
consumers or current semantics:

- [scripts/publication_record.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_record.py)
- [scripts/publication_index.py](/Users/ztatlock/www/ztatlock.github.io/scripts/publication_index.py)
- [scripts/sitebuild/page_projection.py](/Users/ztatlock/www/ztatlock.github.io/scripts/sitebuild/page_projection.py)
- [scripts/page_metadata.py](/Users/ztatlock/www/ztatlock.github.io/scripts/page_metadata.py)
- [scripts/build_pub_inventory.py](/Users/ztatlock/www/ztatlock.github.io/scripts/build_pub_inventory.py)
- [site/pubs/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pubs/index.dj)
- [site/cv/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/cv/index.dj)
- [site/pages/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/pages/index.dj)
- [site/talks/index.dj](/Users/ztatlock/www/ztatlock.github.io/site/talks/index.dj)

What I want from you:

1. Review the requirements document **as a requirements document**, not as a
   disguised schema proposal.
2. Identify missing requirements, hidden assumptions, ambiguities, or places
   where the doc still smuggles in likely solutions too early.
3. Focus especially on whether the requirements fully capture the needs of:
   - individual publication pages
   - the `/pubs/` listing page
   - the CV indexed-publication consumers
   - homepage recent publications
   - collaborator/research-derived consumers
   - internal tooling and analysis/export pipelines
   - likely future curated publication/highlight consumers
4. Be very careful about long-horizon concerns:
   - large future backfill
   - partial or uncertain historical knowledge
   - identifier needs such as DOI/arXiv
   - the relationship to BibTeX
   - compact vs full venue display
   - local-page readiness vs canonical publication existence
   - publication-local talks vs invited/public talks
   - the boundary around Book Chapters and Books
5. Downweight inertia and current implementation convenience.
6. Upweight clarity, future simplicity, robustness, and maintainability.

Important review posture:

- Do **not** assume the current schema is correct just because it exists.
- Do **not** assume the current physical file layout is itself a requirement.
- Do **not** jump straight to proposing a final schema unless doing so is
  necessary to explain a requirements flaw.
- If you mention a likely schema fix, make clear that it is an implication of a
  requirements gap, not the main task.

Please structure your answer as:

1. Findings
   Ordered by severity/importance.
   Focus on requirements-level issues.
2. Open Questions
   Short list of places where the requirements still need a deliberate choice.
3. Overall Assessment
   Is this requirements doc strong enough to serve as the basis for design
   proposals yet, or does it need another refinement pass first?

Please be detailed, sober, and critical.
The goal is to improve the requirements before we draft publication-model
proposals, not to prematurely converge on a schema.
