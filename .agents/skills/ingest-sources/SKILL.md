---
name: ingest-sources
description: Reads scholarly PDFs or notes in sources/chXX-* and builds a verified causal fact sheet in research/ plus full bibliographic entries in bibliography/sources.json.
---

# Skill: Ingest Chapter Sources

When invoked with a chapter ID (e.g., `/ingest-sources ch01`):

1. Read the chapter's entry in `syllabus/master-outline.md` and inspect all files inside `sources/<chapter_id>-*/`.
2. **Register Full Bibliography (`bibliography/sources.json`):** For every book, journal article, edited-volume chapter, excavation report, or primary-source edition referenced in `sources/<chapter_id>-*/`, verify and add (or update `chapters_used` on) its complete Chicago-style entry in `bibliography/sources.json` (full authors/co-authors, translators/editors, year, full title, publisher/journal, volume/issue/pages, ISBN/DOI). Never leave bare last names or partial titles unregistered.
3. Extract concrete physical numbers, causal mechanisms, primary-source quotes/artifacts (with exact museum/catalog IDs like CDLI or accession numbers when available), and scholarly debates—attaching exact `source_id` keys and verified page/chapter locators to every bullet.
4. Write `research/<chapter_id>-fact-sheet.md` following `.agents/rules/rigor-citations.md`.
5. Do NOT fill gaps from unverified general knowledge, and NEVER invent page numbers. If a key physical detail (e.g., how workers were fed or how stone was moved) is missing from `sources/`, add a `## Missing Source Coverage` section at the bottom listing what needs verification.
