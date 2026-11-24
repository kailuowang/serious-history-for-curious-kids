---
name: produce-podcast
description: Produces a standalone, chill two-host (Amy lead Historian, Sam curious Inquirer) companion podcast episode for an audited chapter—spanning blueprint, conversational script, iterative Showrunner flow/engagingness + fact + scope-humility review, dedicated humor/warmth polish, Gemini TTS multi-speaker audio mastering, and audio QA.
---

# Skill: Produce Chapter Podcast (`/produce-podcast`)

When invoked with a chapter ID (e.g., `/produce-podcast ch01`):

## Prerequisites & Context Load
Read:
- `podcasts/show-config.json`
- `.agents/rules/podcast-style.md` and `.agents/rules/lexicon-style.md`
- `syllabus/style-anchor.md` and `syllabus/master-outline.md` (current chapter + next chapter's opening premise)
- `manuscript/<chapter_id>-*.md` (must already be audited via `/audit-chapter`)
- `research/<chapter_id>-fact-sheet.md`
- `ledger/concepts.json` (both prior mastered concepts and this chapter's newly earned concepts)

---

## Pass 0 — One-Time Cast & Theme Check
Inspect `podcasts/show-config.json`.
- If `"status": "pending_audition"`, run the audition script first before producing Episode 1:
  ```bash
  python3 .agents/skills/produce-podcast/scripts/audition_voices.py
  ```
  Present `podcasts/auditions/audition-player.html` (or publish it as a live HTML artifact when running inside Antigravity) so the user can listen to all 4 **Amy & Sam** voice pairs and 3 **Lyria** theme music candidates, pick their favorites, and update `podcasts/show-config.json` (`"status": "locked"`).

---

## Pass 1 — Macro-Mystery & Sub-Mystery Blueprint (**STOP — Approval Gate #1**)
Propose an episode blueprint (~12–15 minutes target runtime, ~1,800–2,250 spoken words at ~150 wpm):
1. **Opening Civilizational Question:** The big serious human puzzle Amy & Sam open with conversationally (zero pop-quiz gimmicks).
2. **Sub-Mystery Ladder (1 Act per newly earned concept in `ledger/concepts.json`):** Matching the manuscript chapter's exact content and causal spine (no extra detours or forced strawmen), map each concrete historical solution (as sample elements from that society, never as a universal civilization formula):
   - `Puzzle & Constraints Opened`
   - `Historical Mechanism & Evidence (plus a real intermediate step only when the chapter has one)`
   - `Exact Moment Concept Is Earned & Named`
   - `Causal Handoff to Next Puzzle`
3. **Prior Concept Callbacks:** Which earlier concepts from `ledger/concepts.json` Amy & Sam build on naturally without re-teaching from scratch.
4. **Hidden Trade-Off & Next-Episode Bridge:** How the closing act uncovers the system's unintended flaw and sets up the next chapter's big question.
5. **Visual-to-Audio Translation Table:** For each diagram/physical mechanism in the chapter (e.g., raised levees, ziggurat reed mats, clay envelopes), write the exact 1-sentence spoken mental model that replaces the visual.
6. **Pronunciation & Time-Anchor Sheet:** Phonetic TTS spellings for tricky ancient/foreign names (e.g., `Uruk` → `OO-rook`, `lugal` → `LOO-gal`, `še-ba` → `SHAY-bah`, `Kushim` → `KOO-sheem`) plus plain human-scale time anchors.

**STOP and wait for user approval on the blueprint before drafting dialogue.**

---

## Pass 2 — Clean Conversational Script Draft (`podcasts/<chapter_id>-script.md`)
Draft the full episode into `podcasts/<chapter_id>-script.md` following `.agents/rules/podcast-style.md`:
- Structure the file with clear act headers matching the blueprint:
  - `## Act 0: Cold Open — <Title>`
  - `## Act 1: <Sub-Mystery 1> (<Concept>)`
  - ...
  - `## Act N: <Hidden Trade-Off & Next Chapter Bridge>`
- Format every spoken turn strictly as `**Amy:** ...` or `**Sam:** ...` (keeping acts roughly 250–480 words each so Gemini native 2-speaker synthesis maintains peak prosody and room tone).
- Focus **100% on conversational chill rhythm, natural Historian/Inquirer roles (Amy ~65%–75% carrying historical detail, Sam ~25%–35% driving transitions, physical catches, and curiosity—with zero machine/AI references and zero sweeping "operating kit" framework claims), causal clarity, and strict factual grounding**. Do **not** force jokes yet—save comedy polish for Pass 4.

---

## Pass 3 — Independent Flow, Engagingness & Fact Review Loop (**Iterates with Pass 2**)
Run a disciplined 2-step editorial loop between Pass 2 and Pass 3 (**minimum 1 full revision cycle, up to 3**) until both reviewers pass cleanly:

1. **Step 3a (First!) — Fresh-Eyes Showrunner Review (Read-Only Subagent):**
   Launch a read-only `podcast-showrunner` subagent (via `define_subagent` or `research` subagent) to read `podcasts/<chapter_id>-script.md` cold from the perspective of an experienced narrative-podcast producer + an analytically sharp 9-year-old listener, and evaluate:
   - **Overall Flow & Engagingness:** Does the episode pull the listener forward effortlessly? Flag any flat textbook stretches, rushed reveals, or saggy middle sections (>60–90 seconds without a fresh constraint or turn in thinking).
   - **Historian / Inquirer Chemistry & Anti-Cringe:** Does Amy carry the historical narrative naturally (~65%–75%) while Sam plays a sharp, natural curious inquirer (~25%–35%) without empty cheerleading (*"Whoa!"*, *"So you're saying..."*) or awkward stat-reciting turns? Also flag **any mention of the hosts being AIs, machines, or software**.
   - **Anti-Grand-Claim / Scope-Humility Check:** Flag any idiosyncratic overstatement treating the chapter's concepts as a universal checklist or grand framework (*"the five building blocks of civilization"*, *"basic operating kit"*, *"cities everywhere"*). Require them to be framed strictly as concrete solutions and examples from this society.
   - **Blindfold Audio Clarity:** Flag any passage that silently assumes a visual diagram, piles too many numbers into one breath, or loses track of historical time.
   - **Unfolding-Mystery Integrity:** Flag any dropped mystery, causal teleport, or concept named before it is earned.

2. **Step 3b — Fact Grounding & Script Telemetry Audit:**
   - Verify **every** number, date, ration, dimension, place name, quote, and causal claim in `podcasts/<chapter_id>-script.md` strictly against `research/<chapter_id>-fact-sheet.md` (catching any ad-libbed details that crept into dialogue).
   - Run the telemetry linter:
     ```bash
     python3 .agents/skills/produce-podcast/scripts/check_script.py <chapter_id>
     ```
     Confirm: ~1,800–2,250 words (~12–15 min), Historian/Inquirer speaking balance cleanly inside target (Amy ~60%–80%, Sam ~20%–40%), varied turn lengths, zero banned corny filler/exclamation marks/unanchored era shorthand, and 100% of chapter concepts from `ledger/concepts.json` covered.

3. **Iterate:** Rewrite `podcasts/<chapter_id>-script.md` to resolve every Showrunner and fact note, then re-run Step 3a + Step 3b until the Showrunner signs off with zero major flow/engagingness issues and `check_script.py` passes cleanly.

---

## Pass 4 — Dedicated Humor, Warmth & Vocal-Tag Polish (**STOP — Approval Gate #2**)
Now that the causal spine and facts are rock-solid:
1. Read through `podcasts/<chapter_id>-script.md` specifically looking for **4–6 natural, dry-humor or warm conversational moments** (organic observations about human nature, relatable modern scale comparisons, or Sam's dry curiosity—zero corny puns, zero fake hype, and zero AI/machine self-references).
2. Add sparse, natural Gemini vocal tags (`[soft laugh]`, `[thoughtfully]`, `[warmly]`, `[sighs]`, `[short pause]`) only where vocal acting genuinely elevates the line (~1 tag per 6–10 turns).
3. Run a quick **Anti-Drift Re-Check**: confirm no added joke smuggled in an unverified historical fact, broke causal flow, or pushed `check_script.py` out of bounds.
4. Compile the structured cue sheet `podcasts/<chapter_id>-script.json` (acts, turns, speaker, display text, phonetic TTS overrides from the Pronunciation Sheet, delivery direction, chapter marker titles).

**STOP and present the final polished script + a short summary of Pass 3–4 improvements for user sign-off before running Gemini TTS.**

---

## Pass 5 — Gemini Multi-Speaker Synthesis & Mastering (`podcasts/<chapter_id>-episode.mp3`)
Run the renderer (auto-loads `GEMINI_API_KEY` from env, `~/.gemini.env`, or `/home/antigravity/upload/*.env`):
```bash
python3 .agents/skills/produce-podcast/scripts/render_podcast.py <chapter_id>
```
What the renderer does automatically:
- Calls **`gemini-3.8-flash-tts`** (per `podcasts/show-config.json`) via the Gemini **Interactions API** in **native 2-speaker mode**, one act per request (~300–480 words each), with per-turn `speech_metadata` annotations, automatic inline vocal-tag conversion (`<laugh>`, `<sigh>`, `<short pause>`), and disk caching in `podcasts/tmp/<chapter_id>/` so partial re-renders only re-bill changed acts.
- Retries transient errors with exponential backoff and supports optional `gemini-3.8-flash-lite-tts` or legacy `gemini-3.1-flash-tts-preview` via `--model`.
- Inserts subtle procedural 2-note wooden marimba chimes between sub-mystery acts, mixes optional Lyria intro/outro themes (`podcasts/assets/theme-intro.mp3`, `theme-outro.mp3`) with gentle crossfades, normalizes final audio to podcast loudness standard (**-16 LUFS**, true peak ≤ -1.5 dBTP) via `ffmpeg`, and embeds ID3 metadata + chapter markers for each sub-mystery.
- Outputs `podcasts/<chapter_id>-episode.mp3`.

---

## Pass 6 — Audio QA & Packaging
1. Inspect the QA report emitted by `render_podcast.py` (duration check, loudness LUFS/TP, unexpected dead-air silences > 2.5s, per-act runtime anomalies that could indicate skipped lines or leaked stage directions).
2. If any act has a mispronunciation or pacing glitch, tweak its phonetic override in `podcasts/<chapter_id>-script.json` and re-render **only** that act (`--only-act <N>`).
3. Update `podcasts/feed.xml` (private RSS feed metadata) and note the finished episode in `README.md` (and optionally add an audio bar/link in `typeset-preview`).
