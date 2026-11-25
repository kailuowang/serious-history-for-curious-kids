---
name: audit-chapter
description: Runs as Stage 4 (right after /review-writing) to audit and lock a chapter's factual grounding, lexicon/rhythm, scope humility, phrase-keyed citations, and ledger/concepts.json before illustration or audio production.
---

# Skill: Audit Chapter (Factual, Lexicon & Citation Lock)

When invoked with a chapter ID (e.g., `/audit-chapter ch01`) right after `/review-writing` (once narrative structure, flow, and writing quality have already been signed off by the independent `writing-reviewer`):

1. **Pass 1 — Fact & Hallucination Check (Prose + Diagrams if present):**
   - Extract and verify every number, date, dimension, ration, place name, artifact, named scholar, and causal claim in `manuscript/<chapter_id>-*.md` (and any `diagrams/<chapter_id>-*.svg` if already created) against `research/<chapter_id>-fact-sheet.md`.
   - Flag and remove or rewrite any unsupported extrapolation (including invented hypothetical numbers, math/unit conversion slips, unverified geographical adjectives, or undocumented outcomes).
   - **Anti-Grand-Claim / Scope-Humility Check:** Flag any unsupported universalizing framework claim (e.g., *"the basic operating kit of early civilization"*, *"the five building blocks of civilization"*, *"every society everywhere ran on..."*) and rewrite it as grounded examples from the chapter's specific time and place.
   - Verify scholarly interpretations and estimates remain transparently framed (e.g., "scholars think," "estimated").

2. **Pass 2 — Lexicon, Tone, Active Voice & Rhythm Linter:**
   - Scan every paragraph (plus any photo captions or diagram labels if present) against `.agents/rules/lexicon-style.md` and `AGENTS.md`:
     - Replace banned Latinate abstractions, vague adjectives (`massive`, `prosperous`, `complex`), LLM transition tics, and exclamation marks.
     - **Flag Unanchored Era & Period Shorthand:** Catch any specialist period label (`Ur III`, `Old Babylonian`, `Uruk III`, `Late Uruk`, `Middle Kingdom`, etc.) that lacks plain dates or human-scale time anchors (*"more than five thousand years ago"*, *"a thousand years later"*) so the reader always knows how old an era is.
     - Ensure concrete units and specialist terms (e.g., *hectare*, *ration*, *shearing*) are explained plainly in-line the first time they appear.
     - Flip stiff passive constructions into active voice with concrete human subjects.
     - Verify only the chapter's newly earned systemic concepts are bolded (consistently on earning + final recap), and flag any **unearned systemic concept** used before being earned in this chapter or `ledger/concepts.json`.
   - Run a Python script to measure per-section and overall word counts (~3,000–3,800 words total) and average sentence length (must stay between **14 and 18 words** overall and per section).

3. **Pass 3 — Phrase-Keyed Citations & Bibliography Check:**
   - Generate or update `research/<chapter_id>-citations.json` mapping verbatim anchor phrases from `manuscript/<chapter_id>-*.md` (grouped by section; plus any `Figure XX.N` diagrams if already built, otherwise populated during `/illustrate-chapter`) to `source_id` keys in `bibliography/sources.json`, with honest `locator` and `verified_page` (`true`/`false`) flags.
   - Run a Python validation script confirming: (a) every `phrase` appears verbatim in `manuscript/<chapter_id>-*.md`, (b) every `source_id` exists in `bibliography/sources.json` with complete bibliographic fields, and (c) every CC-licensed photo in `photos/<chapter_id>-credits.json` (if present) includes a real `creator` name and `license_url`.

4. **Pass 4 — Concept Ledger Update:**
   - Append the chapter's newly introduced bolded systemic concepts (with `chapter`, `term`, and a crisp 1-sentence plain `definition`) to `ledger/concepts.json`, and validate `ledger/concepts.json` parses cleanly as JSON.

5. **Optional Post-Illustration Pass (if `diagrams/<chapter_id>-*.svg` already exist):**
   - Validate every SVG with `xml.etree.ElementTree.parse` (zero invalid HTML entities), confirm zero duplicate `id="..."` attributes across all SVGs in the chapter, and verify every `<style>` rule is scoped to its root `#figXX-N`. (Normally run as Step 4 of `/illustrate-chapter`.)
