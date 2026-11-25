---
name: review-writing
description: Runs right after drafting (Stage 3, before factual/citation audit) using an independent Developmental Book Editor subagent focused purely on narrative arc, structural flow, transitions, pacing, vividness, and readability for a sharp 9-year-old.
---

# Skill: Review Writing Quality & Structure (`/review-writing`)

When invoked with a chapter ID (e.g., `/review-writing ch02`) right after `/draft-chapter` and **before** `/audit-chapter`:

## Purpose: Separate Storytelling Craft from Fact-Checking
Do **not** mix copy-editing, citation validation, or JSON linting into this stage. This stage exists for one purpose: making sure the chapter **reads like gripping, crystal-clear narrative nonfiction** (Will Durant's sweep + David Macaulay's physical clarity) rather than a stiff textbook or a checklist of facts stitched together with mechanical transitions.

## Workflow (Iterative Editorial Loop — Minimum 1 Full Revision Cycle)

1. **Define & Launch Independent `writing-reviewer` Subagent (Read-Only):**
   - Launch a fresh-eyes, read-only `writing-reviewer` subagent (via `define_subagent` with `enable_write_tools: false`) to read `manuscript/<chapter_id>-*.md` cold alongside `syllabus/style-anchor.md` (and the closing paragraph of the previous chapter, if `<chapter_id>` > `ch01`).
   - Do **not** distract the reviewer with bibliography schemas or citation JSONs. Instruct it to evaluate purely as a **senior children's-nonfiction developmental editor + an analytically sharp 9-year-old reader**:
     1. **Macro-Arc & Opening Pull:** Does the opening hook immediately immerse the reader in a vivid physical puzzle and set up the whole chapter's journey smoothly—without abruptly hard-cutting or mechanically announcing *"Before X, society had to solve a political mystery"*?
     2. **Transition Smoothness & Causal Flow:** Does every paragraph earn the next paragraph organically? Flag any jarring topic jump, essay-style signpost transition, dropped thread, premature reveal, or causal teleport.
     3. **Show vs. Tell & Scene Vividness:** Flag any "fact-dump" or "textbook summary" paragraph that stacks dates, measurements, and names without a human scene, physical contrast, or detective question pulling the reader forward.
     4. **Section Architecture & Arc Balance:** Do all four sections feel like interlocking acts of **one unified story**? Does each section ending create genuine curiosity that the next section immediately pays off?
     5. **Voice, Warmth & Respect for a 9-Year-Old:** Does the prose match `syllabus/style-anchor.md`—concrete, crisp, respectful, lively, zero condescension, zero stiffness, zero essay-speak?

2. **Rework the Prose:**
   - Apply deep structural and prose rewrites to `manuscript/<chapter_id>-*.md` addressing every major editorial note from the `writing-reviewer` (reordering paragraphs, rebuilding clunky transitions into organic story bridges, unpacking dense fact-dumps into vivid physical scenes, and sharpening narrative momentum)—while staying strictly within verified facts in `research/<chapter_id>-fact-sheet.md`.

3. **Fresh-Eyes Sign-Off Pass:**
   - Send the revised manuscript back to a fresh `writing-reviewer` pass (or message the reviewer with the updated file) to confirm the transitions, pacing, and narrative arc now read effortlessly from first sentence to last, with zero remaining structural jolts.
   - Once the `writing-reviewer` signs off, proceed to **Stage 4 (`/audit-chapter <chapter_id>`)** for rigorous factual grounding, lexicon/rhythm linting, phrase-keyed citations, and `ledger/concepts.json` lock.
