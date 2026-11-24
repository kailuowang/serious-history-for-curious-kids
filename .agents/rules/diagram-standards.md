---
trigger: glob
globs: "diagrams/**/*"
description: Standards for maps, illustrated plates, engineering cutaways, data charts, and system loops, including mandatory visual render verification.
---

# Diagram & Visual Standards

Target a visual cadence of **one focused graphic every 500–650 words** (**4–6 visuals per 3,000-word chapter**) placed right beside the exact prose section that explains each concept.

## 1. Visual Benchmark & Cohesive Book Palette
Aim for **National Geographic cartography**, **David Macaulay 3/4 architectural cutaways**, **DK Eyewitness artifact field plates**, and **Economist-grade editorial infographics**—never coarse geometric placeholders.

Use a consistent warm print-book palette across all chapters (adapting secondary accents to the era's material culture):
- **Parchment / Page Canvas:** `#FBF8F3` (cards `#FFFFFF`, warm callout fills `#FBF3E4`, border strokes `#D8CFC2`)
- **Primary Ink & Muted Ink:** `#241D18` (headings/outlines), `#5E5248` (subtitles/secondary labels)
- **Functional Accents:** River/Water `#2D7DA3`, Grain/Gold `#D9A34A`, Terracotta/Brick `#B85D3B`, Trade/Craft Green `#1E6A52`, Warning/Limit Crimson `#A63D2F`

## 2. Four Visual Types
- **Regional & Trade Maps (`.svg`):** Authentic coastlines, bathymetry contours, shaded-relief mountain chains, natural meandering rivers, lat/long graticule, calibrated scale bar, compass rose, rainfall/resource zones, and custom trade-item icons.
- **Engineering & Tool Cutaways (`.svg` or text-free `.png` + caption):** Dimensional 3/4 architectural cutaways and geological/mechanical cross-sections with human scale silhouettes, layered materials, dimensions in both metric and feet/inches where grounded, and clear force vectors (gravity/compression, tension/shear, water gradient).
- **Artifact Field Plates (`.svg` or text-free `.png` + caption):** Tactile 3D-shaded archaeological objects (bowls, tablets, seals, coins, tools, contracts) with surface textures, soft grounded shadows, and step-by-step callouts showing how each object solved a real human problem.
- **System Loops & Data Charts (`.mmd` + `.svg`):** Color-coded exhibit cards with custom icon medallions, smooth rounded flow channels, concrete plain-language labels on every arrow, and grounded quantitative charts (never invent intermediate data points).

## 3. Mandatory Visual Render-Inspect-Refine Loop
Every SVG in `diagrams/` MUST pass visual inspection before completion:
1. Render to a 1920px-wide PNG via `rsvg-convert -w 1920 <svg> -o <scratch>/<name>-vN.png`.
2. Inspect the rendered PNG visually using `view_file` to diagnose coarse shapes, text clipping, overlapping labels/arrows, weak depth, or unbalanced margins.
3. Run **at least 2 full refinement passes** (`v0` → `v1` → `v2`, and `v3` if needed) until every detail is crisp, legible, and zero-overlap.

## 4. Technical SVG Hygiene & Source Grounding
- **Strict Grounding & Plain Language:** Every date, ration, dimension, and number must trace directly to `research/chXX-fact-sheet.md`. Obey `.agents/rules/lexicon-style.md` (no unexplained jargon, no exclamation marks).
- **Zero-Collision Inline Namespacing:** Set a unique root `id="figXX-N"` (e.g., `fig02-1`), prefix EVERY `<defs>` ID (`linearGradient`, `radialGradient`, `pattern`, `marker`, `filter`, `clipPath`) with `fXXN-`, and scope EVERY `<style>` rule with `#figXX-N ` so all chapter SVGs can be inlined into one HTML page with zero CSS or ID collisions.
- **Valid Strict XML:** Use only XML-safe entities (`&amp;`, `&lt;`, `&gt;`, `&quot;`)—never HTML entities like `&middot;` or `&deg;` (write literal Unicode `·` and `°`). Validate every file with `xml.etree.ElementTree.parse`.
- **Typography Floor:** Use a `960px`-wide `viewBox` (height scaled cleanly to content) with minimum font size `10.5px` so labels remain effortless to read on an iPad and in 8.5×11 print.
