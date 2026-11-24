---
name: curate-photos
description: Reviews an audited chapter to spot high-impact places for real-world and museum photographs, sources open-licensed (CC0 / Public Domain / CC-BY) images into photos/, visually verifies each photo, and logs attribution credits.
---

# Skill: Curate Real-World & Museum Photographs

When invoked with a chapter ID (e.g., `/curate-photos ch01`):

1. **Photo-Spotter Review:**
   - Read `manuscript/<chapter_id>-*.md`, `research/<chapter_id>-fact-sheet.md`, and list existing `diagrams/<chapter_id>-*.svg` plates.
   - Identify **4–6 concrete visual moments** where a **real photograph** (not another schematic) gives a 9-year-old immediate tactile reality:
     - *Everyday / Nature Anchors:* Crops, landscapes, rivers, raw materials (e.g., barley stalks, natural bitumen tar, lapis lazuli stone, white salt-crusted topsoil).
     - *Real Museum Artifacts & Monuments:* Authentic surviving objects and ruins discussed in the prose (e.g., beveled-rim bowls, Uruk proto-cuneiform tablets, cracked clay contract envelopes, the standing Ziggurat of Ur).
   - Space photos cleanly away from full-width SVG plates (or pair 2 related small photos in a compact side-by-side strip) so every page feels vibrant without overcrowding.

2. **Open-License Sourcing & Local Archiving (`photos/`):**
   - Source strictly **Public Domain / CC0 / CC-BY / CC-BY-SA** photographs via open APIs (Metropolitan Museum of Art Open Access CC0 API, Wikimedia Commons API using a compliant descriptive `User-Agent` header, Louvre / Smithsonian Open Access). Prefer Public Domain, CC0, or CC-BY over ShareAlike (`CC BY-SA`) whenever an equivalent photo is available.
   - Never rely on fragile external hotlinks in compiled outputs: download local copies to `photos/<chapter_id>-<slug>.jpg` (resized cleanly to ~1000–1200px wide for crisp print/iPad quality with reasonable file size).
   - Record every photo's exact `filename`, `section`, `after_paragraph`, `title`, `caption` (plain, jargon-free, grounded in `research/<chapter_id>-fact-sheet.md`), `creator` (actual photographer or agency name—never just "Wikimedia Commons" for CC-BY/CC-BY-SA files), `institution` and `accession_or_id` (for museum artifacts), `credit` (publication-ready attribution line), `license`, `license_url`, and `source_url` inside `photos/<chapter_id>-credits.json`.

3. **Mandatory Visual Verification (`view_file`):**
   - Inspect **every single downloaded photograph** using `view_file`.
   - Reject and replace any photo that is blurry, watermarked, awkwardly cropped, mismatched in historical era/region, or visually confusing.
   - Confirm each photo's caption matches what is *actually visible* in the photograph and strictly obeys `.agents/rules/lexicon-style.md` (zero unexplained jargon, zero exclamation marks).

4. **Handoff to Typesetting:**
   - Run `/typeset-preview <chapter_id>` so all verified photos from `photos/<chapter_id>-credits.json` are embedded inline (base64 data URIs for offline HTML/artifact portability and crisp high-DPI images for Chrome/Typst PDFs) with subtle museum/photo credit lines.
