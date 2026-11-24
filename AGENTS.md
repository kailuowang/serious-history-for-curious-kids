# Project: The Mechanics of Civilization

## Mission
Write a 500-page (~126,000-word, 42-chapter) history of human civilization for an analytically sharp 9-year-old reader.
Our goal is Will and Ariel Durant's civilizational sweep—how societies organize rules, how economies and money operate, and how monumental engineering works—written in crisp, concrete, everyday language with zero condescension and zero unexplained academic jargon.

## Non-Negotiable Principles
1. **Decouple Conceptual Depth from Lexical Complexity:** Explain adult structural mechanisms (caloric surplus, taxation, contract enforcement, division of labor, load-bearing physics, credit) using concrete everyday nouns and active verbs. Never simplify the *mechanism*; simplify the *words*.
2. **Strict Source Grounding:** Never invent historical numbers, wages, rations, or dates from parametric memory. Every factual claim in `manuscript/` and every label/metric in `diagrams/` must trace directly to `research/chXX-fact-sheet.md`. Avoid unverified pop-history tropes (e.g., sudden single-mutation "Cognitive Revolutions" or teleological myths).
3. **Continuity via the Concept Ledger:** Before planning or drafting any chapter, inspect `ledger/concepts.json`. Build explicitly on mechanics already taught in earlier chapters; never re-explain a mastered concept from scratch, and never use an unintroduced systemic concept without earning it first.
4. **Physical & Quantitative Specificity:** Replace vague adjectives ("massive," "prosperous," "complex") with physical quantities ("2.3 million limestone blocks," "two liters of barley per day," "a six-week donkey caravan").
5. **Visual Cadence & Render-Verified Craftsmanship:** Pair prose with **4–6 focused visual plates per chapter** (~1 graphic every 500–650 words—regional map, engineering/tool cutaways, artifact field guide, system loop, data chart) placed right beside the prose they explain. Never ship uninspected, coarse single-pass SVGs; every plate must pass an iterative `rsvg-convert` → visual inspection refinement loop via a dedicated illustrator subagent fleet.
6. **Unfolding-Mystery Causal Flow:** Structure every chapter and every section as a tightly linked mystery chain (**Physical Problem → Clues/Constraints → Mechanism/Payoff → Next Problem**). Never introduce a difficulty or question and silently teleport past it with a summary transition (e.g., "Working together paid off…"); every opened question must be resolved immediately or explicitly handed off to the very next section.

## Standard 7-Stage Chapter Pipeline
1. **`/ingest-sources chXX`** — Register full bibliographic entries in `bibliography/sources.json` and extract verified numbers, causal chains, primary artifacts, scholarly debates, and missing coverage into `research/chXX-fact-sheet.md`.
2. **`/draft-chapter chXX`** — Propose a 4-section blueprint (~750 words/section, explicit **Mystery Chain Map**, newly earned bolded concepts, 4–6 visual plate specs) and **stop for user approval** before drafting prose into `manuscript/chXX-<slug>.md`.
3. **`/illustrate-chapter chXX`** — Launch a parallel specialist illustrator fleet (one subagent per figure) to craft and visually iterate (`rsvg-convert` → `view_file` across ≥2 passes) every plate in `diagrams/chXX-*.svg` (and `.mmd` for system loops).
4. **`/audit-chapter chXX`** — Run a 6-pass audit: (1) fact & hallucination check on prose + diagrams, (2) lexicon/tone/active-voice/rhythm check (14–18 words/sentence), (3) **independent Flow & Causal-Logic Reviewer** subagent checking for dropped mysteries, causal teleports, and smooth unit-to-unit progression, (4) SVG XML & cross-figure namespace integrity check, (5) phrase-keyed citations & bibliography validation (`research/chXX-citations.json` + `bibliography/sources.json`), and (6) `ledger/concepts.json` update.
5. **`/curate-photos chXX`** — Review the audited chapter to spot 4–6 high-impact places for real-world and museum photographs (crops, landscapes, raw materials, surviving artifacts/monuments), download verified open-licensed (CC0 / Public Domain / CC-BY) copies into `photos/chXX-*.jpg` + `photos/chXX-credits.json` (with creator names, museum accession numbers, and license URLs), and visually inspect every photo via `view_file`.
6. **`/typeset-preview chXX`** — Compile the chapter, synced concept callouts, inline-placed SVG plates, curated real-world photographs, and end-of-chapter phrase-keyed **Notes & Sources** into `build/chXX-preview.html` (offline iPad/print copy) and `build/chXX-full.pdf` (via Typst or headless Chrome), plus a live interactive side-pane preview artifact when running in Antigravity.
7. **`/produce-podcast chXX`** — Produce a chill, standalone two-host (**Amy & Sam**) companion podcast episode (~12–15 min) following `.agents/rules/podcast-style.md`: macro-question + nested sub-mystery blueprint (Approval Gate #1), conversational script draft, iterative fresh-eyes Showrunner flow/engagingness + fact + scope-humility audit loop, dedicated dry-humor & vocal-tag polish pass (Approval Gate #2), Gemini multi-speaker TTS synthesis + `ffmpeg` `-16 LUFS` mastering with chapter markers, and Audio QA into `podcasts/chXX-episode.mp3`.

## Cross-Agent Compatibility
Keep `AGENTS.md`, `.agents/rules/`, and `.agents/skills/` self-contained so both Antigravity and CLI agents (e.g., Claude Code) share identical workspace state.

## Repository Map
- `syllabus/master-outline.md` — 42-chapter architecture across 6 historical parts.
- `syllabus/style-anchor.md` — Gold-standard prose voice reference. Read before writing any prose.
- `ledger/concepts.json` — Cumulative registry of systemic concepts introduced by chapter.
- `bibliography/sources.json` — Master Chicago-style bibliography registry across all chapters.
- `sources/chXX-*/` — Raw scholarly PDFs, excerpts, and primary-source translations.
- `research/chXX-fact-sheet.md` — Verified numbers, causal chains, and primary artifacts.
- `research/chXX-citations.json` — End-of-chapter phrase-keyed notes and diagram source mappings linked to `bibliography/sources.json`.
- `manuscript/chXX-*.md` — Final ~3,000-word chapters.
- `diagrams/chXX-*.svg` (and `.mmd`) — Publication-grade regional maps, cutaways, artifact plates, data charts, and system loops.
- `photos/chXX-*.jpg` (and `chXX-credits.json`) — Visually verified open-licensed real-world & museum photographs with full attribution metadata.
- `build/` — Compiled Typst/Chrome PDFs and standalone offline HTML chapter previews for iPad or print co-reading.
- `podcasts/` — Companion two-host (**Amy & Sam**) podcast scripts (`chXX-script.md`/`.json`), show config (`show-config.json`), theme music assets, and mastered episodes (`chXX-episode.mp3`).
