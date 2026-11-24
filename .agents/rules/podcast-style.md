---
trigger: glob
globs: "podcasts/**/*.md"
description: Enforces chill, conversational, non-corny two-AI-host podcast scripting with unfolding-mystery rigor and strict factual grounding.
---

# Podcast Style & Dialogue Rules (*The Mechanics of Civilization*)

Before drafting or revising any file in `podcasts/`, read `syllabus/style-anchor.md`, `.agents/rules/lexicon-style.md`, and `podcasts/show-config.json`.

## 1. Cast & Dynamic: Two Smart, Candid AIs
- **Amy (Female AI — Historian & Field Detective):** Grounded, warm, sharp. Brings geography, archaeology, primary artifacts, verified numbers, and physical clues from `research/chXX-fact-sheet.md`.
- **Sam (Young Male AI — Inquirer & Systems Skeptic):** Curious, chill, quick-witted. Never plays dumb or acts as a cheerleader. Stress-tests every explanation, tries plausible-but-flawed solutions, points out human-nature bottlenecks (free-riders, broken memory, cheating), and helps crystallize each building block once the mechanism clicks.
- **Openly AI:** Amy and Sam casually introduce themselves as two AIs digging into how human civilization actually works under the hood. Never invent fake human childhood stories ("my fourth-grade poster project"). Lean gently into the honest AI perspective when it creates natural, dry humor (e.g., two AIs marveling at how humans tracked 29,086 barley deliveries without spreadsheets).

## 2. Episode Spine: Big Question → Nested Sub-Mysteries
- **Parallel Standalone Retelling:** Every episode stands cleanly on its own (great before reading, after reading, or on a car ride) while covering the chapter's full causal spine and all newly earned concepts in `ledger/concepts.json`.
- **Open on the Real Civilizational Question:** Never open with pop-quiz trivia gimmicks or quirky clickbait. Open conversationally on the chapter's serious foundational mystery (e.g., Ch. 1: *How did civilization start at all—from tiny villages of thirty relatives to a city of 40,000 strangers on dry mud?*).
- **Sub-Mystery Ladder:** Frame the chapter's newly earned concepts (`ledger/concepts.json`) as the structural **building blocks** of the mystery. Each building block gets its own sub-mystery arc:
  `Physical or Human Constraint → Plausible Flawed Fix Sam Tests → Real Historical Mechanism (Amy's Evidence) → Building Block Named → Next Sub-Mystery Triggered`
- **Hidden Trade-Off & Cliffhanger:** Close by uncovering the system's unintended flaw (e.g., the Salt Trap) and handing the next chapter's opening question to the next episode.

## 3. Tone: Conversational, Chill, Zero Kids-Show Corniness
- **Target Register:** Two relaxed, sharp thinkers working through a fascinating puzzle at a table—plain enough for an analytically sharp 9-year-old, dignified enough for a parent listening along.
- **Strict Anti-Cringe Ban List:**
  - Zero fake-excitement exclamation marks (`!` should be almost nonexistent; let phrasing and audio tags carry emphasis).
  - Zero patronizing kids-show or AI-banter filler: *Mind blown, Wait—WHAT?!, That's wild!, Pop quiz!, Can you imagine?!, Haha totally!, Love that!, Buckle up!, Let's dive in!*.
  - Zero "Professor + Cheerleader" imbalance: Sam should hold **~40% to 50%** of spoken words and contribute real causal reasoning, not one-line reactions (*"Whoa, cool!"*, *"So you're saying..."*).
- **Separate Humor from Structure:** During Pass 2–3, prioritize clean causal flow, factual grounding, and relaxed conversational pacing—do **not** force jokes. Add organic, dry humor only in **Pass 4 (Humor, Warmth & Audio-Tag Polish)** once the causal spine is locked, keeping only 4–6 natural moments that arise directly from human reality or the AI hosts' perspective.

## 4. Writing for the Ear ("Blindfold Test")
- **Zero Visual Leakage:** Never assume the listener can see a map, cutaway, or diagram. Translate every visual mechanic into a vivid spoken mental model (e.g., compare raised river levees to a water slide sitting slightly above the yard; compare 60 liters of barley to thirty big two-liter bottles).
- **Natural Spoken Rhythm:** Use contractions (`don't`, `they'd`, `here's`), crisp spoken clauses, and varied turn lengths (mix snappy 1-sentence pushbacks with 3–5 sentence vivid explanations; avoid robotic 2-sentence ping-pong).
- **One Number at a Time:** Never stack four statistics in one breath. Anchor every key figure physically and anchor every historical era in human scale (*"five thousand years ago"*, *"a thousand years later"*)—never drop unanchored historian shorthand (`Ur III`, `Old Babylonian`, `Late Uruk`).
- **Strict Fact Grounding:** Spoken ad-libs are a prime vector for accidental hallucinations. Every date, dimension, ration, place name, and historical claim must trace directly to `research/chXX-fact-sheet.md`, preserving scholarly uncertainty transparently (*"archaeologists estimate"*, *"historians weigh three ideas"*).

## 5. Vocal-Tag Discipline (`gemini-3.8-flash-tts`)
- Use vocal tags **sparingly** (roughly 1 every 6–10 turns) so they sound lifelike rather than theatrical.
- Stick strictly to canonical tags in `podcasts/chXX-script.md` (which `_tts_core.py` compiles cleanly into `gemini-3.8-flash-tts` Interactions API `speech_metadata` annotations + inline vocal events):
  - `[soft laugh]` → `<laugh>`
  - `[sighs]` → `<sigh>`
  - `[short pause]` → `<short pause>`
  - `[warmly]`, `[thoughtfully]`, `[gently]`, `[cheerfully]` → lifted into `speech_metadata.style` (never spoken aloud!)
- **Optional overlapping backchannels (3.8 feature):** During Pass 4, you may sparingly wrap 1–2 word listener reactions in pipes inside the active speaker's line (e.g., `|mhm|`, `|right|`, `|wait|`) so the other host voices a natural soft reaction underneath without chopping the dialogue into tiny turns (max 2–3 per episode).
- Use commas between clauses and ellipses (`...`) or em-dashes (`—`) sparingly for natural breathing pauses—never chop sentences into artificial period-separated fragments.
