---
name: illustrate-chapter
description: Orchestrates a parallel fleet of specialist diagram-illustrator subagents to craft and visually iterate (rsvg-convert + view_file) all 4–6 publication-grade visual plates for a chapter.
---

# Skill: Illustrate Chapter (Parallel Illustrator Fleet)

When invoked with a chapter ID (e.g., `/illustrate-chapter ch02`):

1. **Environment Check (`rsvg-convert` & Fonts):**
   - Check `which rsvg-convert`. If missing, install `librsvg2-bin fonts-liberation fonts-dejavu-core` via `sudo apt-get update -qq && sudo apt-get install -y -qq ...`.
   - Ensure a scratch directory exists for visual iteration renders (e.g., `<artifact_dir>/scratch/` or `/tmp/diagram-renders/<chapter_id>/`).
   - Read `research/<chapter_id>-fact-sheet.md`, `manuscript/<chapter_id>-*.md`, and `.agents/rules/diagram-standards.md`.

2. **Define Specialist Subagent (`diagram-illustrator`):**
   - Define a reusable `diagram-illustrator` subagent with write tools enabled (`enable_write_tools: true`) whose system prompt enforces:
     - Strict source grounding in `research/<chapter_id>-fact-sheet.md` (zero invented numbers, zero exclamation marks, zero unexplained jargon).
     - Strict unique namespace scoping: root `<svg id="figXX-N">`, every `<defs>` ID prefixed `fXXN-`, every `<style>` selector prefixed `#figXX-N `, and strict XML entities only (literal `·` and `°`, never `&middot;` or `&deg;`).
     - **Mandatory Visual Render–Inspect–Refine Loop:**
       1. Draft or inspect baseline SVG → render `rsvg-convert -w 1920 <svg> -o <scratch>/<slug>-v0.png` (or `v1.png`) → visually inspect via `view_file`.
       2. Critique every millimeter for coarse shapes, flat primitives, text clipping, overlapping pills/leaders, weak visual depth, or misaligned proportions.
       3. Execute **at least 2 full visual refinement passes** (`v1` → `v2`, and `v3` if any flaw remains) until the rendered PNG meets National Geographic / David Macaulay / DK Eyewitness print standards.
       4. Validate XML with `python3 -c "import xml.etree.ElementTree as ET; ET.parse('<svg_path>')"`.

3. **Launch Parallel Fleet (1 Dedicated Subagent per Visual Plate):**
   - Invoke one `diagram-illustrator` subagent per planned figure concurrently in a single `invoke_subagent` call (zero file conflicts since each agent owns exactly one `diagrams/<chapter_id>-<slug>.svg` file; if a chapter includes a Mermaid system loop `.mmd`, generate/update that alongside its matching `.svg`).
   - Give each subagent tailored art direction matching the book's unified palette (`#FBF8F3` parchment, `#241D18` ink, `#5E5248` muted ink, era-appropriate accents) and its exact assigned figure number (`Figure X.1` through `Figure X.N`) and namespace prefix (`figXX-N` / `fXXN-`).
   - Wait reactively for all fleet agents to finish (never poll in a loop).

4. **Lead Art-Director Sign-Off & Cross-Figure Integrity Check:**
   - Visually inspect each subagent's final rendered PNG via `view_file`. If any plate still shows overlap, coarseness, or a grounding slip, send targeted feedback to that specific subagent (`send_message`) for one more pass.
   - Run a cross-file Python check across ALL `diagrams/<chapter_id>-*.svg` confirming:
     - Every SVG parses cleanly with `xml.etree.ElementTree.parse`.
     - Zero duplicate `id="..."` values exist across all SVGs in the chapter.
     - Every `<style>` selector is scoped to its own `#figXX-N`.
