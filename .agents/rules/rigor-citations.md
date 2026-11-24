---
trigger: glob
globs: "research/**/*.md"
description: Academic grounding, bibliographic tracking, and anti-hallucination rules for chapter fact sheets and citations.
---

# Historical Rigor & Citation Rules

1. **Source-Bound Claims Only:** Every statistic, ration amount, population estimate, architectural dimension, primary-source quote, and date recorded in `research/` must cite the specific file and section in `sources/chXX-*/` plus its `source_id` from `bibliography/sources.json`.
2. **Full Bibliographic Capture (Zero Shorthand-Only Sources):** Whenever a scholar, book, journal article, edited chapter, or primary-text edition is ingested for a chapter, record its complete Chicago-style entry (full author names, co-authors, translators/editors, year, full title, publisher/journal, volume/issue/pages, ISBN/DOI) in `bibliography/sources.json` and append `<chapter_id>` to `chapters_used`.
3. **Honest Page Locators (Never Fabricate Page Numbers):** Record exact verified page numbers, journal page ranges, or primary catalog IDs (e.g., CDLI / museum accession numbers) whenever available (`"verified_page": true`). When working from summary notes or chapter-level excerpts without verified page numbers, record the chapter/section locator honestly and set `"verified_page": false` so print-prep fact-checking knows exactly which pages still need verification.
4. **Verify Direct Quotes & Named Scholars:** Never style a modern paraphrase as a verbatim ancient quotation without noting that distinction in `research/chXX-citations.json`. Never attribute a scholarly claim to a named scholar in prose without verifying that scholar's actual published position.
5. **Flag Scholarly Uncertainty:** Where historians disagree (e.g., beveled-rim bowls as ration scoops vs. bread molds, or internal vs. external ramp geometry at Giza), record both hypotheses clearly rather than flattening them into false certainty.
6. **Required Four Pillars:** Every `chXX-fact-sheet.md` must organize extracted material into:
   - **Energy & Surplus:** Crops, calories, geography, transport limits.
   - **Rules & Statecraft:** Taxes, laws, enforcement, record-keeping.
   - **Markets & Money:** Wages, trade goods, mediums of exchange, bottlenecks.
   - **Engineering & Material Works:** Materials, geometry/forces, labor organization, concrete primary artifacts.
7. **End-of-Chapter Phrase-Keyed Notes (`research/chXX-citations.json`):** Every chapter must maintain a companion `research/chXX-citations.json` mapping verbatim anchor phrases from `manuscript/chXX-*.md` (plus every `Figure XX.N` diagram) to `bibliography/sources.json` IDs, keeping the main text uncluttered for a 9-year-old reader while maintaining full scholarly traceability.
