# Local Antigravity Handoff — Companion Podcast (`/produce-podcast`)

Everything decided during strategy & pipeline design is already committed into this repository so your local Antigravity environment can pick up seamlessly with your local `GEMINI_API_KEY`.

---

## Locked-In Design Decisions

1. **Format & Role:** **Two-Host Mystery Lab**, **Parallel Standalone Retelling** (~12–15 min, ~1,800–2,250 spoken words per chapter).
2. **Hosts (Candidly Two AIs):**
   - **Amy** — Female AI, Historian & Field Detective (geography, archaeology, primary artifacts, verified numbers).
   - **Sam** — Young Male AI, Inquirer & Systems Skeptic (stress-tests explanations, tests flawed fixes, spots human-nature traps—never a cheerleader).
   - They openly introduce themselves as two AIs digging into how human civilization works under the hood.
3. **Tone & Narrative Spine:**
   - **Conversational, chill, curious, with light dry humor**—zero corny children's-podcast hype or pop-quiz gimmicks.
   - Open on the chapter's big civilizational question (e.g., Ch. 1: *How did civilization start at all?*), with each newly earned concept in `ledger/concepts.json` framed as a nested **sub-mystery / building block**.
4. **Unified Skill (`/produce-podcast chXX`):**
   - **Pass 0:** One-time voice & music audition (`status: "pending_audition"` in `podcasts/show-config.json`).
   - **Pass 1:** Macro-Mystery & Sub-Mystery Blueprint (**Approval Gate #1**).
   - **Pass 2:** Clean conversational dialogue draft (`podcasts/chXX-script.md`)—no forced jokes yet.
   - **Pass 3:** Independent **Flow, Engagingness & Fact Review loop** (fresh-eyes Showrunner subagent checks engagingness/flow *first*, then strict fact audit + `check_script.py` telemetry; iterates with Pass 2 until clean).
   - **Pass 4:** Dedicated **Humor, Warmth & Vocal-Tag Polish** on top of the locked script (**Approval Gate #2**), compiling `podcasts/chXX-script.json`.
   - **Pass 5:** Gemini native 2-speaker TTS synthesis + `ffmpeg` mastering (`-16 LUFS`, optional Lyria intro/outro fade, procedural wooden marimba chimes between sub-mysteries, MP3 chapter markers).
   - **Pass 6:** Automated Audio QA (`silencedetect`, `volumedetect`, per-act WPM anomaly check).
5. **TTS & Music Stack:**
   - **Voices:** Configured for `gemini-3.1-flash-tts-preview` in `podcasts/show-config.json`.
   - **Important heads-up:** Google schedules `gemini-3.1-flash-tts-preview` shutdown on **December 18, 2026**, replaced by **`gemini-3.8-flash-tts`** (GA, lower cost, same 30 prebuilt voices, plus overlapping backchanneling and WAV output). Both `audition_voices.py` and `render_podcast.py` already support **both** schemas natively—just pass `--model gemini-3.8-flash-tts` or update `tts.model` in `podcasts/show-config.json` whenever you want to compare or switch.
   - **Music:** `lyria-3-clip-preview` via the exact same `google-genai` SDK and `GEMINI_API_KEY`.

---

## Files Added in This Setup

- `.agents/rules/podcast-style.md` — Tone, cast dynamic, anti-cringe ban list, blindfold audio rules, vocal tags.
- `.agents/skills/produce-podcast/SKILL.md` — Full 6-pass `/produce-podcast` author skill.
- `.agents/skills/produce-podcast/scripts/_tts_core.py` — Shared Gemini TTS (3.1 & 3.8), Lyria clip generator, and pure-Python wooden marimba chime synthesizer.
- `.agents/skills/produce-podcast/scripts/audition_voices.py` — Renders all 4 Amy & Sam voice pairs + 3 Lyria theme music candidates + offline `podcasts/auditions/audition-player.html`.
- `.agents/skills/produce-podcast/scripts/check_script.py` — Script telemetry linter (word count, runtime, speaker balance, turn-length variance, banned phrases, concept coverage).
- `.agents/skills/produce-podcast/scripts/render_podcast.py` — Full multi-act Gemini TTS renderer, `ffmpeg` `-16 LUFS` masterer with MP3 chapter markers, and Audio QA.
- `podcasts/show-config.json` — Show config (currently `"status": "pending_audition"`).

---

## Next Steps in Your Local Antigravity Session

1. Pull latest `main` and install local dependencies (one-time):
   ```bash
   git pull
   pip install --upgrade google-genai
   # Make sure ffmpeg is installed (e.g., brew install ffmpeg / sudo apt-get install ffmpeg)
   ```
2. Ensure `GEMINI_API_KEY` is exported in your local shell (or saved in a gitignored `.env` or `~/.gemini.env`).
3. Paste this starter prompt directly into your local Antigravity session:

> Read `podcasts/HANDOFF-LOCAL-ANTIGRAVITY.md` and `podcasts/show-config.json`. First, run `.agents/skills/produce-podcast/scripts/audition_voices.py` using my local `GEMINI_API_KEY` to generate the 4 Amy & Sam voice-pair auditions and 3 Lyria theme music options, and open `podcasts/auditions/audition-player.html` so I can listen and pick my favorites. Once I choose the voice pair and music theme, lock them into `podcasts/show-config.json` and start `/produce-podcast ch01` at Pass 1 (Blueprint).
