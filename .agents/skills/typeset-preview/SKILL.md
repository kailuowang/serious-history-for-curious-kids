---
name: typeset-preview
description: Compiles an audited chapter, synced concept callouts, and all inline-placed SVG plates into an offline iPad/print HTML reader (or Typst PDF) plus a live interactive Antigravity preview artifact.
---

# Skill: Typeset Chapter Preview

When invoked with a chapter ID (e.g., `/typeset-preview ch01`):

1. **Check Toolchain & Inputs:**
   - Read `manuscript/<chapter_id>-*.md`, `ledger/concepts.json` (filtering concepts for `<chapter_id>`), all `diagrams/<chapter_id>-*.svg` plates, `photos/<chapter_id>-credits.json` (plus local `photos/<chapter_id>-*.jpg` files, if curated), `research/<chapter_id>-citations.json`, and `bibliography/sources.json`.
   - Check if `typst` or `google-chrome` is installed (`which typst google-chrome`).

2. **Layout & Content Assembly Rules (Applies to Both PDF & HTML):**
   - **Inline Visual Placement:** Embed all 4–6 SVG plates (`diagrams/<chapter_id>-*.svg`) directly beside the exact prose paragraphs that introduce them (strip fixed root `width`/`height` so SVGs scale fluidly; preserve each figure's unique `#figXX-N` scope and `fXXN-` `<defs>` IDs; verify zero duplicate SVG IDs in the final output).
   - **Curated Real-World & Museum Photographs:** Embed verified local images from `photos/<chapter_id>-*.jpg` (base64-inlined in standalone HTML so offline iPad viewing never breaks) as compact **museum photo strips (2-up)** or clean inset cards with plain-English captions and discrete license/source credits from `photos/<chapter_id>-credits.json`.
   - **Synced Concept Callouts:** Automatically insert a **"New Mechanic Earned"** callout box immediately after the paragraph where each bolded concept from `ledger/concepts.json` is first introduced, plus a **"Chapter Mechanics Toolkit"** summary card at the end of the chapter.
   - **End-of-Chapter Phrase-Keyed Notes & Sources (`#notes`):** Keep the main chapter prose completely free of superscript footnote clutter. Immediately after `#toolkit`, render a crisp, book-styled **Notes & Sources** section compiled from `research/<chapter_id>-citations.json`, `bibliography/sources.json`, and `photos/<chapter_id>-credits.json`, containing:
     1. **Phrase-Keyed Notes** grouped by chapter section (bold anchor phrase from the prose + plain scholarly note & short author-year citations),
     2. **Figure & Data Sources** for every SVG plate,
     3. **Photograph & Museum Credits** (with creator names, museum accession numbers, and CC license links), and
     4. **Selected Bibliography** (alphabetized Chicago-style references for the chapter).
   - **Book Typography:** Generous margins, readable book serif prose (`Iowan Old Style` / `Palatino` / `Georgia`, 18px screen / 10.5–12pt print, ~1.5×–1.6× screen / 1.43× print line spacing), drop-cap opening paragraph per section, and `break-inside: avoid` on every callout box, photo strip, figure, and note item.

3. **Build Targets:**
   - **Print PDF (`build/<chapter_id>-full.pdf`):** If `typst` is installed, compile via Typst; otherwise render via headless `google-chrome --headless=new --no-pdf-header-footer --print-to-pdf=...` with running headers and page numbers, and visually verify page breaks with `view_file`.
   - **Offline Standalone HTML (`build/<chapter_id>-preview.html`):** Always build a 100% self-contained offline HTML reader (inline CSS + inline SVGs + base64-inlined photos, zero external CDN dependencies) with sticky section jump links (including `Toolkit` and `Notes`), `@page` print CSS, and a **Print / Save PDF** button.
   - **Live Antigravity Side-Pane Artifact:** When running inside Antigravity, also publish a user-facing standalone HTML artifact (`<artifact_dir>/<chapter_id>-preview.html` with `UserFacing: true`, `RequestFeedback: false`, Tailwind semantic theme variables, `A−`/`A+` co-reading font-size controls, section jump bar, and Print/PDF button) following the `generative_ui` skill.
