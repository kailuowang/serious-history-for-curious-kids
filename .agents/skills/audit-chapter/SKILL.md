---
name: audit-chapter
description: Runs a 5-pass audit on a chapter's prose and SVG diagrams for factual grounding, lexicon/rhythm, independent narrative flow & causal logic, SVG XML/namespace integrity, and updates ledger/concepts.json.
---

# Skill: Audit Chapter

When invoked with a chapter ID (e.g., `/audit-chapter ch01`):

1. **Pass 1 — Fact & Hallucination Check (Prose + Diagrams):**
   - Extract and verify every number, date, dimension, ration, place name, artifact, and causal claim in BOTH `manuscript/<chapter_id>-*.md` AND `diagrams/<chapter_id>-*.svg` against `research/<chapter_id>-fact-sheet.md`.
   - Flag and remove or rewrite any unsupported extrapolation (including invented hypothetical numbers, unverified geographical adjectives, or undocumented outcomes).
   - Verify scholarly interpretations and estimates remain transparently framed (e.g., "scholars think," "estimated").

2. **Pass 2 — Lexicon, Tone, Active Voice & Rhythm Linter:**
   - Scan every paragraph, photo caption, and diagram label against `.agents/rules/lexicon-style.md` and `AGENTS.md`:
     - Replace banned Latinate abstractions, vague adjectives (`massive`, `prosperous`, `complex`), LLM transition tics, and exclamation marks.
     - **Flag Unanchored Era & Period Shorthand:** Catch any specialist period label (`Ur III`, `Old Babylonian`, `Uruk III`, `Late Uruk`, `Middle Kingdom`, etc.) that lacks plain dates or human-scale time anchors (*"more than five thousand years ago"*, *"a thousand years later"*) so the reader always knows how old an era is.
     - Ensure concrete units and specialist terms (e.g., *hectare*, *ration*, *shearing*) are explained plainly in-line the first time they appear.
     - Flip stiff passive constructions into active voice with concrete human subjects.
     - Verify only the chapter's newly earned systemic concepts are bolded (no rigid numeric cap), and flag any **unearned systemic concept** (such as *"political power"*, *"inflation"*, or *"credit"*) used before being earned in this chapter or `ledger/concepts.json`.
   - Run a Python script to measure per-section and overall word counts (~3,000 words total) and average sentence length (must stay between **14 and 18 words** overall and per section).

3. **Pass 3 — Independent Flow & Causal-Logic Reviewer (Fresh-Eyes Subagent):**
   - Launch a read-only `flow-reviewer` subagent (using `define_subagent` with read-only tools or `research` subagent) to read `manuscript/<chapter_id>-*.md` cold from the perspective of an analytically sharp 9-year-old detective and flag EVERY structural flow hole:
     - **Dropped Mysteries / Orphaned Problems:** Any difficulty, tension, or question introduced in a paragraph that is not answered in the very next beat (or explicitly parked as a section-ending cliffhanger paid off at the start of the next section).
     - **Causal Teleports:** Any transition that skips over an unsolved mechanism with a hand-waving summary phrase (e.g., *"Working together under a shared schedule paid off..."* before explaining how people actually coordinated).
     - **Premature Outcomes / Ordering Flaws / Time Disorientation:** Any consequence stated before its cause, any forward reference to an unexplained mechanism, or any unanchored era name (`Ur III`, `Old Babylonian`, etc.) that leaves a 9-year-old unable to tell how old an event is or how it relates in time to the rest of the chapter.
     - **Weak Unit-to-Unit Bridges:** Any section ending that closes flat instead of handing a live puzzle or trade-off to the next section.
   - Apply targeted structural rewrites to close every flagged flow gap, then re-verify word count, sentence rhythm, and factual grounding.

4. **Pass 4 — SVG XML & Cross-Figure Namespace Check:**
   - Validate every `diagrams/<chapter_id>-*.svg` with `xml.etree.ElementTree.parse` (zero invalid HTML entities).
   - Confirm zero duplicate `id="..."` attributes across all SVGs in the chapter and verify every `<style>` rule is scoped to its root `#figXX-N` so inline HTML embedding causes zero visual leaks.

5. **Pass 5 — Concept Ledger Update:**
   - Append the chapter's newly introduced bolded systemic concepts (with `chapter`, `term`, and a crisp 1-sentence plain `definition`) to `ledger/concepts.json`, and validate `ledger/concepts.json` parses cleanly as JSON.
