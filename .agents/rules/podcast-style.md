---
trigger: glob
globs: "podcasts/**/*.md"
description: Enforces chill, conversational, non-corny two-host podcast scripting (Amy lead Historian, Sam curious Inquirer) with unfolding-mystery rigor and strict factual grounding.
---

# Podcast Style & Dialogue Rules (*The Mechanics of Civilization*)

Before drafting or revising any file in `podcasts/`, read `syllabus/style-anchor.md`, `.agents/rules/lexicon-style.md`, and `podcasts/show-config.json`.

## 1. Cast & Dynamic: Lead Historian & Curious Inquirer
- **Amy (Lead Historian & Storyteller, ~65%–75% of spoken words):** Grounded, warm, sharp. Carries the primary historical storytelling—geography, archaeology, primary artifacts, verified numbers, physical mechanisms, and scholarly caveats from `research/chXX-fact-sheet.md`.
- **Sam (Inquirer & Conversational Guide, ~25%–35% of spoken words):** Curious, chill, quick-witted. Drives natural transitions, asks the sharp questions a clever listener is thinking, spots practical catches (free-riders, broken memory, trapped drainage), and chimes in with light dry comments. Never acts as an empty cheerleader (*"Whoa, cool!"*), and never artificially recites historian statistics just to split word count evenly.
- **No Fake Backstories, No Machine/AI Talk:** Keep the conversation grounded strictly in history and physical mechanics. Never invent fake human childhood anecdotes (*"my fourth-grade poster project"*), and **never mention the hosts being AIs, machines, or software**—that framing distracts listeners from the story.

## 2. Episode Spine: Big Question → Nested Sub-Mysteries
- **Parallel Standalone Retelling (Book-Matched Scope):** Every episode stands cleanly on its own (great before reading, after reading, or on a car ride) while presenting the **exact same verified content, causal spine, and newly earned concepts** from the manuscript chapter (`ledger/concepts.json`)—just in conversational audio form, without padding episodes with extra side-detours or content beyond the book.
- **Open on the Real Civilizational Question:** Never open with pop-quiz trivia gimmicks or quirky clickbait. Open conversationally on the chapter's serious foundational mystery (e.g., Ch. 1: *How did cities first take hold on a dry mud plain—from tiny villages to forty thousand strangers at Uruk?*).
- **Sub-Mystery Ladder (Examples, Not a Grand Framework):** Frame the chapter's newly earned concepts (`ledger/concepts.json`) as **concrete historical solutions / sample elements** from that specific time and place—never claim they represent *"the building blocks of all civilization"*, *"the universal operating kit"*, or laws that *"cities everywhere"* followed. Each puzzle follows the chapter's own tight causal spine:
  `Physical or Human Puzzle → Constraints → Real Historical Mechanism (Evidence) → Concept Named as an Example → Next Puzzle Triggered`
  Include an intermediate clumsy or failed attempt only when history (and the chapter) genuinely had one (e.g., hollow clay *bullae* before flat tablets, or open tablets before sealed clay envelopes)—never force Sam to invent artificial strawman fixes.
- **Hidden Trade-Off & Cliffhanger:** Close by uncovering the system's unintended flaw (e.g., the Salt Trap) and handing the next chapter's opening question to the next episode.

## 3. Tone: Conversational, Chill, Zero Kids-Show Corniness
- **Target Register:** A sharp historian and a curious conversational partner unpacking a fascinating puzzle at a table—plain enough for an analytically sharp 9-year-old, dignified enough for a parent listening along.
- **Strict Anti-Cringe Ban List:**
  - Zero fake-excitement exclamation marks (`!` should be almost nonexistent; let phrasing and audio tags carry emphasis).
  - Zero patronizing kids-show or filler praise: *Mind blown, Wait—WHAT?!, That's wild!, Pop quiz!, Can you imagine?!, Haha totally!, Love that!, Buckle up!, Let's dive in!*.
  - Healthy Historian/Inquirer Balance: Aim for **Amy ~65%–75% / Sam ~25%–35%**. Keep Sam engaged with real questions, physical catches, transitions, and dry wit rather than empty cheering (*"Whoa, cool!"*, *"So you're saying..."*) or forced 50/50 lecture-swapping.
- **Separate Humor from Structure:** During Pass 2–3, prioritize clean causal flow, factual grounding, and relaxed conversational pacing—do **not** force jokes. Add organic, dry humor only in **Pass 4 (Humor, Warmth & Audio-Tag Polish)** once the causal spine is locked, keeping only 4–6 natural moments that arise directly from human nature and concrete historical reality.

## 4. Writing for the Ear ("Blindfold Test")
- **Zero Visual Leakage:** Never assume the listener can see a map, cutaway, or diagram. Translate every visual mechanic into a vivid spoken mental model (e.g., compare raised river levees to a water slide sitting slightly above the yard; compare 60 liters of barley to thirty big two-liter bottles).
- **Natural Spoken Rhythm:** Use contractions (`don't`, `they'd`, `here's`), crisp spoken clauses, and varied turn lengths (mix Sam's snappy questions/comments with Amy's vivid 3–5 sentence explanations; avoid robotic ping-pong).
- **One Number at a Time:** Never stack four statistics in one breath. Anchor every key figure physically and anchor every historical era in human scale (*"five thousand years ago"*, *"a thousand years later"*)—never drop unanchored historian shorthand (`Ur III`, `Old Babylonian`, `Late Uruk`).
- **Strict Fact Grounding & Scope Humility:** Spoken ad-libs are a prime vector for both accidental hallucinations and sweeping claims. Every date, dimension, ration, place name, and historical claim must trace directly to `research/chXX-fact-sheet.md`, preserving scholarly uncertainty transparently (*"archaeologists estimate"*, *"historians weigh three ideas"*), and never inflating local Sumerian solutions into a universal formula for all civilizations.

## 5. Vocal-Tag Discipline (`gemini-3.8-flash-tts`)
- Use vocal tags **sparingly** (roughly 1 every 6–10 turns) so they sound lifelike rather than theatrical.
- Stick strictly to canonical tags in `podcasts/chXX-script.md` (which `_tts_core.py` compiles cleanly into `gemini-3.8-flash-tts` Interactions API `speech_metadata` annotations + inline vocal events):
  - `[soft laugh]` → `<laugh>`
  - `[sighs]` → `<sigh>`
  - `[short pause]` → `<short pause>`
  - `[warmly]`, `[thoughtfully]`, `[gently]`, `[cheerfully]` → lifted into `speech_metadata.style` (never spoken aloud!)
- **Optional overlapping backchannels (3.8 feature):** During Pass 4, you may sparingly wrap 1–2 word listener reactions in pipes inside the active speaker's line (e.g., `|mhm|`, `|right|`, `|wait|`) so the other host voices a natural soft reaction underneath without chopping the dialogue into tiny turns (max 2–3 per episode).
- Use commas between clauses and ellipses (`...`) or em-dashes (`—`) sparingly for natural breathing pauses—never chop sentences into artificial period-separated fragments.
