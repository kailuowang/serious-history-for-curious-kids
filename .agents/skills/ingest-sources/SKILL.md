---
name: ingest-sources
description: Reads scholarly PDFs or notes in sources/chXX-* and builds a verified causal fact sheet in research/.
---

# Skill: Ingest Chapter Sources

When invoked with a chapter ID (e.g., `/ingest-sources ch01`):

1. Read the chapter's entry in `syllabus/master-outline.md` and inspect all files inside `sources/<chapter_id>-*/`.
2. Extract concrete physical numbers, causal mechanisms, primary-source quotes/artifacts (e.g., specific clay tablets, inscriptions, ledgers), and scholarly debates.
3. Write `research/<chapter_id>-fact-sheet.md` following `.agents/rules/rigor-citations.md`.
4. Do NOT fill gaps from unverified general knowledge. If a key physical detail (e.g., how workers were fed or how stone was moved) is missing from `sources/`, add a `## Missing Source Coverage` section at the bottom listing what needs verification.
