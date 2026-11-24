---
trigger: glob
globs: "research/**/*.md"
description: Academic grounding and anti-hallucination rules for chapter fact sheets.
---

# Historical Rigor & Extraction Rules

1. **Source-Bound Claims Only:** Every statistic, ration amount, population estimate, architectural dimension, and date recorded in `research/` must cite the specific file and section in `sources/chXX-*/`.
2. **Flag Scholarly Uncertainty:** Where historians disagree (e.g., exact internal vs. external ramp geometry at Giza), record both hypotheses clearly rather than flattening them into false certainty.
3. **Required Four Pillars:** Every `chXX-fact-sheet.md` must organize extracted material into:
   - **Energy & Surplus:** Crops, calories, geography, transport limits.
   - **Rules & Statecraft:** Taxes, laws, enforcement, record-keeping.
   - **Markets & Money:** Wages, trade goods, mediums of exchange, bottlenecks.
   - **Engineering & Material Works:** Materials, geometry/forces, labor organization, concrete primary artifacts.
